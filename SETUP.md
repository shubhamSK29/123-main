# Setup Guide - Fractured Keys

This guide explains how to set up Fractured Keys on any computer, with automatic requirement checking and installation.

## Overview

Fractured Keys includes automated setup scripts that:
- ✅ Check if Python is installed
- ✅ Check if pip is available
- ✅ Install pip automatically if missing
- ✅ Install all required packages from `requirements.txt`
- ✅ Verify installation

## Prerequisites

The only manual prerequisite is **Python 3.7 or higher**. Everything else is handled automatically.

### Installing Python

**Windows:**
1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Complete the installation

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip

# Fedora/RHEL
sudo dnf install python3 python3-pip

# Arch Linux
sudo pacman -S python python-pip
```

**macOS:**
```bash
# Using Homebrew
brew install python3

# Or download from python.org
```

## Automated Setup

### Method 1: Platform-Specific Scripts (Easiest)

**Windows:**
```cmd
setup.bat
```
Double-click `setup.bat` or run it from Command Prompt.

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### Method 2: Python Setup Script (Cross-Platform)

```bash
python setup.py
```

This works on all platforms and provides detailed output.

### Method 3: Smart Launcher (Auto-checks on launch)

The `launch.py` script automatically checks and installs requirements before launching:

```bash
python launch.py          # Launches GUI (checks requirements first)
python launch.py --gui    # Explicitly launch GUI
python launch.py --cli    # Launch CLI version
python launch.py --skip-check  # Skip requirement check
```

## Manual Setup

If you prefer to install manually:

1. **Verify Python:**
   ```bash
   python --version
   # Should show Python 3.7 or higher
   ```

2. **Verify pip:**
   ```bash
   pip --version
   # or
   python -m pip --version
   ```

3. **Install pip if missing:**
   ```bash
   python -m ensurepip --upgrade
   ```

4. **Upgrade pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

5. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

## What Gets Installed

The setup script installs the following packages:

- **cryptography** (>=41.0.0) - Core cryptographic functions
- **argon2-cffi** (>=21.3.0) - Password hashing
- **pycryptodome** (>=3.19.0) - Additional crypto primitives
- **Pillow** (>=10.0.0) - Image processing for steganography
- **colorama** (>=0.4.6) - Colored terminal output
- **customtkinter** (>=5.2.0) - Modern GUI framework
- **pytest** (>=7.4.0) - Testing framework (optional)

## Running the Application

After setup, you can run the application in several ways:

### GUI Version (Recommended)
```bash
python run_gui.py
# or
python launch.py --gui
```

### CLI Version
```bash
python -m __main__
# or
python launch.py --cli
```

## Troubleshooting

### Python Not Found

**Windows:**
- Reinstall Python and make sure "Add Python to PATH" is checked
- Or manually add Python to PATH:
  1. Find Python installation (usually `C:\Python3x` or `C:\Users\YourName\AppData\Local\Programs\Python\Python3x`)
  2. Add to System Environment Variables → Path

**Linux/Mac:**
- Use `python3` instead of `python`
- Install Python if missing: `sudo apt-get install python3` (Linux) or `brew install python3` (Mac)

### pip Not Found

**Windows:**
```bash
python -m ensurepip --upgrade
```

**Linux:**
```bash
sudo apt-get install python3-pip
```

**macOS:**
```bash
python3 -m ensurepip --upgrade
```

### Permission Errors (Linux/Mac)

Use `--user` flag:
```bash
pip install --user -r requirements.txt
```

Or use `sudo` (not recommended):
```bash
sudo pip install -r requirements.txt
```

### Package Installation Fails

1. **Upgrade pip first:**
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Try installing packages individually:**
   ```bash
   pip install cryptography
   pip install argon2-cffi
   # etc.
   ```

3. **Check Python version:**
   ```bash
   python --version
   ```
   Must be 3.7 or higher.

4. **On Windows, try:**
   ```bash
   python -m pip install --upgrade --force-reinstall -r requirements.txt
   ```

### GUI Doesn't Launch

- Make sure `customtkinter` is installed: `pip install customtkinter`
- Check if tkinter is available: `python -m tkinter` (should open a window)
- On Linux, you may need: `sudo apt-get install python3-tk`

### Import Errors

If you see "ModuleNotFoundError":
1. Run setup again: `python setup.py`
2. Verify installation: `pip list`
3. Check if you're using the correct Python interpreter

## Verification

To verify everything is installed correctly:

```bash
python -c "import cryptography; import argon2; import Crypto; import PIL; import colorama; import customtkinter; print('All packages installed successfully!')"
```

## Virtual Environment (Optional but Recommended)

For isolated installation:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Run setup
python setup.py

# Deactivate when done
deactivate
```

## Uninstallation

To remove all installed packages:

```bash
pip uninstall -r requirements.txt -y
```

## Support

If you encounter issues not covered here:
1. Check Python version: `python --version`
2. Check pip version: `pip --version`
3. Try manual installation: `pip install -r requirements.txt`
4. Check error messages for specific package failures
