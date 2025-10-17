#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIX MISSING SFF PATHS - KOF ULTIMATE
Trouve et corrige les chemins SFF incorrects dans les fichiers .def des personnages
"""

import os
import sys
import shutil
import re
from pathlib import Path
from datetime import datetime

class SFFPathFixer:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.chars_path = self.base_path / "chars"

        self.broken_chars = [
            "Akari", "Alou_AKOF", "D.Yashiro.Rhythm(Dusk)1.x", "D_DisciplineGirl",
            "Error Zero", "Graves", "Kei", "Kevenoce", "Maltet", "Nao-MX 1.0",
            "Rozwel S.K (LEGIT)", "Rugal7th", "Ryuji", "Shadow-Dancer",
            "Tenrou_Kunagi", "Wild.O.Yashiro", "baiyi", "bob", "cciking", "kfm"
        ]

    def log(self, message, level="INFO"):
        """Affiche un message avec niveau"""
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✓",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "FIX": "🔧"
        }
        icon = icons.get(level, "•")
        print(f"{icon} {message}")

    def find_sff_file(self, char_folder):
        """Trouve le fichier SFF dans le dossier du personnage"""
        # Chercher tous les fichiers .sff
        sff_files = list(char_folder.glob("**/*.sff"))

        if not sff_files:
            return None

        # Préférer les SFF à la racine
        root_sff = [f for f in sff_files if f.parent == char_folder]
        if root_sff:
            return root_sff[0]

        # Sinon prendre le premier trouvé
        return sff_files[0]

    def fix_char_def(self, char_name):
        """Corrige le fichier .def d'un personnage"""
        char_folder = self.chars_path / char_name

        if not char_folder.exists():
            self.log(f"{char_name}: Dossier introuvable", "ERROR")
            return False

        # Chercher le fichier .def
        def_files = list(char_folder.glob("*.def"))
        if not def_files:
            self.log(f"{char_name}: Aucun fichier .def trouvé", "ERROR")
            return False

        def_file = def_files[0]

        # Trouver le vrai fichier SFF
        sff_file = self.find_sff_file(char_folder)

        if not sff_file:
            self.log(f"{char_name}: Aucun fichier .sff trouvé dans le dossier", "ERROR")
            return False

        # Calculer le chemin relatif depuis le .def
        try:
            relative_sff = sff_file.relative_to(char_folder)
            new_sff_path = str(relative_sff).replace('\\', '/')
        except:
            new_sff_path = sff_file.name

        # Lire le .def
        try:
            content = def_file.read_text(encoding='utf-8', errors='ignore')
        except:
            self.log(f"{char_name}: Erreur lecture .def", "ERROR")
            return False

        # Backup
        backup_file = def_file.with_suffix(f'.def.sff_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        shutil.copy2(def_file, backup_file)

        # Remplacer la ligne sprite =
        old_content = content

        # Trouver et remplacer la ligne sprite
        pattern = r'(sprite\s*=\s*)([^;\n]+)(.*)'

        def replace_sprite(match):
            return f"{match.group(1)}{new_sff_path}{match.group(3)}"

        new_content = re.sub(pattern, replace_sprite, content, flags=re.IGNORECASE)

        if new_content == old_content:
            # Pas de ligne sprite= trouvée, l'ajouter dans [Files]
            files_pattern = r'(\[Files\][^\[]*)'

            def add_sprite(match):
                section = match.group(0)
                if 'sprite' not in section.lower():
                    # Ajouter après la section [Files]
                    lines = section.split('\n')
                    lines.insert(1, f'sprite = {new_sff_path}')
                    return '\n'.join(lines)
                return section

            new_content = re.sub(files_pattern, add_sprite, content, flags=re.IGNORECASE | re.DOTALL)

        # Sauvegarder
        def_file.write_text(new_content, encoding='utf-8')

        self.log(f"{char_name}: sprite = {new_sff_path}", "FIX")
        return True

    def run(self):
        """Exécute le fix complet"""
        print("\n" + "="*70)
        print("  🔧 FIX MISSING SFF PATHS - KOF ULTIMATE")
        print("="*70 + "\n")

        self.log(f"Personnages à corriger: {len(self.broken_chars)}", "INFO")

        print("\n" + "="*70)
        print("  CORRECTION DES CHEMINS SFF")
        print("="*70 + "\n")

        fixed = []
        failed = []

        for char_name in self.broken_chars:
            if self.fix_char_def(char_name):
                fixed.append(char_name)
            else:
                failed.append(char_name)

        print("\n" + "="*70)
        print("  📊 RÉSUMÉ")
        print("="*70)
        self.log(f"Personnages corrigés: {len(fixed)}", "SUCCESS")
        self.log(f"Personnages échoués: {len(failed)}", "WARNING")

        if failed:
            print("\n" + "="*70)
            print("  ⚠️  PERSONNAGES NON CORRIGÉS")
            print("="*70)
            for char in failed[:10]:
                print(f"  • {char}")
            if len(failed) > 10:
                print(f"  ... et {len(failed) - 10} autres")

        print("\n" + "="*70)
        print("  💡 RÉSULTAT")
        print("="*70)
        print("\nLes fichiers .def ont été mis à jour avec les bons chemins SFF.")
        print("Les mini-portraits devraient maintenant s'afficher correctement!")
        print("\nRelancez le jeu pour voir les changements.")
        print("="*70 + "\n")

        return len(fixed), len(failed)

if __name__ == "__main__":
    fixer = SFFPathFixer()
    fixed, failed = fixer.run()

    if failed > 0:
        sys.exit(1)
