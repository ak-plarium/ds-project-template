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
    cookiecutter 
    ```
