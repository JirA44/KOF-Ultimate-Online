@echo off
chcp 65001 > nul
title KOF Ultimate - Lancement Propre (SANS IA)

echo ========================================
echo   LANCEMENT KOF ULTIMATE (MODE NORMAL)
echo ========================================
echo.
echo Ce launcher tue tous les scripts AI
echo et lance le jeu en mode joueur normal.
echo.

REM Tuer tous les processus Python (scripts AI)
echo Arrêt des scripts IA en arrière-plan...
taskkill /F /IM python.exe /T >nul 2>&1

REM Attendre un peu
timeout /t 2 >nul

REM Lancer le jeu
echo.
echo Lancement du jeu...
echo.
cd /d "D:\KOF Ultimate Online"
start "" "KOF_Ultimate_Online.exe"

echo.
echo ✓ Jeu lancé!
echo.
echo IMPORTANT: Ne lance PAS les scripts AI si tu veux jouer manuellement!
echo.
pause
