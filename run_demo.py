#!/usr/bin/env python3
"""
Demonstration script for CodeExplainer
Shows how the system works without requiring installation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pathlib import Path
from codeexplainer.core.analyzer import ProjectAnalyzer
from codeexplainer.utils.config import Config


def run_demo():
    """Run a demonstration of CodeExplainer."""
    print("🚀 CodeExplainer Demo")
    print("=" * 50)
    
    # Use the sample project
    project_path = Path(__file__).parent / "examples" / "sample_project"
    output_path = Path(__file__).parent / "demo_output"
    
    print(f"📁 Analyzing project: {project_path}")
    print(f"📂 Output directory: {output_path}")
    print()
    
    try:
        # Create analyzer with default config
        config = Config({})
        analyzer = ProjectAnalyzer(config.to_dict())
        
        # Run analysis
        result = analyzer.analyze_project(project_path, output_path)
        
        print("✅ Analysis Complete!")
        print(f"📊 Files analyzed: {result['files_analyzed']}")
        print(f"📝 Explanations generated: {result['explanations_generated']}")
        print()
        
        # Show what was created
        print("📦 Generated Files:")
        print("-" * 30)
        
        for item in output_path.rglob("*.txt"):
            relative_path = item.relative_to(output_path)
            print(f"  📄 {relative_path}")
        
        print()
        print("🎯 Sample Explanation:")
        print("=" * 30)
        
        # Show a sample explanation
        sample_explanation = output_path / "main.py_explanation" / "explanation.txt"
        if sample_explanation.exists():
            content = sample_explanation.read_text()
            # Show first part of the explanation
            lines = content.split('\n')[:20]
            for line in lines:
                print(line)
            print("  ... (continued)")
        
        print()
        print("🔊 Sample Audio Script:")
        print("=" * 30)
        
        # Show a sample audio script
        sample_audio = output_path / "main.py_explanation" / "audio_script.txt"
        if sample_audio.exists():
            content = sample_audio.read_text()
            lines = content.split('\n')[:15]
            for line in lines:
                print(line)
            print("  ... (continued)")
        
        print()
        print("📋 Project Summary:")
        print("=" * 30)
        
        summary_file = output_path / "00_project_summary.txt"
        if summary_file.exists():
            content = summary_file.read_text()
            lines = content.split('\n')[:25]
            for line in lines:
                print(line)
        
        print()
        print("🎉 Demo completed successfully!")
        print()
        print("💡 What you can do next:")
        print("  • Read the full explanations in the demo_output folder")
        print("  • Try CodeExplainer on your own projects")
        print("  • Check out the README.md for more information")
        print("  • Explore the source code to see how it works")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_demo()