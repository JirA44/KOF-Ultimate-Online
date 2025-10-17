#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - Installation Automatique Ikemen GO
Télécharge et configure Ikemen GO pour être plug-and-play
"""

import urllib.request
import zipfile
import shutil
import os
from pathlib import Path
import json

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def download_file(url, destination):
    """Télécharge un fichier avec barre de progression"""
    print(f"{Colors.CYAN}Téléchargement depuis: {url}{Colors.RESET}")

    try:
        with urllib.request.urlopen(url) as response:
            file_size = int(response.headers.get('Content-Length', 0))

            with open(destination, 'wb') as f:
                downloaded = 0
                chunk_size = 8192

                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break

                    f.write(chunk)
                    downloaded += len(chunk)

                    if file_size > 0:
                        percent = (downloaded / file_size) * 100
                        print(f"\r  Progression: {percent:.1f}% ({downloaded}/{file_size} bytes)", end='', flush=True)

        print(f"\n{Colors.GREEN}✓ Téléchargement terminé{Colors.RESET}")
        return True

    except Exception as e:
        print(f"\n{Colors.RED}✗ Erreur téléchargement: {e}{Colors.RESET}")
        return False

def setup_ikemen_go():
    """Configure Ikemen GO dans le projet"""

    print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'INSTALLATION IKEMEN GO':^80}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

    base_dir = Path(r"D:\KOF Ultimate Online Online Online")
    ikemen_dir = base_dir / "Ikemen_GO"

    # URLs pour télécharger Ikemen GO
    # Version Windows depuis Archive.org (miroir fiable)
    ikemen_url = "https://archive.org/download/ikemengowinbuilds/Ikemen_GO-v0.99.0-windows.zip"

    print(f"{Colors.CYAN}📁 Répertoire d'installation: {ikemen_dir}{Colors.RESET}\n")

    # Étape 1: Télécharger
    print(f"{Colors.CYAN}{Colors.BOLD}Étape 1/5: Téléchargement{Colors.RESET}")

    zip_path = base_dir / "ikemen_temp.zip"

    if zip_path.exists():
        print(f"{Colors.YELLOW}Archive déjà téléchargée{Colors.RESET}")
    else:
        if not download_file(ikemen_url, zip_path):
            print(f"{Colors.RED}✗ Échec du téléchargement{Colors.RESET}")
            print(f"{Colors.YELLOW}Essaye manuellement:{Colors.RESET}")
            print(f"  1. Télécharge: {ikemen_url}")
            print(f"  2. Décompresse dans: {ikemen_dir}")
            return False

    # Étape 2: Extraire
    print(f"\n{Colors.CYAN}{Colors.BOLD}Étape 2/5: Extraction{Colors.RESET}")

    if ikemen_dir.exists():
        print(f"{Colors.YELLOW}Suppression ancien répertoire...{Colors.RESET}")
        shutil.rmtree(ikemen_dir)

    ikemen_dir.mkdir(exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(ikemen_dir)
        print(f"{Colors.GREEN}✓ Extraction réussie{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}✗ Erreur extraction: {e}{Colors.RESET}")
        return False

    # Étape 3: Vérifier l'exécutable
    print(f"\n{Colors.CYAN}{Colors.BOLD}Étape 3/5: Vérification{Colors.RESET}")

    exe_locations = [
        ikemen_dir / "Ikemen_GO.exe",
        ikemen_dir / "Ikemen_GO" / "Ikemen_GO.exe",
        ikemen_dir / "bin" / "Ikemen_GO.exe"
    ]

    ikemen_exe = None
    for loc in exe_locations:
        if loc.exists():
            ikemen_exe = loc
            print(f"{Colors.GREEN}✓ Exécutable trouvé: {loc}{Colors.RESET}")
            break

    if not ikemen_exe:
        print(f"{Colors.RED}✗ Exécutable Ikemen_GO.exe introuvable{Colors.RESET}")
        return False

    # Étape 4: Créer liens symboliques vers chars/data/stages
    print(f"\n{Colors.CYAN}{Colors.BOLD}Étape 4/5: Configuration{Colors.RESET}")

    # Détecter le répertoire racine Ikemen
    ikemen_root = ikemen_exe.parent

    links_to_create = [
        ("chars", base_dir / "chars"),
        ("data", base_dir / "data"),
        ("stages", base_dir / "stages"),
        ("sound", base_dir / "sound"),
        ("font", base_dir / "font")
    ]

    for link_name, target in links_to_create:
        link_path = ikemen_root / link_name

        # Si le lien/dossier existe déjà, le supprimer
        if link_path.exists() or link_path.is_symlink():
            if link_path.is_symlink():
                link_path.unlink()
            else:
                # C'est un vrai dossier, le renommer en backup
                backup = link_path.parent / f"{link_name}_backup"
                if backup.exists():
                    shutil.rmtree(backup)
                shutil.move(str(link_path), str(backup))
                print(f"{Colors.YELLOW}  Backup: {link_name} → {link_name}_backup{Colors.RESET}")

        # Créer lien symbolique
        try:
            # Sur Windows, utiliser junction pour dossiers
            import subprocess
            subprocess.run(['mklink', '/J', str(link_path), str(target)],
                         shell=True, check=True, capture_output=True)
            print(f"{Colors.GREEN}  ✓ Lien créé: {link_name} → {target}{Colors.RESET}")
        except:
            # Si échec, copier les fichiers importants
            try:
                shutil.copytree(target, link_path, dirs_exist_ok=True)
                print(f"{Colors.YELLOW}  ⚠ Copie: {link_name} (lien symbolique échoué){Colors.RESET}")
            except:
                print(f"{Colors.RED}  ✗ Échec: {link_name}{Colors.RESET}")

    # Étape 5: Créer launcher unifié
    print(f"\n{Colors.CYAN}{Colors.BOLD}Étape 5/5: Création launcher unifié{Colors.RESET}")

    launcher_content = f'''@echo off
chcp 65001 > nul
title KOF ULTIMATE - Launcher

echo ================================
echo   KOF ULTIMATE LAUNCHER
echo ================================
echo.
echo Choisissez le moteur:
echo.
echo [1] M.U.G.E.N (Classique)
echo [2] Ikemen GO (Moderne + Netplay)
echo.
set /p choice="Votre choix (1 ou 2): "

if "%choice%"=="1" (
    echo.
    echo Lancement M.U.G.E.N...
    start "" "KOF_Ultimate_Online.exe"
) else if "%choice%"=="2" (
    echo.
    echo Lancement Ikemen GO...
    cd "{ikemen_root.relative_to(base_dir)}"
    start "" "Ikemen_GO.exe"
) else (
    echo.
    echo Choix invalide!
    pause
)
'''

    launcher_path = base_dir / "LAUNCH_KOF_ULTIMATE.bat"
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_content)

    print(f"{Colors.GREEN}✓ Launcher créé: LAUNCH_KOF_ULTIMATE.bat{Colors.RESET}")

    # Nettoyer
    if zip_path.exists():
        zip_path.unlink()
        print(f"{Colors.GREEN}✓ Archive temporaire supprimée{Colors.RESET}")

    # Résumé
    print(f"\n{Colors.GREEN}{Colors.BOLD}{'='*80}{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}{'✓ INSTALLATION TERMINÉE':^80}{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

    print(f"{Colors.CYAN}Ikemen GO est maintenant installé!{Colors.RESET}")
    print(f"{Colors.CYAN}Exécutable: {ikemen_exe}{Colors.RESET}\n")

    print(f"{Colors.YELLOW}Pour lancer:{Colors.RESET}")
    print(f"  - Double-clic sur: {Colors.GREEN}LAUNCH_KOF_ULTIMATE.bat{Colors.RESET}")
    print(f"  - Choisis M.U.G.E.N ou Ikemen GO\n")

    print(f"{Colors.MAGENTA}Avantages Ikemen GO:{Colors.RESET}")
    print(f"  ✓ Support netplay intégré")
    print(f"  ✓ Meilleure performance")
    print(f"  ✓ Plus de fonctionnalités")
    print(f"  ✓ Compatible chars/stages M.U.G.E.N\n")

    return True

def main():
    try:
        setup_ikemen_go()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Installation annulée{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Erreur: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
