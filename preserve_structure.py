#!/usr/bin/env python3
"""
CLEAN Version - Only source files + explanations (no .venv junk!)
"""
import os
import shutil
from pathlib import Path

def clean_preserve_structure(input_dir, output_dir, original_project_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    original_path = Path(original_project_dir)
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    # SKIP JUNK FOLDERS
    skip_patterns = ['.venv', '__pycache__', '.git', 'node_modules', '.pytest_cache']
    
    copied = 0
    for original_file in original_path.rglob('*'):
        if original_file.is_file():
            relative_path = original_file.relative_to(original_path)
            
            # SKIP JUNK
            if any(skip in str(relative_path).lower() for skip in skip_patterns):
                continue
                
            # Only source files + docs
            if not (original_file.suffix in ['.py', '.md', '.yaml', '.json', '.txt', '.html', '.css', '.js']):
                continue
            
            output_file = output_path / relative_path
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(original_file, output_file)
            print(f"✅ {relative_path}")
            copied += 1
            
            # Add explanation folder
            file_name = original_file.name
            explanation_folder = input_path / f"{file_name}_explanation"
            if explanation_folder.exists():
                output_explanation = output_file.parent / f"{file_name}_explanation"
                if output_explanation.exists():
                    shutil.rmtree(output_explanation)
                shutil.copytree(explanation_folder, output_explanation)
                print(f"   🎤 {file_name}_explanation/")
    
    print(f"\n🎉 CLEAN structure: {copied} files + explanations in {output_dir}")

if __name__ == "__main__":
    clean_preserve_structure(
        'voice-rag-system_explanations',
        'voice-rag-system_clean',
        'E:\\Projects\\voice-rag-system'
    )
