#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - DIAGNOSTIC PRO COMPLET
Audit complet de qualité professionnelle pour détecter TOUTES les erreurs
"""

import os
import re
from pathlib import Path
from datetime import datetime
import json

class KOFProDiagnostic:
    """Diagnostic professionnel complet du jeu"""

    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.errors = []
        self.warnings = []
        self.info = []
        self.stats = {
            'chars_checked': 0,
            'stages_checked': 0,
            'files_scanned': 0,
            'errors_found': 0,
            'warnings_found': 0
        }

    def log(self, message, level="INFO"):
        """Log avec catégorisation"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}"

        if level == "ERROR":
            self.errors.append(entry)
            self.stats['errors_found'] += 1
            print(f"❌ {entry}")
        elif level == "WARNING":
            self.warnings.append(entry)
            self.stats['warnings_found'] += 1
            print(f"⚠️  {entry}")
        else:
            self.info.append(entry)
            print(f"ℹ️  {entry}")

    def check_file_exists(self, filepath, description):
        """Vérifie qu'un fichier existe"""
        if not filepath.exists():
            self.log(f"Fichier manquant: {description} - {filepath}", "ERROR")
            return False
        return True

    def check_def_file(self, def_file):
        """Vérifie un fichier .def pour erreurs de syntaxe"""
        if not def_file.exists():
            return

        self.stats['files_scanned'] += 1

        try:
            content = def_file.read_text(encoding='utf-8', errors='ignore')

            # Vérifier les références de fichiers
            file_refs = re.findall(r'(\w+)\s*=\s*([^\r\n;]+)', content)

            for key, value in file_refs:
                value = value.strip()

                # Ignorer les valeurs numériques
                if value.replace('.', '').replace('-', '').isdigit():
                    continue

                # Vérifier si c'est une référence de fichier
                if any(ext in value.lower() for ext in ['.sff', '.air', '.snd', '.cmd', '.cns', '.st']):
                    ref_path = def_file.parent / value
                    if not ref_path.exists():
                        self.log(f"Référence manquante dans {def_file.name}: {key} = {value}", "ERROR")

            # Vérifier sections requises pour personnages
            if def_file.name.endswith('.def') and 'chars' in str(def_file.parent):
                required_sections = ['Info', 'Files']
                for section in required_sections:
                    if f'[{section}]' not in content:
                        self.log(f"Section [{section}] manquante dans {def_file}", "ERROR")

        except Exception as e:
            self.log(f"Erreur lecture {def_file}: {e}", "ERROR")

    def check_character(self, char_path):
        """Audit complet d'un personnage"""
        self.stats['chars_checked'] += 1

        # Chercher le fichier .def
        def_files = list(char_path.glob('*.def'))

        if not def_files:
            self.log(f"Aucun .def trouvé pour {char_path.name}", "ERROR")
            return

        char_def = def_files[0]
        self.check_def_file(char_def)

        # Vérifier fichiers essentiels
        essential_files = {
            '.sff': 'Sprites',
            '.air': 'Animations',
            '.snd': 'Sons',
            '.cmd': 'Commandes'
        }

        for ext, desc in essential_files.items():
            files = list(char_path.glob(f'*{ext}'))
            if not files:
                self.log(f"{desc} manquant pour {char_path.name}", "ERROR")

        # Vérifier fichiers .cns (states)
        cns_files = list(char_path.glob('*.cns'))
        if not cns_files:
            self.log(f"Aucun fichier .cns trouvé pour {char_path.name}", "WARNING")

    def check_stage(self, stage_def):
        """Vérifie un stage"""
        self.stats['stages_checked'] += 1
        self.check_def_file(stage_def)

        try:
            content = stage_def.read_text(encoding='utf-8', errors='ignore')

            # Vérifier section BG
            if '[BG' not in content:
                self.log(f"Aucune section BG dans {stage_def.name}", "WARNING")

        except Exception as e:
            self.log(f"Erreur lecture stage {stage_def}: {e}", "ERROR")

    def check_select_def(self):
        """Vérifie le fichier select.def"""
        select_def = self.base_path / "data" / "select.def"

        if not self.check_file_exists(select_def, "select.def"):
            return

        self.log("Vérification select.def...", "INFO")

        try:
            content = select_def.read_text(encoding='utf-8', errors='ignore')

            # Extraire les chemins de personnages
            char_pattern = re.compile(r'^([^;\s][^,\n]*),\s*stages/', re.MULTILINE)
            char_entries = char_pattern.findall(content)

            self.log(f"Trouvé {len(char_entries)} entrées de personnages", "INFO")

            # Vérifier que chaque personnage existe
            for char_entry in char_entries:
                char_name = char_entry.strip()
                if not char_name:
                    continue

                char_path = self.base_path / "chars" / char_name
                if not char_path.exists():
                    self.log(f"Personnage référencé mais absent: {char_name}", "ERROR")

        except Exception as e:
            self.log(f"Erreur vérification select.def: {e}", "ERROR")

    def check_mugen_cfg(self):
        """Vérifie mugen.cfg"""
        cfg_file = self.base_path / "data" / "mugen.cfg"

        if not self.check_file_exists(cfg_file, "mugen.cfg"):
            return

        self.log("Vérification mugen.cfg...", "INFO")

        try:
            content = cfg_file.read_text(encoding='utf-8', errors='ignore')

            # Vérifier paramètres critiques
            critical_params = {
                'GameWidth': '640',
                'GameHeight': '480',
            }

            for param, expected in critical_params.items():
                if param not in content:
                    self.log(f"Paramètre {param} manquant dans mugen.cfg", "WARNING")

        except Exception as e:
            self.log(f"Erreur vérification mugen.cfg: {e}", "ERROR")

    def run_full_diagnostic(self):
        """Lance le diagnostic complet"""
        print("\n" + "="*80)
        print("  KOF ULTIMATE - DIAGNOSTIC PRO COMPLET")
        print("  Audit de qualité professionnelle")
        print("="*80 + "\n")

        start_time = datetime.now()

        # 1. Vérifier fichiers système
        self.log("=== VÉRIFICATION FICHIERS SYSTÈME ===", "INFO")
        self.check_mugen_cfg()
        self.check_select_def()

        # 2. Vérifier tous les personnages
        self.log("\n=== AUDIT PERSONNAGES ===", "INFO")
        chars_path = self.base_path / "chars"

        if chars_path.exists():
            char_folders = [d for d in chars_path.iterdir() if d.is_dir()]
            self.log(f"Scan de {len(char_folders)} personnages...", "INFO")

            for char_folder in char_folders:
                self.check_character(char_folder)
        else:
            self.log("Dossier chars/ introuvable!", "ERROR")

        # 3. Vérifier tous les stages
        self.log("\n=== AUDIT STAGES ===", "INFO")
        stages_path = self.base_path / "stages"

        if stages_path.exists():
            stage_defs = list(stages_path.glob('*.def'))
            self.log(f"Scan de {len(stage_defs)} stages...", "INFO")

            for stage_def in stage_defs:
                self.check_stage(stage_def)
        else:
            self.log("Dossier stages/ introuvable!", "ERROR")

        # 4. Vérifier data essentielles
        self.log("\n=== VÉRIFICATION DATA ===", "INFO")
        data_files = [
            'data/common.snd',
            'data/common.cmd',
            'data/fight.def',
            'data/system.def'
        ]

        for data_file in data_files:
            file_path = self.base_path / data_file
            self.check_file_exists(file_path, data_file)

        # Calcul du temps
        duration = (datetime.now() - start_time).total_seconds()

        # RAPPORT FINAL
        self.generate_report(duration)

    def generate_report(self, duration):
        """Génère le rapport final"""
        print("\n" + "="*80)
        print("  RAPPORT DIAGNOSTIC FINAL")
        print("="*80 + "\n")

        print(f"📊 STATISTIQUES:")
        print(f"  • Personnages audités: {self.stats['chars_checked']}")
        print(f"  • Stages audités: {self.stats['stages_checked']}")
        print(f"  • Fichiers scannés: {self.stats['files_scanned']}")
        print(f"  • Durée: {duration:.1f}s")
        print()

        print(f"🔍 RÉSULTATS:")
        print(f"  • ❌ Erreurs: {self.stats['errors_found']}")
        print(f"  • ⚠️  Avertissements: {self.stats['warnings_found']}")
        print(f"  • ℹ️  Infos: {len(self.info)}")
        print()

        if self.errors:
            print(f"❌ ERREURS CRITIQUES ({len(self.errors)}):")
            for error in self.errors[:20]:  # Max 20 premières
                print(f"  {error}")
            if len(self.errors) > 20:
                print(f"  ... et {len(self.errors) - 20} autres")
            print()

        if self.warnings:
            print(f"⚠️  AVERTISSEMENTS ({len(self.warnings)}):")
            for warning in self.warnings[:10]:  # Max 10 premiers
                print(f"  {warning}")
            if len(self.warnings) > 10:
                print(f"  ... et {len(self.warnings) - 10} autres")
            print()

        # Sauvegarder rapport JSON
        report_file = self.base_path / f"diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        report_data = {
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': duration,
            'stats': self.stats,
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info
        }

        report_file.write_text(json.dumps(report_data, indent=2, ensure_ascii=False), encoding='utf-8')

        print(f"💾 Rapport sauvegardé: {report_file.name}")
        print()

        # Conclusion
        if self.stats['errors_found'] == 0:
            print("✅ STATUT: AUCUNE ERREUR CRITIQUE")
        elif self.stats['errors_found'] < 5:
            print("⚠️  STATUT: QUELQUES ERREURS À CORRIGER")
        else:
            print("❌ STATUT: CORRECTIONS REQUISES")

        print("="*80 + "\n")

if __name__ == "__main__":
    diagnostic = KOFProDiagnostic()
    diagnostic.run_full_diagnostic()
