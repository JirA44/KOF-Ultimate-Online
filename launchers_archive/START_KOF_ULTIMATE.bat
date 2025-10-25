@echo off
chcp 65001 > nul
title KOF ULTIMATE - Menu Principal

:menu
cls
echo.
echo ============================================================
echo   🎮 KOF ULTIMATE - MENU PRINCIPAL
echo ============================================================
echo.
echo   MODES DE JEU:
echo   ─────────────────────────────────────────────────────────
echo.
echo   [1] 🎮 JOUER SOLO (Vous vs IA locale)
echo   [2] 🌐 JOUER vs IA EN LIGNE (Netplay simulé)
echo   [3] 🥊 JOUER EN LOCAL (2 joueurs)
echo.
echo   OUTILS:
echo   ─────────────────────────────────────────────────────────
echo.
echo   [4] 🔧 Launcher Auto-Diagnostic
echo   [5] 📋 Générateur de Select.def
echo   [6] 🎮 Mapper Manette → Clavier
echo   [7] ✅ Vérifier Installation
echo.
echo   [0] ❌ QUITTER
echo.
echo ============================================================
echo.
set /p choice="Votre choix: "

if "%choice%"=="1" goto jouer_solo
if "%choice%"=="2" goto jouer_online
if "%choice%"=="3" goto jouer_local
if "%choice%"=="4" goto diagnostic
if "%choice%"=="5" goto select_def
if "%choice%"=="6" goto mapper
if "%choice%"=="7" goto check_install
if "%choice%"=="0" goto quit

echo.
echo ❌ Choix invalide!
timeout /t 2 > nul
goto menu

:jouer_solo
cls
echo.
echo ============================================================
echo   🎮 MODE SOLO - Vous vs IA Locale
echo ============================================================
echo.
call "JOUER_LOCAL_VS_IA.bat"
goto menu

:jouer_online
cls
echo.
echo ============================================================
echo   🌐 MODE NETPLAY - Vous vs IA en Ligne
echo ============================================================
echo.
call "JOUER_CONTRE_IA_ONLINE.bat"
goto menu

:jouer_local
cls
echo.
echo ============================================================
echo   🥊 MODE LOCAL - 2 Joueurs
echo ============================================================
echo.
echo Choisissez le moteur:
echo.
echo   [1] M.U.G.E.N
echo   [2] Ikemen GO
echo.
set /p engine="Votre choix: "

if "%engine%"=="1" (
    cd /d "D:\KOF Ultimate"
    start "" "KOF BLACK R.exe"
) else if "%engine%"=="2" (
    cd /d "D:\KOF Ultimate\Ikemen_GO"
    start "" "Ikemen_GO.exe"
) else (
    echo ❌ Choix invalide!
    timeout /t 2 > nul
    goto menu
)

echo.
echo ✓ Jeu lancé!
echo.
pause
goto menu

:diagnostic
cls
python "D:\KOF Ultimate\launcher_auto_diagnostic.py"
goto menu

:select_def
cls
python "D:\KOF Ultimate\ai_select_def_generator.py"
goto menu

:mapper
cls
echo.
echo ============================================================
echo   🎮 MAPPER MANETTE → CLAVIER
echo ============================================================
echo.
echo Ce mapper convertit votre manette en entrées clavier
echo en temps réel pour jouer au jeu.
echo.
echo ⚠️  Laissez ce mapper tourner pendant que vous jouez!
echo.
pause
start "Mapper Manette" python "D:\KOF Ultimate\gamepad_to_keyboard_mapper.py"
goto menu

:check_install
cls
python "D:\KOF Ultimate\ai_installation_checker.py"
goto menu

:quit
cls
echo.
echo ============================================================
echo   👋 MERCI D'AVOIR JOUÉ À KOF ULTIMATE!
echo ============================================================
echo.
timeout /t 2 > nul
exit
