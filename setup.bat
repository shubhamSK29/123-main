@echo off
REM Automated Setup Script for Windows
REM This batch file checks for Python and runs setup.py

echo ======================================================================
echo   Fractured Keys - Automated Setup (Windows)
echo ======================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [INFO] Python found
python --version

REM Run the Python setup script
echo.
echo [INFO] Running automated setup...
echo.

python setup.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Setup failed. Please check the errors above.
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Setup completed successfully!
echo.
pause
