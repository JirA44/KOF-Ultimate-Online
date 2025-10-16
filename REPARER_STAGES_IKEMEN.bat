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

REM Copier tous les fichiers .def et .sff des stages
xcopy "D:\KOF Ultimate\stages\*.def" "D:\KOF Ultimate\Ikemen_GO\stages\" /Y /I
xcopy "D:\KOF Ultimate\stages\*.sff" "D:\KOF Ultimate\Ikemen_GO\stages\" /Y /I
xcopy "D:\KOF Ultimate\stages\*.mp3" "D:\KOF Ultimate\Ikemen_GO\stages\" /Y /I
xcopy "D:\KOF Ultimate\stages\*.ogg" "D:\KOF Ultimate\Ikemen_GO\stages\" /Y /I

echo.
echo ✓ Stages copiés!
echo.

REM Compter les fichiers
for /f %%A in ('dir /b "D:\KOF Ultimate\Ikemen_GO\stages\*.def" 2^>nul ^| find /c /v ""') do set count=%%A

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
