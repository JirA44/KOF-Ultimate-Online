@echo off
chcp 65001 >nul
title Test Exhaustif - Identification des Crasheurs

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     🔬 TEST EXHAUSTIF - TOUS LES PERSONNAGES             ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Ce test va:
echo   1. Tester CHAQUE personnage contre 3 adversaires
echo   2. Identifier les crasheurs
echo   3. Créer un roster ultra-safe automatiquement
echo.
echo ⏱️  Durée estimée: 10-15 minutes
echo.
pause
echo.

cd /d "D:\KOF Ultimate Online"
python TEST_ALL_CHARACTERS_VS.py

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     ✅ TEST TERMINÉ                                       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Consultez:
echo   - RAPPORT_TEST_EXHAUSTIF.txt
echo   - select_ULTRA_SAFE.def (roster recommandé)
echo.

pause
