#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RÉPARATION COMPLÈTE - CLSN + STORYBOARDS
Scanne et répare tous les personnages du roster
"""
import os
import re
from pathlib import Path

def fix_clsn_errors_in_air(air_file):
    """Répare les erreurs CLSN dans un fichier .air"""
    errors_fixed = 0

    try:
        with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        modified = False
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            # Chercher déclaration Clsn1 ou Clsn2
            clsn_match = re.match(r'(Clsn[12]):\s*(\d+)', line, re.IGNORECASE)
            if clsn_match:
                clsn_type = clsn_match.group(1)
                declared_count = int(clsn_match.group(2))

                # Compter les CLSN suivantes
                actual_count = 0
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    if re.match(rf'{clsn_type}\[\d+\]', next_line, re.IGNORECASE):
                        actual_count += 1
                        j += 1
                    else:
                        break

                # Si déclaré != réel, corriger
                if declared_count != actual_count:
                    # Trouver l'action en cours
                    action_num = "Unknown"
                    for k in range(i-1, max(0, i-20), -1):
                        if lines[k].strip().startswith('[Begin Action'):
                            action_match = re.search(r'Action\s+(\d+)', lines[k])
                            if action_match:
                                action_num = action_match.group(1)
                            break

                    print(f"  ⚠️  Action {action_num}: {clsn_type} déclare {declared_count}, mais trouve {actual_count}")
                    lines[i] = f"{clsn_type}: {actual_count}\n"
                    modified = True
                    errors_fixed += 1
                    print(f"      ✓ Corrigé: {clsn_type}: {actual_count}")

            i += 1

        if modified:
            # Backup
            backup = air_file.parent / f"{air_file.name}.backup_clsn"
            if not backup.exists():
                with open(backup, 'w', encoding='utf-8') as f:
                    with open(air_file, 'r', encoding='utf-8', errors='ignore') as orig:
                        f.write(orig.read())

            # Sauvegarder
            with open(air_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)

        return errors_fixed

    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return 0

def create_missing_storyboards(char_path, def_file):
    """Crée les storyboards manquants"""
    storyboards_created = 0

    try:
        with open(def_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Chercher le fichier sprite
        spr_match = re.search(r'sprite\s*=\s*(.+)', content, re.IGNORECASE)
        spr_file = spr_match.group(1).strip().strip('"') if spr_match else "sprite.sff"

        # Chercher les storyboards manquants
        storyboard_types = ['intro', 'ending']

        for sb_type in storyboard_types:
            sb_match = re.search(rf'{sb_type}\.storyboard\s*=\s*(.+)', content, re.IGNORECASE)
            if sb_match:
                sb_filename = sb_match.group(1).strip().strip('"')
                if sb_filename and sb_filename.lower() != 'none':
                    sb_path = char_path / sb_filename

                    if not sb_path.exists():
                        # Créer le storyboard
                        sb_content = f"""; Auto-generated {sb_type} storyboard
; Created by auto-repair system

[SceneDef]
spr = {spr_file}
; No {sb_type} defined - character will use default
"""
                        sb_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(sb_path, 'w', encoding='utf-8') as f:
                            f.write(sb_content)

                        print(f"  ✓ Créé: {sb_filename}")
                        storyboards_created += 1

        return storyboards_created

    except Exception as e:
        print(f"  ❌ Erreur storyboards: {e}")
        return 0

def main():
    print("="*70)
    print("🛠️  RÉPARATION COMPLÈTE - CLSN + STORYBOARDS")
    print("="*70)

    base_path = Path(r"D:\KOF Ultimate Online")
    select_def = base_path / "data" / "select.def"

    # Lire roster
    chars = []
    with open(select_def, 'r', encoding='utf-8') as f:
        in_chars = False
        for line in f:
            line = line.strip()
            if line.startswith('[Characters]'):
                in_chars = True
                continue
            elif line.startswith('['):
                in_chars = False
                continue

            if in_chars and line and not line.startswith(';'):
                if ',' in line:
                    char_name = line.split(',')[0].strip()
                    if char_name:
                        chars.append(char_name)

    print(f"\n✓ {len(chars)} personnages à analyser\n")

    total_clsn_fixed = 0
    total_storyboards = 0
    chars_path = base_path / "chars"

    for i, char_name in enumerate(chars, 1):
        char_path = chars_path / char_name

        if not char_path.exists():
            continue

        print(f"[{i}/{len(chars)}] {char_name}")

        # Chercher .def
        def_files = list(char_path.glob("*.def"))
        if not def_files:
            print("  ⚠️  Pas de .def")
            continue

        def_file = def_files[0]

        # Lire .def pour trouver .air
        try:
            with open(def_file, 'r', encoding='utf-8', errors='ignore') as f:
                def_content = f.read()

            air_match = re.search(r'anim\s*=\s*(.+)', def_content, re.IGNORECASE)
            if air_match:
                air_filename = air_match.group(1).strip().strip('"')
                air_file = char_path / air_filename

                if air_file.exists():
                    clsn_fixed = fix_clsn_errors_in_air(air_file)
                    total_clsn_fixed += clsn_fixed
                else:
                    print(f"  ⚠️  {air_filename} introuvable")

            # Créer storyboards manquants
            sb_created = create_missing_storyboards(char_path, def_file)
            total_storyboards += sb_created

            if not air_match and sb_created == 0:
                print("  ✓ OK")

        except Exception as e:
            print(f"  ❌ Erreur: {e}")

    # Rapport
    print("\n" + "="*70)
    print("📊 RAPPORT FINAL")
    print("="*70)
    print(f"\nErreurs CLSN réparées:      {total_clsn_fixed}")
    print(f"Storyboards créés:          {total_storyboards}")

    if total_clsn_fixed > 0 or total_storyboards > 0:
        print("\n✅ RÉPARATIONS TERMINÉES!")
        print("\n💡 Testez maintenant le jeu:")
        print("   1. Lancez KOF Ultimate Online")
        print("   2. Sélectionnez les personnages réparés")
        print("   3. Lancez un combat")
    else:
        print("\n✅ Aucune réparation nécessaire")

    input("\nAppuyez sur ENTRÉE pour fermer...")

if __name__ == "__main__":
    main()
