#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix complet pour Eve.air - Ajoute toutes les déclarations Clsn2: manquantes
"""

import re
from pathlib import Path

def fix_air_file(air_path):
    """Répare un fichier .air en ajoutant les déclarations Clsn2: manquantes"""

    print(f"Lecture de {air_path}...")
    with open(air_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    fixed_lines = []
    i = 0
    fixes_applied = 0

    while i < len(lines):
        line = lines[i]
        fixed_lines.append(line)

        # Vérifier si c'est une ligne Clsn2[0] sans déclaration avant
        if re.match(r'\s*Clsn2\[0\]', line):
            # Vérifier la ligne précédente
            prev_line = lines[i-1] if i > 0 else ""

            # Si la ligne précédente n'est PAS une déclaration Clsn2:
            if not re.match(r'\s*Clsn2:\s*\d+', prev_line):
                # Compter combien de Clsn2[X] consécutifs il y a
                count = 0
                j = i
                while j < len(lines) and re.match(r'\s*Clsn2\[\d+\]', lines[j]):
                    count += 1
                    j += 1

                # Insérer la déclaration AVANT la ligne Clsn2[0]
                indent = len(line) - len(line.lstrip())
                declaration = f"{'': <{indent}}Clsn2: {count}\n"

                # Remplacer la dernière ligne ajoutée par déclaration + ligne
                fixed_lines[-1] = declaration
                fixed_lines.append(line)

                fixes_applied += 1
                print(f"  Fix ligne {i+1}: Ajout 'Clsn2: {count}' avant Clsn2[0]")

        i += 1

    # Sauvegarder
    print(f"\nÉcriture du fichier corrigé...")
    with open(air_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

    print(f"\n✓ Fichier corrigé! {fixes_applied} déclarations ajoutées.")
    return fixes_applied

def main():
    air_path = Path(r"D:\KOF Ultimate Online Online Online\chars\Eve\Eve.air")

    if not air_path.exists():
        print(f"❌ Fichier introuvable: {air_path}")
        return

    print("="*80)
    print("RÉPARATION COMPLÈTE EVE.AIR")
    print("="*80 + "\n")

    fixes = fix_air_file(air_path)

    print("\n" + "="*80)
    print(f"TERMINÉ - {fixes} corrections appliquées")
    print("="*80)

if __name__ == '__main__':
    main()
