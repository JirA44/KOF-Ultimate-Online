@echo off
chcp 65001 >nul
title Tuer tous les tests automatiques

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     🛑 ARRÊT DE TOUS LES TESTS AUTOMATIQUES              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo Arrêt de tous les processus Python...
taskkill /F /IM python.exe 2>nul
if %errorlevel%==0 (
    echo   ✓ Processus Python arrêtés
) else (
    echo   - Aucun processus Python trouvé
)

echo.
echo Arrêt de tous les processus du jeu...
taskkill /F /IM KOF_Ultimate_Online.exe 2>nul
taskkill /F /IM Ikemen_GO.exe 2>nul
taskkill /F /IM mugen.exe 2>nul
echo   ✓ Processus du jeu arrêtés

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     ✅ TOUS LES TESTS AUTOMATIQUES SONT ARRÊTÉS          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

pause
