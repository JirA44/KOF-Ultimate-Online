@echo off
REM =========================================
REM   GÉNÉRATEUR DE RAPPORT DE TESTS
REM =========================================

title KOF - Génération Rapport Tests

color 0E

echo.
echo ========================================
echo   📊 GENERATION RAPPORT DE TESTS IA
echo ========================================
echo.

cd /d "D:\KOF Ultimate Online"

python TEST_REPORT_GENERATOR.py

echo.
echo ========================================
echo.
pause
