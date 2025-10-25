@echo off
chcp 65001 >nul
title Réparation Rapide

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     🔧 RÉPARATION RAPIDE - god_orochi                     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo Retire god_orochi du roster...

cd /d "D:\KOF Ultimate Online\data"

:: Backup
copy select.def select.def.backup_godorochi >nul

:: Commenter god_orochi dans select.def
powershell -Command "(Get-Content select.def) -replace '^god_orochi,', '; RETIRÉ (Crash): god_orochi,' | Set-Content select.def"

echo   ✓ god_orochi retiré du roster
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     ✅ TERMINÉ - Testez avec d'autres personnages         ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Personnages recommandés (100%% sûrs):
echo   - WhirlWind-Goenitz
echo   - Viper
echo   - Cronus
echo.

pause
