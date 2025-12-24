# CodeExplainer Makefile
# Simplifies common development tasks

.PHONY: help install install-dev test test-coverage lint format type-check clean build upload

# Default target
help:
	@echo "CodeExplainer Development Commands"
	@echo "=================================="
	@echo ""
	@echo "install      - Install the package"
	@echo "install-dev  - Install in development mode"
	@echo "test         - Run tests"
	@echo "test-coverage - Run tests with coverage"
	@echo "lint         - Run linting"
	@echo "format       - Format code"
	@echo "type-check   - Run type checking"
	@echo "clean        - Clean build artifacts"
	@echo "build        - Build the package"
	@echo "upload       - Upload to PyPI"

# Installation targets
install:
	pip install .

install-dev:
	pip install -e ".[dev]"

# Testing targets
test:
	pytest

test-coverage:
	pytest --cov=src/codeexplainer --cov-report=html --cov-report=term

test-verbose:
	pytest -v

# Code quality targets
lint:
	flake8 src/
	flake8 tests/

format:
	black src/
	black tests/
	isort src/
	isort tests/

type-check:
	mypy src/

# Cleanup targets
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete

clean-all: clean
	rm -rf venv/
	rm -rf .venv/
	rm -rf env/
	rm -rf .env/

# Build targets
build:
	python setup.py sdist bdist_wheel

build-check:
	python setup.py check

upload-test:
	python -m twine upload --repository testpypi dist/*

upload:
	python -m twine upload dist/*

# Development helpers
dev-setup:
	pip install -e ".[dev]"
	pre-commit install

run-example:
	python -m codeexplainer examples/sample_project

# Documentation
docs:
	cd docs && make html

# Docker support
docker-build:
	docker build -t codeexplainer:latest .

docker-run:
	docker run -v $(PWD):/workspace codeexplainer:latest /workspace/examples/sample_project

# Performance testing
benchmark:
	python tests/benchmark.py