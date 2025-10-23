@echo off
REM ================================================================
REM KOF ULTIMATE ONLINE - MINI-FENETRE VISIBLE (SIMPLIFIÉ)
REM Version sans erreurs - Utilise un script Python séparé
REM ================================================================

title KOF Ultimate - Mini Fenetre
color 0B
cls

echo.
echo ================================================================
echo    KOF ULTIMATE ONLINE - MINI-FENETRE VISIBLE
echo ================================================================
echo.

REM Backup de la config originale
if not exist "data\mugen.cfg.original_backup" (
    echo [1/4] Sauvegarde de la config originale...
    copy /Y "data\mugen.cfg" "data\mugen.cfg.original_backup" >nul
    echo [OK] Backup cree
) else (
    echo [1/4] Backup existant trouve
)

REM Appliquer la config mini-fenêtre
echo.
echo [2/4] Application de la configuration mini-fenetre 800x600...
python apply_mini_window_config.py 800 600
if errorlevel 1 (
    echo [WARN] Script Python echoue, utilisation PowerShell...
    powershell -NoProfile -Command "$config = Get-Content 'data\mugen.cfg' -Raw; $config = $config -replace 'fullscreen\s*=\s*1', 'fullscreen = 0'; $config = $config -replace 'vretrace\s*=\s*1', 'vretrace = 0'; $config | Set-Content 'data\mugen.cfg' -NoNewline"

    REM Modifier aussi width et height avec PowerShell
    powershell -NoProfile -Command "$lines = Get-Content 'data\mugen.cfg'; $inVideo = $false; $result = @(); foreach ($line in $lines) { if ($line -match '^\[Video\]') { $inVideo = $true; $result += $line } elseif ($inVideo -and $line -match '^\[') { $inVideo = $false; $result += $line } elseif ($inVideo -and $line -match '^width') { $result += 'width = 800' } elseif ($inVideo -and $line -match '^height') { $result += 'height = 600' } else { $result += $line } }; $result | Set-Content 'data\mugen.cfg'"

    echo [OK] Configuration appliquee via PowerShell
)

REM Arrêter les scripts IA
echo.
echo [3/4] Arret des scripts IA en arriere-plan...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq AI*" >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq IA*" >nul 2>&1
timeout /t 1 /nobreak >nul
echo [OK] Scripts IA arretes

REM Vérifier l'exe
echo.
echo [4/4] Verification du jeu...
if not exist "KOF_Ultimate_Online.exe" (
    echo [ERROR] KOF_Ultimate_Online.exe introuvable!
    pause
    exit /b 1
)
echo [OK] Executable trouve

REM Lancer le jeu
echo.
echo ================================================================
echo    LANCEMENT EN MINI-FENETRE
echo ================================================================
echo    Taille:      800x600 pixels
echo    Mode:        Fenetre visible
echo    VSync:       Desactive
echo    Framerate:   60 FPS
echo ================================================================
echo.
echo Le jeu va se lancer dans 2 secondes...
timeout /t 2 /nobreak >nul

start "KOF Ultimate - Mini Fenetre" /NORMAL "KOF_Ultimate_Online.exe"

echo.
echo [SUCCESS] Jeu lance en mini-fenetre!
echo.
echo ================================================================
echo    INSTRUCTIONS
echo ================================================================
echo.
echo    - La fenetre est visible a l'ecran (800x600)
echo    - Vous pouvez jouer normalement
echo    - Pour fermer: X dans la fenetre ou Echap
echo    - Pour restaurer plein ecran: RESTORE_FULLSCREEN.bat
echo.
echo ================================================================
echo.
echo Cette fenetre peut etre fermee, le jeu continue!
echo.
pause
