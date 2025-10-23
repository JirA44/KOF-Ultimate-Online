#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - DÉTECTION ET CORRECTION EN TEMPS RÉEL
Trouve TOUTES les erreurs et les corrige immédiatement
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

class RealTimeErrorFixer:
    """Détecte et corrige les erreurs en temps réel"""

    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.fixes = 0

    def log(self, message, level="INFO"):
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "FIX": "🔧"}
        print(f"{icons.get(level, '')} {message}")

    def scan_mugen_log_for_errors(self):
        """Analyse mugen.log pour erreurs"""
        mugen_log = self.base_path / "mugen.log"

        if not mugen_log.exists():
            self.log("mugen.log n'existe pas encore", "INFO")
            return []

        errors = []
        try:
            with open(mugen_log, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    line_lower = line.lower()
                    if any(word in line_lower for word in ['error', 'failed', 'crash', 'cannot', 'missing']):
                        errors.append((line_num, line.strip()))
        except Exception as e:
            self.log(f"Erreur lecture mugen.log: {e}", "ERROR")

        return errors

    def fix_select_def_broken_entries(self):
        """Corrige select.def pour enlever les entrées cassées"""
        select_def = self.base_path / "data" / "select.def"

        if not select_def.exists():
            return

        self.log("Nettoyage select.def...", "FIX")

        try:
            content = select_def.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            fixed_lines = []
            chars_path = self.base_path / "chars"
            fixed = 0

            for line in lines:
                # Si c'est une ligne de personnage
                if line.strip() and not line.strip().startswith(';') and not line.strip().startswith('['):
                    # Extraire le nom du personnage
                    match = re.match(r'^([^,\s]+)', line.strip())
                    if match:
                        char_name = match.group(1)
                        char_folder = chars_path / char_name

                        # Vérifier si le dossier existe
                        if not char_folder.exists():
                            fixed_lines.append(f"; {line}  ; AUTO-FIX: Dossier manquant")
                            fixed += 1
                            continue

                        # Vérifier si le personnage a un .def
                        def_files = list(char_folder.glob('*.def'))
                        if not def_files:
                            fixed_lines.append(f"; {line}  ; AUTO-FIX: Aucun .def trouvé")
                            fixed += 1
                            continue

                        # Vérifier si le personnage a au moins un .sff
                        sff_files = list(char_folder.glob('*.sff'))
                        if not sff_files:
                            fixed_lines.append(f"; {line}  ; AUTO-FIX: Aucun sprite")
                            fixed += 1
                            continue

                fixed_lines.append(line)

            if fixed > 0:
                # Backup
                backup = select_def.with_suffix('.def.backup2')
                if not backup.exists():
                    shutil.copy2(select_def, backup)

                # Sauvegarder
                select_def.write_text('\n'.join(fixed_lines), encoding='utf-8')
                self.log(f"✅ {fixed} entrées cassées désactivées dans select.def", "SUCCESS")
                self.fixes += fixed

        except Exception as e:
            self.log(f"Erreur correction select.def: {e}", "ERROR")

    def check_all_characters_have_essentials(self):
        """Vérifie que tous les personnages actifs ont les fichiers essentiels"""
        chars_path = self.base_path / "chars"

        if not chars_path.exists():
            return

        self.log("Vérification des personnages actifs...", "INFO")

        problematic = []

        for char_folder in chars_path.iterdir():
            if not char_folder.is_dir():
                continue

            # Vérifier fichiers essentiels
            has_def = bool(list(char_folder.glob('*.def')))
            has_sff = bool(list(char_folder.glob('*.sff')))
            has_air = bool(list(char_folder.glob('*.air')))
            has_cmd = bool(list(char_folder.glob('*.cmd')))

            if not (has_def and has_sff and has_air):
                problematic.append({
                    'name': char_folder.name,
                    'missing': {
                        'def': not has_def,
                        'sff': not has_sff,
                        'air': not has_air,
                        'cmd': not has_cmd
                    }
                })

        if problematic:
            self.log(f"⚠️  {len(problematic)} personnages avec fichiers manquants", "ERROR")
            for char in problematic[:10]:  # Afficher max 10
                missing = [k for k, v in char['missing'].items() if v]
                self.log(f"  • {char['name']}: manque {', '.join(missing)}", "ERROR")

        return problematic

    def create_minimal_files_for_broken_chars(self):
        """Crée des fichiers minimaux pour les personnages cassés"""
        chars_path = self.base_path / "chars"

        if not chars_path.exists():
            return

        self.log("Création fichiers minimaux pour personnages cassés...", "FIX")

        fixed = 0

        for char_folder in chars_path.iterdir():
            if not char_folder.is_dir():
                continue

            char_name = char_folder.name

            # Si pas de .sff, créer un stub
            if not list(char_folder.glob('*.sff')):
                # On ne peut pas créer de vrais SFF, donc on désactive le perso
                continue

            # Si pas de .def, créer un minimal
            if not list(char_folder.glob('*.def')):
                def_file = char_folder / f"{char_name}.def"

                # Trouver les fichiers existants
                sff_files = list(char_folder.glob('*.sff'))
                air_files = list(char_folder.glob('*.air'))
                snd_files = list(char_folder.glob('*.snd'))
                cmd_files = list(char_folder.glob('*.cmd'))

                if sff_files:  # Seulement si on a au moins un SFF
                    content = f"""[Info]
Name = "{char_name}"
DisplayName = "{char_name}"
Author = "Auto-Generated"

[Files]
cmd = {cmd_files[0].name if cmd_files else 'common.cmd'}
sprite = {sff_files[0].name}
anim = {air_files[0].name if air_files else sff_files[0].stem + '.air'}
sound = {snd_files[0].name if snd_files else 'common.snd'}

[Arcade]
"""
                    def_file.write_text(content, encoding='utf-8')
                    self.log(f"  ✅ {char_name}.def créé", "SUCCESS")
                    fixed += 1
                    self.fixes += 1

        if fixed > 0:
            self.log(f"✅ {fixed} fichiers .def minimaux créés", "SUCCESS")

    def run_full_scan_and_fix(self):
        """Lance scan complet et correction"""
        print("\n" + "="*80)
        print("  DÉTECTION ET CORRECTION EN TEMPS RÉEL")
        print("="*80 + "\n")

        # 1. Analyser le log mugen
        self.log("=== ANALYSE MUGEN.LOG ===", "INFO")
        errors = self.scan_mugen_log_for_errors()

        if errors:
            self.log(f"❌ {len(errors)} lignes d'erreur trouvées dans mugen.log", "ERROR")
            for line_num, error in errors[:10]:
                self.log(f"  Ligne {line_num}: {error[:80]}", "ERROR")
        else:
            self.log("✅ Aucune erreur dans mugen.log", "SUCCESS")

        # 2. Nettoyer select.def
        self.log("\n=== NETTOYAGE SELECT.DEF ===", "INFO")
        self.fix_select_def_broken_entries()

        # 3. Vérifier personnages
        self.log("\n=== VÉRIFICATION PERSONNAGES ===", "INFO")
        problematic = self.check_all_characters_have_essentials()

        # 4. Créer fichiers minimaux
        if problematic:
            self.log("\n=== CRÉATION FICHIERS MINIMAUX ===", "INFO")
            self.create_minimal_files_for_broken_chars()

        # RÉSUMÉ
        print("\n" + "="*80)
        print("  RÉSUMÉ")
        print("="*80)
        print(f"✅ Corrections appliquées: {self.fixes}")
        print(f"⚠️  Personnages problématiques: {len(problematic) if problematic else 0}")
        print()
        print("Recommandations:")
        print("  1. Relancer le jeu pour tester")
        print("  2. Vérifier mugen.log après lancement")
        print("  3. Désactiver les personnages sans sprites dans select.def")
        print("="*80 + "\n")

if __name__ == "__main__":
    fixer = RealTimeErrorFixer()
    fixer.run_full_scan_and_fix()
