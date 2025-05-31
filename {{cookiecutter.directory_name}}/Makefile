# Makefile

VENV=.venv
PYTHON_VERSION = {{cookiecutter.python_version}}
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

STYLE_TITLE=\033[1;34m
STYLE_BOLD=\033[1m
STYLE_SUCCESS=\033[1;32m
STYLE_WARNING=\033[1;33m
STYLE_ERROR=\033[1;31m
STYLE_URL=\033[4;34m
STYLE_RESET=\033[0m

.PHONY: help setup venv install-dev pre-commit clean build sync-repo print-databricks-repo-url \
	_sync-repo-internal \
	_init-git-and-commit \
	_create-remote-repo-and-push \
	_sync-repo-to-databricks \
	

help:
	@echo "\n$(STYLE_TITLE){{cookiecutter.directory_name}} repo common tasks:$(STYLE_RESET)"
	@echo "  $(STYLE_BOLD)make setup$(STYLE_RESET)        	- Create venv and install dev dependencies - use this after updating dependencies (it will skip venv creation if already done)"
	@echo "  $(STYLE_BOLD)make venv$(STYLE_RESET)         	- Create a virtual environment"
	@echo "  $(STYLE_BOLD)make install-dev$(STYLE_RESET)  	- Install in editable mode with [dev] extras"
	@echo "  $(STYLE_BOLD)make pre-commit$(STYLE_RESET)   	- Install and configure pre-commit hooks"
	@echo "  $(STYLE_BOLD)make clean$(STYLE_RESET)        	- Uninstall the build, clean artifacts and delete the venv directory"
	@echo "  $(STYLE_BOLD)make build$(STYLE_RESET)        	- Build the package for distribution"
	@echo "  $(STYLE_BOLD)make sync-repo$(STYLE_RESET)    	- Create a git repo, push it to github and sync it with databricks"
	@echo "  $(STYLE_BOLD)make create-cluster$(STYLE_RESET)	- Will create a cluster with this project's runtime dependencies."
	@echo "\n"


setup: 
	@echo "🔧 $(STYLE_TITLE){{cookiecutter.directory_name}} developer setup$(STYLE_RESET)"
	
	@$(MAKE) venv
	
	@$(MAKE) install-dev 

	@echo "✅ $(STYLE_SUCCESS)Setup complete.$(STYLE_RESET)"
	@echo ""
	@echo "ℹ️  activate the venv with:"
	@echo ""
	@echo "		$(STYLE_BOLD)source .venv/bin/activate$(STYLE_RESET)"
	@echo ""
	@echo "ℹ️  run all tests to check everything is in order with:"
	@echo ""
	@echo "		$(STYLE_BOLD)pytest$(STYLE_RESET)"
	@echo ""
	@echo "ℹ️  sync with github and databricks using:" 
	@echo ""
	@echo "		$(STYLE_BOLD)make sync-repo$(STYLE_RESET)"
	@echo ""


_init-git-and-commit:
	@echo "⚒️ $(STYLE_TITLE)initating git and commiting first commit ...$(STYLE_RESET)"
	@git init
	@git add *
	@git add .gitignore
	@git add .pre-commit-config.yaml
	@git commit -m "init"
	@echo "ℹ️  _init-git-and-commit is done"


_create-remote-repo-and-push:
	@echo "⚒️ $(STYLE_TITLE)creating remote ...$(STYLE_RESET)"
	@gh repo create {{cookiecutter.directory_name}} \
		--private \
		--description "{{cookiecutter.description}}" \
		--disable-wiki \
		--disable-issues;

	@echo "⚒️ $(STYLE_TITLE)pushing to remote ...$(STYLE_RESET)"
	@git remote add origin git@{{cookiecutter.git_host}}:$$(gh api user --jq .login)/{{cookiecutter.directory_name}}.git
	@git branch -M main
	@git push -u origin main
	@echo "ℹ️  _create-remote-repo-and-push is done"


_sync-repo-to-databricks:
	@echo "⚒️ $(STYLE_TITLE)syncing with databricks ...$(STYLE_RESET)"
	@_USER_=$$(gh api user --jq .login); \
	echo "{ \n\t\"url\": \"https://github.com/$$_USER_/ds-repo-example.git\",\n\t\"provider\": \"gitHub\"\n }" > _repo.json; \
	databricks repos create --json @_repo.json --path /Repos/aviad.klein@plarium.com/ds-repo-example;
	@rm _repo.json
	@echo "ℹ️  _sync-repo-to-databrick is done"


print-databricks-repo-url:
	@REPO_ROW=$$(databricks repos list | grep "{{cookiecutter.directory_name}}"); \
	if [ -z "$$REPO_ROW" ]; then \
		echo "❌ $(STYLE_ERROR)Repository not found on databricks:$(STYLE_RESET) $$REPO_NAME"; \
		exit 1; \
	fi; \
	REPO_ID=$$(echo "$$REPO_ROW" | awk '{print $$1}'); \
	DB_HOST_URL=$$(databricks auth describe | grep "Host:" | awk '{print $$2}'); \
	DB_ACCOUNT_ID=$$(echo $$DB_HOST_URL | awk -F'//' '{print $$2}' | awk -F'.' '{print $$1}'); \
	echo "✅ $(STYLE_SUCCESS)All done, go visit your new repo at:$(STYLE_RESET)"; \
	echo ""; \
	echo "		$(STYLE_URL)$$DB_HOST_URL/browse/folders/$$REPO_ID?o=$$DB_ACCOUNT_ID$(STYLE_RESET)"; \
	echo "";


_sync-repo-internal:
	@$(MAKE) _init-git-and-commit

	@$(MAKE) _create-remote-repo-and-push

	@$(MAKE) pre-commit

	@$(MAKE) _sync-repo-to-databricks	

	@$(MAKE) print-databricks-repo-url
	

sync-repo:
	@echo ""; \
	echo "⚠️ $(STYLE_WARNING)This make target will:$(STYLE_RESET)"; \
	echo "    (1) Initialize git and commit the initial files."; \
	echo "    (2) Push to a remote repo under the name '{{cookiecutter.directory_name}}'."; \
	echo "    (3) Install pre-commit hooks."; \
	echo "    (4) Sync the repo with databricks into your databricks account."; \
	echo ""; \
	printf "$(STYLE_TITLE)Are you sure you want to continue? [y/n] $(STYLE_RESET)"; \
	read ANSWER; \
	if [ "$$ANSWER" = "n" ]; then \
		echo "⚠️ $(STYLE_WARNING)Aborting.$(STYLE_RESET)"; \
	elif [ "$$ANSWER" = "y" ]; then \
		echo "⚒️ setting up git (only if it does not exist yet)"; \
		if [ ! -d .git ]; then \
			$(MAKE) _sync-repo-internal; \
		else \
			echo "⚠️ $(STYLE_WARNING)git already initiated, aborting.$(STYLE_RESET)"; \
			echo "⚠️ $(STYLE_WARNING)You can delete the .git directory, but make sure you don't have the repo on GitHub and Databricks.$(STYLE_RESET)"; \
		fi; \
	else \
		echo "⚠️ $(STYLE_WARNING)Unrecognized character '$$ANSWER'. Aborting.$(STYLE_RESET)"; \
	fi


venv:
	@echo "⚒️  $(STYLE_TITLE)Creating venv in $(VENV)...$(STYLE_RESET)" 
	@test -d $(VENV) || python$(PYTHON_VERSION) -m venv $(VENV)
	@echo "🥳 Done."


install-dev:
	@echo "📦 $(STYLE_TITLE)installing dev dependencies$(STYLE_RESET)"
	$(PIP) install --upgrade pip
	$(PIP) install -e '.[dev]'


pre-commit:
	@echo "⚒️  $(STYLE_TITLE)Setting up pre-commit hooks$(STYLE_RESET)"
	$(VENV)/bin/pre-commit install
	$(VENV)/bin/pre-commit install --hook-type pre-push


clean:
	@echo "🧹 $(STYLE_TITLE)Removing virtual environment and build artifacts...$(STYLE_RESET)"
	rm -rf .venv
	rm -rf build dist .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	@echo "✅ $(STYLE_SUCCESS)Clean complete.$(STYLE_RESET)"


build:
	@echo "🛞 $(STYLE_TITLE)Building wheel...$(STYLE_RESET)"
	@python -m build --wheel
	@echo "✅ $(STYLE_SUCCESS)Wheel created in:$(STYLE_RESET)"
	@echo ""
	@echo "		$(STYLE_URL)./dist/$(STYLE_RESET)"
	@echo ""


create-cluster:
	@echo "⚒️  $(STYLE_TITLE)Checking if a cluster already exists for this project...$(STYLE_RESET)"
	@CLUSTERS=$$(databricks clusters list | grep "{{cookiecutter.directory_name}}"); \
	CLUSTER_EXISTS=$$(echo $$CLUSTERS | wc -l | xargs) ;\
	if [ "$$CLUSTER_EXISTS" = "0" ]; then \
		echo "ℹ️ $(STYLE_TITLE)Cluster related to '{{cookiecutter.directory_name}}' not found. Creating..."; \
		
	else \
		echo "⚠️ $(STYLE_WARNING)Found these related clusters:$(STYLE_RESET)"; \
		echo ""; \
		echo $$CLUSTERS; \
		echo ""; \
		echo "⚠️ $(STYLE_WARNING) Aborting.$(STYLE_RESET)";
	
