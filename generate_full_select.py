#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère un select.def avec TOUS les personnages installés dans chars/
"""

import os

def generate_full_select_def():
    """Génère un select.def avec tous les personnages"""

    chars_dir = "chars"
    output_file = "data/select.def"

    # Lister tous les dossiers dans chars/
    all_chars = []
    for item in os.listdir(chars_dir):
        char_path = os.path.join(chars_dir, item)
        if os.path.isdir(char_path):
            # Vérifier qu'il y a un fichier .def dans le dossier
            def_files = [f for f in os.listdir(char_path) if f.endswith('.def')]
            if def_files:
                all_chars.append(item)

    all_chars.sort()

    print(f"✓ {len(all_chars)} personnages trouvés dans chars/")

    # Générer le select.def
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f";Auto-généré - {len(all_chars)} personnages\n")
        f.write("[Characters]\n")
        for char in all_chars:
            f.write(f"{char}\n")
        f.write("\n[ExtraStages]\n\n")
        f.write("[Options]\n")
        f.write("arcade.maxmatches = 1,1,1,0,0,0,0,0,0,0\n")
        f.write("team.maxmatches = 1,1,1,1,0,0,0,0,0,0\n")

    print(f"✓ Fichier généré: {output_file}")
    print(f"✓ {len(all_chars)} personnages ajoutés")

if __name__ == "__main__":
    generate_full_select_def()
