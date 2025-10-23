@echo off
chcp 65001 >nul
title Arrêt Tests Continus - KOF Ultimate
cls

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🛑 ARRÊT DES TESTS CONTINUS                                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo Recherche des processus de test...
echo.

for /f "tokens=2" %%i in ('tasklist /FI "WINDOWTITLE eq Tests Continus KOF" /FO LIST ^| findstr /C:"PID"') do (
    echo Arrêt du processus %%i...
    taskkill /PID %%i /F
)

echo.
echo Fermeture du jeu si ouvert...
wmic process where name="KOF_Ultimate_Online.exe" call terminate 2>nul

echo.
echo ✅ Tests continus arrêtés
echo.

pause
