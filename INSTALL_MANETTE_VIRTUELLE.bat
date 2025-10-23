@echo off
title Installation Manette Virtuelle
color 0B

echo.
echo ═══════════════════════════════════════════════════════
echo    Installation Manette Virtuelle pour Joueurs IA
echo ═══════════════════════════════════════════════════════
echo.
echo Cette installation permet aux joueurs virtuels d'utiliser
echo une MANETTE VIRTUELLE au lieu de votre clavier.
echo.
echo Vous pourrez taper librement pendant que l'IA joue !
echo.
echo ═══════════════════════════════════════════════════════
echo.
echo Installation de vgamepad...
echo.

pip install vgamepad

echo.
echo ═══════════════════════════════════════════════════════
echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ Installation réussie !
    echo.
    echo Vous pouvez maintenant utiliser LAUNCHER_MANETTE.pyw
) else (
    echo ❌ Erreur d'installation
    echo.
    echo Essayez manuellement:
    echo pip install vgamepad
)
echo.
echo ═══════════════════════════════════════════════════════
echo.
pause
