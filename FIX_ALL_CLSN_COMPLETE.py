#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - CORRECTEUR COMPLET CLSN
Détecte et corrige TOUS les problèmes Clsn dans les fichiers AIR
"""

import re
from pathlib import Path
from datetime import datetime
import shutil

game_dir = Path(r"D:\KOF Ultimate Online")
chars_dir = game_dir / "chars"

class CompleteClsnFixer:
    """Correcteur complet pour tous les problèmes Clsn"""

    def __init__(self):
        self.fixed_count = 0
        self.backup_dir = game_dir / "air_backups_complete" / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.errors_fixed = []

    def log(self, message, level='INFO'):
        """Log message"""
        symbols = {
            'INFO': 'ℹ️',
            'SUCCESS': '✅',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'FIX': '🔧'
        }
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {symbols.get(level, '•')} {message}")

    def backup_file(self, file_path):
        """Crée un backup"""
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = self.backup_dir / file_path.name
            shutil.copy2(file_path, backup_path)
            return True
        except Exception as e:
            self.log(f"Erreur backup: {e}", 'ERROR')
            return False

    def parse_actions(self, lines):
        """Parse le fichier AIR et extrait toutes les actions"""
        actions = []
        current_action = None

        for i, line in enumerate(lines):
            # Détecter [Begin Action X]
            match = re.match(r'^\s*\[Begin Action\s+(\d+)\]', line)
            if match:
                if current_action:
                    actions.append(current_action)

                current_action = {
                    'number': int(match.group(1)),
                    'start_line': i,
                    'lines': [line],
                    'clsn1_declared': None,
                    'clsn2_declared': None,
                    'clsn1_boxes': [],
                    'clsn2_boxes': []
                }
            elif current_action:
                current_action['lines'].append(line)

                # Détecter Clsn1: X
                match = re.match(r'^\s*Clsn1:\s*(\d+)', line)
                if match:
                    current_action['clsn1_declared'] = int(match.group(1))

                # Détecter Clsn2: X
                match = re.match(r'^\s*Clsn2:\s*(\d+)', line)
                if match:
                    current_action['clsn2_declared'] = int(match.group(1))

                # Détecter Clsn1[X]
                match = re.match(r'^\s*Clsn1\[(\d+)\]', line)
                if match:
                    current_action['clsn1_boxes'].append({
                        'index': int(match.group(1)),
                        'line': line
                    })

                # Détecter Clsn2[X]
                match = re.match(r'^\s*Clsn2\[(\d+)\]', line)
                if match:
                    current_action['clsn2_boxes'].append({
                        'index': int(match.group(1)),
                        'line': line
                    })

        if current_action:
            actions.append(current_action)

        return actions

    def fix_action_clsn(self, action):
        """Corrige les Clsn d'une action"""
        fixed_lines = []
        changes = []

        # Vérifier Clsn1
        if action['clsn1_boxes']:
            # Vérifier si déclaration manquante
            if action['clsn1_declared'] is None:
                # Ajouter déclaration après [Begin Action]
                fixed_lines.append(action['lines'][0])  # [Begin Action X]
                fixed_lines.append(f"Clsn1: {len(action['clsn1_boxes'])}\n")
                changes.append(f"Added Clsn1: {len(action['clsn1_boxes'])}")

                # Renuméroter les boxes à partir de 0
                box_index = 0
                for line in action['lines'][1:]:
                    if re.match(r'^\s*Clsn1\[\d+\]', line):
                        # Renuméroter
                        new_line = re.sub(r'Clsn1\[\d+\]', f'Clsn1[{box_index}]', line)
                        fixed_lines.append(new_line)
                        box_index += 1
                        changes.append(f"Renumbered Clsn1 box {box_index-1}")
                    else:
                        fixed_lines.append(line)
            else:
                # Vérifier si count correct
                if action['clsn1_declared'] != len(action['clsn1_boxes']):
                    # Corriger la déclaration
                    for line in action['lines']:
                        if re.match(r'^\s*Clsn1:\s*\d+', line):
                            fixed_lines.append(f"Clsn1: {len(action['clsn1_boxes'])}\n")
                            changes.append(f"Fixed Clsn1 count: {action['clsn1_declared']} -> {len(action['clsn1_boxes'])}")
                        else:
                            fixed_lines.append(line)
                else:
                    fixed_lines = action['lines']
        else:
            fixed_lines = action['lines']

        # Vérifier Clsn2 (même logique)
        if action['clsn2_boxes']:
            temp_lines = fixed_lines
            fixed_lines = []

            if action['clsn2_declared'] is None:
                # Ajouter déclaration
                first_clsn2_found = False
                box_index = 0

                for line in temp_lines:
                    if re.match(r'^\s*Clsn2\[\d+\]', line) and not first_clsn2_found:
                        # Insérer déclaration avant la première box
                        fixed_lines.append(f"Clsn2: {len(action['clsn2_boxes'])}\n")
                        changes.append(f"Added Clsn2: {len(action['clsn2_boxes'])}")
                        first_clsn2_found = True

                    if re.match(r'^\s*Clsn2\[\d+\]', line):
                        # Renuméroter
                        new_line = re.sub(r'Clsn2\[\d+\]', f'Clsn2[{box_index}]', line)
                        fixed_lines.append(new_line)
                        box_index += 1
                    else:
                        fixed_lines.append(line)
            elif action['clsn2_declared'] != len(action['clsn2_boxes']):
                # Corriger count
                for line in temp_lines:
                    if re.match(r'^\s*Clsn2:\s*\d+', line):
                        fixed_lines.append(f"Clsn2: {len(action['clsn2_boxes'])}\n")
                        changes.append(f"Fixed Clsn2 count: {action['clsn2_declared']} -> {len(action['clsn2_boxes'])}")
                    else:
                        fixed_lines.append(line)
            else:
                fixed_lines = temp_lines

        return fixed_lines, changes

    def fix_air_file(self, air_path):
        """Corrige un fichier AIR complet"""
        try:
            with open(air_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Parser les actions
            actions = self.parse_actions(lines)

            # Corriger chaque action
            all_changes = []
            fixed_actions = []

            for action in actions:
                fixed_lines, changes = self.fix_action_clsn(action)
                fixed_actions.append(fixed_lines)
                if changes:
                    all_changes.extend([f"Action {action['number']}: {c}" for c in changes])

            if all_changes:
                # Backup
                self.backup_file(air_path)

                # Reconstruire le fichier
                output_lines = []
                action_idx = 0
                in_action = False

                for line in lines:
                    if re.match(r'^\s*\[Begin Action\s+\d+\]', line):
                        # Nouvelle action
                        if action_idx < len(fixed_actions):
                            output_lines.extend(fixed_actions[action_idx])
                            action_idx += 1
                            in_action = True
                    elif not in_action:
                        # Lignes avant première action
                        output_lines.append(line)

                # Sauvegarder
                with open(air_path, 'w', encoding='utf-8') as f:
                    f.writelines(output_lines)

                self.fixed_count += 1
                self.errors_fixed.append({
                    'file': air_path.name,
                    'changes': all_changes
                })

                return True, all_changes

            return False, []

        except Exception as e:
            self.log(f"Erreur: {e}", 'ERROR')
            return False, []

    def fix_all_air_files(self):
        """Corrige tous les fichiers AIR"""
        print()
        print("=" * 70)
        print("  🔧 CORRECTEUR COMPLET CLSN")
        print("=" * 70)
        print()

        # Trouver tous les fichiers AIR
        air_files = list(chars_dir.rglob("*.air"))
        self.log(f"Trouvé {len(air_files)} fichiers AIR")
        print()

        # Corriger chaque fichier
        for air_file in air_files:
            fixed, changes = self.fix_air_file(air_file)
            if fixed:
                rel_path = air_file.relative_to(chars_dir)
                self.log(f"✓ {rel_path}", 'FIX')
                for change in changes[:3]:  # Afficher max 3 changements
                    print(f"     • {change}")
                if len(changes) > 3:
                    print(f"     • ... et {len(changes) - 3} autres")

        print()
        print("=" * 70)
        print("📊 RAPPORT FINAL")
        print("=" * 70)
        print(f"Fichiers scannés:  {len(air_files)}")
        print(f"Fichiers corrigés: {self.fixed_count}")
        print()

        if self.fixed_count > 0:
            print(f"💾 Backups sauvegardés dans:")
            print(f"   {self.backup_dir}")

        print("=" * 70)
        print()

def main():
    """Main function"""
    print()
    print("=" * 70)
    print("  🔧 KOF ULTIMATE - CORRECTEUR COMPLET CLSN")
    print("=" * 70)
    print()

    fixer = CompleteClsnFixer()
    fixer.fix_all_air_files()

    print()
    try:
        input("Appuyez sur ENTRÉE pour fermer...")
    except EOFError:
        pass

if __name__ == '__main__':
    main()
