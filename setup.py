#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Setup Script for Fractured Keys
This script automatically checks and installs all prerequisites:
- Python (checks version)
- pip (installs if missing)
- All required packages from requirements.txt
"""

import sys
import subprocess
import os
import platform
import shutil

# Fix Windows console encoding issues
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_status(text, status="INFO"):
    """Print status messages"""
    # Use ASCII-compatible symbols for Windows compatibility
    symbols = {
        "INFO": "[i]",
        "SUCCESS": "[OK]",
        "ERROR": "[X]",
        "WARNING": "[!]"
    }
    print(f"{symbols.get(status, '[*]')} {text}")

def check_python():
    """Check if Python is installed and version is compatible"""
    print_status("Checking Python installation...", "INFO")
    
    if sys.version_info < (3, 7):
        print_status(f"Python 3.7+ required. Found: {sys.version}", "ERROR")
        print_status("Please install Python 3.7 or higher from https://www.python.org/downloads/", "ERROR")
        return False
    
    print_status(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} found", "SUCCESS")
    return True

def check_pip():
    """Check if pip is installed"""
    print_status("Checking pip installation...", "INFO")
    
    try:
        import pip
        pip_version = subprocess.check_output([sys.executable, "-m", "pip", "--version"], 
                                             stderr=subprocess.STDOUT, 
                                             universal_newlines=True)
        print_status(f"pip found: {pip_version.strip()}", "SUCCESS")
        return True
    except (ImportError, subprocess.CalledProcessError):
        print_status("pip not found. Attempting to install...", "WARNING")
        return install_pip()

def install_pip():
    """Install pip if it's missing"""
    try:
        print_status("Downloading get-pip.py...", "INFO")
        import urllib.request
        
        # Download get-pip.py
        get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
        get_pip_path = os.path.join(os.path.dirname(__file__), "get-pip.py")
        
        urllib.request.urlretrieve(get_pip_url, get_pip_path)
        print_status("Installing pip...", "INFO")
        
        # Run get-pip.py
        result = subprocess.run([sys.executable, get_pip_path], 
                              capture_output=True, 
                              text=True)
        
        # Clean up
        if os.path.exists(get_pip_path):
            os.remove(get_pip_path)
        
        if result.returncode == 0:
            print_status("pip installed successfully", "SUCCESS")
            return True
        else:
            print_status(f"Failed to install pip: {result.stderr}", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Error installing pip: {str(e)}", "ERROR")
        print_status("Please install pip manually: https://pip.pypa.io/en/stable/installation/", "WARNING")
        return False

def upgrade_pip():
    """Upgrade pip to the latest version"""
    print_status("Upgrading pip to latest version...", "INFO")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        print_status("pip upgraded successfully", "SUCCESS")
        return True
    except subprocess.CalledProcessError:
        print_status("Could not upgrade pip (continuing anyway)", "WARNING")
        return False

def install_requirements():
    """Install all packages from requirements.txt"""
    requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    
    if not os.path.exists(requirements_file):
        print_status(f"requirements.txt not found at {requirements_file}", "ERROR")
        return False
    
    print_status("Reading requirements.txt...", "INFO")
    print_status("Installing required packages (this may take a few minutes)...", "INFO")
    
    # Try with --user flag first (for permission issues)
    install_flags = ["-r", requirements_file, "--upgrade", "--user"]
    
    try:
        # Install requirements with verbose output
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install"] + install_flags,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print_status("All requirements installed successfully", "SUCCESS")
            return True
        else:
            # If --user fails, try without it (might need admin)
            if "--user" in install_flags:
                print_status("User installation failed, trying system-wide...", "WARNING")
                install_flags.remove("--user")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install"] + install_flags,
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    print_status("All requirements installed successfully", "SUCCESS")
                    return True
            
            print_status("Some packages failed to install", "ERROR")
            print(result.stdout)
            print(result.stderr)
            
            # Try installing packages one by one for better error reporting
            print_status("Attempting to install packages individually...", "INFO")
            return install_requirements_individually(requirements_file)
            
    except Exception as e:
        print_status(f"Error installing requirements: {str(e)}", "ERROR")
        return False

def install_requirements_individually(requirements_file):
    """Install requirements one by one for better error reporting"""
    failed_packages = []
    
    with open(requirements_file, 'r') as f:
        packages = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    
    # Try with --user flag first
    use_user_flag = True
    
    for package in packages:
        print_status(f"Installing {package}...", "INFO")
        try:
            install_cmd = [sys.executable, "-m", "pip", "install", package, "--upgrade"]
            if use_user_flag:
                install_cmd.append("--user")
            
            subprocess.check_call(
                install_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print_status(f"{package} installed", "SUCCESS")
        except subprocess.CalledProcessError:
            # Try without --user if it failed
            if use_user_flag:
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", package, "--upgrade"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    print_status(f"{package} installed", "SUCCESS")
                    use_user_flag = False  # Don't use --user for remaining packages
                    continue
                except subprocess.CalledProcessError:
                    pass
            
            print_status(f"Failed to install {package}", "ERROR")
            failed_packages.append(package)
    
    if failed_packages:
        print_status(f"Failed packages: {', '.join(failed_packages)}", "ERROR")
        print_status("Try running as administrator or use: pip install --user -r requirements.txt", "WARNING")
        return False
    
    return True

def verify_installation():
    """Verify that all critical packages are installed"""
    print_status("Verifying installation...", "INFO")
    
    critical_packages = [
        "cryptography",
        "argon2_cffi",
        "Crypto",  # pycryptodome
        "PIL",  # Pillow
        "colorama",
        "customtkinter"
    ]
    
    missing_packages = []
    
    for package in critical_packages:
        try:
            if package == "Crypto":
                __import__("Crypto")
            elif package == "PIL":
                __import__("PIL")
            elif package == "argon2_cffi":
                __import__("argon2")
            else:
                __import__(package)
            print_status(f"{package} - OK", "SUCCESS")
        except ImportError:
            print_status(f"{package} - MISSING", "ERROR")
            missing_packages.append(package)
    
    if missing_packages:
        print_status(f"Missing packages: {', '.join(missing_packages)}", "ERROR")
        return False
    
    print_status("All critical packages verified", "SUCCESS")
    return True

def main():
    """Main setup function"""
    print_header("Fractured Keys - Automated Setup")
    
    # Check Python
    if not check_python():
        sys.exit(1)
    
    # Check and install pip
    if not check_pip():
        print_status("Cannot proceed without pip. Please install it manually.", "ERROR")
        sys.exit(1)
    
    # Upgrade pip
    upgrade_pip()
    
    # Install requirements
    if not install_requirements():
        print_status("Failed to install some requirements. Please check errors above.", "ERROR")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print_status("Installation verification failed. Some packages may be missing.", "WARNING")
        print_status("You can try running: pip install -r requirements.txt", "INFO")
    
    print_header("Setup Complete!")
    print_status("All prerequisites have been installed successfully.", "SUCCESS")
    print_status("You can now run the application using:", "INFO")
    print_status("  Python CLI: python -m __main__", "INFO")
    print_status("  GUI: python run_gui.py", "INFO")
    print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_status("\nSetup cancelled by user", "WARNING")
        sys.exit(1)
    except Exception as e:
        print_status(f"Unexpected error: {str(e)}", "ERROR")
        sys.exit(1)
