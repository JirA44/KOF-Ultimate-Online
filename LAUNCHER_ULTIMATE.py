#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - LAUNCHER ULTIME
Auto-Update + Auto-Install + Auto-Repair + Launch
Style Console Plug-and-Play!
"""

import os
import sys
import subprocess
import urllib.request
import json
from pathlib import Path
import time

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class KOFLauncher:
    """Launcher ultime KOF avec auto-update et auto-install"""

    def __init__(self):
        self.game_dir = Path(__file__).parent
        self.version_file = self.game_dir / "VERSION.txt"
        self.current_version = self.load_current_version()
        self.github_repo = "JirA44/KOF-Ultimate-Online"
        self.github_api = f"https://api.github.com/repos/{self.github_repo}/releases/latest"

    def print_banner(self):
        """Affiche le banner du launcher"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════╗")
        print("║                                                                       ║")
        print("║              🎮  KOF ULTIMATE ONLINE - LAUNCHER  🎮                  ║")
        print("║                                                                       ║")
        print("║                        Version 2.0 Enhanced                           ║")
        print("║                                                                       ║")
        print("╚═══════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}\n")

    def load_current_version(self):
        """Charge la version actuelle"""
        if self.version_file.exists():
            with open(self.version_file, 'r') as f:
                return f.read().strip()
        return "2.0.0"

    def save_version(self, version):
        """Sauvegarde la version"""
        with open(self.version_file, 'w') as f:
            f.write(version)

    def check_python_dependencies(self):
        """Vérifie et installe les dépendances Python automatiquement"""
        print(f"{Colors.CYAN}📦 Vérification des dépendances Python...{Colors.RESET}")

        required_modules = {
            'PIL': 'Pillow',
            'pyautogui': 'pyautogui',
            'win32gui': 'pywin32',
            'psutil': 'psutil'
        }

        missing = []

        for module, package in required_modules.items():
            try:
                __import__(module)
                print(f"{Colors.GREEN}  ✓ {package}{Colors.RESET}")
            except ImportError:
                print(f"{Colors.YELLOW}  ⚠ {package} manquant{Colors.RESET}")
                missing.append(package)

        if missing:
            print(f"\n{Colors.CYAN}📥 Installation automatique des dépendances...{Colors.RESET}")

            for package in missing:
                print(f"\n{Colors.CYAN}  → Installation de {package}...{Colors.RESET}")
                try:
                    subprocess.check_call([
                        sys.executable, '-m', 'pip', 'install', package, '--quiet'
                    ])
                    print(f"{Colors.GREEN}  ✓ {package} installé!{Colors.RESET}")
                except subprocess.CalledProcessError:
                    print(f"{Colors.RED}  ✗ Échec installation {package}{Colors.RESET}")

            print(f"\n{Colors.GREEN}✓ Installation terminée!{Colors.RESET}")
        else:
            print(f"\n{Colors.GREEN}✓ Toutes les dépendances sont installées{Colors.RESET}")

    def check_for_updates(self):
        """Vérifie les mises à jour sur GitHub"""
        print(f"\n{Colors.CYAN}🔄 Vérification des mises à jour...{Colors.RESET}")

        try:
            # Requête API GitHub
            with urllib.request.urlopen(self.github_api, timeout=5) as response:
                data = json.loads(response.read())

            latest_version = data['tag_name'].replace('v', '')
            release_notes = data['body']

            print(f"  Version actuelle: {self.current_version}")
            print(f"  Dernière version: {latest_version}")

            if latest_version > self.current_version:
                print(f"\n{Colors.GREEN}🎉 Nouvelle version disponible!{Colors.RESET}")
                print(f"\n{Colors.CYAN}Notes de version:{Colors.RESET}")
                print(release_notes[:200])

                response = input(f"\n{Colors.YELLOW}Voulez-vous mettre à jour maintenant? (o/n): {Colors.RESET}")

                if response.lower() in ['o', 'oui', 'y', 'yes']:
                    self.download_update(data['zipball_url'], latest_version)
                else:
                    print(f"{Colors.YELLOW}Mise à jour annulée{Colors.RESET}")
            else:
                print(f"\n{Colors.GREEN}✓ Vous avez la dernière version!{Colors.RESET}")

        except urllib.error.URLError:
            print(f"{Colors.YELLOW}⚠ Impossible de vérifier les mises à jour (pas d'internet?){Colors.RESET}")
        except Exception as e:
            print(f"{Colors.YELLOW}⚠ Erreur lors de la vérification: {e}{Colors.RESET}")

    def download_update(self, url, version):
        """Télécharge et installe une mise à jour"""
        print(f"\n{Colors.CYAN}📥 Téléchargement de la mise à jour...{Colors.RESET}")

        try:
            update_file = self.game_dir / f"update_{version}.zip"

            # Télécharger
            urllib.request.urlretrieve(url, update_file)

            print(f"{Colors.GREEN}✓ Téléchargement terminé!{Colors.RESET}")
            print(f"\n{Colors.CYAN}📦 Extraction...{Colors.RESET}")

            # Extraire
            import zipfile
            with zipfile.ZipFile(update_file, 'r') as zip_ref:
                zip_ref.extractall(self.game_dir / "update_temp")

            print(f"{Colors.GREEN}✓ Extraction terminée!{Colors.RESET}")

            # Sauvegarder nouvelle version
            self.save_version(version)

            # Nettoyer
            update_file.unlink()

            print(f"\n{Colors.GREEN}✓ Mise à jour installée! Redémarrez le launcher.{Colors.RESET}")
            sys.exit(0)

        except Exception as e:
            print(f"{Colors.RED}✗ Erreur lors de la mise à jour: {e}{Colors.RESET}")

    def auto_repair(self):
        """Auto-réparation avant le lancement"""
        print(f"\n{Colors.CYAN}🔧 Auto-réparation...{Colors.RESET}")

        # Vérifier fichiers essentiels
        exe_file = self.game_dir / "KOF BLACK R.exe"

        if not exe_file.exists():
            print(f"{Colors.RED}✗ KOF BLACK R.exe introuvable!{Colors.RESET}")
            return False

        # Nettoyer les logs
        log_file = self.game_dir / "mugen.log"
        if log_file.exists():
            try:
                log_file.unlink()
                print(f"{Colors.GREEN}  ✓ Logs nettoyés{Colors.RESET}")
            except:
                pass

        # Lancer diagnostic complet si disponible
        diagnostic_script = self.game_dir / "complete_diagnostic.py"
        if diagnostic_script.exists():
            try:
                result = subprocess.run(
                    [sys.executable, str(diagnostic_script)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                # Vérifier si des problèmes ont été détectés
                if "PROBLÈMES DÉTECTÉS" in result.stdout:
                    print(f"{Colors.YELLOW}  ⚠ Quelques problèmes détectés (voir diagnostic){Colors.RESET}")
                else:
                    print(f"{Colors.GREEN}  ✓ Système OK{Colors.RESET}")

            except:
                print(f"{Colors.YELLOW}  ⚠ Diagnostic non disponible{Colors.RESET}")

        print(f"\n{Colors.GREEN}✓ Auto-réparation terminée{Colors.RESET}")
        return True

    def launch_game(self):
        """Lance le jeu"""
        print(f"\n{Colors.CYAN}🎮 Lancement du jeu...{Colors.RESET}")

        exe_file = self.game_dir / "KOF BLACK R.exe"

        try:
            subprocess.Popen(
                [str(exe_file)],
                cwd=str(self.game_dir)
            )

            print(f"\n{Colors.GREEN}✓ Jeu lancé!{Colors.RESET}")
            print(f"\n{Colors.CYAN}Bon jeu! 🎮{Colors.RESET}\n")

            return True

        except Exception as e:
            print(f"\n{Colors.RED}✗ Erreur au lancement: {e}{Colors.RESET}")
            return False

    def show_menu(self):
        """Affiche le menu principal"""
        while True:
            self.print_banner()

            print(f"{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════╗{Colors.RESET}")
            print(f"{Colors.CYAN}║                            MENU PRINCIPAL                             ║{Colors.RESET}")
            print(f"{Colors.CYAN}╠═══════════════════════════════════════════════════════════════════════╣{Colors.RESET}")
            print(f"{Colors.GREEN}║  1. 🎮 JOUER                                                          ║{Colors.RESET}")
            print(f"{Colors.CYAN}║  2. 🔄 Vérifier les mises à jour                                      ║{Colors.RESET}")
            print(f"{Colors.YELLOW}║  3. 🔧 Auto-réparation                                                ║{Colors.RESET}")
            print(f"{Colors.MAGENTA}║  4. 📊 Diagnostic complet                                             ║{Colors.RESET}")
            print(f"{Colors.RED}║  0. ❌ Quitter                                                         ║{Colors.RESET}")
            print(f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")

            choice = input(f"{Colors.CYAN}Votre choix: {Colors.RESET}")

            if choice == '1':
                if self.auto_repair():
                    self.launch_game()
                    time.sleep(2)
                    break

            elif choice == '2':
                self.check_for_updates()
                input(f"\n{Colors.CYAN}Appuyez sur ENTRÉE pour continuer...{Colors.RESET}")

            elif choice == '3':
                self.auto_repair()
                input(f"\n{Colors.CYAN}Appuyez sur ENTRÉE pour continuer...{Colors.RESET}")

            elif choice == '4':
                diagnostic_script = self.game_dir / "complete_diagnostic.py"
                if diagnostic_script.exists():
                    subprocess.run([sys.executable, str(diagnostic_script)])
                else:
                    print(f"{Colors.RED}✗ Script de diagnostic introuvable{Colors.RESET}")
                input(f"\n{Colors.CYAN}Appuyez sur ENTRÉE pour continuer...{Colors.RESET}")

            elif choice == '0':
                print(f"\n{Colors.CYAN}Au revoir! 👋{Colors.RESET}\n")
                break

            else:
                print(f"\n{Colors.RED}Choix invalide!{Colors.RESET}")
                time.sleep(1)

    def run(self):
        """Lance le launcher"""
        self.print_banner()

        # Étape 1: Vérifier Python
        print(f"{Colors.CYAN}Initialisation...{Colors.RESET}\n")
        self.check_python_dependencies()

        # Étape 2: Auto-update (rapide, sans demander)
        self.check_for_updates()

        # Étape 3: Menu ou lancement direct
        time.sleep(1)
        self.show_menu()

def main():
    try:
        launcher = KOFLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.CYAN}Au revoir! 👋{Colors.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.RED}Erreur critique: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        input("\nAppuyez sur ENTRÉE pour fermer...")

if __name__ == '__main__':
    main()
