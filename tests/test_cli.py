"""
Tests for the Command Line Interface
"""

import pytest
from pathlib import Path
from click.testing import CliRunner
from codeexplainer.cli import main


class TestCLI:
    """Test cases for the CLI interface."""
    
    def test_help_command(self):
        """Test that help command works."""
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert 'Analyze a software project' in result.output
    
    def test_version_command(self):
        """Test that version command works."""
        runner = CliRunner()
        result = runner.invoke(main, ['--version'])
        assert result.exit_code == 0
        assert 'CodeExplainer' in result.output
    
    def test_missing_argument(self):
        """Test that missing project path shows error."""
        runner = CliRunner()
        result = runner.invoke(main, [])
        assert result.exit_code != 0
    
    def test_invalid_project_path(self):
        """Test that invalid project path shows error."""
        runner = CliRunner()
        result = runner.invoke(main, ['/nonexistent/path'])
        assert result.exit_code != 0
    
    def test_valid_project_analysis(self, tmp_path):
        """Test analysis of a valid project."""
        # Create a simple test project
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        # Create a Python file
        test_file = project_dir / "test.py"
        test_file.write_text("print('Hello, world!')\n")
        
        runner = CliRunner()
        result = runner.invoke(main, [str(project_dir), '--no-audio'])
        
        # Should complete successfully
        assert result.exit_code == 0
        assert 'Analysis complete!' in result.output
    
    def test_output_directory_option(self, tmp_path):
        """Test custom output directory option."""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        output_dir = tmp_path / "custom_output"
        
        runner = CliRunner()
        result = runner.invoke(main, [
            str(project_dir),
            '--output-dir', str(output_dir),
            '--no-audio'
        ])
        
        assert result.exit_code == 0
        assert str(output_dir) in result.output