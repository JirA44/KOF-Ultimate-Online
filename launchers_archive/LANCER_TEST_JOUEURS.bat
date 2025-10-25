@echo off
chcp 65001 >nul
title TEST JOUEURS RÉELS - KOF Ultimate Online

cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🎮 TEST MULTI-JOUEURS AUTOMATIQUE                          ║
echo ║     KOF Ultimate Online                                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo  Ce script va simuler de VRAIS joueurs qui:
echo  ✓ Parcourent les menus
echo  ✓ Jouent des matchs
echo  ✓ Testent toutes les fonctionnalités
echo  ✓ Reportent les bugs et problèmes UX
echo.
echo  ⚠️  IMPORTANT:
echo      - NE TOUCHEZ PAS la souris/clavier pendant les tests
echo      - Durée: ~30-45 minutes
echo      - Le jeu va se lancer automatiquement
echo.
echo ────────────────────────────────────────────────────────────────
echo.

pause

echo.
echo 🚀 Lancement de la simulation...
echo.

python SIMULATEUR_JOUEURS_REELS.py

echo.
echo ════════════════════════════════════════════════════════════════
echo  ✅ SIMULATION TERMINÉE!
echo ════════════════════════════════════════════════════════════════
echo.
echo  📁 Consultez les rapports dans: logs\player_simulation\
echo.
pause
