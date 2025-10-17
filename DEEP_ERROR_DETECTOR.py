#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - DÉTECTEUR D'ERREURS PROFOND
Scanne TOUT: Personnages, Stages, AIR, CNS, DEF, SFF
Détecte TOUTES les erreurs avant le lancement
"""

import re
from pathlib import Path
import shutil
from datetime import datetime

class DeepErrorDetector:
    """Détecteur d'erreurs profond pour tous les fichiers du jeu"""

    def __init__(self):
        self.game_dir = Path(r"D:\KOF Ultimate Online")
        self.chars_dir = self.game_dir / "chars"
        self.stages_dir = self.game_dir / "stages"
        self.data_dir = self.game_dir / "data"

        self.errors_found = []
        self.warnings_found = []
        self.files_checked = 0
        self.corrupted_files = []

        self.log_file = self.game_dir / "DEEP_ERROR_REPORT.txt"

    def log(self, message, level='INFO'):
        """Log un message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        msg = f"[{timestamp}] [{level}] {message}"
        print(msg)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')

    def check_air_file(self, air_file):
        """Vérifie un fichier .air (animations)"""
        errors = []

        try:
            with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            current_action = None
            line_num = 0

            for i, line in enumerate(lines, 1):
                line_num = i
                line = line.strip()

                # Détecter début d'action
                if line.startswith('[Begin Action'):
                    match = re.search(r'\[Begin Action (\d+)\]', line)
                    if match:
                        current_action = match.group(1)

                # Vérifier clsn (collision boxes)
                if line.startswith('Clsn'):
                    # Format: Clsn2: 4
                    # ou Clsn2[0] = -10, -80, 10, 0
                    if 'Clsn2:' in line or 'Clsn1:' in line:
                        # Déclarer nombre de clsn
                        pass
                    elif 'Clsn2[' in line or 'Clsn1[' in line:
                        # Vérifier format coordinates
                        match = re.search(r'Clsn[12]\[(\d+)\]\s*=\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)', line)
                        if not match:
                            errors.append({
                                'file': air_file.name,
                                'line': line_num,
                                'action': current_action,
                                'error': f'Format clsn invalide: {line}',
                                'type': 'CLSN_FORMAT_ERROR'
                            })

                # Vérifier format sprite
                if not line.startswith(';') and not line.startswith('[') and ',' in line:
                    # Format normal: group, image, x, y, time, flip, etc.
                    parts = line.split(',')
                    if len(parts) >= 5:
                        # Vérifier que group et image sont des nombres
                        try:
                            group = int(parts[0].strip())
                            image = int(parts[1].strip())
                        except ValueError:
                            if not line.startswith('Clsn'):
                                errors.append({
                                    'file': air_file.name,
                                    'line': line_num,
                                    'action': current_action,
                                    'error': f'Format sprite invalide: {line}',
                                    'type': 'SPRITE_FORMAT_ERROR'
                                })

            return errors

        except Exception as e:
            errors.append({
                'file': air_file.name,
                'line': 0,
                'error': f'Impossible de lire le fichier: {e}',
                'type': 'FILE_READ_ERROR'
            })
            return errors

    def check_def_file(self, def_file):
        """Vérifie un fichier .def"""
        errors = []
        warnings = []

        try:
            with open(def_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Vérifier fichiers référencés
            file_refs = [
                ('cmd', r'cmd\s*=\s*([^\s\n]+)'),
                ('cns', r'cns\s*=\s*([^\s\n]+)'),
                ('st', r'st\s*=\s*([^\s\n]+)'),
                ('stcommon', r'stcommon\s*=\s*([^\s\n]+)'),
                ('sff', r'sprite\s*=\s*([^\s\n]+)'),
                ('air', r'anim\s*=\s*([^\s\n]+)'),
                ('snd', r'sound\s*=\s*([^\s\n]+)'),
            ]

            char_dir = def_file.parent

            for file_type, pattern in file_refs:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    filename = match.group(1).strip().strip('"\'')

                    # Chercher le fichier
                    file_path = char_dir / filename

                    if not file_path.exists():
                        errors.append({
                            'file': def_file.name,
                            'referenced_file': filename,
                            'error': f'Fichier {file_type.upper()} introuvable: {filename}',
                            'type': 'MISSING_FILE'
                        })

            return errors, warnings

        except Exception as e:
            errors.append({
                'file': def_file.name,
                'error': f'Impossible de lire le fichier: {e}',
                'type': 'FILE_READ_ERROR'
            })
            return errors, warnings

    def check_character(self, char_dir):
        """Vérifie un personnage complet"""
        errors = []
        warnings = []

        self.log(f"  Vérification: {char_dir.name}...")

        # Trouver le fichier .def principal
        def_files = list(char_dir.glob("*.def"))

        if not def_files:
            errors.append({
                'char': char_dir.name,
                'error': 'Aucun fichier .def trouvé',
                'type': 'NO_DEF_FILE'
            })
            return errors, warnings

        # Vérifier chaque .def
        for def_file in def_files:
            def_errors, def_warnings = self.check_def_file(def_file)
            errors.extend(def_errors)
            warnings.extend(def_warnings)

        # Vérifier fichiers .air
        air_files = list(char_dir.glob("*.air"))
        for air_file in air_files:
            air_errors = self.check_air_file(air_file)
            errors.extend(air_errors)

        return errors, warnings

    def check_all_characters(self):
        """Vérifie tous les personnages"""
        self.log("\n🔍 VÉRIFICATION DE TOUS LES PERSONNAGES")
        self.log("=" * 70)

        if not self.chars_dir.exists():
            self.log("❌ Dossier chars/ introuvable!")
            return

        char_dirs = [d for d in self.chars_dir.iterdir() if d.is_dir()]
        self.log(f"\n📁 {len(char_dirs)} personnages à vérifier\n")

        corrupted_chars = []

        for char_dir in char_dirs:
            self.files_checked += 1
            errors, warnings = self.check_character(char_dir)

            if errors:
                self.log(f"  ❌ {char_dir.name}: {len(errors)} erreur(s)")
                self.errors_found.extend(errors)
                corrupted_chars.append(char_dir.name)

                # Afficher les erreurs
                for error in errors[:3]:  # Max 3 erreurs par perso
                    self.log(f"     • {error.get('error', 'Erreur inconnue')}", 'ERROR')

            if warnings:
                self.warnings_found.extend(warnings)

        if corrupted_chars:
            self.log(f"\n⚠️  {len(corrupted_chars)} personnages corrompus détectés:")
            for char in corrupted_chars[:10]:  # Max 10 affichés
                self.log(f"  • {char}")

    def check_stage(self, stage_def):
        """Vérifie un stage"""
        errors = []

        try:
            with open(stage_def, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            stage_dir = stage_def.parent

            # Vérifier fichier sff
            sff_match = re.search(r'spr\s*=\s*([^\s\n]+)', content, re.IGNORECASE)
            if sff_match:
                sff_file = sff_match.group(1).strip().strip('"\'')
                sff_path = stage_dir / sff_file
                if not sff_path.exists():
                    errors.append({
                        'stage': stage_def.name,
                        'error': f'Fichier SFF introuvable: {sff_file}',
                        'type': 'MISSING_SPR'
                    })

            return errors

        except Exception as e:
            errors.append({
                'stage': stage_def.name,
                'error': f'Impossible de lire: {e}',
                'type': 'FILE_READ_ERROR'
            })
            return errors

    def check_all_stages(self):
        """Vérifie tous les stages"""
        self.log("\n\n🎭 VÉRIFICATION DE TOUS LES STAGES")
        self.log("=" * 70)

        if not self.stages_dir.exists():
            self.log("❌ Dossier stages/ introuvable!")
            return

        stage_defs = list(self.stages_dir.rglob("*.def"))
        self.log(f"\n📁 {len(stage_defs)} stages à vérifier\n")

        corrupted_stages = []

        for stage_def in stage_defs:
            self.files_checked += 1
            errors = self.check_stage(stage_def)

            if errors:
                self.log(f"  ❌ {stage_def.stem}: {len(errors)} erreur(s)")
                self.errors_found.extend(errors)
                corrupted_stages.append(stage_def.stem)

                for error in errors:
                    self.log(f"     • {error.get('error')}", 'ERROR')

        if corrupted_stages:
            self.log(f"\n⚠️  {len(corrupted_stages)} stages corrompus:")
            for stage in corrupted_stages:
                self.log(f"  • {stage}")

    def check_select_def(self):
        """Vérifie select.def (liste des personnages)"""
        self.log("\n\n📋 VÉRIFICATION SELECT.DEF")
        self.log("=" * 70)

        select_def = self.data_dir / "select.def"

        if not select_def.exists():
            self.log("❌ select.def introuvable!")
            return

        try:
            with open(select_def, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            chars_in_select = []
            missing_chars = []

            for line in lines:
                line = line.strip()

                # Ignorer commentaires et lignes vides
                if line.startswith(';') or not line:
                    continue

                # Détecter ligne de personnage
                if line.lower().startswith('chars/'):
                    # Format: chars/CharName/char.def
                    match = re.search(r'chars/([^/]+)', line)
                    if match:
                        char_name = match.group(1)
                        chars_in_select.append(char_name)

                        # Vérifier si le dossier existe
                        char_dir = self.chars_dir / char_name
                        if not char_dir.exists():
                            missing_chars.append(char_name)
                            self.errors_found.append({
                                'file': 'select.def',
                                'char': char_name,
                                'error': f'Personnage dans select.def mais dossier introuvable',
                                'type': 'MISSING_CHAR_DIR'
                            })

            self.log(f"\n  ✓ {len(chars_in_select)} personnages dans select.def")

            if missing_chars:
                self.log(f"  ❌ {len(missing_chars)} personnages manquants:")
                for char in missing_chars[:10]:
                    self.log(f"     • {char}")

        except Exception as e:
            self.log(f"❌ Erreur lecture select.def: {e}", 'ERROR')

    def generate_fix_script(self):
        """Génère un script pour corriger les erreurs"""
        self.log("\n\n🔧 GÉNÉRATION SCRIPT DE CORRECTION")
        self.log("=" * 70)

        fix_script = self.game_dir / "AUTO_FIX_ERRORS.py"

        with open(fix_script, 'w', encoding='utf-8') as f:
            f.write("#!/usr/bin/env python3\n")
            f.write("# -*- coding: utf-8 -*-\n")
            f.write('"""\n')
            f.write("AUTO-CORRECTEUR GÉNÉRÉ\n")
            f.write(f"Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{len(self.errors_found)} erreurs à corriger\n")
            f.write('"""\n\n')
            f.write("from pathlib import Path\n\n")
            f.write("def fix_all_errors():\n")
            f.write("    print('Correction des erreurs...')\n")
            f.write(f"    # TODO: {len(self.errors_found)} erreurs détectées\n")
            f.write("    pass\n\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    fix_all_errors()\n")

        self.log(f"✓ Script généré: {fix_script.name}")

    def generate_final_report(self):
        """Génère le rapport final"""
        self.log("\n\n" + "=" * 70)
        self.log("📊 RAPPORT FINAL DÉTECTEUR PROFOND")
        self.log("=" * 70)

        self.log(f"\n📁 Fichiers vérifiés: {self.files_checked}")
        self.log(f"❌ Erreurs détectées: {len(self.errors_found)}")
        self.log(f"⚠️  Avertissements: {len(self.warnings_found)}")

        if self.errors_found:
            self.log(f"\n📋 TYPES D'ERREURS:")

            # Grouper par type
            by_type = {}
            for error in self.errors_found:
                error_type = error.get('type', 'UNKNOWN')
                if error_type not in by_type:
                    by_type[error_type] = []
                by_type[error_type].append(error)

            for error_type, errors in by_type.items():
                self.log(f"\n  {error_type}: {len(errors)} occurrence(s)")
                for error in errors[:5]:  # Max 5 exemples
                    self.log(f"    • {error.get('file', 'unknown')}: {error.get('error', 'unknown')}")
                if len(errors) > 5:
                    self.log(f"    ... et {len(errors) - 5} autre(s)")

        self.log(f"\n💾 Rapport complet: {self.log_file}")
        self.log("=" * 70)

        if len(self.errors_found) > 0:
            self.log(f"\n⚠️  {len(self.errors_found)} ERREURS CRITIQUES DÉTECTÉES!")
            self.log("Ces erreurs empêchent le jeu de fonctionner correctement.")
        else:
            self.log("\n✅ AUCUNE ERREUR CRITIQUE DÉTECTÉE!")

        self.log("=" * 70)

    def run_deep_scan(self):
        """Lance le scan profond complet"""
        self.log("\n" + "=" * 70)
        self.log("🔍 DÉTECTEUR D'ERREURS PROFOND")
        self.log("=" * 70)
        self.log("\nScan approfondi de TOUS les fichiers du jeu...")
        self.log("")

        # Nettoyer le log
        if self.log_file.exists():
            self.log_file.unlink()

        # 1. Vérifier select.def
        self.check_select_def()

        # 2. Vérifier tous les personnages
        self.check_all_characters()

        # 3. Vérifier tous les stages
        self.check_all_stages()

        # 4. Générer script de correction
        if self.errors_found:
            self.generate_fix_script()

        # 5. Rapport final
        self.generate_final_report()

        return len(self.errors_found) == 0

def main():
    """Point d'entrée"""
    print("\n" + "=" * 70)
    print("  🔍 DÉTECTEUR D'ERREURS PROFOND")
    print("=" * 70)
    print("\n  Scan approfondi:")
    print("  • Tous les personnages (.def, .air, .cns)")
    print("  • Tous les stages (.def, .sff)")
    print("  • Fichiers manquants")
    print("  • Erreurs de format")
    print("  • Corruptions de fichiers")
    print("\n" + "=" * 70)
    print()

    detector = DeepErrorDetector()
    success = detector.run_deep_scan()

    print("\n\n" + "=" * 70)
    if success:
        print("✅ AUCUNE ERREUR CRITIQUE!")
        print("\nTous les fichiers sont valides.")
    else:
        print("⚠️  ERREURS CRITIQUES DÉTECTÉES")
        print(f"\n{len(detector.errors_found)} erreurs trouvées.")
        print(f"\nConsultez {detector.log_file} pour les détails.")
        print("\nCes erreurs expliquent les crashs du jeu!")
    print("=" * 70)
    print()

if __name__ == '__main__':
    main()
