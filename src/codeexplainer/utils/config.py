from typing import Any
"""
Configuration management for CodeExplainer

Handles loading and validating configuration from YAML files
and command-line arguments.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from loguru import logger


class Config:
    """Configuration manager with defaults and validation."""
    
    DEFAULT_CONFIG = {
        "analysis": {
            "max_file_size_mb": 10,
            "timeout_seconds": 30,
            "override_language": None,
            "include_comments": True,
            "include_docstrings": True,
        },
        "output": {
            "generate_audio_scripts": True,
            "explanation_style": "simple",
            "include_line_numbers": False,
            "max_explanation_length": 2000,
        },
        "file_filters": {
            "include_patterns": [],
            "exclude_patterns": [],
            "max_depth": None,
            "skip_hidden": True,
        },
        "templates": {
            "use_custom_templates": False,
            "template_directory": None,
        },
        "logging": {
            "level": "INFO",
            "format": "{time:HH:mm:ss} | {level: <8} | {message}",
        },
    }
    
    def __init__(self, config_dict: Optional[dict[str, Any]] = None):
        """
        Initialize configuration with defaults and overrides.
        
        Args:
            config_dict: Dictionary with configuration overrides
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_dict:
            self._merge_config(self.config, config_dict)
        
        # Extract sections for easy access
        self.analysis = self.config["analysis"]
        self.output = self.config["output"]
        self.file_filters = self.config["file_filters"]
        self.templates = self.config["templates"]
        self.logging = self.config["logging"]
    
    def _merge_config(self, base: dict[str, Any], override: dict[str, Any]) -> None:
        """
        Recursively merge configuration dictionaries.
        
        Args:
            base: Base configuration dictionary
            override: Dictionary with override values
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-separated key.
        
        Args:
            key: Dot-separated key (e.g., 'analysis.max_file_size_mb')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def to_dict(self) -> dict[str, Any]:
        """Return the full configuration as a dictionary."""
        return self.config.copy()


def load_config(config_file: Optional[Path] = None) -> dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    config_dict = {}
    
    # Load default config from package
    default_config_path = Path(__file__).parent.parent / "config" / "default.yaml"
    
    if default_config_path.exists():
        try:
            with open(default_config_path, "r", encoding="utf-8") as f:
                config_dict = yaml.safe_load(f) or {}
            logger.info(f"Loaded default config from {default_config_path}")
        except Exception as e:
            logger.warning(f"Could not load default config: {e}")
    
    # Load user config file if provided
    if config_file and config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                user_config = yaml.safe_load(f) or {}
            
            # Merge user config with default
            _merge_dicts(config_dict, user_config)
            logger.info(f"Loaded user config from {config_file}")
            
        except Exception as e:
            logger.warning(f"Could not load user config from {config_file}: {e}")
    
    # Apply environment variable overrides
    env_config = _load_env_config()
    if env_config:
        _merge_dicts(config_dict, env_config)
        logger.info("Applied environment variable configuration")
    
    return config_dict


def _merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> None:
    """
    Recursively merge two dictionaries.
    
    Args:
        base: Base dictionary (modified in place)
        override: Dictionary to merge into base
    """
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _merge_dicts(base[key], value)
        else:
            base[key] = value


def _load_env_config() -> dict[str, Any]:
    """
    Load configuration from environment variables.
    
    Environment variables should be prefixed with CODEEXPLAINER_
    and use double underscores for nested keys.
    
    Returns:
        Configuration dictionary from environment variables
    """
    env_config = {}
    prefix = "CODEEXPLAINER_"
    
    for env_var, value in os.environ.items():
        if env_var.startswith(prefix):
            # Convert environment variable to config key
            config_key = env_var[len(prefix):].lower().replace("__", ".")
            
            # Try to convert value to appropriate type
            converted_value = _convert_env_value(value)
            
            # Set nested value
            keys = config_key.split(".")
            current = env_config
            
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            current[keys[-1]] = converted_value
    
    return env_config


def _convert_env_value(value: str) -> Any:
    """
    Convert environment variable string to appropriate Python type.
    
    Args:
        value: Environment variable value as string
        
    Returns:
        Converted value
    """
    # Handle boolean values
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    
    # Handle numeric values
    try:
        if "." in value:
            return float(value)
        else:
            return int(value)
    except ValueError:
        pass
    
    # Handle lists (comma-separated)
    if "," in value:
        return [item.strip() for item in value.split(",")]
    
    # Return as string
    return value


def save_config(config: dict[str, Any], output_file: Path) -> None:
    """
    Save configuration to a YAML file.
    
    Args:
        config: Configuration dictionary
        output_file: Path to save the configuration
    """
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=True)
        
        logger.info(f"Configuration saved to {output_file}")
        
    except Exception as e:
        logger.error(f"Failed to save configuration: {e}")
        raise