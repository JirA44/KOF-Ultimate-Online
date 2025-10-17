@echo off
chcp 65001 > nul
title KOF Ultimate - Sélection Mode de Jeu

:MENU
cls
echo.
echo ============================================================
echo   🎮 KOF ULTIMATE - SÉLECTION MODE
echo ============================================================
echo.
echo Choisis ton mode de jeu:
echo.
echo   [1] 🥊 Solo vs IA (Mode Normal)
echo       Tu joues P1, l'ordinateur joue P2
echo.
echo   [2] 👥 Versus Local (2 Joueurs)
echo       P1 et P2 sur le même PC
echo.
echo   [3] 🌐 Netplay (En Ligne)
echo       Jouer contre quelqu'un sur internet
echo.
echo   [0] ❌ Quitter
echo.
echo ============================================================
echo.

set /p choice="Ton choix (1, 2, 3 ou 0): "

if "%choice%"=="1" goto SOLO
if "%choice%"=="2" goto VERSUS
if "%choice%"=="3" goto NETPLAY
if "%choice%"=="0" goto END
goto MENU

:SOLO
cls
echo.
echo ============================================================
echo   MODE SOLO vs IA
echo ============================================================
echo.
echo Arrêt des scripts IA externes...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 1 >nul

echo Lancement M.U.G.E.N (Mode Normal)...
echo.
echo Tu contrôles P1, l'IA du jeu contrôle P2.
echo.
cd /d "D:\KOF Ultimate Online"
start "" "KOF_Ultimate_Online.exe"
echo.
echo ✓ Jeu lancé!
echo.
pause
goto MENU

:VERSUS
cls
echo.
echo ============================================================
echo   MODE VERSUS LOCAL (2 JOUEURS)
echo ============================================================
echo.
echo Arrêt des scripts IA externes...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 1 >nul

echo.
echo Configuration:
echo   P1: Clavier (flèches + A/S/D/Z/X/C) ou Manette 1
echo   P2: Clavier (E/R/T/Y + touches) ou Manette 2
echo.
echo Lancement M.U.G.E.N...
cd /d "D:\KOF Ultimate Online"
start "" "KOF_Ultimate_Online.exe"
echo.
echo ✓ Jeu lancé!
echo.
echo Dans le menu:
echo   1. Choisis "Versus Mode"
echo   2. Les 2 joueurs sélectionnent leurs personnages
echo   3. Combat!
echo.
pause
goto MENU

:NETPLAY
cls
echo.
echo ============================================================
echo   MODE NETPLAY (EN LIGNE)
echo ============================================================
echo.
echo Pour jouer en ligne, utilise Ikemen GO (pas M.U.G.E.N).
echo.
echo Arrêt des scripts IA externes...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 1 >nul

echo.
echo Vérification Ikemen GO...
if not exist "D:\KOF Ultimate Online\Ikemen_GO\Ikemen_GO.exe" (
    echo.
    echo ❌ ERREUR: Ikemen GO n'est pas installé!
    echo.
    echo Pour installer:
    echo   Lance: python setup_ikemen_go.py
    echo.
    pause
    goto MENU
)

echo.
echo Lancement Ikemen GO...
cd /d "D:\KOF Ultimate Online\Ikemen_GO"
start "" "Ikemen_GO.exe"
echo.
echo ✓ Ikemen GO lancé!
echo.
echo Dans le menu:
echo   1. Choisis "Network"
echo   2. "Host Game" (héberger) ou "Join Game" (rejoindre)
echo   3. Configure ton match
echo   4. Attends ton adversaire / Rejoins l'hôte
echo   5. Combat!
echo.
pause
goto MENU

:END
echo.
echo 👋 À bientôt!
echo.
timeout /t 2 >nul
exit
