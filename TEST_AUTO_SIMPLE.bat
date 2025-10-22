@echo off
title KOF Test Auto Continu

:LOOP
cls
echo ════════════════════════════════════════════════════════════
echo   🪟 KOF ULTIMATE - Test Automatique Continu
echo   %date% %time%
echo ════════════════════════════════════════════════════════════
echo.
echo ✓ Mode: Mini-fenêtre 640x480
echo ✓ Test en cours...
echo.
echo Pour arrêter: Fermer cette fenêtre
echo.

REM Lancer le jeu en mini-fenêtre
start /MIN "" "D:\KOF Ultimate Online\KOF_Ultimate_Online.exe"

REM Attendre 3 minutes (180 secondes)
echo Cycle de test de 3 minutes...
timeout /t 180 /nobreak >nul

REM Tuer le processus du jeu
taskkill /IM "KOF_Ultimate_Online.exe" /F >nul 2>&1

REM Sauvegarder le log avec timestamp
if exist "mugen.log" (
    if not exist "logs" mkdir logs
    copy /Y "mugen.log" "logs\test_%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log" >nul 2>&1
)

REM Pause avant le prochain cycle
echo.
echo Pause 10 secondes avant prochain cycle...
timeout /t 10 /nobreak >nul

goto LOOP
