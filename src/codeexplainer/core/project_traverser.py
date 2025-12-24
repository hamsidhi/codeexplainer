from typing import Any
"""
ProjectTraverser - Recursively traverses project directories

This module handles walking through the project structure and
identifying files that need to be analyzed.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import pathspec
from pygments.lexers import get_lexer_for_filename, guess_lexer_for_filename
import magic
from loguru import logger


class ProjectTraverser:
    """Traverses project directories and identifies files for analysis."""
    
    # Supported programming languages and their file extensions
    LANGUAGE_EXTENSIONS = {
        # Web Technologies
        "javascript": [".js", ".jsx", ".mjs"],
        "typescript": [".ts", ".tsx"],
        "html": [".html", ".htm"],
        "css": [".css", ".scss", ".sass", ".less"],
        "xml": [".xml", ".xhtml"],
        
        # Programming Languages
        "python": [".py", ".pyx", ".pyi"],
        "java": [".java"],
        "c": [".c", ".h"],
        "cpp": [".cpp", ".cxx", ".cc", ".hpp", ".hxx"],
        "c_sharp": [".cs"],
        "go": [".go"],
        "rust": [".rs"],
        "ruby": [".rb", ".rake", ".gemspec"],
        "php": [".php", ".phtml", ".php3", ".php4", ".php5"],
        "swift": [".swift"],
        "kotlin": [".kt", ".kts"],
        
        # Scripting Languages
        "bash": [".sh", ".bash"],
        "powershell": [".ps1", ".psm1"],
        "perl": [".pl", ".pm"],
        "lua": [".lua"],
        
        # Data and Config
        "json": [".json"],
        "yaml": [".yaml", ".yml"],
        "sql": [".sql"],
        "markdown": [".md", ".markdown"],
        
        # Build and Config Files
        "docker": ["Dockerfile"],
        "makefile": ["Makefile", "makefile"],
        "cmake": ["CMakeLists.txt"],
    }
    
    # Common directories and files to ignore
    DEFAULT_IGNORE_PATTERNS = [
        # Version control
        ".git", ".gitignore", ".gitattributes",
        ".svn", ".hg",
        
        # Python
        "__pycache__", "*.pyc", "*.pyo", "*.pyd",
        ".pytest_cache", ".coverage", "htmlcov",
        "*.egg-info", "dist", "build", ".eggs",
        "venv", ".venv", "env", ".env",
        
        # Node.js
        "node_modules", ".npm", ".yarn",
        "package-lock.json", "yarn.lock",
        
        # Java
        "target", ".gradle", "build",
        
        # IDE and Editor files
        ".idea", ".vscode", ".vs",
        "*.swp", "*.swo", "*~",
        ".DS_Store", "Thumbs.db",
        
        # Documentation build
        "_build", "_site", ".tox",
        
        # Temporary and backup files
        "*.tmp", "*.temp", "*.bak", "*.backup",
        
        # Compiled binaries
        "*.exe", "*.dll", "*.so", "*.dylib",
        "*.bin", "*.dat", "*.o", "*.obj",
        
        # Media and binary assets
        "*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp",
        "*.mp3", "*.mp4", "*.avi", "*.mov", "*.wav",
        "*.zip", "*.tar", "*.gz", "*.rar", "*.7z",
        "*.pdf", "*.doc", "*.docx", "*.xls", "*.xlsx",
        
        # Logs and databases
        "*.log", "*.sqlite", "*.db", "*.mdb",
    ]
    
    def __init__(self, file_filters: Optional[dict[str, Any]] = None):
        """
        Initialize the project traverser.
        
        Args:
            file_filters: Dictionary with 'include_patterns' and 'exclude_patterns'
        """
        self.file_filters = file_filters or {}
        
        # Create pathspec matchers
        self.exclude_spec = self._create_exclude_spec()
        self.include_spec = self._create_include_spec()
        
        logger.info("ProjectTraverser initialized")
    
    def _create_exclude_spec(self) -> pathspec.PathSpec:
        """Create pathspec for files/directories to exclude."""
        patterns = list(self.DEFAULT_IGNORE_PATTERNS)
        
        # Add custom exclude patterns
        custom_excludes = self.file_filters.get("exclude_patterns", [])
        patterns.extend(custom_excludes)
        
        return pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    
    def _create_include_spec(self) -> Optional[pathspec.PathSpec]:
        """Create pathspec for files to specifically include."""
        includes = self.file_filters.get("include_patterns", [])
        
        if not includes:
            return None
        
        return pathspec.PathSpec.from_lines("gitwildmatch", includes)
    
    def traverse(self, project_path: Path) -> list[dict[str, Any]]:
        """
        Traverse the project directory and return files to analyze.
        
        Args:
            project_path: Path to the project root directory
            
        Returns:
            List of dictionaries containing file information
        """
        if not project_path.is_dir():
            raise ValueError(f"Project path is not a directory: {project_path}")
        
        files_to_analyze = []
        
        logger.info(f"Traversing project: {project_path}")
        
        for root, dirs, files in os.walk(project_path):
            root_path = Path(root)
            
            # Filter out excluded directories
            dirs[:] = [
                d for d in dirs
                if not self.exclude_spec.match_file(str(root_path / d))
            ]
            
            for filename in files:
                file_path = root_path / filename
                
                # Check if file should be excluded
                relative_path = file_path.relative_to(project_path)
                
                if self.exclude_spec.match_file(str(relative_path)):
                    continue
                
                # Check if file should be included (if include patterns specified)
                if self.include_spec and not self.include_spec.match_file(str(relative_path)):
                    continue
                
                # Determine file type and language
                file_info = self._analyze_file(file_path, project_path)
                
                if file_info and file_info.get("language"):
                    files_to_analyze.append(file_info)
                    logger.debug(f"Found file to analyze: {relative_path} ({file_info['language']})")
        
        logger.info(f"Traversal complete. Found {len(files_to_analyze)} files to analyze")
        return files_to_analyze
    
    def _analyze_file(self, file_path: Path, project_path: Path) -> Optional[dict[str, Any]]:
        """
        Analyze a single file to determine its type and language.
        
        Args:
            file_path: Path to the file
            project_path: Root project path for calculating relative paths
            
        Returns:
            Dictionary with file information or None if not analyzable
        """
        try:
            # Get basic file info
            relative_path = file_path.relative_to(project_path)
            file_size = file_path.stat().st_size
            
            # Skip empty files
            if file_size == 0:
                return None
            
            # Detect language
            language = self._detect_language(file_path)
            
            if not language:
                return None
            
            # Get file type using magic
            try:
                file_type = magic.from_file(str(file_path), mime=True)
            except Exception:
                file_type = "text/plain"
            
            return {
                "path": file_path,
                "relative_path": str(relative_path),
                "filename": file_path.name,
                "extension": file_path.suffix,
                "size": file_size,
                "language": language,
                "mime_type": file_type,
                "directory": str(relative_path.parent) if relative_path.parent != "." else "root"
            }
            
        except Exception as e:
            logger.warning(f"Could not analyze file {file_path}: {e}")
            return None
    
    def _detect_language(self, file_path: Path) -> Optional[str]:
        """
        Detect the programming language of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Language name or None if not detected
        """
        filename = file_path.name
        extension = file_path.suffix.lower()
        
        # First, try by extension
        for language, extensions in self.LANGUAGE_EXTENSIONS.items():
            if extension in extensions or filename in extensions:
                return language
        
        # Try to detect using Pygments
        try:
            lexer = get_lexer_for_filename(filename)
            language_name = lexer.name.lower()
            
            # Map Pygments language names to our internal names
            language_mapping = {
                "python": "python",
                "java": "java",
                "javascript": "javascript",
                "typescript": "typescript",
                "c": "c",
                "c++": "cpp",
                "c#": "c_sharp",
                "go": "go",
                "rust": "rust",
                "ruby": "ruby",
                "php": "php",
                "swift": "swift",
                "kotlin": "kotlin",
                "bash": "bash",
                "powershell": "powershell",
                "perl": "perl",
                "lua": "lua",
                "json": "json",
                "yaml": "yaml",
                "sql": "sql",
                "markdown": "markdown",
            }
            
            for key, value in language_mapping.items():
                if key in language_name:
                    return value
                    
        except Exception:
            pass
        
        # Try guessing by content
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(1024)  # Read first 1KB
                
                if content:
                    lexer = guess_lexer_for_filename(filename, content)
                    if lexer:
                        language_name = lexer.name.lower()
                        for key, value in language_mapping.items():
                            if key in language_name:
                                return value
        except Exception:
            pass
        
        return None