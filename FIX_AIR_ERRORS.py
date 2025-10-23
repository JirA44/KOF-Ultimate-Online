#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIX AIR ERRORS
Désactive les personnages avec erreurs dans les fichiers .air
"""

import re
from pathlib import Path
import shutil
from datetime import datetime

class AIRErrorFixer:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.select_def = self.base_path / "data" / "select.def"
        self.broken_chars = []

    def log(self, message, level="INFO"):
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "FIX": "🔧"}
        print(f"{icons.get(level, '')} {message}")

    def check_air_file_syntax(self, air_file):
        """Vérifie la syntaxe d'un fichier .air"""
        try:
            content = air_file.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')

            current_action = None

            for i, line in enumerate(lines, 1):
                line = line.strip()

                # Ignorer commentaires
                if line.startswith(';') or not line:
                    continue

                # Détecter les actions
                if line.startswith('[Begin Action'):
                    current_action = line

                # Vérifier les clsn (collision boxes)
                if line.startswith('Clsn') or line.startswith('clsn'):
                    # Format: Clsn2: N ou Clsn2[N]: x1,y1,x2,y2
                    # Vérifier qu'il y a bien le bon format
                    if ':' in line:
                        parts = line.split(':')
                        if len(parts) < 2:
                            return False, f"Ligne {i}: Format clsn invalide"

                        # Si c'est une définition de box, vérifier le format
                        if '[' in parts[0]:
                            values = parts[1].strip()
                            if values:  # Si ce n'est pas vide
                                coords = values.split(',')
                                if len(coords) != 4:
                                    return False, f"Ligne {i}: clsn doit avoir 4 coordonnées"

                                # Vérifier que ce sont des nombres
                                try:
                                    for coord in coords:
                                        int(coord.strip())
                                except ValueError:
                                    return False, f"Ligne {i}: coordonnées clsn invalides"

            return True, "OK"

        except Exception as e:
            return False, f"Erreur lecture: {e}"

    def scan_all_characters_air_files(self):
        """Scanne tous les fichiers .air des personnages"""
        self.log("Scan des fichiers .air...", "INFO")

        chars_path = self.base_path / "chars"
        if not chars_path.exists():
            return

        checked = 0
        broken = []

        for char_folder in sorted(chars_path.iterdir()):
            if not char_folder.is_dir():
                continue

            char_name = char_folder.name
            air_files = list(char_folder.glob('*.air'))

            if not air_files:
                continue

            # Vérifier chaque fichier .air
            for air_file in air_files:
                checked += 1
                is_valid, reason = self.check_air_file_syntax(air_file)

                if not is_valid:
                    broken.append((char_name, air_file.name, reason))
                    self.log(f"  ❌ {char_name}/{air_file.name}: {reason}", "ERROR")

        self.log(f"✅ {checked} fichiers .air vérifiés", "SUCCESS")
        self.log(f"❌ {len(broken)} fichiers avec erreurs", "ERROR")

        return broken

    def check_mugen_log_for_errors(self):
        """Lit mugen.log pour identifier les personnages problématiques"""
        self.log("Analyse mugen.log pour erreurs de chargement...", "INFO")

        mugen_log = self.base_path / "mugen.log"
        if not mugen_log.exists():
            self.log("mugen.log n'existe pas", "INFO")
            return []

        broken_chars = []

        try:
            content = mugen_log.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')

            for i, line in enumerate(lines):
                # Chercher les erreurs de chargement
                if 'Error loading chars/' in line:
                    # Extraire le nom du personnage
                    match = re.search(r'chars/([^/]+)/', line)
                    if match:
                        char_name = match.group(1)
                        if char_name not in broken_chars:
                            broken_chars.append(char_name)
                            self.log(f"  ❌ Trouvé erreur: {char_name}", "ERROR")

                # Chercher les erreurs .air spécifiques
                if 'Error in' in line and '.air' in line:
                    match = re.search(r'Error in ([^.]+)\.air', line)
                    if match:
                        char_name = match.group(1)
                        if char_name not in broken_chars:
                            broken_chars.append(char_name)
                            self.log(f"  ❌ Erreur .air: {char_name}", "ERROR")

        except Exception as e:
            self.log(f"Erreur lecture log: {e}", "ERROR")

        return broken_chars

    def disable_characters_in_select(self, char_names):
        """Désactive une liste de personnages dans select.def"""
        if not char_names:
            self.log("Aucun personnage à désactiver", "INFO")
            return

        self.log(f"Désactivation de {len(char_names)} personnages...", "FIX")

        # Backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = self.select_def.with_suffix(f'.def.backup_air_{timestamp}')
        shutil.copy2(self.select_def, backup)

        try:
            content = self.select_def.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            new_lines = []
            disabled = 0

            for line in lines:
                # Si c'est une ligne de personnage
                if line.strip() and not line.strip().startswith(';') and not line.strip().startswith('['):
                    # Vérifier si c'est un des personnages à désactiver
                    should_disable = False
                    for char_name in char_names:
                        if line.strip().startswith(char_name + ',') or line.strip().startswith(char_name + ' '):
                            should_disable = True
                            break

                    if should_disable:
                        new_lines.append(f"; {line}  ; AUTO-DISABLED: Erreur .air détectée")
                        disabled += 1
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)

            # Écrire
            self.select_def.write_text('\n'.join(new_lines), encoding='utf-8')
            self.log(f"✅ {disabled} personnages désactivés", "SUCCESS")

        except Exception as e:
            self.log(f"Erreur: {e}", "ERROR")

    def run_fix(self):
        """Lance la correction"""
        print("\n" + "="*80)
        print("  FIX AIR ERRORS - Désactivation personnages problématiques")
        print("="*80 + "\n")

        # 1. Analyser mugen.log
        self.log("=== ANALYSE MUGEN.LOG ===", "INFO")
        broken_from_log = self.check_mugen_log_for_errors()

        # 2. Scanner les fichiers .air (optionnel - peut être lent)
        # self.log("\n=== SCAN FICHIERS .AIR ===", "INFO")
        # broken_from_scan = self.scan_all_characters_air_files()

        # 3. Désactiver tous les personnages problématiques
        all_broken = list(set(broken_from_log))

        if all_broken:
            self.log("\n=== DÉSACTIVATION ===", "FIX")
            self.log(f"Personnages à désactiver: {', '.join(all_broken)}", "INFO")
            self.disable_characters_in_select(all_broken)

        # RÉSUMÉ
        print("\n" + "="*80)
        print("  RÉSUMÉ")
        print("="*80)
        print(f"❌ Personnages problématiques: {len(all_broken)}")

        if all_broken:
            print("\nPersonnages désactivés:")
            for char in all_broken:
                print(f"  • {char}")

        print("\n✅ Relancez le jeu pour vérifier")
        print("="*80 + "\n")

if __name__ == "__main__":
    fixer = AIRErrorFixer()
    fixer.run_fix()
