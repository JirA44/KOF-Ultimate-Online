#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère les portraits pour l'encyclopédie
Cherche les fichiers d'images dans chars/ et crée un mapping
"""

import os
import json
from pathlib import Path
import shutil

# Chemins
BASE_DIR = Path("D:/KOF Ultimate Online")
CHARS_DIR = BASE_DIR / "chars"
PORTRAITS_DIR = BASE_DIR / "portraits_encyclopedia"
OUTPUT_JSON = BASE_DIR / "portraits_mapping.json"

# Extensions d'images recherchées
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.sff']

def find_portrait_for_character(char_name, char_dir):
    """
    Cherche le portrait d'un personnage
    Priorité:
    1. portrait.png/jpg
    2. [nom].png/jpg
    3. face.png/jpg
    4. Premier .png trouvé
    5. Première image dans .sff (si disponible)
    """

    # Lister tous les fichiers
    files = list(char_dir.iterdir())

    # Rechercher par priorité
    priorities = [
        f"portrait{ext}" for ext in IMAGE_EXTENSIONS
    ] + [
        f"{char_name.lower()}{ext}" for ext in IMAGE_EXTENSIONS
    ] + [
        f"face{ext}" for ext in IMAGE_EXTENSIONS
    ] + [
        f"icon{ext}" for ext in IMAGE_EXTENSIONS
    ]

    # Essayer les noms prioritaires
    for filename in priorities:
        for file in files:
            if file.name.lower() == filename.lower():
                return file

    # Sinon, chercher le premier PNG
    for file in files:
        if file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif']:
            return file

    return None

def create_portraits_dir():
    """Crée le dossier portraits_encyclopedia"""
    PORTRAITS_DIR.mkdir(exist_ok=True)
    print(f"✓ Dossier créé: {PORTRAITS_DIR}")

def scan_all_characters():
    """Scanne tous les personnages et leurs portraits"""

    if not CHARS_DIR.exists():
        print(f"❌ Dossier chars introuvable: {CHARS_DIR}")
        return None

    print(f"📂 Scan de: {CHARS_DIR}\n")

    char_dirs = [d for d in CHARS_DIR.iterdir() if d.is_dir()]
    print(f"🔍 {len(char_dirs)} personnages trouvés\n")

    portraits_mapping = {}
    found_count = 0
    missing_count = 0

    for char_dir in sorted(char_dirs):
        char_name = char_dir.name

        # Chercher le portrait
        portrait_file = find_portrait_for_character(char_name, char_dir)

        if portrait_file:
            # Copier dans portraits_encyclopedia
            dest_file = PORTRAITS_DIR / f"{char_name}{portrait_file.suffix}"

            try:
                shutil.copy2(portrait_file, dest_file)

                # Enregistrer le mapping (chemin relatif pour HTML)
                portraits_mapping[char_name] = f"portraits_encyclopedia/{char_name}{portrait_file.suffix}"

                print(f"✓ {char_name}: {portrait_file.name}")
                found_count += 1
            except Exception as e:
                print(f"❌ {char_name}: Erreur copie - {e}")
                portraits_mapping[char_name] = None
                missing_count += 1
        else:
            print(f"⚠️  {char_name}: Aucun portrait trouvé")
            portraits_mapping[char_name] = None
            missing_count += 1

    print(f"\n{'='*60}")
    print(f"📊 RÉSUMÉ")
    print(f"{'='*60}")
    print(f"✓ Portraits trouvés: {found_count}")
    print(f"❌ Portraits manquants: {missing_count}")
    print(f"📁 Total personnages: {len(char_dirs)}")

    return portraits_mapping

def save_mapping(mapping):
    """Sauvegarde le mapping JSON"""
    try:
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Mapping sauvegardé: {OUTPUT_JSON}")
        return True
    except Exception as e:
        print(f"\n❌ Erreur sauvegarde: {e}")
        return False

def generate_js_mapping(mapping):
    """Génère un fichier JS pour l'encyclopédie"""

    js_output = BASE_DIR / "portraits_mapping.js"

    # Créer le contenu JavaScript
    js_content = "// Mapping des portraits - Généré automatiquement\n"
    js_content += "const portraitsMapping = {\n"

    for char_name, portrait_path in sorted(mapping.items()):
        if portrait_path:
            js_content += f'  "{char_name}": "{portrait_path}",\n'
        else:
            js_content += f'  "{char_name}": null,\n'

    js_content += "};\n"

    try:
        with open(js_output, 'w', encoding='utf-8') as f:
            f.write(js_content)

        print(f"✓ Fichier JS créé: {js_output}")
        return True
    except Exception as e:
        print(f"❌ Erreur création JS: {e}")
        return False

def main():
    """Point d'entrée"""
    print("="*60)
    print("📸  GÉNÉRATION PORTRAITS ENCYCLOPÉDIE")
    print("="*60)
    print()

    # Créer le dossier portraits
    create_portraits_dir()
    print()

    # Scanner tous les personnages
    mapping = scan_all_characters()

    if mapping:
        # Sauvegarder le mapping
        save_mapping(mapping)

        # Générer le fichier JS
        generate_js_mapping(mapping)

        print(f"\n{'='*60}")
        print("✅ TERMINÉ!")
        print(f"{'='*60}")
        print("\nProchaine étape:")
        print("• Mettre à jour ENCYCLOPEDIE_PERSONNAGES.html")
        print("• Ajouter <script src='portraits_mapping.js'></script>")
        print("• Afficher les portraits dans les cartes personnages")

    input("\nAppuyez sur ENTRÉE pour fermer...")

if __name__ == "__main__":
    main()
