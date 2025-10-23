@echo off
title KOF Ultimate Online - Quick Launch
cd /d "%~dp0"

echo.
echo ========================================
echo   KOF Ultimate Online
echo   Quick Launch
echo ========================================
echo.

REM Arrêter les scripts IA externes
taskkill /F /IM python.exe /T >nul 2>&1

echo Lancement du jeu...
start "" "KOF_Ultimate_Online.exe"

echo.
echo Jeu lance!
timeout /t 2 >nul
exit
