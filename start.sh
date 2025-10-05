#!/bin/bash

echo "================================================"
echo "Starting Agent Saad"
echo "================================================"
echo ""

if [ -d "venv" ]; then
    source venv/bin/activate
    python run.py
else
    echo "Virtual environment not found!"
    echo "Please run ./install.sh first."
fi

