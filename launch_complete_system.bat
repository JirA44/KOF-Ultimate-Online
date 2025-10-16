@echo off
title KOF Ultimate - Système Complet
color 0A
echo.
echo ================================================================
echo           KOF ULTIMATE - COMPLETE LAUNCH SYSTEM
echo ================================================================
echo.
echo [1/3] Demarrage du nouveau launcher moderne...
start "KOF Launcher" python launcher_modern.py

timeout /t 2 /nobreak >nul

echo [2/3] Demarrage du monitoring des manettes (hot-plug)...
start "Gamepad Monitor" python gamepad_hotplug_monitor.py

timeout /t 1 /nobreak >nul

echo [3/3] Demarrage de l'agent IA navigator (optionnel)...
start "AI Navigator" python launcher_ai_navigator.py

echo.
echo ================================================================
echo                     SYSTEME LANCE!
echo ================================================================
echo.
echo   Fenetres actives:
echo   [*] KOF Ultimate Launcher (moderne)
echo   [*] Gamepad Hot-Plug Monitor (branchement temps reel)
echo   [*] AI Navigator (detection problemes)
echo.
echo   Fonctionnalites:
echo   - Branchez/debranchez vos manettes a tout moment
echo   - Configuration automatique instantanee
echo   - Detection temps reel pendant le jeu
echo   - Agent IA surveille les problemes
echo.
echo ================================================================
echo.
pause
