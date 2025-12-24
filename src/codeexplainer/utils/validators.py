from typing import Any
"""
Validation utilities for CodeExplainer

Handles input validation and error checking for various
parts of the system.
"""

import os
from pathlib import Path
from typing import Optional, Union
from loguru import logger


def validate_project_path(project_path: Path) -> bool:
    """
    Validate that a path is a valid project directory.
    
    Args:
        project_path: Path to validate
        
    Returns:
        True if valid, raises exception otherwise
        
    Raises:
        ValueError: If path is not valid
    """
    if not project_path:
        raise ValueError("Project path cannot be empty")
    
    if not project_path.exists():
        raise ValueError(f"Project path does not exist: {project_path}")
    
    if not project_path.is_dir():
        raise ValueError(f"Project path is not a directory: {project_path}")
    
    if not os.access(project_path, os.R_OK):
        raise ValueError(f"No read permission for project path: {project_path}")
    
    # Check if directory is empty
    try:
        contents = list(project_path.iterdir())
        if not contents:
            logger.warning(f"Project directory is empty: {project_path}")
    except Exception as e:
        raise ValueError(f"Cannot read project directory: {e}")
    
    logger.info(f"Validated project path: {project_path}")
    return True


def validate_output_path(output_path: Path) -> bool:
    """
    Validate that a path is suitable for output.
    
    Args:
        output_path: Path to validate
        
    Returns:
        True if valid, raises exception otherwise
        
    Raises:
        ValueError: If path is not valid
    """
    if not output_path:
        raise ValueError("Output path cannot be empty")
    
    # Check if parent directory exists and is writable
    parent = output_path.parent
    if not parent.exists():
        try:
            parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ValueError(f"Cannot create output directory: {e}")
    
    if not os.access(parent, os.W_OK):
        raise ValueError(f"No write permission for output directory: {parent}")
    
    # Check if output path itself is writable (if it exists)
    if output_path.exists():
        if output_path.is_file():
            raise ValueError(f"Output path is a file, not a directory: {output_path}")
        elif output_path.is_dir():
            if not os.access(output_path, os.W_OK):
                raise ValueError(f"No write permission for output directory: {output_path}")
    
    logger.info(f"Validated output path: {output_path}")
    return True


def validate_language_support(language: str) -> bool:
    """
    Validate that a language is supported.
    
    Args:
        language: Language name to validate
        
    Returns:
        True if supported, False otherwise
    """
    from ..parsers import get_language_mapping
    
    language_mapping = get_language_mapping()
    
    # Check exact match first
    if language in language_mapping:
        return True
    
    # Check case-insensitive match
    language_lower = language.lower()
    for supported_lang in language_mapping.keys():
        if supported_lang.lower() == language_lower:
            return True
    
    logger.warning(f"Language not supported: {language}")
    return False


def validate_file_size(file_path: Path, max_size_mb: int = 10) -> bool:
    """
    Validate that a file is not too large.
    
    Args:
        file_path: Path to file
        max_size_mb: Maximum allowed size in megabytes
        
    Returns:
        True if file size is acceptable, False otherwise
    """
    try:
        if not file_path.exists():
            return False
        
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        
        if file_size_mb > max_size_mb:
            logger.warning(f"File too large: {file_path} ({file_size_mb:.1f} MB)")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Could not check file size for {file_path}: {e}")
        return False


def validate_configuration(config: dict[str, Any]) -> bool:
    """
    Validate configuration dictionary.
    
    Args:
        config: Configuration dictionary to validate
        
    Returns:
        True if valid, raises exception otherwise
        
    Raises:
        ValueError: If configuration is invalid
    """
    if not isinstance(config, dict):
        raise ValueError("Configuration must be a dictionary")
    
    # Validate analysis section
    analysis = config.get("analysis", {})
    if "max_file_size_mb" in analysis:
        max_size = analysis["max_file_size_mb"]
        if not isinstance(max_size, (int, float)) or max_size <= 0:
            raise ValueError("max_file_size_mb must be a positive number")
    
    if "timeout_seconds" in analysis:
        timeout = analysis["timeout_seconds"]
        if not isinstance(timeout, int) or timeout <= 0:
            raise ValueError("timeout_seconds must be a positive integer")
    
    # Validate output section
    output = config.get("output", {})
    if "generate_audio_scripts" in output:
        if not isinstance(output["generate_audio_scripts"], bool):
            raise ValueError("generate_audio_scripts must be a boolean")
    
    if "max_explanation_length" in output:
        max_len = output["max_explanation_length"]
        if not isinstance(max_len, int) or max_len <= 0:
            raise ValueError("max_explanation_length must be a positive integer")
    
    # Validate file filters section
    file_filters = config.get("file_filters", {})
    for key in ["include_patterns", "exclude_patterns"]:
        if key in file_filters:
            patterns = file_filters[key]
            if not isinstance(patterns, list):
                raise ValueError(f"{key} must be a list")
            if not all(isinstance(p, str) for p in patterns):
                raise ValueError(f"All {key} must be strings")
    
    if "max_depth" in file_filters:
        max_depth = file_filters["max_depth"]
        if max_depth is not None and (not isinstance(max_depth, int) or max_depth < 0):
            raise ValueError("max_depth must be a non-negative integer or None")
    
    logger.info("Configuration validation passed")
    return True


def validate_explanation_content(content: str) -> bool:
    """
    Validate that explanation content is appropriate.
    
    Args:
        content: Explanation content to validate
        
    Returns:
        True if content is valid, False otherwise
    """
    if not content or not content.strip():
        logger.warning("Explanation content is empty")
        return False
    
    if len(content) < 10:
        logger.warning("Explanation content is too short")
        return False
    
    if len(content) > 10000:
        logger.warning("Explanation content is too long")
        return False
    
    # Check for common issues
    issues = []
    
    if content.count('(') != content.count(')'):
        issues.append("mismatched parentheses")
    
    if content.count('[') != content.count(']'):
        issues.append("mismatched brackets")
    
    if content.count('{') != content.count('}'):
        issues.append("mismatched braces")
    
    if issues:
        logger.warning(f"Content validation issues: {', '.join(issues)}")
    
    return True


def sanitize_path_component(component: str) -> str:
    """
    Sanitize a path component for safe use in filenames.
    
    Args:
        component: Path component to sanitize
        
    Returns:
        Sanitized path component
    """
    if not component:
        return "unnamed"
    
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    sanitized = component
    for char in invalid_chars:
        sanitized = sanitized.replace(char, '_')
    
    # Remove control characters
    sanitized = ''.join(char for char in sanitized if ord(char) >= 32)
    
    # Trim whitespace
    sanitized = sanitized.strip()
    
    # Ensure it's not empty
    if not sanitized:
        sanitized = "unnamed"
    
    # Limit length
    if len(sanitized) > 50:
        sanitized = sanitized[:50]
    
    return sanitized