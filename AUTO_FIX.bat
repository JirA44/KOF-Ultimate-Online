@echo off
chcp 65001 > nul
echo ====================================
echo  KOF ULTIMATE - AUTO-FIX
echo ====================================
echo.

echo 1. Nettoyage des logs...
if exist "D:\KOF Ultimate\mugen.log" del "D:\KOF Ultimate\mugen.log"
echo    ✓ Logs nettoyés

echo.
echo 2. Vérification des fichiers...
python "D:\KOF Ultimate\complete_diagnostic.py"

echo.
echo 3. Lancement du jeu...
cd /d "D:\KOF Ultimate"
start "" "KOF BLACK R.exe"

echo.
echo ✓ Jeu lancé!
pause
