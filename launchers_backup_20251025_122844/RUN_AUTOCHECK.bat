@echo off
title KOF Ultimate - Auto-Verification System
color 0A
cls

echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║   KOF ULTIMATE - LANCEMENT AUTO-VERIFICATION         ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

python AUTOCHECK_SYSTEM.py

echo.
echo Appuyez sur une touche pour fermer...
pause > nul
