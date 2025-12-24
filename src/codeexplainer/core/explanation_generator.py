from typing import Any, Optional
"""
ExplanationGenerator - Creates beginner-friendly explanations

This module transforms technical analysis results into easy-to-understand
explanations suitable for beginners and audio narration.
"""

import os
from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader, BaseLoader
from loguru import logger

from ..utils.text_utils import simplify_technical_terms, optimize_for_tts
from ..utils.file_utils import sanitize_filename


class ExplanationGenerator:
    """Generates beginner-friendly explanations from code analysis."""
    
    # Templates for different types of explanations
    EXPLANATION_TEMPLATES = {
        "simple_script": """
What this file does:
-------------------
This is a {{ language }} script called "{{ filename }}". It's like a recipe that tells the computer to do a specific task.

Why this file exists:
--------------------
{{ purpose_explanation }}

How it works (in simple steps):
-----------------------------
{% for step in steps %}
{{ loop.index }}. {{ step }}
{% endfor %}

Where input comes from:
----------------------
{{ input_source }}

Where output goes:
-----------------
{{ output_destination }}

How it connects to other files:
------------------------------
{{ connections }}

Key things to know:
------------------
{% for fact in key_facts %}
• {{ fact }}
{% endfor %}

Beginner tip:
------------
{{ beginner_tip }}
""",
        
        "library_module": """
What this file does:
-------------------
This is a {{ language }} module called "{{ filename }}". Think of it like a toolbox full of useful tools (functions) that other parts of the program can use.

Why this file exists:
--------------------
{{ purpose_explanation }}

What's inside this toolbox:
--------------------------
{% if functions %}
Functions (the tools):
{% for func in functions %}
  • {{ func.name }} - {{ func.description }}
{% endfor %}
{% endif %}

{% if classes %}
Blueprints (the templates):
{% for class in classes %}
  • {{ class.name }} - {{ class.description }}
{% endfor %}
{% endif %}

How it connects to other files:
------------------------------
{{ connections }}

How to use this module:
----------------------
{{ usage_example }}

Key things to know:
------------------
{% for fact in key_facts %}
• {{ fact }}
{% endfor %}

Beginner tip:
------------
{{ beginner_tip }}
""",
        
        "configuration": """
What this file does:
-------------------
This is a configuration file called "{{ filename }}". It's like the settings menu for the program - it tells the program how to behave.

Why this file exists:
--------------------
{{ purpose_explanation }}

What settings it controls:
-------------------------
{% for setting in settings %}
• {{ setting.name }}: {{ setting.description }}
{% endfor %}

How it works:
------------
{{ how_it_works }}

Where it's used:
---------------
{{ usage_context }}

Key things to know:
------------------
{% for fact in key_facts %}
• {{ fact }}
{% endfor %}

Beginner tip:
------------
{{ beginner_tip }}
""",
    }
    
    def __init__(self, output_config: dict[str, Any]):
        """
        Initialize the explanation generator.
        
        Args:
            output_config: Configuration for output generation
        """
        self.config = output_config
        
        # Set up Jinja2 template environment
        self.template_env = Environment(
            loader=BaseLoader(),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        logger.info("ExplanationGenerator initialized")
    
    def generate(self, analysis: dict[str, Any], output_dir: Path) -> list[Path]:
        """
        Generate explanations for a file analysis.
        
        Args:
            analysis: Analysis results from FileAnalyzer
            output_dir: Directory where explanations should be saved
            
        Returns:
            List of paths to generated explanation files
        """
        generated_files = []
        
        # Create output directory for this file
        safe_filename = sanitize_filename(analysis["filename"])
        file_output_dir = output_dir / f"{safe_filename}_explanation"
        file_output_dir.mkdir(exist_ok=True)
        
        # Generate beginner-friendly explanation
        explanation_path = self._generate_explanation_text(analysis, file_output_dir)
        if explanation_path:
            generated_files.append(explanation_path)
        
        # Generate audio script if enabled
        if self.config.get("generate_audio_scripts", True):
            audio_script_path = self._generate_audio_script(analysis, file_output_dir)
            if audio_script_path:
                generated_files.append(audio_script_path)
        
        logger.info(f"Generated {len(generated_files)} explanation files in {file_output_dir}")
        return generated_files
    
    def _generate_explanation_text(self, analysis: dict[str, Any], output_dir: Path) -> Optional[Path]:
        """
        Generate a beginner-friendly text explanation.
        
        Args:
            analysis: Analysis results
            output_dir: Directory to save the explanation
            
        Returns:
            Path to the generated file or None if failed
        """
        try:
            # Prepare context for template
            context = self._create_explanation_context(analysis)
            
            # Get appropriate template
            purpose = analysis.get("purpose", "simple_script")
            template_text = self.EXPLANATION_TEMPLATES.get(purpose, self.EXPLANATION_TEMPLATES["simple_script"])
            
            # Render template
            template = self.template_env.from_string(template_text)
            explanation_text = template.render(**context)
            
            # Save to file
            output_path = output_dir / "explanation.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(explanation_text)
            
            logger.debug(f"Generated explanation: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to generate explanation: {e}")
            return None
    
    def _generate_audio_script(self, analysis: dict[str, Any], output_dir: Path) -> Optional[Path]:
        """
        Generate an audio script optimized for text-to-speech.
        
        Args:
            analysis: Analysis results
            output_dir: Directory to save the audio script
            
        Returns:
            Path to the generated file or None if failed
        """
        try:
            # Create audio-optimized explanation
            audio_content = self._create_audio_script_content(analysis)
            
            # Save to file
            output_path = output_dir / "audio_script.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(audio_content)
            
            logger.debug(f"Generated audio script: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to generate audio script: {e}")
            return None
    
    def _create_explanation_context(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """
        Create context dictionary for template rendering.
        
        Args:
            analysis: Analysis results
            
        Returns:
            Context dictionary for templates
        """
        # Determine purpose-based explanations
        purpose = analysis.get("purpose", "simple_script")
        purpose_explanations = self._get_purpose_explanations(analysis, purpose)
        
        # Create steps for how it works
        steps = self._create_explanation_steps(analysis, purpose)
        
        # Determine input/output sources
        input_source = self._determine_input_source(analysis)
        output_destination = self._determine_output_destination(analysis)
        
        # Create connections explanation
        connections = self._create_connections_explanation(analysis)
        
        # Generate key facts
        key_facts = self._generate_key_facts(analysis)
        
        # Create beginner tip
        beginner_tip = self._create_beginner_tip(analysis, purpose)
        
        # Format functions and classes for display
        functions = self._format_functions_for_display(analysis.get("functions", []))
        classes = self._format_classes_for_display(analysis.get("classes", []))
        
        return {
            "filename": analysis["filename"],
            "language": self._get_friendly_language_name(analysis["language"]),
            "purpose_explanation": purpose_explanations,
            "steps": steps,
            "input_source": input_source,
            "output_destination": output_destination,
            "connections": connections,
            "key_facts": key_facts,
            "beginner_tip": beginner_tip,
            "functions": functions,
            "classes": classes,
            "settings": self._extract_settings(analysis),
            "how_it_works": self._explain_how_it_works(analysis),
            "usage_example": self._create_usage_example(analysis),
            "usage_context": self._explain_usage_context(analysis),
        }
    
    def _create_audio_script_content(self, analysis: dict[str, Any]) -> str:
        """
        Create content optimized for text-to-speech.
        
        Args:
            analysis: Analysis results
            
        Returns:
            Audio-optimized text content
        """
        # Get basic context
        context = self._create_explanation_context(analysis)
        
        # Create audio-optimized content
        lines = []
        lines.append(f"Audio explanation for {analysis['filename']}")
        lines.append("=" * 50)
        lines.append("")
        
        # Introduction
        lines.append(f"This is a {context['language']} file called {analysis['filename']}.")
        lines.append("")
        
        # Purpose
        lines.append("What it does:")
        lines.append(context["purpose_explanation"])
        lines.append("")
        
        # How it works (simplified for audio)
        lines.append("How it works:")
        for i, step in enumerate(context["steps"][:3], 1):  # Limit to 3 steps for audio
            lines.append(f"Step {i}: {optimize_for_tts(step)}")
        lines.append("")
        
        # Key connections
        lines.append("Connections to other files:")
        lines.append(optimize_for_tts(context["connections"]))
        lines.append("")
        
        # Important facts (limited for audio)
        lines.append("Important to know:")
        for fact in context["key_facts"][:2]:
            lines.append(f"• {optimize_for_tts(fact)}")
        lines.append("")
        
        # Reading pace instructions
        lines.append("---")
        lines.append("Note: This script is optimized for text-to-speech conversion.")
        lines.append("Numbers and technical terms have been formatted for better pronunciation.")
        
        return "\n".join(lines)
    
    def _get_purpose_explanations(self, analysis: dict[str, Any], purpose: str) -> str:
        """Get purpose explanation based on file type."""
        filename = analysis["filename"]
        language = analysis["language"]
        
        purpose_explanations = {
            "main_program": f"This is the main program file. When you run the {language} program, this is where it starts. It's like the front door of a house - everything begins here.",
            "library_module": f"This file contains useful functions and tools that other parts of the program can use. Think of it like a toolbox - it doesn't do anything by itself, but other files can borrow its tools to get their jobs done.",
            "configuration": f"This file contains settings and preferences for the program. It's like the settings menu on your phone - it tells the program how to behave without changing the actual code.",
            "test_file": f"This file contains tests to make sure the program works correctly. It's like a practice test before the real exam - it checks that everything is working as expected.",
            "data_model": f"This file defines how data is organized and structured. Think of it like a blueprint for a building - it describes what information the program will work with.",
            "utility_functions": f"This file contains helper functions that make common tasks easier. It's like having a Swiss Army knife - lots of useful tools in one place.",
            "simple_script": f"This is a {language} script that performs a specific task. It's like a simple recipe - it follows steps to get something done.",
        }
        
        return purpose_explanations.get(purpose, purpose_explanations["simple_script"])
    
    def _create_explanation_steps(self, analysis: dict[str, Any], purpose: str) -> list[str]:
        """Create step-by-step explanation of how the file works."""
        steps = []
        
        # Generic steps based on purpose
        if purpose == "main_program":
            steps = [
                "The program starts and loads any necessary tools (imports)",
                "It reads any input or settings it needs",
                "It performs the main task using functions and logic",
                "It shows results or saves them somewhere",
            ]
        elif purpose == "library_module":
            steps = [
                "Other files can import this module to use its tools",
                "The module provides functions they can call",
                "Each function does a specific job and returns results",
                "The calling file gets the results and continues its work",
            ]
        elif purpose == "configuration":
            steps = [
                "The program reads this file when it starts",
                "It gets the settings and preferences from here",
                "The settings control how the program behaves",
                "Different settings can change the program's behavior",
            ]
        else:
            steps = [
                "The code is organized into logical sections",
                "It uses variables to store information",
                "Functions perform specific tasks when called",
                "The code follows instructions step by step",
            ]
        
        return steps
    
    def _determine_input_source(self, analysis: dict[str, Any]) -> str:
        """Determine where the file gets its input from."""
        filename = analysis["filename"]
        dependencies = analysis.get("dependencies", [])
        
        input_sources = [
            "User input (when someone types something)",
            "Files on the computer",
            "The internet or a database",
            "Other parts of the program",
        ]
        
        if "input" in filename.lower() or "read" in filename.lower():
            return "This file reads information from files or user input"
        elif dependencies:
            return f"This file gets information from other modules: {', '.join(dependencies[:2])}"
        else:
            return "This file gets its input from user interactions or other parts of the program"
    
    def _determine_output_destination(self, analysis: dict[str, Any]) -> str:
        """Determine where the file sends its output."""
        filename = analysis["filename"]
        
        if "output" in filename.lower() or "write" in filename.lower():
            return "This file writes results to files or displays them on screen"
        elif "log" in filename.lower():
            return "This file records information in log files"
        else:
            return "This file returns results to other parts of the program or displays them to users"
    
    def _create_connections_explanation(self, analysis: dict[str, Any]) -> str:
        """Explain how this file connects to others."""
        dependencies = analysis.get("dependencies", [])
        functions = analysis.get("functions", [])
        classes = analysis.get("classes", [])
        
        connections = []
        
        if dependencies:
            connections.append(f"Uses tools from: {', '.join(dependencies[:3])}")
        
        if functions:
            connections.append(f"Provides {len(functions)} functions that other files can use")
        
        if classes:
            connections.append(f"Defines {len(classes)} blueprints (classes) for creating objects")
        
        if not connections:
            connections.append("This file works independently but is part of the larger program")
        
        return "; ".join(connections)
    
    def _generate_key_facts(self, analysis: dict[str, Any]) -> list[str]:
        """Generate key facts about the file."""
        facts = []
        metrics = analysis.get("metrics", {})
        structure = analysis.get("structure", {})
        
        # Basic metrics
        if metrics.get("lines"):
            facts.append(f"This file has {metrics['lines']} lines of code")
        
        # Programming style
        if structure.get("has_classes"):
            facts.append("It uses object-oriented programming (organizes code into objects)")
        elif structure.get("has_functions"):
            facts.append("It uses functions to organize code into reusable pieces")
        
        # Complexity
        if metrics.get("complexity", {}).get("score"):
            complexity_score = metrics["complexity"]["score"]
            if complexity_score < 5:
                facts.append("This is a relatively simple file")
            elif complexity_score < 15:
                facts.append("This file has moderate complexity")
            else:
                facts.append("This is a complex file with many interconnected parts")
        
        # Add language-specific facts
        language = analysis.get("language", "")
        if language == "python":
            facts.append("It's written in Python, known for being beginner-friendly")
        elif language == "javascript":
            facts.append("It's written in JavaScript, commonly used for websites")
        elif language == "java":
            facts.append("It's written in Java, used for many enterprise applications")
        
        return facts
    
    def _create_beginner_tip(self, analysis: dict[str, Any], purpose: str) -> str:
        """Create a helpful tip for beginners."""
        tips = {
            "simple_script": "Start by reading the code from top to bottom. Each line happens in order, like following a recipe.",
            "library_module": "Don't worry if you don't understand everything at once. Focus on understanding what each function does, not how it does it.",
            "configuration": "Configuration files are usually safe to modify. Just make sure to save a backup copy first!",
            "main_program": "This is where the action starts! Try running this file to see what happens.",
            "test_file": "Tests help ensure the code works correctly. Reading tests can also help you understand what the code is supposed to do.",
        }
        
        return tips.get(purpose, "Take your time and don't be afraid to experiment. The best way to learn is by trying things out!")
    
    def _get_friendly_language_name(self, language: str) -> str:
        """Convert technical language name to friendly name."""
        friendly_names = {
            "python": "Python",
            "javascript": "JavaScript",
            "typescript": "TypeScript",
            "java": "Java",
            "cpp": "C++",
            "c": "C",
            "go": "Go",
            "rust": "Rust",
            "ruby": "Ruby",
            "php": "PHP",
            "swift": "Swift",
            "kotlin": "Kotlin",
            "bash": "Bash",
            "powershell": "PowerShell",
            "sql": "SQL",
            "json": "JSON",
            "yaml": "YAML",
            "html": "HTML",
            "css": "CSS",
        }
        
        return friendly_names.get(language, language.title())
    
    def _format_functions_for_display(self, functions: list[Dict]) -> list[dict[str, str]]:
        """Format functions for display in explanations."""
        formatted = []
        
        for func in functions[:5]:  # Limit to first 5 functions
            name = func.get("name", "unknown")
            params = func.get("parameters", [])
            
            if params:
                desc = f"Takes {len(params)} input{'s' if len(params) > 1 else ''}: {', '.join(params)}"
            else:
                desc = "Performs a task without needing any input"
            
            formatted.append({
                "name": name,
                "description": desc
            })
        
        return formatted
    
    def _format_classes_for_display(self, classes: list[Dict]) -> list[dict[str, str]]:
        """Format classes for display in explanations."""
        formatted = []
        
        for cls in classes[:3]:  # Limit to first 3 classes
            name = cls.get("name", "unknown")
            inherits = cls.get("inherits", [])
            
            if inherits:
                desc = f"Based on: {', '.join(inherits)}"
            else:
                desc = "Creates objects with specific properties and behaviors"
            
            formatted.append({
                "name": name,
                "description": desc
            })
        
        return formatted
    
    def _extract_settings(self, analysis: dict[str, Any]) -> list[dict[str, str]]:
        """Extract settings from configuration files."""
        # This is a simplified version - in production, you'd parse the actual config
        return [
            {"name": "Setting 1", "description": "Controls basic behavior"},
            {"name": "Setting 2", "description": "Affects performance or output"},
        ]
    
    def _explain_how_it_works(self, analysis: dict[str, Any]) -> str:
        """Explain how the file works."""
        return "This file contains instructions that the computer follows step by step."
    
    def _create_usage_example(self, analysis: dict[str, Any]) -> str:
        """Create a usage example."""
        filename = analysis["filename"]
        language = analysis["language"]
        
        if language == "python":
            return f"Other Python files can use this module by writing: import {filename.replace('.py', '')}"
        elif language == "javascript":
            return f"Other JavaScript files can import this with: const myModule = require('./{filename}')"
        else:
            return "Other parts of the program can use the functions and tools provided by this file."
    
    def _explain_usage_context(self, analysis: dict[str, Any]) -> str:
        """Explain where this file is used."""
        return "This file is used throughout the project to provide necessary functionality and settings."