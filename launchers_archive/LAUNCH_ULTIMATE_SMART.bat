@echo off
chcp 65001 >nul
cd /d "D:\KOF Ultimate Online"
cls
echo.
echo ================================================================================
echo                    KOF ULTIMATE ONLINE - SMART LAUNCHER
echo ================================================================================
echo.
echo [1/3] Nettoyage des processus IA...
taskkill /F /IM python.exe /T >nul 2>&1
echo ✓ Scripts IA arrêtés
echo.
echo [2/3] Auto-diagnostic et auto-correction...
python launcher_auto_diagnostic.py --autolaunch 2>nul
if errorlevel 1 (
    echo ⚠️  Auto-diagnostic désactivé, lancement direct...
)
echo.
echo [3/3] Lancement du jeu...
echo.
timeout /t 2 >nul

REM Vérifier quel exécutable existe
if exist "KOF_Ultimate_Online.exe" (
    start "" "KOF_Ultimate_Online.exe"
    echo ✓ M.U.G.E.N lancé avec succès!
) else if exist "Ikemen_GO\Ikemen_GO.exe" (
    cd Ikemen_GO
    start "" "Ikemen_GO.exe"
    echo ✓ Ikemen GO lancé avec succès!
) else (
    echo ❌ Aucun exécutable trouvé!
    echo.
    echo Fichiers recherchés:
    echo   - KOF_Ultimate_Online.exe
    echo   - Ikemen_GO\Ikemen_GO.exe
    echo.
    pause
    exit /b 1
)

echo.
echo Appuyez sur une touche pour fermer cette fenêtre...
pause >nul
