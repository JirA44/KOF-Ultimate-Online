@echo off
title CORRECTION URGENTE - KOF Ultimate
color 0C
cls

echo.
echo ================================================================
echo             CORRECTION URGENTE - KOF Ultimate
echo ================================================================
echo.
echo Le jeu ne demarre pas a cause des backgrounds PNG.
echo MUGEN a besoin de fichiers SFF, pas de PNG.
echo.
echo Cette correction va restaurer la configuration originale.
echo.
pause

cd /d "D:\KOF Ultimate\data"

echo.
echo [1/2] Recherche des backups...

set RESTORED=0

if exist mugen.cfg.backup (
    copy /Y mugen.cfg.backup mugen.cfg >nul 2>&1
    echo   [OK] mugen.cfg restaure depuis backup
    set RESTORED=1
) else (
    echo   [!] Backup mugen.cfg non trouve
)

if exist mugen.cfg.backup_backgrounds (
    copy /Y mugen.cfg.backup_backgrounds mugen.cfg >nul 2>&1
    echo   [OK] mugen.cfg restaure depuis backup_backgrounds
    set RESTORED=1
)

echo.
echo [2/2] Suppression des modifications problematiques dans system.def...

cd /d "D:\KOF Ultimate"

python -c "import pathlib; p = pathlib.Path('data/system.def'); lines = p.read_text(encoding='utf-8', errors='ignore').split('\n'); cleaned = [l for l in lines if 'data/backgrounds/' not in l or l.strip().startswith(';')]; p.write_text('\n'.join(cleaned), encoding='utf-8')" 2>nul

echo   [OK] Lignes problematiques supprimees

echo.
echo ================================================================
echo                    CORRECTION TERMINEE !
echo ================================================================
echo.
echo Le jeu devrait maintenant fonctionner normalement.
echo.
echo NOTE: Les backgrounds PNG sont dans data/backgrounds/
echo       mais ne sont pas utilises par le jeu (MUGEN ne supporte pas PNG).
echo.
echo Pour utiliser ces backgrounds, il faut:
echo   1. Les convertir en SFF avec Fighter Factory
echo   2. Modifier system.def manuellement
echo.
echo ================================================================
echo.
echo Vous pouvez maintenant lancer le jeu !
echo.
pause
