@echo off
REM ================================================================
REM KOF ULTIMATE ONLINE - TEST EN BOUCLE MINI-FENETRE
REM Version sans erreurs
REM ================================================================

title KOF Ultimate - Test Boucle
color 0A

REM Créer le compteur si inexistant
if not exist "test_cycle_counter.txt" echo 0 > test_cycle_counter.txt

:DEBUT
cls
echo.
echo ================================================================
echo    KOF ULTIMATE ONLINE - TEST BOUCLE MINI-FENETRE
echo ================================================================

REM Incrémenter le compteur
set /p CYCLES=<test_cycle_counter.txt
set /a CYCLES+=1
echo %CYCLES% > test_cycle_counter.txt

echo.
echo [CYCLE %CYCLES%] Preparation...

REM Backup au premier cycle
if %CYCLES% equ 1 (
    if not exist "data\mugen.cfg.original_backup" (
        echo [BACKUP] Sauvegarde de la config...
        copy /Y "data\mugen.cfg" "data\mugen.cfg.original_backup" >nul
    )
)

REM Appliquer config mini-fenêtre
echo [CONFIG] Application mini-fenetre 800x600...
python apply_mini_window_config.py 800 600 2>nul
if errorlevel 1 (
    powershell -NoProfile -Command "$config = Get-Content 'data\mugen.cfg' -Raw; $config = $config -replace 'fullscreen\s*=\s*1', 'fullscreen = 0'; $config = $config -replace 'vretrace\s*=\s*1', 'vretrace = 0'; $config | Set-Content 'data\mugen.cfg' -NoNewline"
)

REM Arrêter les IA
taskkill /F /IM python.exe /FI "WINDOWTITLE eq AI*" >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq IA*" >nul 2>&1
timeout /t 1 /nobreak >nul

echo.
echo ================================================================
echo [CYCLE %CYCLES%] LANCEMENT
echo ================================================================
echo    Taille: 800x600 pixels
echo    Duree:  60 secondes
echo ================================================================
echo.

REM Lancer le jeu
start "KOF Test Cycle %CYCLES%" /NORMAL "KOF_Ultimate_Online.exe"

echo [WAIT] Attente demarrage (10 secondes)...
timeout /t 10 /nobreak >nul

REM Vérifier si lancé
tasklist | find /i "KOF_Ultimate_Online.exe" >nul
if %errorlevel% equ 0 (
    echo [OK] Jeu lance! Cycle %CYCLES% en cours...
    echo.
    echo [TIMER] Duree du cycle: 60 secondes

    REM Compte à rebours visible
    for /L %%i in (60,-5,1) do (
        echo [CYCLE %CYCLES%] Temps restant: %%i secondes...
        timeout /t 5 /nobreak >nul
    )

    echo.
    echo [CLEANUP] Fermeture du jeu...
    taskkill /F /IM KOF_Ultimate_Online.exe >nul 2>&1
    timeout /t 2 /nobreak >nul
    echo [OK] Cycle %CYCLES% termine!
) else (
    echo [ERROR] Echec du lancement!
    taskkill /F /IM KOF_Ultimate_Online.exe >nul 2>&1
    timeout /t 3 /nobreak
)

echo.
echo ================================================================
echo [PAUSE] 5 secondes avant le prochain cycle...
echo ================================================================
timeout /t 5 /nobreak

REM Recommencer
goto DEBUT
