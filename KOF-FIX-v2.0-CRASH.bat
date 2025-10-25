@echo off
chcp 65001 >nul
title Correction Crash VS - KOF Ultimate
cls

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🔧 CORRECTION CRASH MODE VS                                ║
echo ║     Retire les personnages problématiques                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Ce script va:
echo   1. Sauvegarder votre select.def actuel
echo   2. Retirer les personnages ultra-complexes
echo   3. Garder seulement les personnages vanilla simples
echo.
echo ⚠️  Ceci devrait corriger le crash en mode VS
echo.

pause

python FIX_CRASH_SELECT_DEF.py

echo.
echo ✅ Correction terminée !
echo.
echo Lancez maintenant le jeu et testez le mode VS.
echo.

pause
