@echo off
chcp 65001 > nul
title KOF ULTIMATE - IAs Complete Test System
color 0B
cls

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║    KOF ULTIMATE - SYSTÈME DE TEST COMPLET PAR IAs            ║
echo ║                                                                ║
echo ║  Ce système va:                                               ║
echo ║  • Lancer le jeu automatiquement                             ║
echo ║  • Cliquer dans TOUS les menus                               ║
echo ║  • Tester TOUS les 189 personnages                           ║
echo ║  • Détecter TOUTES les erreurs                               ║
echo ║  • Logger tout dans des fichiers                             ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo.

echo [ÉTAPE 1/5] Vérification des dépendances...
echo.

python -c "import pyautogui" 2>nul
if errorlevel 1 (
    echo    ⚠ Installation de pyautogui...
    python -m pip install -q pyautogui
    echo    ✓ Installé!
)

python -c "import win32gui" 2>nul
if errorlevel 1 (
    echo    ⚠ Installation de pywin32...
    python -m pip install -q pywin32
    echo    ✓ Installé!
)

echo    ✓ Toutes les dépendances OK
echo.
echo.

echo [ÉTAPE 2/5] Nettoyage des anciens logs...
if exist "char_test_log.txt" del /q "char_test_log.txt"
if exist "ia_screenshots\*.png" del /q "ia_screenshots\*.png" 2>nul
echo    ✓ Logs nettoyés
echo.
echo.

echo [ÉTAPE 3/5] Lancement du jeu...
echo    Le jeu va se lancer dans 3 secondes...
timeout /t 3 /nobreak >nul

start "" "KOF BLACK R.exe"

echo    ✓ Jeu lancé
echo    ⏳ Attente du chargement (15s)...
timeout /t 15 /nobreak >nul
echo.
echo.

echo [ÉTAPE 4/5] Lancement des IAs en parallèle...
echo.
echo    ┌─────────────────────────────────────────────────┐
echo    │  IA 1: Navigator - Teste tous les menus        │
echo    │  IA 2: Character Tester - Teste 189 persos     │
echo    │  IA 3: Auto Clicker - Clique en continu        │
echo    └─────────────────────────────────────────────────┘
echo.

REM Lancer les IAs en arrière-plan
start "IA Navigator" cmd /c "python ia_navigator_simple.py > ia_navigator.log 2>&1"
timeout /t 2 /nobreak >nul

start "IA Char Tester" cmd /c "python ia_test_all_chars.py > ia_chars.log 2>&1"
timeout /t 2 /nobreak >nul

start "IA Auto Clicker" cmd /c "python auto_clicker_kof.py > ia_clicker.log 2>&1"

echo    ✓ 3 IAs lancées!
echo.
echo.

echo [ÉTAPE 5/5] Monitoring en temps réel...
echo.
echo ═══════════════════════════════════════════════════════════════
echo   LES IAs TRAVAILLENT MAINTENANT!
echo ═══════════════════════════════════════════════════════════════
echo.
echo   Fenêtres ouvertes:
echo   • IA Navigator       - Explore tous les menus
echo   • IA Char Tester     - Teste tous les personnages
echo   • IA Auto Clicker    - Clique en continu
echo.
echo   Fichiers de log en cours de création:
echo   • ia_navigator.log   - Log de navigation
echo   • ia_chars.log       - Log des tests persos
echo   • char_test_log.txt  - Détails des tests
echo   • ia_screenshots\    - Screenshots de tous les tests
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo   ⚠️  NE TOUCHEZ PAS AU JEU!
echo   Les IAs vont cliquer automatiquement partout.
echo.
echo   Durée estimée: 30-45 minutes pour tout tester
echo.
echo   Vous pouvez surveiller les logs en temps réel:
echo      • tail -f ia_navigator.log
echo      • tail -f char_test_log.txt
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo   Appuyez sur une touche pour voir le monitoring...
pause >nul
echo.
echo.

REM Monitoring loop
echo ┌───────────────────────────────────────────────────────────┐
echo │              MONITORING DES IAs                           │
echo └───────────────────────────────────────────────────────────┘
echo.

:monitor_loop

cls
echo ═══════════════════════════════════════════════════════════════
echo   MONITORING EN TEMPS RÉEL
echo ═══════════════════════════════════════════════════════════════
echo   Heure: %TIME%
echo.

REM Compter les screenshots
for /f %%A in ('dir /b "ia_screenshots\*.png" 2^>nul ^| find /c /v ""') do set screenshot_count=%%A
echo   📸 Screenshots pris: %screenshot_count%
echo.

REM Vérifier les logs
if exist "char_test_log.txt" (
    echo   📄 Log des tests personnages:
    echo   ─────────────────────────────────────────────────────────
    type "char_test_log.txt" | find "Personnage" | more +0
    echo   ─────────────────────────────────────────────────────────
    echo.
)

REM Vérifier les erreurs
if exist "char_test_log.txt" (
    for /f %%A in ('type "char_test_log.txt" 2^>nul ^| find /c "ERREUR"') do set error_count=%%A
    if %error_count% GTR 0 (
        echo   ⚠️  ERREURS DÉTECTÉES: %error_count%
        echo.
        type "char_test_log.txt" | find "ERREUR"
        echo.
    )
)

echo ═══════════════════════════════════════════════════════════════
echo   Appuyez sur Ctrl+C pour arrêter le monitoring
echo   Le monitoring se rafraîchit toutes les 10 secondes...
echo ═══════════════════════════════════════════════════════════════
echo.

timeout /t 10 /nobreak >nul
goto monitor_loop

echo.
echo.
echo ═══════════════════════════════════════════════════════════════
echo   TESTS TERMINÉS!
echo ═══════════════════════════════════════════════════════════════
echo.
echo   Consultez les logs pour voir les résultats:
echo   • char_test_log.txt  - Résultats détaillés
echo   • ia_screenshots\    - Tous les screenshots
echo.
pause
