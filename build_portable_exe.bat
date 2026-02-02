@echo off
REM ============================================================================
REM Trade Mirroring App - Portable EXE Builder
REM Creates a standalone .exe for ANY Windows system (no Python required)
REM ============================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ============================================================================
echo  Trade Mirroring App - Building Standalone EXE
echo  This will create an .exe that runs on ANY Windows 10+ system
echo ============================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [1/5] Checking Python installation...
python --version

REM Create virtual environment
echo.
echo [2/5] Creating Python environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate venv
echo [3/5] Installing dependencies...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip and install packages
python -m pip install --quiet --upgrade pip 2>nul
pip install --quiet pyinstaller 2>nul
pip install --quiet -r requirements.txt 2>nul

if errorlevel 1 (
    echo WARNING: Some packages failed to install, continuing anyway...
)

REM Build EXE - ONEFILE (portable, single executable)
echo.
echo [4/5] Building standalone EXE (one-file mode)...
echo This may take 2-3 minutes...
echo.

rmdir /s /q build dist 2>nul
rmdir /s /q build 2>nul

pyinstaller --noconfirm --onefile --windowed ^
  --name "TradeMirrorApp" ^
  --hidden-import=PyQt5.sip ^
  --hidden-import=PyQt5.QtCore ^
  --hidden-import=PyQt5.QtGui ^
  --hidden-import=PyQt5.QtWidgets ^
  --hidden-import=PyQt5.QtNetwork ^
  --add-data "config.py;." ^
  --add-data "data;data" ^
  --add-data "logs;logs" ^
  --add-data "reports;reports" ^
  --distpath "dist" ^
    --workpath "build_temp" ^
  --specpath "build_spec" ^
  --collect-all PyQt5 ^
  main.py

if errorlevel 1 (
    echo.
    echo WARNING: One-file build attempt had issues, trying directory mode...
    echo.
    
        pyinstaller --noconfirm --onedir --windowed ^
      --name "TradeMirrorApp" ^
      --hidden-import=PyQt5.sip ^
      --hidden-import=PyQt5.QtCore ^
      --hidden-import=PyQt5.QtGui ^
      --hidden-import=PyQt5.QtWidgets ^
            --add-data "config.py;." ^
      --add-data "data;data" ^
      --add-data "logs;logs" ^
      --add-data "reports;reports" ^
      --distpath "dist" ^
            --workpath "build_temp" ^
      --specpath "build_spec" ^
      --collect-all PyQt5 ^
      main.py
)

REM Cleanup temp folders
rmdir /s /q build_temp 2>nul
rmdir /s /q build_spec 2>nul

REM Check if build succeeded
echo.
echo [5/5] Verifying build...
echo.

if exist "dist\TradeMirrorApp.exe" (
    echo.
    echo ============================================================================
    echo  SUCCESS! Portable EXE Created
    echo ============================================================================
    echo.
    echo Location: dist\TradeMirrorApp.exe
    echo Size: ~200-250 MB (includes all dependencies)
    echo.
    echo You can NOW:
    echo  1. Run it: dist\TradeMirrorApp.exe
    echo  2. Copy to USB and run on ANY Windows 10+ computer
    echo  3. Share the .exe file with others
    echo  4. No Python needed on target PC!
    echo.
    echo ============================================================================
) else if exist "dist\TradeMirrorApp\TradeMirrorApp.exe" (
    echo.
    echo ============================================================================
    echo  SUCCESS! Portable App Directory Created
    echo ============================================================================
    echo.
    echo Location: dist\TradeMirrorApp\ (folder)
    echo.
    echo You can NOW:
    echo  1. Run it: dist\TradeMirrorApp\TradeMirrorApp.exe
    echo  2. Copy the ENTIRE folder to USB and run on ANY Windows 10+ computer
    echo  3. Share the folder with others
    echo  4. No Python needed on target PC!
    echo.
    echo Note: Make sure to copy the entire folder, not just the .exe
    echo ============================================================================
) else (
    echo.
    echo ============================================================================
    echo  ERROR: Build failed!
    echo ============================================================================
    echo.
    echo Possible solutions:
    echo  1. Make sure you have enough disk space (2 GB)
    echo  2. Close antivirus temporarily during build
    echo  3. Run Command Prompt as Administrator
    echo  4. Try manual build (see BUILD_EXE.md)
    echo.
)

echo.
pause
