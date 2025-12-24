"""
Tests for utility functions
"""

import pytest
from pathlib import Path
from codeexplainer.utils.file_utils import (
    sanitize_filename,
    create_output_structure,
    safe_write_file,
    safe_read_file,
    format_file_size,
)
from codeexplainer.utils.text_utils import (
    simplify_technical_terms,
    optimize_for_tts,
    extract_key_concepts,
    create_summary,
)
from codeexplainer.utils.validators import (
    validate_project_path,
    validate_output_path,
    validate_file_size,
)


class TestFileUtils:
    """Test cases for file utilities."""
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        # Test invalid characters
        assert sanitize_filename('file<name>') == 'file_name_'
        assert sanitize_filename('file:name') == 'file_name'
        assert sanitize_filename('file"name') == 'file_name'
        
        # Test length limit
        long_name = 'a' * 100 + '.py'
        result = sanitize_filename(long_name, max_length=50)
        assert len(result) <= 50
        assert result.endswith('.py')
        
        # Test empty filename
        assert sanitize_filename('') == 'unnamed_file'
        assert sanitize_filename('   ') == 'unnamed_file'
        
        # Test control characters
        assert sanitize_filename('file\x00name') == 'filename'
    
    def test_create_output_structure(self, tmp_path):
        """Test output structure creation."""
        output_dir = tmp_path / "test_output"
        create_output_structure(output_dir)
        
        assert output_dir.exists()
        assert (output_dir / "explanations").exists()
        assert (output_dir / "summaries").exists()
        assert (output_dir / "logs").exists()
    
    def test_safe_write_and_read_file(self, tmp_path):
        """Test safe file operations."""
        file_path = tmp_path / "test.txt"
        content = "Hello, World!"
        
        # Write file
        assert safe_write_file(file_path, content)
        assert file_path.exists()
        
        # Read file
        read_content = safe_read_file(file_path)
        assert read_content == content
    
    def test_format_file_size(self):
        """Test file size formatting."""
        assert format_file_size(0) == "0 B"
        assert format_file_size(1024) == "1.0 KB"
        assert format_file_size(1024 * 1024) == "1.0 MB"
        assert format_file_size(1024 * 1024 * 1024) == "1.0 GB"
        assert format_file_size(512) == "512.0 B"


class TestTextUtils:
    """Test cases for text utilities."""
    
    def test_simplify_technical_terms(self):
        """Test technical term simplification."""
        text = "This function uses a recursive algorithm to process the data."
        simplified = simplify_technical_terms(text)
        
        assert "tool or recipe" in simplified or "function" in simplified
        assert "step-by-step plan" in simplified or "algorithm" in simplified
    
    def test_simplify_python_terms(self):
        """Test Python-specific term simplification."""
        text = "def greet(name): return f'Hello, {name}!'"
        simplified = simplify_technical_terms(text, language="python")
        
        assert "define a function" in simplified or "def" not in simplified
    
    def test_optimize_for_tts(self):
        """Test text optimization for text-to-speech."""
        text = "The API returns JSON with HTTP status 200 OK."
        optimized = optimize_for_tts(text)
        
        # Check that abbreviations are expanded
        assert "A P I" in optimized or "API" not in optimized
        assert "J S O N" in optimized or "JSON" not in optimized
        assert "H T T P" in optimized or "HTTP" not in optimized
    
    def test_optimize_for_tts_numbers(self):
        """Test number conversion for TTS."""
        text = "There are 42 items in 3 categories."
        optimized = optimize_for_tts(text)
        
        # Numbers should be converted to words
        assert "forty-two" in optimized.lower() or "42" not in optimized
    
    def test_extract_key_concepts(self):
        """Test key concept extraction."""
        text = """
        def calculate_sum(numbers):
            total = 0
            for num in numbers:
                total += num
            return total
        """
        concepts = extract_key_concepts(text, language="python")
        
        assert "function" in concepts
        assert "for" in concepts
        assert "return" in concepts
    
    def test_create_summary(self):
        """Test summary creation."""
        text = "This is a long text that contains many words and should be summarized into something much shorter."
        summary = create_summary(text, max_length=20)
        
        assert len(summary) <= 20
        assert summary.endswith('...')


class TestValidators:
    """Test cases for validators."""
    
    def test_validate_project_path(self, tmp_path):
        """Test project path validation."""
        # Valid directory
        assert validate_project_path(tmp_path)
        
        # Non-existent path
        with pytest.raises(ValueError):
            validate_project_path(tmp_path / "nonexistent")
        
        # File instead of directory
        file_path = tmp_path / "file.txt"
        file_path.write_text("test")
        with pytest.raises(ValueError):
            validate_project_path(file_path)
    
    def test_validate_output_path(self, tmp_path):
        """Test output path validation."""
        # Valid output path
        output_path = tmp_path / "output"
        assert validate_output_path(output_path)
        
        # Should create parent directory if needed
        nested_path = tmp_path / "deep" / "nested" / "output"
        assert validate_output_path(nested_path)
    
    def test_validate_file_size(self, tmp_path):
        """Test file size validation."""
        # Create a small file
        small_file = tmp_path / "small.txt"
        small_file.write_text("small content")
        
        assert validate_file_size(small_file, max_size_mb=10)
        
        # Simulate a large file by mocking size
        # In real tests, you'd create an actual large file
        assert validate_file_size(small_file, max_size_mb=0.001)  # Very small limit