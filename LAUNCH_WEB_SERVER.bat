@echo off
chcp 65001 >nul
title KOF Ultimate Online - Serveur Web
cls

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║        🌐 KOF ULTIMATE ONLINE - SERVEUR WEB 🌐           ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo.

cd /d "D:\KOF Ultimate Online"

echo [INFO] Vérification de Node.js...
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Node.js n'est pas installé
    echo.
    echo Veuillez installer Node.js depuis: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo [OK] Node.js est installé
node --version
echo.

echo [INFO] Vérification des dépendances...
if not exist "node_modules" (
    echo [INFO] Installation des dépendances...
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo [ERREUR] Échec installation des dépendances
        pause
        exit /b 1
    )
    echo [OK] Dépendances installées
    echo.
)

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║              🚀 DÉMARRAGE DU SERVEUR WEB                  ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo.
echo [INFO] Le serveur va démarrer...
echo [INFO] Accédez au site sur: http://localhost:3000
echo.
echo [INFO] Pages disponibles:
echo   - http://localhost:3000/              (Accueil)
echo   - http://localhost:3000/dashboard.html (Dashboard)
echo   - http://localhost:3000/leaderboard.html (Classement)
echo.
echo [INFO] Pour arrêter le serveur: Appuyez sur Ctrl+C
echo.
echo.

node web_server.js

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo.
    echo [ERREUR] Le serveur s'est arrêté avec une erreur
    echo.
    pause
    exit /b 1
)
