@echo off
chcp 65001 > nul
title KOF ULTIMATE - Nettoyage Portraits Cassés

cd /d "D:\KOF Ultimate Online"

cls
echo ============================================================
echo   🗑️  NETTOYAGE PORTRAITS CASSÉS
echo ============================================================
echo.
echo Ce script va retirer les 20 personnages sans mini-portraits
echo.

echo o | python REMOVE_BROKEN_PORTRAITS.py

echo.
pause
