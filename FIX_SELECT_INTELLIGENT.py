#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIX SELECT INTELLIGENT
Ne garde QUE les personnages avec .def ET .sff (fonctionnels)
"""

import shutil
from pathlib import Path
from datetime import datetime

class IntelligentSelectFixer:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.chars_path = self.base_path / "chars"
        self.select_def = self.base_path / "data" / "select.def"

    def log(self, message, level="INFO"):
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "FIX": "🔧"}
        print(f"{icons.get(level, '')} {message}")

    def check_character_is_valid(self, char_name):
        """Vérifie si un personnage est fonctionnel (a .def ET .sff minimum)"""
        char_folder = self.chars_path / char_name

        if not char_folder.exists() or not char_folder.is_dir():
            return False, "Dossier n'existe pas"

        # Vérifier fichiers essentiels
        has_def = bool(list(char_folder.glob('*.def')))
        has_sff = bool(list(char_folder.glob('*.sff')))

        if not has_def:
            return False, "Pas de .def"
        if not has_sff:
            return False, "Pas de .sff"

        return True, "OK"

    def scan_all_available_characters(self):
        """Scanne le dossier chars/ et liste TOUS les personnages fonctionnels"""
        self.log("Scan des personnages disponibles...", "INFO")

        valid_chars = []
        invalid_chars = []

        if not self.chars_path.exists():
            self.log("❌ Dossier chars/ introuvable!", "ERROR")
            return [], []

        for char_folder in sorted(self.chars_path.iterdir()):
            if not char_folder.is_dir():
                continue

            char_name = char_folder.name
            is_valid, reason = self.check_character_is_valid(char_name)

            if is_valid:
                valid_chars.append(char_name)
            else:
                invalid_chars.append((char_name, reason))

        self.log(f"✅ {len(valid_chars)} personnages fonctionnels trouvés", "SUCCESS")
        self.log(f"❌ {len(invalid_chars)} personnages cassés", "ERROR")

        return valid_chars, invalid_chars

    def rebuild_select_def(self, valid_chars):
        """Reconstruit select.def avec UNIQUEMENT les personnages valides"""
        self.log("Reconstruction de select.def...", "FIX")

        # Backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = self.select_def.with_suffix(f'.def.backup_{timestamp}')
        shutil.copy2(self.select_def, backup)
        self.log(f"Backup créé: {backup.name}", "INFO")

        # Lire le select.def actuel pour garder la structure
        try:
            content = self.select_def.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
        except:
            lines = []

        new_lines = []
        in_characters_section = False
        chars_added = 0

        # Copier l'en-tête et les sections jusqu'à Characters
        for line in lines:
            if '[Characters]' in line:
                in_characters_section = True
                new_lines.append(line)
                new_lines.append(';')
                new_lines.append('; === PERSONNAGES ACTIFS (AUTO-GÉNÉRÉ) ===')
                new_lines.append(';')

                # Ajouter tous les personnages valides
                for char_name in valid_chars:
                    new_lines.append(f"{char_name}, stages/Abyss-Rugal-Palace.def")
                    chars_added += 1

                new_lines.append(';')
                new_lines.append(f'; Total: {chars_added} personnages fonctionnels')
                new_lines.append(';')
                break
            else:
                new_lines.append(line)

        # Copier le reste (ExtraStages, Options, etc.)
        copy_rest = False
        for line in lines:
            if '[ExtraStages]' in line or '[Options]' in line:
                copy_rest = True

            if copy_rest:
                new_lines.append(line)

        # Écrire le nouveau fichier
        self.select_def.write_text('\n'.join(new_lines), encoding='utf-8')
        self.log(f"✅ {chars_added} personnages ajoutés à select.def", "SUCCESS")

    def run_fix(self):
        """Lance la correction intelligente"""
        print("\n" + "="*80)
        print("  FIX SELECT INTELLIGENT")
        print("  Ne garde QUE les personnages fonctionnels")
        print("="*80 + "\n")

        # 1. Scanner tous les personnages
        valid_chars, invalid_chars = self.scan_all_available_characters()

        if not valid_chars:
            self.log("❌ AUCUN personnage fonctionnel trouvé!", "ERROR")
            return

        # 2. Afficher quelques exemples
        self.log("\n📋 Exemples de personnages VALIDES:", "INFO")
        for char in valid_chars[:10]:
            self.log(f"  ✓ {char}", "SUCCESS")

        if len(valid_chars) > 10:
            self.log(f"  ... et {len(valid_chars) - 10} autres", "INFO")

        self.log("\n❌ Exemples de personnages CASSÉS:", "INFO")
        for char, reason in invalid_chars[:10]:
            self.log(f"  ✗ {char} ({reason})", "ERROR")

        if len(invalid_chars) > 10:
            self.log(f"  ... et {len(invalid_chars) - 10} autres", "INFO")

        # 3. Reconstruire select.def
        self.log("\n🔧 RECONSTRUCTION SELECT.DEF", "FIX")
        self.rebuild_select_def(valid_chars)

        # RÉSUMÉ
        print("\n" + "="*80)
        print("  RÉSUMÉ")
        print("="*80)
        print(f"✅ Personnages fonctionnels: {len(valid_chars)}")
        print(f"❌ Personnages cassés exclus: {len(invalid_chars)}")
        print()
        print("Le jeu devrait maintenant afficher les personnages correctement!")
        print("="*80 + "\n")

if __name__ == "__main__":
    fixer = IntelligentSelectFixer()
    fixer.run_fix()
