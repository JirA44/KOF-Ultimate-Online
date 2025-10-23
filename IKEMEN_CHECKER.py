#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IKEMEN GO - VÉRIFICATEUR ET RÉPARATEUR INTELLIGENT
Comprend vraiment le format des fichiers Ikemen GO
"""
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

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

class IkemenChecker:
    """Vérifie et répare les fichiers de configuration Ikemen GO"""

    def __init__(self, base_path=None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent
        self.errors = []
        self.warnings = []
        self.repairs = []

    def print_header(self, text):
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.WHITE}  {text}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

    def print_success(self, text):
        print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

    def print_error(self, text):
        print(f"{Colors.RED}❌ {text}{Colors.RESET}")
        self.errors.append(text)

    def print_warning(self, text):
        print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")
        self.warnings.append(text)

    def print_info(self, text):
        print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")

    def print_repair(self, text):
        print(f"{Colors.MAGENTA}🔧 {text}{Colors.RESET}")
        self.repairs.append(text)

    def parse_select_def(self, file_path):
        """Parse intelligemment le fichier select.def"""

        if not os.path.exists(file_path):
            self.print_error(f"Fichier manquant: {file_path}")
            return None

        config = {
            'characters': [],
            'stages': [],
            'extra_stages': [],
            'settings': {}
        }

        current_section = None

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()

                    # Ignorer les lignes vides et commentaires
                    if not line or line.startswith(';'):
                        continue

                    # Détecter les sections
                    if line.startswith('[') and line.endswith(']'):
                        current_section = line[1:-1].lower()
                        continue

                    # Parser selon la section
                    if current_section == 'characters':
                        # C'est un personnage si ça ne contient pas '='
                        if '=' not in line:
                            config['characters'].append({
                                'path': line,
                                'line': line_num
                            })
                        else:
                            # C'est un paramètre de configuration
                            key, value = line.split('=', 1)
                            config['settings'][key.strip()] = value.strip()

                    elif current_section == 'extrastages':
                        if '=' not in line:
                            config['extra_stages'].append({
                                'path': line,
                                'line': line_num
                            })

                    elif current_section == 'stages':
                        if '=' not in line:
                            config['stages'].append({
                                'path': line,
                                'line': line_num
                            })

                    elif current_section == 'options':
                        if '=' in line:
                            key, value = line.split('=', 1)
                            config['settings'][key.strip()] = value.strip()

        except Exception as e:
            self.print_error(f"Erreur lors de la lecture: {e}")
            return None

        return config

    def verify_characters(self, config):
        """Vérifie que tous les personnages listés existent"""

        self.print_header("VÉRIFICATION DES PERSONNAGES")

        chars_dir = self.base_path / 'chars'

        if not chars_dir.exists():
            self.print_error(f"Dossier chars/ manquant!")
            return False

        valid_chars = []
        invalid_chars = []

        for char in config['characters']:
            char_path = char['path']
            full_path = self.base_path / char_path

            if full_path.exists():
                valid_chars.append(char)
                # print(f"{Colors.GREEN}✓{Colors.RESET} {char_path}")
            else:
                invalid_chars.append(char)
                self.print_error(f"Ligne {char['line']}: {char_path} - FICHIER MANQUANT")

        print(f"\n{Colors.BOLD}Résumé:{Colors.RESET}")
        print(f"  Personnages valides: {Colors.GREEN}{len(valid_chars)}{Colors.RESET}")
        print(f"  Personnages invalides: {Colors.RED}{len(invalid_chars)}{Colors.RESET}")

        return len(invalid_chars) == 0, invalid_chars

    def verify_stages(self, config):
        """Vérifie que tous les stages listés existent"""

        self.print_header("VÉRIFICATION DES STAGES")

        stages_dir = self.base_path / 'stages'

        if not stages_dir.exists():
            self.print_error(f"Dossier stages/ manquant!")
            return False

        all_stages = config['stages'] + config['extra_stages']
        valid_stages = []
        invalid_stages = []

        for stage in all_stages:
            stage_path = stage['path']
            full_path = self.base_path / stage_path

            if full_path.exists():
                valid_stages.append(stage)
                # print(f"{Colors.GREEN}✓{Colors.RESET} {stage_path}")
            else:
                invalid_stages.append(stage)
                self.print_error(f"Ligne {stage['line']}: {stage_path} - FICHIER MANQUANT")

        print(f"\n{Colors.BOLD}Résumé:{Colors.RESET}")
        print(f"  Stages valides: {Colors.GREEN}{len(valid_stages)}{Colors.RESET}")
        print(f"  Stages invalides: {Colors.RED}{len(invalid_stages)}{Colors.RESET}")

        return len(invalid_stages) == 0, invalid_stages

    def create_backup(self, file_path):
        """Crée un backup horodaté du fichier"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.backup_{timestamp}"

        try:
            shutil.copy2(file_path, backup_path)
            self.print_success(f"Backup créé: {os.path.basename(backup_path)}")
            return backup_path
        except Exception as e:
            self.print_error(f"Erreur lors du backup: {e}")
            return None

    def repair_select_def(self, file_path, invalid_chars, invalid_stages):
        """Répare le fichier select.def en supprimant les entrées invalides"""

        if not invalid_chars and not invalid_stages:
            self.print_success("Aucune réparation nécessaire!")
            return True

        self.print_header("RÉPARATION AUTOMATIQUE")

        # Créer un backup
        backup = self.create_backup(file_path)
        if not backup:
            return False

        # Lire le fichier
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        # Marquer les lignes à supprimer
        lines_to_remove = set()
        for item in invalid_chars + invalid_stages:
            lines_to_remove.add(item['line'] - 1)  # -1 car enumerate commence à 0

        # Créer le nouveau contenu
        new_lines = []
        for i, line in enumerate(lines):
            if i in lines_to_remove:
                self.print_repair(f"Suppression ligne {i+1}: {line.strip()}")
            else:
                new_lines.append(line)

        # Écrire le fichier réparé
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

            self.print_success(f"Fichier réparé! ({len(lines_to_remove)} lignes supprimées)")
            return True

        except Exception as e:
            self.print_error(f"Erreur lors de l'écriture: {e}")

            # Restaurer le backup
            try:
                shutil.copy2(backup, file_path)
                self.print_warning("Backup restauré suite à l'erreur")
            except:
                pass

            return False

    def verify_executable(self):
        """Vérifie la présence de l'exécutable"""

        self.print_header("VÉRIFICATION EXÉCUTABLE")

        exe_files = [
            'KOF_Ultimate_Online.exe',
            'Ikemen_GO.exe'
        ]

        found = False
        for exe in exe_files:
            exe_path = self.base_path / exe
            if exe_path.exists():
                self.print_success(f"Trouvé: {exe}")
                found = True

        if not found:
            self.print_error("Aucun exécutable trouvé!")

        return found

    def verify_folders(self):
        """Vérifie la structure des dossiers"""

        self.print_header("VÉRIFICATION STRUCTURE")

        required_folders = [
            'chars',
            'data',
            'stages',
            'sound'
        ]

        all_ok = True
        for folder in required_folders:
            folder_path = self.base_path / folder
            if folder_path.exists():
                self.print_success(f"Dossier {folder}/ présent")
            else:
                self.print_error(f"Dossier {folder}/ MANQUANT")
                all_ok = False

        return all_ok

    def run_full_check(self, auto_repair=False):
        """Exécute une vérification complète"""

        print(f"\n{Colors.BOLD}{Colors.CYAN}")
        print("╔" + "="*68 + "╗")
        print("║" + "  🔍 IKEMEN GO - VÉRIFICATION INTELLIGENTE".ljust(68) + "║")
        print("║" + f"  Base: {str(self.base_path)[:50]}".ljust(68) + "║")
        print("╚" + "="*68 + "╝")
        print(Colors.RESET)

        # Vérifier les dossiers
        folders_ok = self.verify_folders()

        # Vérifier l'exécutable
        exe_ok = self.verify_executable()

        # Parser select.def
        select_def_path = self.base_path / 'data' / 'select.def'
        config = self.parse_select_def(select_def_path)

        if not config:
            return False

        self.print_info(f"Personnages listés: {len(config['characters'])}")
        self.print_info(f"Stages listés: {len(config['stages']) + len(config['extra_stages'])}")

        # Vérifier les personnages
        chars_ok, invalid_chars = self.verify_characters(config)

        # Vérifier les stages
        stages_ok, invalid_stages = self.verify_stages(config)

        # Résumé
        self.print_header("RÉSUMÉ")

        total_issues = len(self.errors)

        if total_issues == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}")
            print("╔" + "="*68 + "╗")
            print("║" + "  ✅ INSTALLATION PARFAITE !".ljust(68) + "║")
            print("║" + "  Aucun problème détecté".ljust(68) + "║")
            print("╚" + "="*68 + "╝")
            print(Colors.RESET)
        else:
            print(f"{Colors.RED}Erreurs détectées: {total_issues}{Colors.RESET}")

            if auto_repair and (invalid_chars or invalid_stages):
                print(f"\n{Colors.YELLOW}Mode réparation automatique activé...{Colors.RESET}")
                if self.repair_select_def(select_def_path, invalid_chars, invalid_stages):
                    print(f"\n{Colors.GREEN}{Colors.BOLD}✅ RÉPARATION RÉUSSIE !{Colors.RESET}")
                    print(f"{Colors.GREEN}Vous pouvez maintenant lancer le jeu.{Colors.RESET}")
                else:
                    print(f"\n{Colors.RED}{Colors.BOLD}❌ ÉCHEC DE LA RÉPARATION{Colors.RESET}")

        if len(self.warnings) > 0:
            print(f"{Colors.YELLOW}Avertissements: {len(self.warnings)}{Colors.RESET}")

        return total_issues == 0


def main():
    """Point d'entrée principal"""

    import argparse

    parser = argparse.ArgumentParser(description='Vérificateur intelligent Ikemen GO')
    parser.add_argument('--auto-repair', action='store_true',
                       help='Réparer automatiquement les problèmes')
    parser.add_argument('--path', type=str,
                       help='Chemin de base du jeu')

    args = parser.parse_args()

    checker = IkemenChecker(base_path=args.path)
    success = checker.run_full_check(auto_repair=args.auto_repair)

    print()

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
