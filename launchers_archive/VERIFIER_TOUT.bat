@echo off
chcp 65001 >nul
title Vérification Installation - KOF Ultimate
cls

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🔍 VÉRIFICATION COMPLÈTE D'INSTALLATION                    ║
echo ║     Vérifie TOUT avant de lancer le jeu                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

python VERIFIER_INSTALLATION.py

pause
