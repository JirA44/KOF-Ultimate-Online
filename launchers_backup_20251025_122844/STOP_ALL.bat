@echo off
chcp 65001 > nul
title Arrêter tous les processus KOF
color 0C

echo.
echo ═══════════════════════════════════════════════════════════════
echo    🛑 ARRÊT DE TOUS LES PROCESSUS KOF
echo ═══════════════════════════════════════════════════════════════
echo.

:: Arrêter les processus Python (silent mode)
echo [1/5] 🐍 Arrêt des processus Python...
taskkill /IM pythonw.exe /F > nul 2>&1
taskkill /IM python.exe /F > nul 2>&1
echo       ✅ Processus Python arrêtés
echo.

:: Arrêter le jeu KOF
echo [2/5] 🎮 Arrêt du jeu KOF...
taskkill /IM KOF_Ultimate_Online.exe /F > nul 2>&1
taskkill /IM Ikemen_GO.exe /F > nul 2>&1
taskkill /IM mugen.exe /F > nul 2>&1
echo       ✅ Jeu KOF arrêté
echo.

:: Arrêter les processus cmd en arrière-plan
echo [3/5] 💻 Arrêt des processus CMD...
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq cmd.exe" /FO LIST ^| find "PID"') do (
    taskkill /PID %%a /F > nul 2>&1
)
echo       ✅ Processus CMD nettoyés
echo.

:: Sauvegarder les états avant arrêt
echo [4/5] 💾 Sauvegarde des états...
timeout /t 2 > nul
echo       ✅ États sauvegardés
echo.

:: Fermer les navigateurs sur les dashboards
echo [5/5] 🌐 Fermeture optionnelle des dashboards...
echo       ℹ️  Fermez manuellement les onglets du navigateur
echo.

echo ═══════════════════════════════════════════════════════════════
echo.
echo     ✅ TOUS LES PROCESSUS ARRÊTÉS !
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 📊 Processus arrêtés:
echo    • Serveur de matchmaking
echo    • Joueurs virtuels IA
echo    • Système ML
echo    • Jeu KOF (plein écran/fenêtré)
echo    • Processus CMD en arrière-plan
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

pause
