@echo off
chcp 65001 >nul
title Restaurer Roster Complet

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     🔄 RESTAURER ROSTER COMPLET (26 PERSONNAGES)         ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo ⚠️  ATTENTION: Le roster complet contient des crasheurs!
echo.
echo Roster actuel: 5 persos stables
echo Roster à restaurer: 26 persos (dont ~60%% crashent)
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
choice /C ON /M "Voulez-vous vraiment restaurer le roster complet"

if errorlevel 2 goto cancel
if errorlevel 1 goto restore

:restore
echo.
echo 🔄 Restauration du roster complet...
cd /d "D:\KOF Ultimate Online\data"
copy /Y select.def.backup_before_safe select.def
echo.
echo ✅ Roster complet restauré!
echo.
echo ⚠️  RAPPEL: Crasheurs connus:
echo    - Athena
echo    - boss-orochi
echo    - Viper
echo    - Rose
echo    - akuma
echo    - Final-IGNIZ
echo    - god_orochi
echo.
pause
goto end

:cancel
echo.
echo ❌ Restauration annulée
echo.
pause
goto end

:end
