from typing import Any
"""
CodeExplainer - The Ultimate Code Understanding Tool for Beginners

A powerful, open-source tool that analyzes any software project and generates
beginner-friendly explanations for every file. Perfect for learning, teaching,
and understanding codebases of any size.

Example:
    >>> from codeexplainer.core import ProjectAnalyzer
    >>> analyzer = ProjectAnalyzer({})
    >>> result = analyzer.analyze_project("/path/to/project", "/path/to/output")
    >>> print(f"Analyzed {result['files_analyzed']} files")
"""

__version__ = "1.0.0"
__author__ = "CodeExplainer Team"
__email__ = "contact@codeexplainer.dev"
__license__ = "MIT"

from .core import ProjectAnalyzer, FileAnalyzer, ProjectTraverser
from .utils import Config, load_config

__all__ = [
    "ProjectAnalyzer",
    "FileAnalyzer", 
    "ProjectTraverser",
    "Config",
    "load_config",
]