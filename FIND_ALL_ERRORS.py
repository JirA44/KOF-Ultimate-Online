#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIND ALL ERRORS - Trouve TOUTES les erreurs dans KOF Ultimate
Scanner ultra-complet de tous les fichiers et configurations
"""

import os
import sys
import re
from pathlib import Path
from collections import defaultdict
import traceback

class ComprehensiveErrorScanner:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.errors = defaultdict(list)
        self.warnings = defaultdict(list)
        self.total_checked = 0

    def log(self, message, level="INFO"):
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✓",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "SCAN": "🔍"
        }
        print(f"{icons.get(level, '')} {message}")

    def scan_character_files(self):
        """Scan complet de tous les fichiers des personnages"""
        self.log("Scan des personnages...", "SCAN")

        chars_path = self.base_path / "chars"
        if not chars_path.exists():
            return

        for char_folder in chars_path.iterdir():
            if not char_folder.is_dir():
                continue

            char_name = char_folder.name
            self.total_checked += 1

            # Vérifier fichier .def
            def_files = list(char_folder.glob("*.def"))
            if not def_files:
                self.errors["char_no_def"].append(char_name)
                continue

            def_file = def_files[0]

            try:
                content = def_file.read_text(encoding='utf-8', errors='ignore')

                # Vérifier SFF
                if not re.search(r'sprite\s*=\s*.+\.sff', content, re.IGNORECASE):
                    self.errors["char_no_sff_ref"].append(char_name)
                else:
                    sff_match = re.search(r'sprite\s*=\s*(.+)', content, re.IGNORECASE)
                    if sff_match:
                        sff_name = sff_match.group(1).strip().split(';')[0].strip()
                        sff_path = char_folder / sff_name
                        if not sff_path.exists():
                            self.errors["char_missing_sff"].append(f"{char_name} → {sff_name}")

                # Vérifier AIR
                if not re.search(r'anim\s*=\s*.+\.air', content, re.IGNORECASE):
                    self.errors["char_no_air_ref"].append(char_name)
                else:
                    air_match = re.search(r'anim\s*=\s*(.+)', content, re.IGNORECASE)
                    if air_match:
                        air_name = air_match.group(1).strip().split(';')[0].strip()
                        air_path = char_folder / air_name
                        if not air_path.exists():
                            self.errors["char_missing_air"].append(f"{char_name} → {air_name}")

                # Vérifier CMD
                cmd_match = re.search(r'cmd\s*=\s*(.+)', content, re.IGNORECASE)
                if cmd_match:
                    cmd_name = cmd_match.group(1).strip().split(';')[0].strip()
                    cmd_path = char_folder / cmd_name
                    if not cmd_path.exists():
                        self.errors["char_missing_cmd"].append(f"{char_name} → {cmd_name}")

                # Vérifier CNS
                cns_match = re.search(r'st\s*=\s*(.+)', content, re.IGNORECASE)
                if cns_match:
                    cns_name = cns_match.group(1).strip().split(';')[0].strip()
                    cns_path = char_folder / cns_name
                    if not cns_path.exists():
                        self.errors["char_missing_cns"].append(f"{char_name} → {cns_name}")

                # Vérifier SND
                snd_match = re.search(r'sound\s*=\s*(.+)', content, re.IGNORECASE)
                if snd_match:
                    snd_name = snd_match.group(1).strip().split(';')[0].strip()
                    snd_path = char_folder / snd_name
                    if not snd_path.exists():
                        self.warnings["char_missing_snd"].append(f"{char_name} → {snd_name}")

            except Exception as e:
                self.errors["char_read_error"].append(f"{char_name}: {str(e)}")

        self.log(f"Analysé {self.total_checked} personnages", "SUCCESS")

    def scan_stages(self):
        """Scan complet des stages"""
        self.log("Scan des stages...", "SCAN")

        stages_path = self.base_path / "stages"
        if not stages_path.exists():
            return

        stage_count = 0
        for stage_file in stages_path.glob("*.def"):
            stage_name = stage_file.stem
            stage_count += 1

            try:
                content = stage_file.read_text(encoding='utf-8', errors='ignore')

                # Vérifier SFF
                sff_match = re.search(r'spr\s*=\s*(.+)', content, re.IGNORECASE)
                if not sff_match:
                    self.errors["stage_no_spr"].append(stage_name)
                else:
                    sff_name = sff_match.group(1).strip().split(';')[0].strip()
                    sff_path = stages_path / sff_name
                    if not sff_path.exists():
                        self.errors["stage_missing_spr"].append(f"{stage_name} → {sff_name}")

                # Vérifier BGM
                bgm_match = re.search(r'bgmusic\s*=\s*(.+)', content, re.IGNORECASE)
                if bgm_match:
                    bgm_name = bgm_match.group(1).strip().split(';')[0].strip()
                    if bgm_name and bgm_name != '0':
                        bgm_path = self.base_path / "sound" / bgm_name
                        if not bgm_path.exists():
                            self.warnings["stage_missing_bgm"].append(f"{stage_name} → {bgm_name}")

            except Exception as e:
                self.errors["stage_read_error"].append(f"{stage_name}: {str(e)}")

        self.log(f"Analysé {stage_count} stages", "SUCCESS")

    def scan_system_config(self):
        """Scan de la configuration système"""
        self.log("Scan configuration système...", "SCAN")

        # system.def
        system_def = self.base_path / "data" / "system.def"
        if not system_def.exists():
            self.errors["system"].append("system.def manquant!")
            return

        try:
            content = system_def.read_text(encoding='utf-8', errors='ignore')

            # Vérifier fichiers critiques
            critical_files = [
                (r'spr\s*=\s*(.+)', "System SFF"),
                (r'snd\s*=\s*(.+)', "System SND"),
            ]

            for pattern, desc in critical_files:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    file_name = match.group(1).strip().split(';')[0].strip()
                    file_path = self.base_path / "data" / file_name
                    if not file_path.exists():
                        self.errors["system_file"].append(f"{desc} manquant: {file_name}")

            # Vérifier configuration Select Info
            if '[Select Info]' not in content:
                self.errors["system"].append("Section [Select Info] manquante!")

        except Exception as e:
            self.errors["system"].append(f"Erreur lecture system.def: {e}")

    def scan_fight_config(self):
        """Scan de la configuration fight"""
        self.log("Scan configuration fight...", "SCAN")

        fight_def = self.base_path / "data" / "fight.def"
        if not fight_def.exists():
            self.errors["fight"].append("fight.def manquant!")
            return

        try:
            content = fight_def.read_text(encoding='utf-8', errors='ignore')

            # Vérifier fichiers critiques
            if not re.search(r'spr\s*=\s*.+\.sff', content, re.IGNORECASE):
                self.errors["fight"].append("Fight SFF non spécifié!")

            if not re.search(r'snd\s*=\s*.+\.snd', content, re.IGNORECASE):
                self.warnings["fight"].append("Fight SND non spécifié!")

        except Exception as e:
            self.errors["fight"].append(f"Erreur lecture fight.def: {e}")

    def scan_select_def(self):
        """Scan du select.def"""
        self.log("Scan select.def...", "SCAN")

        select_def = self.base_path / "data" / "select.def"
        if not select_def.exists():
            self.errors["select"].append("select.def manquant!")
            return

        try:
            content = select_def.read_text(encoding='utf-8', errors='ignore')

            # Compter les personnages actifs
            chars_active = len([l for l in content.split('\n')
                               if l.strip() and not l.strip().startswith(';')
                               and not l.strip().startswith('[')])

            if chars_active < 50:
                self.warnings["select"].append(f"Seulement {chars_active} personnages actifs")

            # Vérifier sections critiques
            required_sections = ['[Characters]', '[ExtraStages]']
            for section in required_sections:
                if section not in content:
                    self.warnings["select"].append(f"Section {section} manquante")

        except Exception as e:
            self.errors["select"].append(f"Erreur lecture select.def: {e}")

    def scan_air_files(self):
        """Scan des fichiers AIR pour erreurs de syntaxe"""
        self.log("Scan fichiers AIR...", "SCAN")

        air_errors = 0
        air_count = 0

        for air_file in self.base_path.glob("**/*.air"):
            air_count += 1
            try:
                content = air_file.read_text(encoding='utf-8', errors='ignore')

                # Vérifier erreurs communes
                if 'Clsn2Default' in content and 'Clsn2Default:' not in content:
                    air_errors += 1
                    self.errors["air_syntax"].append(f"{air_file.parent.name}/{air_file.name}: Clsn2Default sans :")

                # Vérifier sprites manquants (lignes orphelines)
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith('[Begin Action'):
                        # Vérifier qu'il y a au moins une ligne de sprite après
                        has_sprite = False
                        for j in range(i+1, min(i+10, len(lines))):
                            if re.match(r'^\s*\d+\s*,\s*\d+', lines[j]):
                                has_sprite = True
                                break
                        if not has_sprite:
                            self.warnings["air_empty"].append(f"{air_file.parent.name}/{air_file.name}:{i+1}")

            except Exception as e:
                self.errors["air_read"].append(f"{air_file.name}: {str(e)}")

        self.log(f"Analysé {air_count} fichiers AIR, {air_errors} erreurs trouvées", "SUCCESS")

    def print_report(self):
        """Affiche le rapport complet"""
        print("\n" + "="*70)
        print("  🔍 RAPPORT COMPLET DES ERREURS")
        print("="*70 + "\n")

        total_errors = sum(len(e) for e in self.errors.values())
        total_warnings = sum(len(w) for w in self.warnings.values())

        print(f"Fichiers vérifiés: {self.total_checked}")
        print(f"❌ Erreurs critiques: {total_errors}")
        print(f"⚠️  Avertissements: {total_warnings}")
        print()

        if total_errors == 0 and total_warnings == 0:
            self.log("Aucune erreur détectée! 🎉", "SUCCESS")
            return

        # Afficher les erreurs par catégorie
        if self.errors:
            print("="*70)
            print("  ❌ ERREURS CRITIQUES")
            print("="*70 + "\n")

            for error_type, errors in sorted(self.errors.items()):
                if errors:
                    print(f"\n📌 {error_type.replace('_', ' ').upper()} ({len(errors)})")
                    print("─" * 70)
                    for error in errors[:20]:  # Limiter à 20 par catégorie
                        print(f"  • {error}")
                    if len(errors) > 20:
                        print(f"  ... et {len(errors) - 20} autres")

        if self.warnings:
            print("\n" + "="*70)
            print("  ⚠️  AVERTISSEMENTS")
            print("="*70 + "\n")

            for warn_type, warnings in sorted(self.warnings.items()):
                if warnings:
                    print(f"\n📌 {warn_type.replace('_', ' ').upper()} ({len(warnings)})")
                    print("─" * 70)
                    for warning in warnings[:10]:  # Limiter à 10 par catégorie
                        print(f"  • {warning}")
                    if len(warnings) > 10:
                        print(f"  ... et {len(warnings) - 10} autres")

        print("\n" + "="*70)

    def save_report(self):
        """Sauvegarde le rapport"""
        report_file = self.base_path / "ERROR_REPORT_COMPLETE.txt"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("  RAPPORT COMPLET DES ERREURS - KOF ULTIMATE\n")
            f.write("="*70 + "\n\n")

            f.write(f"Fichiers vérifiés: {self.total_checked}\n")
            f.write(f"Erreurs: {sum(len(e) for e in self.errors.values())}\n")
            f.write(f"Avertissements: {sum(len(w) for w in self.warnings.values())}\n\n")

            if self.errors:
                f.write("\nERREURS CRITIQUES:\n")
                f.write("="*70 + "\n\n")
                for error_type, errors in sorted(self.errors.items()):
                    if errors:
                        f.write(f"\n{error_type.upper()}:\n")
                        f.write("-"*70 + "\n")
                        for error in errors:
                            f.write(f"  • {error}\n")

            if self.warnings:
                f.write("\n\nAVERTISSEMENTS:\n")
                f.write("="*70 + "\n\n")
                for warn_type, warnings in sorted(self.warnings.items()):
                    if warnings:
                        f.write(f"\n{warn_type.upper()}:\n")
                        f.write("-"*70 + "\n")
                        for warning in warnings:
                            f.write(f"  • {warning}\n")

        self.log(f"Rapport sauvegardé: {report_file.name}", "SUCCESS")

    def run(self):
        """Lance le scan complet"""
        print("\n" + "="*70)
        print("  🔍 SCAN COMPLET DE TOUTES LES ERREURS")
        print("="*70 + "\n")

        self.scan_character_files()
        self.scan_stages()
        self.scan_system_config()
        self.scan_fight_config()
        self.scan_select_def()
        self.scan_air_files()

        self.print_report()
        self.save_report()

        return len(self.errors) == 0

if __name__ == "__main__":
    scanner = ComprehensiveErrorScanner()
    success = scanner.run()
    sys.exit(0 if success else 1)
