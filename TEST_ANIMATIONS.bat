@echo off
echo ============================================================
echo    KOF ULTIMATE ONLINE - TEST DES ANIMATIONS
echo ============================================================
echo.
echo Les animations sont configurees dans:
echo   - Menu principal: system.def [TitleBG 1] et [TitleBG 2]
echo   - Menu select: system.def [SelectBG 0] et [SelectBG 1]
echo.
echo Actions animees actives:
echo   - Action 4: Animation menu titre (fade in/out)
echo   - Action 5: Animation titre (glow/pulse)
echo   - Action 7: Animation select screen (base)
echo   - Action 8: Animation select screen (effets)
echo   - Action 495: Animation flames
echo   - Action 496: Animation flash
echo   - Action 497: Animation characters
echo.
echo ============================================================
echo.
echo Lancement du jeu pour verification visuelle...
echo.
pause

cd "D:\KOF Ultimate Online"
start "" "KOF_Ultimate_Online.exe"

echo.
echo Verifiez visuellement:
echo   1. Menu principal - Y a-t-il des effets animes?
echo   2. Ecran de selection - Y a-t-il des animations?
echo   3. Backgrounds animees/particules?
echo.
pause
