@echo off
chcp 65001 >nul
cls
echo.
echo ══════════════════════════════════════════════════════════════
echo   🎮 KOF ULTIMATE ONLINE - LANCEMENT
echo ══════════════════════════════════════════════════════════════
echo.
echo   ✅ 124 personnages validés et fonctionnels!
echo   ✅ Jeu stable - crashs au chargement corrigés
echo.
echo ══════════════════════════════════════════════════════════════
echo.
echo   ⏳ Lancement du jeu...
echo.

cd /d "D:\KOF Ultimate Online"

REM Vérifier que l'exe existe
if not exist "KOF_Ultimate_Online.exe" (
    echo ❌ ERREUR: KOF_Ultimate_Online.exe introuvable!
    echo.
    echo Vérifiez que vous êtes dans le bon dossier.
    pause
    exit
)

REM Lancer le jeu
start "" "KOF_Ultimate_Online.exe"

echo.
echo   ✓ Jeu lancé!
echo.
echo ══════════════════════════════════════════════════════════════
echo   ⚠️  RAPPEL - JOUER VOUS-MÊME (PAS L'IA!)
echo ══════════════════════════════════════════════════════════════
echo.
echo   Pour jouer MANUELLEMENT:
echo   1. Menu Versus
echo   2. Choisissez un personnage
echo   3. MAINTENEZ ESPACE (START)
echo   4. Tout en maintenant ESPACE, appuyez ENTRÉE
echo   5. Relâchez ESPACE
echo   6. ✅ VOUS contrôlez!
echo.
echo   ❌ Sans ESPACE = L'IA joue à votre place!
echo.
echo ══════════════════════════════════════════════════════════════
echo.
pause
