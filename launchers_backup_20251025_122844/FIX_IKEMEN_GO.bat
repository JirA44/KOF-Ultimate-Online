@echo off
chcp 65001 > nul
title Réparation Ikemen GO - KOF Ultimate

cls
echo.
echo ============================================================
echo   🔧 RÉPARATION IKEMEN GO
echo ============================================================
echo.
echo Ce script va:
echo   1. Vérifier l'installation d'Ikemen GO
echo   2. Créer les dossiers manquants
echo   3. Créer des liens vers les dossiers M.U.G.E.N
echo.
pause

REM Vérifier si Ikemen_GO existe
if not exist "D:\KOF Ultimate Online\Ikemen_GO\Ikemen_GO.exe" (
    echo.
    echo ❌ ERREUR: Ikemen GO n'est pas installé!
    echo.
    echo Pour installer Ikemen GO:
    echo   1. Téléchargez depuis: https://github.com/ikemen-engine/Ikemen-GO/releases/latest
    echo   2. Téléchargez: Ikemen_GO_Win.zip
    echo   3. Extrayez dans: D:\KOF Ultimate Online\Ikemen_GO\
    echo.
    echo Ou utilisez: install_ikemen_go.bat
    echo.
    pause
    exit /b 1
)

echo.
echo ✓ Ikemen GO trouvé!
echo.

REM Créer les dossiers s'ils n'existent pas
echo 📁 Création des dossiers dans Ikemen_GO...
echo.

cd /d "D:\KOF Ultimate Online\Ikemen_GO"

REM Supprimer les anciens liens/dossiers s'ils existent
if exist "data" rd /S /Q "data" 2>nul
if exist "font" rd /S /Q "font" 2>nul
if exist "chars" rd /S /Q "chars" 2>nul
if exist "stages" rd /S /Q "stages" 2>nul
if exist "sound" rd /S /Q "sound" 2>nul

REM Créer des liens symboliques (junctions) vers les dossiers M.U.G.E.N
echo ⚡ Création des liens symboliques...
echo.

mklink /J "data" "..\data"
if %errorlevel%==0 (
    echo   ✓ data linked
) else (
    echo   ⚠️  data link failed, copying instead...
    xcopy /E /I /Y "..\data" "data" >nul
)

mklink /J "font" "..\font"
if %errorlevel%==0 (
    echo   ✓ font linked
) else (
    echo   ⚠️  font link failed, copying instead...
    xcopy /E /I /Y "..\font" "font" >nul
)

mklink /J "chars" "..\chars"
if %errorlevel%==0 (
    echo   ✓ chars linked
) else (
    echo   ⚠️  chars link failed, copying instead...
    xcopy /E /I /Y "..\chars" "chars" >nul
)

mklink /J "stages" "..\stages"
if %errorlevel%==0 (
    echo   ✓ stages linked
) else (
    echo   ⚠️  stages link failed, copying instead...
    xcopy /E /I /Y "..\stages" "stages" >nul
)

mklink /J "sound" "..\sound"
if %errorlevel%==0 (
    echo   ✓ sound linked
) else (
    echo   ⚠️  sound link failed, copying instead...
    xcopy /E /I /Y "..\sound" "sound" >nul
)

echo.
echo ============================================================
echo   ✓ RÉPARATION TERMINÉE!
echo ============================================================
echo.
echo Ikemen GO devrait maintenant fonctionner correctement.
echo.
echo Pour tester: Double-clic sur Ikemen_GO.exe
echo.
pause
