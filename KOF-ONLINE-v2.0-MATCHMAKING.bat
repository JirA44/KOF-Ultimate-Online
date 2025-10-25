@echo off
echo ============================================================
echo    KOF ULTIMATE ONLINE - DEMARRAGE SYSTEME MATCHMAKING
echo ============================================================
echo.

echo [1/2] Lancement du serveur de matchmaking...
start "Serveur Matchmaking" cmd /k "python matchmaking_server.py"

echo.
echo [2/2] Attente de 3 secondes...
timeout /t 3 /nobreak > nul

echo.
echo [3/3] Lancement du launcher...
python launcher_with_profiles.py

echo.
echo ============================================================
echo    Systeme arrete
echo ============================================================
pause
