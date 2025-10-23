@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:MENU
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🎮 KOF ULTIMATE ONLINE - MENU PRINCIPAL                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo   1. 🚀 Lancer le jeu (vérifie et répare auto)
echo   2. 🔍 Vérifier l'installation seulement
echo   3. 🔨 Reconstruire select.def (force)
echo   4. 📊 Voir les statistiques
echo   5. ❌ Quitter
echo.
echo ──────────────────────────────────────────────────────────────
echo.
choice /C 12345 /N /M "Votre choix : "
set CHOICE=%ERRORLEVEL%

if %CHOICE%==1 goto LAUNCH
if %CHOICE%==2 goto VERIFY
if %CHOICE%==3 goto REBUILD
if %CHOICE%==4 goto STATS
if %CHOICE%==5 goto EXIT

:LAUNCH
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🚀 LANCEMENT DU JEU                                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo [1/2] Vérification rapide...
python IKEMEN_CHECKER.py >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo ✅ Installation OK
    echo.
    echo [2/2] Lancement...
    timeout /t 1 /nobreak >nul
    start "" "KOF_Ultimate_Online.exe"
    goto MENU
) else (
    echo ⚠️  Problèmes détectés - Réparation automatique...
    python REBUILD_SELECT.py --yes >nul 2>&1
    echo ✅ Réparé!
    echo.
    echo Lancement...
    timeout /t 1 /nobreak >nul
    start "" "KOF_Ultimate_Online.exe"
    goto MENU
)

:VERIFY
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🔍 VÉRIFICATION COMPLÈTE                                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
python IKEMEN_CHECKER.py
echo.
echo ──────────────────────────────────────────────────────────────
echo.
pause
goto MENU

:REBUILD
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🔨 RECONSTRUCTION DE SELECT.DEF                            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo ⚠️  Cette opération va reconstruire complètement le fichier
echo    select.def en scannant tous les personnages disponibles.
echo.
echo    Un backup sera créé automatiquement.
echo.
choice /C ON /M "Continuer ? (O/N) "
if %ERRORLEVEL%==2 goto MENU

echo.
python REBUILD_SELECT.py --yes
echo.
echo ──────────────────────────────────────────────────────────────
echo.
pause
goto MENU

:STATS
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  📊 STATISTIQUES                                            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Compter les personnages
set /a CHAR_COUNT=0
for /d %%D in ("chars\*") do set /a CHAR_COUNT+=1

:: Compter les stages
set /a STAGE_COUNT=0
for %%F in ("stages\*.def") do set /a STAGE_COUNT+=1

echo   Dossier : %CD%
echo.
echo   📁 Structure :
echo      • Personnages disponibles : %CHAR_COUNT%
echo      • Stages disponibles      : %STAGE_COUNT%
echo.

:: Taille du dossier
for /f "tokens=3" %%a in ('dir /s /-c ^| find "bytes"') do set SIZE=%%a
echo   💾 Espace disque : %SIZE% octets
echo.

:: Vérifier l'état du select.def
if exist "data\select.def" (
    for %%F in ("data\select.def") do set SELECTSIZE=%%~zF
    echo   📄 select.def : !SELECTSIZE! octets
) else (
    echo   📄 select.def : ❌ MANQUANT
)

echo.
echo ──────────────────────────────────────────────────────────────
echo.
pause
goto MENU

:EXIT
cls
echo.
echo À bientôt ! 👋
echo.
timeout /t 1 /nobreak >nul
exit /b 0
