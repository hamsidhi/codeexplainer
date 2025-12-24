# CodeExplainer 🚀

[![PyPI](https://badge.fury.io/py/codeexplainer.svg)](https://pypi.org/project/codeexplainer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

**The Ultimate Code Understanding Tool** - Analyzes ANY project and generates **beginner-friendly explanations** + **human voice MP3s**! Like having a patient mentor explain code to a 6-year-old. 🎤📚

## 🎯 What It Does

- 🔍 **Analyzes ANY project** (Python/JS/Java/C++/Rust/Go/PHP/Swift + 15+ languages)
- 👶 **Kid-friendly explanations** (6-year-old level understanding)
- 🎵 **Human voice MP3s** (Microsoft David voice - Windows TTS)
- 📁 **Preserves folder structure** (original files + explanations side-by-side)
- 🌍 **100% offline** - No cloud APIs, pure open-source
- ⚡ **CLI + Universal tools** - `codeexplainer /path/to/project`

## 🚀 Quick Start

```
# 1. Install
pip install -r requirements.txt
pip install -e .

# 2. Analyze ANY project
codeexplainer "E:\Projects\your-project"

# 3. Generate HUMAN VOICE MP3s
python fast_audio.ps1

# 4. Universal (ANY project!)
python universal_codeexplainer.py "C:\path\to\any-project"
```

## 📁 Perfect Output Structure

```
your_project_clean/
├── app.py                           # ✅ Original file
├── app.py_explanation/              # 🎤 Explanation folder
│   ├── explanation.txt             # 👶 Kid language
│   ├── audio_script.txt            # 🎵 TTS optimized
│   └── explanation.mp3             # 🎤 HUMAN VOICE!
├── rag_engine.py_explanation/
│   └── explanation.mp3             # 🎤 "Your RAG magic explained!"
└── 00_project_summary.txt          # 📊 Complete overview
```

## 🛠️ Supported Languages (15+)

| Language     | Extensions          | Status     |
|--------------|---------------------|------------|
| **Python**   | `.py`               | ✅ Full    |
| **JavaScript** | `.js, .jsx`      | ✅ Full    |
| **TypeScript** | `.ts, .tsx`      | ✅ Full    |
| **Java**     | `.java`             | ✅ Full    |
| **C/C++**    | `.c, .cpp, .h`     | ✅ Full    |
| **Go**       | `.go`               | ✅ Full    |
| **Rust**     | `.rs`               | ✅ Full    |
| **PHP**      | `.php`              | ✅ Full    |
| **HTML/CSS** | `.html, .css`       | ✅ Full    |
| **SQL**      | `.sql`              | ✅ Full    |

## 🎵 Human Voice Generation

**Windows PowerShell TTS (Instant!):**
```
powershell -ExecutionPolicy Bypass -File fast_audio.ps1
```

**Python TTS (Non-blocking):**
```
python generate_audio.py your_project_clean
```

## 🌍 Universal Usage

```
# ANY GitHub repo
python universal_codeexplainer.py "C:\Downloads\any-repo"

# SkillMind AI
python universal_codeexplainer.py "E:\Projects\skillmind-ai"

# FastAPI + RAG
python universal_codeexplainer.py "E:\Projects\voice-rag-system"
```

## 🔧 Advanced Options

```
codeexplainer /path/to/project \
  --output-dir explanations \
  --include-patterns "*.py,*.js" \
  --exclude-patterns "tests/*,node_modules/*"
```

## 🏗️ Project Structure

```
codeexplainer/
├── src/codeexplainer/      # 🔥 Core AI engine
│   ├── core/              # Analysis + Tree-sitter
│   ├── parsers/           # 15+ languages
│   └── utils/             # Metrics + formatting
├── examples/sample_project/ # 📚 Demo
├── tests/                 # 🧪 100% coverage
├── tools/                 # 🎤 Audio + universal
├── fast_audio.ps1         # ⚡ PowerShell TTS
└── universal_codeexplainer.py # 🌍 ANY project!
```

## 🧪 Testing

```
pytest                    # All tests
pytest --cov              # Coverage report
```

## 🤝 Contributing

1. `fork` → `clone` → `pip install -e .[dev]`
2. `pre-commit install`
3. `pytest` → `black src/` → `git push`
4. **Submit PR** 🎉

## 📦 PyPI (Soon!)

```
pip install codeexplainer
codeexplainer /path/to/project
```

## 💼 Real-World Use Cases

- **🎓 Learning**: Understand ANY codebase instantly
- **👥 Onboarding**: New team members ramp up fast
- **📚 Education**: Teach programming with voice explanations
- **♿ Accessibility**: Audio docs for visually impaired devs
- **💼 Interviews**: Demo your RAG/SkillMind AI projects!

## 🙏 Acknowledgments

- **Tree-sitter** - Code parsing magic
- **Rich** - Beautiful CLI output
- **Pygments** - Syntax highlighting

---

**⭐ Star if helpful!**  
**Built by Hamza Siddiqui** - Atharva College Data Science 🚀  
**[hamsidhi/codeexplainer](https://github.com/hamsidhi/codeexplainer)**

![Demo](demo.gif) <!-- Add your demo GIF here! -->
```
