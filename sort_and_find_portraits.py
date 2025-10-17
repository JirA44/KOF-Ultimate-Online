#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour trier le select.def et trouver les portraits manquants
"""
import os
import shutil
from collections import defaultdict

CHARS_DIR = r"D:\KOF Ultimate Online\chars"
SELECT_DEF = r"D:\KOF Ultimate Online\data\select.def"
SELECT_DEF_SORTED = r"D:\KOF Ultimate Online\data\select_sorted.def"

def read_select_def():
    """Lit le select.def"""
    with open(SELECT_DEF, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    header = []
    chars = []
    footer = []

    in_chars = False
    after_chars = False

    for line in lines:
        stripped = line.strip()

        if stripped == '[Characters]':
            in_chars = True
            header.append(line)
            continue

        if in_chars and stripped.startswith('['):
            after_chars = True
            in_chars = False

        if not in_chars and not after_chars:
            header.append(line)
        elif in_chars:
            if stripped and not stripped.startswith(';'):
                chars.append(stripped)
        elif after_chars:
            footer.append(line)

    return header, chars, footer

def check_portrait_files(char_name):
    """Vérifie si un personnage a des fichiers de portrait"""
    char_dir = os.path.join(CHARS_DIR, char_name)
    if not os.path.exists(char_dir):
        return {'mini': None, 'big': None, 'dir_exists': False}

    mini_path = None
    big_path = None

    for root, dirs, files in os.walk(char_dir):
        for file in files:
            if file.startswith('9000,0.') or file.startswith('9000_0.'):
                mini_path = os.path.join(root, file)
            if file.startswith('9000,1.') or file.startswith('9000_1.'):
                big_path = os.path.join(root, file)

    return {'mini': mini_path, 'big': big_path, 'dir_exists': True}

def main():
    print("=== TRI DES PERSONNAGES PAR PORTRAITS ===\n")

    # Lire le select.def
    header, chars, footer = read_select_def()
    print(f"Total personnages: {len(chars)}\n")

    # Scanner tous les personnages
    chars_with_mini = []
    chars_with_big_only = []
    chars_without = []

    portrait_info = {}

    for char in chars:
        result = check_portrait_files(char)
        portrait_info[char] = result

        if result['mini']:
            chars_with_mini.append(char)
        elif result['big']:
            chars_with_big_only.append(char)
        else:
            chars_without.append(char)

    print(f"✅ Avec mini-portrait: {len(chars_with_mini)}")
    print(f"⚠️  Avec big uniquement: {len(chars_with_big_only)}")
    print(f"❌ Sans portraits: {len(chars_without)}\n")

    # Trier
    sorted_chars = chars_with_mini + chars_with_big_only + chars_without

    # Sauvegarder le select.def trié
    with open(SELECT_DEF_SORTED, 'w', encoding='utf-8') as f:
        # Header
        for line in header:
            f.write(line)

        # Chars with mini
        if chars_with_mini:
            f.write("; === PERSONNAGES AVEC MINI-PORTRAITS ===\n")
            for char in chars_with_mini:
                f.write(f"{char}\n")
            f.write("\n")

        # Chars with big only
        if chars_with_big_only:
            f.write("; === PERSONNAGES AVEC BIG PORTRAIT UNIQUEMENT ===\n")
            for char in chars_with_big_only:
                f.write(f"{char}\n")
            f.write("\n")

        # Chars without
        if chars_without:
            f.write("; === PERSONNAGES SANS PORTRAITS ===\n")
            for char in chars_without:
                f.write(f"{char}\n")
            f.write("\n")

        # Footer
        for line in footer:
            f.write(line)

    print(f"✅ select.def trié sauvegardé: {SELECT_DEF_SORTED}\n")

    # Rapport détaillé
    report_path = r"D:\KOF Ultimate Online\PORTRAIT_LOCATIONS.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=== EMPLACEMENTS DES PORTRAITS ===\n\n")

        f.write("AVEC MINI-PORTRAITS:\n")
        f.write("=" * 80 + "\n")
        for char in chars_with_mini:
            info = portrait_info[char]
            f.write(f"\n{char}:\n")
            if info['mini']:
                f.write(f"  Mini: {info['mini']}\n")
            if info['big']:
                f.write(f"  Big:  {info['big']}\n")

        f.write("\n\n" + "=" * 80)
        f.write("\n\nSANS PORTRAITS (À CRÉER):\n")
        f.write("=" * 80 + "\n")
        for char in chars_without:
            f.write(f"  - {char}\n")

    print(f"✅ Rapport détaillé: {report_path}")
    print(f"\nPour appliquer le tri, remplacez select.def par select_sorted.def")

if __name__ == '__main__':
    main()
