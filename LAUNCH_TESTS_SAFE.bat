@echo off
REM Lance les tests KOF SANS TOUCHER AU CLAVIER
title Tests KOF - Mode Safe (Sans Keyboard)

cd /d "D:\KOF Ultimate Online"

echo ========================================
echo   TESTS KOF - MODE SAFE
echo   Ce script ne touche PAS votre clavier
echo ========================================
echo.
echo Lancement des tests...
echo.

python AUTO_TEST_MINI_WINDOWS.py

pause
