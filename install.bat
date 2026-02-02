@echo off
REM Installation script for Trade Mirroring System (Windows)

echo ========================================
echo Trade Mirroring System - Setup Script
echo ========================================
echo.

REM Check Python version
echo. Checking Python version...
python --version >nul 2>&1 || (
    echo X Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Create virtual environment
echo. Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
echo. Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create necessary directories
echo. Creating directories...
if not exist data mkdir data
if not exist logs mkdir logs
if not exist reports mkdir reports

echo.
echo ========================================
echo. Setup completed successfully!
echo ========================================
echo.
echo To start the application, run:
echo   venv\Scripts\activate.bat
echo   python main.py
echo.
pause
