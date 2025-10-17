@echo off
chcp 65001 > nul
title KOF ULTIMATE - Auto-Détecteur d'Erreurs
color 0B
cls

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║    KOF ULTIMATE - AUTO-DÉTECTEUR ET CORRECTEUR UNIVERSEL    ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo  Ce système va automatiquement:
echo.
echo  ✓ Scanner TOUS les fichiers Python
echo  ✓ Détecter TOUTES les erreurs
echo  ✓ Corriger automatiquement ce qui peut l'être
echo  ✓ Vérifier la configuration MUGEN
echo  ✓ Vérifier les packages Python
echo  ✓ Générer un rapport complet
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause
echo.

python AUTO_DETECT_FIX_ALL_ERRORS.py

echo.
echo ═══════════════════════════════════════════════════════════════
echo  Détection et correction terminées
echo ═══════════════════════════════════════════════════════════════
echo.
echo  📄 Consultez: AUTO_FIX_REPORT.txt
echo.
pause
