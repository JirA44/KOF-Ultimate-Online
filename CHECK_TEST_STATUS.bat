@echo off
chcp 65001 >nul
title Status Tests KOF - Vérification en cours
color 0B
cls

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🔍 STATUS DES TESTS - KOF ULTIMATE ONLINE                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo ⏰ Heure: %TIME%
echo.
echo ══════════════════════════════════════════════════════════════
echo   PROCESSUS EN COURS
echo ══════════════════════════════════════════════════════════════
echo.

REM Vérifier Python
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Test Python: EN COURS
    for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr "PID"') do (
        echo    PID: %%a
    )
) else (
    echo ❌ Test Python: TERMINÉ ou NON LANCÉ
)

echo.

REM Vérifier jeu
tasklist /FI "IMAGENAME eq KOF_Ultimate_Online.exe" 2>nul | find /I "KOF" >nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Jeu KOF: EN COURS
) else (
    echo ⏸️  Jeu KOF: Arrêté
)

echo.
echo ══════════════════════════════════════════════════════════════
echo   LOGS MUGEN
echo ══════════════════════════════════════════════════════════════
echo.

if exist mugen.log (
    echo Dernières lignes du log:
    echo.
    powershell -Command "Get-Content mugen.log -Tail 10"
) else (
    echo Aucun log disponible
)

echo.
echo ══════════════════════════════════════════════════════════════
echo.
pause
