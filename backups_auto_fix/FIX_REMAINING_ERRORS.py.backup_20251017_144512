#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - CORRECTEUR ERREURS RESTANTES
Corrige les patterns spécifiques non détectés par le scanner universel
"""

import re
from pathlib import Path
import shutil
from datetime import datetime

class RemainingErrorsFixer:
    """Correcteur d'erreurs spécifiques restantes"""

    def __init__(self):
        self.game_dir = Path(r"D:\KOF Ultimate Online")
        self.chars_dir = self.game_dir / "chars"
        self.backup_dir = self.game_dir / "backups_remaining_fixes"
        self.backup_dir.mkdir(exist_ok=True)

        self.fixes_applied = []

    def log(self, message, level='INFO'):
        """Log un message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def backup_file(self, filepath):
        """Backup avant modification"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{filepath.name}.remaining_{timestamp}"
            backup_path = self.backup_dir / backup_name
            shutil.copy2(filepath, backup_path)
            return True
        except:
            return False

    def fix_air_file_advanced(self, air_file):
        """Corrige patterns complexes dans fichiers .air"""
        try:
            with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            fixed_lines = []
            modified = False

            for i, line in enumerate(lines):
                # PATTERN 1: Clsn[X] = ... Clsn2: Y sur même ligne
                # Ex: Clsn2[0] = 7,-84, 35,-42 Clsn2: 1
                match = re.match(r'^(\s*Clsn[12]\[\d+\]\s*=\s*-?\d+\s*,\s*-?\d+\s*,\s*-?\d+\s*,\s*-?\d+)\s+(Clsn[12]:.+)$', line)
                if match:
                    clsn_part = match.group(1)
                    extra_part = match.group(2)
                    fixed_lines.append(clsn_part + '\n')
                    fixed_lines.append(extra_part + '\n')
                    modified = True
                    self.log(f"  {air_file.name}:{i+1} - Séparé Clsn + Clsn2:")
                    continue

                # PATTERN 2: Clsn1[X] = ... Clsn2: Y sur même ligne
                # Ex: Clsn1[0] = 28,-69, 94,-49 Clsn2: 3
                match = re.match(r'^(\s*Clsn[12]\[\d+\]\s*=\s*-?\d+\s*,\s*-?\d+\s*,\s*-?\d+\s*,\s*-?\d+)\s+(Clsn[12]:?\s*\d+)$', line)
                if match:
                    clsn_part = match.group(1)
                    extra_part = match.group(2)
                    fixed_lines.append(clsn_part + '\n')
                    fixed_lines.append(extra_part + '\n')
                    modified = True
                    self.log(f"  {air_file.name}:{i+1} - Séparé Clsn + compteur")
                    continue

                # PATTERN 3: Espaces autour des virgules dans Clsn
                if 'Clsn' in line and '=' in line:
                    # Normaliser espaces: -5, -114, 19, -90
                    fixed_line = re.sub(r'\s*,\s*', ', ', line)
                    if fixed_line != line:
                        line = fixed_line
                        modified = True

                fixed_lines.append(line)

            if modified:
                self.backup_file(air_file)
                with open(air_file, 'w', encoding='utf-8') as f:
                    f.writelines(fixed_lines)

                self.fixes_applied.append(f"Corrigé {air_file.name}")
                return True

            return False

        except Exception as e:
            self.log(f"Erreur {air_file.name}: {e}", 'ERROR')
            return False

    def fix_specific_files(self):
        """Corrige les fichiers spécifiques signalés"""
        self.log("\n" + "=" * 70)
        self.log("🔧 CORRECTEUR ERREURS RESTANTES")
        self.log("=" * 70)

        # Fichiers signalés avec erreurs
        problem_files = [
            "Akari/akari.air",
            "Kychiel/Kychiel.air"
        ]

        fixed_count = 0

        for file_path in problem_files:
            full_path = self.chars_dir / file_path
            if full_path.exists():
                self.log(f"\n🔍 Correction de {file_path}...")
                if self.fix_air_file_advanced(full_path):
                    fixed_count += 1
                    self.log(f"  ✅ {file_path} corrigé")
                else:
                    self.log(f"  ⚠️  Aucune modification nécessaire")
            else:
                self.log(f"  ❌ Fichier introuvable: {file_path}")

        # Scanner TOUS les .air pour ce pattern
        self.log(f"\n🔍 Scan de tous les .air pour patterns similaires...")
        air_files = list(self.chars_dir.rglob("*.air"))

        for air_file in air_files:
            # Skip déjà traités
            if any(str(air_file).endswith(pf) for pf in problem_files):
                continue

            if self.fix_air_file_advanced(air_file):
                fixed_count += 1
                self.log(f"  ✅ {air_file.parent.name}/{air_file.name}")

        # Rapport
        self.log("\n" + "=" * 70)
        self.log("📊 RAPPORT FINAL")
        self.log("=" * 70)

        if self.fixes_applied:
            self.log(f"\n✅ {len(self.fixes_applied)} fichiers corrigés")
            self.log(f"💾 Backups: {self.backup_dir}")
        else:
            self.log("\n✓ Aucune erreur trouvée")

        self.log("=" * 70)

        return len(self.fixes_applied) > 0

def main():
    """Point d'entrée"""
    print("\n" + "=" * 70)
    print("  🔧 CORRECTEUR ERREURS RESTANTES")
    print("=" * 70)
    print("\n  Corrige:")
    print("  • akari.air:561 - Clsn + Clsn2: sur même ligne")
    print("  • Kychiel.air:8 - Clsn + Clsn2: sur même ligne")
    print("  • Tous patterns similaires")
    print("\n" + "=" * 70)
    print()

    fixer = RemainingErrorsFixer()
    success = fixer.fix_specific_files()

    print("\n\n" + "=" * 70)
    if success:
        print("✅ CORRECTIONS APPLIQUÉES!")
        print("\nRelancez le jeu pour vérifier.")
    else:
        print("✓ AUCUNE ERREUR TROUVÉE")
    print("=" * 70)
    print()

if __name__ == '__main__':
    main()
