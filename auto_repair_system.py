#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système d'auto-détection et auto-réparation pour KOF Ultimate
Scanne les logs, détecte les erreurs et les corrige automatiquement
"""

import os
import re
from pathlib import Path
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class AutoRepairSystem:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.log_file = self.base_dir / "mugen.log"
        self.repairs_made = []
        self.errors_found = []

    def log(self, message, level="INFO", color=Colors.WHITE):
        """Log un message avec couleur"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{color}[{timestamp}] [{level}] {message}{Colors.RESET}")

    def print_header(self, text):
        """Affiche un en-tête"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{text:^80}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

    def scan_log_errors(self):
        """Scanne le fichier de log pour détecter les erreurs"""
        if not self.log_file.exists():
            self.log("Aucun log trouvé - première exécution", "INFO", Colors.BLUE)
            return []

        errors = []

        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Détecter les erreurs de personnages
            char_errors = re.findall(
                r'Error in (.+?\.air):(\d+)\s+Error loading (chars/.+?\.def)',
                content
            )

            for air_file, line_num, char_def in char_errors:
                errors.append({
                    'type': 'character_error',
                    'air_file': air_file,
                    'line': line_num,
                    'char': char_def
                })

            # Détecter erreurs de background
            bg_errors = re.findall(r'Error loading (\w+BG)', content)
            for bg_name in bg_errors:
                errors.append({
                    'type': 'background_error',
                    'bg_name': bg_name
                })

            # Détecter erreurs de fichiers manquants
            missing_files = re.findall(r'Error reading character file: (chars/.+?\.def)', content)
            for file_path in missing_files:
                errors.append({
                    'type': 'missing_character',
                    'file': file_path
                })

        except Exception as e:
            self.log(f"Erreur lors de la lecture du log: {e}", "ERROR", Colors.RED)

        return errors

    def repair_character_air(self, char_path, air_file, line_num):
        """Répare une erreur dans un fichier .air"""
        air_path = self.base_dir / "chars" / char_path / air_file

        if not air_path.exists():
            self.log(f"Fichier {air_file} introuvable", "WARN", Colors.YELLOW)
            return False

        try:
            with open(air_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            line_idx = int(line_num) - 1

            if line_idx < 0 or line_idx >= len(lines):
                return False

            original_line = lines[line_idx]

            # Réparer les erreurs de clsn (collision) communes
            if 'clsn' in original_line.lower():
                # Corriger les valeurs invalides
                fixed_line = re.sub(r'clsn\d+:\s*$', 'clsn2: 0', original_line, flags=re.IGNORECASE)
                fixed_line = re.sub(r'clsn\d+\s*=\s*$', 'clsn2 = 0', fixed_line, flags=re.IGNORECASE)

                if fixed_line != original_line:
                    lines[line_idx] = fixed_line

                    with open(air_path, 'w', encoding='utf-8') as f:
                        f.writelines(lines)

                    self.repairs_made.append(f"Réparé {air_file}:{line_num}")
                    return True

            # Si erreur non réparable, commenter la ligne
            if not original_line.strip().startswith(';'):
                lines[line_idx] = '; ' + original_line

                with open(air_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                self.repairs_made.append(f"Commenté ligne problématique {air_file}:{line_num}")
                return True

        except Exception as e:
            self.log(f"Erreur lors de la réparation: {e}", "ERROR", Colors.RED)

        return False

    def remove_problematic_character(self, char_def):
        """Retire un personnage problématique de select.def"""
        select_def = self.base_dir / 'data' / 'select.def'

        if not select_def.exists():
            return False

        try:
            with open(select_def, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            char_name = char_def.replace('chars/', '').replace('.def', '').split('/')[0]
            modified = False

            for i, line in enumerate(lines):
                if char_name in line and not line.strip().startswith(';'):
                    lines[i] = '; ' + line
                    modified = True

            if modified:
                with open(select_def, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                self.repairs_made.append(f"Désactivé personnage problématique: {char_name}")
                return True

        except Exception as e:
            self.log(f"Erreur lors de la modification de select.def: {e}", "ERROR", Colors.RED)

        return False

    def check_joystick_config(self):
        """Vérifie et optimise la configuration joystick"""
        mugen_cfg = self.base_dir / 'data' / 'mugen.cfg'

        if not mugen_cfg.exists():
            return False

        try:
            with open(mugen_cfg, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Vérifier les paramètres joystick
            if 'P1.Joystick.type = 0' in content or 'P2.Joystick.type = 0' in content:
                # Activer l'auto-détection
                content = content.replace('P1.Joystick.type = 0', 'P1.Joystick.type = 1')
                content = content.replace('P2.Joystick.type = 0', 'P2.Joystick.type = 1')

                with open(mugen_cfg, 'w', encoding='utf-8') as f:
                    f.write(content)

                self.repairs_made.append("Activé auto-détection des manettes")
                return True

            self.log("Configuration manette OK", "INFO", Colors.GREEN)
            return True

        except Exception as e:
            self.log(f"Erreur configuration manette: {e}", "ERROR", Colors.RED)

        return False

    def run_full_scan(self):
        """Lance un scan complet et répare automatiquement"""
        self.print_header("AUTO-REPAIR SYSTEM - SCAN COMPLET")

        # 1. Scanner les erreurs
        self.log("Scan des logs d'erreurs...", "INFO", Colors.BLUE)
        errors = self.scan_log_errors()

        if errors:
            self.log(f"Trouvé {len(errors)} erreur(s)", "WARN", Colors.YELLOW)
            self.errors_found = errors
        else:
            self.log("Aucune erreur détectée", "OK", Colors.GREEN)

        # 2. Réparer les erreurs de personnages
        for error in errors:
            if error['type'] == 'character_error':
                self.log(f"Réparation de {error['char']}...", "INFO", Colors.BLUE)

                # Extraire le nom du personnage
                char_name = error['char'].replace('chars/', '').replace('.def', '').split('/')[0]

                if self.repair_character_air(char_name, error['air_file'], error['line']):
                    self.log(f"✓ Réparé {error['air_file']}", "OK", Colors.GREEN)
                else:
                    # Si réparation impossible, désactiver le personnage
                    self.log(f"Désactivation de {char_name}...", "WARN", Colors.YELLOW)
                    self.remove_problematic_character(error['char'])

        # 3. Vérifier configuration manette
        self.log("Vérification configuration manette...", "INFO", Colors.BLUE)
        self.check_joystick_config()

        # 4. Rapport final
        self.print_header("RAPPORT DE RÉPARATION")

        print(f"{Colors.BOLD}Erreurs détectées:{Colors.RESET} {len(self.errors_found)}")
        print(f"{Colors.BOLD}Réparations effectuées:{Colors.RESET} {len(self.repairs_made)}")

        if self.repairs_made:
            print(f"\n{Colors.GREEN}{Colors.BOLD}Réparations:{Colors.RESET}")
            for repair in self.repairs_made:
                print(f"{Colors.GREEN}  ✓ {repair}{Colors.RESET}")

        if len(self.errors_found) == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ SYSTÈME EN PARFAIT ÉTAT{Colors.RESET}")
        elif len(self.repairs_made) > 0:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ RÉPARATIONS APPLIQUÉES - Relancez le jeu{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ ERREURS NON RÉPARABLES - Vérification manuelle requise{Colors.RESET}")

        print()

def main():
    repair_system = AutoRepairSystem()
    repair_system.run_full_scan()

if __name__ == '__main__':
    main()
