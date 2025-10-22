#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTO FIX VISUAL BUGS - Correction automatique des bugs visuels
"""

import os
import sys
import re
import shutil
from pathlib import Path
from datetime import datetime

class VisualBugFixer:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.chars_path = self.base_path / "chars"
        self.stages_path = self.base_path / "stages"
        self.data_path = self.base_path / "data"
        self.select_def = self.data_path / "select.def"

        # Personnages et stages problématiques identifiés
        self.broken_chars = [
            "Akari", "Alou_AKOF", "baiyi", "bob", "cciking",
            "D.Yashiro.Rhythm(Dusk)1.x", "D_DisciplineGirl", "Error Zero",
            "Graves", "Kei", "Kevenoce", "Maltet", "Nao-MX 1.0",
            "Rozwel S.K (LEGIT)", "Rugal7th", "Ryuji", "Shadow-Dancer",
            "Tenrou_Kunagi", "Wild.O.Yashiro", "Lane.Blood-CKOFM"
        ]

        self.broken_stages = [
            "Anime Blu", "Basque Palace", "BLACK SON DROTIME", "Black wall",
            "clones lab destroyed", "DARK SAID RUGAL S  ", "DROBLOOD R 2.0",
            "Exagon Force", "Far from here", "forest infernal fire",
            "Galaxy BG", "light kyouki", "Moon of dark wall",
            "Moon recidence", "O.DB DRORANGE BLACK", "Palece Mistery R",
            "The Will Of Hades S  ", "TIME INGCODNITA", "Wall of paintings"
        ]

    def log(self, message, level="INFO"):
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✓",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "FIX": "🔧"
        }
        print(f"{icons.get(level, '')} {message}")

    def fix_select_def(self):
        """Désactive les personnages problématiques dans select.def"""
        self.log("Correction du select.def...", "INFO")

        if not self.select_def.exists():
            self.log("select.def non trouvé!", "ERROR")
            return False

        # Backup
        backup_file = self.select_def.with_suffix(f'.def.visualfix_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        shutil.copy2(self.select_def, backup_file)
        self.log(f"Backup: {backup_file.name}", "SUCCESS")

        # Lire et modifier
        content = self.select_def.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')
        fixed_count = 0

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            # Vérifier si c'est une ligne de personnage
            if line_stripped and not line_stripped.startswith(';') and not line_stripped.startswith('['):
                char_name = line_stripped.split(',')[0].strip()

                # Si c'est un personnage problématique, le commenter
                for broken_char in self.broken_chars:
                    if broken_char.lower() in char_name.lower():
                        if not line.startswith(';'):
                            lines[i] = f';FIXED_MISSING_FILES: {line}'
                            fixed_count += 1
                            self.log(f"Désactivé: {char_name}", "FIX")
                        break

        # Sauvegarder
        content = '\n'.join(lines)
        self.select_def.write_text(content, encoding='utf-8')

        self.log(f"{fixed_count} personnages désactivés", "SUCCESS")
        return True

    def clean_stages_list(self):
        """Nettoie la liste des stages dans select.def"""
        self.log("Nettoyage de la liste des stages...", "INFO")

        if not self.select_def.exists():
            return False

        content = self.select_def.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')
        fixed_count = 0
        in_extrastages = False

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            if line_stripped == '[ExtraStages]':
                in_extrastages = True
                continue
            elif line_stripped.startswith('['):
                in_extrastages = False
                continue

            if in_extrastages and line_stripped and not line_stripped.startswith(';'):
                # Extraire le nom du stage (avant .def)
                stage_ref = line_stripped.split('.def')[0].strip()
                stage_name = stage_ref.replace('stages/', '').strip()

                # Vérifier si c'est un stage problématique
                for broken_stage in self.broken_stages:
                    if broken_stage.lower() in stage_name.lower():
                        if not line.startswith(';'):
                            lines[i] = f';FIXED_MISSING_SFF: {line}'
                            fixed_count += 1
                            self.log(f"Stage désactivé: {stage_name}", "FIX")
                        break

        # Sauvegarder
        content = '\n'.join(lines)
        self.select_def.write_text(content, encoding='utf-8')

        self.log(f"{fixed_count} stages désactivés", "SUCCESS")
        return True

    def verify_fixes(self):
        """Vérifie que les corrections ont été appliquées"""
        self.log("Vérification des corrections...", "INFO")

        content = self.select_def.read_text(encoding='utf-8', errors='ignore')

        # Compter les lignes FIXED
        fixed_chars = content.count(';FIXED_MISSING_FILES:')
        fixed_stages = content.count(';FIXED_MISSING_SFF:')

        self.log(f"Personnages corrigés: {fixed_chars}", "INFO")
        self.log(f"Stages corrigés: {fixed_stages}", "INFO")

        return True

    def run(self):
        """Exécute toutes les corrections"""
        print("\n" + "="*70)
        print("  🔧 AUTO FIX VISUAL BUGS - KOF ULTIMATE")
        print("="*70 + "\n")

        self.fix_select_def()
        print()
        self.clean_stages_list()
        print()
        self.verify_fixes()

        print("\n" + "="*70)
        print("  ✓ CORRECTIONS APPLIQUÉES!")
        print("="*70 + "\n")
        print("Les personnages et stages problématiques ont été désactivés.")
        print("Le jeu devrait maintenant s'afficher correctement.")
        print("\nTestez le jeu pour vérifier!")

        return True

if __name__ == "__main__":
    fixer = VisualBugFixer()
    fixer.run()
