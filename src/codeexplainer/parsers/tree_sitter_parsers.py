from typing import Any
"""
Tree-sitter parser management for CodeExplainer

Handles initialization and management of tree-sitter parsers
for different programming languages.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import tree_sitter
from tree_sitter import Language, Parser
from loguru import logger


# Language mapping configuration
LANGUAGE_MAPPING = {
    "python": {
        "extensions": [".py", ".pyx", ".pyi"],
        "parser_name": "python",
        "build_command": "tree-sitter-python",
    },
    "javascript": {
        "extensions": [".js", ".jsx", ".mjs"],
        "parser_name": "javascript",
        "build_command": "tree-sitter-javascript",
    },
    "typescript": {
        "extensions": [".ts", ".tsx"],
        "parser_name": "typescript",
        "build_command": "tree-sitter-typescript",
    },
    "java": {
        "extensions": [".java"],
        "parser_name": "java",
        "build_command": "tree-sitter-java",
    },
    "c": {
        "extensions": [".c", ".h"],
        "parser_name": "c",
        "build_command": "tree-sitter-c",
    },
    "cpp": {
        "extensions": [".cpp", ".cxx", ".cc", ".hpp", ".hxx", ".h"],
        "parser_name": "cpp",
        "build_command": "tree-sitter-cpp",
    },
    "go": {
        "extensions": [".go"],
        "parser_name": "go",
        "build_command": "tree-sitter-go",
    },
    "rust": {
        "extensions": [".rs"],
        "parser_name": "rust",
        "build_command": "tree-sitter-rust",
    },
    "ruby": {
        "extensions": [".rb", ".rake", ".gemspec"],
        "parser_name": "ruby",
        "build_command": "tree-sitter-ruby",
    },
    "php": {
        "extensions": [".php", ".phtml", ".php3", ".php4", ".php5"],
        "parser_name": "php",
        "build_command": "tree-sitter-php",
    },
    "bash": {
        "extensions": [".sh", ".bash"],
        "parser_name": "bash",
        "build_command": "tree-sitter-bash",
    },
    "html": {
        "extensions": [".html", ".htm"],
        "parser_name": "html",
        "build_command": "tree-sitter-html",
    },
    "css": {
        "extensions": [".css", ".scss", ".sass", ".less"],
        "parser_name": "css",
        "build_command": "tree-sitter-css",
    },
    "json": {
        "extensions": [".json"],
        "parser_name": "json",
        "build_command": "tree-sitter-json",
    },
    "yaml": {
        "extensions": [".yaml", ".yml"],
        "parser_name": "yaml",
        "build_command": "tree-sitter-yaml",
    },
    "sql": {
        "extensions": [".sql"],
        "parser_name": "sql",
        "build_command": "tree-sitter-sql",
    },
    "markdown": {
        "extensions": [".md", ".markdown"],
        "parser_name": "markdown",
        "build_command": "tree-sitter-markdown",
    },
}


class ParserManager:
    """Manages tree-sitter parsers for different languages."""
    
    def __init__(self):
        """Initialize the parser manager."""
        self.parsers: dict[str, Parser] = {}
        self.languages: dict[str, Language] = {}
        self.initialized = False
        
        # Initialize parsers on creation
        self.initialize_parsers()
    
    def initialize_parsers(self) -> None:
        """Initialize all available tree-sitter parsers."""
        if self.initialized:
            return
        
        logger.info("Initializing tree-sitter parsers...")
        
        for language, config in LANGUAGE_MAPPING.items():
            try:
                parser = self._create_parser(language)
                if parser:
                    self.parsers[language] = parser
                    logger.debug(f"Successfully initialized {language} parser")
                else:
                    logger.warning(f"Failed to initialize {language} parser")
            except Exception as e:
                logger.warning(f"Could not initialize {language} parser: {e}")
        
        self.initialized = True
        logger.info(f"Initialized {len(self.parsers)} parsers")
    
    def _create_parser(self, language: str) -> Optional[Parser]:
        """
        Create a tree-sitter parser for the given language.
        
        Args:
            language: Language name
            
        Returns:
            Tree-sitter parser or None if not available
        """
        if language not in LANGUAGE_MAPPING:
            return None
        
        config = LANGUAGE_MAPPING[language]
        parser_name = config["parser_name"]
        
        try:
            # Try to get the language library
            language_lib = self._get_language_library(parser_name)
            
            if not language_lib:
                return None
            
            # Create parser
            parser = Parser()
            parser.set_language(language_lib)
            
            return parser
            
        except Exception as e:
            logger.debug(f"Could not create parser for {language}: {e}")
            return None
    
    def _get_language_library(self, parser_name: str) -> Optional[Language]:
        """
        Get or create a tree-sitter language library.
        
        Args:
            parser_name: Name of the parser
            
        Returns:
            Tree-sitter language library or None
        """
        if parser_name in self.languages:
            return self.languages[parser_name]
        
        try:
            # Try to import the language library
            # This assumes the tree-sitter parsers are installed
            if parser_name == "python":
                from tree_sitter_python import language_python
                lang = language_python()
            elif parser_name == "javascript":
                from tree_sitter_javascript import language_javascript
                lang = language_javascript()
            elif parser_name == "typescript":
                from tree_sitter_typescript import language_typescript
                lang = language_typescript()
            elif parser_name == "java":
                from tree_sitter_java import language_java
                lang = language_java()
            elif parser_name == "c":
                from tree_sitter_c import language_c
                lang = language_c()
            elif parser_name == "cpp":
                from tree_sitter_cpp import language_cpp
                lang = language_cpp()
            elif parser_name == "go":
                from tree_sitter_go import language_go
                lang = language_go()
            elif parser_name == "rust":
                from tree_sitter_rust import language_rust
                lang = language_rust()
            elif parser_name == "ruby":
                from tree_sitter_ruby import language_ruby
                lang = language_ruby()
            elif parser_name == "php":
                from tree_sitter_php import language_php
                lang = language_php()
            elif parser_name == "bash":
                from tree_sitter_bash import language_bash
                lang = language_bash()
            elif parser_name == "html":
                from tree_sitter_html import language_html
                lang = language_html()
            elif parser_name == "css":
                from tree_sitter_css import language_css
                lang = language_css()
            elif parser_name == "json":
                from tree_sitter_json import language_json
                lang = language_json()
            elif parser_name == "yaml":
                from tree_sitter_yaml import language_yaml
                lang = language_yaml()
            elif parser_name == "sql":
                from tree_sitter_sql import language_sql
                lang = language_sql()
            elif parser_name == "markdown":
                from tree_sitter_markdown import language_markdown
                lang = language_markdown()
            else:
                return None
            
            self.languages[parser_name] = lang
            return lang
            
        except ImportError:
            logger.debug(f"Tree-sitter parser not installed for {parser_name}")
            return None
        except Exception as e:
            logger.debug(f"Error loading language library for {parser_name}: {e}")
            return None
    
    def get_parser(self, language: str) -> Optional[Parser]:
        """
        Get a parser for the specified language.
        
        Args:
            language: Language name
            
        Returns:
            Tree-sitter parser or None if not available
        """
        return self.parsers.get(language)
    
    def get_supported_languages(self) -> list:
        """
        Get list of supported languages.
        
        Returns:
            List of language names that have parsers
        """
        return list(self.parsers.keys())
    
    def is_language_supported(self, language: str) -> bool:
        """
        Check if a language is supported.
        
        Args:
            language: Language name to check
            
        Returns:
            True if language is supported
        """
        return language in self.parsers


# Global parser manager instance
_parser_manager: Optional[ParserManager] = None


def initialize_parsers() -> None:
    """Initialize the global parser manager."""
    global _parser_manager
    if _parser_manager is None:
        _parser_manager = ParserManager()


def get_parser_for_language(language: str) -> Optional[Parser]:
    """
    Get a tree-sitter parser for the specified language.
    
    Args:
        language: Language name
        
    Returns:
        Tree-sitter parser or None if not available
    """
    global _parser_manager
    
    if _parser_manager is None:
        initialize_parsers()
    
    return _parser_manager.get_parser(language)


def get_language_mapping() -> dict[str, Any]:
    """
    Get the language mapping configuration.
    
    Returns:
        Dictionary mapping languages to their configurations
    """
    return LANGUAGE_MAPPING.copy()


def get_supported_languages() -> list:
    """
    Get list of supported languages.
    
    Returns:
        List of language names that have parsers
    """
    global _parser_manager
    
    if _parser_manager is None:
        initialize_parsers()
    
    return _parser_manager.get_supported_languages()


def is_language_supported(language: str) -> bool:
    """
    Check if a language is supported.
    
    Args:
        language: Language name to check
        
    Returns:
        True if language is supported
    """
    global _parser_manager
    
    if _parser_manager is None:
        initialize_parsers()
    
    return _parser_manager.is_language_supported(language)


def get_language_from_extension(file_extension: str) -> Optional[str]:
    """
    Get language name from file extension.
    
    Args:
        file_extension: File extension (with or without dot)
        
    Returns:
        Language name or None if not found
    """
    # Remove leading dot if present
    if file_extension.startswith("."):
        file_extension = file_extension[1:]
    
    file_extension = "." + file_extension.lower()
    
    for language, config in LANGUAGE_MAPPING.items():
        if file_extension in config.get("extensions", []):
            return language
    
    return None


def get_extension_from_language(language: str) -> Optional[str]:
    """
    Get primary file extension from language name.
    
    Args:
        language: Language name
        
    Returns:
        Primary file extension or None if not found
    """
    config = LANGUAGE_MAPPING.get(language)
    if config and config.get("extensions"):
        return config["extensions"][0]
    
    return None