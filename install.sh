#!/bin/bash

echo "================================================"
echo "Agent Saad - Installation Script"
echo "================================================"
echo ""

echo "Creating virtual environment..."
python3 -m venv venv

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "================================================"
echo "Installation complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API credentials"
echo "2. Run: python run.py"
echo "3. Open browser to: http://localhost:5000"
echo ""

