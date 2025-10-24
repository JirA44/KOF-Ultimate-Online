#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIX CRASH ON LOAD - Détecte et corrige les personnages qui causent des crashs
"""

import os
import re
from pathlib import Path
from datetime import datetime

class CrashFixer:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.chars_dir = self.base_path / "chars"
        self.select_file = self.base_path / "data" / "select.def"
        self.problem_chars = []
        self.safe_chars = []

    def log(self, msg, level="INFO"):
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
        print(f"{icons.get(level, '')} {msg}")

    def check_char_integrity(self, char_name):
        """Vérifie l'intégrité d'un personnage"""
        char_path = self.chars_dir / char_name

        if not char_path.exists():
            return False, "Dossier manquant"

        # Chercher le fichier .def
        def_files = list(char_path.glob("*.def"))
        if not def_files:
            return False, "Fichier .def manquant"

        def_file = def_files[0]

        try:
            with open(def_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Vérifier sections critiques
            required_sections = ['Info', 'Files']
            missing_sections = []

            for section in required_sections:
                if f'[{section}]' not in content:
                    missing_sections.append(section)

            if missing_sections:
                return False, f"Sections manquantes: {', '.join(missing_sections)}"

            # Vérifier fichiers requis
            files_section = content.split('[Files]')[1].split('[')[0] if '[Files]' in content else ""

            # Extraire les fichiers référencés
            file_refs = {
                'cmd': re.search(r'cmd\s*=\s*([^\s\n]+)', files_section, re.I),
                'cns': re.search(r'cns\s*=\s*([^\s\n]+)', files_section, re.I),
                'sff': re.search(r'sff\s*=\s*([^\s\n]+)', files_section, re.I),
                'air': re.search(r'air\s*=\s*([^\s\n]+)', files_section, re.I),
            }

            missing_files = []
            for file_type, match in file_refs.items():
                if match:
                    filename = match.group(1).strip()
                    file_path = char_path / filename
                    if not file_path.exists():
                        missing_files.append(f"{file_type}: {filename}")

            if missing_files:
                return False, f"Fichiers manquants: {', '.join(missing_files)}"

            # Vérifier le fichier AIR pour merged lines
            if file_refs['air']:
                air_file = char_path / file_refs['air'].group(1).strip()
                if air_file.exists():
                    try:
                        with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
                            air_content = f.read()

                        # Détecter merged lines (bug critique)
                        if re.search(r'Clsn[12]\[\d+\]\s*=\s*[^\n]+\[Begin Action', air_content):
                            return False, "Fichier AIR corrompu (merged lines)"
                    except:
                        pass

            return True, "OK"

        except Exception as e:
            return False, f"Erreur: {str(e)}"

    def scan_all_characters(self):
        """Scanne tous les personnages"""
        self.log("\n" + "="*60)
        self.log("SCAN DES PERSONNAGES")
        self.log("="*60 + "\n")

        # Lire select.def
        with open(self.select_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        char_count = 0
        problem_count = 0

        for i, line in enumerate(lines, 1):
            line = line.strip()

            # Ignorer commentaires et sections
            if not line or line.startswith(';') or line.startswith('['):
                continue

            # Extraire nom personnage
            if ',' in line:
                char_name = line.split(',')[0].strip()
                char_count += 1

                # Vérifier intégrité
                is_ok, reason = self.check_char_integrity(char_name)

                if is_ok:
                    self.safe_chars.append((i, char_name, line))
                else:
                    self.problem_chars.append((i, char_name, reason))
                    problem_count += 1
                    self.log(f"❌ Ligne {i}: {char_name} - {reason}", "ERROR")

        self.log(f"\n✅ Personnages OK: {len(self.safe_chars)}/{char_count}", "SUCCESS")
        self.log(f"❌ Personnages problématiques: {problem_count}/{char_count}", "ERROR")

    def create_safe_select_def(self):
        """Crée un select.def sécurisé"""
        self.log("\n" + "="*60)
        self.log("CRÉATION SELECT.DEF SÉCURISÉ")
        self.log("="*60 + "\n")

        # Backup original
        backup_file = self.select_file.parent / f"select.def.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        import shutil
        shutil.copy2(self.select_file, backup_file)
        self.log(f"Backup créé: {backup_file.name}", "SUCCESS")

        # Lire template original
        with open(self.select_file, 'r', encoding='utf-8', errors='ignore') as f:
            original_lines = f.readlines()

        # Créer nouveau contenu
        new_lines = []
        new_lines.append("; IKEMEN GO Select.def\n")
        new_lines.append(f"; Auto-corrigé le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        new_lines.append("; Par FIX_CRASH_ON_LOAD.py\n")
        new_lines.append(";\n")
        new_lines.append("; ⚠️  Personnages problématiques désactivés automatiquement\n")
        new_lines.append(";\n\n")
        new_lines.append("[Characters]\n")
        new_lines.append(";\n")
        new_lines.append("; === PERSONNAGES VALIDÉS (SAFE) ===\n")
        new_lines.append(";\n")

        # Ajouter personnages sûrs
        for line_num, char_name, full_line in self.safe_chars:
            new_lines.append(full_line + "\n")

        # Ajouter personnages problématiques en commentaire
        if self.problem_chars:
            new_lines.append(";\n")
            new_lines.append("; === PERSONNAGES DÉSACTIVÉS (PROBLÉMATIQUES) ===\n")
            new_lines.append(";\n")

            for line_num, char_name, reason in self.problem_chars:
                new_lines.append(f"; {char_name}, stages/Abyss-Rugal-Palace.def  ; DÉSACTIVÉ: {reason}\n")

        new_lines.append(";\n")
        new_lines.append(f"; Total: {len(self.safe_chars)} personnages sûrs\n")
        new_lines.append(f"; Désactivés: {len(self.problem_chars)} personnages problématiques\n")
        new_lines.append(";\n")

        # Copier le reste (stages, etc.)
        in_stages_section = False
        for line in original_lines:
            if '[ExtraStages]' in line or '[Stages]' in line:
                in_stages_section = True

            if in_stages_section:
                new_lines.append(line)

        # Écrire nouveau fichier
        with open(self.select_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        self.log(f"✅ Nouveau select.def créé avec {len(self.safe_chars)} personnages sûrs", "SUCCESS")
        self.log(f"⚠️  {len(self.problem_chars)} personnages désactivés", "WARNING")

    def generate_report(self):
        """Génère un rapport détaillé"""
        report_file = self.base_path / f"RAPPORT_CRASH_FIX_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 🔧 RAPPORT CORRECTION CRASHS\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            f.write("## ✅ PERSONNAGES SÛRS\n\n")
            f.write(f"**Total:** {len(self.safe_chars)} personnages\n\n")

            f.write("## ❌ PERSONNAGES PROBLÉMATIQUES\n\n")
            f.write(f"**Total:** {len(self.problem_chars)} personnages\n\n")

            if self.problem_chars:
                f.write("### Liste des Problèmes\n\n")
                for line_num, char_name, reason in self.problem_chars:
                    f.write(f"- **{char_name}** (ligne {line_num}): {reason}\n")

            f.write("\n---\n\n")
            f.write("## 🛠️ ACTIONS EFFECTUÉES\n\n")
            f.write("1. ✅ Backup du select.def original créé\n")
            f.write("2. ✅ Nouveau select.def généré avec seulement les personnages sûrs\n")
            f.write("3. ✅ Personnages problématiques désactivés (commentés)\n\n")

            f.write("## 🎮 RÉSULTAT ATTENDU\n\n")
            f.write("- ✅ Plus de crashs lors de l'entrée en combat\n")
            f.write("- ✅ Plus de cases vides dans la sélection\n")
            f.write("- ✅ Tous les personnages affichés sont fonctionnels\n\n")

        self.log(f"\n📄 Rapport sauvegardé: {report_file.name}", "SUCCESS")
        return report_file

    def run(self):
        """Lance la correction complète"""
        print("\n" + "="*70)
        print("  🔧 FIX CRASH ON LOAD - CORRECTION AUTOMATIQUE")
        print("="*70 + "\n")

        self.scan_all_characters()

        if self.problem_chars:
            self.create_safe_select_def()
            report_file = self.generate_report()

            print("\n" + "="*70)
            print("  ✅ CORRECTION TERMINÉE")
            print("="*70)
            print(f"\n✅ {len(self.safe_chars)} personnages sûrs conservés")
            print(f"❌ {len(self.problem_chars)} personnages problématiques désactivés")
            print(f"\n📄 Rapport: {report_file.name}")
            print("\n⚠️  RELANCEZ LE JEU pour tester les corrections\n")
        else:
            print("\n" + "="*70)
            print("  ✅ AUCUN PROBLÈME DÉTECTÉ")
            print("="*70)
            print("\nTous les personnages sont OK!")
            print("Le problème de crash doit venir d'ailleurs.\n")

if __name__ == "__main__":
    fixer = CrashFixer()
    fixer.run()
