@echo off
REM ================================================================
REM KOF ULTIMATE ONLINE - MINI-FENÊTRE CONTINUE (SIMPLE)
REM Lance le jeu une fois en mini-fenêtre et le laisse tourner
REM ================================================================

title KOF Ultimate - Mini Fenetre Continue
color 0B
cls

echo.
echo ================================================================
echo    KOF ULTIMATE ONLINE - MINI-FENETRE CONTINUE
echo ================================================================
echo.
echo [1/4] Configuration de la mini-fenetre visible...

REM Backup si nécessaire
if not exist "data\mugen.cfg.original_backup" (
    echo [BACKUP] Sauvegarde de la config originale...
    copy /Y "data\mugen.cfg" "data\mugen.cfg.original_backup" >nul
)

REM Appliquer config mini-fenêtre avec Python
echo [CONFIG] Application de la configuration optimisee...
python -c "
import re

with open('data/mugen.cfg', 'r', encoding='utf-8', errors='ignore') as f:
    config = f.read()

# Mini-fenêtre visible et pratique
config = re.sub(r'fullscreen\s*=\s*\d+', 'fullscreen = 0', config)
config = re.sub(r'(?<=[^game])width\s*=\s*\d+', 'width = 800', config)
config = re.sub(r'(?<=[^game])height\s*=\s*\d+', 'height = 600', config)
config = re.sub(r'vretrace\s*=\s*\d+', 'vretrace = 0', config)

with open('data/mugen.cfg', 'w', encoding='utf-8') as f:
    f.write(config)

print('[OK] Mini-fenetre 800x600 configuree')
" 2>nul

if errorlevel 1 (
    echo [WARN] Config automatique echouee, utilisation manuelle...
)

echo.
echo [2/4] Arret des scripts en arriere-plan...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq AI*" >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq IA*" >nul 2>&1
timeout /t 1 /nobreak >nul
echo [OK] Scripts IA arretes

echo.
echo [3/4] Verification du jeu...
if not exist "KOF_Ultimate_Online.exe" (
    echo [ERROR] Executable introuvable!
    pause
    exit /b 1
)
echo [OK] Executable trouve

echo.
echo [4/4] Lancement en mini-fenetre continue...
echo.
echo ================================================================
echo    PARAMETRES
echo ================================================================
echo    Taille:      800x600 pixels
echo    Mode:        Fenetre (redimensionnable)
echo    VSync:       Desactive (reactif)
echo    Framerate:   60 FPS
echo    Duree:       Continue (jusqu'a fermeture)
echo ================================================================
echo.
echo Le jeu va se lancer dans 3 secondes...
timeout /t 3 /nobreak >nul

REM Lancer en fenêtre normale
start "KOF Ultimate - Mini Fenetre" /NORMAL "KOF_Ultimate_Online.exe"

echo.
echo [SUCCESS] Jeu lance en mini-fenetre!
echo.
echo ================================================================
echo    INSTRUCTIONS
echo ================================================================
echo.
echo    La fenetre de jeu est maintenant visible a l'ecran
echo.
echo    VOUS POUVEZ:
echo      - Jouer normalement
echo      - Deplacer la fenetre
echo      - Redimensionner la fenetre
echo      - Basculer vers d'autres programmes (ALT+TAB)
echo.
echo    POUR FERMER LE JEU:
echo      - Cliquer sur X dans la fenetre du jeu
echo      - Ou appuyer sur Echap dans le menu
echo.
echo    POUR RESTAURER LE PLEIN ECRAN:
echo      - Lancer: RESTORE_FULLSCREEN.bat
echo.
echo ================================================================
echo.
echo Cette fenetre peut etre fermee, le jeu continue!
echo.
pause
