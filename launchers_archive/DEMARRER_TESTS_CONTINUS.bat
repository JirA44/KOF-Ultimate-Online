@echo off
chcp 65001 >nul
title Tests Continus - KOF Ultimate
cls

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🎮 DÉMARRAGE DES TESTS CONTINUS                            ║
echo ║     Tests automatiques en arrière-plan                      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo ✅ Les tests tournent en arrière-plan
echo ✅ Vous pouvez continuer à travailler normalement
echo ✅ Rapports générés automatiquement dans logs/tests_continus/
echo.
echo Configuration:
echo   - Intervalle: 5 minutes entre chaque test
echo   - Durée d'un test: ~90 secondes
echo   - Logs: D:\KOF Ultimate Online\logs\tests_continus\
echo.
echo Lancement...
echo.

start /MIN "Tests Continus KOF" cmd /c "python test_continu_autonome.py 2>&1 > logs\tests_continus\console.log"

echo.
echo ✅ Tests continus démarrés en arrière-plan !
echo.
echo Pour voir l'état des tests:
echo   - VOIR_RAPPORTS_CONTINUS.bat
echo.
echo Pour arrêter les tests:
echo   - ARRETER_TESTS_CONTINUS.bat
echo.

timeout /t 3
