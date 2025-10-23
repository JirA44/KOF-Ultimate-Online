@echo off
REM ================================================================
REM KOF ULTIMATE ONLINE - BATTLE.NET LAUNCHER
REM Style Warcraft 3 Battle.net
REM ================================================================

title KOF Ultimate Online - Battle.net
color 0B
mode con: cols=90 lines=35

:MENU
cls
echo.
echo ================================================================================
echo.
echo            ██╗  ██╗ ██████╗ ███████╗    ██╗   ██╗██╗  ████████╗██╗███╗   ███╗
echo            ██║ ██╔╝██╔═══██╗██╔════╝    ██║   ██║██║  ╚══██╔══╝██║████╗ ████║
echo            █████╔╝ ██║   ██║█████╗      ██║   ██║██║     ██║   ██║██╔████╔██║
echo            ██╔═██╗ ██║   ██║██╔══╝      ██║   ██║██║     ██║   ██║██║╚██╔╝██║
echo            ██║  ██╗╚██████╔╝██║         ╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║
echo            ╚═╝  ╚═╝ ╚═════╝ ╚═╝          ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝
echo.
echo                          ULTIMATE ONLINE - BATTLE.NET
echo.
echo ================================================================================
echo.
echo                           ⚔️  MODE DE JEU  ⚔️
echo.
echo      [1] 🎮 JOUER EN SOLO (vs IA)
echo          Lance le jeu en mode solo contre l'ordinateur
echo.
echo      [2] 🌐 JOUER EN LIGNE (Battle.net Style)
echo          Interface complète avec lobby, chat, matchmaking
echo.
echo      [3] 🏠 CRÉER UNE PARTIE (Host Netplay)
echo          Héberger une partie pour jouer avec un ami
echo.
echo      [4] 🎯 REJOINDRE UNE PARTIE (Join Netplay)
echo          Rejoindre la partie d'un ami via IP
echo.
echo      [5] 📊 STATISTIQUES ET CLASSEMENT
echo          Voir ton profil, stats, ladder
echo.
echo      [6] ⚙️  PARAMÈTRES
echo          Configuration, contrôles, graphismes
echo.
echo      [7] 🚪 QUITTER
echo.
echo ================================================================================
echo.
choice /c 1234567 /n /m "Choix: "

if errorlevel 7 goto QUIT
if errorlevel 6 goto SETTINGS
if errorlevel 5 goto STATS
if errorlevel 4 goto JOIN_GAME
if errorlevel 3 goto HOST_GAME
if errorlevel 2 goto ONLINE_BATTLENET
if errorlevel 1 goto SOLO_GAME

:SOLO_GAME
cls
echo.
echo ================================================================
echo   🎮 MODE SOLO - vs IA
echo ================================================================
echo.
echo [INFO] Lancement du jeu en mode solo...
echo [INFO] Vous jouez contre l'ordinateur
echo.

REM Arrêter les scripts IA
taskkill /F /IM python.exe /FI "WINDOWTITLE eq AI*" >nul 2>&1

REM Lancer en mini-fenêtre visible
if exist "apply_mini_window_config.py" (
    echo [CONFIG] Application mini-fenetre 960x720...
    python apply_mini_window_config.py 960 720 2>nul
)

echo [LAUNCH] Démarrage du jeu...
timeout /t 2 /nobreak >nul

start "KOF Ultimate - Solo" /NORMAL "KOF_Ultimate_Online.exe"

echo.
echo ✓ Jeu lancé en mode solo!
echo.
echo Appuyez sur une touche pour retourner au menu...
pause >nul
goto MENU

:ONLINE_BATTLENET
cls
echo.
echo ================================================================
echo   🌐 BATTLE.NET - MODE EN LIGNE
echo ================================================================
echo.
echo [1/3] Vérification du serveur de matchmaking...

REM Vérifier si le serveur tourne
tasklist | find /i "python" | find /i "matchmaking_server" >nul
if errorlevel 1 (
    echo [WARN] Serveur non détecté, lancement automatique...
    start "Matchmaking Server" /MIN python matchmaking_server.py
    timeout /t 3 /nobreak >nul
    echo [OK] Serveur lancé!
) else (
    echo [OK] Serveur déjà actif!
)

echo.
echo [2/3] Lancement de l'interface Battle.net...
timeout /t 1 /nobreak >nul

REM Lancer l'interface Battle.net
start "KOF Battle.net" python battlenet_interface.py

echo.
echo [3/3] Interface Battle.net lancée!
echo.
echo ================================================================
echo   FONCTIONNALITÉS BATTLE.NET:
echo ================================================================
echo   ✓ Lobby avec joueurs en ligne
echo   ✓ Chat en temps réel
echo   ✓ Classement / Ladder
echo   ✓ Création de parties custom
echo   ✓ Matchmaking automatique
echo   ✓ Profils et statistiques
echo ================================================================
echo.
echo L'interface s'ouvre dans une nouvelle fenêtre!
echo.
pause
goto MENU

:HOST_GAME
cls
echo.
echo ================================================================
echo   🏠 CRÉER UNE PARTIE (NETPLAY)
echo ================================================================
echo.
echo [INFO] Vous allez héberger une partie Ikemen GO
echo [INFO] Votre ami devra rejoindre avec votre IP
echo.
echo [1/3] Récupération de votre IP...

REM Obtenir l'IP locale
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do set IP=%%a
set IP=%IP:~1%

echo [OK] Votre IP locale: %IP%
echo.
echo [2/3] Pour jouer en ligne, communiquez votre IP PUBLIQUE:
echo       → Visitez: https://whatismyip.com
echo       → Ouvrez le port 7500 sur votre routeur
echo.

set /p CONTINUE="[3/3] Prêt à lancer le jeu en mode hôte? (O/N): "
if /i not "%CONTINUE%"=="O" goto MENU

echo.
echo [LAUNCH] Lancement d'Ikemen GO en mode hôte...
cd Ikemen_GO
start "KOF Ultimate - Host" /NORMAL "Ikemen_GO.exe"
cd ..

echo.
echo ================================================================
echo   INSTRUCTIONS HÔTE:
echo ================================================================
echo   1. Dans le menu, sélectionnez "MULTIJOUEUR EN LIGNE"
echo   2. Choisissez "CRÉER UNE PARTIE"
echo   3. Partagez votre IP avec votre ami
echo   4. Attendez qu'il se connecte!
echo ================================================================
echo.
pause
goto MENU

:JOIN_GAME
cls
echo.
echo ================================================================
echo   🎯 REJOINDRE UNE PARTIE (NETPLAY)
echo ================================================================
echo.
echo [INFO] Vous allez rejoindre une partie Ikemen GO
echo.
set /p HOST_IP="Entrez l'IP de l'hôte: "

if "%HOST_IP%"=="" (
    echo [ERROR] IP invalide!
    pause
    goto MENU
)

echo.
echo [OK] Connexion à %HOST_IP%...
echo [LAUNCH] Lancement d'Ikemen GO...

cd Ikemen_GO
start "KOF Ultimate - Client" /NORMAL "Ikemen_GO.exe"
cd ..

echo.
echo ================================================================
echo   INSTRUCTIONS CLIENT:
echo ================================================================
echo   1. Dans le menu, sélectionnez "MULTIJOUEUR EN LIGNE"
echo   2. Choisissez "REJOINDRE UNE PARTIE"
echo   3. Entrez l'IP: %HOST_IP%
echo   4. Port: 7500 (par défaut)
echo   5. Connectez-vous et jouez!
echo ================================================================
echo.
pause
goto MENU

:STATS
cls
echo.
echo ================================================================
echo   📊 STATISTIQUES ET CLASSEMENT
echo ================================================================
echo.

if not exist "profiles\profiles_database.json" (
    echo [INFO] Aucun profil trouvé.
    echo [INFO] Créez un profil via l'interface Battle.net!
    echo.
    pause
    goto MENU
)

echo [INFO] Affichage des statistiques...
echo.
python -c "
import json
from pathlib import Path

db_file = Path('profiles/profiles_database.json')
if db_file.exists():
    with open(db_file, 'r') as f:
        data = json.load(f)

    profiles = data.get('profiles', {})

    if not profiles:
        print('Aucun profil trouvé.')
    else:
        print('═' * 70)
        print('  TOP 10 JOUEURS')
        print('═' * 70)

        # Trier par MMR
        sorted_players = sorted(profiles.items(), key=lambda x: x[1].get('stats', {}).get('ranking_points', 0), reverse=True)

        for i, (username, data) in enumerate(sorted_players[:10], 1):
            stats = data.get('stats', {})
            mmr = stats.get('ranking_points', 1000)
            wins = stats.get('wins', 0)
            losses = stats.get('losses', 0)
            level = stats.get('level', 1)

            print(f'{i:2d}. {username:20s} | MMR: {mmr:4d} | Niv.{level:2d} | {wins}V-{losses}D')

        print('═' * 70)
else:
    print('Base de données non trouvée.')
" 2>nul

echo.
echo.
pause
goto MENU

:SETTINGS
cls
echo.
echo ================================================================
echo   ⚙️  PARAMÈTRES
echo ================================================================
echo.
echo   [1] 🖥️  Mini-fenêtre visible (800x600)
echo   [2] 🖥️  Mini-fenêtre moyenne (960x720)
echo   [3] 🖥️  Plein écran (restaurer)
echo   [4] 🔧 Diagnostic complet
echo   [5] 🔙 Retour au menu
echo.
choice /c 12345 /n /m "Choix: "

if errorlevel 5 goto MENU
if errorlevel 4 goto DIAGNOSTIC
if errorlevel 3 goto RESTORE_FULL
if errorlevel 2 goto APPLY_960
if errorlevel 1 goto APPLY_800

:APPLY_800
echo.
echo [CONFIG] Application mini-fenêtre 800x600...
python apply_mini_window_config.py 800 600 2>nul
echo [OK] Configuration appliquée!
pause
goto SETTINGS

:APPLY_960
echo.
echo [CONFIG] Application mini-fenêtre 960x720...
python apply_mini_window_config.py 960 720 2>nul
echo [OK] Configuration appliquée!
pause
goto SETTINGS

:RESTORE_FULL
echo.
echo [RESTORE] Restauration du plein écran...
if exist "data\mugen.cfg.original_backup" (
    copy /Y "data\mugen.cfg.original_backup" "data\mugen.cfg" >nul
    echo [OK] Plein écran restauré!
) else (
    echo [WARN] Backup non trouvé, configuration manuelle nécessaire
)
pause
goto SETTINGS

:DIAGNOSTIC
cls
echo.
echo ================================================================
echo   🔧 DIAGNOSTIC COMPLET
echo ================================================================
echo.
python DIAGNOSTIC_JOUABILITE.py
pause
goto SETTINGS

:QUIT
cls
echo.
echo ================================================================
echo   🚪 FERMETURE
echo ================================================================
echo.
echo Merci d'avoir joué à KOF Ultimate Online!
echo À bientôt sur le Battle.net! ⚔️
echo.
timeout /t 2 /nobreak >nul
exit /b 0
