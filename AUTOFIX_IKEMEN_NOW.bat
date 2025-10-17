@echo off
chcp 65001 >nul
title AUTO-DIAGNOSTIC ET CORRECTION IKEMEN GO

cls
echo.
echo ============================================================
echo   AUTO-FIX IKEMEN GO
echo ============================================================
echo.

cd /d "D:\KOF Ultimate Online\Ikemen_GO"

echo 1. Suppression anciens dossiers vides...
rd /S /Q data 2>nul
rd /S /Q font 2>nul
rd /S /Q chars 2>nul
rd /S /Q stages 2>nul
rd /S /Q sound 2>nul
echo    Done.

echo.
echo 2. Création liens symboliques...

mklink /J data "..\data"
if %errorlevel%==0 (echo    [OK] data) else (echo    [FAIL] data)

mklink /J font "..\font"
if %errorlevel%==0 (echo    [OK] font) else (echo    [FAIL] font)

mklink /J chars "..\chars"
if %errorlevel%==0 (echo    [OK] chars) else (echo    [FAIL] chars)

mklink /J stages "..\stages"
if %errorlevel%==0 (echo    [OK] stages) else (echo    [FAIL] stages)

mklink /J sound "..\sound"
if %errorlevel%==0 (echo    [OK] sound) else (echo    [FAIL] sound)

echo.
echo 3. Vérification system.def...
if exist "data\system.def" (
    echo    [OK] system.def trouvé
) else (
    echo    [ERREUR] system.def MANQUANT
)

echo.
echo 4. Suppression ancien log...
del Ikemen.log 2>nul

echo.
echo ============================================================
echo   CORRECTION TERMINÉE!
echo ============================================================
echo.
echo Ikemen GO est maintenant configuré.
echo.
pause
