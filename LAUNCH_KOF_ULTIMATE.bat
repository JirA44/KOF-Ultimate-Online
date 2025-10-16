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
    start "" "KOF BLACK R.exe"
) else if "%choice%"=="2" (
    echo.
    echo Lancement Ikemen GO...
    cd "Ikemen_GO"
    start "" "Ikemen_GO.exe"
) else (
    echo.
    echo Choix invalide!
    pause
)
