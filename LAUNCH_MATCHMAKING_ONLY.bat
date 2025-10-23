@echo off
chcp 65001 > nul
title KOF Ultimate - Matchmaking Only (No Game)
color 0B

echo.
echo ═══════════════════════════════════════════════════════════════
echo    🔇 MATCHMAKING SILENCIEUX UNIQUEMENT 🔇
echo ═══════════════════════════════════════════════════════════════
echo.
echo    ❌ Le jeu NE sera PAS lancé
echo    ✅ Seulement le système de matchmaking virtuel
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
if not exist "player_profiles" mkdir "player_profiles"
if not exist "logs" mkdir "logs"

echo ✅ Environnement prêt
echo.
echo 🚀 Lancement du matchmaking (SANS LE JEU)...
echo.

:: 1. SERVEUR DE MATCHMAKING
echo [1/3] 🌐 Serveur de Matchmaking...
start /B pythonw matchmaking_server.py > logs\matchmaking.log 2>&1
timeout /t 2 > nul
echo       ✅ Serveur lancé (port 9999)
echo.

:: 2. JOUEURS VIRTUELS IA
echo [2/3] 🤖 20 Joueurs Virtuels IA...
start /B pythonw virtual_players_ai.py > logs\players.log 2>&1
timeout /t 3 > nul
echo       ✅ 20 bots lancés
echo.

:: 3. SYSTÈME ML
echo [3/3] 🧠 Système ML (amélioration continue)...
start /B pythonw ml_continuous_improver.py > logs\ml_system.log 2>&1
timeout /t 2 > nul
echo       ✅ ML actif
echo.

:: OUVRIR LE DASHBOARD
echo 📊 Ouverture du dashboard de monitoring...
start "" "monitoring_dashboard.html"
timeout /t 1 > nul
echo.

echo ═══════════════════════════════════════════════════════════════
echo.
echo     ✅ MATCHMAKING LANCÉ EN MODE SILENCIEUX !
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo ✅ CE QUI TOURNE:
echo    • Serveur de matchmaking (port 9999)
echo    • 20 joueurs virtuels IA
echo    • Système ML (cycle 30 min)
echo    • Dashboard de monitoring
echo.
echo ❌ CE QUI NE TOURNE PAS:
echo    • Le jeu KOF (pas de plein écran!)
echo    • Auto-combat
echo.
echo 📊 MONITORING:
echo    • Dashboard Web    → monitoring_dashboard.html
echo    • Logs             → dossier "logs\"
echo.
echo 🛑 POUR ARRÊTER:
echo    • Lancer STOP_ALL.bat
echo    • OU: taskkill /IM pythonw.exe /F
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo Vous pouvez fermer cette fenêtre.
echo Les processus continueront en arrière-plan.
echo.

pause
