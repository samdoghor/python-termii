# python-termii — Local Setup Guide

A clean and lightweight Python SDK for [Termii](https://termii.com) — send SMS, OTPs, and voice messages effortlessly.

---

## Prerequisites

Before anything else, you'll need:

- A [Termii account](https://accounts.termii.com/#/register) (free to sign up)
- Your **Termii API Key** — found in your dashboard under **Settings → API Keys**
- Git installed on your machine
- Python 3.8 or higher

---

## Step 1 — Install Python

### Windows

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download the latest Python 3.x installer
3. Run the installer — **check the box that says "Add Python to PATH"** before clicking Install
4. Verify the installation:

```bash
python --version
```

### macOS

macOS ships with Python 2 (don't touch it). Install Python 3 via Homebrew:

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Verify
python3 --version
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# Verify
python3 --version
```

---

## Step 2 — Clone the Repository

```bash
git clone https://github.com/samdoghor/python-termii.git
cd python-termii
```

---

## Step 3 — Create a Virtual Environment

A virtual environment keeps your project dependencies isolated — no global pollution, no version conflicts.

### Windows

```bash
python -m venv venv
source venv/Scripts/activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

You'll know it's active when your terminal prompt shows `(venv)` at the front. To deactivate later, just run
`deactivate`.

---

## Step 4 — Install Dependencies

With the virtual environment active, install the project and its dependencies:

The project has a `requirements.txt`, run this:

```bash
pip install -r requirements.txt
```

If you want to install the package itself in editable mode (so you can import it in your scripts), run:

```bash
pip install -e .
```

The `-e` flag installs it in **editable mode**, meaning changes you make to the source code are reflected immediately
without reinstalling.

---

## Step 5 — Set Up Your API Key

Never hardcode your API key in source files. Use an environment variable instead.

### Use a `.env` file (recommended)

Create a `.env` file in the project root:

```
TERMII_API_KEY=your_api_key_here
TERMII_BASE_URL=your_base_url_here
```

> ⚠️ The `.gitignore` already excludes `.env` files. Do **not** commit your API key to version control.

---

## Step 6 — Run the  (Ignoring tests for now)

Ignore this as test case are not yet pushed to the repo.

The project includes a `test/` directory and a `test_data.py` file. Run the tests to confirm everything is wired up
correctly:

```bash
python -m pytest test/
```

Or run the test data file directly:

```bash
python test_data.py
```

If `pytest` isn't installed:

```bash
pip install pytest
python -m pytest test/
```

---

## Step 7 — Using the SDK

Here's a quick example of what using `python-termii` looks like in practice:

create a file named `example.py` in the project root with the following content:

```python
import os
from termii_py import Termii  # adjust import based on actual module structure

# Initialize with your API key
client = Termii(api_key=os.environ.get("TERMII_API_KEY"), base_url=os.environ.get("TERMII_BASE_URL"))

# Send an SMS
response = client.message.send_message(
    to="2348012345678",  # recipient phone number (international format)
    from_="YourSenderID",  # approved sender ID from your Termii dashboard
    message="Hello from python-termii!",
    type="plain",
    channel="generic"
)

print(response)
```

```bash
python example.py
```

there is an already a `test_data.py` file in the repo that you can use as a reference for how to call the SDK methods.

```bash
python test_data.py
```

> **Note:** Phone numbers must be in international format **without** the `+` sign (e.g., `2348012345678` for a Nigerian
> number).

---

## Project Structure

```
python-termii/
├── termii_py/          # Core SDK source code
├── test/               # Test files
├── test_data.py        # Sample test data / quick test runner
├── pyproject.toml      # Project metadata and build config
├── .gitignore
└── LICENSE
```

---

## Common Issues

**`ModuleNotFoundError: No module named 'termii_py'`**
Make sure you ran `pip install -e .` from the project root with your virtual environment active.

**`python: command not found` (macOS/Linux)**
Use `python3` instead of `python`. You can alias it: `alias python=python3`

**API key not being read**
Double-check that you exported the environment variable in the **same terminal session** you're running the script from.
Each new terminal session starts fresh.

**Invalid sender ID**
Sender IDs must be pre-registered and approved in your Termii dashboard before use.

---

## Resources

- [Termii API Documentation](https://developers.termii.com)
- [Termii Dashboard](https://accounts.termii.com)
- [Repository](https://github.com/samdoghor/python-termii)
- [MIT License](./LICENSE)

---

*Built by [Samuel Doghor](https://github.com/samdoghor)*
