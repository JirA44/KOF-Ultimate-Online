@echo off
title Lancement Joueurs Virtuels KOF
color 0A
chcp 65001 >nul

echo.
echo ═══════════════════════════════════════════════════════════
echo          🎮 SYSTÈME JOUEURS VIRTUELS EN CONTINU 🎮
echo                   KOF Ultimate Online
echo ═══════════════════════════════════════════════════════════
echo.
echo.
echo 📋 Options disponibles:
echo.
echo   [1] Lancer 3 joueurs virtuels (session 2h)
echo   [2] Lancer 5 joueurs virtuels (session 2h)
echo   [3] Lancer 10 joueurs virtuels (session infinie)
echo   [4] Ouvrir le Dashboard de monitoring
echo   [5] Voir les logs des joueurs
echo   [6] Voir les statistiques
echo   [Q] Quitter
echo.
echo ═══════════════════════════════════════════════════════════
echo.

set /p choice="Votre choix: "

if "%choice%"=="1" goto launch3
if "%choice%"=="2" goto launch5
if "%choice%"=="3" goto launch10
if "%choice%"=="4" goto dashboard
if "%choice%"=="5" goto logs
if "%choice%"=="6" goto stats
if /i "%choice%"=="Q" goto end

echo Choix invalide!
timeout /t 2 >nul
goto start

:launch3
echo.
echo 🚀 Lancement de 3 joueurs virtuels...
echo.
start "" python VIRTUAL_PLAYERS_CONTINUOUS.py
timeout /t 2
start "" VIRTUAL_PLAYERS_DASHBOARD.html
echo.
echo ✅ Système lancé! Dashboard ouvert automatiquement.
echo.
pause
goto end

:launch5
echo.
echo 🚀 Lancement de 5 joueurs virtuels...
echo.
echo Ce mode nécessite une modification du script.
echo Éditer VIRTUAL_PLAYERS_CONTINUOUS.py et changer num_players = 5
echo.
pause
goto start

:launch10
echo.
echo 🚀 Lancement de 10 joueurs virtuels (SESSION INFINIE)...
echo.
echo ⚠️  ATTENTION: Ce mode peut être très intensif!
echo ⚠️  Assurez-vous que votre PC peut le supporter.
echo.
pause
start "" python VIRTUAL_PLAYERS_CONTINUOUS.py
start "" VIRTUAL_PLAYERS_DASHBOARD.html
echo.
echo ✅ Système lancé!
echo.
pause
goto end

:dashboard
echo.
echo 📊 Ouverture du dashboard...
start "" VIRTUAL_PLAYERS_DASHBOARD.html
timeout /t 1
goto start

:logs
echo.
echo 📝 Logs des joueurs virtuels:
echo.
dir /B virtual_player_*_logs 2>nul
echo.
echo Pour voir les logs d'un joueur, ouvrir:
echo   virtual_player_X_logs\player_X.log
echo.
pause
goto start

:stats
echo.
echo 📊 Statistiques des joueurs:
echo.
dir /B virtual_player_*_logs\stats_*.json 2>nul
echo.
echo Pour voir les stats, ouvrir les fichiers .json
echo.
pause
goto start

:end
echo.
echo ✅ Au revoir!
timeout /t 2
exit
