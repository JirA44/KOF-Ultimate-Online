@echo off
chcp 65001 >nul
cls
echo.
echo ================================================================================
echo                    KOF ULTIMATE ONLINE - SMART LAUNCHER
echo ================================================================================
echo.
echo [1/3] Vérification et auto-réparation du système...
python auto_repair_system.py
echo.
echo [2/3] Tests automatisés...
python auto_test_system.py
echo.
echo [3/3] Lancement du jeu...
echo.
timeout /t 2 >nul
start "" "KOF BLACK R.exe"
echo.
echo ✓ Jeu lancé avec succès!
echo.
echo Appuyez sur une touche pour fermer cette fenêtre...
pause >nul
