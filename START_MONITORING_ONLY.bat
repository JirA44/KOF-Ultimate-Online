@echo off
chcp 65001 > nul
title KOF - Monitoring Only (NO GAME)
color 0E

echo.
echo ═══════════════════════════════════════════════════════════════
echo    📊 MONITORING UNIQUEMENT - JAMAIS DE JEU 📊
echo ═══════════════════════════════════════════════════════════════
echo.

:: ARRÊTER TOUT D'ABORD
echo 🛑 Arrêt de tous les processus existants...
taskkill /IM pythonw.exe /F > nul 2>&1
taskkill /IM python.exe /F > nul 2>&1
taskkill /IM KOF_Ultimate_Online.exe /F > nul 2>&1
taskkill /IM Ikemen_GO.exe /F > nul 2>&1
timeout /t 2 > nul
echo    ✅ Tout arrêté
echo.

:: Créer dossiers
if not exist "player_profiles" mkdir "player_profiles"
if not exist "logs" mkdir "logs"

echo 🚀 Lancement (mode minimal)...
echo.

:: 1. Serveur (fenêtre minimisée)
echo [1/3] 🌐 Serveur...
start "KOF-Server" /MIN cmd /c "python matchmaking_server.py > logs\server.log 2>&1"
timeout /t 3 > nul
echo       ✅ Lancé
echo.

:: 2. Joueurs (fenêtre minimisée)
echo [2/3] 🤖 Joueurs...
start "KOF-Players" /MIN cmd /c "python virtual_players_ai.py > logs\players.log 2>&1"
timeout /t 4 > nul
echo       ✅ Lancé
echo.

:: 3. ML (fenêtre minimisée)
echo [3/3] 🧠 ML...
start "KOF-ML" /MIN cmd /c "python ml_continuous_improver.py > logs\ml.log 2>&1"
timeout /t 2 > nul
echo       ✅ Lancé
echo.

:: Dashboard
echo 📊 Ouverture dashboard...
start "" "monitoring_dashboard.html"
echo.

echo ═══════════════════════════════════════════════════════════════
echo.
echo     ✅ SYSTÈME LANCÉ !
echo.
echo     📊 Dashboard ouvert dans le navigateur
echo     🔇 Processus minimisés dans la barre des tâches
echo     ❌ AUCUN JEU NE SERA LANCÉ
echo.
echo     Pour arrêter: EMERGENCY_STOP.bat
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

pause
