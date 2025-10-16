@echo off
title KOF ULTIMATE ONLINE - Launcher Rapide
cd /d "%~dp0"

echo.
echo ========================================
echo   KOF ULTIMATE ONLINE
echo   Launcher Rapide avec Guide
echo ========================================
echo.
echo Lancement...
echo.

REM Ouvrir le visualiseur de personnages dans le navigateur par défaut
start "" "VISUALISEUR_PERSONNAGES_FIXED.html"

REM Attendre 2 secondes
timeout /t 2 /nobreak >nul

REM Lancer le jeu
start "" "KOF_Ultimate_Online.exe"

echo.
echo ========================================
echo   INSTRUCTIONS RAPIDES
echo ========================================
echo.
echo 1. Dans le menu du jeu:
echo    - Choisissez "B - VS MODE"
echo    - PAS "I - WATCH" (c'est IA vs IA)
echo.
echo 2. Selectionnez votre personnage:
echo    - Vous etes Player 1 (curseur rouge)
echo    - Appuyez A ou Bouton 1 pour confirmer
echo.
echo 3. Consultez le visualiseur:
echo    - Alt+Tab pour basculer
echo    - Cherchez votre personnage
echo    - Voyez tous ses coups
echo.
echo ========================================
echo   CONTROLES CLAVIER
echo ========================================
echo.
echo Fleches: Mouvement
echo A: Light Punch
echo S: Medium Punch
echo D: Heavy Punch
echo F: Light Kick
echo G: Medium Kick
echo H: Heavy Kick
echo Enter: Start/Pause
echo.
echo ========================================
echo.
echo Le jeu et le guide sont maintenant ouverts!
echo.
echo Appuyez sur une touche pour fermer cette fenetre...
pause >nul
