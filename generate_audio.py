#!/usr/bin/env python3
import pyttsx3
import os
import glob
import threading
import time

def generate_mp3_silent(engine, text, mp3_file):
    """Generate MP3 without blocking/hanging"""
    try:
        engine.save_to_file(text, mp3_file)
        engine.runAndWait()
        return True
    except:
        return False

def generate_audio(folder='voice-rag-system_clean'):
    print(f"🎤 Generating HUMAN VOICE MP3s in {folder}/")
    
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 0.9)
    
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'david' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            print(f"🎤 Using: {voice.name}")
            break
    
    audio_files = glob.glob(f'{folder}/**/*_explanation/audio_script.txt', recursive=True)
    if not audio_files:
        print(f"❌ No audio_script.txt in {folder}")
        return
    
    generated = 0
    for txt_file in audio_files:
        mp3_file = txt_file.replace('audio_script.txt', 'explanation.mp3')
        if os.path.exists(mp3_file):
            os.remove(mp3_file)
        
        with open(txt_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # NON-BLOCKING generation
        thread = threading.Thread(target=generate_mp3_silent, args=(engine, text, mp3_file))
        thread.start()
        thread.join(timeout=10)  # 10s timeout per file
        
        if os.path.exists(mp3_file) and os.path.getsize(mp3_file) > 1000:
            print(f"✅ {mp3_file}")
            generated += 1
        else:
            print(f"⚠️ Skipped {mp3_file}")
    
    print(f"\n🎉 {generated} MP3s created!")
    print(f"🎵 explorer \"{folder}\"")

if __name__ == "__main__":
    import sys
    folder = sys.argv[1] if len(sys.argv) > 1 else 'voice-rag-system_clean'
    generate_audio(folder)
