@echo off
echo ================================================
echo Starting Agent Saad
echo ================================================
echo.

if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    python run.py
) else (
    echo Virtual environment not found!
    echo Please run install.bat first.
    pause
)

