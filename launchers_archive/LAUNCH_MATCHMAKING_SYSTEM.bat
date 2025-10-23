@echo off
chcp 65001 > nul
title KOF Ultimate Online - Matchmaking System Launcher
color 0A

echo.
echo ═══════════════════════════════════════════════════════════════
echo    ⚔️  KOF ULTIMATE ONLINE - MATCHMAKING SYSTEM ⚔️
echo ═══════════════════════════════════════════════════════════════
echo.
echo    🤖 Système de Matchmaking avec Amélioration Continue IA
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

:: Vérifier que Python est installé
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo.
    echo Veuillez installer Python 3.8+ depuis: https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python détecté
echo.

:: Créer le dossier pour les profils
if not exist "player_profiles" mkdir "player_profiles"
echo ✅ Dossier player_profiles créé
echo.

echo ┌─────────────────────────────────────────────────────────────┐
echo │  Lancement du système de matchmaking...                     │
echo └─────────────────────────────────────────────────────────────┘
echo.

:: 1. Lancer le serveur de matchmaking
echo 🚀 Démarrage du serveur de matchmaking...
start "KOF Matchmaking Server" /MIN cmd /c "cd /d "%~dp0" && python matchmaking_server.py"
timeout /t 3 > nul
echo ✅ Serveur lancé
echo.

:: 2. Lancer les joueurs virtuels IA
echo 🤖 Démarrage des joueurs virtuels IA (20 joueurs)...
start "KOF Virtual Players" /MIN cmd /c "cd /d "%~dp0" && python virtual_players_ai.py"
timeout /t 5 > nul
echo ✅ Joueurs virtuels lancés
echo.

:: 3. Lancer le système ML d'amélioration continue
echo 🧠 Démarrage du système ML d'amélioration continue...
start "KOF ML Improvement" /MIN cmd /c "cd /d "%~dp0" && python ml_continuous_improver.py"
timeout /t 2 > nul
echo ✅ Système ML lancé
echo.

:: 4. Ouvrir le dashboard HTML
echo 📊 Ouverture du dashboard...
start "" "matchmaking_dashboard.html"
echo ✅ Dashboard ouvert
echo.

echo ═══════════════════════════════════════════════════════════════
echo.
echo ✅ SYSTÈME COMPLÈTEMENT LANCÉ !
echo.
echo    🌐 Dashboard:           matchmaking_dashboard.html
echo    🖥️  Serveur:             Port 9999
echo    🤖 Joueurs virtuels:    20 bots avec IA
echo    🧠 ML Amélioration:     Actif (cycle: 30 min)
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 📌 Les fenêtres sont minimisées en arrière-plan
echo 📌 Actualisez le dashboard pour voir les stats en temps réel
echo 📌 Appuyez sur Ctrl+C dans chaque fenêtre pour arrêter
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

pause
