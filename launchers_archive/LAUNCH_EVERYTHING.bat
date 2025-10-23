@echo off
chcp 65001 > nul
title KOF Ultimate Online - LAUNCH EVERYTHING
color 0B

echo.
echo ═══════════════════════════════════════════════════════════════
echo    🔥 KOF ULTIMATE ONLINE - LANCEMENT COMPLET 🔥
echo ═══════════════════════════════════════════════════════════════
echo.
echo    🎮 Jeu + 🤖 Matchmaking + 🧠 ML + 📊 Dashboard
echo    ⚡ TOUT EN MÊME TEMPS !
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

echo ✅ Python OK
echo.

:: Créer les dossiers nécessaires
if not exist "player_profiles" mkdir "player_profiles"
echo ✅ Dossiers créés
echo.

echo ┌─────────────────────────────────────────────────────────────┐
echo │  🚀 LANCEMENT SÉQUENTIEL DE TOUS LES SYSTÈMES               │
echo └─────────────────────────────────────────────────────────────┘
echo.

:: 1. SERVEUR DE MATCHMAKING
echo [1/7] 🌐 Serveur de Matchmaking...
start "⚔️ KOF Matchmaking Server" /MIN cmd /c "cd /d "%~dp0" && python matchmaking_server.py 2>&1 > matchmaking_server.log"
timeout /t 2 > nul
echo       ✅ Serveur lancé (port 9999)
echo.

:: 2. JOUEURS VIRTUELS IA
echo [2/7] 🤖 Joueurs Virtuels IA (20 bots)...
start "🤖 KOF Virtual Players" /MIN cmd /c "cd /d "%~dp0" && python virtual_players_ai.py 2>&1 > virtual_players.log"
timeout /t 3 > nul
echo       ✅ 20 bots IA lancés
echo.

:: 3. SYSTÈME ML AMÉLIORATION CONTINUE
echo [3/7] 🧠 Système ML d'amélioration...
start "🧠 KOF ML System" /MIN cmd /c "cd /d "%~dp0" && python ml_continuous_improver.py 2>&1 > ml_system.log"
timeout /t 2 > nul
echo       ✅ ML actif (cycle: 30 min)
echo.

:: 4. DASHBOARD HTML
echo [4/7] 📊 Dashboard Web...
start "" "matchmaking_dashboard.html"
timeout /t 1 > nul
echo       ✅ Dashboard ouvert
echo.

:: 5. AUTO-TEST DU JEU (mini fenêtre)
echo [5/7] 🎮 Lancement du jeu KOF (auto-combat)...
if exist "AUTO_TEST_MINI_WINDOWS.py" (
    start "🎮 KOF Auto-Combat" /MIN cmd /c "cd /d "%~dp0" && python AUTO_TEST_MINI_WINDOWS.py 2>&1 > kof_game.log"
    timeout /t 2 > nul
    echo       ✅ Jeu lancé en mode auto-combat
) else if exist "PLAY_MINI_WINDOW.bat" (
    start "🎮 KOF Game" /MIN cmd /c "cd /d "%~dp0" && PLAY_MINI_WINDOW.bat"
    timeout /t 2 > nul
    echo       ✅ Jeu lancé
) else if exist "KOF_Ultimate_Online.exe" (
    start "🎮 KOF Game" /MIN "" "KOF_Ultimate_Online.exe"
    timeout /t 2 > nul
    echo       ✅ Jeu lancé
) else if exist "Ikemen_GO.exe" (
    start "🎮 KOF Game" /MIN "" "Ikemen_GO.exe"
    timeout /t 2 > nul
    echo       ✅ Jeu lancé
) else (
    echo       ⚠️  Aucun exécutable de jeu trouvé
)
echo.

:: 6. LAUNCHER DASHBOARD (si existe)
echo [6/7] 🖥️  Launcher Dashboard...
if exist "LAUNCHER_DASHBOARD.py" (
    start "📊 Launcher Dashboard" /MIN cmd /c "cd /d "%~dp0" && python LAUNCHER_DASHBOARD.py 2>&1 > launcher_dashboard.log"
    timeout /t 2 > nul
    echo       ✅ Launcher dashboard lancé
) else (
    echo       ℹ️  Launcher dashboard non trouvé (optionnel)
)
echo.

:: 7. DASHBOARD KOF (si existe)
echo [7/7] 📈 Dashboard KOF HTML...
if exist "DASHBOARD_KOF.html" (
    start "" "DASHBOARD_KOF.html"
    timeout /t 1 > nul
    echo       ✅ Dashboard KOF ouvert
) else (
    echo       ℹ️  Dashboard KOF non trouvé (optionnel)
)
echo.

echo ═══════════════════════════════════════════════════════════════
echo.
echo     ✅✅✅ TOUT EST LANCÉ ! ✅✅✅
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🌐 SYSTÈMES ACTIFS:
echo    • Serveur Matchmaking     → Port 9999
echo    • 20 Joueurs Virtuels IA  → Actifs
echo    • Système ML              → Amélioration auto (30 min)
echo    • Dashboard Web           → matchmaking_dashboard.html
echo    • Jeu KOF                 → Combats automatiques
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 📂 LOGS DISPONIBLES:
echo    • matchmaking_server.log
echo    • virtual_players.log
echo    • ml_system.log
echo    • kof_game.log
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 💡 CONSEILS:
echo    • Actualisez les dashboards pour voir les stats temps réel
echo    • Les fenêtres sont minimisées en arrière-plan
echo    • Consultez les logs en cas de problème
echo    • Ctrl+C dans chaque fenêtre pour arrêter
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🎮 Le système tourne maintenant de manière autonome !
echo    Les bots jouent, apprennent et s'améliorent automatiquement.
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

pause
