@echo off
chcp 65001 > nul
title KOF ULTIMATE - Launcher

echo ================================
echo   KOF ULTIMATE LAUNCHER
echo ================================
echo.
echo Choisissez le moteur:
echo.
echo [1] M.U.G.E.N (Classique)
echo [2] Ikemen GO (Moderne + Netplay)
echo.
set /p choice="Votre choix (1 ou 2): "

if "%choice%"=="1" (
    echo.
    echo Lancement M.U.G.E.N...
    start "" "KOF_Ultimate_Online.exe"
) else if "%choice%"=="2" (
    echo.
    echo Lancement Launcher Graphique...
    start "" "KOF Ultimate Launcher.exe"
) else (
    echo.
    echo Choix invalide!
    pause
)
