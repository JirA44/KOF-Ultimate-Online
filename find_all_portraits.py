#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chercher TOUS les fichiers portraits dans tout le répertoire KOF
"""
import os

ROOT_DIR = r"D:\KOF Ultimate Online"

def find_all_portraits():
    """Trouve tous les fichiers 9000,0.* et 9000,1.* dans tout le répertoire"""
    mini_portraits = []
    big_portraits = []

    print("Recherche de TOUS les fichiers portraits...")
    print("Cela peut prendre quelques minutes...\n")

    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            file_lower = file.lower()

            if file_lower.startswith('9000,0.') or file_lower.startswith('9000_0.'):
                mini_portraits.append(os.path.join(root, file))
            elif file_lower.startswith('9000,1.') or file_lower.startswith('9000_1.'):
                big_portraits.append(os.path.join(root, file))

    print(f"✅ Mini-portraits trouvés: {len(mini_portraits)}")
    print(f"✅ Big portraits trouvés: {len(big_portraits)}\n")

    # Sauvegarder le rapport
    report_path = r"D:\KOF Ultimate Online\ALL_PORTRAITS_FOUND.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=== TOUS LES PORTRAITS TROUVÉS DANS LE SYSTÈME ===\n\n")

        f.write(f"MINI-PORTRAITS (9000,0.*) - Total: {len(mini_portraits)}\n")
        f.write("=" * 80 + "\n")
        for portrait in sorted(mini_portraits):
            f.write(f"{portrait}\n")

        f.write("\n\n" + "=" * 80)
        f.write(f"\n\nBIG PORTRAITS (9000,1.*) - Total: {len(big_portraits)}\n")
        f.write("=" * 80 + "\n")
        for portrait in sorted(big_portraits):
            f.write(f"{portrait}\n")

    print(f"Rapport sauvegardé: {report_path}")

    return mini_portraits, big_portraits

if __name__ == '__main__':
    mini, big = find_all_portraits()
