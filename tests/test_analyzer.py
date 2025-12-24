"""
Tests for the Project Analyzer
"""

import pytest
from pathlib import Path
from codeexplainer.core.analyzer import ProjectAnalyzer
from codeexplainer.utils.config import Config


class TestProjectAnalyzer:
    """Test cases for the ProjectAnalyzer class."""
    
    def test_analyzer_initialization(self):
        """Test that analyzer initializes correctly."""
        config = Config({})
        analyzer = ProjectAnalyzer(config.to_dict())
        assert analyzer is not None
    
    def test_analyze_empty_project(self, tmp_path):
        """Test analysis of an empty project."""
        config = Config({})
        analyzer = ProjectAnalyzer(config.to_dict())
        
        result = analyzer.analyze_project(tmp_path, tmp_path / "output")
        
        assert result["files_analyzed"] == 0
        assert result["explanations_generated"] == 0
    
    def test_analyze_python_project(self, tmp_path):
        """Test analysis of a simple Python project."""
        # Create project structure
        project_dir = tmp_path / "python_project"
        project_dir.mkdir()
        
        # Create main.py
        main_file = project_dir / "main.py"
        main_file.write_text("""
def greet(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("World"))
""")
        
        # Create utils.py
        utils_file = project_dir / "utils.py"
        utils_file.write_text("""
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
""")
        
        # Analyze the project
        config = Config({})
        analyzer = ProjectAnalyzer(config.to_dict())
        
        output_dir = tmp_path / "output"
        result = analyzer.analyze_project(project_dir, output_dir)
        
        # Check results
        assert result["files_analyzed"] == 2
        assert result["explanations_generated"] == 4  # 2 files × 2 explanations each
        
        # Check that output files were created
        assert output_dir.exists()
        summary_file = output_dir / "00_project_summary.txt"
        assert summary_file.exists()
    
    def test_analyze_mixed_project(self, tmp_path):
        """Test analysis of a project with multiple languages."""
        project_dir = tmp_path / "mixed_project"
        project_dir.mkdir()
        
        # Create Python file
        py_file = project_dir / "app.py"
        py_file.write_text("print('Python app')")
        
        # Create JavaScript file
        js_file = project_dir / "script.js"
        js_file.write_text("console.log('JavaScript');")
        
        # Create HTML file
        html_file = project_dir / "index.html"
        html_file.write_text("<html><body>Hello</body></html>")
        
        # Analyze
        config = Config({})
        analyzer = ProjectAnalyzer(config.to_dict())
        
        output_dir = tmp_path / "output"
        result = analyzer.analyze_project(project_dir, output_dir)
        
        # Should have analyzed 3 files
        assert result["files_analyzed"] == 3
        assert result["explanations_generated"] == 6  # 3 files × 2 explanations each
    
    def test_project_summary_generation(self, tmp_path):
        """Test that project summary is generated correctly."""
        project_dir = tmp_path / "summary_test"
        project_dir.mkdir()
        
        # Create some files
        for i in range(3):
            file = project_dir / f"file_{i}.py"
            file.write_text(f"# File {i}\nprint('Hello {i}')\n")
        
        # Analyze
        config = Config({})
        analyzer = ProjectAnalyzer(config.to_dict())
        
        output_dir = tmp_path / "output"
        result = analyzer.analyze_project(project_dir, output_dir)
        
        # Check summary file
        summary_file = Path(result["summary_file"])
        assert summary_file.exists()
        
        summary_content = summary_file.read_text()
        assert "PROJECT SUMMARY" in summary_content
        assert "Total Files Analyzed: 3" in summary_content
        assert "python: 3 files" in summary_content