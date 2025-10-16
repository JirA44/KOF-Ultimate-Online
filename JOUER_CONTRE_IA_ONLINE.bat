@echo off
chcp 65001 > nul
title KOF ULTIMATE - Jouer contre IA en ligne

cls
echo ============================================================
echo   🎮 KOF ULTIMATE - MODE NETPLAY VS IA
echo ============================================================
echo.
echo Ce mode lance:
echo   • Session 1: VOUS (Player 1 - Humain)
echo   • Session 2: IA ADVERSAIRE (Player 2 - Automatique)
echo.
echo L'IA joue comme un vrai joueur en ligne!
echo.
echo ============================================================
echo CHOISISSEZ LA DIFFICULTÉ DE L'IA:
echo ============================================================
echo.
echo   [1] 😊 FACILE     - IA fait beaucoup d'erreurs
echo   [2] 😐 MOYEN      - IA joue normalement
echo   [3] 😈 DIFFICILE  - IA très forte
echo.
set /p difficulty="Votre choix (1/2/3): "

if "%difficulty%"=="1" set skill=easy
if "%difficulty%"=="2" set skill=medium
if "%difficulty%"=="3" set skill=hard

if not defined skill (
    echo.
    echo ❌ Choix invalide!
    pause
    exit /b
)

cls
echo ============================================================
echo   🚀 LANCEMENT DU MODE NETPLAY VS IA
echo ============================================================
echo.
echo Difficulté: %skill%
echo.
echo ⏳ Étape 1/3: Lancement du jeu (VOUS)...
echo.

REM Lancer Ikemen GO pour le joueur
cd /d "D:\KOF Ultimate\Ikemen_GO"
start "KOF - Vous" "Ikemen_GO.exe"

echo ✓ Jeu lancé!
echo.
echo ⏳ Attente de 15 secondes pour que le jeu démarre...
timeout /t 15 /nobreak > nul

echo.
echo ⏳ Étape 2/3: Lancement de l'IA adversaire...
echo.
echo ⚠️  IMPORTANT: Ne touchez pas la souris/clavier pendant 20 secondes!
echo    L'IA va sélectionner son personnage automatiquement.
echo.
timeout /t 3 /nobreak > nul

REM Lancer l'IA adversaire
cd /d "D:\KOF Ultimate"
start "IA Adversaire" python ai_netplay_opponent.py --skill %skill% --wait 5

echo.
echo ============================================================
echo   ✓ TOUT EST LANCÉ!
echo ============================================================
echo.
echo 🎮 Session 1: VOUS êtes Player 1
echo 🤖 Session 2: IA est Player 2
echo.
echo L'IA va jouer automatiquement contre vous!
echo.
echo Bon combat! 🥊
echo.
echo ============================================================
echo.
pause
