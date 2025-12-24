"""
Tests for the File Analyzer
"""

import pytest
from pathlib import Path
from codeexplainer.core.file_analyzer import FileAnalyzer


class TestFileAnalyzer:
    """Test cases for the FileAnalyzer class."""
    
    def test_analyze_python_file(self, tmp_path):
        """Test analysis of a Python file."""
        file_path = tmp_path / "test.py"
        file_path.write_text("""
def greet(name):
    """Return a greeting."""
    return f"Hello, {name}!"

class Calculator:
    def add(self, a, b):
        return a + b
""")
        
        analyzer = FileAnalyzer({})
        result = analyzer.analyze(file_path, "python")
        
        assert result is not None
        assert result["language"] == "python"
        assert result["filename"] == "test.py"
        assert len(result["functions"]) == 2  # greet and add
        assert len(result["classes"]) == 1    # Calculator
        assert "greet" in [f["name"] for f in result["functions"]]
    
    def test_analyze_javascript_file(self, tmp_path):
        """Test analysis of a JavaScript file."""
        file_path = tmp_path / "test.js"
        file_path.write_text("""
function greet(name) {
    return `Hello, ${name}!`;
}

class Calculator {
    add(a, b) {
        return a + b;
    }
}

export { greet, Calculator };
""")
        
        analyzer = FileAnalyzer({})
        result = analyzer.analyze(file_path, "javascript")
        
        assert result is not None
        assert result["language"] == "javascript"
        assert len(result["functions"]) >= 1  # greet
        assert len(result["classes"]) == 1    # Calculator
    
    def test_analyze_java_file(self, tmp_path):
        """Test analysis of a Java file."""
        file_path = tmp_path / "Test.java"
        file_path.write_text("""
public class Test {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
    
    public int add(int a, int b) {
        return a + b;
    }
}
""")
        
        analyzer = FileAnalyzer({})
        result = analyzer.analyze(file_path, "java")
        
        assert result is not None
        assert result["language"] == "java"
        assert len(result["classes"]) == 1  # Test class
    
    def test_analyze_empty_file(self, tmp_path):
        """Test analysis of an empty file."""
        file_path = tmp_path / "empty.py"
        file_path.write_text("")
        
        analyzer = FileAnalyzer({})
        result = analyzer.analyze(file_path)
        
        assert result is None  # Empty files are skipped
    
    def test_detect_language_from_extension(self, tmp_path):
        """Test automatic language detection from file extension."""
        test_cases = [
            ("test.py", "python", "print('hello')"),
            ("test.js", "javascript", "console.log('hello');"),
            ("test.java", "java", "public class Test {}"),
            ("test.go", "go", "package main"),
        ]
        
        for filename, expected_lang, content in test_cases:
            file_path = tmp_path / filename
            file_path.write_text(content)
            
            analyzer = FileAnalyzer({})
            result = analyzer.analyze(file_path)
            
            if result:
                assert result["language"] == expected_lang
    
    def test_extract_dependencies(self, tmp_path):
        """Test extraction of dependencies from code."""
        file_path = tmp_path / "imports.py"
        file_path.write_text("""
import os
from pathlib import Path
import numpy as np
from django import models
""")
        
        analyzer = FileAnalyzer({})
        result = analyzer.analyze(file_path, "python")
        
        assert result is not None
        dependencies = result["dependencies"]
        assert "os" in dependencies
        assert "pathlib" in dependencies
        assert "numpy" in dependencies
        assert "django" in dependencies
    
    def test_calculate_metrics(self, tmp_path):
        """Test calculation of code metrics."""
        file_path = tmp_path / "metrics.py"
        file_path.write_text("""
# This is a test file

def simple_function():
    return 42

def complex_function(x):
    if x > 0:
        for i in range(x):
            if i % 2 == 0:
                print(i)
    else:
        return -1
""")
        
        analyzer = FileAnalyzer({})
        result = analyzer.analyze(file_path, "python")
        
        assert result is not None
        metrics = result["metrics"]
        
        assert "lines" in metrics
        assert "lines_of_code" in metrics
        assert "complexity" in metrics
        assert metrics["lines"] > 0
        assert metrics["lines_of_code"] > 0
    
    def test_analyze_without_parser(self, tmp_path):
        """Test fallback analysis when parser is not available."""
        file_path = tmp_path / "unknown.xyz"
        file_path.write_text("This is not a recognized programming language file.")
        
        analyzer = FileAnalyzer({})
        result = analyzer.analyze(file_path, "unknown_language")
        
        # Should still provide basic analysis
        assert result is not None
        assert result["language"] == "unknown_language"
        assert "metrics" in result
        assert "purpose" in result