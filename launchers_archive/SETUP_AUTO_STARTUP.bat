@echo off
title KOF Ultimate - Configuration Auto-Startup
color 0B
cls

echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║   KOF ULTIMATE - CONFIGURATION AUTO-STARTUP          ║
echo ╚═══════════════════════════════════════════════════════╝
echo.
echo Ce script va configurer l'auto-lancement des checkers
echo au démarrage de Windows.
echo.
pause

echo.
echo 🔧 Configuration en cours...
echo.

REM Créer un raccourci dans le dossier Startup
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set TARGET_PATH=%CD%\AUTO_LAUNCHER.py
set SHORTCUT_PATH=%STARTUP_FOLDER%\KOF_AutoCheck.lnk

echo Création du raccourci dans le dossier Startup...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = '\"%TARGET_PATH%\"'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Save()"

if exist "%SHORTCUT_PATH%" (
    echo.
    echo ✅ Configuration réussie!
    echo.
    echo Les autocheckers se lanceront automatiquement au démarrage.
    echo.
    echo Emplacement: %SHORTCUT_PATH%
) else (
    echo.
    echo ❌ Erreur lors de la configuration.
    echo.
)

echo.
echo ═══════════════════════════════════════════════════════
pause
