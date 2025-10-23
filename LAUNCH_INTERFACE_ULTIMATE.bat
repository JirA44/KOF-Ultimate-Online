@echo off
title KOF Ultimate - Interface Launcher
color 0B

echo.
echo ======================================
echo    KOF ULTIMATE - LAUNCHER
echo ======================================
echo.
echo Lancement de l'interface modernisee...
echo.

cd /d "%~dp0"
python LAUNCH_ULTIMATE_INTERFACE.py

if errorlevel 1 (
    echo.
    echo [ERREUR] Impossible de lancer le launcher
    echo.
    pause
)
