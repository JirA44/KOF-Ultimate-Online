#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IKEMEN GO - RECONSTRUCTEUR AUTOMATIQUE DE SELECT.DEF
Scanne les personnages et stages disponibles et reconstruit le fichier
"""
import os
import sys
from pathlib import Path
from datetime import datetime
import shutil

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class SelectDefRebuilder:
    """Reconstruit le fichier select.def en scannant les fichiers disponibles"""

    def __init__(self, base_path=None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent
        self.characters = []
        self.stages = []

    def print_header(self, text):
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.WHITE}  {text}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

    def print_success(self, text):
        print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

    def print_info(self, text):
        print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")

    def print_warning(self, text):
        print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

    def scan_characters(self):
        """Scanne le dossier chars/ pour trouver tous les personnages disponibles"""

        self.print_header("SCAN DES PERSONNAGES DISPONIBLES")

        chars_dir = self.base_path / 'chars'

        if not chars_dir.exists():
            print(f"{Colors.RED}❌ Dossier chars/ manquant!{Colors.RESET}")
            return False

        self.characters = []

        # Parcourir tous les sous-dossiers
        for char_folder in sorted(chars_dir.iterdir()):
            if not char_folder.is_dir():
                continue

            # Chercher le fichier .def principal
            # Le nom du fichier .def devrait correspondre au nom du dossier
            char_name = char_folder.name
            def_file = char_folder / f"{char_name}.def"

            if def_file.exists():
                # Chemin relatif depuis la racine
                relative_path = f"chars/{char_name}/{char_name}.def"
                self.characters.append(relative_path)
                print(f"{Colors.GREEN}✓{Colors.RESET} {relative_path}")
            else:
                # Parfois le fichier .def a un nom différent
                # Chercher tous les .def dans le dossier
                def_files = list(char_folder.glob("*.def"))
                if def_files:
                    # Prendre le premier trouvé
                    def_file = def_files[0]
                    relative_path = f"chars/{char_name}/{def_file.name}"
                    self.characters.append(relative_path)
                    print(f"{Colors.YELLOW}✓{Colors.RESET} {relative_path} {Colors.YELLOW}(nom différent){Colors.RESET}")
                else:
                    print(f"{Colors.RED}✗{Colors.RESET} {char_name} {Colors.RED}(pas de .def trouvé){Colors.RESET}")

        print(f"\n{Colors.BOLD}Total: {len(self.characters)} personnages trouvés{Colors.RESET}")
        return True

    def scan_stages(self):
        """Scanne le dossier stages/ pour trouver tous les stages disponibles"""

        self.print_header("SCAN DES STAGES DISPONIBLES")

        stages_dir = self.base_path / 'stages'

        if not stages_dir.exists():
            print(f"{Colors.RED}❌ Dossier stages/ manquant!{Colors.RESET}")
            return False

        self.stages = []

        # Chercher tous les fichiers .def directement dans stages/
        for stage_file in sorted(stages_dir.glob("*.def")):
            relative_path = f"stages/{stage_file.name}"
            self.stages.append(relative_path)
            print(f"{Colors.GREEN}✓{Colors.RESET} {relative_path}")

        # Chercher aussi dans les sous-dossiers
        for stage_folder in sorted(stages_dir.iterdir()):
            if not stage_folder.is_dir():
                continue

            for stage_file in stage_folder.glob("*.def"):
                relative_path = f"stages/{stage_folder.name}/{stage_file.name}"
                self.stages.append(relative_path)
                print(f"{Colors.GREEN}✓{Colors.RESET} {relative_path}")

        print(f"\n{Colors.BOLD}Total: {len(self.stages)} stages trouvés{Colors.RESET}")
        return True

    def create_backup(self, file_path):
        """Crée un backup horodaté du fichier"""

        if not os.path.exists(file_path):
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.backup_{timestamp}"

        try:
            shutil.copy2(file_path, backup_path)
            self.print_success(f"Backup créé: {os.path.basename(backup_path)}")
            return backup_path
        except Exception as e:
            print(f"{Colors.RED}❌ Erreur lors du backup: {e}{Colors.RESET}")
            return None

    def read_original_settings(self, file_path):
        """Lit les paramètres de configuration de l'ancien fichier"""

        settings = {
            'arcade.maxmatches': '6,1,1,0,0,0,0,0,0,0',
            'team.maxmatches': '4,1,1,0,0,0,0,0,0,0',
        }

        if not os.path.exists(file_path):
            return settings

        try:
            current_section = None
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()

                    if not line or line.startswith(';'):
                        continue

                    if line.startswith('[') and line.endswith(']'):
                        current_section = line[1:-1].lower()
                        continue

                    if current_section in ['characters', 'options'] and '=' in line:
                        key, value = line.split('=', 1)
                        settings[key.strip()] = value.strip()

        except Exception as e:
            self.print_warning(f"Erreur lors de la lecture des paramètres: {e}")

        return settings

    def write_select_def(self, file_path):
        """Écrit le nouveau fichier select.def"""

        self.print_header("RECONSTRUCTION DU FICHIER SELECT.DEF")

        # Créer un backup de l'ancien fichier
        self.create_backup(file_path)

        # Lire les paramètres de l'ancien fichier
        settings = self.read_original_settings(file_path)

        # Générer le contenu
        content = []

        # En-tête
        content.append("; IKEMEN GO Select.def")
        content.append("; Auto-généré le " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        content.append("; Par REBUILD_SELECT.py")
        content.append("")

        # Section Characters
        content.append("[Characters]")
        content.append(";------------------------------")
        content.append("")

        # Paramètres
        content.append(f"arcade.maxmatches = {settings.get('arcade.maxmatches', '6,1,1,0,0,0,0,0,0,0')}")
        content.append(f"team.maxmatches = {settings.get('team.maxmatches', '4,1,1,0,0,0,0,0,0,0')}")
        content.append("")

        # Liste des personnages
        for char_path in self.characters:
            content.append(char_path)

        content.append("")

        # Section ExtraStages
        content.append("[ExtraStages]")
        content.append(";------------------------------")
        content.append("")

        # Ajouter quelques stages en extra (les 5 premiers)
        for stage_path in self.stages[:5]:
            content.append(stage_path)

        content.append("")

        # Section Stages
        content.append("[Stages]")
        content.append(";------------------------------")
        content.append("")

        # Tous les stages
        for stage_path in self.stages:
            content.append(stage_path)

        content.append("")

        # Section Options
        content.append("[Options]")
        content.append(";------------------------------")
        content.append("")
        content.append("arcade.rematches = 0")
        content.append("team.loseondraw = 1")
        content.append("")

        # Écrire le fichier
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(content))

            self.print_success(f"Fichier créé: {file_path}")
            self.print_info(f"  {len(self.characters)} personnages")
            self.print_info(f"  {len(self.stages)} stages")

            return True

        except Exception as e:
            print(f"{Colors.RED}❌ Erreur lors de l'écriture: {e}{Colors.RESET}")
            return False

    def rebuild(self):
        """Reconstruit complètement le select.def"""

        print(f"\n{Colors.BOLD}{Colors.CYAN}")
        print("╔" + "="*68 + "╗")
        print("║" + "  🔨 RECONSTRUCTION AUTOMATIQUE DE SELECT.DEF".ljust(68) + "║")
        print("╚" + "="*68 + "╝")
        print(Colors.RESET)

        # Scanner les personnages
        if not self.scan_characters():
            return False

        # Scanner les stages
        if not self.scan_stages():
            return False

        # Reconstruire le fichier
        select_def_path = self.base_path / 'data' / 'select.def'
        if not self.write_select_def(select_def_path):
            return False

        # Résumé
        print(f"\n{Colors.GREEN}{Colors.BOLD}")
        print("╔" + "="*68 + "╗")
        print("║" + "  ✅ RECONSTRUCTION RÉUSSIE !".ljust(68) + "║")
        print("║" + f"  {len(self.characters)} personnages + {len(self.stages)} stages configurés".ljust(68) + "║")
        print("╚" + "="*68 + "╝")
        print(Colors.RESET)

        return True


def main():
    """Point d'entrée principal"""

    import argparse

    parser = argparse.ArgumentParser(description='Reconstructeur select.def')
    parser.add_argument('--path', type=str,
                       help='Chemin de base du jeu')
    parser.add_argument('--yes', action='store_true',
                       help='Ne pas demander de confirmation')

    args = parser.parse_args()

    rebuilder = SelectDefRebuilder(base_path=args.path)

    if not args.yes:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}ATTENTION !{Colors.RESET}")
        print(f"{Colors.YELLOW}Cette opération va REMPLACER le fichier select.def actuel.{Colors.RESET}")
        print(f"{Colors.YELLOW}Un backup sera créé automatiquement.{Colors.RESET}\n")

        response = input("Continuer ? (o/N) : ").strip().lower()
        if response not in ['o', 'oui', 'y', 'yes']:
            print(f"\n{Colors.RED}Opération annulée.{Colors.RESET}\n")
            return 1

    success = rebuilder.rebuild()

    print()

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
