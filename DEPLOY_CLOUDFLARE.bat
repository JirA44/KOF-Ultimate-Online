@echo off
chcp 65001 >nul
title KOF Ultimate Online - Déploiement Cloudflare
cls

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║     🌐 DÉPLOIEMENT CLOUDFLARE PAGES - KOF ULTIMATE       ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo.

cd /d "D:\KOF Ultimate Online"

echo [INFO] Ce script va préparer et pousser le site vers GitHub
echo [INFO] puis Cloudflare Pages le déploiera automatiquement
echo.
echo.

REM Vérifier que Git est installé
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Git n'est pas installé
    echo.
    echo Veuillez installer Git depuis: https://git-scm.com/
    echo.
    pause
    exit /b 1
)

echo [OK] Git est installé
git --version
echo.
echo.

REM Vérifier qu'on est sur la branche main
echo [INFO] Vérification de la branche Git...
git rev-parse --abbrev-ref HEAD >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Initialisation de Git...
    git init
    git branch -M main
    echo [OK] Git initialisé
)
echo.

REM Ajouter les fichiers web
echo [INFO] Ajout des fichiers du site web...
git add web/
git add .gitignore
git add README_CLOUDFLARE.md
git add README_SITE_WEB.md
echo [OK] Fichiers ajoutés
echo.

REM Créer un commit
echo [INFO] Création du commit...
set /p commit_msg="Message du commit (ou Enter pour utiliser le message par défaut): "
if "%commit_msg%"=="" set commit_msg=Mise à jour du site web KOF Ultimate Online

git commit -m "%commit_msg%"
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Aucun changement à commiter ou commit déjà fait
)
echo.

REM Vérifier qu'un remote existe
git remote get-url origin >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ╔═══════════════════════════════════════════════════════════╗
    echo ║                                                           ║
    echo ║              CONFIGURATION GITHUB NÉCESSAIRE              ║
    echo ║                                                           ║
    echo ╚═══════════════════════════════════════════════════════════╝
    echo.
    echo [ACTION REQUISE] Vous devez d'abord créer un repository sur GitHub
    echo.
    echo Étapes:
    echo   1. Allez sur https://github.com/new
    echo   2. Nom du repository: kof-ultimate-online-web
    echo   3. Public ou Private (au choix)
    echo   4. NE PAS initialiser avec README
    echo   5. Créez le repository
    echo   6. Copiez l'URL du repository (ex: https://github.com/USERNAME/kof-ultimate-online-web.git)
    echo.
    echo.
    set /p repo_url="Collez l'URL de votre repository GitHub: "

    if "%repo_url%"=="" (
        echo [ERREUR] URL du repository non fournie
        pause
        exit /b 1
    )

    git remote add origin "%repo_url%"
    echo [OK] Remote ajouté: %repo_url%
    echo.
)

REM Pousser vers GitHub
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║                 PUSH VERS GITHUB                          ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo [INFO] Push vers GitHub...
echo.

git push -u origin main
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERREUR] Échec du push
    echo.
    echo Causes possibles:
    echo   - Vous n'êtes pas authentifié sur GitHub
    echo   - L'URL du repository est incorrecte
    echo   - Vous n'avez pas les permissions
    echo.
    echo Solution:
    echo   - Configurez Git avec vos identifiants GitHub
    echo   - Vérifiez l'URL du repository
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Code poussé vers GitHub avec succès!
echo.
echo.

echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║              ✅ PUSH GITHUB RÉUSSI !                      ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo.
echo PROCHAINES ÉTAPES:
echo.
echo 1. Allez sur: https://dash.cloudflare.com
echo.
echo 2. Connectez-vous ou créez un compte (gratuit)
echo.
echo 3. Allez dans "Workers ^& Pages" puis "Create application"
echo.
echo 4. Choisissez "Pages" puis "Connect to Git"
echo.
echo 5. Sélectionnez votre repository GitHub
echo.
echo 6. Configurez:
echo      - Build output directory: web
echo      - Build command: (laisser vide)
echo.
echo 7. Cliquez sur "Save and Deploy"
echo.
echo 8. Attendez 1-2 minutes
echo.
echo 9. Votre site sera accessible sur: https://VOTRE-PROJET.pages.dev
echo.
echo.
echo 📖 Guide complet: README_CLOUDFLARE.md
echo.
echo.

pause
