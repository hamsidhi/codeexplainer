"""
Configuration settings for the sample project.
This module contains application configuration and settings.
"""

import os
from pathlib import Path


class Config:
    """Application configuration class."""
    
    # Application metadata
    APP_NAME = "Simple Calculator"
    VERSION = "1.0.0"
    AUTHOR = "CodeExplainer Team"
    
    # Display settings
    DECIMAL_PLACES = 2
    SHOW_OPERATIONS = True
    
    # File paths
    @staticmethod
    def get_data_directory() -> Path:
        """Get the data directory path."""
        return Path(__file__).parent / "data"
    
    @staticmethod
    def get_log_file() -> Path:
        """Get the log file path."""
        return Path(__file__).parent / "app.log"
    
    # Environment settings
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    TESTING = os.environ.get('TESTING', 'False').lower() == 'true'
    
    # Performance settings
    MAX_OPERATIONS = 1000
    PRECISION = 10
    
    # User interface settings
    WELCOME_MESSAGE = f"Welcome to {APP_NAME} v{VERSION}!"
    GOODBYE_MESSAGE = "Thank you for using the calculator!"
    
    @classmethod
    def display_config(cls) -> None:
        """Display current configuration settings."""
        print(f"Application: {cls.APP_NAME}")
        print(f"Version: {cls.VERSION}")
        print(f"Author: {cls.AUTHOR}")
        print(f"Debug Mode: {cls.DEBUG}")
        print(f"Max Operations: {cls.MAX_OPERATIONS}")
        print(f"Decimal Places: {cls.DECIMAL_PLACES}")