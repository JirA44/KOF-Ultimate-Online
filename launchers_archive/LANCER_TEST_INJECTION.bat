@echo off
chcp 65001 >nul
title Test Injection Inputs - KOF Ultimate
cls

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🎮 TEST AVEC INJECTION D'INPUTS                            ║
echo ║     Inputs envoyés DIRECTEMENT au jeu                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo ✅ VOS AUTRES FENÊTRES NE SONT PAS AFFECTÉES !
echo ✅ Vous pouvez continuer à travailler normalement
echo.
echo Le test va:
echo   1. Lancer le jeu
echo   2. Envoyer les inputs via Windows Messages
echo   3. Tester tous les menus et le gameplay
echo   4. Générer un rapport
echo.
echo Durée estimée: 2 minutes
echo.

python test_input_injection.py

pause
