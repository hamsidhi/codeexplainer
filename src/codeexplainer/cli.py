from typing import Any
"""
Command Line Interface for CodeExplainer

This module handles all command-line interactions and orchestrates
the entire analysis workflow.
"""

import click
import sys
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from loguru import logger

from .core.analyzer import ProjectAnalyzer
from .utils.config import load_config
from .utils.validators import validate_project_path


console = Console()


@click.command()
@click.argument("project_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(path_type=Path),
    help="Directory where explanations will be saved (default: project_path/_explained)",
)
@click.option(
    "--config-file",
    "-c",
    type=click.Path(exists=True, path_type=Path),
    help="Path to custom configuration file",
)
@click.option(
    "--include-patterns",
    "-i",
    multiple=True,
    help="File patterns to include (can be used multiple times)",
)
@click.option(
    "--exclude-patterns",
    "-e",
    multiple=True,
    help="File patterns to exclude (can be used multiple times)",
)
@click.option(
    "--language",
    "-l",
    help="Override language detection for specific language",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose logging",
)
@click.option(
    "--no-audio",
    is_flag=True,
    help="Skip generating audio scripts",
)
@click.version_option(version="1.0.0", prog_name="CodeExplainer")
def main(
    project_path: Path,
    output_dir: Optional[Path],
    config_file: Optional[Path],
    include_patterns: tuple,
    exclude_patterns: tuple,
    language: Optional[str],
    verbose: bool,
    no_audio: bool,
) -> None:
    """
    Analyze a software project and generate beginner-friendly explanations.
    
    PROJECT_PATH: Path to the root folder of your software project
    
    Example:
        codeexplainer ./my-python-project
        codeexplainer ./my-java-project --output-dir ./explanations
        codeexplainer ./mixed-project --include-patterns "*.py" --include-patterns "*.js"
    """
    
    # Configure logging
    log_level = "DEBUG" if verbose else "INFO"
    logger.remove()
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>"
    )
    
    try:
        # Validate project path
        console.print(f"[bold blue]Analyzing project:[/bold blue] {project_path}")
        validate_project_path(project_path)
        
        # Set default output directory
        if output_dir is None:
            output_dir = project_path / "_explained"
        
        # Load configuration
        config = load_config(config_file)
        
        # Override config with command-line options
        if include_patterns:
            config["file_filters"]["include_patterns"] = list(include_patterns)
        if exclude_patterns:
            config["file_filters"]["exclude_patterns"] = list(exclude_patterns)
        if language:
            config["analysis"]["override_language"] = language
        if no_audio:
            config["output"]["generate_audio_scripts"] = False
        
        # Create analyzer instance
        analyzer = ProjectAnalyzer(config)
        
        # Run analysis with progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Analyzing project...", total=None)
            
            result = analyzer.analyze_project(
                project_path=project_path,
                output_dir=output_dir,
            )
            
            progress.update(task, description="Complete!")
        
        # Show results
        console.print(f"\n[bold green]✓ Analysis complete![/bold green]")
        console.print(f"[blue]Files analyzed:[/blue] {result['files_analyzed']}")
        console.print(f"[blue]Explanations generated:[/blue] {result['explanations_generated']}")
        console.print(f"[blue]Output directory:[/blue] {result['output_dir']}")
        
        # Show project summary location
        summary_file = Path(result['output_dir']) / "00_project_summary.txt"
        console.print(f"\n[bold yellow]📋 Project Summary:[/bold yellow] {summary_file}")
        
    except Exception as e:
        console.print(f"\n[bold red]✗ Error:[/bold red] {str(e)}")
        if verbose:
            console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()