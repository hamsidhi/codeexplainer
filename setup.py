"""
CodeExplainer - Setup Script
A tool that analyzes software projects and generates beginner-friendly explanations.
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="codeexplainer",
    version="1.0.0",
    author="CodeExplainer Team",
    author_email="contact@codeexplainer.dev",
    description="Analyzes software projects and generates beginner-friendly explanations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/codeexplainer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Documentation",
        "Topic :: Education",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "codeexplainer=codeexplainer.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "codeexplainer": [
            "config/*.yaml",
            "templates/*.j2",
        ],
    },
)