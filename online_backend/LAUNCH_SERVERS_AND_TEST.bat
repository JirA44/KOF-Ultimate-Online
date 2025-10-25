@echo off
REM Lancement des serveurs et test multijoueur
cd /d "%~dp0"

echo.
echo ================================================================================
echo   LANCEMENT SYSTEME MULTIJOUEUR COMPLET - KOF Ultimate Online
echo ================================================================================
echo.

REM Vérifier que node_modules existe
if not exist "node_modules" (
    echo [ERREUR] node_modules manquant - Installation des dependances...
    call npm install
    if errorlevel 1 (
        echo [ERREUR] npm install a echoue
        pause
        exit /b 1
    )
)

echo [1/4] Nettoyage des processus existants...
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 >nul

echo [2/4] Lancement API Server (port 3100)...
start /MIN "KOF API Server" cmd /c "node api_server.js > api_server.log 2>&1"
timeout /t 3 >nul

echo [3/4] Lancement Matchmaking Server (port 3101)...
start /MIN "KOF Matchmaking Server" cmd /c "node matchmaking_server.js > matchmaking_server.log 2>&1"
timeout /t 3 >nul

echo [4/4] Verification des serveurs...
timeout /t 5 >nul

REM Test de santé de l'API
curl -s http://localhost:3100/api/health >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] API Server ne repond pas
    echo Verifiez api_server.log pour plus de details
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo   [OK] SERVEURS LANCES AVEC SUCCES!
echo ================================================================================
echo.
echo   - API Server:          http://localhost:3100
echo   - Matchmaking Server:  ws://localhost:3101
echo   - Base de donnees:     kof_online.db
echo.
echo ================================================================================
echo.

echo Appuyez sur une touche pour lancer le test de simulation multijoueur...
pause >nul

echo.
echo ================================================================================
echo   LANCEMENT TEST SIMULATION MULTIJOUEUR
echo ================================================================================
echo.

node TEST_MULTIPLAYER_SIMULATION.js

echo.
echo.
echo ================================================================================
echo   Test termine!
echo ================================================================================
echo.
echo Pour arreter les serveurs:
echo   - Fermez cette fenetre ou appuyez sur Ctrl+C
echo   - Ou executez: taskkill /F /IM node.exe
echo.
pause
