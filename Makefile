# Makefile

VENV=.venv
PYTHON_VERSION = 3.11
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: help contributor-setup clean

help:
	@echo "Data Science Project Template repo common tasks:"
	@echo "  make contributor-setup        - venv and install dev dependencies"
	@echo "  make clean                    - clean the directory"


contributor-setup:
	@echo "🔧 Data Science Project Template developer setup"
	@echo "⚒️  Creating venv in $(VENV)..." 
	@test -d $(VENV) || python$(PYTHON_VERSION) -m venv $(VENV)
	
	@echo "📦 installing dev dependencies"
	$(PIP) install --upgrade pip
	$(PIP) install -r contribution_requirements.txt
	@echo "📦 Done installing dev dependencies"

	@echo "⚒️  Setting up pre-commit hooks"
	$(VENV)/bin/pre-commit install
	$(VENV)/bin/pre-commit install --hook-type pre-push
	@echo "⚒️  Done"

	@echo "⚒️  Pointing git's excludesFile to .template_gitignore"
	@git config core.excludesFile .template_gitignore
	@echo "⚒️  Done"

	@echo "✅ Setup complete."
	@echo "ℹ️  activate the venv with:"
	@echo "         source .venv/bin/activate"
	@echo "ℹ️  run all tests to check everything is in order with:"
	@echo "         pytest"

clean:
	@echo "🧹 Removing virtual environment and artifacts..."
	rm -rf .venv
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "✅ Clean complete."