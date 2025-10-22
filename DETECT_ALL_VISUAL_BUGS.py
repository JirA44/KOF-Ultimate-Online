#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DETECT ALL VISUAL BUGS - Détection automatique de tous les bugs visuels in-game
"""

import os
import sys
import re
from pathlib import Path
from collections import defaultdict

class VisualBugDetector:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.chars_path = self.base_path / "chars"
        self.stages_path = self.base_path / "stages"
        self.data_path = self.base_path / "data"
        self.bugs = defaultdict(list)

    def log(self, message, level="INFO"):
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✓",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "BUG": "🐛"
        }
        print(f"{icons.get(level, '')} {message}")

    def check_character_sprites(self):
        """Vérifie les problèmes de sprites des personnages"""
        self.log("Vérification des sprites de personnages...", "INFO")

        if not self.chars_path.exists():
            return

        for char_folder in self.chars_path.iterdir():
            if not char_folder.is_dir():
                continue

            char_name = char_folder.name

            # Vérifier le fichier .def
            def_files = list(char_folder.glob("*.def"))
            if not def_files:
                self.bugs["missing_def"].append(char_name)
                continue

            def_file = def_files[0]
            content = def_file.read_text(encoding='utf-8', errors='ignore')

            # Vérifier le fichier SFF
            sff_match = re.search(r'sprite\s*=\s*(.+)', content, re.IGNORECASE)
            if sff_match:
                sff_name = sff_match.group(1).strip()
                sff_path = char_folder / sff_name
                if not sff_path.exists():
                    self.bugs["missing_sff"].append(f"{char_name} ({sff_name})")

            # Vérifier le fichier AIR
            air_match = re.search(r'anim\s*=\s*(.+)', content, re.IGNORECASE)
            if air_match:
                air_name = air_match.group(1).strip()
                air_path = char_folder / air_name
                if not air_path.exists():
                    self.bugs["missing_air"].append(f"{char_name} ({air_name})")

        self.log(f"Analysé {len(list(self.chars_path.iterdir()))} dossiers de personnages", "SUCCESS")

    def check_stage_backgrounds(self):
        """Vérifie les problèmes de décors de stages"""
        self.log("Vérification des décors de stages...", "INFO")

        if not self.stages_path.exists():
            return

        for stage_file in self.stages_path.glob("*.def"):
            stage_name = stage_file.stem
            content = stage_file.read_text(encoding='utf-8', errors='ignore')

            # Vérifier le fichier SFF du stage
            sff_match = re.search(r'spr\s*=\s*(.+)', content, re.IGNORECASE)
            if sff_match:
                sff_name = sff_match.group(1).strip()
                sff_path = self.stages_path / sff_name
                if not sff_path.exists():
                    self.bugs["missing_stage_sff"].append(f"{stage_name} ({sff_name})")

        self.log(f"Analysé {len(list(self.stages_path.glob('*.def')))} stages", "SUCCESS")

    def check_system_graphics(self):
        """Vérifie les ressources graphiques système"""
        self.log("Vérification des graphiques système...", "INFO")

        system_def = self.data_path / "system.def"
        if not system_def.exists():
            self.bugs["system"].append("system.def manquant")
            return

        content = system_def.read_text(encoding='utf-8', errors='ignore')

        # Vérifier les fichiers SFF système
        patterns = [
            (r'spr\s*=\s*(.+)', "System SFF"),
            (r'snd\s*=\s*(.+)', "System SND"),
            (r'font\d*\s*=\s*(.+)', "System Font"),
        ]

        for pattern, desc in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                file_name = match.group(1).strip().split(',')[0]
                file_path = self.data_path / file_name

                if not file_path.exists():
                    self.bugs["missing_system_files"].append(f"{desc}: {file_name}")

        self.log("Vérification des graphiques système terminée", "SUCCESS")

    def check_select_screen_config(self):
        """Vérifie la configuration de l'écran de sélection"""
        self.log("Vérification de l'écran de sélection...", "INFO")

        system_def = self.data_path / "system.def"
        if not system_def.exists():
            return

        content = system_def.read_text(encoding='utf-8', errors='ignore')

        # Extraire la configuration de [Select Info]
        in_select = False
        config = {}

        for line in content.split('\n'):
            line = line.strip()
            if line == '[Select Info]':
                in_select = True
            elif line.startswith('['):
                in_select = False
            elif in_select and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()

        # Vérifier les valeurs critiques
        if 'cell.size' in config:
            try:
                w, h = map(int, config['cell.size'].split(','))
                if w < 30 or h < 30:
                    self.bugs["select_screen"].append(f"Cellules trop petites: {w}x{h} (recommandé: 30x30 min)")
            except:
                pass

        if 'portrait.scale' in config:
            try:
                sx, sy = map(float, config['portrait.scale'].split(','))
                if sx > 0.5 or sy > 0.5:
                    self.bugs["select_screen"].append(f"Échelle portraits trop grande: {sx}x{sy}")
            except:
                pass

        if 'rows' in config and 'columns' in config:
            try:
                rows = int(config['rows'])
                cols = int(config['columns'])
                total = rows * cols
                if total < 100:
                    self.bugs["select_screen"].append(f"Grille trop petite: {rows}x{cols}={total} (besoin ~189)")
            except:
                pass

        self.log("Vérification de l'écran de sélection terminée", "SUCCESS")

    def check_lifebar_config(self):
        """Vérifie la configuration de la barre de vie"""
        self.log("Vérification de la barre de vie...", "INFO")

        fight_def = self.data_path / "fight.def"
        if not fight_def.exists():
            self.bugs["lifebar"].append("fight.def manquant")
            return

        content = fight_def.read_text(encoding='utf-8', errors='ignore')

        # Vérifier les fichiers de fonts lifebar
        font_matches = re.finditer(r'font\s*=\s*(.+)', content, re.IGNORECASE)
        for match in font_matches:
            font_spec = match.group(1).strip()
            # Format: font = fichier, bank, align
            parts = font_spec.split(',')
            if parts:
                font_file = parts[0].strip()
                font_path = self.data_path / font_file
                if not font_path.exists():
                    self.bugs["lifebar"].append(f"Font manquant: {font_file}")

        self.log("Vérification de la barre de vie terminée", "SUCCESS")

    def print_report(self):
        """Affiche le rapport complet"""
        print("\n" + "="*70)
        print("  🐛 RAPPORT DES BUGS VISUELS DÉTECTÉS")
        print("="*70 + "\n")

        if not any(self.bugs.values()):
            self.log("Aucun bug visuel détecté! 🎉", "SUCCESS")
            return

        # Compter le total
        total_bugs = sum(len(bugs) for bugs in self.bugs.values())
        self.log(f"Total: {total_bugs} problèmes détectés", "WARNING")
        print()

        # Afficher par catégorie
        categories = {
            "missing_def": "Personnages sans fichier .def",
            "missing_sff": "Personnages sans sprites (SFF manquant)",
            "missing_air": "Personnages sans animations (AIR manquant)",
            "missing_stage_sff": "Stages sans sprites (SFF manquant)",
            "missing_system_files": "Fichiers système manquants",
            "select_screen": "Problèmes d'écran de sélection",
            "lifebar": "Problèmes de barre de vie",
            "system": "Problèmes système",
        }

        for bug_type, description in categories.items():
            if bug_type in self.bugs and self.bugs[bug_type]:
                print(f"\n{'─'*70}")
                print(f"📌 {description}")
                print(f"{'─'*70}")
                for bug in self.bugs[bug_type]:
                    print(f"  • {bug}")

        print("\n" + "="*70)
        print("  💡 RECOMMANDATIONS")
        print("="*70 + "\n")

        if self.bugs.get("missing_sff") or self.bugs.get("missing_air"):
            print("  → Vérifier l'intégrité des dossiers personnages")
            print("  → Réinstaller les personnages problématiques")

        if self.bugs.get("missing_stage_sff"):
            print("  → Vérifier l'intégrité des dossiers stages")
            print("  → Utiliser FIX_IKEMEN_GO.bat pour réparer")

        if self.bugs.get("select_screen"):
            print("  → Exécuter FIX_PORTRAITS_AUTO.py")
            print("  → Ajuster la configuration de l'écran de sélection")

        if self.bugs.get("missing_system_files"):
            print("  → Vérifier l'installation du jeu")
            print("  → Restaurer les fichiers système depuis backup")

        print()

    def save_report(self):
        """Sauvegarde le rapport dans un fichier"""
        report_file = self.base_path / "VISUAL_BUGS_REPORT.txt"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("  RAPPORT DES BUGS VISUELS - KOF ULTIMATE\n")
            f.write(f"  Généré le: {Path(__file__).stat().st_mtime}\n")
            f.write("="*70 + "\n\n")

            if not any(self.bugs.values()):
                f.write("Aucun bug visuel détecté!\n")
            else:
                total = sum(len(bugs) for bugs in self.bugs.values())
                f.write(f"Total: {total} problèmes détectés\n\n")

                for bug_type, bugs in self.bugs.items():
                    if bugs:
                        f.write(f"\n{bug_type.upper()}:\n")
                        f.write("-"*70 + "\n")
                        for bug in bugs:
                            f.write(f"  • {bug}\n")

        self.log(f"Rapport sauvegardé: {report_file.name}", "SUCCESS")

    def run(self):
        """Exécute toutes les vérifications"""
        print("\n" + "="*70)
        print("  🔍 DÉTECTION AUTOMATIQUE DES BUGS VISUELS")
        print("="*70 + "\n")

        self.check_character_sprites()
        self.check_stage_backgrounds()
        self.check_system_graphics()
        self.check_select_screen_config()
        self.check_lifebar_config()

        self.print_report()
        self.save_report()

        return len(self.bugs) == 0

if __name__ == "__main__":
    detector = VisualBugDetector()
    success = detector.run()
    sys.exit(0 if success else 1)
