@echo off
chcp 65001 >nul
title Test Rapide - KOF Ultimate
cls

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🧪 TEST RAPIDE DE L'INSTALLATION                           ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo Lancement du vérificateur...
echo.

python IKEMEN_CHECKER.py

echo.
echo ══════════════════════════════════════════════════════════════
echo.

if %ERRORLEVEL% EQU 0 (
    echo ╔══════════════════════════════════════════════════════════════╗
    echo ║  ✅ TOUT EST PARFAIT !                                       ║
    echo ║                                                              ║
    echo ║  Votre installation est prête à jouer !                      ║
    echo ║                                                              ║
    echo ║  Utilisez LAUNCH_MENU.bat pour lancer le jeu                ║
    echo ╚══════════════════════════════════════════════════════════════╝
) else (
    echo ╔══════════════════════════════════════════════════════════════╗
    echo ║  ⚠️  PROBLÈMES DÉTECTÉS                                      ║
    echo ║                                                              ║
    echo ║  Lancez LAUNCH_MENU.bat et choisissez :                     ║
    echo ║  Option 3 - Reconstruire select.def                         ║
    echo ╚══════════════════════════════════════════════════════════════╝
)

echo.
pause
