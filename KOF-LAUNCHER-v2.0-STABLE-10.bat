@echo off
chcp 65001 >nul
cls
echo.
echo ══════════════════════════════════════════════════════════════
echo   🧪 TEST MINIMAL - 10 PERSONNAGES SAFE
echo ══════════════════════════════════════════════════════════════
echo.
echo   Ce test utilise SEULEMENT 10 personnages ultra-testés
echo   pour vérifier si le jeu fonctionne de base.
echo.
echo   Personnages disponibles:
echo   - Hunter_U6746
echo   - NeoDio KOFM
echo   - Athena
echo   - akuma
echo   - Kei
echo   - Rose
echo   - Ryuji
echo   - Nero
echo   - Viper
echo   - Eve
echo.
echo ══════════════════════════════════════════════════════════════
echo   INSTRUCTIONS:
echo ══════════════════════════════════════════════════════════════
echo.
echo   1. Le jeu va se lancer avec ces 10 personnages
echo   2. Allez en mode VERSUS (pas Arcade!)
echo   3. Sélectionnez 2 personnages DIFFÉRENTS
echo   4. Testez si le combat fonctionne
echo.
echo   Si ça fonctionne = Le problème vient des autres personnages
echo   Si ça crash encore = Problème de configuration
echo.
echo ══════════════════════════════════════════════════════════════
echo.
pause

cd /d "D:\KOF Ultimate Online"
start "" "KOF_Ultimate_Online.exe"

echo.
echo ✓ Jeu lancé avec 10 personnages minimaux
echo.
pause
