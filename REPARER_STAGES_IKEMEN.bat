@echo off
chcp 65001 > nul
title Copie des Stages vers Ikemen GO

cls
echo.
echo ============================================================
echo   🏟️  RÉPARATION DES STAGES IKEMEN GO
echo ============================================================
echo.
echo Ce script va copier tous les stages de MUGEN
echo vers Ikemen GO pour corriger l'erreur de crash.
echo.
pause

echo.
echo ⏳ Copie des stages en cours...
echo.

REM Vérifier si Ikemen_GO existe
if not exist "D:\KOF Ultimate Online\Ikemen_GO\" (
    echo.
    echo ❌ ERREUR: Le dossier Ikemen_GO n'existe pas!
    echo.
    echo Ikemen GO n'est pas installé dans ce répertoire.
    echo Veuillez d'abord installer Ikemen GO ou vérifier le chemin.
    echo.
    pause
    exit /b 1
)

REM Copier tous les fichiers .def et .sff des stages
xcopy "D:\KOF Ultimate Online\stages\*.def" "D:\KOF Ultimate Online\Ikemen_GO\stages\" /Y /I
xcopy "D:\KOF Ultimate Online\stages\*.sff" "D:\KOF Ultimate Online\Ikemen_GO\stages\" /Y /I
xcopy "D:\KOF Ultimate Online\stages\*.mp3" "D:\KOF Ultimate Online\Ikemen_GO\stages\" /Y /I
xcopy "D:\KOF Ultimate Online\stages\*.ogg" "D:\KOF Ultimate Online\Ikemen_GO\stages\" /Y /I

echo.
echo ✓ Stages copiés!
echo.

REM Compter les fichiers
for /f %%A in ('dir /b "D:\KOF Ultimate Online\Ikemen_GO\stages\*.def" 2^>nul ^| find /c /v ""') do set count=%%A

echo.
echo ============================================================
echo   ✓ RÉPARATION TERMINÉE!
echo ============================================================
echo.
echo Nombre de stages copiés: %count%
echo.
echo Ikemen GO devrait maintenant fonctionner sans crash!
echo.
pause
