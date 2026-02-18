Fractured Keys is an experimental approach to secure credential storage that avoids traditional single-point vaults.
Instead of keeping an encrypted blob in one place, the data is divided, transformed, and distributed across multiple independent carriers.

This project explores:

- Offline security models — no reliance on online services.

- Redundancy with thresholds — only partial components are required to recover the whole.

- Steganographic concealment — information is embedded where it is least expected.

- Layered cryptography — multiple primitives combined to resist straightforward analysis.

The result is a system that doesn't resemble a password manager in its raw form — the stored material does not look like secrets at all.

Fractured Keys is research-driven, cross-platform, and intended for educational and experimental use.


Key Ideas

- Storage without central vaults.

- Recovery through controlled reconstruction.

- Blending security mechanisms from multiple domains (cryptography, coding theory, image processing).

## Quick Start

### Automated Setup (Recommended)

The project includes automated setup scripts that will check and install all prerequisites automatically:

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Cross-platform (Python):**
```bash
python setup.py
```

### Manual Setup

1. **Install Python 3.7+** (if not already installed)
   - Download from: https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

**Option 1: Smart Launcher (Auto-checks requirements)**
```bash
python launch.py          # Launches GUI (default)
python launch.py --gui    # Explicitly launch GUI
python launch.py --cli    # Launch CLI version
```

**Option 2: Direct Launch**
```bash
# GUI Version
python run_gui.py

# CLI Version
python -m __main__
```

## Requirements

- Python 3.7 or higher
- pip (Python package manager)
- All packages listed in `requirements.txt`:
  - cryptography (>=41.0.0)
  - argon2-cffi (>=21.3.0)
  - pycryptodome (>=3.19.0)
  - Pillow (>=10.0.0)
  - colorama (>=0.4.6)
  - customtkinter (>=5.2.0)
  - pytest (>=7.4.0) - for development/testing

## Troubleshooting

If you encounter issues:

1. **Python not found**: Make sure Python is installed and added to your PATH
2. **pip not found**: Run `python -m ensurepip` or install pip manually
3. **Package installation fails**: Try upgrading pip first: `python -m pip install --upgrade pip`
4. **Permission errors**: On Linux/Mac, you may need to use `pip3` instead of `pip` or use `--user` flag

For more details, see `SETUP.md`.
