@echo off
REM =========================================
REM   LAUNCHER MASTER - TOUS TESTS IA
REM   Lance TOUTES les IA en silencieux
REM   pour tester tous les modes de jeu
REM =========================================

title KOF - Tests Complets IA Silencieux

color 0A

echo.
echo ========================================
echo   🤖 TESTS COMPLETS IA - MODE SILENCIEUX
echo ========================================
echo.
echo Ce launcher va demarrer:
echo.
echo   [1] IA Multi-Modes (3 instances)
echo   [2] IA vs IA Match
echo   [3] IA Silent Players
echo   [4] Virtual Players AI
echo.
echo Tous les tests tournent en arriere-plan
echo sans vous deranger !
echo ========================================
echo.

cd /d "D:\KOF Ultimate Online"

REM Creer les dossiers de logs
if not exist "logs" mkdir logs
if not exist "test_results" mkdir test_results

echo [%time%] Demarrage des tests...
echo.

REM ========================================
REM   TEST 1: IA Multi-Modes (3 instances)
REM ========================================
echo [1/4] Lancement IA Multi-Modes...
echo        Instance 1: Mode Balanced
start /MIN "AI-MultiMode-1" python AI_MULTI_MODE_SYSTEM.py
timeout /t 5 /nobreak > nul

echo        Instance 2: Mode Aggressive
start /MIN "AI-MultiMode-2" python AI_MULTI_MODE_SYSTEM.py
timeout /t 5 /nobreak > nul

echo        Instance 3: Mode Defensive
start /MIN "AI-MultiMode-3" python AI_MULTI_MODE_SYSTEM.py
timeout /t 5 /nobreak > nul

echo        ✓ 3 IA Multi-Modes lancees
echo.

REM ========================================
REM   TEST 2: IA vs IA Match
REM ========================================
echo [2/4] Lancement AI vs AI Match...
start /MIN "AI-vs-AI" python ai_vs_ai_match.py
timeout /t 3 /nobreak > nul
echo        ✓ AI vs AI lance
echo.

REM ========================================
REM   TEST 3: IA Silent Players
REM ========================================
echo [3/4] Lancement IA Silent Players...
start /MIN "AI-Silent" python AI_PLAYS_SILENT.py
timeout /t 3 /nobreak > nul
echo        ✓ IA Silent lancee
echo.

REM ========================================
REM   TEST 4: Virtual Players AI
REM ========================================
echo [4/4] Lancement Virtual Players...
start /MIN "AI-Virtual" python virtual_players_ai.py
timeout /t 3 /nobreak > nul
echo        ✓ Virtual Players lances
echo.

REM ========================================
REM   MONITORING
REM ========================================
echo.
echo ========================================
echo   ✅ TOUS LES TESTS SONT LANCES !
echo ========================================
echo.
echo   Total: 7 processus IA actifs
echo.
echo   📂 Logs:
echo      D:\KOF Ultimate Online\logs\
echo.
echo   📊 Resultats:
echo      D:\KOF Ultimate Online\test_results\
echo.
echo   🖥️  Processus actifs:
echo.

tasklist | findstr /I "python.exe" | find /C "python.exe" > temp_count.txt
set /p AI_COUNT=<temp_count.txt
del temp_count.txt

echo      %AI_COUNT% processus Python detectes
echo.
echo ========================================
echo.
echo   Pour arreter tous les tests:
echo      STOP_ALL_AI_TESTS.bat
echo.
echo   Pour voir les logs en temps reel:
echo      MONITOR_AI_LOGS.bat
echo.
echo ========================================
echo.
echo Appuyez sur une touche pour fermer...
pause > nul
