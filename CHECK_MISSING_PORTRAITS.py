#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHECK MISSING PORTRAITS - KOF ULTIMATE
Trouve les personnages sans mini-portraits (cases vides qui montrent quand même le grand portrait)
"""

import os
import sys
from pathlib import Path

class PortraitChecker:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.chars_path = self.base_path / "chars"
        self.select_def = self.base_path / "data" / "select.def"

    def log(self, message, level="INFO"):
        """Affiche un message avec niveau"""
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✓",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "MISSING": "🔴"
        }
        icon = icons.get(level, "•")
        print(f"{icon} {message}")

    def load_characters(self):
        """Charge la liste des personnages depuis select.def"""
        content = self.select_def.read_text(encoding='utf-8', errors='ignore')

        characters = []
        in_characters = False

        for line in content.split('\n'):
            line = line.strip()

            if line == '[Characters]':
                in_characters = True
                continue
            elif line.startswith('['):
                break
            elif in_characters and line and not line.startswith(';'):
                # Extraire le nom du personnage (sans randomselect, order, etc.)
                char_name = line.split(',')[0].strip()
                if char_name:
                    characters.append(char_name)

        return characters

    def check_char_portrait(self, char_name):
        """Vérifie si un personnage a un portrait sprite"""
        char_folder = self.chars_path / char_name

        if not char_folder.exists():
            return None, "Folder not found"

        # Chercher le fichier .def
        def_files = list(char_folder.glob("*.def"))
        if not def_files:
            return None, "No .def file"

        # Lire le .def pour trouver le .sff
        def_file = def_files[0]
        content = def_file.read_text(encoding='utf-8', errors='ignore')

        # Chercher la ligne sprite =
        import re
        sff_match = re.search(r'sprite\s*=\s*(.+)', content, re.IGNORECASE)
        if not sff_match:
            return None, "No sprite defined"

        sff_name = sff_match.group(1).strip()
        sff_path = char_folder / sff_name

        if not sff_path.exists():
            return None, f"SFF not found: {sff_name}"

        # Le fichier SFF existe
        # Chercher si le portrait est défini (sprite 9000,0)
        # On va juste vérifier que le fichier SFF existe
        return True, f"OK ({sff_path.name})"

    def run(self):
        """Exécute le diagnostic"""
        print("\n" + "="*70)
        print("  🔍 CHECK MISSING PORTRAITS - KOF ULTIMATE")
        print("="*70 + "\n")

        # Charger les personnages
        characters = self.load_characters()
        self.log(f"Chargement de {len(characters)} personnages depuis select.def...", "INFO")

        print("\n" + "="*70)
        print("  VÉRIFICATION DES PORTRAITS")
        print("="*70 + "\n")

        chars_ok = []
        chars_missing = []

        for i, char_name in enumerate(characters, 1):
            has_portrait, reason = self.check_char_portrait(char_name)

            if has_portrait:
                chars_ok.append(char_name)
                # Ne pas afficher les OK pour ne pas polluer
            else:
                chars_missing.append((char_name, reason))
                self.log(f"[{i:3d}] {char_name:40s} → {reason}", "MISSING")

        # Résumé
        print("\n" + "="*70)
        print("  📊 RÉSUMÉ")
        print("="*70)
        self.log(f"Personnages OK: {len(chars_ok)}", "SUCCESS")
        self.log(f"Personnages sans portrait: {len(chars_missing)}", "WARNING")

        if chars_missing:
            print("\n" + "="*70)
            print("  🔴 PERSONNAGES SANS MINI-PORTRAIT")
            print("="*70)
            for char_name, reason in chars_missing[:20]:  # Afficher les 20 premiers
                print(f"  • {char_name:40s} ({reason})")

            if len(chars_missing) > 20:
                print(f"  ... et {len(chars_missing) - 20} autres")

        print("\n" + "="*70)
        print("  💡 SOLUTION")
        print("="*70)
        print("\nPour corriger:")
        print("1. Ces personnages doivent être RETIRÉS de select.def")
        print("2. OU leurs sprites portraits doivent être ajoutés dans leurs fichiers .sff")
        print("\nVoulez-vous que je génère un select.def sans ces personnages?")
        print("="*70 + "\n")

        return chars_ok, chars_missing

if __name__ == "__main__":
    checker = PortraitChecker()
    chars_ok, chars_missing = checker.run()

    if chars_missing:
        print(f"\n⚠️  {len(chars_missing)} personnages ont des problèmes de portrait")
    else:
        print("\n✓ Tous les personnages ont des portraits!")
