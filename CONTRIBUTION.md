# Contributing to the template

## ⚠️Contributing Guidelines(!!!)⚠️

- Do not commit directly to `main`.
- Create feature branches off of `develop`.
- Submit pull requests to `develop` only.
- `main` accepts changes only via approved PRs from `develop`.

## Local setup

This repo contains some logic that should be tested, read further if you wich to contribute. We don't use `pyproject.toml` since this repo will not be a package.

1. Make sure you have python3.11 in your global interpreters (it is the supported version for DataBricks). If not:
   ```
   brew install python@3.11
   ```

2. Clone the repo cd into it and create a venv:
   ```bash
   git clone [repo-url]
   cd ds-project-template
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```

3. Check the installation worked properly with:
   ```bash
   which python
   which pip
   ```
   Both should point to the .venv in the project directory.

4. Install dependencies for developing locally:
   ```
   pip install -r contribution_requirements.txt
   ```

5. Run tests
   ```
   pytest
   ```

## Checking out a new version of the template

When you have the template created and you wish to check that everything works fine, 
It means that:
- You have branched off `develop` into a new branch
- You pushed your new branch to github

you can use cookiecutter's `checkout` flag to download the template from your branch

```bash
cookiecutter [THIS-REPO-URL] --checkout [BRANCH_NAME]
```





