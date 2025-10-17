#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REMOVE BROKEN PORTRAITS - KOF ULTIMATE
Génère un select.def nettoyé sans les personnages qui n'ont pas de mini-portraits
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

class BrokenPortraitRemover:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.chars_path = self.base_path / "chars"
        self.select_def = self.base_path / "data" / "select.def"

        # Liste des personnages problématiques détectés
        self.broken_chars = [
            "Akari",
            "Alou_AKOF",
            "D.Yashiro.Rhythm(Dusk)1.x",
            "D_DisciplineGirl",
            "Error Zero",
            "Graves",
            "Kei",
            "Kevenoce",
            "Maltet",
            "Nao-MX 1.0",
            "Rozwel S.K (LEGIT)",
            "Rugal7th",
            "Ryuji",
            "Shadow-Dancer",
            "Tenrou_Kunagi",
            "Wild.O.Yashiro",
            "baiyi",
            "bob",
            "cciking",
            "kfm"
        ]

    def log(self, message, level="INFO"):
        """Affiche un message avec niveau"""
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✓",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "REMOVE": "🗑️"
        }
        icon = icons.get(level, "•")
        print(f"{icon} {message}")

    def check_char_has_portrait(self, char_name):
        """Vérifie si un personnage a un portrait sprite"""
        char_folder = self.chars_path / char_name

        if not char_folder.exists():
            return False

        # Chercher le fichier .def
        def_files = list(char_folder.glob("*.def"))
        if not def_files:
            return False

        # Lire le .def pour trouver le .sff
        def_file = def_files[0]
        try:
            content = def_file.read_text(encoding='utf-8', errors='ignore')
        except:
            return False

        # Chercher la ligne sprite =
        import re
        sff_match = re.search(r'sprite\s*=\s*(.+)', content, re.IGNORECASE)
        if not sff_match:
            return False

        sff_name = sff_match.group(1).strip()
        # Retirer les commentaires
        if ';' in sff_name:
            sff_name = sff_name.split(';')[0].strip()

        sff_path = char_folder / sff_name

        # Le fichier SFF existe?
        return sff_path.exists()

    def generate_clean_select_def(self):
        """Génère un nouveau select.def sans les personnages cassés"""
        # Backup
        backup_file = self.select_def.with_suffix(f'.def.clean_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        shutil.copy2(self.select_def, backup_file)
        self.log(f"Backup créé: {backup_file.name}", "SUCCESS")

        # Lire le fichier actuel
        content = self.select_def.read_text(encoding='utf-8', errors='ignore')

        # Traiter ligne par ligne
        lines = content.split('\n')
        new_lines = []
        in_characters = False
        removed_count = 0
        kept_count = 0

        for line in lines:
            stripped = line.strip()

            # Début de la section Characters
            if stripped == '[Characters]':
                in_characters = True
                new_lines.append(line)
                continue

            # Fin de la section Characters
            elif stripped.startswith('[') and in_characters:
                in_characters = False
                new_lines.append(line)
                continue

            # Dans la section Characters
            elif in_characters and line and not stripped.startswith(';'):
                # Extraire le nom du personnage
                char_name = stripped.split(',')[0].strip()

                if char_name:
                    # Vérifier si c'est un personnage cassé
                    is_broken = char_name in self.broken_chars

                    if is_broken:
                        # Commenter la ligne au lieu de la supprimer
                        new_lines.append(f";REMOVED_NO_PORTRAIT: {line}")
                        removed_count += 1
                        self.log(f"Retiré: {char_name}", "REMOVE")
                    else:
                        new_lines.append(line)
                        kept_count += 1
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        # Sauvegarder
        self.select_def.write_text('\n'.join(new_lines), encoding='utf-8')
        self.log(f"Fichier sauvegardé: {self.select_def}", "SUCCESS")

        return removed_count, kept_count

    def run(self):
        """Exécute le nettoyage complet"""
        print("\n" + "="*70)
        print("  🗑️  REMOVE BROKEN PORTRAITS - KOF ULTIMATE")
        print("="*70 + "\n")

        self.log(f"Personnages à retirer: {len(self.broken_chars)}", "INFO")

        print("\n" + "="*70)
        print("  PERSONNAGES QUI SERONT RETIRÉS:")
        print("="*70)
        for char in self.broken_chars:
            print(f"  • {char}")

        print("\n" + "="*70)
        print("  ⚠️  AVERTISSEMENT")
        print("="*70)
        self.log("Cette opération va modifier select.def", "WARNING")
        self.log("Les personnages cassés seront commentés (pas supprimés)", "INFO")
        self.log("Vous pourrez les restaurer manuellement si besoin", "INFO")

        user_input = input("\nContinuer? (o/N): ")

        if user_input.lower() not in ['o', 'oui', 'y', 'yes']:
            self.log("Opération annulée par l'utilisateur", "INFO")
            return False

        print("\n" + "="*70)
        print("  NETTOYAGE EN COURS...")
        print("="*70 + "\n")

        removed, kept = self.generate_clean_select_def()

        print("\n" + "="*70)
        print("  ✓ NETTOYAGE TERMINÉ!")
        print("="*70)
        self.log(f"Personnages retirés: {removed}", "SUCCESS")
        self.log(f"Personnages conservés: {kept}", "SUCCESS")

        print("\n" + "="*70)
        print("  💡 RÉSULTAT")
        print("="*70)
        print("\nLe fichier select.def a été nettoyé!")
        print("Les 20 personnages sans mini-portraits ont été commentés.")
        print("\nRelancez le jeu pour voir les changements.")
        print("="*70 + "\n")

        return True

if __name__ == "__main__":
    remover = BrokenPortraitRemover()
    success = remover.run()

    if not success:
        sys.exit(1)
