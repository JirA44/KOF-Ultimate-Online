#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - CORRECTEUR AVANCÉ DES FICHIERS AIR
Corrige TOUS les types d'erreurs AIR incluant:
- Clsn count mismatches
- Clsn2Default conflicts
- Literal \\n
- Missing Clsn declarations
"""

import re
from pathlib import Path
from datetime import datetime

game_dir = Path(r"D:\KOF Ultimate Online Online Online")
chars_dir = game_dir / "chars"

class AdvancedAIRFixer:
    """Correcteur avancé de fichiers AIR"""

    def __init__(self):
        self.fixed_count = 0
        self.error_count = 0
        self.backup_dir = game_dir / "air_backups_advanced" / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.fixes_applied = []

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
        """Corrige un fichier AIR avec toutes les règles"""
        try:
            with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')

            changes_made = False
            fixes_for_file = []

            # FIX 1: Supprimer les literal \\n
            if r'\n' in content and '; ' not in content[:content.find(r'\n')]:
                content = content.replace(r'\n', '\n')
                changes_made = True
                fixes_for_file.append("Removed literal \\n")

            # Reparser les lignes
            lines = content.split('\n')
            fixed_lines = []
            in_action = False
            action_num = None
            action_start_idx = 0
            has_clsn_default = False
            clsn1_declared = 0
            clsn2_declared = 0
            clsn1_boxes = []
            clsn2_boxes = []

            i = 0
            while i < len(lines):
                line = lines[i]

                # Détection début d'action
                match = re.match(r'^\[Begin Action (\d+)\]', line, re.IGNORECASE)
                if match:
                    # Corriger l'action précédente si nécessaire
                    if in_action:
                        if clsn1_declared != len(clsn1_boxes) or clsn2_declared != len(clsn2_boxes):
                            # Corriger les déclarations
                            for j in range(action_start_idx, len(fixed_lines)):
                                if re.match(r'^\s*Clsn1:\s*\d+', fixed_lines[j]):
                                    fixed_lines[j] = f"Clsn1: {len(clsn1_boxes)}"
                                    changes_made = True
                                    if f"Action {action_num} Clsn1 fixed" not in fixes_for_file:
                                        fixes_for_file.append(f"Action {action_num} Clsn1 fixed")
                                elif re.match(r'^\s*Clsn2:\s*\d+', fixed_lines[j]):
                                    fixed_lines[j] = f"Clsn2: {len(clsn2_boxes)}"
                                    changes_made = True
                                    if f"Action {action_num} Clsn2 fixed" not in fixes_for_file:
                                        fixes_for_file.append(f"Action {action_num} Clsn2 fixed")

                    # Nouvelle action
                    in_action = True
                    action_num = int(match.group(1))
                    action_start_idx = len(fixed_lines)
                    has_clsn_default = False
                    clsn1_declared = 0
                    clsn2_declared = 0
                    clsn1_boxes = []
                    clsn2_boxes = []
                    fixed_lines.append(line)
                    i += 1
                    continue

                # FIX 2: Détecter Clsn2Default (conflit avec Clsn2)
                if re.match(r'^\s*Clsn2Default:\s*\d+', line, re.IGNORECASE):
                    has_clsn_default = True
                    # NE PAS ajouter cette ligne si on a déjà un Clsn2 dans l'action
                    # On va vérifier les lignes suivantes
                    next_lines_preview = '\n'.join(lines[i:min(i+10, len(lines))])
                    if re.search(r'^\s*Clsn2:\s*\d+', next_lines_preview, re.MULTILINE):
                        # Il y a un Clsn2 après, donc skip le Default
                        changes_made = True
                        fixes_for_file.append(f"Action {action_num} removed Clsn2Default")
                        i += 1
                        continue
                    else:
                        fixed_lines.append(line)
                        i += 1
                        continue

                # FIX 3: Détecter Clsn1Default
                if re.match(r'^\s*Clsn1Default:\s*\d+', line, re.IGNORECASE):
                    next_lines_preview = '\n'.join(lines[i:min(i+10, len(lines))])
                    if re.search(r'^\s*Clsn1:\s*\d+', next_lines_preview, re.MULTILINE):
                        changes_made = True
                        fixes_for_file.append(f"Action {action_num} removed Clsn1Default")
                        i += 1
                        continue
                    else:
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
            if in_action:
                if clsn1_declared != len(clsn1_boxes) or clsn2_declared != len(clsn2_boxes):
                    for j in range(action_start_idx, len(fixed_lines)):
                        if re.match(r'^\s*Clsn1:\s*\d+', fixed_lines[j]):
                            fixed_lines[j] = f"Clsn1: {len(clsn1_boxes)}"
                            changes_made = True
                            if f"Action {action_num} Clsn1 fixed" not in fixes_for_file:
                                fixes_for_file.append(f"Action {action_num} Clsn1 fixed")
                        elif re.match(r'^\s*Clsn2:\s*\d+', fixed_lines[j]):
                            fixed_lines[j] = f"Clsn2: {len(clsn2_boxes)}"
                            changes_made = True
                            if f"Action {action_num} Clsn2 fixed" not in fixes_for_file:
                                fixes_for_file.append(f"Action {action_num} Clsn2 fixed")

            # Sauvegarder si des changements ont été faits
            if changes_made:
                # Backup d'abord
                if self.backup_file(air_file):
                    with open(air_file, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(fixed_lines))
                    self.fixed_count += 1
                    self.fixes_applied.append({
                        'file': air_file.relative_to(chars_dir),
                        'fixes': fixes_for_file
                    })
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
        print("  🔧 CORRECTION AVANCÉE DES FICHIERS AIR")
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
        print()

        if self.fixes_applied:
            print("🔧 DÉTAILS DES CORRECTIONS:")
            print()
            for fix_info in self.fixes_applied[:20]:
                print(f"  📄 {fix_info['file']}")
                for fix in fix_info['fixes'][:3]:
                    print(f"     • {fix}")
            if len(self.fixes_applied) > 20:
                print(f"\n  ... et {len(self.fixes_applied) - 20} autres fichiers")

        print()
        print(f"✅ Backups sauvegardés dans:")
        print(f"   {self.backup_dir}")
        print("=" * 70)
        print()

def main():
    """Main function"""
    fixer = AdvancedAIRFixer()
    fixer.fix_all()

    print()
    try:
        input("Appuyez sur ENTRÉE pour fermer...")
    except EOFError:
        pass

if __name__ == '__main__':
    main()
