@echo off
title KOF Ultimate - Test Continu Mini-Fenêtre

echo ════════════════════════════════════════════════════════════
echo   🪟 KOF ULTIMATE - Test Continu en Mini-Fenêtre
echo ════════════════════════════════════════════════════════════
echo.
echo Configuration appliquée : Mode fenêtré 640x480
echo.
echo Lancement du jeu en mode test automatique...
echo Les fenêtres seront petites et non intrusives.
echo.
echo ⚠️  Pour arrêter : Fermer cette fenêtre ou CTRL+C
echo.

timeout /t 3 /nobreak >nul

:LOOP

echo ═══════════════════════════════════════════════════════════
echo   Lancement nouvelle session de test...
echo   %date% %time%
echo ═══════════════════════════════════════════════════════════

REM Lancer le jeu en mini-fenêtre avec l'IA silencieuse
start /MIN "" "D:\KOF Ultimate Online\KOF_Ultimate_Online.exe"

REM Attendre 3 minutes (180 secondes) pour que l'IA teste
echo Attente 3 minutes pour test automatique...
timeout /t 180 /nobreak >nul

REM Fermer le jeu proprement
echo Fermeture de la session de test...
taskkill /IM "KOF_Ultimate_Online.exe" /F >nul 2>&1

REM Attendre 10 secondes avant de relancer
echo Pause 10 secondes...
timeout /t 10 /nobreak >nul

REM Sauvegarder les logs
if exist "mugen.log" (
    echo Sauvegarde du log...
    copy /Y "mugen.log" "logs\test_mini_%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log" >nul 2>&1
)

REM Boucler
goto LOOP
