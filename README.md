# Plarium's DS Project Template

This template is the agreed upon structure for DS projects for Plarium's DS.<br>
It allows for developing sources offline in an IDE of one's choice and also allows working with DataBricks for extra fire-power 🔫

The template is using [cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/index.html).

## Template structure

```
├── .gitignore
├── .pre-commit-config.yaml
├── Makefile
├── README.md
├── notebooks
│   ├── _init_.ipynb
│   └── example.ipynb
├── pyproject.toml
├── pytest.ini
├── src
│   └── {{cookiecutter.project_slug}}
│       ├── __init__.py
│       └── util.py
└── tests
    ├── __init__.py
    └── test_util.py
```

### `Makefile`

Standard way to automate actions in a direcory.<br>
Running `make help` will detail the default actions.

### `notebooks/_ini_.ipynb`

Part of the setup to work both locally and remotely with DataBricks.<br>
Every notebook's first cell must include:

```python
%run "./_init_.py"
``` 

This will point the sources path to the `src` directory allowing for importing directly from sources.

Locally, it will have no use. Proper installation using `make setup` will install the sources in ["editable" mode](https://setuptools.pypa.io/en/latest/userguide/development_mode.html).

### pytest

We are using `pytest` for unittest discovery. The template include a simple unittest to check if everything works.

### `.pre-commit-config.yaml`

Contains [`pre-commit`](https://pre-commit.com/) hooks.<br>
The hooks we have ensure:<br>
1. [`nbstripout`](https://github.com/kynan/nbstripout) to clean notebooks before they are pushed to a git repo. To keep results, make sure you create a report.
2. Running tests before we push to git.

## Using the template

1. [Install cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/installation.html) it should NOT be installed in a specific virtual environment, rather it should be installed in the global python you have on your machine.

    ```bash
    pip install cookiecutter
    ```

2. Go to the directory where your project root will be created. No need to perform `mkdir [project-root]`.

    ```bash
    cookiecutter https://github.com/ak-plarium/ds-project-template
    ```

    You will be prompted to fill the details of the project.

3. Next, `cd` into your new project directoy and run `make setup`. <br>
    ```bash
    cd [project_directory]
    make setup
    ```

    This will:<br>
    1. Initiate a git repo (Only if you have not already)
    2. Create a venv
    3. Install requirements from `pyporoject.toml` as an editable copy.
    4. Install pre-commit and setup the local hooks.

4. To test everything has installed properly, activate the venv and run tests.

    ```bash
    source .venv/bin/activate
    pytest
    ```

    You should see:
    ```bash
    .                           [100%]
    1 passed in 0.01s
    ```

## Syncing with DataBricks

WIP

## Contributing to this template

Please contact the DS team.
