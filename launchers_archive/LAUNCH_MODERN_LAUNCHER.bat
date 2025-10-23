@echo off
title KOF Ultimate Online - Modern Launcher
echo ========================================
echo   KOF Ultimate Online - Modern Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
pip install -q -r requirements_launcher.txt

echo [2/3] Starting modern launcher...
python modern_launcher.py

if errorlevel 1 (
    echo.
    echo ERROR: Launcher failed to start!
    echo Check the error messages above.
    pause
)
