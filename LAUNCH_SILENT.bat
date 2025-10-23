@echo off
chcp 65001 > nul
title KOF Ultimate Online - Silent Launcher
color 0E

echo.
echo ═══════════════════════════════════════════════════════════════
echo    🔇 KOF ULTIMATE ONLINE - LANCEMENT SILENCIEUX 🔇
echo ═══════════════════════════════════════════════════════════════
echo.
echo    Tous les processus tournent en arrière-plan
echo    Monitoring disponible dans le dashboard
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
echo 🚀 Lancement de tous les systèmes en mode SILENCIEUX...
echo.

:: 1. SERVEUR DE MATCHMAKING (pythonw = pas de fenêtre console)
echo [1/5] 🌐 Serveur de Matchmaking...
start /B pythonw matchmaking_server.py > logs\matchmaking.log 2>&1
timeout /t 2 > nul
echo       ✅ Lancé en arrière-plan
echo.

:: 2. JOUEURS VIRTUELS IA
echo [2/5] 🤖 20 Joueurs Virtuels IA...
start /B pythonw virtual_players_ai.py > logs\players.log 2>&1
timeout /t 3 > nul
echo       ✅ Lancé en arrière-plan
echo.

:: 3. SYSTÈME ML
echo [3/5] 🧠 Système ML...
start /B pythonw ml_continuous_improver.py > logs\ml_system.log 2>&1
timeout /t 2 > nul
echo       ✅ Lancé en arrière-plan
echo.

:: 4. AUTO-COMBAT KOF (si existe)
echo [4/5] 🎮 Auto-Combat KOF...
if exist "auto_combat_new_maps.py" (
    start /B pythonw auto_combat_new_maps.py > logs\kof_combat.log 2>&1
    echo       ✅ Lancé en arrière-plan
) else (
    echo       ℹ️  Script auto-combat non trouvé
)
echo.

:: 5. DASHBOARD DE MONITORING
echo [5/5] 📊 Dashboard de Monitoring...
start "" "monitoring_dashboard.html"
timeout /t 1 > nul
echo       ✅ Dashboard ouvert
echo.

echo ═══════════════════════════════════════════════════════════════
echo.
echo     ✅ SYSTÈME LANCÉ EN MODE SILENCIEUX !
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 📊 MONITORING:
echo    • Dashboard Web       → monitoring_dashboard.html
echo    • Logs centralisés    → dossier "logs\"
echo.
echo 🔇 AUCUNE FENÊTRE VISIBLE:
echo    • Tous les processus en arrière-plan
echo    • Utiliser le dashboard pour surveiller
echo    • Consulter les logs pour déboguer
echo.
echo 🛑 POUR ARRÊTER:
echo    • Utiliser STOP_ALL.bat
echo    • OU: taskkill /IM pythonw.exe /F
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo Vous pouvez fermer cette fenêtre.
echo Les processus continueront en arrière-plan.
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

pause
