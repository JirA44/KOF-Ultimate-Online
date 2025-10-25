@echo off
title Test de la Manette
color 0A
cls

echo.
echo ================================================================
echo                  TEST DE LA MANETTE
echo ================================================================
echo.

cd /d "D:\KOF Ultimate"

echo [1/3] Detection de la manette...
python -c "import pygame; pygame.init(); pygame.joystick.init(); c = pygame.joystick.get_count(); print(f'\n  Manettes trouvees: {c}'); [print(f'  - {pygame.joystick.Joystick(i).get_name()}') for i in range(c)] if c > 0 else print('  AUCUNE manette branchee !'); pygame.quit()"

echo.
echo [2/3] Configuration automatique...
python gamepad_auto_config.py

echo.
echo [3/3] Test de navigation...
echo.
echo ================================================================
echo   INSTRUCTIONS DE TEST:
echo ================================================================
echo.
echo   1. Lancez maintenant le jeu
echo   2. Dans les menus, essayez:
echo      - D-Pad / Stick gauche pour naviguer
echo      - Bouton A (Xbox) pour valider
echo      - Bouton Start pour pause
echo.
echo   Si ca ne fonctionne pas, appuyez sur une touche maintenant
echo   et je vais reessayer avec une configuration differente.
echo.
echo ================================================================
pause

echo.
echo Voulez-vous lancer le jeu maintenant? (O/N)
choice /C ON /N /M "Appuyez sur O pour OUI ou N pour NON: "

if errorlevel 2 goto :end
if errorlevel 1 goto :launch

:launch
echo.
echo Lancement du jeu...
start "" "KOF BLACK R.exe"
goto :end

:end
echo.
echo Termine !
timeout /t 3 /nobreak >nul
