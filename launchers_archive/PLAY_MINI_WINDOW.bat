@echo off
REM ========================================
REM KOF ULTIMATE ONLINE - MINI WINDOW MODE
REM Mode mini-fenêtre optimisé pour jouabilité
REM ========================================

title KOF Ultimate Online - Mini Window Launcher
color 0B
cls

echo.
echo ===============================================
echo    KOF ULTIMATE ONLINE - MINI WINDOW MODE
echo ===============================================
echo.
echo [1/5] Préparation du mode mini-fenêtre...

REM Sauvegarder la config actuelle
if not exist "data\mugen.cfg.fullscreen_backup" (
    echo [BACKUP] Sauvegarde de la config actuelle...
    copy /Y "data\mugen.cfg" "data\mugen.cfg.fullscreen_backup" >nul
    echo [OK] Backup créé: mugen.cfg.fullscreen_backup
)

echo.
echo [2/5] Application de la configuration mini-fenêtre...

REM Créer une config temporaire optimisée pour mini-fenêtre
python -c "
import re

# Lire la config actuelle
with open('data/mugen.cfg', 'r', encoding='utf-8', errors='ignore') as f:
    config = f.read()

# Paramètres optimisés pour mini-fenêtre jouable
changes = {
    r'fullscreen\s*=\s*1': 'fullscreen = 0',  # Mode fenêtré
    r'width\s*=\s*\d+': 'width = 960',         # Taille moyenne (960x720)
    r'height\s*=\s*\d+': 'height = 720',       # Ratio 4:3
    r'vretrace\s*=\s*1': 'vretrace = 0',       # Désactiver VSync pour meilleure réactivité
}

# Appliquer les changements
for pattern, replacement in changes.items():
    config = re.sub(pattern, replacement, config)

# Écrire la nouvelle config
with open('data/mugen.cfg', 'w', encoding='utf-8') as f:
    f.write(config)

print('[OK] Configuration mini-fenêtre appliquée')
print('      - Taille: 960x720 (fenêtré)')
print('      - VSync: Désactivé (meilleure réactivité)')
print('      - Ratio: 4:3 (optimal pour fighting game)')
" 2>nul

if errorlevel 1 (
    echo [WARNING] Échec de la modification automatique.
    echo [INFO] Application manuelle de la config mini-fenêtre...

    REM Fallback: Modifier directement avec PowerShell
    powershell -Command "(Get-Content 'data\mugen.cfg') -replace 'fullscreen\s*=\s*1', 'fullscreen = 0' -replace 'width\s*=\s*\d+', 'width = 960' -replace 'height\s*=\s*\d+', 'height = 720' | Set-Content 'data\mugen.cfg'"
)

echo.
echo [3/5] Arrêt des scripts IA en arrière-plan...
tasklist | find /i "python" >nul 2>&1
if %errorlevel% equ 0 (
    echo [CLEANUP] Arrêt des processus Python en cours...
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq AI*" >nul 2>&1
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq IA*" >nul 2>&1
    timeout /t 1 /nobreak >nul
    echo [OK] Scripts IA arrêtés
) else (
    echo [OK] Aucun script IA en cours
)

echo.
echo [4/5] Vérification du jeu...
if not exist "KOF_Ultimate_Online.exe" (
    echo [ERROR] KOF_Ultimate_Online.exe introuvable!
    echo [INFO] Essai avec Ikemen_GO...
    if exist "Ikemen_GO\Ikemen_GO.exe" (
        cd Ikemen_GO
        echo [OK] Ikemen_GO trouvé
    ) else (
        echo [FATAL] Aucun exécutable de jeu trouvé!
        pause
        exit /b 1
    )
)

echo.
echo [5/5] Lancement du jeu en mode mini-fenêtre...
echo.
echo ===============================================
echo    PARAMETRES MINI-FENÊTRE
echo ===============================================
echo    Taille: 960x720 pixels (fenêtré)
echo    Ratio: 4:3 (optimal pour fighting game)
echo    VSync: Désactivé (réactivité maximale)
echo    Mode: Fenêtré (non plein écran)
echo ===============================================
echo.
echo [INFO] Le jeu va se lancer dans 2 secondes...
echo [INFO] Vous pouvez bouger/redimensionner la fenêtre!
echo.
timeout /t 2 /nobreak >nul

REM Lancer le jeu
if exist "KOF_Ultimate_Online.exe" (
    start "" "KOF_Ultimate_Online.exe"
) else (
    start "" "Ikemen_GO.exe"
)

echo.
echo [SUCCESS] Jeu lancé en mode mini-fenêtre!
echo.
echo ===============================================
echo    CONTRÔLES OPTIMISÉS
echo ===============================================
echo    JOUEUR 1 (Clavier):
echo      Déplacement: Flèches directionnelles
echo      Attaques: A, S, D (léger/moyen/fort)
echo      Sauts spéciaux: F, G, H
echo      Start: Entrée
echo.
echo    JOUEUR 1 (Manette):
echo      Stick analogique / D-Pad
echo      Boutons selon config manette
echo.
echo ===============================================
echo    ASTUCES JOUABILITÉ
echo ===============================================
echo    1. La fenêtre est redimensionnable!
echo    2. Mode fenêtré = ALT+TAB possible
echo    3. Pour restaurer plein écran:
echo       - Lancer restore_original_config.bat
echo       - Ou copier mugen.cfg.fullscreen_backup
echo.
echo    4. Si le jeu lag:
echo       - Fermer programmes en arrière-plan
echo       - Désactiver VSync (déjà fait)
echo       - Baisser résolution dans mugen.cfg
echo.
echo ===============================================

REM Créer un fichier de restauration si besoin
if not exist "RESTORE_FULLSCREEN.bat" (
    echo @echo off > RESTORE_FULLSCREEN.bat
    echo echo Restauration du mode plein écran... >> RESTORE_FULLSCREEN.bat
    echo copy /Y "data\mugen.cfg.fullscreen_backup" "data\mugen.cfg" >> RESTORE_FULLSCREEN.bat
    echo echo Mode plein écran restauré! >> RESTORE_FULLSCREEN.bat
    echo pause >> RESTORE_FULLSCREEN.bat
)

echo [INFO] Fichier de restauration créé: RESTORE_FULLSCREEN.bat
echo.
echo Appuyez sur une touche pour fermer ce launcher...
pause >nul
