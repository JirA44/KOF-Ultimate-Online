@echo off
chcp 65001 > nul
title Créer Raccourci Bureau

cls
echo.
echo ============================================================
echo   🎮 CRÉATION DE RACCOURCI SUR LE BUREAU
echo ============================================================
echo.
echo Ce script va créer un raccourci "KOF ULTIMATE" sur
echo votre bureau pour lancer facilement le jeu.
echo.
pause

REM Créer le raccourci avec PowerShell
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\KOF ULTIMATE.lnk'); $Shortcut.TargetPath = 'D:\KOF Ultimate\START_KOF_ULTIMATE.bat'; $Shortcut.WorkingDirectory = 'D:\KOF Ultimate'; $Shortcut.Description = 'KOF Ultimate - Menu Principal'; $Shortcut.Save()"

echo.
echo ✓ Raccourci créé sur le bureau!
echo.
echo Vous pouvez maintenant lancer le jeu en double-cliquant
echo sur l'icône "KOF ULTIMATE" sur votre bureau.
echo.
pause
