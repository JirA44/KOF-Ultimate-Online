#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Applique la configuration optimale pour le character select screen
Configuration: Balanced Grid (14×15)
"""

from pathlib import Path
import shutil
from datetime import datetime

def apply_optimal_config():
    """Applique la configuration optimale à system.def"""

    system_file = Path(r"D:\KOF Ultimate Online\data\system.def")

    if not system_file.exists():
        print(f"❌ {system_file} n'existe pas!")
        return False

    # Backup
    backup_file = system_file.with_suffix(f'.def.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    shutil.copy2(system_file, backup_file)
    print(f"✓ Backup créé: {backup_file.name}")

    # Lire le fichier
    with open(system_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    # Configuration optimale
    optimal_config = {
        'rows': '14',
        'columns': '15',
        'cell.size': '34,34',
        'cell.spacing': '2',
        'pos': '6,52',
    }

    # Modifier les lignes
    new_lines = []
    in_select_info = False
    modified_keys = set()

    for line in lines:
        stripped = line.strip()

        # Détecter [Select Info]
        if stripped == "[Select Info]":
            in_select_info = True
            new_lines.append(line)
            continue

        # Détecter fin de section
        if in_select_info and stripped.startswith('[') and stripped != "[Select Info]":
            in_select_info = False

        # Modifier les paramètres dans [Select Info]
        if in_select_info and '=' in stripped and not stripped.startswith(';'):
            key = stripped.split('=')[0].strip()

            if key in optimal_config:
                # Remplacer par valeur optimale
                indent = len(line) - len(line.lstrip())
                new_line = ' ' * indent + f"{key} = {optimal_config[key]}\n"
                new_lines.append(new_line)
                modified_keys.add(key)
                continue

        new_lines.append(line)

    # Vérifier que toutes les clés ont été modifiées
    if len(modified_keys) != len(optimal_config):
        missing = set(optimal_config.keys()) - modified_keys
        print(f"⚠️  Certaines clés n'ont pas été trouvées: {missing}")

    # Écrire le fichier
    with open(system_file, 'w', encoding='utf-8', errors='ignore') as f:
        f.writelines(new_lines)

    return True

def main():
    print("="*70)
    print("  APPLICATION CONFIGURATION OPTIMALE")
    print("="*70)
    print()

    print("Configuration appliquée:")
    print("  rows = 14")
    print("  columns = 15")
    print("  cell.size = 34,34")
    print("  cell.spacing = 2")
    print("  pos = 6,52")
    print()

    print("Avantages:")
    print("  ✓ 210 slots (189 chars + 21 vides)")
    print("  ✓ Cellules 34×34 (taille optimale)")
    print("  ✓ Espacement 2px (lisible)")
    print("  ✓ Largeur: 538px (dans écran 640px)")
    print("  ✓ Grille équilibrée et centrée")
    print()

    if apply_optimal_config():
        print("✅ Configuration appliquée avec succès!")
        print()
        print("Relance le jeu pour voir les changements:")
        print("  LAUNCH_WITH_MODE_SELECT.bat")
    else:
        print("❌ Erreur lors de l'application")

    print()
    print("="*70)

if __name__ == "__main__":
    main()
