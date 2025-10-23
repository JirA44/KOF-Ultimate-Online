@echo off
title KOF Ultimate Online - Launcher
echo.
echo ════════════════════════════════════════════════════════════
echo   🎮 KOF ULTIMATE ONLINE - Launcher Principal
echo ════════════════════════════════════════════════════════════
echo.
echo Lancement du launcher graphique...
echo.

python LAUNCHER_DASHBOARD.py

if errorlevel 1 (
    echo.
    echo ❌ Erreur lors du lancement du launcher
    echo.
    echo Alternatives disponibles:
    echo   1. Double-cliquer sur DASHBOARD_KOF.html
    echo   2. Double-cliquer sur KOF_Ultimate_Online.exe
    echo.
    pause
)
