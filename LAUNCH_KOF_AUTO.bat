@echo off
chcp 65001 > nul
title KOF ULTIMATE - Auto Launch
color 0A
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║        KOF ULTIMATE - LANCEMENT AUTOMATIQUE               ║
echo ║                                                            ║
echo ║   Auto-Clicker actif - Pas besoin de clé API!            ║
echo ║   Le jeu va se lancer et naviguer automatiquement         ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo.

echo [1/2] Vérification des dépendances...
python -c "import pyautogui" 2>nul
if errorlevel 1 (
    echo    ⚠ Installation de pyautogui...
    python -m pip install -q pyautogui
    echo    ✓ Installé!
)

python -c "import win32gui" 2>nul
if errorlevel 1 (
    echo    ⚠ Installation de pywin32...
    python -m pip install -q pywin32
    echo    ✓ Installé!
)

echo    ✓ Toutes les dépendances sont présentes
echo.
echo.

echo [2/2] Lancement de l'auto-clicker...
echo.
echo    Le jeu va se lancer dans quelques secondes...
echo    L'auto-clicker va:
echo      • Lancer le jeu
echo      • Passer les écrans de titre
echo      • Naviguer jusqu'au mode Arcade
echo      • Sélectionner un personnage
echo.
echo    VOUS N'AVEZ RIEN À FAIRE!
echo.
echo ════════════════════════════════════════════════════════════
echo.

python auto_clicker_kof.py

echo.
echo ════════════════════════════════════════════════════════════
echo.
echo ✓ Auto-clicker terminé
echo.
pause
