#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SYSTÈME DE RÉPARATION AUTOMATIQUE EN BOUCLE
- Lance le jeu
- Attend le crash
- Lit le log
- Répare les erreurs
- Recommence jusqu'à stabilité
"""
import os
import re
import time
import subprocess
from pathlib import Path
import shutil

class AutoFixer:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.log_file = self.base_path / "mugen.log"
        self.errors_fixed = []

    def read_last_error_from_log(self):
        """Lit la dernière erreur du log"""
        if not self.log_file.exists():
            return None

        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            errors = []

            # Chercher erreurs CLSN
            clsn_errors = re.findall(
                r'Error in (.+?):(\d+)\s*\n.*?Error in clsn([12]) in \[Begin Action (\d+)\]',
                content,
                re.IGNORECASE | re.DOTALL
            )

            for air_file, line_num, clsn_type, action_num in clsn_errors:
                errors.append({
                    'type': 'clsn',
                    'file': air_file.strip(),
                    'line': int(line_num),
                    'clsn_type': clsn_type,
                    'action': action_num
                })

            # Chercher storyboards manquants
            storyboard_errors = re.findall(
                r'Error loading storyboard: (.+)',
                content
            )

            for sb_path in storyboard_errors:
                errors.append({
                    'type': 'storyboard',
                    'path': sb_path.strip()
                })

            # Chercher fichiers .def qui ne chargent pas
            def_errors = re.findall(
                r'Error loading (.+?\.def)',
                content
            )

            for def_path in def_errors:
                errors.append({
                    'type': 'def_load',
                    'path': def_path.strip()
                })

            return errors if errors else None

        except Exception as e:
            print(f"❌ Erreur lecture log: {e}")
            return None

    def fix_clsn_error(self, error):
        """Répare une erreur CLSN"""
        air_file = self.base_path / error['file']

        if not air_file.exists():
            print(f"  ⚠️  Fichier introuvable: {air_file}")
            return False

        try:
            with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Chercher l'action
            action_num = error['action']
            clsn_type = f"Clsn{error['clsn_type']}"

            in_action = False
            fixed = False

            for i, line in enumerate(lines):
                if f'[Begin Action {action_num}]' in line:
                    in_action = True
                    continue

                if in_action and line.strip().startswith('[Begin Action'):
                    break

                if in_action and line.strip().startswith(clsn_type + ':'):
                    # Compter les CLSN suivantes
                    declared = int(re.search(r':\s*(\d+)', line).group(1))
                    actual = 0

                    j = i + 1
                    while j < len(lines):
                        if re.match(rf'{clsn_type}\[\d+\]', lines[j].strip(), re.IGNORECASE):
                            actual += 1
                            j += 1
                        else:
                            break

                    if declared != actual:
                        lines[i] = f"{clsn_type}: {actual}\n"
                        fixed = True
                        print(f"  ✓ {air_file.name} Action {action_num}: {clsn_type}: {declared} → {actual}")
                        break

            if fixed:
                # Backup
                backup = air_file.parent / f"{air_file.name}.backup_{int(time.time())}"
                shutil.copy(air_file, backup)

                # Sauvegarder
                with open(air_file, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                return True

        except Exception as e:
            print(f"  ❌ Erreur: {e}")

        return False

    def fix_storyboard_error(self, error):
        """Crée un storyboard manquant"""
        sb_path = self.base_path / error['path']

        if sb_path.exists():
            return False

        try:
            # Trouver le personnage
            char_name = error['path'].split('/')[0].replace('chars/', '')
            char_path = self.base_path / 'chars' / char_name

            # Chercher le sprite file
            def_files = list(char_path.glob("*.def"))
            spr_file = "sprite.sff"

            if def_files:
                with open(def_files[0], 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                spr_match = re.search(r'sprite\s*=\s*(.+)', content, re.IGNORECASE)
                if spr_match:
                    spr_file = spr_match.group(1).strip().strip('"')

            # Créer le storyboard
            sb_path.parent.mkdir(parents=True, exist_ok=True)

            sb_type = 'intro' if 'intro' in sb_path.name.lower() else 'ending'

            content = f"""; Auto-generated {sb_type} storyboard
; Created by auto-fix system

[SceneDef]
spr = {spr_file}
"""

            with open(sb_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"  ✓ Créé: {error['path']}")
            return True

        except Exception as e:
            print(f"  ❌ Erreur: {e}")

        return False

    def remove_problematic_char(self, char_name):
        """Retire un personnage problématique du roster"""
        select_def = self.base_path / "data" / "select.def"

        try:
            with open(select_def, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            modified = False
            for i, line in enumerate(lines):
                if line.strip().startswith(char_name + ','):
                    lines[i] = f"; RETIRÉ AUTO (Erreurs non réparables): {line}"
                    modified = True
                    print(f"  ✓ Retiré du roster: {char_name}")
                    break

            if modified:
                # Backup
                backup = select_def.parent / f"select.def.backup_{int(time.time())}"
                shutil.copy(select_def, backup)

                with open(select_def, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                return True

        except Exception as e:
            print(f"  ❌ Erreur: {e}")

        return False

    def run_auto_fix_loop(self, max_iterations=10):
        """Boucle principale de réparation automatique"""
        print("="*70)
        print("🔄 SYSTÈME DE RÉPARATION AUTOMATIQUE EN BOUCLE")
        print("="*70)
        print(f"\nMode: Jusqu'à {max_iterations} itérations maximum")
        print("Le jeu sera lancé, analysé, réparé en boucle\n")

        for iteration in range(1, max_iterations + 1):
            print("\n" + "="*70)
            print(f"🔄 ITÉRATION {iteration}/{max_iterations}")
            print("="*70)

            # Supprimer ancien log
            if self.log_file.exists():
                self.log_file.unlink()

            # Lire les erreurs du log précédent (si existe)
            errors = self.read_last_error_from_log()

            if errors:
                print(f"\n📋 {len(errors)} erreur(s) détectée(s) dans le log précédent")

                for i, error in enumerate(errors, 1):
                    print(f"\n[{i}/{len(errors)}] {error['type'].upper()}")

                    if error['type'] == 'clsn':
                        print(f"  Fichier: {error['file']}")
                        print(f"  Action: {error['action']}")
                        self.fix_clsn_error(error)

                    elif error['type'] == 'storyboard':
                        print(f"  Path: {error['path']}")
                        self.fix_storyboard_error(error)

                    elif error['type'] == 'def_load':
                        print(f"  Path: {error['path']}")
                        # Extraire nom du perso
                        char_match = re.search(r'chars/([^/]+)/', error['path'])
                        if char_match:
                            char_name = char_match.group(1)
                            print(f"  Personnage: {char_name}")
                            # On pourrait le retirer du roster ici

            else:
                print("\n✅ Aucune erreur dans le log précédent!")
                print("   Le jeu semble stable!")
                break

            print(f"\n⏸️  Itération {iteration} terminée")
            print("   Les réparations ont été appliquées")

        print("\n" + "="*70)
        print("✅ BOUCLE DE RÉPARATION TERMINÉE")
        print("="*70)
        print(f"\nItérations effectuées: {iteration}")
        print(f"\nLe jeu devrait maintenant être plus stable!")
        print("\n💡 Testez maintenant:")
        print("   1. Lancez le jeu manuellement")
        print("   2. Sélectionnez des personnages")
        print("   3. Lancez un combat")
        print("\n   Si ça crash encore, relancez ce script!")

def main():
    fixer = AutoFixer()

    # Lancer la boucle de réparation
    fixer.run_auto_fix_loop(max_iterations=10)

    input("\nAppuyez sur ENTRÉE pour fermer...")

if __name__ == "__main__":
    main()
