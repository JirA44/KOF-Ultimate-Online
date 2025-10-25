@echo off
chcp 65001 >nul
title Test Exhaustif - Tous les Personnages
color 0E
cls

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🧪 TEST EXHAUSTIF - TOUS LES PERSONNAGES                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo   Ce test va vérifier CHAQUE personnage individuellement
echo   pour identifier ceux qui causent des crashs.
echo.
echo   📊 Personnages à tester: 124
echo   ⏱️  Durée estimée: 1h40 - 2h00
echo.
echo ══════════════════════════════════════════════════════════════
echo   ⚠️  IMPORTANT
echo ══════════════════════════════════════════════════════════════
echo.
echo   - Laissez le test tourner sans toucher au PC
echo   - Le jeu va se lancer et fermer automatiquement
echo   - Vous pouvez vaquer à vos occupations
echo   - Un rapport sera généré à la fin
echo.
echo ══════════════════════════════════════════════════════════════
echo.

pause

cls
echo.
echo 🚀 Lancement du test exhaustif...
echo.

python TEST_ALL_CHARACTERS.py

echo.
echo ══════════════════════════════════════════════════════════════
echo   ✅ TEST TERMINÉ
echo ══════════════════════════════════════════════════════════════
echo.
echo   Consultez le rapport généré pour voir les résultats.
echo.
pause
