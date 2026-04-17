# Pyenv Setup and Installing Requirements

This guide explains how to install `pyenv`, create a Python environment for this project, and install the required packages.

## 1. Install pyenv prerequisites
For Debian/Ubuntu-based systems, run:

```bash
sudo apt update
sudo apt install -y build-essential curl git libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl
```

For other Linux distributions or macOS, follow the official pyenv installation instructions at https://github.com/pyenv/pyenv.

## 2. Install pyenv

```bash
curl https://pyenv.run | bash
```

Then add the following lines to your shell profile file (`~/.bashrc`, `~/.zshrc`, or equivalent):

```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Reload the shell:

```bash
source ~/.bashrc
# or
source ~/.zshrc
```

Verify installation:

```bash
pyenv --version
```

## 3. Install a Python version

Choose a Python version that works for your environment. A good default is `3.12.2` or `3.11.6`.

```bash
pyenv install 3.12.2
```

Set that version for this project directory:

```bash
cd /home/luqmanr/workspace/ngajar/web-tutorial
pyenv local 3.12.2
```

This creates a `.python-version` file in the repo root.

## 4. Create and activate a virtual environment (recommended)

If you have `pyenv-virtualenv` installed, create a named environment:

```bash
pyenv virtualenv 3.12.2 webtutorial
pyenv local webtutorial
```

Otherwise, use the local pyenv Python directly:

```bash
python -m venv .venv
source .venv/bin/activate
```

## 5. Install repository requirements

This project does not have a single root requirements file, but the Docker example includes dependencies in:

```bash
belajar/belajar_docker/requirements.txt
```

Install those requirements:

```bash
pip install -r belajar/belajar_docker/requirements.txt
```

## 6. Install extra packages used by scraping scripts

For the web scraping examples in `belajar/scraping`, install:

```bash
pip install requests beautifulsoup4 selenium webdriver-manager
```

If you are using a Chrome browser for Selenium, also install a compatible ChromeDriver or use `webdriver-manager` which downloads it automatically.

## 7. Verify the environment

Check the installed Python and packages:

```bash
python --version
pip list
```

## 8. Optional: Use `pyenv shell` for a temporary environment

If you want to switch versions only for the current terminal session:

```bash
pyenv shell 3.12.2
```

## 9. Notes

- If you use `pyenv local` in the repo root, every time you open a shell inside this folder, that Python version will be active.
- If you use `.venv`, remember to run `source .venv/bin/activate` before working with the project.
- If the script requires additional packages later, install them with `pip install <package>` and optionally add them to a requirements file.
