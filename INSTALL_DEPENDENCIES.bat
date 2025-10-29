@echo off
chcp 65001 >nul
title KOF Ultimate Online - Installation des Dépendances
cls

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║     📦 KOF ULTIMATE ONLINE - INSTALLATION DÉPENDANCES    ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo.

echo [INFO] Vérification de Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Python n'est pas installé ou n'est pas dans le PATH
    echo.
    echo Veuillez installer Python depuis: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python est installé
python --version
echo.

echo [INFO] Mise à jour de pip...
python -m pip install --upgrade pip
echo.

echo [INFO] Installation des dépendances...
echo.

echo [1/3] Installation de websockets...
pip install websockets
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Échec installation websockets
    pause
    exit /b 1
)
echo [OK] websockets installé
echo.

echo [2/3] Installation de psutil...
pip install psutil
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Échec installation psutil
    pause
    exit /b 1
)
echo [OK] psutil installé
echo.

echo [3/3] Installation de asyncio (vérification)...
python -c "import asyncio; print('[OK] asyncio disponible')"
echo.

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║         ✅ INSTALLATION TERMINÉE AVEC SUCCÈS ✅            ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo.
echo Vous pouvez maintenant lancer le système avec:
echo   - LAUNCH_ULTIMATE.bat
echo.
echo.

pause
