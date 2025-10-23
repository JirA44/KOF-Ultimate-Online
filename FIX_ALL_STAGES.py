#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIX ALL STAGES
Corrige TOUTES les erreurs dans les fichiers de stages
"""

import re
import shutil
from pathlib import Path
from datetime import datetime

class StagesFixer:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.stages_path = self.base_path / "stages"
        self.fixes = 0

    def log(self, message, level="INFO"):
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "FIX": "🔧"}
        print(f"{icons.get(level, '')} {message}")

    def check_stage_sff_reference(self, stage_def):
        """Vérifie si la référence au .sff dans un stage est correcte"""
        try:
            content = stage_def.read_text(encoding='utf-8', errors='ignore')

            # Chercher la ligne spr = xxx.sff
            match = re.search(r'spr\s*=\s*(.+\.sff)', content, re.IGNORECASE)

            if not match:
                return False, "Pas de référence spr trouvée"

            sff_name = match.group(1).strip()
            sff_path = self.stages_path / sff_name

            if not sff_path.exists():
                # Chercher le bon fichier .sff
                stage_name = stage_def.stem

                # Essayer avec le nom du stage
                possible_sff = self.stages_path / f"{stage_name}.sff"
                if possible_sff.exists():
                    return False, f"Référence incorrecte: '{sff_name}' devrait être '{stage_name}.sff'"

                # Chercher tous les .sff dans le dossier
                all_sff = list(self.stages_path.glob('*.sff'))

                # Chercher un .sff qui contient une partie du nom du stage
                for sff_file in all_sff:
                    if stage_name.lower().replace(' ', '') in sff_file.stem.lower().replace(' ', ''):
                        return False, f"Référence incorrecte: '{sff_name}' devrait être '{sff_file.name}'"

                return False, f"Fichier '{sff_name}' introuvable"

            return True, "OK"

        except Exception as e:
            return False, f"Erreur: {e}"

    def fix_stage_sff_reference(self, stage_def):
        """Corrige la référence au .sff dans un stage"""
        try:
            content = stage_def.read_text(encoding='utf-8', errors='ignore')
            original_content = content

            # Chercher la ligne spr = xxx.sff
            match = re.search(r'spr\s*=\s*(.+\.sff)', content, re.IGNORECASE)

            if not match:
                return False

            old_sff_name = match.group(1).strip()
            stage_name = stage_def.stem

            # Essayer de trouver le bon .sff
            correct_sff = None

            # 1. Essayer avec le nom exact du stage
            possible = self.stages_path / f"{stage_name}.sff"
            if possible.exists():
                correct_sff = possible.name

            # 2. Chercher un .sff qui contient le nom du stage
            if not correct_sff:
                all_sff = list(self.stages_path.glob('*.sff'))
                for sff_file in all_sff:
                    # Normaliser pour comparaison
                    stage_normalized = stage_name.lower().replace(' ', '').replace('-', '')
                    sff_normalized = sff_file.stem.lower().replace(' ', '').replace('-', '')

                    if stage_normalized in sff_normalized or sff_normalized in stage_normalized:
                        correct_sff = sff_file.name
                        break

            if correct_sff and correct_sff != old_sff_name:
                # Remplacer
                content = re.sub(
                    r'(spr\s*=\s*)(.+\.sff)',
                    f'\\1{correct_sff}',
                    content,
                    flags=re.IGNORECASE
                )

                if content != original_content:
                    # Backup
                    backup = stage_def.with_suffix('.def.backup_fix')
                    if not backup.exists():
                        shutil.copy2(stage_def, backup)

                    # Écrire
                    stage_def.write_text(content, encoding='utf-8')
                    self.log(f"  ✅ {stage_def.name}: '{old_sff_name}' → '{correct_sff}'", "SUCCESS")
                    self.fixes += 1
                    return True

            return False

        except Exception as e:
            self.log(f"  ❌ Erreur correction {stage_def.name}: {e}", "ERROR")
            return False

    def check_stage_animations(self, stage_def):
        """Vérifie que les animations référencées existent"""
        try:
            content = stage_def.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')

            # Chercher les références à actionno
            action_refs = set()
            for line in lines:
                match = re.search(r'actionno\s*=\s*(\d+)', line, re.IGNORECASE)
                if match:
                    action_refs.add(int(match.group(1)))

            # Chercher les définitions [Begin Action X]
            action_defs = set()
            for line in lines:
                match = re.search(r'\[Begin Action\s+(\d+)\]', line, re.IGNORECASE)
                if match:
                    action_defs.add(int(match.group(1)))

            # Trouver les actions manquantes
            missing = action_refs - action_defs

            if missing:
                return False, f"Actions manquantes: {missing}"

            return True, "OK"

        except Exception as e:
            return False, f"Erreur: {e}"

    def scan_all_stages(self):
        """Scanne tous les stages"""
        self.log("Scan de tous les stages...", "INFO")

        if not self.stages_path.exists():
            self.log("❌ Dossier stages/ introuvable", "ERROR")
            return []

        stage_defs = list(self.stages_path.glob('*.def'))
        self.log(f"Trouvé {len(stage_defs)} fichiers .def", "INFO")

        problems = []

        for stage_def in sorted(stage_defs):
            # Vérifier référence .sff
            is_valid_sff, msg_sff = self.check_stage_sff_reference(stage_def)

            if not is_valid_sff:
                problems.append((stage_def.name, "SFF", msg_sff))
                self.log(f"  ❌ {stage_def.name}: {msg_sff}", "ERROR")

            # Vérifier animations
            is_valid_anim, msg_anim = self.check_stage_animations(stage_def)

            if not is_valid_anim:
                problems.append((stage_def.name, "ANIM", msg_anim))
                self.log(f"  ⚠️  {stage_def.name}: {msg_anim}", "ERROR")

        return problems

    def fix_all_stages(self):
        """Corrige tous les stages"""
        self.log("\n🔧 Correction de tous les stages...", "FIX")

        if not self.stages_path.exists():
            return

        stage_defs = list(self.stages_path.glob('*.def'))

        for stage_def in sorted(stage_defs):
            self.fix_stage_sff_reference(stage_def)

    def run_full_fix(self):
        """Lance le scan et la correction"""
        print("\n" + "="*80)
        print("  FIX ALL STAGES - Correction complète des stages")
        print("="*80 + "\n")

        # 1. Scanner
        self.log("=== SCAN DES STAGES ===", "INFO")
        problems = self.scan_all_stages()

        if problems:
            self.log(f"\n❌ {len(problems)} problèmes détectés", "ERROR")

            # 2. Corriger
            self.log("\n=== CORRECTION ===", "FIX")
            self.fix_all_stages()
        else:
            self.log("\n✅ Tous les stages sont corrects", "SUCCESS")

        # RÉSUMÉ
        print("\n" + "="*80)
        print("  RÉSUMÉ")
        print("="*80)
        print(f"✅ Corrections appliquées: {self.fixes}")

        if self.fixes > 0:
            print("\n💾 Backups créés: *.def.backup_fix")
            print("✅ Relancez le jeu pour tester")

        print("="*80 + "\n")

if __name__ == "__main__":
    fixer = StagesFixer()
    fixer.run_full_fix()
