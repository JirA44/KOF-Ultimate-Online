@echo off
REM =========================================
REM   ARRÊT DE TOUS LES TESTS IA
REM =========================================

title KOF - Arrêt Tests IA

color 0C

echo.
echo ========================================
echo   ⏹️  ARRÊT DE TOUS LES TESTS IA
echo ========================================
echo.

echo Arret des processus Python...

REM Compter les processus avant
tasklist | findstr /I "python.exe" | find /C "python.exe" > temp_before.txt
set /p BEFORE=<temp_before.txt
del temp_before.txt

echo Processus detectes: %BEFORE%
echo.

REM Arrêter tous les processus Python
wmic process where "name='python.exe'" call terminate > nul 2>&1

timeout /t 2 /nobreak > nul

REM Compter après
tasklist | findstr /I "python.exe" | find /C "python.exe" > temp_after.txt 2>nul
set /p AFTER=<temp_after.txt 2>nul
if exist temp_after.txt del temp_after.txt

if "%AFTER%"=="" set AFTER=0

echo.
echo ========================================
echo   ✅ PROCESSUS ARRETES
echo ========================================
echo.
echo   Avant:  %BEFORE% processus
echo   Apres:  %AFTER% processus
echo.
echo ========================================
echo.
pause
