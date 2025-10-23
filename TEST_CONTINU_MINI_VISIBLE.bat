@echo off
REM ================================================================
REM KOF ULTIMATE ONLINE - TEST CONTINU EN MINI-FENÊTRE VISIBLE
REM Lance le jeu en boucle infinie avec fenêtre visible
REM ================================================================

title KOF Ultimate - Test Continu Mini Fenêtre
color 0A
mode con: cols=80 lines=30

:DEBUT
cls
echo.
echo ================================================================
echo    KOF ULTIMATE ONLINE - TEST CONTINU MINI-FENETRE
echo ================================================================
echo.
echo [INFO] Ce script lance le jeu en continu en mode mini-fenetre
echo [INFO] La fenetre de jeu reste visible et accessible
echo.
echo ================================================================

REM Compteur de cycles
if not exist "test_cycle_counter.txt" echo 0 > test_cycle_counter.txt
set /p CYCLES=<test_cycle_counter.txt
set /a CYCLES+=1
echo %CYCLES% > test_cycle_counter.txt

echo.
echo [CYCLE %CYCLES%] Preparation du lancement...
echo.

REM Sauvegarder la config si premier cycle
if %CYCLES% equ 1 (
    if not exist "data\mugen.cfg.original_backup" (
        echo [BACKUP] Sauvegarde de la config originale...
        copy /Y "data\mugen.cfg" "data\mugen.cfg.original_backup" >nul
        echo [OK] Backup cree
    )
)

REM Appliquer la config mini-fenêtre visible
echo [CONFIG] Application de la configuration mini-fenetre visible...

python -c "
import re

# Lire config
with open('data/mugen.cfg', 'r', encoding='utf-8', errors='ignore') as f:
    config = f.read()

# Config mini-fenêtre VISIBLE (pas minimisée)
# Taille moyenne pour rester visible à l'écran
changes = {
    r'fullscreen\s*=\s*1': 'fullscreen = 0',     # Mode fenêtré
    r'width\s*=\s*\d+': 'width = 800',           # 800x600 (taille visible)
    r'height\s*=\s*\d+': 'height = 600',         # Ratio 4:3
    r'vretrace\s*=\s*1': 'vretrace = 0',         # Pas de VSync
}

for pattern, replacement in changes.items():
    config = re.sub(pattern, replacement, config)

# Écrire
with open('data/mugen.cfg', 'w', encoding='utf-8') as f:
    f.write(config)

print('[OK] Config mini-fenetre appliquee: 800x600 (visible)')
" 2>nul

if errorlevel 1 (
    echo [WARN] Python non disponible, utilisation PowerShell...
    powershell -Command "(Get-Content 'data\mugen.cfg') -replace 'fullscreen\s*=\s*1', 'fullscreen = 0' -replace 'width\s*=\s*\d+', 'width = 800' -replace 'height\s*=\s*\d+', 'height = 600' -replace 'vretrace\s*=\s*1', 'vretrace = 0' | Set-Content 'data\mugen.cfg'"
)

REM Arrêter les scripts IA
echo [CLEANUP] Arret des scripts IA...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq AI*" >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq IA*" >nul 2>&1
timeout /t 1 /nobreak >nul

REM Vérifier l'exe
if not exist "KOF_Ultimate_Online.exe" (
    echo [ERROR] KOF_Ultimate_Online.exe introuvable!
    pause
    exit /b 1
)

echo.
echo ================================================================
echo [CYCLE %CYCLES%] LANCEMENT EN MINI-FENETRE VISIBLE
echo ================================================================
echo    Taille: 800x600 pixels
echo    Position: Coin superieur gauche
echo    Mode: Fenetre (non plein ecran)
echo    Visibilite: COMPLETE (pas minimise)
echo ================================================================
echo.
echo [INFO] Le jeu va se lancer maintenant...
echo [INFO] Vous pouvez interagir avec la fenetre!
echo [INFO] Pour ARRETER le cycle: Fermez cette console
echo.

REM Lancer le jeu en fenêtre normale (pas minimisée)
start "KOF Ultimate Online - Cycle %CYCLES%" /NORMAL "KOF_Ultimate_Online.exe"

REM Attendre que le jeu démarre
echo [WAIT] Attente du demarrage (10 secondes)...
timeout /t 10 /nobreak

REM Vérifier si le jeu tourne
tasklist | find /i "KOF_Ultimate_Online.exe" >nul
if %errorlevel% equ 0 (
    echo [SUCCESS] Jeu lance avec succes! (Cycle %CYCLES%)
    echo.
    echo [INFO] Le jeu tourne en mini-fenetre visible
    echo [INFO] Vous pouvez:
    echo        - Bouger la fenetre
    echo        - Jouer normalement
    echo        - Observer le test
    echo.
    echo [TIMER] Duree du cycle: 60 secondes
    echo.

    REM Laisser tourner 60 secondes
    for /L %%i in (60,-1,1) do (
        echo [CYCLE %CYCLES%] Temps restant: %%i secondes...
        timeout /t 1 /nobreak >nul
    )

    REM Fermer le jeu proprement
    echo.
    echo [CLEANUP] Fermeture du jeu...
    taskkill /F /IM KOF_Ultimate_Online.exe >nul 2>&1
    timeout /t 2 /nobreak >nul

    echo [OK] Cycle %CYCLES% termine!

) else (
    echo [ERROR] Le jeu n'a pas demarre correctement!
    echo [INFO] Tentative de nettoyage...
    taskkill /F /IM KOF_Ultimate_Online.exe >nul 2>&1
    timeout /t 3
)

REM Pause avant le prochain cycle
echo.
echo ================================================================
echo [PAUSE] Pause de 5 secondes avant le prochain cycle...
echo ================================================================
timeout /t 5 /nobreak

REM Redémarrer le cycle
goto DEBUT
