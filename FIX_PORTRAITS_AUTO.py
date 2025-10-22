#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIX PORTRAITS AUTO - Correction automatique des portraits
"""

import os
import sys
import re
import shutil
from pathlib import Path
from datetime import datetime

class PortraitFixer:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.system_def = self.base_path / "data" / "system.def"

    def log(self, message):
        print(f"✓ {message}")

    def fix_portraits(self):
        """Applique les corrections optimales"""

        if not self.system_def.exists():
            print(f"❌ Fichier system.def non trouvé: {self.system_def}")
            return False

        # Backup
        backup_file = self.system_def.with_suffix(f'.def.portrait_fix_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        shutil.copy2(self.system_def, backup_file)
        self.log(f"Backup créé: {backup_file.name}")

        # Lire le fichier
        content = self.system_def.read_text(encoding='utf-8', errors='ignore')

        # Configuration optimale
        # Cellules de 32x32 px (plus grande que 27x27)
        # Échelle de 0.32 pour portraits 100x100px

        fixes = {
            'cell.size': '32,32',           # Cellules plus grandes
            'cell.spacing': '2',            # Espacement correct
            'portrait.scale': '0.32,0.32',  # Échelle proportionnelle
            'portrait.offset': '0,0',       # Centré
        }

        # Appliquer les corrections dans la section [Select Info]
        lines = content.split('\n')
        in_select_info = False
        modified = False

        for i, line in enumerate(lines):
            if line.strip() == '[Select Info]':
                in_select_info = True
                continue
            elif line.strip().startswith('[') and in_select_info:
                in_select_info = False
                continue

            if in_select_info:
                for key, value in fixes.items():
                    pattern = key.replace('.', r'\.')
                    if re.match(rf'{pattern}\s*=', line):
                        lines[i] = f'{key} = {value}'
                        self.log(f"Modifié: {key} = {value}")
                        modified = True

        if modified:
            # Sauvegarder
            content = '\n'.join(lines)
            self.system_def.write_text(content, encoding='utf-8')
            self.log("Modifications sauvegardées!")
            return True
        else:
            print("⚠️ Aucune modification appliquée")
            return False

    def run(self):
        """Exécute la correction"""
        print("\n" + "="*70)
        print("  🎨 FIX PORTRAITS AUTO - KOF ULTIMATE")
        print("="*70 + "\n")

        success = self.fix_portraits()

        if success:
            print("\n" + "="*70)
            print("  ✓ CORRECTIONS APPLIQUÉES AVEC SUCCÈS!")
            print("="*70 + "\n")
            print("Les portraits devraient maintenant s'afficher correctement.")
            print("Lancez le jeu pour tester!")

        return success

if __name__ == "__main__":
    fixer = PortraitFixer()
    fixer.run()
