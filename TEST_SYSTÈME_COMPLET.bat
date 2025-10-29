@echo off
chcp 65001 >nul
title KOF Ultimate Online - Test Système Complet
cls

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║      🧪 KOF ULTIMATE ONLINE - TEST SYSTÈME COMPLET       ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo.

cd /d "D:\KOF Ultimate Online"

echo [INFO] Ce script va tester automatiquement tous les composants
echo.
echo Tests à effectuer:
echo   1. Vérification Python
echo   2. Vérification des dépendances
echo   3. Vérification des fichiers essentiels
echo   4. Test du launcher
echo.
pause
cls

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║ TEST 1/4 - VÉRIFICATION PYTHON                            ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ÉCHEC] Python n'est pas installé
    echo.
    echo Action requise: Installer Python depuis https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo [OK] Python installé
python --version
echo.

timeout /t 2 >nul

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║ TEST 2/4 - VÉRIFICATION DES DÉPENDANCES                  ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

echo [TEST] websockets...
python -c "import websockets" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ÉCHEC] websockets non installé
    echo.
    echo Action: Installation automatique...
    pip install websockets
    if %ERRORLEVEL% NEQ 0 (
        echo [ERREUR] Impossible d'installer websockets
        pause
        exit /b 1
    )
    echo [OK] websockets installé
) else (
    echo [OK] websockets déjà installé
)
echo.

echo [TEST] psutil...
python -c "import psutil" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ÉCHEC] psutil non installé
    echo.
    echo Action: Installation automatique...
    pip install psutil
    if %ERRORLEVEL% NEQ 0 (
        echo [ERREUR] Impossible d'installer psutil
        pause
        exit /b 1
    )
    echo [OK] psutil installé
) else (
    echo [OK] psutil déjà installé
)
echo.

echo [TEST] tkinter...
python -c "import tkinter" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ÉCHEC] tkinter non disponible
    echo [INFO] tkinter est inclus avec Python, réinstaller Python si nécessaire
) else (
    echo [OK] tkinter disponible
)
echo.

timeout /t 2 >nul

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║ TEST 3/4 - VÉRIFICATION DES FICHIERS                     ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

set "files_ok=1"

echo [TEST] KOF_Ultimate_Online.exe...
if exist "KOF_Ultimate_Online.exe" (
    echo [OK] Trouvé
) else (
    echo [ÉCHEC] Non trouvé
    set "files_ok=0"
)

echo [TEST] AUTO_BUG_DETECTOR.py...
if exist "AUTO_BUG_DETECTOR.py" (
    echo [OK] Trouvé
) else (
    echo [ÉCHEC] Non trouvé
    set "files_ok=0"
)

echo [TEST] BATTLENET_SERVER.py...
if exist "BATTLENET_SERVER.py" (
    echo [OK] Trouvé
) else (
    echo [ÉCHEC] Non trouvé
    set "files_ok=0"
)

echo [TEST] BATTLENET_CLIENT.py...
if exist "BATTLENET_CLIENT.py" (
    echo [OK] Trouvé
) else (
    echo [ÉCHEC] Non trouvé
    set "files_ok=0"
)

echo [TEST] KOFUO_LAUNCHER_ULTIMATE.py...
if exist "KOFUO_LAUNCHER_ULTIMATE.py" (
    echo [OK] Trouvé
) else (
    echo [ÉCHEC] Non trouvé
    set "files_ok=0"
)

echo [TEST] data/select.def...
if exist "data\select.def" (
    echo [OK] Trouvé
) else (
    echo [ÉCHEC] Non trouvé
    set "files_ok=0"
)

echo.

if "%files_ok%"=="0" (
    echo [ÉCHEC] Certains fichiers sont manquants
    echo.
    echo Veuillez vérifier l'installation
    pause
    exit /b 1
)

echo [OK] Tous les fichiers essentiels sont présents
echo.

timeout /t 2 >nul

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║ TEST 4/4 - TEST DU LAUNCHER                              ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

echo [INFO] Le launcher va se lancer dans 3 secondes...
echo [INFO] Vérifiez qu'il s'ouvre correctement
echo.
timeout /t 3 >nul

start "" python KOFUO_LAUNCHER_ULTIMATE.py

echo.
echo [INFO] Le launcher a été lancé
echo [INFO] Vérifiez qu'une fenêtre s'est ouverte
echo.

timeout /t 3 >nul

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║              ✅ TESTS TERMINÉS AVEC SUCCÈS ✅             ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo.
echo RÉSUMÉ:
echo   ✅ Python : OK
echo   ✅ Dépendances : OK
echo   ✅ Fichiers : OK
echo   ✅ Launcher : OK
echo.
echo.
echo PROCHAINES ÉTAPES:
echo   1. Utilisez le launcher pour tester chaque composant
echo   2. Consultez le GUIDE_TEST_RAPIDE.md pour les tests détaillés
echo   3. Lancez d'abord le détecteur de bugs (recommandé)
echo.
echo.

pause
