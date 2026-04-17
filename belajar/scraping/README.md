# Coretax Scraping Project

This folder contains the Coretax scraping script and the setup instructions for this specific project.

## Requirements

This script uses Python and Selenium to attach to an already-running Chrome browser session.

Required Python packages:

```bash
pip install selenium webdriver-manager
```

If you want to keep the project isolated, install them from the local requirements file:

```bash
pip install -r requirements.txt
```

## Python environment setup (pyenv)

1. Install `pyenv` and dependencies.
2. From this project folder:

```bash
cd /home/luqmanr/workspace/ngajar/web-tutorial/belajar/scraping
pyenv install 3.12.2
pyenv local 3.12.2
```

3. Create a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Chrome setup

**Important:** Chrome must be running with remote debugging enabled BEFORE running the scraper script. You cannot use the default Chrome data directory for remote debugging.

### Use a separate profile (recommended)

```bash
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-coretax
```

This creates a temporary Chrome profile that won't conflict with your regular browsing.

### Use your default Chrome profile

If you want to use your default Chrome profile with remote debugging, you need to copy it to a temporary location first:

```bash
# Create a temporary directory for the profile copy
mkdir -p /tmp/chrome-debug-profile

# Copy your default profile (adjust path if needed)
cp -r "$HOME/.config/google-chrome/Default" /tmp/chrome-debug-profile/

# Start Chrome with the copied profile
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug-profile
```

> **Warning:** 
> - This copies your profile to a temporary location. Any changes made during the session won't persist to your main profile.
> - Close all other Chrome windows first to avoid conflicts.
> - The temporary profile will be lost when you delete the `/tmp/chrome-debug-profile` directory.

If you want changes to persist, you can copy the profile back after the session:

```bash
# After finishing, copy changes back to default profile
cp -r /tmp/chrome-debug-profile/Default/* "$HOME/.config/google-chrome/Default/"
```

Then run the script from this folder:

```bash
python test_coretax.py
```

## Login flow

1. The script attaches to the existing Chrome session.
2. It opens the Coretax document page.
3. The script waits until you manually log in.
4. After you press Enter, it verifies login status and continues with the scraping logic.

## Notes

- Keep the Chrome browser window open while the script runs.
- Use the same Chrome profile if you need persistent login state.
- If you want to quit before login, type `q` when prompted.
