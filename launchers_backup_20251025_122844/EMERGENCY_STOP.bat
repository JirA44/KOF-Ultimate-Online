@echo off
title ARRÊT D'URGENCE - KOF
color 0C

echo.
echo ═══════════════════════════════════════════════════════════════
echo    🚨 ARRÊT D'URGENCE - TOUS LES PROCESSUS 🚨
echo ═══════════════════════════════════════════════════════════════
echo.

echo Arrêt de TOUS les processus Python...
taskkill /IM pythonw.exe /F > nul 2>&1
taskkill /IM python.exe /F > nul 2>&1
echo ✅ Python arrêté

echo.
echo Arrêt de TOUS les jeux...
taskkill /IM KOF_Ultimate_Online.exe /F > nul 2>&1
taskkill /IM Ikemen_GO.exe /F > nul 2>&1
taskkill /IM mugen.exe /F > nul 2>&1
echo ✅ Jeux arrêtés

echo.
echo Nettoyage des processus CMD...
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq cmd.exe" /FO LIST ^| find "PID"') do (
    if not "%%a"=="%~p" (
        taskkill /PID %%a /F > nul 2>&1
    )
)
echo ✅ CMD nettoyé

echo.
echo ═══════════════════════════════════════════════════════════════
echo     ✅ TOUT EST ARRÊTÉ !
echo ═══════════════════════════════════════════════════════════════
echo.

pause
