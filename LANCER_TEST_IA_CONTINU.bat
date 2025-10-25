@echo off
chcp 65001 >nul
cls

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║      🤖  TEST AUTOMATIQUE IA vs IA - MODE CONTINU             ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo   Ce script va lancer des combats IA vs IA automatiquement
echo   pour tester tous les personnages sans vous déranger.
echo.
echo   Les IAs vont combattre toutes seules, je log juste les résultats.
echo.
echo ══════════════════════════════════════════════════════════════════
echo   FONCTIONNEMENT:
echo ══════════════════════════════════════════════════════════════════
echo.
echo   • Sélection aléatoire de 2 personnages
echo   • Combat IA vs IA (60s max)
echo   • Détection automatique des crashes
echo   • Identification des personnages problématiques
echo   • Rapport en temps réel
echo.
echo   📊 Résultats: test_ia_results.json
echo   📋 Logs: auto_test_ia_vs_ia.log
echo.
echo ══════════════════════════════════════════════════════════════════
echo.
pause

cd /d "%~dp0"
python AUTO_TEST_IA_VS_IA.py

echo.
echo ✅ Test terminé!
echo.
echo Consultez:
echo   • test_ia_results.json (résultats détaillés)
echo   • auto_test_ia_vs_ia.log (log complet)
echo.
pause
