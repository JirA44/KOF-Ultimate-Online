@echo off
REM =========================================
REM   LANCEUR IA MULTI-MODES AUTONOME
REM   Les IA jouent dans tous les modes
REM   sans vous déranger !
REM =========================================

title KOF - IA Multi-Modes Autonome

echo.
echo ====================================
echo   🤖 IA MULTI-MODES AUTONOME
echo ====================================
echo.
echo Les IA vont jouer automatiquement dans:
echo   • Mode Arcade
echo   • Mode Versus
echo   • Mode Team
echo   • Mode Survival
echo   • Time Attack
echo   • Training Mode
echo.
echo Le système tourne en arrière-plan
echo et ne vous dérangera pas.
echo.
echo Appuyez sur Ctrl+C pour arrêter
echo ====================================
echo.

REM Lancer en mode minimisé
start /MIN "IA Multi-Modes 1" python "AI_MULTI_MODE_SYSTEM.py"

echo.
echo ✅ IA Multi-Modes lancée !
echo.
echo 📂 Logs: D:\KOF Ultimate Online\logs\ai_multi_mode.log
echo 📸 Screenshots: D:\KOF Ultimate Online\ai_screenshots_p1\
echo.
echo Appuyez sur une touche pour fermer cette fenêtre...
pause > nul
