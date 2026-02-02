#!/bin/bash
# Installation script for Trade Mirroring System

echo "========================================"
echo "Trade Mirroring System - Setup Script"
echo "========================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version || { echo "✗ Python 3 is required"; exit 1; }

# Create virtual environment
echo "✓ Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "✓ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "✓ Creating directories..."
mkdir -p data logs reports

# Run application
echo ""
echo "========================================"
echo "✓ Setup completed successfully!"
echo "========================================"
echo ""
echo "To start the application, run:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
