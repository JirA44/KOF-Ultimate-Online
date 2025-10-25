@echo off
chcp 65001 >nul
title TEST RAPIDE - Un Joueur

cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  ⚡ TEST RAPIDE - UN JOUEUR                                  ║
echo ║     Diagnostic UX en 2 minutes                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo  Ce test va:
echo  ✓ Lancer le jeu
echo  ✓ Parcourir les menus
echo  ✓ Jouer un match de 30s
echo  ✓ Tester pause/sortie
echo  ✓ Générer un rapport
echo.
echo  ⏱️  Durée: ~2 minutes
echo  ⚠️  NE PAS toucher souris/clavier!
echo.
pause

python TEST_RAPIDE_UN_JOUEUR.py

pause
