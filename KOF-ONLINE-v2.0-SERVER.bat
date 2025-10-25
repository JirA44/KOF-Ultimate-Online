@echo off
title KOF Ultimate Online - Matchmaking Server
echo ========================================
echo   KOF Ultimate Online Server
echo   Matchmaking & Online Services
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

echo [1/3] Checking dependencies...
pip install -q -r requirements_server.txt

echo [2/3] Starting matchmaking server...
echo Server will be available on port 7500
echo Press Ctrl+C to stop the server
echo.

python matchmaking_server_pro.py

if errorlevel 1 (
    echo.
    echo ERROR: Server failed to start!
    echo Check if port 7500 is already in use.
    pause
)
