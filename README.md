# CodeExplainer 🚀

**The Ultimate Code Understanding Tool for Beginners**

CodeExplainer is a powerful, open-source tool that analyzes any software project and generates beginner-friendly explanations for every file. It's like having a patient mentor who explains code in simple terms that even a 6-year-old can understand!

## 🎯 What It Does

- **Analyzes** any software project recursively
- **Explains** what each file does in simple language
- **Generates** audio scripts optimized for text-to-speech
- **Creates** a comprehensive project summary
- **Supports** all major programming languages
- **Works** completely offline with 100% open-source tools

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/codeexplainer.git
cd codeexplainer

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Basic Usage

```bash
# Analyze a project
codeexplainer /path/to/your/project

# Specify output directory
codeexplainer /path/to/project --output-dir /path/to/explanations

# Include only specific file types
codeexplainer /path/to/project --include-patterns "*.py" --include-patterns "*.js"

# Skip audio scripts
codeexplainer /path/to/project --no-audio
```

## 📁 What You Get

For each file in your project, CodeExplainer creates a folder containing:

### 1. `explanation.txt` - Beginner-Friendly Explanation

```
What this file does:
-------------------
This is a Python script called "calculator.py". It's like a recipe that 
tells the computer how to do math calculations.

Why this file exists:
--------------------
This file contains useful math functions that other parts of the program 
can use to perform calculations like addition, subtraction, multiplication, 
and division.

How it works (in simple steps):
-----------------------------
1. The file defines different math functions (tools)
2. Each function takes numbers as input
3. The function does the calculation
4. The function gives back the answer

Where input comes from:
----------------------
Other parts of the program call these functions and give them numbers to work with.

Where output goes:
-----------------
The calculated results go back to whatever part of the program asked for them.

How it connects to other files:
------------------------------
Other Python files can import this module and use its math functions.

Key things to know:
------------------
• This file has 5 functions for different math operations
• It's written in Python, known for being beginner-friendly
• Each function is like a separate calculator button

Beginner tip:
------------
Start by reading the code from top to bottom. Each line happens in order, 
like following a recipe.
```

### 2. `audio_script.txt` - Text-to-Speech Optimized

```
Audio explanation for calculator.py
==================================================

This is a Python file called calculator dot P Y.

What it does:
This file is like a collection of math tools. It contains functions that can add, 
subtract, multiply, and divide numbers.

How it works, step by step:
Step one: The file creates different math functions.
Step two: Other files can borrow these functions when they need to do math.
Step three: Each function takes numbers, does the calculation, and returns the answer.

Connections to other files:
Other Python files can import this file and use its math functions whenever they need 
to do calculations.

Important to know:
This file contains five separate math functions.
It's written in Python, which is known for being easy to read and understand.

Note: This script is optimized for text-to-speech conversion. Numbers and technical 
terms have been formatted for better pronunciation.
```

### 3. `00_project_summary.txt` - Complete Project Overview

A comprehensive summary of the entire project including:
- Total files analyzed
- Programming languages used
- Project structure
- Key findings
- How to navigate the explanations

## 🛠️ Supported Languages

CodeExplainer supports all major programming languages:

| Language | Extensions | Status |
|----------|------------|--------|
| Python | `.py`, `.pyx`, `.pyi` | ✅ Full Support |
| JavaScript | `.js`, `.jsx`, `.mjs` | ✅ Full Support |
| TypeScript | `.ts`, `.tsx` | ✅ Full Support |
| Java | `.java` | ✅ Full Support |
| C/C++ | `.c`, `.cpp`, `.h`, `.hpp` | ✅ Full Support |
| Go | `.go` | ✅ Full Support |
| Rust | `.rs` | ✅ Full Support |
| Ruby | `.rb` | ✅ Full Support |
| PHP | `.php` | ✅ Full Support |
| Swift | `.swift` | ✅ Full Support |
| Kotlin | `.kt` | ✅ Full Support |
| Bash | `.sh` | ✅ Full Support |
| HTML/CSS | `.html`, `.css` | ✅ Full Support |
| JSON/YAML | `.json`, `.yaml` | ✅ Full Support |
| SQL | `.sql` | ✅ Full Support |
| Markdown | `.md` | ✅ Full Support |

## 🔧 Advanced Usage

### Configuration File

Create a `codeexplainer.yaml` file to customize behavior:

```yaml
# Custom configuration
analysis:
  max_file_size_mb: 5
  timeout_seconds: 60

output:
  explanation_style: "detailed"
  generate_audio_scripts: true

file_filters:
  include_patterns:
    - "*.py"
    - "*.js"
  exclude_patterns:
    - "test_*.py"
```

Use the config file:

```bash
codeexplainer /path/to/project --config-file codeexplainer.yaml
```

### Environment Variables

You can also configure CodeExplainer using environment variables:

```bash
export CODEEXPLAINER_ANALYSIS_MAX_FILE_SIZE_MB=5
export CODEEXPLAINER_OUTPUT_EXPLANATION_STYLE="detailed"
export CODEEXPLAINER_LOGGING_LEVEL="DEBUG"
```

## 🏗️ Project Structure

```
codeexplainer/
├── src/
│   └── codeexplainer/
│       ├── core/              # Main analysis engine
│       ├── parsers/           # Language parsers
│       ├── utils/             # Utility functions
│       └── cli.py             # Command-line interface
├── config/                    # Configuration files
├── tests/                     # Test suite
├── docs/                      # Documentation
├── examples/                  # Example projects
├── requirements.txt           # Dependencies
├── setup.py                   # Package setup
└── README.md                  # This file
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/codeexplainer

# Run specific test file
pytest tests/test_analyzer.py
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Make** your changes
4. **Test** your changes: `pytest`
5. **Commit** your changes: `git commit -m 'Add feature'`
6. **Push** to the branch: `git push origin feature-name`
7. **Submit** a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/codeexplainer.git
cd codeexplainer

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Code Style

- Use **Black** for code formatting: `black src/`
- Use **isort** for import sorting: `isort src/`
- Use **flake8** for linting: `flake8 src/`
- Use **mypy** for type checking: `mypy src/`

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Tree-sitter** for the amazing parsing library
- **Rich** for beautiful terminal output
- **Jinja2** for template rendering
- **Loguru** for logging
- **Pygments** for syntax highlighting

## 📚 Examples

Check out the `examples/` directory for sample projects and their generated explanations.

## 🔍 How It Works

1. **Traverse**: Recursively walks through all directories
2. **Detect**: Identifies programming language of each file
3. **Parse**: Uses tree-sitter to analyze code structure
4. **Understand**: Extracts purpose, functions, classes, and dependencies
5. **Explain**: Generates beginner-friendly explanations using templates
6. **Optimize**: Creates audio scripts optimized for text-to-speech
7. **Summarize**: Creates a comprehensive project overview

## 💡 Use Cases

- **Learning**: Understand any codebase quickly
- **Onboarding**: Help new team members get up to speed
- **Documentation**: Generate explanations for legacy code
- **Education**: Teach programming concepts with real examples
- **Accessibility**: Provide audio explanations for visually impaired developers

## 🆘 Support

- **Documentation**: [docs.codeexplainer.dev](https://docs.codeexplainer.dev)
- **Issues**: [GitHub Issues](https://github.com/your-org/codeexplainer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/codeexplainer/discussions)

## 📊 Roadmap

- [ ] **VS Code Extension**: Direct integration with your editor
- [ ] **Web Interface**: Browser-based analysis
- [ ] **Multi-language**: Support for more programming languages
- [ ] **AI Enhancement**: Use LLMs for even better explanations
- [ ] **Team Features**: Collaborative code understanding
- [ ] **API**: REST API for integration with other tools

---

**Made with ❤️ for developers, learners, and educators everywhere!**

*If this project helps you, please give it a ⭐ on GitHub!*#   c o d e e x p l a i n e r  
 