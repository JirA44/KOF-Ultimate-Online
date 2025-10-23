@echo off
chcp 65001 > nul
title KOF Ultimate - SAFE MODE (No Game EVER)
color 0A

echo.
echo ═══════════════════════════════════════════════════════════════
echo    ✅ MODE SÉCURISÉ - JAMAIS DE JEU EN PLEIN ÉCRAN ✅
echo ═══════════════════════════════════════════════════════════════
echo.
echo    🔒 Le jeu ne sera JAMAIS lancé
echo    ✅ Seulement le système de matchmaking virtuel
echo    📊 Dashboard de monitoring disponible
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

:: Vérifier Python
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python non détecté
    pause
    exit /b 1
)

:: Créer les dossiers
if not exist "player_profiles" mkdir "player_profiles" > nul 2>&1
if not exist "logs" mkdir "logs" > nul 2>&1

echo ✅ Environnement prêt
echo.

:: ARRÊTER d'abord tout ce qui pourrait tourner
echo 🛑 Nettoyage des processus existants...
taskkill /IM pythonw.exe /F > nul 2>&1
taskkill /IM python.exe /F > nul 2>&1
taskkill /IM KOF_Ultimate_Online.exe /F > nul 2>&1
taskkill /IM Ikemen_GO.exe /F > nul 2>&1
timeout /t 2 > nul
echo    ✅ Nettoyage terminé
echo.

echo 🚀 Lancement du système (MODE SÉCURISÉ)...
echo.

:: 1. SERVEUR DE MATCHMAKING
echo [1/3] 🌐 Serveur de Matchmaking...
start /B pythonw matchmaking_server.py > logs\matchmaking.log 2>&1
timeout /t 3 > nul
echo       ✅ Serveur lancé (port 9999)
echo.

:: 2. JOUEURS VIRTUELS IA
echo [2/3] 🤖 20 Joueurs Virtuels IA...
start /B pythonw virtual_players_ai.py > logs\players.log 2>&1
timeout /t 4 > nul
echo       ✅ 20 bots lancés
echo.

:: 3. SYSTÈME ML
echo [3/3] 🧠 Système ML (amélioration continue)...
start /B pythonw ml_continuous_improver.py > logs\ml_system.log 2>&1
timeout /t 2 > nul
echo       ✅ ML actif
echo.

:: OUVRIR LE DASHBOARD
echo 📊 Ouverture du dashboard...
start "" "monitoring_dashboard.html"
timeout /t 2 > nul
echo.

echo ═══════════════════════════════════════════════════════════════
echo.
echo     ✅ SYSTÈME LANCÉ EN MODE SÉCURISÉ !
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo ✅ ACTIF:
echo    • Serveur de matchmaking (port 9999)
echo    • 20 joueurs virtuels IA
echo    • Système ML (cycle 30 min)
echo    • Dashboard de monitoring
echo.
echo 🔒 DÉSACTIVÉ (JAMAIS LANCÉ):
echo    • Jeu KOF
echo    • Auto-combat
echo    • Tout processus qui ouvre des fenêtres
echo.
echo 📊 MONITORING:
echo    • Dashboard: monitoring_dashboard.html (ouvert)
echo    • Logs:      dossier "logs\"
echo.
echo 🛑 POUR ARRÊTER:
echo    • EMERGENCY_STOP.bat
echo    • OU: taskkill /IM pythonw.exe /F
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🔇 Tous les processus tournent en arrière-plan silencieusement
echo.
echo Vous pouvez fermer cette fenêtre.
echo Le système continuera en arrière-plan.
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

pause
