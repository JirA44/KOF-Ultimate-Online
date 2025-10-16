@echo off
echo Restauration de la configuration originale...
echo.

cd /d "D:\KOF Ultimate\data"

if exist system.def.backup (
    copy /Y system.def.backup system.def
    echo Configuration system.def restauree !
) else (
    echo Backup system.def non trouve
)

if exist mugen.cfg.backup_backgrounds (
    copy /Y mugen.cfg.backup_backgrounds mugen.cfg
    echo Configuration mugen.cfg restauree !
) else if exist mugen.cfg.backup (
    copy /Y mugen.cfg.backup mugen.cfg
    echo Configuration mugen.cfg restauree !
)

echo.
echo Configuration originale restauree !
echo Le jeu devrait maintenant fonctionner.
echo.
pause
