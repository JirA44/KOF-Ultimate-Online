#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANALYSE ET RÉPARE LES ERREURS DU JEU
Lit PASTE_ERROR_HERE.txt et répare automatiquement
"""
import re
from pathlib import Path
import shutil

def main():
    print("="*70)
    print("🔍 ANALYSE ET RÉPARATION DES ERREURS")
    print("="*70)

    base_path = Path(r"D:\KOF Ultimate Online")
    error_file = base_path / "PASTE_ERROR_HERE.txt"

    if not error_file.exists():
        print("\n❌ Fichier PASTE_ERROR_HERE.txt introuvable!")
        input("\nAppuyez sur ENTRÉE...")
        return

    # Lire les erreurs
    with open(error_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    print(f"\n📄 Lecture de {error_file.name}...")
    print(f"   {len(content)} caractères lus\n")

    # Analyser les erreurs
    errors_found = []

    # 1. Erreurs CLSN
    clsn_matches = re.findall(
        r'Error in clsn([12]) in \[Begin Action (\d+)\]',
        content,
        re.IGNORECASE
    )

    # 2. Fichiers .air
    air_matches = re.findall(
        r'Error in (.+?\.air):(\d+)',
        content
    )

    # 3. Storyboards manquants
    sb_matches = re.findall(
        r'Error loading storyboard: (.+)',
        content
    )

    # 4. Fichiers .def
    def_matches = re.findall(
        r'Error loading (.+?\.def)',
        content
    )

    # Afficher ce qui a été trouvé
    print("📋 ERREURS DÉTECTÉES:")
    print("-" * 70)

    if clsn_matches:
        print(f"\n✓ {len(clsn_matches)} erreur(s) CLSN:")
        for clsn_type, action_num in clsn_matches[:5]:
            print(f"  - CLSN{clsn_type} dans Action {action_num}")

    if air_matches:
        print(f"\n✓ {len(air_matches)} erreur(s) dans fichiers .air:")
        for air_file, line_num in air_matches[:5]:
            print(f"  - {air_file} ligne {line_num}")

    if sb_matches:
        print(f"\n✓ {len(sb_matches)} storyboard(s) manquant(s):")
        for sb_path in sb_matches[:5]:
            print(f"  - {sb_path}")

    if def_matches:
        print(f"\n✓ {len(def_matches)} fichier(s) .def problématique(s):")
        for def_path in def_matches[:5]:
            print(f"  - {def_path}")

    if not any([clsn_matches, air_matches, sb_matches, def_matches]):
        print("\n⚠️  Aucune erreur reconnue dans le fichier")
        print("   Assurez-vous d'avoir collé les erreurs du jeu")
        input("\nAppuyez sur ENTRÉE...")
        return

    # RÉPARATION
    print("\n" + "="*70)
    print("🔧 RÉPARATION AUTOMATIQUE")
    print("="*70)

    total_fixed = 0

    # Réparer les storyboards
    if sb_matches:
        print("\n📝 Création des storyboards manquants...")
        for sb_path in sb_matches:
            sb_full_path = base_path / sb_path

            if sb_full_path.exists():
                print(f"  ⚠️  {sb_path} existe déjà, ignoré")
                continue

            try:
                # Extraire nom perso
                char_match = re.search(r'chars/([^/]+)/', sb_path)
                if not char_match:
                    continue

                char_name = char_match.group(1)
                char_path = base_path / 'chars' / char_name

                # Trouver sprite file
                def_files = list(char_path.glob("*.def"))
                spr_file = "sprite.sff"

                if def_files:
                    with open(def_files[0], 'r', encoding='utf-8', errors='ignore') as f:
                        def_content = f.read()
                    spr_match = re.search(r'sprite\s*=\s*(.+)', def_content, re.IGNORECASE)
                    if spr_match:
                        spr_file = spr_match.group(1).strip().strip('"')

                # Créer storyboard
                sb_full_path.parent.mkdir(parents=True, exist_ok=True)

                sb_type = 'intro' if 'intro' in sb_path.lower() else 'ending'

                content = f"""; Auto-generated {sb_type} storyboard
; Created by ANALYZE_AND_FIX_ERRORS

[SceneDef]
spr = {spr_file}
"""

                with open(sb_full_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                print(f"  ✅ Créé: {sb_path}")
                total_fixed += 1

            except Exception as e:
                print(f"  ❌ Erreur: {e}")

    # Réparer les erreurs CLSN dans .air
    if air_matches and clsn_matches:
        print("\n🔧 Réparation des erreurs CLSN...")

        # Grouper par fichier
        air_files_to_fix = {}
        for air_file, line_num in air_matches:
            air_files_to_fix[air_file] = line_num

        for air_filename in air_files_to_fix:
            # Chercher le fichier
            air_paths = list(base_path.glob(f"**/{air_filename}"))

            if not air_paths:
                print(f"  ⚠️  {air_filename} introuvable")
                continue

            air_path = air_paths[0]

            try:
                with open(air_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                modified = False
                i = 0

                while i < len(lines):
                    line = lines[i].strip()

                    # Chercher déclaration CLSN
                    clsn_match = re.match(r'(Clsn[12]):\s*(\d+)', line, re.IGNORECASE)
                    if clsn_match:
                        clsn_type = clsn_match.group(1)
                        declared_count = int(clsn_match.group(2))

                        # Compter les CLSN réelles
                        actual_count = 0
                        j = i + 1
                        while j < len(lines):
                            next_line = lines[j].strip()
                            if re.match(rf'{clsn_type}\[\d+\]', next_line, re.IGNORECASE):
                                actual_count += 1
                                j += 1
                            else:
                                break

                        # Corriger si nécessaire
                        if declared_count != actual_count:
                            # Trouver numéro action
                            action_num = "Unknown"
                            for k in range(i-1, max(0, i-20), -1):
                                if lines[k].strip().startswith('[Begin Action'):
                                    action_match = re.search(r'Action\s+(\d+)', lines[k])
                                    if action_match:
                                        action_num = action_match.group(1)
                                    break

                            lines[i] = f"{clsn_type}: {actual_count}\n"
                            modified = True
                            print(f"  ✅ {air_filename} Action {action_num}: {clsn_type}: {declared_count} → {actual_count}")
                            total_fixed += 1

                    i += 1

                if modified:
                    # Backup
                    backup = air_path.parent / f"{air_path.name}.backup_autofix"
                    if not backup.exists():
                        shutil.copy(air_path, backup)

                    # Sauvegarder
                    with open(air_path, 'w', encoding='utf-8') as f:
                        f.writelines(lines)

                    print(f"  ✅ {air_filename} réparé!")

            except Exception as e:
                print(f"  ❌ Erreur: {e}")

    # Rapport final
    print("\n" + "="*70)
    print("✅ RÉPARATION TERMINÉE")
    print("="*70)
    print(f"\nRéparations effectuées: {total_fixed}")

    if total_fixed > 0:
        print("\n💡 Testez maintenant:")
        print("   1. Relancez le jeu")
        print("   2. Testez le même combat")
        print("   3. Si nouvelles erreurs, collez-les dans PASTE_ERROR_HERE.txt")
        print("   4. Relancez ce script")
    else:
        print("\n⚠️  Aucune réparation effectuée")
        print("   Vérifiez le contenu de PASTE_ERROR_HERE.txt")

    input("\nAppuyez sur ENTRÉE pour fermer...")

if __name__ == "__main__":
    main()
