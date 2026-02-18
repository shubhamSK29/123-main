#!/usr/bin/env python3
"""
Smart Launcher for Fractured Keys
Automatically checks and installs requirements before launching the application
"""

import sys
import os
import subprocess

def check_and_install_requirements():
    """Check if requirements are installed, install if missing"""
    requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    
    if not os.path.exists(requirements_file):
        print("ERROR: requirements.txt not found!")
        return False
    
    # Read required packages
    required_packages = []
    with open(requirements_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Extract package name (before >=, ==, etc.)
                package_name = line.split('>=')[0].split('==')[0].split(' ')[0]
                required_packages.append(package_name.lower())
    
    # Map package names to import names
    import_map = {
        'cryptography': 'cryptography',
        'argon2-cffi': 'argon2',
        'pycryptodome': 'Crypto',
        'pillow': 'PIL',
        'colorama': 'colorama',
        'customtkinter': 'customtkinter',
        'pytest': 'pytest'
    }
    
    missing_packages = []
    
    # Check each package
    for package in required_packages:
        import_name = import_map.get(package, package)
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package)
    
    # If packages are missing, run setup
    if missing_packages:
        print("=" * 70)
        print("  Missing Requirements Detected")
        print("=" * 70)
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("\nRunning automated setup...")
        print("=" * 70 + "\n")
        
        # Run setup.py
        setup_script = os.path.join(os.path.dirname(__file__), "setup.py")
        if os.path.exists(setup_script):
            result = subprocess.run([sys.executable, setup_script], 
                                  capture_output=False)
            if result.returncode != 0:
                print("\nERROR: Setup failed. Please run setup.py manually.")
                return False
        else:
            # Fallback: install requirements directly
            print("Installing missing packages...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file],
                                  capture_output=False)
            if result.returncode != 0:
                print("\nERROR: Failed to install requirements.")
                return False
    
    return True

def launch_gui():
    """Launch the GUI application"""
    try:
        from fractured_gui import main
        main()
    except ImportError as e:
        print(f"ERROR: Could not import GUI module: {e}")
        print("Please run: python setup.py")
        return False
    except Exception as e:
        print(f"ERROR: Failed to launch GUI: {e}")
        return False
    return True

def launch_cli():
    """Launch the CLI application"""
    try:
        from __main__ import main
        main()
    except ImportError as e:
        print(f"ERROR: Could not import CLI module: {e}")
        print("Please run: python setup.py")
        return False
    except Exception as e:
        print(f"ERROR: Failed to launch CLI: {e}")
        return False
    return True

def main():
    """Main launcher function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fractured Keys Launcher')
    parser.add_argument('--gui', action='store_true', help='Launch GUI application')
    parser.add_argument('--cli', action='store_true', help='Launch CLI application')
    parser.add_argument('--skip-check', action='store_true', help='Skip requirement check')
    
    args = parser.parse_args()
    
    # Check requirements unless skipped
    if not args.skip_check:
        if not check_and_install_requirements():
            sys.exit(1)
    
    # Launch appropriate mode
    if args.gui:
        if not launch_gui():
            sys.exit(1)
    elif args.cli:
        if not launch_cli():
            sys.exit(1)
    else:
        # Default: try GUI first, fallback to CLI
        print("Launching GUI...")
        if not launch_gui():
            print("\nGUI failed, trying CLI...")
            if not launch_cli():
                sys.exit(1)

if __name__ == "__main__":
    main()
