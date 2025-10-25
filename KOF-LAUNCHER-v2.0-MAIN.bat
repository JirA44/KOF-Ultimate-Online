@echo off
chcp 65001 >nul
color 0B
title KOF Ultimate Online - Main Launcher v2.0

:MAIN_MENU
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                            ║
echo ║              ██╗  ██╗ ██████╗ ███████╗    ██╗   ██╗██╗  ████████╗         ║
echo ║              ██║ ██╔╝██╔═══██╗██╔════╝    ██║   ██║██║  ╚══██╔══╝         ║
echo ║              █████╔╝ ██║   ██║█████╗      ██║   ██║██║     ██║            ║
echo ║              ██╔═██╗ ██║   ██║██╔══╝      ██║   ██║██║     ██║            ║
echo ║              ██║  ██╗╚██████╔╝██║         ╚██████╔╝███████╗██║            ║
echo ║              ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ╚═════╝ ╚══════╝╚═╝            ║
echo ║                                                                            ║
echo ║                         ULTIMATE ONLINE  v2.0                              ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo    ┌─────────────────────────────────────────────────────────────────────┐
echo    │                        🎮  SOLO / LOCAL                             │
echo    └─────────────────────────────────────────────────────────────────────┘
echo.
echo       [1] 🎯 Lancer le jeu (Simple)
echo       [2] 🎯 Lancer le jeu (Stable 10 personnages)
echo       [3] 🎯 Lancement rapide
echo.
echo    ┌─────────────────────────────────────────────────────────────────────┐
echo    │                     🌐  ONLINE MULTIPLAYER                          │
echo    └─────────────────────────────────────────────────────────────────────┘
echo.
echo       [4] 🌐 Système Matchmaking
echo       [5] 🌐 Démarrer Serveur
echo       [6] 🌐 Jouer vs IA Online
echo       [7] 🌐 Lobby Multi-Joueurs
echo.
echo    ┌─────────────────────────────────────────────────────────────────────┐
echo    │                     🧪  TEST ^& DIAGNOSTIC                           │
echo    └─────────────────────────────────────────────────────────────────────┘
echo.
echo       [8] 🧪 Test exhaustif personnages
echo       [9] 🧪 Auto-diagnostic complet
echo.
echo    ┌─────────────────────────────────────────────────────────────────────┐
echo    │                     ⚙️  CONFIGURATION ^& OUTILS                      │
echo    └─────────────────────────────────────────────────────────────────────┘
echo.
echo       [R] 🔧 Outils de Réparation
echo       [C] ⚙️  Configuration
echo       [D] 📊 Dashboard
echo.
echo       [0] ❌ Quitter
echo.
echo ══════════════════════════════════════════════════════════════════════════════
echo.
set /p choice="   Votre choix: "

if "%choice%"=="1" goto LAUNCH_SIMPLE
if "%choice%"=="2" goto LAUNCH_STABLE
if "%choice%"=="3" goto LAUNCH_QUICK
if "%choice%"=="4" goto ONLINE_MATCHMAKING
if "%choice%"=="5" goto ONLINE_SERVER
if "%choice%"=="6" goto ONLINE_VS_AI
if "%choice%"=="7" goto ONLINE_LOBBY
if "%choice%"=="8" goto TEST_EXHAUSTIF
if "%choice%"=="9" goto TEST_DIAGNOSTIC
if /i "%choice%"=="R" goto MENU_REPAIR
if /i "%choice%"=="C" goto MENU_CONFIG
if /i "%choice%"=="D" goto DASHBOARD
if "%choice%"=="0" goto EXIT

goto MAIN_MENU

REM ═══════════════════════════════════════════════════════════════════════════════
REM  SOLO / LOCAL
REM ═══════════════════════════════════════════════════════════════════════════════

:LAUNCH_SIMPLE
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║          🎮  LANCEMENT SIMPLE - TOUS PERSONNAGES ACTIFS            ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo   Lancement du jeu avec tous les personnages actifs (121 personnages)
echo.
cd /d "D:\KOF Ultimate Online"
start "" "KOF_Ultimate_Online.exe"
echo.
echo   ✓ Jeu lancé!
echo.
timeout /t 3
goto MAIN_MENU

:LAUNCH_STABLE
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║          🎯  LANCEMENT STABLE - 10 PERSONNAGES TESTÉS              ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo   Lancement avec 10 personnages ultra-testés pour stabilité maximale
echo.
echo   Personnages: Hunter_U6746, NeoDio KOFM, Athena, akuma, Kei,
echo                Rose, Ryuji, Nero, Viper, Eve
echo.
cd /d "D:\KOF Ultimate Online"

REM Backup current select.def
if exist "data\select.def" copy /Y "data\select.def" "data\select.def.backup" >nul

REM Use minimal select
copy /Y "data\select_minimal.def" "data\select.def" >nul

start "" "KOF_Ultimate_Online.exe"
echo.
echo   ✓ Jeu lancé en mode stable!
echo   ℹ  select.def sauvegardé dans select.def.backup
echo.
timeout /t 3
goto MAIN_MENU

:LAUNCH_QUICK
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║               ⚡  LANCEMENT RAPIDE                                  ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
cd /d "D:\KOF Ultimate Online"
start "" "KOF_Ultimate_Online.exe"
echo   ✓ Lancé!
timeout /t 1
goto MAIN_MENU

REM ═══════════════════════════════════════════════════════════════════════════════
REM  ONLINE MULTIPLAYER
REM ═══════════════════════════════════════════════════════════════════════════════

:ONLINE_MATCHMAKING
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║          🌐  SYSTÈME MATCHMAKING ONLINE                            ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo   Démarrage du système de matchmaking...
echo.
cd /d "D:\KOF Ultimate Online"
if exist "START_MATCHMAKING_SYSTEM.bat" (
    call "START_MATCHMAKING_SYSTEM.bat"
) else (
    echo   ❌ Fichier START_MATCHMAKING_SYSTEM.bat non trouvé
    echo.
    pause
)
goto MAIN_MENU

:ONLINE_SERVER
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║          🌐  DÉMARRAGE SERVEUR MULTIJOUEUR                         ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo   Démarrage du serveur...
echo.
cd /d "D:\KOF Ultimate Online"
if exist "START_SERVER.bat" (
    call "START_SERVER.bat"
) else (
    echo   ❌ Fichier START_SERVER.bat non trouvé
    echo.
    pause
)
goto MAIN_MENU

:ONLINE_VS_AI
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║          🌐  JOUER VS IA ONLINE                                    ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo   Lancement du mode VS IA Online...
echo.
cd /d "D:\KOF Ultimate Online"
if exist "JOUER_CONTRE_IA_ONLINE.bat" (
    call "JOUER_CONTRE_IA_ONLINE.bat"
) else (
    echo   ❌ Fichier JOUER_CONTRE_IA_ONLINE.bat non trouvé
    echo.
    pause
)
goto MAIN_MENU

:ONLINE_LOBBY
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║          🌐  LOBBY MULTI-JOUEURS (En développement)                ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo   Cette fonctionnalité est en cours de développement.
echo.
echo   Fonctionnalités prévues:
echo   • Liste des joueurs en ligne
echo   • Création de salles personnalisées
echo   • Chat en temps réel
echo   • Système de classement
echo.
pause
goto MAIN_MENU

REM ═══════════════════════════════════════════════════════════════════════════════
REM  TEST & DIAGNOSTIC
REM ═══════════════════════════════════════════════════════════════════════════════

:TEST_EXHAUSTIF
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║          🧪  TEST EXHAUSTIF DES PERSONNAGES                        ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo   Lancement du test de tous les personnages...
echo.
cd /d "D:\KOF Ultimate Online"
if exist "LANCER_TEST_EXHAUSTIF.bat" (
    call "LANCER_TEST_EXHAUSTIF.bat"
) else (
    echo   ❌ Fichier LANCER_TEST_EXHAUSTIF.bat non trouvé
    echo.
    pause
)
goto MAIN_MENU

:TEST_DIAGNOSTIC
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║          🧪  AUTO-DIAGNOSTIC COMPLET                               ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo   Lancement de l'auto-diagnostic...
echo.
cd /d "D:\KOF Ultimate Online"
if exist "LANCER_AUTO_DIAGNOSTIC.bat" (
    call "LANCER_AUTO_DIAGNOSTIC.bat"
) else (
    echo   ❌ Fichier LANCER_AUTO_DIAGNOSTIC.bat non trouvé
    echo.
    pause
)
goto MAIN_MENU

REM ═══════════════════════════════════════════════════════════════════════════════
REM  MENU RÉPARATION
REM ═══════════════════════════════════════════════════════════════════════════════

:MENU_REPAIR
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                   🔧  OUTILS DE RÉPARATION                         ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo   [1] 🔧 Correction des crashes
echo   [2] 🔧 Réparation générale
echo   [3] 🔧 Réparer Ikemen GO
echo   [4] 🔧 Nettoyer portraits cassés
echo.
echo   [0] ← Retour
echo.
set /p repair_choice="   Votre choix: "

if "%repair_choice%"=="1" (
    if exist "CORRIGER_CRASH.bat" (
        call "CORRIGER_CRASH.bat"
    ) else (
        echo   ❌ Fichier non trouvé
        pause
    )
    goto MENU_REPAIR
)
if "%repair_choice%"=="2" (
    if exist "REPARER_JEU.bat" (
        call "REPARER_JEU.bat"
    ) else (
        echo   ❌ Fichier non trouvé
        pause
    )
    goto MENU_REPAIR
)
if "%repair_choice%"=="3" (
    if exist "FIX_IKEMEN_GO.bat" (
        call "FIX_IKEMEN_GO.bat"
    ) else (
        echo   ❌ Fichier non trouvé
        pause
    )
    goto MENU_REPAIR
)
if "%repair_choice%"=="4" (
    if exist "NETTOYER_PORTRAITS_CASSES.bat" (
        call "NETTOYER_PORTRAITS_CASSES.bat"
    ) else (
        echo   ❌ Fichier non trouvé
        pause
    )
    goto MENU_REPAIR
)
if "%repair_choice%"=="0" goto MAIN_MENU
goto MENU_REPAIR

REM ═══════════════════════════════════════════════════════════════════════════════
REM  MENU CONFIGURATION
REM ═══════════════════════════════════════════════════════════════════════════════

:MENU_CONFIG
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                   ⚙️  CONFIGURATION                                 ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo   [1] ⚙️  Restaurer configuration par défaut
echo   [2] ⚙️  Restaurer select.def depuis backup
echo   [3] ⚙️  Voir configuration actuelle
echo.
echo   [0] ← Retour
echo.
set /p config_choice="   Votre choix: "

if "%config_choice%"=="1" (
    cd /d "D:\KOF Ultimate Online"
    if exist "restore_original_config.bat" (
        call "restore_original_config.bat"
    ) else (
        echo   ❌ Fichier non trouvé
    )
    pause
    goto MENU_CONFIG
)
if "%config_choice%"=="2" (
    cd /d "D:\KOF Ultimate Online"
    if exist "data\select.def.backup" (
        copy /Y "data\select.def.backup" "data\select.def" >nul
        echo   ✓ select.def restauré depuis backup
    ) else (
        echo   ❌ Aucun backup trouvé
    )
    pause
    goto MENU_CONFIG
)
if "%config_choice%"=="3" (
    cd /d "D:\KOF Ultimate Online"
    if exist "data\select.def" (
        notepad "data\select.def"
    ) else (
        echo   ❌ select.def non trouvé
        pause
    )
    goto MENU_CONFIG
)
if "%config_choice%"=="0" goto MAIN_MENU
goto MENU_CONFIG

REM ═══════════════════════════════════════════════════════════════════════════════
REM  DASHBOARD
REM ═══════════════════════════════════════════════════════════════════════════════

:DASHBOARD
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                   📊  DASHBOARD KOF ULTIMATE                       ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
cd /d "D:\KOF Ultimate Online"
if exist "OUVRIR_DASHBOARD.bat" (
    call "OUVRIR_DASHBOARD.bat"
) else (
    echo   ❌ Fichier OUVRIR_DASHBOARD.bat non trouvé
    echo.
    pause
)
goto MAIN_MENU

REM ═══════════════════════════════════════════════════════════════════════════════
REM  EXIT
REM ═══════════════════════════════════════════════════════════════════════════════

:EXIT
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                                                                    ║
echo ║                  Merci d'avoir utilisé                             ║
echo ║              KOF ULTIMATE ONLINE v2.0                              ║
echo ║                                                                    ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
timeout /t 2
exit
