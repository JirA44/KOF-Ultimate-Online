@echo off
chcp 65001 > nul
title KOF ULTIMATE - Système Complet
color 0A
cls

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║         KOF ULTIMATE ONLINE - SYSTÈME COMPLET                ║
echo ║                                                                ║
echo ║              Auto-Détection + Auto-Correction                 ║
echo ║                  + Tests + Diagnostics                         ║
echo ║                                                                ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo.
echo  ╔═══════════════════════════════════════════════════════════╗
echo  ║               QUE VOULEZ-VOUS FAIRE ?                    ║
echo  ╠═══════════════════════════════════════════════════════════╣
echo  ║                                                            ║
echo  ║  1. 🔍 Auto-Détection et Correction d'Erreurs            ║
echo  ║     → Scanne et corrige TOUT automatiquement             ║
echo  ║                                                            ║
echo  ║  2. 🧪 Tester Tous les Launchers                         ║
echo  ║     → Vérifie que tous les launchers fonctionnent        ║
echo  ║                                                            ║
echo  ║  3. 🚨 Correction d'Urgence (Chemins Dupliqués)          ║
echo  ║     → Si problème de chemins répétés                     ║
echo  ║                                                            ║
echo  ║  4. 🎨 Corrections Visuelles (Graphismes)                ║
echo  ║     → Améliore couleurs, animations, grille chars        ║
echo  ║                                                            ║
echo  ║  5. 📊 Rapport Complet                                    ║
echo  ║     → Affiche rapport auto-correcteur                    ║
echo  ║                                                            ║
echo  ║  6. 🎮 Lancer le Jeu (Launcher Ultimate)                 ║
echo  ║     → Lance le launcher principal                        ║
echo  ║                                                            ║
echo  ║  7. 🔬 Visual Inspector                                   ║
echo  ║     → Interface pour tester visuellement                 ║
echo  ║                                                            ║
echo  ║  8. 👤 Character Dashboard                               ║
echo  ║     → Voir tous les personnages et leurs coups           ║
echo  ║                                                            ║
echo  ║  9. 🚀 Lancer TOUT (Détection + Tests + Jeu)             ║
echo  ║     → Pipeline complet automatique                       ║
echo  ║                                                            ║
echo  ║  0. ❌ Quitter                                            ║
echo  ║                                                            ║
echo  ╚═══════════════════════════════════════════════════════════╝
echo.
set /p choice="  Votre choix (0-9): "
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

if "%choice%"=="1" goto auto_detect
if "%choice%"=="2" goto test_launchers
if "%choice%"=="3" goto emergency_fix
if "%choice%"=="4" goto visual_fixes
if "%choice%"=="5" goto show_report
if "%choice%"=="6" goto launch_game
if "%choice%"=="7" goto visual_inspector
if "%choice%"=="8" goto char_dashboard
if "%choice%"=="9" goto run_all
if "%choice%"=="0" goto quit

echo ❌ Choix invalide!
timeout /t 2 > nul
goto :eof

:auto_detect
echo 🔍 LANCEMENT AUTO-DÉTECTEUR...
echo.
python AUTO_DETECT_FIX_ALL_ERRORS.py
echo.
echo ═══════════════════════════════════════════════════════════════
pause
goto :eof

:test_launchers
echo 🧪 TEST DE TOUS LES LAUNCHERS...
echo.
python test_all_launchers.py
echo.
echo ═══════════════════════════════════════════════════════════════
echo   Résultats: launcher_test_results.txt
pause
goto :eof

:emergency_fix
echo 🚨 CORRECTION D'URGENCE CHEMINS DUPLIQUÉS...
echo.
python FIX_DUPLICATE_PATHS_EMERGENCY.py
echo.
echo ═══════════════════════════════════════════════════════════════
pause
goto :eof

:visual_fixes
echo 🎨 CORRECTIONS VISUELLES...
echo.
python fix_all_visual.py
echo.
python fix_cursor_animations.py
echo.
echo ═══════════════════════════════════════════════════════════════
pause
goto :eof

:show_report
echo 📊 AFFICHAGE RAPPORT COMPLET...
echo.
if exist "RAPPORT_AUTO_CORRECTEUR.md" (
    start RAPPORT_AUTO_CORRECTEUR.md
    echo ✓ Rapport ouvert dans votre éditeur par défaut
) else (
    echo ❌ Rapport introuvable!
    echo    Lancez d'abord l'auto-détecteur (option 1^)
)
echo.
pause
goto :eof

:launch_game
echo 🎮 LANCEMENT DU JEU...
echo.
python LAUNCHER_ULTIMATE_V2.py
goto :eof

:visual_inspector
echo 🔬 LANCEMENT VISUAL INSPECTOR...
echo.
python visual_inspector.py
goto :eof

:char_dashboard
echo 👤 LANCEMENT CHARACTER DASHBOARD...
echo.
python character_dashboard.py
goto :eof

:run_all
echo 🚀 PIPELINE COMPLET - LANCEMENT...
echo.
echo [1/3] Auto-Détection et Correction...
python AUTO_DETECT_FIX_ALL_ERRORS.py
echo.
echo ═══════════════════════════════════════════════════════════════
echo [2/3] Tests des Launchers...
python test_all_launchers.py
echo.
echo ═══════════════════════════════════════════════════════════════
echo [3/3] Lancement du Jeu...
echo.
pause
python LAUNCHER_ULTIMATE_V2.py
goto :eof

:quit
echo.
echo ══════════════════════════════════════════════════════════════
echo   Au revoir! 👋
echo ══════════════════════════════════════════════════════════════
echo.
timeout /t 2 > nul
exit

