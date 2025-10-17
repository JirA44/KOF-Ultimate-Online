#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - AUTO-CORRECTEUR FICHIERS CORROMPUS
Répare automatiquement TOUS les fichiers corrompus détectés
"""

import re
from pathlib import Path
import shutil
from datetime import datetime

class CorruptedFileFixer:
    """Correcteur automatique de fichiers corrompus"""

    def __init__(self):
        self.game_dir = Path(r"D:\KOF Ultimate Online")
        self.chars_dir = self.game_dir / "chars"
        self.stages_dir = self.game_dir / "stages"
        self.data_dir = self.game_dir / "data"

        self.backup_dir = self.game_dir / "backups_corrupted_fix"
        self.backup_dir.mkdir(exist_ok=True)

        self.fixes_applied = []
        self.files_removed = []
        self.select_def_cleaned = False

    def log(self, message, level='INFO'):
        """Log un message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def backup_file(self, filepath):
        """Backup avant modification"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{filepath.name}.corrupted_backup_{timestamp}"
            backup_path = self.backup_dir / backup_name
            shutil.copy2(filepath, backup_path)
            return True
        except:
            return False

    def fix_air_clsn_errors(self, air_file):
        """Corrige les erreurs clsn2 dans fichiers .air"""
        try:
            with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            modified = False
            fixed_lines = []
            in_action = False
            current_action = None

            for i, line in enumerate(lines):
                original_line = line

                # Détecter action
                if '[Begin Action' in line:
                    match = re.search(r'\[Begin Action (\d+)\]', line)
                    if match:
                        current_action = match.group(1)
                        in_action = True

                # Corriger format clsn invalide
                if in_action and ('Clsn2[' in line or 'Clsn1[' in line):
                    # Format attendu: Clsn2[0] = -10, -80, 10, 0
                    # Corriger formats invalides

                    # Enlever espaces multiples
                    line = re.sub(r'\s+', ' ', line)

                    # Corriger virgules manquantes
                    match = re.search(r'(Clsn[12]\[\d+\])\s*=\s*(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)', line)
                    if match:
                        clsn_part = match.group(1)
                        v1, v2, v3, v4 = match.group(2), match.group(3), match.group(4), match.group(5)
                        line = f"{clsn_part} = {v1}, {v2}, {v3}, {v4}\n"
                        modified = True

                # Corriger format sprite invalide
                if in_action and not line.strip().startswith(';') and not line.strip().startswith('['):
                    # Format: group, image, x, y, time
                    # Corriger: "5.0, 0,0, 2, H" → "5, 0, 0, 0, 2"
                    if '.' in line and ',' in line:
                        # Enlever les décimales
                        line = re.sub(r'(\d+)\.(\d+)', r'\1', line)
                        modified = True

                    # Corriger espaces manquants après virgules
                    if ',0,' in line or ', 0,' in line:
                        parts = line.split(',')
                        if len(parts) >= 5:
                            # Nettoyer et reformater
                            cleaned_parts = [p.strip() for p in parts[:5]]
                            line = ', '.join(cleaned_parts) + '\n'
                            modified = True

                fixed_lines.append(line)

            if modified:
                self.backup_file(air_file)
                with open(air_file, 'w', encoding='utf-8') as f:
                    f.writelines(fixed_lines)

                self.fixes_applied.append(f"Corrigé {air_file.name}")
                return True

            return False

        except Exception as e:
            self.log(f"Erreur correction {air_file.name}: {e}", 'ERROR')
            return False

    def create_missing_common1_cns(self):
        """Crée un fichier common1.cns par défaut si manquant"""
        common1_content = """; Common1.cns - États communs
; Fichier généré automatiquement

[Statedef -1]
; États communs pour tous les personnages
"""

        # Créer common1.cns dans data/
        common1_path = self.data_dir / "common1.cns"

        if not common1_path.exists():
            with open(common1_path, 'w', encoding='utf-8') as f:
                f.write(common1_content)

            self.fixes_applied.append("Créé common1.cns manquant")
            self.log("✓ Créé common1.cns dans data/")
            return True

        return False

    def remove_corrupted_from_select(self):
        """Enlève les personnages corrompus de select.def"""
        select_def = self.data_dir / "select.def"

        if not select_def.exists():
            return False

        try:
            self.backup_file(select_def)

            with open(select_def, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Liste des personnages connus corrompus
            corrupted_chars = [
                'Akiha Yagami', 'Akiha Yagami DK', 'Athena Asamiya MI KOFM',
                'Athena-Heidern', 'BLAKE V3-1.1', 'Clone Zero', 'Eputh Blood-KOFM',
                'Final Adel', 'Final Goeniko', 'GARS', 'Kaori Yumiko',
                'kfm', 'Lane.Blood-CKOFM', 'LUMIEL', 'Orochi Kyo WF',
                'Unleashesd God Kula', 'Voltage Zeroko-Pre'
            ]

            cleaned_lines = []
            removed_count = 0

            for line in lines:
                # Vérifier si la ligne contient un perso corrompu
                is_corrupted = False

                for corrupted in corrupted_chars:
                    if corrupted.lower() in line.lower() and 'chars/' in line.lower():
                        is_corrupted = True
                        removed_count += 1
                        self.log(f"  Enlevé de select.def: {corrupted}")
                        break

                if not is_corrupted:
                    cleaned_lines.append(line)

            # Écrire select.def nettoyé
            with open(select_def, 'w', encoding='utf-8') as f:
                f.writelines(cleaned_lines)

            self.fixes_applied.append(f"Enlevé {removed_count} persos corrompus de select.def")
            self.select_def_cleaned = True
            return True

        except Exception as e:
            self.log(f"Erreur nettoyage select.def: {e}", 'ERROR')
            return False

    def fix_stage_def_files(self):
        """Corrige les fichiers .def de stages"""
        if not self.stages_dir.exists():
            return 0

        fixed_count = 0
        stage_defs = list(self.stages_dir.rglob("*.def"))

        for stage_def in stage_defs:
            try:
                with open(stage_def, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                modified = False

                # Chercher référence spr invalide
                spr_match = re.search(r'spr\s*=\s*([^\s\n]+)', content, re.IGNORECASE)

                if spr_match:
                    spr_file = spr_match.group(1).strip().strip('"\'')
                    stage_dir = stage_def.parent

                    # Si fichier SFF n'existe pas
                    if not (stage_dir / spr_file).exists():
                        # Chercher un .sff disponible dans le même dossier
                        available_sff = list(stage_dir.glob("*.sff"))

                        if available_sff:
                            # Utiliser le premier .sff trouvé
                            new_spr = available_sff[0].name
                            content = re.sub(
                                r'(spr\s*=\s*)([^\s\n]+)',
                                f'spr = {new_spr}',
                                content,
                                flags=re.IGNORECASE
                            )
                            modified = True
                            self.log(f"  Corrigé stage {stage_def.stem}: {spr_file} → {new_spr}")
                        else:
                            # Pas de .sff disponible, créer un debugbg
                            content = re.sub(
                                r'(spr\s*=\s*)([^\s\n]+)',
                                'spr = debugbg',
                                content,
                                flags=re.IGNORECASE
                            )
                            modified = True
                            self.log(f"  Stage {stage_def.stem}: Utilise debugbg")

                if modified:
                    self.backup_file(stage_def)
                    with open(stage_def, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixed_count += 1

            except Exception as e:
                continue

        if fixed_count > 0:
            self.fixes_applied.append(f"Corrigé {fixed_count} stages")

        return fixed_count

    def fix_all_air_files(self):
        """Corrige tous les fichiers .air corrompus"""
        if not self.chars_dir.exists():
            return 0

        self.log("\n🔧 CORRECTION FICHIERS .AIR")
        self.log("=" * 70)

        air_files = list(self.chars_dir.rglob("*.air"))
        fixed_count = 0

        for air_file in air_files:
            if self.fix_air_clsn_errors(air_file):
                fixed_count += 1
                self.log(f"  ✓ {air_file.parent.name}/{air_file.name}")

        self.log(f"\n✓ {fixed_count} fichiers .air corrigés")
        return fixed_count

    def run_auto_fix(self):
        """Lance toutes les corrections automatiques"""
        self.log("\n" + "=" * 70)
        self.log("🔧 AUTO-CORRECTEUR FICHIERS CORROMPUS")
        self.log("=" * 70)
        self.log("\nRéparation automatique en cours...")
        self.log("")

        # 1. Créer common1.cns si manquant
        self.log("\n📝 Création fichiers manquants...")
        self.create_missing_common1_cns()

        # 2. Corriger fichiers .air
        air_fixed = self.fix_all_air_files()

        # 3. Corriger stages
        self.log("\n🎭 Correction stages...")
        stages_fixed = self.fix_stage_def_files()

        # 4. Nettoyer select.def
        self.log("\n📋 Nettoyage select.def...")
        self.remove_corrupted_from_select()

        # Rapport final
        self.log("\n" + "=" * 70)
        self.log("📊 RAPPORT FINAL")
        self.log("=" * 70)

        self.log(f"\n✅ Corrections appliquées:")
        for fix in self.fixes_applied:
            self.log(f"  • {fix}")

        self.log(f"\n💾 Backups: {self.backup_dir}")
        self.log("=" * 70)

        if len(self.fixes_applied) > 0:
            self.log(f"\n✅ {len(self.fixes_applied)} CORRECTIONS APPLIQUÉES!")
            self.log("Le jeu devrait maintenant démarrer correctement.")
        else:
            self.log("\n⚠️  Aucune correction automatique possible")

        self.log("=" * 70)

        return len(self.fixes_applied) > 0

def main():
    """Point d'entrée"""
    print("\n" + "=" * 70)
    print("  🔧 AUTO-CORRECTEUR FICHIERS CORROMPUS")
    print("=" * 70)
    print("\n  Corrections automatiques:")
    print("  • Fichiers .air corrompus (clsn2, format)")
    print("  • Fichiers manquants (common1.cns)")
    print("  • Stages avec .sff manquants")
    print("  • Nettoyage select.def")
    print("\n" + "=" * 70)
    print()

    fixer = CorruptedFileFixer()
    success = fixer.run_auto_fix()

    print("\n\n" + "=" * 70)
    if success:
        print("✅ CORRECTIONS APPLIQUÉES!")
        print("\nLe jeu devrait maintenant démarrer sans erreurs.")
        print("\nRelancez le jeu pour vérifier.")
    else:
        print("⚠️  CORRECTIONS IMPOSSIBLES")
        print("\nCertaines erreurs nécessitent intervention manuelle.")
    print("=" * 70)
    print()

if __name__ == '__main__':
    main()
