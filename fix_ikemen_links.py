#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Réparation rapide Ikemen GO - Création liens symboliques
"""

import os
import shutil
from pathlib import Path

ikemen_dir = Path(r"D:\KOF Ultimate Online\Ikemen_GO")
base_dir = Path(r"D:\KOF Ultimate Online")

print()
print("=" * 60)
print(" RÉPARATION IKEMEN GO - Création liens symboliques")
print("=" * 60)
print()

if not ikemen_dir.exists():
    print("❌ Erreur: Ikemen_GO n'existe pas!")
    input("Appuyez sur Entrée...")
    exit(1)

# Dossiers à lier
folders_to_link = ['data', 'font', 'chars', 'stages', 'sound']

for folder in folders_to_link:
    target = ikemen_dir / folder
    source = base_dir / folder

    # Supprimer si existe (fichier, dossier ou lien)
    if target.exists() or target.is_symlink():
        print(f"🗑️  Suppression ancien {folder}...")
        if target.is_symlink() or target.is_file():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(target)

    # Créer lien symbolique (junction sur Windows)
    try:
        import subprocess
        result = subprocess.run(
            ['cmd', '/c', f'mklink /J "{target}" "{source}"'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ {folder} -> lien créé")
        else:
            # Si lien échoue, copier
            print(f"⚠️  {folder} -> copie (lien impossible)")
            shutil.copytree(source, target, dirs_exist_ok=True)
    except Exception as e:
        print(f"❌ {folder} -> erreur: {e}")

print()
print("=" * 60)
print(" ✅ RÉPARATION TERMINÉE!")
print("=" * 60)
print()
print("Ikemen GO devrait maintenant fonctionner.")
print()
input("Appuyez sur Entrée pour fermer...")
