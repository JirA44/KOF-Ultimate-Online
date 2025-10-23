#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCAN AND FIX CLSN ERRORS
Trouve et désactive les personnages avec erreurs de collision boxes
"""

import re
from pathlib import Path
import shutil
from datetime import datetime

class CLSNErrorScanner:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.chars_path = self.base_path / "chars"
        self.broken_chars = []

    def log(self, message, level="INFO"):
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "FIX": "🔧"}
        print(f"{icons.get(level, '')} {message}")

    def check_air_clsn_consistency(self, air_file):
        """Vérifie la cohérence des CLSN dans un fichier .air"""
        try:
            content = air_file.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')

            current_action = None
            clsn1_declared = 0
            clsn2_declared = 0
            clsn1_defined = set()
            clsn2_defined = set()
            errors = []

            for i, line in enumerate(lines, 1):
                line_stripped = line.strip()

                # Ignorer commentaires
                if line_stripped.startswith(';') or not line_stripped:
                    continue

                # Nouvelle action
                if line_stripped.startswith('[Begin Action'):
                    # Vérifier l'action précédente
                    if current_action:
                        # Vérifier clsn1
                        if clsn1_declared > 0:
                            if len(clsn1_defined) != clsn1_declared:
                                errors.append(f"{current_action}: Clsn1 déclare {clsn1_declared} mais définit {clsn1_defined}")

                        # Vérifier clsn2
                        if clsn2_declared > 0:
                            if len(clsn2_defined) != clsn2_declared:
                                errors.append(f"{current_action}: Clsn2 déclare {clsn2_declared} mais définit {clsn2_defined}")

                    # Reset pour nouvelle action
                    current_action = line_stripped
                    clsn1_declared = 0
                    clsn2_declared = 0
                    clsn1_defined = set()
                    clsn2_defined = set()

                # Déclaration Clsn1: N
                elif re.match(r'^Clsn1:\s*(\d+)', line_stripped, re.IGNORECASE):
                    match = re.match(r'^Clsn1:\s*(\d+)', line_stripped, re.IGNORECASE)
                    clsn1_declared = int(match.group(1))

                # Déclaration Clsn2: N
                elif re.match(r'^Clsn2:\s*(\d+)', line_stripped, re.IGNORECASE):
                    match = re.match(r'^Clsn2:\s*(\d+)', line_stripped, re.IGNORECASE)
                    clsn2_declared = int(match.group(1))

                # Définition Clsn1[N]
                elif re.match(r'^Clsn1\[(\d+)\]', line_stripped, re.IGNORECASE):
                    match = re.match(r'^Clsn1\[(\d+)\]', line_stripped, re.IGNORECASE)
                    idx = int(match.group(1))
                    clsn1_defined.add(idx)

                # Définition Clsn2[N]
                elif re.match(r'^Clsn2\[(\d+)\]', line_stripped, re.IGNORECASE):
                    match = re.match(r'^Clsn2\[(\d+)\]', line_stripped, re.IGNORECASE)
                    idx = int(match.group(1))
                    clsn2_defined.add(idx)

            # Vérifier la dernière action
            if current_action:
                if clsn1_declared > 0 and len(clsn1_defined) != clsn1_declared:
                    errors.append(f"{current_action}: Clsn1 déclare {clsn1_declared} mais définit {clsn1_defined}")
                if clsn2_declared > 0 and len(clsn2_defined) != clsn2_declared:
                    errors.append(f"{current_action}: Clsn2 déclare {clsn2_declared} mais définit {clsn2_defined}")

            if errors:
                return False, errors
            return True, []

        except Exception as e:
            return False, [f"Erreur lecture: {e}"]

    def scan_all_characters(self):
        """Scanne tous les personnages"""
        self.log("Scan de tous les personnages pour erreurs CLSN...", "INFO")

        if not self.chars_path.exists():
            return []

        broken_chars = []
        checked = 0

        for char_folder in sorted(self.chars_path.iterdir()):
            if not char_folder.is_dir():
                continue

            char_name = char_folder.name
            air_files = list(char_folder.glob('*.air'))

            for air_file in air_files:
                checked += 1
                is_valid, errors = self.check_air_clsn_consistency(air_file)

                if not is_valid:
                    self.log(f"  ❌ {char_name}/{air_file.name}:", "ERROR")
                    for error in errors[:3]:  # Max 3 erreurs affichées
                        self.log(f"      {error}", "ERROR")
                    broken_chars.append(char_name)
                    break  # Une seule erreur suffit pour désactiver le perso

        self.log(f"✅ {checked} fichiers .air vérifiés", "SUCCESS")
        self.log(f"❌ {len(broken_chars)} personnages avec erreurs CLSN", "ERROR")

        return broken_chars

    def disable_broken_characters(self, broken_chars):
        """Désactive les personnages cassés dans select.def"""
        if not broken_chars:
            return

        select_def = self.base_path / "data" / "select.def"

        self.log(f"\nDésactivation de {len(broken_chars)} personnages...", "FIX")

        # Backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = select_def.with_suffix(f'.def.backup_clsn_{timestamp}')
        shutil.copy2(select_def, backup)

        try:
            content = select_def.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            new_lines = []
            disabled = 0

            for line in lines:
                should_disable = False

                # Si c'est une ligne de personnage non commentée
                if line.strip() and not line.strip().startswith(';') and not line.strip().startswith('['):
                    for char_name in broken_chars:
                        if line.strip().startswith(char_name + ',') or line.strip() == char_name:
                            should_disable = True
                            break

                if should_disable:
                    new_lines.append(f"; {line}  ; AUTO-DISABLED: Erreur CLSN dans .air")
                    disabled += 1
                else:
                    new_lines.append(line)

            select_def.write_text('\n'.join(new_lines), encoding='utf-8')
            self.log(f"✅ {disabled} personnages désactivés dans select.def", "SUCCESS")

        except Exception as e:
            self.log(f"Erreur: {e}", "ERROR")

    def run_scan(self):
        """Lance le scan complet"""
        print("\n" + "="*80)
        print("  SCAN CLSN ERRORS - Détection erreurs collision boxes")
        print("="*80 + "\n")

        # Scanner tous les personnages
        broken_chars = self.scan_all_characters()

        if broken_chars:
            self.log("\n📋 PERSONNAGES AVEC ERREURS:", "ERROR")
            for char in broken_chars[:20]:
                self.log(f"  • {char}", "ERROR")

            if len(broken_chars) > 20:
                self.log(f"  ... et {len(broken_chars) - 20} autres", "ERROR")

            # Désactiver
            self.disable_broken_characters(broken_chars)

        # RÉSUMÉ
        print("\n" + "="*80)
        print("  RÉSUMÉ")
        print("="*80)
        print(f"❌ Personnages problématiques: {len(broken_chars)}")
        print()

        if broken_chars:
            print("Ces personnages ont été désactivés dans select.def")
            print("Vous pouvez les réactiver après avoir corrigé leurs fichiers .air")
        else:
            print("✅ Tous les personnages actifs ont des fichiers .air valides!")

        print("="*80 + "\n")

if __name__ == "__main__":
    scanner = CLSNErrorScanner()
    scanner.run_scan()
