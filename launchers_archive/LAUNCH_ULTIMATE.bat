@echo off
title KOF ULTIMATE - Lancement Automatique
color 0A
cls

echo.
echo ================================================================
echo           KOF ULTIMATE - LANCEMENT AUTOMATIQUE
echo ================================================================
echo.
echo [1/4] Auto-Setup des dependances...
python auto_setup_complete.py

if errorlevel 1 (
    echo.
    echo [!] Auto-setup termine, mais avec avertissements
    echo     Le systeme va quand meme demarrer...
    timeout /t 3 /nobreak >nul
)

echo.
echo [2/4] Demarrage du launcher moderne...
start "KOF Launcher" python launcher_modern.py

timeout /t 2 /nobreak >nul

echo [3/4] Demarrage du monitor hot-plug des manettes...
start "Gamepad Monitor" python gamepad_hotplug_monitor.py

timeout /t 1 /nobreak >nul

echo [4/4] Demarrage de l'agent IA (optionnel)...
start /min "AI Navigator" python launcher_ai_navigator.py

echo.
echo ================================================================
echo                   SYSTEME LANCE!
echo ================================================================
echo.
echo   [*] Launcher moderne (design ultra-moderne)
echo   [*] Gamepad Monitor (hot-plug temps reel)
echo   [*] AI Navigator (detection des problemes)
echo.
echo   TOUT EST AUTOMATIQUE:
echo   - Dependencies auto-installees
echo   - Manettes auto-detectees
echo   - Configuration auto-realisee
echo   - Backgrounds deja integres
echo.
echo   VOUS POUVEZ:
echo   - Brancher/debrancher manettes a tout moment
echo   - Changer de manette pendant le jeu
echo   - Naviguer dans les menus avec la manette
echo.
echo ================================================================
echo.
echo Pret a jouer ! Cliquez sur "JOUER" dans le launcher.
echo.
pause
