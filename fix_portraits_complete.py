#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour copier les portraits existants vers la racine et créer des portraits par défaut
"""
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

CHARS_DIR = r"D:\KOF Ultimate Online\chars"
SELECT_DEF = r"D:\KOF Ultimate Online\data\select.def"

def read_select_def():
    """Lit le select.def et extrait la liste des personnages"""
    chars = []
    with open(SELECT_DEF, 'r', encoding='utf-8') as f:
        in_chars = False
        for line in f:
            line = line.strip()
            if line == '[Characters]':
                in_chars = True
                continue
            if in_chars:
                if line.startswith('['):
                    break
                if line and not line.startswith(';'):
                    chars.append(line)
    return chars

def find_portrait_in_subfolders(char_dir):
    """Cherche récursivement un portrait dans les sous-dossiers"""
    mini_portrait = None
    big_portrait = None

    for root, dirs, files in os.walk(char_dir):
        for file in files:
            file_lower = file.lower()
            if (file_lower.startswith('9000,0.') or file_lower.startswith('9000_0.')) and not mini_portrait:
                mini_portrait = os.path.join(root, file)
            if (file_lower.startswith('9000,1.') or file_lower.startswith('9000_1.')) and not big_portrait:
                big_portrait = os.path.join(root, file)

            if mini_portrait and big_portrait:
                break
        if mini_portrait and big_portrait:
            break

    return mini_portrait, big_portrait

def copy_portrait_to_root(char_name):
    """Copie le portrait trouvé vers la racine du dossier personnage"""
    char_dir = os.path.join(CHARS_DIR, char_name)
    if not os.path.exists(char_dir):
        return False, "Dossier introuvable"

    mini, big = find_portrait_in_subfolders(char_dir)

    copied = False

    # Copier le mini portrait
    if mini:
        ext = os.path.splitext(mini)[1]
        dest = os.path.join(char_dir, f"9000,0{ext}")
        if not os.path.exists(dest):
            shutil.copy2(mini, dest)
            print(f"  ✅ Copié mini: {char_name}")
            copied = True

    # Copier le big portrait
    if big:
        ext = os.path.splitext(big)[1]
        dest = os.path.join(char_dir, f"9000,1{ext}")
        if not os.path.exists(dest):
            shutil.copy2(big, dest)
            print(f"  ✅ Copié big: {char_name}")
            copied = True

    return copied, "OK" if copied else "Pas de portrait trouvé"

def create_default_portrait(char_name, portrait_type='mini'):
    """Crée un portrait par défaut (PNG noir avec le nom)"""
    char_dir = os.path.join(CHARS_DIR, char_name)
    if not os.path.exists(char_dir):
        return False

    # Taille du portrait
    if portrait_type == 'mini':
        width, height = 27, 27
        filename = "9000,0.png"
    else:
        width, height = 100, 100
        filename = "9000,1.png"

    dest_path = os.path.join(char_dir, filename)

    # Ne pas écraser si existe déjà
    if os.path.exists(dest_path):
        return False

    # Créer image noire
    img = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(img)

    # Ajouter texte (nom du personnage)
    try:
        # Tenter d'utiliser une police par défaut
        text = char_name[:10]  # Limiter à 10 caractères
        # Dessiner juste un point blanc au centre comme indicateur
        center_x, center_y = width // 2, height // 2
        draw.rectangle([center_x-1, center_y-1, center_x+1, center_y+1], fill='white')
    except:
        pass

    # Sauvegarder
    img.save(dest_path)
    return True

def main():
    print("=== RÉPARATION COMPLÈTE DES PORTRAITS ===\n")

    chars = read_select_def()
    print(f"Total personnages: {len(chars)}\n")

    stats = {
        'copied': 0,
        'created_mini': 0,
        'created_big': 0,
        'skipped': 0
    }

    # Étape 1: Copier les portraits existants depuis les sous-dossiers
    print("ÉTAPE 1: Copie des portraits depuis sous-dossiers...\n")
    for char in chars:
        copied, msg = copy_portrait_to_root(char)
        if copied:
            stats['copied'] += 1

    print(f"\n✅ {stats['copied']} portraits copiés\n")

    # Étape 2: Créer des portraits par défaut pour ceux manquants
    print("ÉTAPE 2: Création portraits par défaut...\n")
    for char in chars:
        char_dir = os.path.join(CHARS_DIR, char)
        if not os.path.exists(char_dir):
            continue

        # Vérifier mini portrait
        mini_exists = any(os.path.exists(os.path.join(char_dir, f"9000,0{ext}"))
                          for ext in ['.pcx', '.png', '.bmp'])

        if not mini_exists:
            if create_default_portrait(char, 'mini'):
                print(f"  🆕 Créé mini par défaut: {char}")
                stats['created_mini'] += 1

        # Vérifier big portrait
        big_exists = any(os.path.exists(os.path.join(char_dir, f"9000,1{ext}"))
                         for ext in ['.pcx', '.png', '.bmp'])

        if not big_exists:
            if create_default_portrait(char, 'big'):
                print(f"  🆕 Créé big par défaut: {char}")
                stats['created_big'] += 1

    print(f"\n✅ TERMINÉ!")
    print(f"   Portraits copiés: {stats['copied']}")
    print(f"   Mini-portraits créés: {stats['created_mini']}")
    print(f"   Big portraits créés: {stats['created_big']}")

if __name__ == '__main__':
    main()
