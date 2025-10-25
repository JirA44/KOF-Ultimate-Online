@echo off
chcp 65001 >nul
echo ╔════════════════════════════════════════════════════╗
echo ║   Installation d'Ikemen GO pour KOF Ultimate      ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM Créer le dossier d'installation
set "INSTALL_DIR=D:\KOF Ultimate Online"
if not exist "%INSTALL_DIR%" (
    echo Création du dossier: %INSTALL_DIR%
    mkdir "%INSTALL_DIR%"
)

echo.
echo Options d'installation:
echo.
echo 1. Télécharger Ikemen GO automatiquement (nécessite wget ou curl)
echo 2. Ouvrir la page de téléchargement dans le navigateur
echo 3. Instructions manuelles
echo.
set /p choice="Votre choix (1-3): "

if "%choice%"=="1" goto auto_download
if "%choice%"=="2" goto open_browser
if "%choice%"=="3" goto manual
goto end

:auto_download
echo.
echo Téléchargement d'Ikemen GO...
echo.

REM Vérifier si curl est disponible
where curl >nul 2>nul
if %errorlevel%==0 (
    echo Utilisation de curl...
    curl -L -o "%INSTALL_DIR%\Ikemen_GO.zip" "https://github.com/ikemen-engine/Ikemen-GO/releases/latest/download/Ikemen_GO_Win.zip"
    if %errorlevel%==0 (
        echo.
        echo ✓ Téléchargement réussi!
        echo Extraction...
        powershell -Command "Expand-Archive -Path '%INSTALL_DIR%\Ikemen_GO.zip' -DestinationPath '%INSTALL_DIR%' -Force"
        echo ✓ Installation terminée!
        goto end
    )
)

echo.
echo ❌ curl non disponible. Utilisation du navigateur...
goto open_browser

:open_browser
echo.
echo Ouverture de la page de téléchargement...
start https://github.com/ikemen-engine/Ikemen-GO/releases/latest
echo.
echo Instructions:
echo 1. Téléchargez le fichier "Ikemen_GO_Win.zip"
echo 2. Extrayez-le dans: %INSTALL_DIR%
echo 3. Relancez le launcher KOF Ultimate
echo.
goto end

:manual
echo.
echo ═══════════════════════════════════════════════════
echo Instructions d'installation manuelle:
echo ═══════════════════════════════════════════════════
echo.
echo 1. Allez sur: https://github.com/ikemen-engine/Ikemen-GO/releases/latest
echo.
echo 2. Téléchargez: Ikemen_GO_Win.zip
echo.
echo 3. Extrayez le contenu dans:
echo    %INSTALL_DIR%\
echo.
echo 4. La structure doit être:
echo    %INSTALL_DIR%\
echo      ├── Ikemen_GO.exe
echo      ├── data\
echo      ├── external\
echo      └── ...
echo.
echo 5. Copiez vos personnages KOF dans:
echo    %INSTALL_DIR%\chars\
echo.
echo 6. Copiez vos stages dans:
echo    %INSTALL_DIR%\stages\
echo.
echo 7. Lancez Ikemen_GO.exe pour tester
echo.
goto end

:end
echo.
echo ════════════════════════════════════════════════════
echo Installation terminée!
echo ════════════════════════════════════════════════════
echo.
pause
