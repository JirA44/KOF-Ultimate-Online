#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRECTEUR SPÉCIFIQUE RUGAL-KOFM.AIR
Corrige les lignes clsn2 avec sprite data mélangé
"""

import re
from pathlib import Path
import shutil
from datetime import datetime

def fix_rugal_air():
    """Corrige Rugal-KOFM.air"""
    air_file = Path(r"D:\KOF Ultimate Online Online Online\chars\Rugal7th\Rugal-KOFM.air")

    if not air_file.exists():
        print(f"❌ Fichier introuvable: {air_file}")
        return False

    # Backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = air_file.parent / f"Rugal-KOFM.air.backup_{timestamp}"
    shutil.copy2(air_file, backup_path)
    print(f"💾 Backup: {backup_path.name}")

    # Lire
    with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    fixed_lines = []
    fixes_count = 0

    for i, line in enumerate(lines):
        # Détecter ligne problématique: Clsn2[0] = x, y, z, w SPRITE_DATA
        # Pattern: Clsn2[0] = -18, -115, 22, 0 9999, 9, 0, 0, 6
        match = re.match(r'^(\s*Clsn[12]\[\d+\]\s*=\s*-?\d+,\s*-?\d+,\s*-?\d+,\s*-?\d+)\s+(\d+,\s*.+)$', line)

        if match:
            clsn_part = match.group(1)
            sprite_part = match.group(2)

            # Séparer en deux lignes
            fixed_lines.append(clsn_part + '\n')
            fixed_lines.append(sprite_part + '\n')
            fixes_count += 1
            print(f"  Ligne {i+1}: Séparé clsn2 et sprite data")
        else:
            fixed_lines.append(line)

    # Écrire
    with open(air_file, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

    print(f"\n✅ {fixes_count} lignes corrigées dans Rugal-KOFM.air")
    return True

if __name__ == '__main__':
    print("=" * 70)
    print("🔧 CORRECTEUR RUGAL-KOFM.AIR")
    print("=" * 70)
    print()

    success = fix_rugal_air()

    if success:
        print("\n✅ CORRECTION TERMINÉE!")
        print("Relancez le jeu pour vérifier.")
    else:
        print("\n❌ ERREUR lors de la correction")

    print("=" * 70)
