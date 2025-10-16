@echo off
echo ====================================
echo Creation des raccourcis KOF Ultimate
echo ====================================
echo.

REM Copier l'exe dans le dossier principal
echo Copie de l'executable...
copy "D:\KOF Ultimate\dist\KOF Ultimate Launcher.exe" "D:\KOF Ultimate\KOF Ultimate Launcher.exe"
if errorlevel 1 (
    echo ERREUR: Impossible de copier l'executable
) else (
    echo OK: Executable copie dans le dossier principal
)
echo.

REM Creer un raccourci sur le bureau
echo Creation du raccourci sur le bureau...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\KOF Ultimate.lnk'); $Shortcut.TargetPath = 'D:\KOF Ultimate\dist\KOF Ultimate Launcher.exe'; $Shortcut.WorkingDirectory = 'D:\KOF Ultimate'; $Shortcut.Save()" 2>nul
if errorlevel 1 (
    echo INFO: Raccourci bureau non cree
) else (
    echo OK: Raccourci cree sur le bureau
)
echo.

echo ====================================
echo Terminé!
echo ====================================
echo.
echo L'executable se trouve maintenant:
echo 1. Dans: D:\KOF Ultimate\KOF Ultimate Launcher.exe
echo 2. Dans: D:\KOF Ultimate\dist\KOF Ultimate Launcher.exe
echo 3. Sur le bureau: KOF Ultimate.lnk
echo.
pause
