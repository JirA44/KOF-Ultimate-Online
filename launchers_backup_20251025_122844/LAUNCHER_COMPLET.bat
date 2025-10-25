@echo off
title KOF ULTIMATE ONLINE - Launcher Complet
color 0B

:MENU
cls
echo.
echo ===============================================================================
echo    KOF ULTIMATE ONLINE - LAUNCHER COMPLET
echo ===============================================================================
echo.
echo  1. Lancer le jeu normalement
echo  2. Gestionnaire de profils (Choisir fond anime)
echo  3. Tests automatiques SANS CLAVIER (1 test)
echo  4. Tests automatiques SANS CLAVIER (5 tests continus)
echo  5. Diagnostic complet
echo  6. Corriger les erreurs
echo  0. Quitter
echo.
echo ===============================================================================
echo.

set /p choice="Votre choix: "

if "%choice%"=="1" goto LAUNCH_GAME
if "%choice%"=="2" goto PROFILES
if "%choice%"=="3" goto TEST_SINGLE
if "%choice%"=="4" goto TEST_CONTINUOUS
if "%choice%"=="5" goto DIAGNOSTIC
if "%choice%"=="6" goto FIX
if "%choice%"=="0" goto END

goto MENU

:LAUNCH_GAME
cls
echo.
echo Lancement du jeu...
echo.
start "" "KOF_Ultimate_Online.exe"
timeout /t 2 >nul
goto MENU

:PROFILES
cls
echo.
echo ===============================================================================
echo    GESTIONNAIRE DE PROFILS
echo ===============================================================================
echo.
python PROFILE_MANAGER.py
pause
goto MENU

:TEST_SINGLE
cls
echo.
echo ===============================================================================
echo    TEST AUTOMATIQUE SANS CLAVIER (1 test)
echo ===============================================================================
echo.
echo IMPORTANT: Vos touches restent LIBRES pendant le test !
echo.
pause
python TEST_AUTO_SANS_CLAVIER.py
pause
goto MENU

:TEST_CONTINUOUS
cls
echo.
echo ===============================================================================
echo    TESTS AUTOMATIQUES CONTINUS (5 tests)
echo ===============================================================================
echo.
echo IMPORTANT: Vos touches restent LIBRES pendant les tests !
echo Le jeu va se lancer/fermer automatiquement 5 fois.
echo.
pause
echo 2 | python TEST_AUTO_SANS_CLAVIER.py
pause
goto MENU

:DIAGNOSTIC
cls
echo.
echo ===============================================================================
echo    DIAGNOSTIC COMPLET
echo ===============================================================================
echo.
python DIAGNOSTIC_PRO_COMPLET.py
pause
goto MENU

:FIX
cls
echo.
echo ===============================================================================
echo    CORRECTION DES ERREURS
echo ===============================================================================
echo.
echo 1. Corriger erreurs de configuration
echo 2. Reconstruire select.def intelligent
echo 3. Scanner erreurs CLSN dans fichiers .air
echo 0. Retour
echo.
set /p fixchoice="Votre choix: "

if "%fixchoice%"=="1" (
    python AUTO_FIX_ALL_ERRORS.py
    pause
    goto FIX
)
if "%fixchoice%"=="2" (
    python FIX_SELECT_INTELLIGENT.py
    pause
    goto FIX
)
if "%fixchoice%"=="3" (
    python SCAN_AND_FIX_CLSN_ERRORS.py
    pause
    goto FIX
)
goto MENU

:END
cls
echo.
echo Au revoir !
echo.
timeout /t 2 >nul
exit
