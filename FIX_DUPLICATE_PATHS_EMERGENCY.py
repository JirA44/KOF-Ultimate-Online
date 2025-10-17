#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - CORRECTEUR D'URGENCE CHEMINS DUPLIQUÉS
Corrige le problème de chemins répétés créés par le correcteur automatique
"""

import re
from pathlib import Path
import shutil
from datetime import datetime

class EmergencyPathFixer:
    """Correcteur d'urgence pour les chemins dupliqués"""

    def __init__(self):
        self.game_dir = Path(__file__).parent
        self.correct_path = r"D:\KOF Ultimate Online Online Online Online"
        self.backup_dir = self.game_dir / "backups_emergency"
        self.backup_dir.mkdir(exist_ok=True)
        self.files_fixed = 0

    def log(self, message):
        """Log un message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def backup_file(self, filepath):
        """Sauvegarde avant modification"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{filepath.name}.emergency_backup_{timestamp}"
            backup_path = self.backup_dir / backup_name
            shutil.copy2(filepath, backup_path)
            return True
        except Exception as e:
            self.log(f"⚠️  Erreur backup: {e}")
            return False

    def fix_duplicate_paths_in_file(self, filepath):
        """Corrige les chemins dupliqués dans un fichier"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            original_content = content

            # Pattern pour détecter les chemins dupliqués
            # Match: D:\KOF Ultimate Online Online Online Online...
            pattern = r'D:\\KOF Ultimate(?:( Online)+)'

            def replace_func(match):
                # Remplacer par le chemin correct une seule fois
                return r'D:\KOF Ultimate Online Online Online Online'

            # Remplacer tous les chemins dupliqués
            content = re.sub(pattern, replace_func, content)

            # Même chose pour les chemins avec /
            pattern_slash = r'D:/KOF Ultimate(?:( Online)+)'
            content = re.sub(pattern_slash, lambda m: 'D:/KOF Ultimate Online', content)

            # Si le contenu a changé, sauvegarder
            if content != original_content:
                self.backup_file(filepath)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

                self.log(f"✅ {filepath.name}: Corrigé!")
                self.files_fixed += 1
                return True

            return False

        except Exception as e:
            self.log(f"❌ Erreur avec {filepath.name}: {e}")
            return False

    def fix_all_python_files(self):
        """Corrige tous les fichiers Python"""
        self.log("\n🚨 CORRECTION D'URGENCE - CHEMINS DUPLIQUÉS")
        self.log("=" * 70)

        python_files = list(self.game_dir.glob("*.py"))

        self.log(f"\n📁 Scan de {len(python_files)} fichiers...")
        self.log("")

        for py_file in python_files:
            self.fix_duplicate_paths_in_file(py_file)

        self.log("\n" + "=" * 70)
        self.log(f"📊 RÉSULTAT: {self.files_fixed} fichier(s) corrigé(s)")
        self.log(f"💾 Backups dans: {self.backup_dir}")
        self.log("=" * 70)

        if self.files_fixed > 0:
            self.log("\n✅ CORRECTION D'URGENCE TERMINÉE!")
        else:
            self.log("\n✅ Aucune correction nécessaire - Tout est OK!")

def main():
    """Point d'entrée"""
    print("\n" + "=" * 70)
    print("  🚨 CORRECTEUR D'URGENCE - CHEMINS DUPLIQUÉS")
    print("=" * 70)
    print("\n  Correction des chemins répétés type:")
    print("  'D:\\KOF Ultimate Online Online Online...' → 'D:\\KOF Ultimate Online'")
    print("\n" + "=" * 70)
    print()

    fixer = EmergencyPathFixer()
    fixer.fix_all_python_files()

    print()

if __name__ == '__main__':
    main()
