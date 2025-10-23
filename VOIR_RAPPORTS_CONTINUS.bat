@echo off
chcp 65001 >nul
title Rapports Tests Continus - KOF Ultimate
cls

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  📊 RAPPORTS DES TESTS CONTINUS                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

if not exist "logs\tests_continus\stats.json" (
    echo ❌ Aucune statistique disponible
    echo    Les tests ne sont peut-être pas encore lancés
    echo.
    pause
    exit /b
)

echo STATISTIQUES GLOBALES:
echo ═══════════════════════════════════════════════════════════════
type logs\tests_continus\stats.json
echo.
echo.

echo DERNIERS TESTS:
echo ═══════════════════════════════════════════════════════════════
for /f %%i in ('dir /b /o-d logs\tests_continus\test_*.txt 2^>nul ^| more +0') do (
    echo.
    echo ──────────────────────────────────────────────────────────────
    type "logs\tests_continus\%%i"
    echo ──────────────────────────────────────────────────────────────
    goto :break
)
:break

echo.
echo LOG CONTINU (50 dernières lignes):
echo ═══════════════════════════════════════════════════════════════
powershell -Command "Get-Content 'logs\tests_continus\continuous.log' -Tail 50"

echo.
echo.
pause
