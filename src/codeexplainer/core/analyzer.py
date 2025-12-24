from typing import Any
"""
ProjectAnalyzer - Main orchestrator for project analysis

This module coordinates the entire analysis workflow:
1. Traverses project structure
2. Analyzes each file
3. Generates explanations
4. Creates project summary
"""

import os
from pathlib import Path
from typing import Dict, List, Any
from loguru import logger

from .project_traverser import ProjectTraverser
from .file_analyzer import FileAnalyzer
from .explanation_generator import ExplanationGenerator
from ..utils.file_utils import create_output_structure
from ..utils.config import Config


class ProjectAnalyzer:
    """Main class that orchestrates the entire analysis workflow."""
    
    def __init__(self, config: dict[str, Any]):
        """
        Initialize the project analyzer.
        
        Args:
            config: Configuration dictionary containing all settings
        """
        self.config = Config(config)
        self.traverser = ProjectTraverser(self.config.file_filters)
        self.file_analyzer = FileAnalyzer(self.config.analysis)
        self.explanation_generator = ExplanationGenerator(self.config.output)
        
        logger.info("ProjectAnalyzer initialized")
    
    def analyze_project(self, project_path: Path, output_dir: Path) -> dict[str, Any]:
        """
        Analyze an entire project and generate explanations.
        
        Args:
            project_path: Path to the project root directory
            output_dir: Directory where explanations will be saved
            
        Returns:
            Dictionary containing analysis results and statistics
        """
        logger.info(f"Starting analysis of project: {project_path}")
        
        # Create output directory structure
        create_output_structure(output_dir)
        
        # Traverse project and get all files to analyze
        project_files = self.traverser.traverse(project_path)
        logger.info(f"Found {len(project_files)} files to analyze")
        
        # Analyze each file and generate explanations
        analysis_results = []
        files_analyzed = 0
        explanations_generated = 0
        
        for file_info in project_files:
            try:
                # Analyze the file
                analysis = self.file_analyzer.analyze(
                    file_path=file_info["path"],
                    language=file_info.get("language")
                )
                
                if analysis:
                    # Generate explanations
                    explanations = self.explanation_generator.generate(
                        analysis=analysis,
                        output_dir=output_dir
                    )
                    
                    analysis_results.append({
                        "file_info": file_info,
                        "analysis": analysis,
                        "explanations": explanations
                    })
                    
                    files_analyzed += 1
                    explanations_generated += len(explanations)
                    
                    logger.debug(f"Successfully analyzed: {file_info['path']}")
                    
            except Exception as e:
                logger.error(f"Failed to analyze {file_info['path']}: {e}")
                continue
        
        # Generate project summary
        summary_path = self._generate_project_summary(
            analysis_results=analysis_results,
            project_path=project_path,
            output_dir=output_dir
        )
        
        logger.info(f"Analysis complete. Files analyzed: {files_analyzed}")
        
        return {
            "files_analyzed": files_analyzed,
            "explanations_generated": explanations_generated,
            "output_dir": str(output_dir),
            "summary_file": str(summary_path),
            "results": analysis_results
        }
    
    def _generate_project_summary(
        self,
        analysis_results: list[Dict],
        project_path: Path,
        output_dir: Path
    ) -> Path:
        """
        Generate a comprehensive project-level summary.
        
        Args:
            analysis_results: Results from all file analyses
            project_path: Original project path
            output_dir: Output directory for the summary
            
        Returns:
            Path to the generated summary file
        """
        logger.info("Generating project summary...")
        
        # Collect statistics
        languages = {}
        file_types = {}
        total_lines = 0
        
        for result in analysis_results:
            analysis = result["analysis"]
            
            # Language statistics
            lang = analysis["language"]
            languages[lang] = languages.get(lang, 0) + 1
            
            # File type statistics
            ext = Path(analysis["file_path"]).suffix
            file_types[ext] = file_types.get(ext, 0) + 1
            
            # Lines of code
            total_lines += analysis.get("metrics", {}).get("lines", 0)
        
        # Generate summary content
        summary_content = self._create_summary_content(
            project_path=project_path,
            languages=languages,
            file_types=file_types,
            total_files=len(analysis_results),
            total_lines=total_lines,
            analysis_results=analysis_results
        )
        
        # Save summary
        summary_path = output_dir / "00_project_summary.txt"
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary_content)
        
        logger.info(f"Project summary saved to: {summary_path}")
        return summary_path
    
    def _create_summary_content(
        self,
        project_path: Path,
        languages: dict[str, int],
        file_types: dict[str, int],
        total_files: int,
        total_lines: int,
        analysis_results: list[Dict]
    ) -> str:
        """
        Create the content for the project summary.
        
        Args:
            project_path: Original project path
            languages: Dictionary of language counts
            file_types: Dictionary of file extension counts
            total_files: Total number of files analyzed
            total_lines: Total lines of code
            analysis_results: Detailed analysis results
            
        Returns:
            Formatted summary content
        """
        lines = []
        lines.append("=" * 80)
        lines.append("PROJECT SUMMARY - CodeExplainer Analysis")
        lines.append("=" * 80)
        lines.append("")
        
        # Basic project info
        lines.append(f"Project Name: {project_path.name}")
        lines.append(f"Project Path: {project_path.absolute()}")
        lines.append(f"Analysis Date: {os.popen('date').read().strip()}")
        lines.append("")
        
        # Statistics
        lines.append("PROJECT STATISTICS")
        lines.append("-" * 40)
        lines.append(f"Total Files Analyzed: {total_files}")
        lines.append(f"Total Lines of Code: {total_lines:,}")
        lines.append("")
        
        # Languages used
        lines.append("PROGRAMMING LANGUAGES")
        lines.append("-" * 40)
        for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  {lang}: {count} files")
        lines.append("")
        
        # File types
        lines.append("FILE TYPES")
        lines.append("-" * 40)
        for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  {ext}: {count} files")
        lines.append("")
        
        # Project structure overview
        lines.append("PROJECT STRUCTURE")
        lines.append("-" * 40)
        
        # Group files by directory
        directory_structure = {}
        for result in analysis_results:
            file_path = Path(result["analysis"]["file_path"])
            relative_path = file_path.relative_to(project_path)
            directory = str(relative_path.parent) if relative_path.parent != "." else "root"
            
            if directory not in directory_structure:
                directory_structure[directory] = []
            directory_structure[directory].append(relative_path.name)
        
        for directory, files in sorted(directory_structure.items()):
            lines.append(f"  {directory}/")
            for filename in sorted(files):
                lines.append(f"    ├── {filename}")
        lines.append("")
        
        # Key findings
        lines.append("KEY FINDINGS")
        lines.append("-" * 40)
        lines.append("This project contains:")
        
        for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                lines.append(f"• {count} {lang} files")
        
        lines.append(f"\nTotal complexity: {total_lines:,} lines of code across {total_files} files")
        lines.append("")
        
        # How to use the explanations
        lines.append("HOW TO USE THESE EXPLANATIONS")
        lines.append("-" * 40)
        lines.append("For each file in this project, you'll find:")
        lines.append("• explanation.txt - A beginner-friendly explanation of what the file does")
        lines.append("• audio_script.txt - The same explanation optimized for text-to-speech")
        lines.append("")
        lines.append("Start by reading the explanation.txt files to understand each component,")
        lines.append("then use the audio_script.txt files if you want to listen to the explanations.")
        lines.append("")
        
        lines.append("=" * 80)
        lines.append("End of Project Summary")
        lines.append("=" * 80)
        
        return "\n".join(lines)