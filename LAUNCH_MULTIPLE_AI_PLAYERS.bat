@echo off
REM =========================================
REM   LANCEUR MULTI-IA SIMULTANÉES
REM   Plusieurs IA jouent en même temps
REM   dans différents modes !
REM =========================================

title KOF - Multiple IA Multi-Modes

echo.
echo ====================================
echo   🤖🤖🤖 MULTI-IA SIMULTANÉES
echo ====================================
echo.
echo Ce launcher démarre plusieurs IA
echo qui jouent simultanément dans
echo différents modes de jeu !
echo.
echo Combien d'IA voulez-vous lancer ?
echo.
set /p NUM_AI="Nombre d'IA (1-5): "

if "%NUM_AI%"=="" set NUM_AI=1

echo.
echo Lancement de %NUM_AI% IA...
echo.

for /L %%i in (1,1,%NUM_AI%) do (
    echo 🤖 Lancement IA #%%i...
    start /MIN "IA Multi-Modes %%i" python "AI_MULTI_MODE_SYSTEM.py"
    timeout /t 5 /nobreak > nul
)

echo.
echo ====================================
echo   ✅ %NUM_AI% IA LANCÉES !
echo ====================================
echo.
echo 📂 Logs: D:\KOF Ultimate Online\logs\
echo 📸 Screenshots: D:\KOF Ultimate Online\ai_screenshots_*\
echo.
echo Les IA jouent maintenant en arrière-plan
echo dans tous les modes de jeu disponibles !
echo.
echo Pour arrêter les IA, fermez les fenêtres
echo Python minimisées dans la barre des tâches.
echo.
echo Appuyez sur une touche pour fermer...
pause > nul
