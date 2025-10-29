@echo off
chcp 65001 >nul
title KOF Ultimate Online - Launcher
cls

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║         ⚔️  KOF ULTIMATE ONLINE - LAUNCHER  ⚔️            ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo.

echo [INFO] Lancement du Launcher Ultimate...
echo.

cd /d "D:\KOF Ultimate Online"

python KOFUO_LAUNCHER_ULTIMATE.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERREUR] Le launcher n'a pas pu démarrer.
    echo.
    echo Vérifications possibles:
    echo   - Python est installé
    echo   - Les dépendances sont installées: pip install websockets
    echo   - Le répertoire est correct
    echo.
    pause
    exit /b 1
)

exit /b 0
