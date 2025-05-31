# Makefile

VENV=.venv
PYTHON_VERSION = {{cookiecutter.python_version}}
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: help setup venv install-dev pre-commit clean build

help:
	@echo "{{cookiecutter.directory_name}} repo common tasks:"
	@echo "  make setup        - Create git, venv and install dev dependencies"
	@echo "  make venv         - Create a virtual environment"
	@echo "  make install-dev  - Install in editable mode with [dev] extras"
	@echo "  make pre-commit   - Install and configure pre-commit hooks"
	@echo "  make clean        - Uninstall the build, clean artifacts and delete the venv directory"
	@echo "  make build        - Build the package for distribution."

setup: 
	@echo "🔧 {{cookiecutter.directory_name}} developer setup"
	@echo "⚒️ setting up git (only if it does not exist yet)"
	
	@[ -d .git ] || git init
	
	@$(MAKE) venv
	
	@$(MAKE) install-dev 

	@$(MAKE) pre-commit
	@echo "✅ Setup complete."
	@echo "ℹ️  activate the venv with:"
	@echo "         source .venv/bin/activate"
	@echo "ℹ️  run all tests to check everything is in order with:"
	@echo "         pytest"

venv:
	@echo "⚒️  Creating venv in $(VENV)..." 
	@test -d $(VENV) || python$(PYTHON_VERSION) -m venv $(VENV)
	@echo "🥳 Done."

install-dev:
	@echo "📦 installing dev dependencies"
	$(PIP) install --upgrade pip
	$(PIP) install -e '.[dev]'

pre-commit:
	@echo "⚒️  Setting up pre-commit hooks"
	$(VENV)/bin/pre-commit install
	$(VENV)/bin/pre-commit install --hook-type pre-push

clean:
	@echo "🧹 Removing virtual environment and build artifacts..."
	rm -rf .venv
	rm -rf build dist .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	@echo "✅ Clean complete."

build:
	@echo "🛞 Building wheel..."
	@python -m build --wheel
	@echo "✅ Wheel created in ./dist/"

