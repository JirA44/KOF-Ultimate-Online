@echo off
chcp 65001 > nul
title KOF ULTIMATE - Auto Test Infini
color 0C
cls

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║         KOF ULTIMATE - AUTO TEST INFINI                      ║
echo ║                                                                ║
echo ║  Ce système va:                                               ║
echo ║  • Lancer le jeu EN BOUCLE                                   ║
echo ║  • Cliquer PARTOUT automatiquement                           ║
echo ║  • Tester des persos aléatoires                              ║
echo ║  • Logger TOUTES les erreurs détectées                       ║
echo ║  • Recommencer à l'infini jusqu'à Ctrl+C                    ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo.

echo [PRÉPARATION] Nettoyage des anciens logs...
if exist "errors_auto_detected.txt" del /q "errors_auto_detected.txt"
echo   ✓ Logs nettoyés
echo.

echo [LANCEMENT] Démarrage de l'auto-testeur infini...
echo.
echo   ⚠️  ATTENTION:
echo     • Le jeu va se lancer et fermer en boucle
echo     • Les IAs vont cliquer automatiquement partout
echo     • Toutes les erreurs seront loggées
echo     • Appuyez sur Ctrl+C pour arrêter
echo.
echo   📄 Log en direct: errors_auto_detected.txt
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause
echo.

python auto_test_infinite.py

echo.
echo ═══════════════════════════════════════════════════════════════
echo   Tests arrêtés
echo ═══════════════════════════════════════════════════════════════
echo.
echo   Consultez: errors_auto_detected.txt
echo.
pause
