#!/bin/bash
# Build Windows EXE locally using PyInstaller
# Usage: bash build_exe.sh (runs on WSL or cross-platform aware systems)

set -e  # Exit on error

echo ""
echo "=========================================="
echo "Trade Mirroring App - Windows EXE Builder"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found"
    exit 1
fi

# Create/activate venv
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
python -m pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
pip install pyinstaller > /dev/null 2>&1

echo ""
echo "Building Windows EXE..."
echo ""

# Build EXE (note: only works on Windows; on Linux/Mac cross-compilation is limited)
pyinstaller --noconfirm --onefile --windowed \
  --name "TradeMirrorApp" \
  --hidden-import=PyQt5.sip \
  --hidden-import=PyQt5.QtCore \
  --hidden-import=PyQt5.QtGui \
  --hidden-import=PyQt5.QtWidgets \
  --add-data "data:data" \
  --add-data "logs:logs" \
  --add-data "reports:reports" \
  --distpath "./build/dist" \
    --workpath "./build/build" \
  --specpath "./build" \
  main.py

echo ""
echo "=========================================="
if [ -f "build/dist/TradeMirrorApp" ]; then
    echo "SUCCESS: EXE created at: build/dist/TradeMirrorApp"
    echo ""
    echo "You can now:"
    echo "  1. Copy to Windows: build/dist/"
    echo "  2. Run on Windows: TradeMirrorApp.exe"
    echo "  3. Distribute or wrap with installer"
elif [ -d "build/dist/TradeMirrorApp" ]; then
    echo "SUCCESS: App directory created at: build/dist/TradeMirrorApp"
    echo ""
    echo "You can now:"
    echo "  1. Copy to Windows: build/dist/TradeMirrorApp/"
    echo "  2. Run: TradeMirrorApp.exe"
    echo "  3. Distribute or wrap with installer"
else
    echo "FAILED: Build did not complete successfully"
    echo "Check above for error messages"
    exit 1
fi
echo "=========================================="
echo ""
