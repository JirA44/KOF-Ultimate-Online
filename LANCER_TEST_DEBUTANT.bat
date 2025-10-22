@echo off
title KOF Ultimate - Test Joueur Débutant

echo.
echo ════════════════════════════════════════════════════════════
echo   🎮 TEST JOUEUR DÉBUTANT - KOF ULTIMATE
echo ════════════════════════════════════════════════════════════
echo.
echo Ce test simule un joueur débutant qui découvre le jeu :
echo   • Navigation dans les menus
echo   • Test du mode en ligne
echo   • Essai de différents modes
echo   • Exploration complète
echo.
echo ⚠️  DEUX OPTIONS DISPONIBLES :
echo.
echo   [1] Test Automatique (Simulation IA - 20 min)
echo       → Le jeu se lance et teste automatiquement
echo       → Ne touchez pas au clavier pendant le test
echo.
echo   [2] Test Manuel (Guide étape par étape)
echo       → Vous testez manuellement avec un guide
echo       → Checklist complète fournie
echo.
echo ════════════════════════════════════════════════════════════
echo.

choice /C 12 /N /M "Choisissez [1] Auto ou [2] Manuel : "

if errorlevel 2 goto MANUEL
if errorlevel 1 goto AUTO

:AUTO
echo.
echo Lancement du test automatique...
echo.
python TEST_JOUEUR_DEBUTANT.py
goto END

:MANUEL
echo.
echo Ouverture du guide de test manuel...
echo.
start "" "GUIDE_TEST_DEBUTANT.md"
echo.
echo ✓ Guide ouvert!
echo.
echo Suivez les étapes du guide et cochez chaque élément.
echo Lancez le jeu avec : KOF_Ultimate_Online.exe
echo.
pause
goto END

:END
exit
