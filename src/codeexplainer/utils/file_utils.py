from typing import Any
"""
File and directory utilities for CodeExplainer

Handles creating output directories, managing file paths,
and ensuring safe file operations.
"""

import os
import shutil
from pathlib import Path
from typing import Optional
from loguru import logger


def create_output_structure(output_dir: Path) -> None:
    """
    Create the output directory structure for explanations.
    
    Args:
        output_dir: Root directory for all output
    """
    try:
        # Create main output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for organization
        subdirs = ["explanations", "summaries", "logs"]
        for subdir in subdirs:
            (output_dir / subdir).mkdir(exist_ok=True)
        
        logger.info(f"Created output structure at: {output_dir}")
        
    except Exception as e:
        logger.error(f"Failed to create output structure: {e}")
        raise


def sanitize_filename(filename: str, max_length: int = 50) -> str:
    """
    Sanitize a filename for safe use across different operating systems.
    
    Args:
        filename: Original filename
        max_length: Maximum length for the sanitized filename
        
    Returns:
        Sanitized filename safe for all operating systems
    """
    # Characters that are invalid in filenames on various systems
    invalid_chars = '<>:"/\\|?*'
    
    # Replace invalid characters with underscores
    sanitized = filename
    for char in invalid_chars:
        sanitized = sanitized.replace(char, '_')
    
    # Remove control characters
    sanitized = ''.join(char for char in sanitized if ord(char) >= 32)
    
    # Trim whitespace
    sanitized = sanitized.strip()
    
    # Ensure it's not empty
    if not sanitized:
        sanitized = "unnamed_file"
    
    # Limit length while preserving extension
    if len(sanitized) > max_length:
        name, ext = os.path.splitext(sanitized)
        max_name_length = max_length - len(ext)
        if max_name_length > 0:
            sanitized = name[:max_name_length] + ext
        else:
            sanitized = sanitized[:max_length]
    
    # Ensure it doesn't end with a dot or space
    sanitized = sanitized.rstrip('. ')
    
    return sanitized


def ensure_directory(path: Path) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path to ensure
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {e}")
        raise


def safe_write_file(file_path: Path, content: str, encoding: str = "utf-8") -> bool:
    """
    Safely write content to a file with error handling.
    
    Args:
        file_path: Path to write to
        content: Content to write
        encoding: File encoding
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
        
        logger.debug(f"Successfully wrote file: {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to write file {file_path}: {e}")
        return False


def safe_read_file(file_path: Path, encoding: str = "utf-8") -> Optional[str]:
    """
    Safely read content from a file with error handling.
    
    Args:
        file_path: Path to read from
        encoding: File encoding
        
    Returns:
        File content or None if failed
    """
    try:
        with open(file_path, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        return None


def get_file_info(file_path: Path) -> dict:
    """
    Get comprehensive information about a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary with file information
    """
    try:
        stat = file_path.stat()
        
        return {
            "path": str(file_path),
            "name": file_path.name,
            "stem": file_path.stem,
            "suffix": file_path.suffix,
            "size_bytes": stat.st_size,
            "size_human": format_file_size(stat.st_size),
            "modified": stat.st_mtime,
            "is_file": file_path.is_file(),
            "is_directory": file_path.is_dir(),
            "exists": file_path.exists(),
        }
    except Exception as e:
        logger.error(f"Failed to get file info for {file_path}: {e}")
        return {}


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {size_names[i]}"


def copy_file_with_metadata(src: Path, dst: Path) -> bool:
    """
    Copy a file preserving metadata.
    
    Args:
        src: Source file path
        dst: Destination file path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        logger.debug(f"Copied file: {src} -> {dst}")
        return True
    except Exception as e:
        logger.error(f"Failed to copy file {src} to {dst}: {e}")
        return False


def list_files_recursive(directory: Path, pattern: str = "*") -> list:
    """
    List all files in a directory recursively.
    
    Args:
        directory: Directory to search
        pattern: File pattern to match
        
    Returns:
        List of matching file paths
    """
    try:
        return list(directory.rglob(pattern))
    except Exception as e:
        logger.error(f"Failed to list files in {directory}: {e}")
        return []


def cleanup_directory(directory: Path, preserve_structure: bool = False) -> bool:
    """
    Clean up a directory by removing all contents.
    
    Args:
        directory: Directory to clean
        preserve_structure: If True, keep the directory itself
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if directory.exists():
            if preserve_structure:
                # Remove contents but keep directory
                for item in directory.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
            else:
                # Remove entire directory
                shutil.rmtree(directory)
        
        logger.info(f"Cleaned up directory: {directory}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to cleanup directory {directory}: {e}")
        return False


def get_unique_filename(directory: Path, base_name: str, extension: str = "") -> Path:
    """
    Generate a unique filename in the given directory.
    
    Args:
        directory: Directory where file will be created
        base_name: Base filename without extension
        extension: File extension (with or without dot)
        
    Returns:
        Path to unique filename
    """
    # Ensure extension starts with dot
    if extension and not extension.startswith("."):
        extension = "." + extension
    
    # Try base name first
    candidate = directory / f"{base_name}{extension}"
    if not candidate.exists():
        return candidate
    
    # Generate unique name with counter
    counter = 1
    while True:
        candidate = directory / f"{base_name}_{counter}{extension}"
        if not candidate.exists():
            return candidate
        counter += 1


def validate_output_path(path: Path) -> bool:
    """
    Validate that a path is suitable for output.
    
    Args:
        path: Path to validate
        
    Returns:
        True if path is valid, False otherwise
    """
    try:
        # Check if path is writable
        test_file = path / ".test_write"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(test_file, "w") as f:
            f.write("test")
        
        test_file.unlink()
        return True
        
    except Exception:
        return False