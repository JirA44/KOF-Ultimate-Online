#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - SCANNER UNIVERSEL D'ERREURS
Détecte et corrige AUTOMATIQUEMENT toutes les erreurs
"""

import re
from pathlib import Path
import shutil
from datetime import datetime

class UniversalErrorScanner:
    """Scanner universel qui détecte TOUTES les erreurs"""

    def __init__(self):
        self.game_dir = Path(r"D:\KOF Ultimate Online")
        self.chars_dir = self.game_dir / "chars"
        self.stages_dir = self.game_dir / "stages"
        self.data_dir = self.game_dir / "data"

        self.backup_dir = self.game_dir / "backups_auto_fix"
        self.backup_dir.mkdir(exist_ok=True)

        self.errors_found = []
        self.fixes_applied = []

    def log(self, message, level='INFO'):
        """Log un message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def backup_file(self, filepath):
        """Backup avant modification"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{filepath.name}.autofix_{timestamp}"
            backup_path = self.backup_dir / backup_name
            shutil.copy2(filepath, backup_path)
            return True
        except:
            return False

    def scan_and_fix_air_files(self):
        """Scanne et corrige TOUS les .air"""
        self.log("\n🔍 SCAN FICHIERS .AIR")
        self.log("=" * 70)

        air_files = list(self.chars_dir.rglob("*.air"))
        fixed_count = 0

        for air_file in air_files:
            if self.fix_air_file(air_file):
                fixed_count += 1
                self.log(f"  ✓ Corrigé: {air_file.parent.name}/{air_file.name}")

        self.log(f"\n✅ {fixed_count}/{len(air_files)} fichiers .air corrigés")
        return fixed_count

    def fix_air_file(self, air_file):
        """Corrige un fichier .air"""
        try:
            with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            fixed_lines = []
            modified = False

            for i, line in enumerate(lines):
                original_line = line

                # ERREUR 1: Clsn2[0] = x, y, z, w SPRITE_DATA sur même ligne
                match = re.match(r'^(\s*Clsn[12]\[\d+\]\s*=\s*-?\d+,\s*-?\d+,\s*-?\d+,\s*-?\d+)\s+(\d+.+)$', line)
                if match:
                    clsn_part = match.group(1)
                    sprite_part = match.group(2)
                    fixed_lines.append(clsn_part + '\n')
                    fixed_lines.append(sprite_part + '\n')
                    modified = True
                    self.errors_found.append(f"{air_file.name}:{i+1} - clsn2 + sprite sur même ligne")
                    continue

                # ERREUR 2: Espaces multiples dans clsn
                if 'Clsn' in line and '=' in line:
                    fixed_line = re.sub(r'\s+', ' ', line.strip()) + '\n'
                    if fixed_line != line:
                        line = fixed_line
                        modified = True

                # ERREUR 3: Virgules manquantes dans clsn
                match = re.search(r'(Clsn[12]\[\d+\])\s*=\s*(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)', line)
                if match:
                    clsn_part = match.group(1)
                    v1, v2, v3, v4 = match.group(2), match.group(3), match.group(4), match.group(5)
                    line = f"{clsn_part} = {v1}, {v2}, {v3}, {v4}\n"
                    modified = True
                    self.errors_found.append(f"{air_file.name}:{i+1} - virgules manquantes")

                # ERREUR 4: Décimales dans sprites
                if '.' in line and ',' in line and not line.strip().startswith(';'):
                    if re.search(r'\d+\.\d+', line):
                        line = re.sub(r'(\d+)\.(\d+)', r'\1', line)
                        modified = True
                        self.errors_found.append(f"{air_file.name}:{i+1} - décimales dans sprite")

                fixed_lines.append(line)

            if modified:
                self.backup_file(air_file)
                with open(air_file, 'w', encoding='utf-8') as f:
                    f.writelines(fixed_lines)
                self.fixes_applied.append(f"Corrigé {air_file.name}")
                return True

            return False

        except Exception as e:
            self.log(f"Erreur scan {air_file.name}: {e}", 'ERROR')
            return False

    def scan_and_fix_stage_defs(self):
        """Scanne et corrige TOUS les stages .def"""
        self.log("\n🔍 SCAN STAGES .DEF")
        self.log("=" * 70)

        if not self.stages_dir.exists():
            return 0

        stage_defs = list(self.stages_dir.rglob("*.def"))
        fixed_count = 0

        for stage_def in stage_defs:
            if self.fix_stage_def(stage_def):
                fixed_count += 1
                self.log(f"  ✓ Corrigé: {stage_def.name}")

        self.log(f"\n✅ {fixed_count}/{len(stage_defs)} stages corrigés")
        return fixed_count

    def fix_stage_def(self, stage_def):
        """Corrige un fichier stage .def"""
        try:
            with open(stage_def, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            modified = False

            # ERREUR 1: spr = fichier.sff = 1 (double égal)
            if re.search(r'spr\s*=\s*[^=\n]+\s*=\s*\d+', content):
                content = re.sub(
                    r'(spr\s*=\s*)([^\s=]+)\s*=\s*\d+',
                    r'\1\2',
                    content
                )
                modified = True
                self.errors_found.append(f"{stage_def.name} - double égal dans spr")

            # ERREUR 2: Fichier .sff manquant
            spr_match = re.search(r'spr\s*=\s*([^\s\n]+)', content, re.IGNORECASE)
            if spr_match:
                spr_file = spr_match.group(1).strip().strip('"\'')
                stage_dir = stage_def.parent

                if not (stage_dir / spr_file).exists():
                    # Chercher un .sff disponible
                    available_sff = list(stage_dir.glob("*.sff"))

                    if available_sff:
                        new_spr = available_sff[0].name
                        content = re.sub(
                            r'(spr\s*=\s*)([^\s\n]+)',
                            f'spr = {new_spr}',
                            content,
                            flags=re.IGNORECASE
                        )
                        modified = True
                        self.errors_found.append(f"{stage_def.name} - .sff manquant: {spr_file}")
                        self.log(f"  Stage {stage_def.stem}: {spr_file} → {new_spr}")
                    else:
                        # Utiliser debugbg par défaut
                        content = re.sub(
                            r'(spr\s*=\s*)([^\s\n]+)',
                            'spr = debugbg',
                            content,
                            flags=re.IGNORECASE
                        )
                        modified = True
                        self.errors_found.append(f"{stage_def.name} - aucun .sff, utilise debugbg")

            if modified:
                self.backup_file(stage_def)
                with open(stage_def, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixes_applied.append(f"Corrigé stage {stage_def.name}")
                return True

            return False

        except Exception as e:
            self.log(f"Erreur scan {stage_def.name}: {e}", 'ERROR')
            return False

    def scan_and_fix_char_defs(self):
        """Scanne et corrige TOUS les personnages .def"""
        self.log("\n🔍 SCAN PERSONNAGES .DEF")
        self.log("=" * 70)

        if not self.chars_dir.exists():
            return 0

        char_defs = list(self.chars_dir.rglob("*.def"))
        fixed_count = 0

        for char_def in char_defs:
            if self.fix_char_def(char_def):
                fixed_count += 1
                self.log(f"  ✓ Corrigé: {char_def.parent.name}/{char_def.name}")

        self.log(f"\n✅ {fixed_count}/{len(char_defs)} personnages corrigés")
        return fixed_count

    def fix_char_def(self, char_def):
        """Corrige un fichier character .def"""
        try:
            with open(char_def, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            modified = False
            fixed_lines = []

            for line in lines:
                # Vérifier références de fichiers
                if '=' in line and not line.strip().startswith(';'):
                    # Enlever espaces excessifs
                    if '  ' in line:
                        line = re.sub(r'\s+', ' ', line.strip()) + '\n'
                        modified = True

                fixed_lines.append(line)

            if modified:
                self.backup_file(char_def)
                with open(char_def, 'w', encoding='utf-8') as f:
                    f.writelines(fixed_lines)
                self.fixes_applied.append(f"Corrigé char {char_def.name}")
                return True

            return False

        except Exception as e:
            return False

    def create_missing_files(self):
        """Crée les fichiers manquants"""
        self.log("\n📝 CRÉATION FICHIERS MANQUANTS")
        self.log("=" * 70)

        created_count = 0

        # common1.cns
        common1_path = self.data_dir / "common1.cns"
        if not common1_path.exists():
            common1_content = """; Common1.cns - États communs
; Fichier généré automatiquement

[Statedef -1]
; États communs pour tous les personnages
"""
            with open(common1_path, 'w', encoding='utf-8') as f:
                f.write(common1_content)

            self.fixes_applied.append("Créé common1.cns")
            self.log("  ✓ Créé common1.cns")
            created_count += 1

        return created_count

    def run_full_scan(self):
        """Lance un scan complet et corrige tout"""
        self.log("\n" + "=" * 70)
        self.log("🔍 SCANNER UNIVERSEL D'ERREURS")
        self.log("=" * 70)
        self.log("\nDétection et correction automatique de TOUTES les erreurs...")
        self.log("")

        # 1. Fichiers manquants
        self.create_missing_files()

        # 2. Fichiers .air
        air_fixed = self.scan_and_fix_air_files()

        # 3. Stages
        stages_fixed = self.scan_and_fix_stage_defs()

        # 4. Personnages
        chars_fixed = self.scan_and_fix_char_defs()

        # Rapport final
        self.log("\n" + "=" * 70)
        self.log("📊 RAPPORT FINAL")
        self.log("=" * 70)

        self.log(f"\n✅ Corrections appliquées: {len(self.fixes_applied)}")
        self.log(f"❌ Erreurs détectées: {len(self.errors_found)}")

        if self.fixes_applied:
            self.log(f"\n💾 Backups sauvegardés dans: {self.backup_dir}")

        self.log("\n" + "=" * 70)

        if len(self.fixes_applied) > 0:
            self.log(f"\n✅ {len(self.fixes_applied)} CORRECTIONS APPLIQUÉES!")
            self.log("Le jeu devrait maintenant démarrer correctement.")
        else:
            self.log("\n✓ Aucune erreur détectée")

        self.log("=" * 70)

        return len(self.fixes_applied) > 0

def main():
    """Point d'entrée"""
    print("\n" + "=" * 70)
    print("  🔍 SCANNER UNIVERSEL D'ERREURS")
    print("=" * 70)
    print("\n  Détection et correction automatique:")
    print("  • Fichiers .air corrompus")
    print("  • Stages .def invalides")
    print("  • Fichiers manquants")
    print("  • Personnages .def")
    print("\n" + "=" * 70)
    print()

    scanner = UniversalErrorScanner()
    success = scanner.run_full_scan()

    print("\n\n" + "=" * 70)
    if success:
        print("✅ SCAN TERMINÉ - CORRECTIONS APPLIQUÉES!")
        print("\nRelancez le jeu pour vérifier.")
    else:
        print("✓ SCAN TERMINÉ - Aucune erreur trouvée")
    print("=" * 70)
    print()

if __name__ == '__main__':
    main()
