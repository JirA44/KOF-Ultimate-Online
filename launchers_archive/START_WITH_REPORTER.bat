@echo off
chcp 65001 > nul
title KOF Ultimate - Complete System with Live Reports
color 0B

echo.
echo ═══════════════════════════════════════════════════════════════
echo    🎬 SYSTÈME COMPLET + RAPPORTS EN DIRECT 🎬
echo ═══════════════════════════════════════════════════════════════
echo.

:: ARRÊTER TOUT D'ABORD
echo 🛑 Nettoyage...
taskkill /IM pythonw.exe /F > nul 2>&1
taskkill /IM python.exe /F > nul 2>&1
taskkill /IM KOF_Ultimate_Online.exe /F > nul 2>&1
taskkill /IM Ikemen_GO.exe /F > nul 2>&1
timeout /t 2 > nul
echo    ✅ Nettoyé
echo.

:: Créer dossiers
if not exist "player_profiles" mkdir "player_profiles" > nul 2>&1
if not exist "logs" mkdir "logs" > nul 2>&1

echo 🚀 Lancement du système complet...
echo.

:: 1. Serveur
echo [1/4] 🌐 Serveur de Matchmaking...
start "KOF-Server" /MIN cmd /c "python matchmaking_server.py > logs\server.log 2>&1"
timeout /t 3 > nul
echo       ✅ Lancé
echo.

:: 2. Joueurs
echo [2/4] 🤖 20 Joueurs Virtuels IA...
start "KOF-Players" /MIN cmd /c "python virtual_players_ai.py > logs\players.log 2>&1"
timeout /t 4 > nul
echo       ✅ Lancé
echo.

:: 3. ML
echo [3/4] 🧠 Système ML...
start "KOF-ML" /MIN cmd /c "python ml_continuous_improver.py > logs\ml.log 2>&1"
timeout /t 2 > nul
echo       ✅ Lancé
echo.

:: 4. Dashboard
echo [4/4] 📊 Dashboard Web...
start "" "monitoring_dashboard.html"
timeout /t 2 > nul
echo       ✅ Ouvert
echo.

echo ═══════════════════════════════════════════════════════════════
echo.
echo     ✅ SYSTÈME LANCÉ !
echo.
echo     Attente de 15 secondes pour que les données se génèrent...
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

timeout /t 15 > nul

:: 5. Lancer le Live Reporter (dans cette fenêtre)
echo.
echo 📊 Démarrage du Live Reporter (rapports toutes les 5 min)...
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

python live_reporter.py

:: Si le reporter s'arrête, proposer de relancer
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo Le reporter s'est arrêté.
echo.
echo Pour relancer uniquement le reporter: python live_reporter.py
echo Pour tout arrêter: EMERGENCY_STOP.bat
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

pause
