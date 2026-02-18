#!/bin/bash
# Automated Setup Script for Linux/Mac
# This script checks for Python and runs setup.py

echo "======================================================================"
echo "  Fractured Keys - Automated Setup (Linux/Mac)"
echo "======================================================================"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH"
    echo ""
    echo "Please install Python 3.7+ using your package manager:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  macOS: brew install python3"
    echo "  Or download from: https://www.python.org/downloads/"
    echo ""
    exit 1
fi

echo "[INFO] Python found"
python3 --version

# Check if pip3 is available
if ! command -v pip3 &> /dev/null; then
    echo "[WARNING] pip3 not found. Attempting to install..."
    
    # Try to install pip using ensurepip
    python3 -m ensurepip --upgrade 2>/dev/null || {
        echo "[ERROR] Could not install pip automatically"
        echo "Please install pip manually:"
        echo "  Ubuntu/Debian: sudo apt-get install python3-pip"
        echo "  macOS: python3 -m ensurepip --upgrade"
        exit 1
    }
fi

echo "[INFO] Running automated setup..."
echo ""

# Run the Python setup script
python3 setup.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Setup failed. Please check the errors above."
    exit 1
fi

echo ""
echo "[SUCCESS] Setup completed successfully!"
echo ""
