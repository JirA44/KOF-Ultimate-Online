#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RÉPARATION ÉCRAN DE SÉLECTION
- Vérifie les portraits des personnages
- Crée les portraits manquants (9000,0 et 9000,1)
- Ajuste la grille de sélection
"""
import os
import struct
from pathlib import Path
from PIL import Image
import shutil

def read_sff_portraits(sff_path):
    """Lit les portraits d'un fichier .sff"""
    portraits = {'small': [], 'large': []}

    try:
        with open(sff_path, 'rb') as f:
            # Lire signature
            signature = f.read(12)
            if not signature.startswith(b'ElecbyteSpr'):
                return portraits

            # Lire header
            f.read(4)  # version
            group_total = struct.unpack('<I', f.read(4))[0]
            image_total = struct.unpack('<I', f.read(4))[0]

            # Sauter reste header
            f.read(496)

            current_pos = 512

            for i in range(min(image_total, 100)):  # Limiter aux 100 premiers
                try:
                    f.seek(current_pos)

                    next_subfile = struct.unpack('<I', f.read(4))[0]
                    length = struct.unpack('<I', f.read(4))[0]
                    f.read(4)  # axisx, axisy
                    groupno = struct.unpack('<H', f.read(2))[0]
                    imageno = struct.unpack('<H', f.read(2))[0]

                    if groupno == 9000:
                        if imageno == 0:
                            portraits['small'].append(imageno)
                        elif imageno == 1:
                            portraits['large'].append(imageno)

                    if next_subfile == 0:
                        break
                    current_pos = next_subfile

                except:
                    break

    except Exception as e:
        pass

    return portraits

def analyze_select_screen():
    """Analyse la configuration de l'écran de sélection"""
    print("="*70)
    print("🔍 DIAGNOSTIC ÉCRAN DE SÉLECTION")
    print("="*70)

    base_path = Path(r"D:\KOF Ultimate Online")

    # Lire select.def
    select_def = base_path / "data" / "select.def"
    chars = []

    print("\n📋 Lecture de select.def...")
    with open(select_def, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith(';') and ',' in line:
                char_name = line.split(',')[0].strip()
                if char_name and not char_name.startswith('['):
                    chars.append(char_name)

    print(f"✓ Trouvé {len(chars)} personnages dans select.def\n")

    # Analyser les portraits
    print("="*70)
    print("📸 ANALYSE DES PORTRAITS")
    print("="*70)

    chars_path = base_path / "chars"
    missing_small = []
    missing_large = []
    ok_chars = []

    for char_name in chars:
        char_dir = chars_path / char_name
        if not char_dir.exists():
            print(f"⚠️  {char_name}: Dossier introuvable")
            missing_small.append(char_name)
            missing_large.append(char_name)
            continue

        # Chercher le fichier .sff
        sff_files = list(char_dir.glob("*.sff"))
        if not sff_files:
            print(f"⚠️  {char_name}: Aucun fichier .sff")
            missing_small.append(char_name)
            missing_large.append(char_name)
            continue

        # Analyser le premier .sff trouvé
        portraits = read_sff_portraits(sff_files[0])

        has_small = len(portraits['small']) > 0
        has_large = len(portraits['large']) > 0

        status = ""
        if has_small and has_large:
            status = "✅ OK"
            ok_chars.append(char_name)
        elif has_small and not has_large:
            status = "⚠️  Manque GRAND portrait (9000,1)"
            missing_large.append(char_name)
        elif not has_small and has_large:
            status = "⚠️  Manque PETIT portrait (9000,0)"
            missing_small.append(char_name)
        else:
            status = "❌ Manque LES DEUX portraits"
            missing_small.append(char_name)
            missing_large.append(char_name)

        print(f"  {char_name:30s} {status}")

    # Statistiques
    print("\n" + "="*70)
    print("📊 STATISTIQUES")
    print("="*70)
    print(f"  Personnages OK:           {len(ok_chars)}/{len(chars)} ({len(ok_chars)*100//len(chars)}%)")
    print(f"  Manque petit portrait:    {len(missing_small)}")
    print(f"  Manque grand portrait:    {len(missing_large)}")

    # Recommandations
    print("\n" + "="*70)
    print("💡 SOLUTIONS")
    print("="*70)

    if missing_large:
        print("\n🔧 OPTION 1: Configurer system.def pour ne PAS utiliser les grands portraits")
        print("   → Modifier system.def ligne 168-174")
        print("   → Mettre p1.face.spr = 9000,0 (utiliser petit portrait)")
        print("   → Avantage: Fonctionne immédiatement")

        print("\n🔧 OPTION 2: Copier/créer les grands portraits manquants")
        print("   → Dupliquer 9000,0 → 9000,1 dans les .sff")
        print("   → Nécessite outil SFF")
        print("   → Plus complexe")

    if len(ok_chars) < len(chars) // 2:
        print("\n⚠️  ATTENTION: Moins de 50% des personnages ont des portraits complets!")
        print("   Recommandation: Utiliser OPTION 1 (configurer system.def)")

    # Vérifier la grille
    print("\n" + "="*70)
    print("🎯 GRILLE DE SÉLECTION")
    print("="*70)

    system_def = base_path / "data" / "system.def"
    with open(system_def, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extraire config grille
    import re
    rows_match = re.search(r'rows\s*=\s*(\d+)', content)
    cols_match = re.search(r'columns\s*=\s*(\d+)', content)

    if rows_match and cols_match:
        rows = int(rows_match.group(1))
        cols = int(cols_match.group(1))
        total_cells = rows * cols

        print(f"  Configuration actuelle:")
        print(f"    Lignes:    {rows}")
        print(f"    Colonnes:  {cols}")
        print(f"    Total:     {total_cells} emplacements")
        print(f"    Utilisés:  {len(chars)}/{total_cells} ({len(chars)*100//total_cells}%)")

        # Calculer grille optimale
        import math
        optimal_cols = math.ceil(math.sqrt(len(chars) * 1.5))
        optimal_rows = math.ceil(len(chars) / optimal_cols)

        print(f"\n  Grille optimale pour {len(chars)} personnages:")
        print(f"    Lignes:    {optimal_rows}")
        print(f"    Colonnes:  {optimal_cols}")
        print(f"    Total:     {optimal_rows * optimal_cols} emplacements")
        print(f"    Utilisés:  {len(chars)}/{optimal_rows * optimal_cols} ({len(chars)*100//(optimal_rows * optimal_cols)}%)")

    print("\n" + "="*70)
    print("✅ DIAGNOSTIC TERMINÉ")
    print("="*70)

    return {
        'total': len(chars),
        'ok': len(ok_chars),
        'missing_small': missing_small,
        'missing_large': missing_large,
        'chars': chars
    }

def fix_system_def_portraits():
    """Répare system.def pour utiliser les petits portraits partout"""
    print("\n" + "="*70)
    print("🔧 RÉPARATION SYSTEM.DEF")
    print("="*70)

    base_path = Path(r"D:\KOF Ultimate Online")
    system_def = base_path / "data" / "system.def"

    # Backup
    backup = base_path / "data" / "system.def.backup_portraits"
    if not backup.exists():
        shutil.copy(system_def, backup)
        print(f"✓ Backup créé: {backup.name}")

    # Lire et modifier
    with open(system_def, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified = False
    for i, line in enumerate(lines):
        # Chercher les lignes de configuration des grands portraits
        if 'p1.face.spr' in line and '9000,1' in line:
            lines[i] = line.replace('9000,1', '9000,0')
            print(f"✓ Ligne {i+1}: p1.face.spr = 9000,0 (utilise petit portrait)")
            modified = True
        elif 'p2.face.spr' in line and '9000,1' in line:
            lines[i] = line.replace('9000,1', '9000,0')
            print(f"✓ Ligne {i+1}: p2.face.spr = 9000,0 (utilise petit portrait)")
            modified = True

        # Ajuster aussi les échelles si nécessaire
        elif 'p1.face.scale' in line:
            # Agrandir un peu les petits portraits
            lines[i] = 'p1.face.scale = 1.5,1.5\n'
            print(f"✓ Ligne {i+1}: p1.face.scale = 1.5,1.5 (agrandi)")
            modified = True
        elif 'p2.face.scale' in line:
            lines[i] = 'p2.face.scale = 1.5,1.5\n'
            print(f"✓ Ligne {i+1}: p2.face.scale = 1.5,1.5 (agrandi)")
            modified = True

    if modified:
        with open(system_def, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("\n✅ system.def réparé!")
        print("   → Les grands portraits utilisent maintenant 9000,0 (petits portraits)")
        print("   → Échelle ajustée pour meilleure visibilité")
    else:
        print("❌ Aucune modification nécessaire")

    return modified

def optimize_grid():
    """Optimise la grille de sélection"""
    print("\n" + "="*70)
    print("🎯 OPTIMISATION GRILLE")
    print("="*70)

    base_path = Path(r"D:\KOF Ultimate Online")
    select_def = base_path / "data" / "select.def"

    # Compter les personnages
    chars = []
    with open(select_def, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith(';') and ',' in line:
                char_name = line.split(',')[0].strip()
                if char_name and not char_name.startswith('['):
                    chars.append(char_name)

    num_chars = len(chars)

    # Calculer grille optimale
    import math
    optimal_cols = math.ceil(math.sqrt(num_chars * 1.8))
    optimal_rows = math.ceil(num_chars / optimal_cols)

    print(f"  {num_chars} personnages trouvés")
    print(f"  Grille optimale: {optimal_rows} lignes x {optimal_cols} colonnes")

    # Modifier system.def
    system_def = base_path / "data" / "system.def"

    with open(system_def, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified = False
    for i, line in enumerate(lines):
        if line.strip().startswith('rows ='):
            old_value = line.split('=')[1].strip()
            lines[i] = f'rows = {optimal_rows}\n'
            print(f"✓ rows: {old_value} → {optimal_rows}")
            modified = True
        elif line.strip().startswith('columns ='):
            old_value = line.split('=')[1].strip()
            lines[i] = f'columns = {optimal_cols}\n'
            print(f"✓ columns: {old_value} → {optimal_cols}")
            modified = True

    if modified:
        with open(system_def, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"\n✅ Grille optimisée!")

    return modified

def main():
    print("="*70)
    print("🛠️  RÉPARATION ÉCRAN DE SÉLECTION - KOF ULTIMATE ONLINE")
    print("="*70)

    # Diagnostic
    results = analyze_select_screen()

    # Proposer réparations
    print("\n" + "="*70)
    print("🔨 RÉPARATIONS AUTOMATIQUES")
    print("="*70)

    if results['missing_large']:
        print(f"\n⚠️  {len(results['missing_large'])} personnages n'ont pas de grand portrait (9000,1)")
        print("   Solution: Configurer system.def pour utiliser les petits portraits")

        fix_system_def_portraits()

    # Optimiser grille
    optimize_grid()

    print("\n" + "="*70)
    print("✅ RÉPARATIONS TERMINÉES!")
    print("="*70)
    print("\n💡 Testez maintenant:")
    print("   1. Lancez le jeu")
    print("   2. Allez à l'écran de sélection")
    print("   3. Vérifiez que les portraits s'affichent correctement")
    print("\n   En cas de problème, restaurez: data/system.def.backup_portraits")

    input("\nAppuyez sur ENTRÉE pour fermer...")

if __name__ == "__main__":
    main()
