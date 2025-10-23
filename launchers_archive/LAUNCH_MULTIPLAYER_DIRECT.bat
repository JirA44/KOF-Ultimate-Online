@echo off
title KOF Ultimate - Multijoueur
color 0B

echo.
echo ======================================
echo    MULTIJOUEUR BATTLE.NET STYLE
echo ======================================
echo.
echo Lancement de l'interface multijoueur...
echo.

cd /d "%~dp0"
python LAUNCH_ULTIMATE_INTERFACE.py multiplayer

if errorlevel 1 (
    echo.
    echo [ERREUR] Impossible de lancer l'interface
    echo.
    pause
)
