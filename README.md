# Plarium's DS Project Template

This template is the agreed upon structure for DS projects for Plarium's Data Science team.<br><br>
It allows for:
- Developing sources offline in an IDE of one's choice.
- Working with DataBricks for extra fire-power 🔫.
- Managing virtual environments and dependencies like pros.
- Maintain documentation within the project.

The template is using [cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/index.html).

## Template structure

```
{{cookiecutter.project_name}}
├── data
├── notebooks
│   └── example.ipynb
├── reports
├── src
│   └── {{cookiecutter.project_slug}}
│       ├── __init__.py
│       └── util.py
├── tests
│   ├── __init__.py
│   └── test_util.py
├── __util__.py
├── pyproject.toml
├── pytest.ini
├── Makefile
├── README.md
├── .gitignore
└── .pre-commit-config.yaml
```

### `Makefile`

Standard way to automate actions in a direcory, for more information about make, visit [here](https://makefiletutorial.com/).<br>
Running `make help` will detail the default actions:
```
{{cookiecutter.project_name}} repo common tasks:
  make setup        - Create git, venv and install dev dependencies
  make venv         - Create a virtual environment
  make install-dev  - Install in editable mode with [dev] extras
  make pre-commit   - Install and configure pre-commit hooks
  make clean        - Uninstall the build, clean artifacts and delete the venv directory
  make build        - Build the package for distribution.
```

### Using notebooks

The main idea of this mode of work is to allow for working online and offline.<br>
Locally, we use an ["editable"](https://setuptools.pypa.io/en/latest/userguide/development_mode.html) version which installs the `src` directory under the `cookicutter.project_slug` alias.<br>
Remotely however, we cannot perform an editable install, instead we use the code below at the top of every notebook:

```python
try:
   from __util__ import __attach_src; __attach_src()
except ModuleNotFoundError as e:
   if e.msg != \"No module named '__util__'\":
      raise e
``` 

Locally this code will do nothing. On the remote it will add the `src` path to `sys.path`

### Unit-testing

We encourage the use of unit-testing. As a DS writes code in notebooks, anything reuable should be moved to `src` and should be tested.
We are using [pytest](https://docs.pytest.org/en/stable/) for unittest discovery. The template include a simple unittest to check if everything works.

### `.pre-commit-config.yaml`

Contains [pre-commit](https://pre-commit.com/) hooks.<br>
The hooks we have ensure:<br>
1. [`nbstripout`](https://github.com/kynan/nbstripout) to clean notebooks before they are pushed to a git repo. To keep results, make sure you create a report.
2. Running tests before we push to git.

## Pre-requisites

### What to install

| # | App               | What is it?                                                                                    | Installation instructions            |
|---|-------------------|------------------------------------------------------------------------------------------------|--------------------------------------|
| 1 | `brew`            | macOS package manager, it will help install a lot of stuff                                     | Go [here](https://brew.sh/)          |
| 2 | python3.11        | This will be your global python interpreter<br> the version is aligned with the DataBricks one | ```bash brew install python@3.11 ``` |
| 3 | make              | An automation tool for running tasks                                                           | ```bash brew install make ```        |
| 4 | git               | You should know                                                                                | ```bash brew install git ```         |
| 5 | gh                | GitHub client                                                                                  | ```bash brew install gh ```          |
| 6 | databricks client | Controls your databricks account from command line                                             | ```bash brew tap databricks/tap; brew install databricks``` |
| 7 | cookiecutter      | Allows to create projects from templates                                                       | ```bash python3.11 -m pip install cookiecutter``` |

### Setting up your GitHub account

1. If you have not done so, set a ssh key for github, following the instructions [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

2. Plarium uses SSO for the keys so you will have to authorize it for Plarium-repo. 
   - Go to [github.com](https://github.com/)
   - Under your profile image in the top right, click **Settings** > **SSH and GPG keys**. if your key is configured you should see this: 
![SSH on the Github settings](./readme-images/ssh%20keys.png)

   - Click the `Confgire SSO` drop down menu, and click authorize here:
![Authorization popup](./readme-images/authorization.png)

### Setting up GitHub client

In a terminal, run:

```bash
gh auth login
```
Fill up the interactive form like so:

| # | Question               | Answer |
|---|------------------------|--------|
| 1 | ? Where do you use GitHub? | Choose: `GitHub.com` |
| 2 |  What is your preferred protocol for Git operations on this host? | Choose: `SSH` |
| 3 | ? Upload your SSH public key to your GitHub account? | You should see the path to your ssh key | ? Title for your SSH key: | Use the default `GitHub CLI` |
| 4 | ? How would you like to authenticate GitHub CLI? | Choose `Login with a web browser` |

Follow the rest of the CLI instructions, it will take you to github with a code to verify your account vai Okta.
```bash
! First copy your one-time code: XXXX-YYYY
Press Enter to open https://github.com/login/device in your browser... 
```

A successful message should look like this:
```bash
✓ Authentication complete.
- gh config set -h github.com git_protocol ssh
✓ Configured git protocol
✓ SSH key already existed on your GitHub account: /Users/YOUR-PLARIUM-USERNAME/.ssh/id_mac_key_ed25519.pub
✓ Logged in as YOUR-GITHUB-USERNAME
```

### Syncing GitHub with DataBricks

Create a **Personal Access Token** for DataBricks 
- Go to: **Settings** > **Developer Settings** > **Personal access tokens**
- Choose **Tokens (classic)**. Click **Generate new token** > **Generate new token (classic)**. 
- Under the **Note** write `databricks` 
- Under **Expiration** choose `No Expiration`
- Under **Select Scopes** mark all of the `repo` scope. This is how your screen should look like this: ![pat setup](./readme-images/pat%20setup.png)
- Scroll down and click **Generate token**
- Copy the token from here:![github token](./readme-images/copy%20token.png)
- Click the **Configue SSO** and authorize (like you did with the SSH token).
- Go to databricks, under your profile choose **Settings** > **Linked accounts**
- Under **Git integration**, set **Git provider** to `GitHub`
- Choose **Personal access token**
- Under **Git provider username or email** enter your git username
- Paste the token from github under . Your screen should look like this: ![github token setup](./readme-images/github%20token%20setup.png)
- Click **Save**. Yay! 🥳


### Setting up the DataBricks CLI

In a terminal, run:

```bash
databricks auth login --host https://2358571090677488.8.gcp.databricks.com --profile [PLARIUM EMAIL]
```

Follow the instructions.

## Creating a new project using the template

1. Go to the directory where your project root will be created and run:

    ```bash
    cookiecutter https://github.com/ak-plarium/ds-project-template
    ```

    You will be prompted to fill the details of the project - **Note:** to use an underscore (`_`) instead of a hyphen (`-`) in `project_slug`.
    

2. Next, `cd` into your new project directoy and run `make setup`. <br>
    ```bash
    cd [project_directory]
    make setup
    ```

    This will:<br>
    1. Create a venv
    2. Install requirements from `pyporoject.toml` and the package itself as an editable copy.

3. To test everything has installed properly, activate the venv and run tests.

    ```bash
    source .venv/bin/activate
    pytest
    ```

    You should see that 1 test has passed:
    ```bash
    .                           [100%]
    1 passed in 0.01s
    ```

### Syncing with github and databricks

This is the only place where automation will touch your git, and thus it requires your approval.
In the terminal, run:

```bash
make sync-repo
```

Follow the instructions, it should print a lot of logs and finally show you a link to your databricks repo:

<iframe width="560" height="315" src="https://drive.google.com/file/d/1TPRAH1O-5vMvt889Of2PI0s1_mPCPrvo/view?usp=drive_link" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>



### Test it

1. Go to the repo, choose **notebooks** > **example**
2. Start a machine or choose one that is running. This can take some time... ☕️.
3. Run the 2 cells, it should print "Hello World!". You should see something like this:
![result](./readme-images/toy%20project%20example.png)

## Creating a job on DataBricks that points to your repo and branch

Once your repo is synced, and you have a notebook you want to put in a workflow:

1. On DataBricks go to **Workflows** > **Create** > **Job**
2. Fill up:
   1. Task name
   2. Type: Choose Notebook
   3. Source: Choose Git Provider
      1. Click **Edit**, a pop up form will appear
      2. Paste the github-url
      3. Choose the right git reference for your project (recommended: main branch)
      4. Click **Confirm**
      ![provider info](/readme-images/Git%20provider%20info.png)
      
   4. Path: write the path from the root of the directory: i.e. `notebooks/example` without file extensions
   4. Compute: Choose the right machine for the job (TBD more on this later). Your form should look like this:
   ![form](/readme-images/set%20up%20toy%20job.png)
   5. Click **create task**
   6. On the right hand panel under Schedules and triggers you can schedule or set a trigger. Or.. just click **Run now** and see if the job runs.
   If all works well you should see:
   ![job success](/readme-images/job%20success.png)



