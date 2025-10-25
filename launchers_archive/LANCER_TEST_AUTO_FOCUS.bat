@echo off
chcp 65001 >nul
title Test Auto avec Focus - KOF Ultimate
cls

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🎮 TEST AUTO AVEC FOCUS FORCÉ                              ║
echo ║     Plus sûr pour vos autres fenêtres                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo ⚠️  Ce test force le focus sur le jeu avant chaque touche
echo ⚠️  Minimisez vos fenêtres importantes avant de lancer
echo.

python TEST_AUTO_AVEC_FOCUS.py

pause
