@echo off
chcp 65001 >nul 2>&1
title KOF ULTIMATE ONLINE
color 0B

cls
echo.
echo     ╔══════════════════════════════════════════════════════════╗
echo     ║                                                          ║
echo     ║            🎮 KOF ULTIMATE ONLINE 🎮                    ║
echo     ║                                                          ║
echo     ║                  Version 2.0 Enhanced                    ║
echo     ║                                                          ║
echo     ╚══════════════════════════════════════════════════════════╝
echo.
echo.
echo         ► 188 Personnages
echo         ► 31 Stages
echo         ► Multijoueur En Ligne
echo         ► Auto-Réparation
echo.
echo.
echo     ⏳ Lancement du jeu...
echo.

REM Nettoyer les anciens logs
if exist mugen.log del mugen.log >nul 2>&1

REM Lancer le jeu
start "" "KOF BLACK R.exe"

echo     ✓ Jeu lancé!
echo.
echo     Appuyez sur une touche pour fermer cette fenêtre...
pause >nul
