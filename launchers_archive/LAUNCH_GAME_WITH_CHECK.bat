@echo off
title KOF Ultimate - Lancement avec Vérification
color 0A
cls

echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║   KOF ULTIMATE - LANCEMENT AVEC AUTO-CHECK           ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

REM Lancer l'autocheck d'abord
echo 🔍 Vérification du système...
echo.
python AUTOCHECK_SYSTEM.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Système vérifié - Prêt à lancer!
    echo.
    echo 🎮 Lancement du jeu dans 3 secondes...
    timeout /t 3 /nobreak > nul
    
    REM Lancer le jeu
    start "" "KOF_Ultimate_Online.exe"
    
    echo.
    echo ✅ Jeu lancé!
    echo.
) else (
    echo.
    echo ⚠️  Des problèmes ont été détectés.
    echo    Voulez-vous quand même lancer le jeu?
    echo.
    choice /C ON /M "Lancer le jeu"
    
    if %ERRORLEVEL% EQU 1 (
        start "" "KOF_Ultimate_Online.exe"
        echo ✅ Jeu lancé malgré les avertissements.
    ) else (
        echo ❌ Lancement annulé.
    )
)

echo.
pause
