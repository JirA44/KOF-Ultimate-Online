@echo off
chcp 65001 >nul
title KOF Ultimate - Monitoring Tests en Cours
color 0A
cls

:LOOP
cls
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║  📊 MONITORING TESTS EN COURS - KOF ULTIMATE ONLINE          ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo ⏰ Heure: %TIME%
echo.
echo ══════════════════════════════════════════════════════════════
echo   PROCESSUS EN COURS
echo ══════════════════════════════════════════════════════════════
echo.

REM Vérifier si Python tourne
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Tests Python: ACTIFS
    tasklist /FI "IMAGENAME eq python.exe" /FO LIST | findstr "PID Mémoire"
) else (
    echo ❌ Tests Python: ARRÊTÉS
)

echo.

REM Vérifier si le jeu tourne
tasklist /FI "IMAGENAME eq KOF_Ultimate_Online.exe" 2>nul | find /I "KOF" >nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Jeu KOF: EN COURS
    tasklist /FI "IMAGENAME eq KOF_Ultimate_Online.exe" /FO LIST | findstr "PID Mémoire"
) else (
    echo ⏸️  Jeu KOF: Arrêté (normal entre les cycles)
)

echo.
echo ══════════════════════════════════════════════════════════════
echo   DERNIÈRES LIGNES DU LOG MUGEN
echo ══════════════════════════════════════════════════════════════
echo.

if exist mugen.log (
    powershell -Command "Get-Content mugen.log -Tail 5"
) else (
    echo Aucun log disponible
)

echo.
echo ══════════════════════════════════════════════════════════════
echo   LOGS DE TESTS GÉNÉRÉS
echo ══════════════════════════════════════════════════════════════
echo.

if exist logs\ (
    for /f %%i in ('dir /b logs\test_mini_*.log 2^>nul ^| find /c /v ""') do set COUNT=%%i
    echo 📁 Logs mini-tests: %COUNT% fichiers
    dir /b /o-d logs\test_mini_*.log 2>nul | head -3
) else (
    echo Aucun log de test disponible
)

echo.
echo.
echo ══════════════════════════════════════════════════════════════
echo   ⚠️  Pour arrêter les tests: Fermez cette fenêtre et lancez
echo      STOP_ALL.bat ou utilisez Ctrl+C dans les fenêtres de test
echo ══════════════════════════════════════════════════════════════
echo.
echo ⏳ Rafraîchissement dans 10 secondes...
echo.

timeout /t 10 >nul
goto LOOP
