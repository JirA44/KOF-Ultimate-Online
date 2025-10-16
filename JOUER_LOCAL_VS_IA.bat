@echo off
chcp 65001 > nul
title KOF ULTIMATE - Jouer contre IA Locale

cls
echo ============================================================
echo   🎮 KOF ULTIMATE - MODE LOCAL VS IA
echo ============================================================
echo.
echo Ce mode lance le jeu avec:
echo   • Player 1: VOUS (avec votre manette/clavier)
echo   • Player 2: IA automatique (difficulté paramétrable)
echo.
echo ⚠️  IMPORTANT:
echo   • Utilisez votre MANETTE ou le CLAVIER pour jouer
echo   • L'IA contrôlera Player 2 automatiquement
echo   • Le mapper manette est désactivé pour ce mode
echo.
echo ============================================================
echo CHOISISSEZ LE MOTEUR:
echo ============================================================
echo.
echo   [1] 🥊 M.U.G.E.N (Classique)
echo   [2] 🌐 Ikemen GO (Moderne)
echo.
set /p engine="Votre choix (1/2): "

if "%engine%"=="1" set exe=KOF BLACK R.exe& set path_game=D:\KOF Ultimate
if "%engine%"=="2" set exe=Ikemen_GO.exe& set path_game=D:\KOF Ultimate\Ikemen_GO

if not defined exe (
    echo.
    echo ❌ Choix invalide!
    pause
    exit /b
)

cls
echo ============================================================
echo   🚀 LANCEMENT DU JEU
echo ============================================================
echo.
echo ⏳ Démarrage...
echo.

REM Lancer le jeu
cd /d "%path_game%"
start "" "%exe%"

echo ✓ Jeu lancé!
echo.
echo ============================================================
echo   ✓ C'EST PARTI!
echo ============================================================
echo.
echo 🎮 Player 1: VOUS
echo 🤖 Player 2: IA du jeu (sélectionner VS CPU)
echo.
echo Dans le menu du jeu:
echo   1. Sélectionnez "VS CPU" ou "Arcade"
echo   2. Choisissez votre personnage
echo   3. Configurez la difficulté de l'IA
echo   4. Jouez!
echo.
echo ASTUCE: Dans MUGEN, la difficulté de l'IA se configure
echo         dans Options → Game Settings → Difficulty
echo.
echo Bon combat! 🥊
echo.
echo ============================================================
echo.
pause
