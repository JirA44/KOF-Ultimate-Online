@echo off
chcp 65001 >nul
title Progression Test Exhaustif
cls

echo.
echo ══════════════════════════════════════════════════════════════
echo   📊 PROGRESSION DU TEST EXHAUSTIF
echo ══════════════════════════════════════════════════════════════
echo.

if exist "characters_test_report.txt" (
    echo ✅ Rapport trouvé!
    echo.
    findstr /C:"Total testés" /C:"✓ OK:" /C:"✗ ÉCHOUÉS:" /C:"⊘ IGNORÉS:" characters_test_report.txt
    echo.
    echo ══════════════════════════════════════════════════════════════
    echo   TEST TERMINÉ! Consultez characters_test_report.txt
    echo ══════════════════════════════════════════════════════════════
) else (
    echo ⏳ Test en cours...
    echo.
    echo Le rapport sera généré à la fin (~15 minutes au total)
    echo.

    REM Vérifier si le jeu tourne
    tasklist /FI "IMAGENAME eq KOF_Ultimate_Online.exe" /NH 2>nul | find /I "KOF_Ultimate_Online.exe" >nul
    if %ERRORLEVEL%==0 (
        echo ✅ Jeu actuellement lancé - Test en cours
    ) else (
        echo ⚠️  Jeu non actif actuellement
    )

    echo.
    echo Dernière modification de mugen.log:
    dir mugen.log 2>nul | find "mugen.log"
)

echo.
pause
