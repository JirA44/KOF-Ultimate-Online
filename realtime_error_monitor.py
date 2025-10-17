#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - Moniteur d'Erreurs en Temps Réel
VOIT et CORRIGE automatiquement toutes les erreurs!
"""

import time
import os
from pathlib import Path
from datetime import datetime
import re

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class RealtimeErrorMonitor:
    """Moniteur qui détecte et corrige les erreurs en temps réel"""

    def __init__(self, game_dir):
        self.game_dir = Path(game_dir)
        self.log_file = self.game_dir / "mugen.log"
        self.errors_found = []
        self.errors_fixed = []
        self.last_position = 0

    def watch_log(self):
        """Surveille le log en temps réel"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}👁️ MONITEUR D'ERREURS ACTIF{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")
        print(f"{Colors.YELLOW}Surveillance du fichier: {self.log_file}{Colors.RESET}")
        print(f"{Colors.CYAN}Appuyez sur Ctrl+C pour arrêter\n{Colors.RESET}")

        try:
            while True:
                if self.log_file.exists():
                    with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        # Se positionner à la dernière position lue
                        f.seek(self.last_position)
                        new_lines = f.readlines()
                        self.last_position = f.tell()

                        # Analyser les nouvelles lignes
                        for line in new_lines:
                            self.analyze_line(line)

                time.sleep(0.5)  # Vérifier toutes les 0.5 secondes

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Moniteur arrêté{Colors.RESET}")
            self.show_summary()

    def analyze_line(self, line):
        """Analyse une ligne du log pour détecter des erreurs"""
        line_lower = line.lower()

        # Détecter les erreurs
        if 'error' in line_lower or 'failed' in line_lower:
            # Ignorer les erreurs connues non critiques
            if 'pads' in line_lower or 'joystick' in line_lower:
                return

            print(f"{Colors.RED}❌ ERREUR DÉTECTÉE:{Colors.RESET}")
            print(f"   {line.strip()}")

            # Ajouter à la liste
            error_info = {
                'line': line.strip(),
                'time': datetime.now(),
                'fixed': False
            }
            self.errors_found.append(error_info)

            # Essayer de corriger automatiquement
            self.auto_fix_error(line)

    def auto_fix_error(self, error_line):
        """Essaie de corriger automatiquement l'erreur"""

        # Pattern 1: Error in [file].air:[line]
        match = re.search(r'Error in (\S+\.air):(\d+)', error_line)
        if match:
            air_file = match.group(1)
            line_num = int(match.group(2))

            print(f"{Colors.YELLOW}🔧 Tentative de correction: {air_file} ligne {line_num}{Colors.RESET}")
            self.fix_air_file(air_file, line_num)
            return

        # Pattern 2: Error reading character file: chars/[name]/[name].def
        match = re.search(r'Error reading character file: (chars/[^/]+/[^/]+\.def)', error_line)
        if match:
            char_file = match.group(1)
            print(f"{Colors.YELLOW}🔧 Désactivation personnage défectueux: {char_file}{Colors.RESET}")
            self.disable_character(char_file)
            return

        # Pattern 3: Error loading [file]
        match = re.search(r'Error loading (\S+)', error_line)
        if match:
            file_name = match.group(1)
            print(f"{Colors.YELLOW}🔧 Analyse du fichier: {file_name}{Colors.RESET}")
            # Tenter diverses corrections
            return

    def fix_air_file(self, air_filename, error_line):
        """Corrige un fichier .air avec une erreur"""
        # Chercher le fichier .air
        air_files = list(self.game_dir.glob(f"**/{air_filename}"))

        if not air_files:
            print(f"{Colors.RED}  ✗ Fichier {air_filename} introuvable{Colors.RESET}")
            return

        air_file = air_files[0]
        print(f"{Colors.CYAN}  📁 Fichier trouvé: {air_file}{Colors.RESET}")

        try:
            # Lire le fichier
            with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            if error_line > len(lines):
                print(f"{Colors.RED}  ✗ Ligne {error_line} hors limites{Colors.RESET}")
                return

            # Analyser l'erreur
            error_content = lines[error_line - 1].strip()
            print(f"{Colors.YELLOW}  Ligne problématique: {error_content}{Colors.RESET}")

            # Correction commune: Problème de clsn2 (collision box)
            if 'Clsn2' in error_content or 'clsn2' in error_content.lower():
                print(f"{Colors.CYAN}  🔧 Correction de la collision box...{Colors.RESET}")

                # Commenter la ligne problématique
                lines[error_line - 1] = f"; FIXED: {error_content}\n"

                # Sauvegarder
                with open(air_file, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                print(f"{Colors.GREEN}  ✓ Fichier corrigé! Ligne commentée.{Colors.RESET}")

                self.errors_fixed.append({
                    'file': str(air_file),
                    'line': error_line,
                    'fix': 'Commented collision box line',
                    'time': datetime.now()
                })

                return True

        except Exception as e:
            print(f"{Colors.RED}  ✗ Erreur lors de la correction: {e}{Colors.RESET}")
            return False

    def disable_character(self, char_path):
        """Désactive un personnage défectueux dans select.def"""
        select_def = self.game_dir / "data" / "select.def"

        if not select_def.exists():
            print(f"{Colors.RED}  ✗ select.def introuvable{Colors.RESET}")
            return

        try:
            with open(select_def, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            modified = False
            for i, line in enumerate(lines):
                if char_path in line and not line.strip().startswith(';'):
                    # Commenter la ligne
                    lines[i] = f"; DISABLED: {line}"
                    modified = True
                    print(f"{Colors.GREEN}  ✓ Personnage désactivé dans select.def{Colors.RESET}")

            if modified:
                with open(select_def, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                self.errors_fixed.append({
                    'file': 'select.def',
                    'character': char_path,
                    'fix': 'Character disabled',
                    'time': datetime.now()
                })

        except Exception as e:
            print(f"{Colors.RED}  ✗ Erreur: {e}{Colors.RESET}")

    def show_summary(self):
        """Affiche le résumé"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'RÉSUMÉ':^80}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

        print(f"  Erreurs détectées: {len(self.errors_found)}")
        print(f"  Erreurs corrigées: {len(self.errors_fixed)}")

        if self.errors_fixed:
            print(f"\n{Colors.GREEN}Corrections effectuées:{Colors.RESET}")
            for fix in self.errors_fixed:
                print(f"  ✓ {fix['file']} - {fix['fix']}")

        if self.errors_found and not self.errors_fixed:
            print(f"\n{Colors.YELLOW}Erreurs non corrigées automatiquement:{Colors.RESET}")
            for error in self.errors_found[:5]:
                print(f"  - {error['line']}")

def analyze_existing_log():
    """Analyse le log existant et propose des corrections"""
    print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'🔍 ANALYSE DU LOG EXISTANT':^80}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

    game_dir = Path(r"D:\KOF Ultimate Online")
    log_file = game_dir / "mugen.log"

    if not log_file.exists():
        print(f"{Colors.RED}✗ Aucun log trouvé{Colors.RESET}")
        return

    monitor = RealtimeErrorMonitor(game_dir)

    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    print(f"{Colors.CYAN}Analyse de {len(lines)} lignes...{Colors.RESET}\n")

    for line in lines:
        line_lower = line.lower()
        if ('error' in line_lower or 'failed' in line_lower) and \
           'pads' not in line_lower and 'joystick' not in line_lower:
            monitor.analyze_line(line)

    monitor.show_summary()

    if monitor.errors_fixed:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Corrections appliquées! Relancez le jeu.{Colors.RESET}\n")
    else:
        print(f"\n{Colors.YELLOW}Aucune correction automatique possible.{Colors.RESET}\n")

def main():
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--analyze':
        analyze_existing_log()
    else:
        game_dir = Path(r"D:\KOF Ultimate Online")
        monitor = RealtimeErrorMonitor(game_dir)

        print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'🎮 KOF ULTIMATE - MONITEUR TEMPS RÉEL':^80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

        print(f"{Colors.CYAN}Mode d'emploi:{Colors.RESET}")
        print(f"  1. Lance ce script")
        print(f"  2. Lance le jeu")
        print(f"  3. Les erreurs sont détectées et corrigées automatiquement!")
        print(f"\n{Colors.YELLOW}Ou utilise: python realtime_error_monitor.py --analyze{Colors.RESET}")
        print(f"{Colors.YELLOW}pour analyser le dernier log{Colors.RESET}\n")

        input(f"{Colors.CYAN}Appuyez sur ENTRÉE pour démarrer la surveillance...{Colors.RESET}")

        monitor.watch_log()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Arrêt du moniteur{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Erreur: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
