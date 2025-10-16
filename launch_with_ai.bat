@echo off
echo ============================================================
echo KOF Ultimate - Launcher + AI Navigator
echo ============================================================
echo.
echo Lancement du launcher principal...
start "KOF Launcher" python launcher.py

timeout /t 2 /nobreak >nul

echo Lancement de l'agent IA navigator...
start "AI Navigator" python launcher_ai_navigator.py

echo.
echo ============================================================
echo Les deux fenetres sont maintenant ouvertes!
echo.
echo - Fenetre 1: KOF Ultimate Launcher (principal)
echo - Fenetre 2: AI Navigator (monitoring)
echo.
echo L'IA va detecter automatiquement tous les problemes!
echo ============================================================
echo.
pause
