@echo off
chcp 65001 >nul
title KOF Ultimate - Lancement Sécurisé
cls

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🎮 KOF ULTIMATE - LANCEUR INTELLIGENT                      ║
echo ║     Vérifie et répare automatiquement avant de lancer       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo [1/3] Vérification de l'installation...
python IKEMEN_CHECKER.py >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo ✅ Installation OK - Lancement du jeu...
    echo.
    timeout /t 2 /nobreak >nul
    start "" "KOF_Ultimate_Online.exe"
    exit /b 0
) else (
    echo.
    echo ⚠️  Problèmes détectés dans l'installation
    echo.
    echo [2/3] Reconstruction automatique en cours...
    python REBUILD_SELECT.py --yes

    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ✅ Réparation réussie!
        echo.
        echo [3/3] Vérification finale...
        python IKEMEN_CHECKER.py >nul 2>&1

        if %ERRORLEVEL% EQU 0 (
            echo ✅ Tout est OK - Lancement du jeu...
            echo.
            timeout /t 2 /nobreak >nul
            start "" "KOF_Ultimate_Online.exe"
            exit /b 0
        ) else (
            echo ❌ Échec de la vérification finale
            echo.
            echo Appuyez sur une touche pour voir les détails...
            pause >nul
            python IKEMEN_CHECKER.py
            pause
            exit /b 1
        )
    ) else (
        echo ❌ Échec de la réparation
        echo.
        pause
        exit /b 1
    )
)
