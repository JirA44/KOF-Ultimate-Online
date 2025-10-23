@echo off
REM =========================================
REM   MONITORING DES LOGS IA EN TEMPS RÉEL
REM =========================================

title KOF - Monitoring Logs IA

color 0B

:MENU
cls
echo.
echo ========================================
echo   📊 MONITORING LOGS IA
echo ========================================
echo.
echo   Quel log voulez-vous monitorer?
echo.
echo   [1] Tous les logs (resume)
echo   [2] IA Multi-Mode
echo   [3] AI vs AI
echo   [4] IA Silent
echo   [5] Virtual Players
echo   [6] Stats JSON
echo   [7] Retour
echo.
echo ========================================
echo.
set /p CHOICE="Votre choix (1-7): "

if "%CHOICE%"=="1" goto ALL_LOGS
if "%CHOICE%"=="2" goto MULTIMODE
if "%CHOICE%"=="3" goto VSAI
if "%CHOICE%"=="4" goto SILENT
if "%CHOICE%"=="5" goto VIRTUAL
if "%CHOICE%"=="6" goto STATS
if "%CHOICE%"=="7" goto END

goto MENU

:ALL_LOGS
cls
echo.
echo ======== RESUME DE TOUS LES LOGS ========
echo.

if exist "logs\ai_multi_mode.log" (
    echo --- IA Multi-Mode (dernieres lignes) ---
    type "logs\ai_multi_mode.log" | more +50
    echo.
)

if exist "ai_multi_mode.log" (
    echo --- IA Multi-Mode Alt (dernieres lignes) ---
    type "ai_multi_mode.log" | more +50
    echo.
)

echo.
echo ==========================================
pause
goto MENU

:MULTIMODE
cls
echo.
echo ======== LOGS IA MULTI-MODE ========
echo.

if exist "logs\ai_multi_mode.log" (
    type "logs\ai_multi_mode.log"
) else if exist "ai_multi_mode.log" (
    type "ai_multi_mode.log"
) else (
    echo Pas de logs disponibles
)

echo.
echo ====================================
pause
goto MENU

:VSAI
cls
echo.
echo ======== LOGS AI vs AI ========
echo.

if exist "logs\ai_vs_ai.log" (
    type "logs\ai_vs_ai.log"
) else (
    echo Pas de logs disponibles
)

echo.
echo ===============================
pause
goto MENU

:SILENT
cls
echo.
echo ======== LOGS IA SILENT ========
echo.

if exist "logs\ai_silent.log" (
    type "logs\ai_silent.log"
) else (
    echo Pas de logs disponibles
)

echo.
echo ================================
pause
goto MENU

:VIRTUAL
cls
echo.
echo ======== LOGS VIRTUAL PLAYERS ========
echo.

if exist "logs\virtual_players.log" (
    type "logs\virtual_players.log"
) else (
    echo Pas de logs disponibles
)

echo.
echo ======================================
pause
goto MENU

:STATS
cls
echo.
echo ======== STATISTIQUES JSON ========
echo.

if exist "ai_logs\stats_player_1.json" (
    echo --- Player 1 ---
    type "ai_logs\stats_player_1.json"
    echo.
)

if exist "ai_logs\stats_player_2.json" (
    echo --- Player 2 ---
    type "ai_logs\stats_player_2.json"
    echo.
)

if exist "ai_logs\stats_player_3.json" (
    echo --- Player 3 ---
    type "ai_logs\stats_player_3.json"
    echo.
)

echo.
echo ===================================
pause
goto MENU

:END
exit
