@echo off
chcp 65001 >nul
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║     🔄  RÉORGANISATION DES LAUNCHERS v2.0                          ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo   Cette opération va:
echo   1. Créer un dossier launchers_archive/
echo   2. Renommer les 25 fichiers essentiels avec versioning v2.0
echo   3. Archiver les 44 fichiers obsolètes
echo.
echo   ⚠️  Un backup sera créé avant toute modification
echo.
pause

cd /d "D:\KOF Ultimate Online"

REM Créer dossier d'archive
echo.
echo [1/4] Création du dossier launchers_archive...
if not exist "launchers_archive" mkdir "launchers_archive"
echo   ✓ Dossier créé

REM Créer backup
echo.
echo [2/4] Création du backup...
if not exist "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%" mkdir "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%"
echo   ✓ Backup créé

REM ═══════════════════════════════════════════════════════════════════
REM  CATÉGORIE 1: LAUNCHERS DE JEU
REM ═══════════════════════════════════════════════════════════════════

echo.
echo [3/4] Renommage des fichiers essentiels...
echo   → Catégorie: LAUNCHERS DE JEU

if exist "LANCER_JEU_SIMPLE.bat" (
    copy "LANCER_JEU_SIMPLE.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "LANCER_JEU_SIMPLE.bat" "KOF-LAUNCHER-v2.0-SIMPLE.bat" >nul
    echo     ✓ LANCER_JEU_SIMPLE.bat → KOF-LAUNCHER-v2.0-SIMPLE.bat
)

if exist "TEST_MINIMAL_10_PERSOS.bat" (
    copy "TEST_MINIMAL_10_PERSOS.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "TEST_MINIMAL_10_PERSOS.bat" "KOF-LAUNCHER-v2.0-STABLE-10.bat" >nul
    echo     ✓ TEST_MINIMAL_10_PERSOS.bat → KOF-LAUNCHER-v2.0-STABLE-10.bat
)

if exist "PLAY.bat" (
    copy "PLAY.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "PLAY.bat" "KOF-LAUNCHER-v2.0-QUICK.bat" >nul
    echo     ✓ PLAY.bat → KOF-LAUNCHER-v2.0-QUICK.bat
)

if exist "LAUNCHER_COMPLET.bat" (
    copy "LAUNCHER_COMPLET.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "LAUNCHER_COMPLET.bat" "KOF-LAUNCHER-v2.0-FULL.bat" >nul
    echo     ✓ LAUNCHER_COMPLET.bat → KOF-LAUNCHER-v2.0-FULL.bat
)

REM ═══════════════════════════════════════════════════════════════════
REM  CATÉGORIE 2: MULTIJOUEUR / ONLINE
REM ═══════════════════════════════════════════════════════════════════

echo   → Catégorie: ONLINE MULTIPLAYER

if exist "START_MATCHMAKING_SYSTEM.bat" (
    copy "START_MATCHMAKING_SYSTEM.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "START_MATCHMAKING_SYSTEM.bat" "KOF-ONLINE-v2.0-MATCHMAKING.bat" >nul
    echo     ✓ START_MATCHMAKING_SYSTEM.bat → KOF-ONLINE-v2.0-MATCHMAKING.bat
)

if exist "START_SERVER.bat" (
    copy "START_SERVER.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "START_SERVER.bat" "KOF-ONLINE-v2.0-SERVER.bat" >nul
    echo     ✓ START_SERVER.bat → KOF-ONLINE-v2.0-SERVER.bat
)

if exist "JOUER_CONTRE_IA_ONLINE.bat" (
    copy "JOUER_CONTRE_IA_ONLINE.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "JOUER_CONTRE_IA_ONLINE.bat" "KOF-ONLINE-v2.0-VS-AI.bat" >nul
    echo     ✓ JOUER_CONTRE_IA_ONLINE.bat → KOF-ONLINE-v2.0-VS-AI.bat
)

if exist "LAUNCH_VIRTUAL_PLAYERS.bat" (
    copy "LAUNCH_VIRTUAL_PLAYERS.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "LAUNCH_VIRTUAL_PLAYERS.bat" "KOF-ONLINE-v2.0-VIRTUAL-PLAYERS.bat" >nul
    echo     ✓ LAUNCH_VIRTUAL_PLAYERS.bat → KOF-ONLINE-v2.0-VIRTUAL-PLAYERS.bat
)

REM ═══════════════════════════════════════════════════════════════════
REM  CATÉGORIE 3: TESTS & DIAGNOSTIC
REM ═══════════════════════════════════════════════════════════════════

echo   → Catégorie: TESTS ^& DIAGNOSTIC

if exist "LANCER_TEST_EXHAUSTIF.bat" (
    copy "LANCER_TEST_EXHAUSTIF.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "LANCER_TEST_EXHAUSTIF.bat" "KOF-TEST-v2.0-EXHAUSTIF.bat" >nul
    echo     ✓ LANCER_TEST_EXHAUSTIF.bat → KOF-TEST-v2.0-EXHAUSTIF.bat
)

if exist "LANCER_AUTO_DIAGNOSTIC.bat" (
    copy "LANCER_AUTO_DIAGNOSTIC.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "LANCER_AUTO_DIAGNOSTIC.bat" "KOF-TEST-v2.0-DIAGNOSTIC.bat" >nul
    echo     ✓ LANCER_AUTO_DIAGNOSTIC.bat → KOF-TEST-v2.0-DIAGNOSTIC.bat
)

if exist "CHECK_TEST_PROGRESS.bat" (
    copy "CHECK_TEST_PROGRESS.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "CHECK_TEST_PROGRESS.bat" "KOF-TEST-v2.0-PROGRESS.bat" >nul
    echo     ✓ CHECK_TEST_PROGRESS.bat → KOF-TEST-v2.0-PROGRESS.bat
)

if exist "RUN_AUTOCHECK.bat" (
    copy "RUN_AUTOCHECK.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "RUN_AUTOCHECK.bat" "KOF-TEST-v2.0-AUTOCHECK.bat" >nul
    echo     ✓ RUN_AUTOCHECK.bat → KOF-TEST-v2.0-AUTOCHECK.bat
)

REM ═══════════════════════════════════════════════════════════════════
REM  CATÉGORIE 4: RÉPARATION & MAINTENANCE
REM ═══════════════════════════════════════════════════════════════════

echo   → Catégorie: RÉPARATION ^& MAINTENANCE

if exist "CORRIGER_CRASH.bat" (
    copy "CORRIGER_CRASH.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "CORRIGER_CRASH.bat" "KOF-FIX-v2.0-CRASH.bat" >nul
    echo     ✓ CORRIGER_CRASH.bat → KOF-FIX-v2.0-CRASH.bat
)

if exist "REPARER_JEU.bat" (
    copy "REPARER_JEU.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "REPARER_JEU.bat" "KOF-FIX-v2.0-GENERAL.bat" >nul
    echo     ✓ REPARER_JEU.bat → KOF-FIX-v2.0-GENERAL.bat
)

if exist "FIX_IKEMEN_GO.bat" (
    copy "FIX_IKEMEN_GO.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "FIX_IKEMEN_GO.bat" "KOF-FIX-v2.0-IKEMEN.bat" >nul
    echo     ✓ FIX_IKEMEN_GO.bat → KOF-FIX-v2.0-IKEMEN.bat
)

if exist "NETTOYER_PORTRAITS_CASSES.bat" (
    copy "NETTOYER_PORTRAITS_CASSES.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "NETTOYER_PORTRAITS_CASSES.bat" "KOF-FIX-v2.0-PORTRAITS.bat" >nul
    echo     ✓ NETTOYER_PORTRAITS_CASSES.bat → KOF-FIX-v2.0-PORTRAITS.bat
)

REM ═══════════════════════════════════════════════════════════════════
REM  CATÉGORIE 5: IA & AUTOMATION
REM ═══════════════════════════════════════════════════════════════════

echo   → Catégorie: IA ^& AUTOMATION

if exist "LAUNCH_AI_MULTI_MODES.bat" (
    copy "LAUNCH_AI_MULTI_MODES.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "LAUNCH_AI_MULTI_MODES.bat" "KOF-AI-v2.0-MULTI-MODES.bat" >nul
    echo     ✓ LAUNCH_AI_MULTI_MODES.bat → KOF-AI-v2.0-MULTI-MODES.bat
)

if exist "LAUNCH_MULTIPLE_AI_PLAYERS.bat" (
    copy "LAUNCH_MULTIPLE_AI_PLAYERS.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "LAUNCH_MULTIPLE_AI_PLAYERS.bat" "KOF-AI-v2.0-MULTI-PLAYERS.bat" >nul
    echo     ✓ LAUNCH_MULTIPLE_AI_PLAYERS.bat → KOF-AI-v2.0-MULTI-PLAYERS.bat
)

if exist "JOUER_LOCAL_VS_IA.bat" (
    copy "JOUER_LOCAL_VS_IA.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "JOUER_LOCAL_VS_IA.bat" "KOF-AI-v2.0-LOCAL-VS.bat" >nul
    echo     ✓ JOUER_LOCAL_VS_IA.bat → KOF-AI-v2.0-LOCAL-VS.bat
)

REM ═══════════════════════════════════════════════════════════════════
REM  CATÉGORIE 6: MONITORING & RAPPORTS
REM ═══════════════════════════════════════════════════════════════════

echo   → Catégorie: MONITORING ^& RAPPORTS

if exist "OUVRIR_DASHBOARD.bat" (
    copy "OUVRIR_DASHBOARD.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "OUVRIR_DASHBOARD.bat" "KOF-MONITOR-v2.0-DASHBOARD.bat" >nul
    echo     ✓ OUVRIR_DASHBOARD.bat → KOF-MONITOR-v2.0-DASHBOARD.bat
)

if exist "VOIR_RAPPORTS_CONTINUS.bat" (
    copy "VOIR_RAPPORTS_CONTINUS.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "VOIR_RAPPORTS_CONTINUS.bat" "KOF-MONITOR-v2.0-REPORTS.bat" >nul
    echo     ✓ VOIR_RAPPORTS_CONTINUS.bat → KOF-MONITOR-v2.0-REPORTS.bat
)

REM ═══════════════════════════════════════════════════════════════════
REM  CATÉGORIE 7: CONTRÔLE & ARRÊT
REM ═══════════════════════════════════════════════════════════════════

echo   → Catégorie: CONTRÔLE ^& ARRÊT

if exist "STOP_ALL.bat" (
    copy "STOP_ALL.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "STOP_ALL.bat" "KOF-CONTROL-v2.0-STOP-ALL.bat" >nul
    echo     ✓ STOP_ALL.bat → KOF-CONTROL-v2.0-STOP-ALL.bat
)

if exist "EMERGENCY_STOP.bat" (
    copy "EMERGENCY_STOP.bat" "launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\" >nul
    move "EMERGENCY_STOP.bat" "KOF-CONTROL-v2.0-EMERGENCY.bat" >nul
    echo     ✓ EMERGENCY_STOP.bat → KOF-CONTROL-v2.0-EMERGENCY.bat
)

REM ═══════════════════════════════════════════════════════════════════
REM  ARCHIVAGE DES FICHIERS OBSOLÈTES
REM ═══════════════════════════════════════════════════════════════════

echo.
echo [4/4] Archivage des fichiers obsolètes...

REM Tests obsolètes
if exist "LANCER_TEST_MANUEL.bat" move "LANCER_TEST_MANUEL.bat" "launchers_archive\" >nul
if exist "LANCER_TEST_RAPIDE.bat" move "LANCER_TEST_RAPIDE.bat" "launchers_archive\" >nul
if exist "LANCER_TEST_AUTO_FOCUS.bat" move "LANCER_TEST_AUTO_FOCUS.bat" "launchers_archive\" >nul
if exist "LANCER_TEST_INJECTION.bat" move "LANCER_TEST_INJECTION.bat" "launchers_archive\" >nul
if exist "LANCER_TEST_JOUEURS.bat" move "LANCER_TEST_JOUEURS.bat" "launchers_archive\" >nul
if exist "TEST_AUTO_SIMPLE.bat" move "TEST_AUTO_SIMPLE.bat" "launchers_archive\" >nul
if exist "TEST_RAPIDE.bat" move "TEST_RAPIDE.bat" "launchers_archive\" >nul
if exist "TEST_ANIMATIONS.bat" move "TEST_ANIMATIONS.bat" "launchers_archive\" >nul
if exist "CONTINUOUS_MINI_TEST.bat" move "CONTINUOUS_MINI_TEST.bat" "launchers_archive\" >nul
if exist "TEST_CONTINU_MINI_VISIBLE.bat" move "TEST_CONTINU_MINI_VISIBLE.bat" "launchers_archive\" >nul
if exist "TEST_MINI_FENETRE_BOUCLE.bat" move "TEST_MINI_FENETRE_BOUCLE.bat" "launchers_archive\" >nul
if exist "LAUNCH_TESTS_SAFE.bat" move "LAUNCH_TESTS_SAFE.bat" "launchers_archive\" >nul
if exist "TEST_MANETTE.bat" move "TEST_MANETTE.bat" "launchers_archive\" >nul

REM Réparation obsolète
if exist "AUTO_FIX.bat" move "AUTO_FIX.bat" "launchers_archive\" >nul
if exist "AUTOFIX_IKEMEN_NOW.bat" move "AUTOFIX_IKEMEN_NOW.bat" "launchers_archive\" >nul
if exist "FIX_GAME_NOW.bat" move "FIX_GAME_NOW.bat" "launchers_archive\" >nul
if exist "REPARER_STAGES_IKEMEN.bat" move "REPARER_STAGES_IKEMEN.bat" "launchers_archive\" >nul
if exist "restore_original_config.bat" move "restore_original_config.bat" "launchers_archive\" >nul

REM IA obsolète
if exist "LAUNCH_ALL_AI_TESTS_SILENT.bat" move "LAUNCH_ALL_AI_TESTS_SILENT.bat" "launchers_archive\" >nul
if exist "STOP_ALL_AI_TESTS.bat" move "STOP_ALL_AI_TESTS.bat" "launchers_archive\" >nul
if exist "MONITOR_AI_LOGS.bat" move "MONITOR_AI_LOGS.bat" "launchers_archive\" >nul

REM Monitoring obsolète
if exist "MONITOR_TESTS.bat" move "MONITOR_TESTS.bat" "launchers_archive\" >nul
if exist "START_MONITORING_ONLY.bat" move "START_MONITORING_ONLY.bat" "launchers_archive\" >nul
if exist "START_WITH_REPORTER.bat" move "START_WITH_REPORTER.bat" "launchers_archive\" >nul
if exist "VOIR_DASHBOARD.bat" move "VOIR_DASHBOARD.bat" "launchers_archive\" >nul
if exist "VOIR_RAPPORT_PORTRAITS.bat" move "VOIR_RAPPORT_PORTRAITS.bat" "launchers_archive\" >nul
if exist "VOIR_TESTS_EN_DIRECT.bat" move "VOIR_TESTS_EN_DIRECT.bat" "launchers_archive\" >nul
if exist "GENERATE_TEST_REPORT.bat" move "GENERATE_TEST_REPORT.bat" "launchers_archive\" >nul

REM Contrôle obsolète
if exist "ARRETER_TESTS_CONTINUS.bat" move "ARRETER_TESTS_CONTINUS.bat" "launchers_archive\" >nul
if exist "DEMARRER_TESTS_CONTINUS.bat" move "DEMARRER_TESTS_CONTINUS.bat" "launchers_archive\" >nul

REM Installation obsolète
if exist "install_ikemen_go.bat" move "install_ikemen_go.bat" "launchers_archive\" >nul
if exist "INSTALL_MANETTE_VIRTUELLE.bat" move "INSTALL_MANETTE_VIRTUELLE.bat" "launchers_archive\" >nul
if exist "SETUP_AUTO_STARTUP.bat" move "SETUP_AUTO_STARTUP.bat" "launchers_archive\" >nul
if exist "create_shortcuts.bat" move "create_shortcuts.bat" "launchers_archive\" >nul
if exist "CREER_RACCOURCI_BUREAU.bat" move "CREER_RACCOURCI_BUREAU.bat" "launchers_archive\" >nul

REM Autres obsolètes
if exist "START_KOF_ULTIMATE.bat" move "START_KOF_ULTIMATE.bat" "launchers_archive\" >nul
if exist "LAUNCH_GAME.bat" move "LAUNCH_GAME.bat" "launchers_archive\" >nul
if exist "LAUNCH_WITH_MODE_SELECT.bat" move "LAUNCH_WITH_MODE_SELECT.bat" "launchers_archive\" >nul
if exist "LANCER_JEU_AVEC_GUIDE.bat" move "LANCER_JEU_AVEC_GUIDE.bat" "launchers_archive\" >nul
if exist "LANCER_MINI_FENETRE_CONTINUE.bat" move "LANCER_MINI_FENETRE_CONTINUE.bat" "launchers_archive\" >nul
if exist "LANCER_MINI_FENETRE_SIMPLE.bat" move "LANCER_MINI_FENETRE_SIMPLE.bat" "launchers_archive\" >nul
if exist "PLAY_MINI_WINDOW.bat" move "PLAY_MINI_WINDOW.bat" "launchers_archive\" >nul
if exist "VERIFIER_TOUT.bat" move "VERIFIER_TOUT.bat" "launchers_archive\" >nul
if exist "PREUVE_SYSTEME.bat" move "PREUVE_SYSTEME.bat" "launchers_archive\" >nul

echo   ✓ Fichiers obsolètes archivés dans launchers_archive\

REM ═══════════════════════════════════════════════════════════════════
REM  RÉSUMÉ
REM ═══════════════════════════════════════════════════════════════════

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                  ✅  RÉORGANISATION TERMINÉE                       ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo   📊 Résumé:
echo   • ~25 fichiers renommés avec versioning v2.0
echo   • ~44 fichiers archivés dans launchers_archive\
echo   • Backup créé dans launchers_backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%\
echo.
echo   🎮 Nouveau launcher principal: KOF-LAUNCHER-v2.0-MAIN.bat
echo   🌐 Nouveau lobby online: KOF-ONLINE-v2.0-LOBBY.bat
echo.
echo   Pour lancer le jeu, utilisez maintenant:
echo   • KOF-LAUNCHER-v2.0-MAIN.bat (recommandé)
echo   • KOF-LAUNCHER-v2.0-SIMPLE.bat (lancement direct)
echo   • KOF-LAUNCHER-v2.0-STABLE-10.bat (10 persos testés)
echo.
pause
