@echo off
chcp 65001 >nul
color 0B
cls

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║       🌐  KOF ULTIMATE ONLINE - BACKEND COMPLET                ║
echo ║                    Version 2.0.0                               ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM Check if node_modules exists
if not exist "node_modules\" (
    echo ⚠️  node_modules non trouvé. Installation des dépendances...
    echo.
    call npm install
    echo.
)

echo 🚀 Démarrage des serveurs...
echo.
echo    [1] API Server         → http://localhost:3100
echo    [2] Matchmaking Server → ws://localhost:3101
echo.

REM Start API Server in new window
start "KOF API Server" cmd /k "node api_server.js"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start Matchmaking Server in new window
start "KOF Matchmaking Server" cmd /k "node matchmaking_server.js"

echo.
echo ✅ Serveurs démarrés!
echo.
echo 📋 Services disponibles:
echo    • API REST      : http://localhost:3100
echo    • WebSocket     : ws://localhost:3101
echo    • Health Check  : http://localhost:3100/api/health
echo.
echo 📖 Documentation: README.md
echo.
echo Appuyez sur une touche pour ouvrir le dashboard...
pause >nul

start http://localhost:3100/api/health

echo.
echo Pour arrêter les serveurs, fermez les fenêtres de commande.
echo.
pause
