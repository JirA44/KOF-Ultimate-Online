@echo off
chcp 65001 > nul
title KOF ULTIMATE - Rapport Diagnostic Portraits

cd /d "D:\KOF Ultimate Online"

cls
echo ============================================================
echo   🎨 RAPPORT DIAGNOSTIC PORTRAITS
echo ============================================================
echo.
echo Ouverture du rapport visuel HTML...
echo.

start "" "PORTRAIT_DIAGNOSTIC_REPORT.html"

echo.
echo ✓ Rapport ouvert dans votre navigateur!
echo.
pause
