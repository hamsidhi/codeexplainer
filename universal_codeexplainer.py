#!/usr/bin/env python3
"""
🚀 UNIVERSAL CodeExplainer - Analyze ANY project → Clean structure + Human voice MP3s!
Usage: python universal_codeexplainer.py "E:\Projects\your-project"
"""
import sys
import os
import shutil
import subprocess
from pathlib import Path

def universal_analyze(project_path, output_name="explained_project"):
    """Complete workflow for ANY project"""
    
    project_path = Path(project_path)
    if not project_path.exists():
        print(f"❌ Project not found: {project_path}")
        return
    
    print(f"🚀 Analyzing: {project_path}")
    
    # 1. Analyze with CodeExplainer
    print("📊 Step 1: Analyzing project...")
    subprocess.run([
        'codeexplainer', str(project_path), 
        f'--output-dir', f'{output_name}_raw'
    ])
    
    # 2. Create clean structure
    print("📁 Step 2: Creating clean structure...")
    raw_dir = f'{output_name}_raw'
    clean_dir = f'{output_name}_clean'
    
    # Copy original files (skip junk)
    for src_file in project_path.rglob('*'):
        if src_file.is_file() and src_file.suffix in ['.py', '.md', '.yaml', '.json', '.txt', '.html', '.js', '.css']:
            rel_path = src_file.relative_to(project_path)
            dst_file = Path(clean_dir) / rel_path
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst_file)
            print(f"  ✅ {rel_path}")
    
    # 3. Copy explanations
    for expl_folder in Path(raw_dir).glob('*_explanation'):
        dst_folder = Path(clean_dir) / expl_folder.name
        if dst_folder.exists():
            shutil.rmtree(dst_folder)
        shutil.copytree(expl_folder, dst_folder)
        print(f"  🎤 {expl_folder.name}")
    
    # 4. Generate human voice MP3s
    print("🎵 Step 3: Generating human voice MP3s...")
    os.system(f'python generate_audio.py {clean_dir}')
    
    print(f"\n🎉 COMPLETE! Check: {clean_dir}")
    print(f"📂 Explorer: explorer \"{clean_dir}\"")
    print(f"🎤 Play: start \"{clean_dir}\\*_explanation\\explanation.mp3\"")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python universal_codeexplainer.py \"E:\\Projects\\your-project\"")
        sys.exit(1)
    
    universal_analyze(sys.argv[1])
