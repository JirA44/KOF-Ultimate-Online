#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - CORRECTEUR AUTOMATIQUE DES FICHIERS AIR
Corrige automatiquement les problèmes de Clsn dans tous les fichiers AIR
"""

import re
from pathlib import Path
from datetime import datetime

game_dir = Path(r"D:\KOF Ultimate Online")
chars_dir = game_dir / "chars"

class AIRFixer:
    """Correcteur de fichiers AIR"""

    def __init__(self):
        self.fixed_count = 0
        self.error_count = 0
        self.backup_dir = game_dir / "air_backups" / datetime.now().strftime("%Y%m%d_%H%M%S")

    def log(self, message, level='INFO'):
        """Log message"""
        symbols = {
            'INFO': 'ℹ️',
            'SUCCESS': '✅',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'FIX': '🔧'
        }
        print(f"{symbols.get(level, '•')} {message}")

    def backup_file(self, air_file):
        """Sauvegarde le fichier avant modification"""
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = self.backup_dir / air_file.relative_to(chars_dir)
            backup_path.parent.mkdir(parents=True, exist_ok=True)

            with open(air_file, 'rb') as src:
                backup_path.write_bytes(src.read())

            return True
        except Exception as e:
            self.log(f"Erreur backup {air_file.name}: {e}", 'ERROR')
            return False

    def fix_air_file(self, air_file):
        """Corrige un fichier AIR"""
        try:
            with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            fixed_lines = []
            in_action = False
            clsn1_declared = 0
            clsn2_declared = 0
            clsn1_boxes = []
            clsn2_boxes = []
            action_start_idx = 0
            action_num = None
            changes_made = False

            i = 0
            while i < len(lines):
                line = lines[i]

                # Détection début d'action
                match = re.match(r'^\[Begin Action (\d+)\]', line, re.IGNORECASE)
                if match:
                    # Corriger l'action précédente si nécessaire
                    if in_action and (clsn1_declared != len(clsn1_boxes) or clsn2_declared != len(clsn2_boxes)):
                        # Corriger les déclarations
                        for j in range(action_start_idx, i):
                            if re.match(r'^\s*Clsn1:\s*\d+', fixed_lines[j]):
                                fixed_lines[j] = f"Clsn1: {len(clsn1_boxes)}\n"
                                changes_made = True
                            elif re.match(r'^\s*Clsn2:\s*\d+', fixed_lines[j]):
                                fixed_lines[j] = f"Clsn2: {len(clsn2_boxes)}\n"
                                changes_made = True

                    # Nouvelle action
                    in_action = True
                    action_num = int(match.group(1))
                    action_start_idx = len(fixed_lines)
                    clsn1_declared = 0
                    clsn2_declared = 0
                    clsn1_boxes = []
                    clsn2_boxes = []
                    fixed_lines.append(line)
                    i += 1
                    continue

                # Compter Clsn déclarés
                match = re.match(r'^\s*Clsn1:\s*(\d+)', line)
                if match:
                    clsn1_declared = int(match.group(1))
                    fixed_lines.append(line)
                    i += 1
                    continue

                match = re.match(r'^\s*Clsn2:\s*(\d+)', line)
                if match:
                    clsn2_declared = int(match.group(1))
                    fixed_lines.append(line)
                    i += 1
                    continue

                # Compter les boxes Clsn
                if re.match(r'^\s*Clsn1\[\d+\]', line):
                    clsn1_boxes.append(line)
                elif re.match(r'^\s*Clsn2\[\d+\]', line):
                    clsn2_boxes.append(line)

                fixed_lines.append(line)
                i += 1

            # Corriger la dernière action
            if in_action and (clsn1_declared != len(clsn1_boxes) or clsn2_declared != len(clsn2_boxes)):
                for j in range(action_start_idx, len(fixed_lines)):
                    if re.match(r'^\s*Clsn1:\s*\d+', fixed_lines[j]):
                        fixed_lines[j] = f"Clsn1: {len(clsn1_boxes)}\n"
                        changes_made = True
                    elif re.match(r'^\s*Clsn2:\s*\d+', fixed_lines[j]):
                        fixed_lines[j] = f"Clsn2: {len(clsn2_boxes)}\n"
                        changes_made = True

            # Sauvegarder si des changements ont été faits
            if changes_made:
                # Backup d'abord
                if self.backup_file(air_file):
                    with open(air_file, 'w', encoding='utf-8') as f:
                        f.writelines(fixed_lines)
                    self.fixed_count += 1
                    return True

            return False

        except Exception as e:
            self.log(f"Erreur lors de la correction de {air_file.name}: {e}", 'ERROR')
            self.error_count += 1
            return False

    def fix_all(self):
        """Corrige tous les fichiers AIR"""
        print()
        print("=" * 70)
        print("  🔧 CORRECTION AUTOMATIQUE DES FICHIERS AIR")
        print("=" * 70)
        print()

        air_files = list(chars_dir.rglob("*.air"))
        self.log(f"Trouvé {len(air_files)} fichiers AIR")
        print()

        self.log(f"Les backups seront sauvegardés dans:", 'INFO')
        self.log(f"  {self.backup_dir}", 'INFO')
        print()

        for air_file in air_files:
            rel_path = air_file.relative_to(chars_dir)
            if self.fix_air_file(air_file):
                self.log(f"✓ Corrigé: {rel_path}", 'FIX')

        print()
        print("=" * 70)
        print("📊 RAPPORT FINAL")
        print("=" * 70)
        print(f"Fichiers scannés:  {len(air_files)}")
        print(f"Fichiers corrigés: {self.fixed_count}")
        print(f"Erreurs:           {self.error_count}")
        print(f"")
        print(f"✅ Backups sauvegardés dans:")
        print(f"   {self.backup_dir}")
        print("=" * 70)
        print()

def main():
    """Main function"""
    fixer = AIRFixer()
    fixer.fix_all()

    print()
    input("Appuyez sur ENTRÉE pour fermer...")

if __name__ == '__main__':
    main()
