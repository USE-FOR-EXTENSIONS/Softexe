@echo off
REM Build Windows EXE locally using PyInstaller
REM Usage: build_exe.bat

echo.
echo ==========================================
echo Trade Mirroring App - Windows EXE Builder
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    exit /b 1
)

REM Create/activate venv
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip >nul
pip install -r requirements.txt >nul
pip install pyinstaller >nul

echo.
echo Building Windows EXE...
echo.

REM Build EXE
pyinstaller --noconfirm --onefile --windowed ^
  --name "TradeMirrorApp" ^
  --hidden-import=PyQt5.sip ^
  --hidden-import=PyQt5.QtCore ^
  --hidden-import=PyQt5.QtGui ^
  --hidden-import=PyQt5.QtWidgets ^
  --add-data "%~dp0config.py;." ^
  --add-data "%~dp0data;data" ^
  --add-data "%~dp0logs;logs" ^
  --add-data "%~dp0reports;reports" ^
  --distpath ".\build\dist" ^
    --workpath ".\build\build" ^
  --specpath ".\build" ^
  main.py

if errorlevel 1 (
    echo.
    echo WARNING: One-file build failed, trying directory format...
    echo.
    
    pyinstaller --noconfirm --onedir --windowed ^
      --name "TradeMirrorApp" ^
      --hidden-import=PyQt5.sip ^
      --hidden-import=PyQt5.QtCore ^
      --hidden-import=PyQt5.QtGui ^
      --hidden-import=PyQt5.QtWidgets ^
      --add-data "%~dp0config.py;." ^
      --add-data "%~dp0data;data" ^
      --add-data "%~dp0logs;logs" ^
      --add-data "%~dp0reports;reports" ^
      --distpath ".\build\dist" ^
        --workpath ".\build\build" ^
      --specpath ".\build" ^
      main.py
)

echo.
echo ==========================================
if exist "build\dist\TradeMirrorApp.exe" (
    echo SUCCESS: EXE created at: build\dist\TradeMirrorApp.exe
    echo.
    echo You can now:
    echo  1. Run: build\dist\TradeMirrorApp.exe
    echo  2. Distribute: build\dist\ folder
    echo  3. Install: Wrap with Inno Setup or NSIS
) else if exist "build\dist\TradeMirrorApp" (
    echo SUCCESS: App directory created at: build\dist\TradeMirrorApp
    echo.
    echo You can now:
    echo  1. Run: build\dist\TradeMirrorApp\TradeMirrorApp.exe
    echo  2. Distribute: build\dist\TradeMirrorApp folder
    echo  3. Install: Wrap with Inno Setup or NSIS
) else (
    echo FAILED: Build did not complete successfully
    echo Check above for error messages
)
echo ==========================================
echo.

pause
