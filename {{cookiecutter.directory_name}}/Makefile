# Makefile

VENV=.venv
PYTHON_VERSION = {{cookiecutter.python_version}}
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: help setup venv install-dev pre-commit clean build \
	sync-repo \
	_sync-repo-internal \
	_init-git-and-commit \
	_create-remote-repo-and-push \
	_sync-repo-to-databricks \
	print-databricks-repo-url

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
	@echo "ℹ️  activate the venv with: source .venv/bin/activate"
	@echo "ℹ️  run all tests to check everything is in order with: pytest" 


_init-git-and-commit:
	@echo "⚒️ initating git and commiting first commit ..."
	@git init
	@git add *
	@git add .gitignore
	@git add .pre-commit-config.yaml
	@git commit -m "init"

_create-remote-repo-and-push:
	@echo "⚒️ creating remote ..."
	@gh repo create {{cookiecutter.directory_name}} \
		--private \
		--team pdp-ds \
		--description "{{cookiecutter.description}}" \
		--disable-wiki \
		--disable-issues;

	@echo "⚒️ pushing to remote ..."
	@git remote add origin git@{{cookiecutter.git_host}}:$(gh api user --jq .login)/{{cookiecutter.directory_name}}.git
	@git branch -M main
	@git push -u origin main

_sync-repo-to-databricks:
	@echo "⚒️ syncing with databricks ..."
	@databricks repos create \ 
		--json '{ \
			"url": "https://github.com/$(gh api user --jq .login)/{{cookiecutter.directory_name}}.git", \
			}' \
		--path /Repos/{{cookiecutter.author_email}}/{{cookiecutter.directory_name}}

print-databricks-repo-url:
	@REPO_ROW=$$(databricks repos list | grep "{{cookiecutter.directory_name}}"); \
	if [ -z "$$REPO_ROW" ]; then \
		echo "❌ Repository not found on databricks: $$REPO_NAME"; \
		exit 1; \
	fi; \
	REPO_ID=$$(echo "$$REPO_ROW" | awk '{print $$1}'); \
	DB_HOST_URL=$$(databricks auth describe | grep "Host:" | awk '{print $$2}'); \
	DB_ACCOUNT_ID=$$(echo $$DB_HOST_URL | awk -F'//' '{print $$2}' | awk -F'.' '{print $$1}'); \
	echo "✅ All done, go visit your new repo at:\n\n		$$DB_HOST_URL/browse/folders/$$REPO_ID?o=$$DB_ACCOUNT_ID\n";

_sync-repo-internal:
	@$(MAKE) _init-git-and-commit

	@$(MAKE) _create-remote-repo-and-push

	@$(MAKE) _sync-repo-to-databricks	

	@$(MAKE) print-databricks-repo-url
	

# Will create a git repo, sync it with github, and sync it with databricks
sync-repo:
	@if [ -d .git ]; then \
		$(MAKE) _sync-repo-internal ; \
	else \
		echo "⚠️ git already initiated, aborting."; \
		echo "⚠️ You can delete the .git directory, but make sure you don't have the repo on github and databricks"; \
	fi
	

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

