#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RÉPARATION common1.cns
Copie le fichier common1.cns vers tous les personnages qui en ont besoin
"""
import shutil
from pathlib import Path
import re

def main():
    print("="*70)
    print("🔧 RÉPARATION common1.cns POUR TOUS LES PERSONNAGES")
    print("="*70)

    base_path = Path(r"D:\KOF Ultimate Online")
    source_common = base_path / "data" / "common1.cns"

    if not source_common.exists():
        print("\n❌ ERREUR: data/common1.cns introuvable!")
        print("   Impossible de continuer.")
        input("\nAppuyez sur ENTRÉE...")
        return

    print(f"\n✓ Fichier source trouvé: {source_common}")
    print(f"  Taille: {source_common.stat().st_size} bytes")

    # Lire select.def
    select_def = base_path / "data" / "select.def"
    chars = []

    with open(select_def, 'r', encoding='utf-8') as f:
        in_chars = False
        for line in f:
            line = line.strip()
            if line.startswith('[Characters]'):
                in_chars = True
                continue
            elif line.startswith('['):
                in_chars = False
                continue

            if in_chars and line and not line.startswith(';'):
                if ',' in line:
                    char_name = line.split(',')[0].strip()
                    if char_name:
                        chars.append(char_name)

    print(f"\n✓ {len(chars)} personnages dans select.def")

    # Traiter chaque personnage
    print("\n" + "="*70)
    print("📋 COPIE DE common1.cns")
    print("="*70)

    copied = 0
    skipped = 0
    errors = 0

    chars_path = base_path / "chars"

    for i, char_name in enumerate(chars, 1):
        char_path = chars_path / char_name

        if not char_path.exists():
            print(f"\n[{i}/{len(chars)}] {char_name}")
            print(f"  ⚠️  Dossier introuvable, ignoré")
            skipped += 1
            continue

        # Vérifier si common1.cns existe déjà
        dest_common = char_path / "common1.cns"

        if dest_common.exists():
            print(f"\n[{i}/{len(chars)}] {char_name}")
            print(f"  ✓ common1.cns déjà présent, ignoré")
            skipped += 1
            continue

        # Copier
        try:
            shutil.copy(source_common, dest_common)
            print(f"\n[{i}/{len(chars)}] {char_name}")
            print(f"  ✅ common1.cns copié!")
            copied += 1
        except Exception as e:
            print(f"\n[{i}/{len(chars)}] {char_name}")
            print(f"  ❌ Erreur: {e}")
            errors += 1

    # Rapport
    print("\n" + "="*70)
    print("📊 RAPPORT FINAL")
    print("="*70)
    print(f"\n  Copiés:  {copied}")
    print(f"  Ignorés: {skipped}")
    print(f"  Erreurs: {errors}")

    if copied > 0:
        print("\n✅ RÉPARATION TERMINÉE!")
        print(f"\n   {copied} personnages ont maintenant common1.cns")
        print("\n💡 Prochaines étapes:")
        print("   1. Relancez le jeu")
        print("   2. Testez l'écran de sélection")
        print("   3. Lancez un combat")

    input("\nAppuyez sur ENTRÉE pour fermer...")

if __name__ == "__main__":
    main()
