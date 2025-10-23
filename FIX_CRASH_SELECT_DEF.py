#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRECTION CRASH - Garde seulement les personnages simples
"""

import shutil
from pathlib import Path
from datetime import datetime

SELECT_FILE = Path("data/select.def")
BACKUP_FILE = Path(f"data/select.def.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

# Personnages "safe" - vanilla KOF qui ne crashent généralement pas
SAFE_CHARACTERS = [
    "Kyo", "Iori", "Terry", "Mai", "Athena", "Benimaru", "Yuri",
    "Ryo", "Robert", "Andy", "Joe", "Kim", "Chang", "Choi",
    "Leona", "Ralf", "Clark", "Whip", "K", "Maxima",
    "Vanessa", "Ramon", "Blue Mary", "King", "Yashiro",
    "Shermie", "Chris", "Rugal", "Geese", "Krauser"
]

# Mots-clés problématiques (personnages ultra-complexes)
RISKY_KEYWORDS = [
    "blood", "orochi", "chaos", "abyss", "mega", "clone",
    "ultimate", "final", "god", "demon", "omega", "rare"
]

def is_safe_character(line):
    """Vérifie si un personnage est safe"""
    line_lower = line.lower()

    # Déjà commenté
    if line.strip().startswith(';'):
        return False

    # Ligne vide ou section
    if not line.strip() or line.strip().startswith('['):
        return True

    # Contient un mot-clé risqué
    for keyword in RISKY_KEYWORDS:
        if keyword in line_lower:
            return False

    # Contient un nom safe
    for safe in SAFE_CHARACTERS:
        if safe.lower() in line_lower:
            return True

    # Par défaut, considérer risqué
    return False

def create_safe_select_def():
    """Crée un select.def avec seulement les personnages safe"""

    if not SELECT_FILE.exists():
        print(f"❌ {SELECT_FILE} introuvable!")
        return

    # Backup
    print(f"📁 Sauvegarde: {BACKUP_FILE}")
    shutil.copy(SELECT_FILE, BACKUP_FILE)

    # Lire
    with open(SELECT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Filtrer
    safe_lines = []
    removed_count = 0
    kept_count = 0

    in_characters_section = False

    for line in lines:
        # Détecter section [Characters]
        if '[Characters]' in line:
            in_characters_section = True
            safe_lines.append(line)
            continue

        # Autres sections
        if line.strip().startswith('[') and '[Characters]' not in line:
            in_characters_section = False
            safe_lines.append(line)
            continue

        # Dans section personnages
        if in_characters_section:
            if is_safe_character(line):
                # Ligne safe (commentaire, vide, ou perso safe)
                if line.strip() and not line.strip().startswith(';') and not line.strip().startswith('['):
                    kept_count += 1
                safe_lines.append(line)
            else:
                # Personnage risqué - commenter
                if line.strip() and not line.strip().startswith(';'):
                    safe_lines.append(f"; [RISKY_REMOVED] {line}")
                    removed_count += 1
                else:
                    safe_lines.append(line)
        else:
            # Hors section personnages
            safe_lines.append(line)

    # Écrire
    with open(SELECT_FILE, 'w', encoding='utf-8') as f:
        f.writelines(safe_lines)

    print(f"\n✅ Fichier modifié:")
    print(f"   Personnages conservés: {kept_count}")
    print(f"   Personnages retirés: {removed_count}")
    print(f"\n📄 Backup disponible: {BACKUP_FILE}")

    # Résumé
    print(f"\n" + "="*70)
    print("RÉSUMÉ")
    print("="*70)
    print(f"Les personnages complexes/risqués ont été commentés.")
    print(f"Seuls les personnages vanilla KOF simples sont conservés.")
    print(f"\nTestez maintenant le mode VS - il ne devrait plus crasher!")
    print(f"\nSi ça ne marche toujours pas, utilisez:")
    print(f"  - RESTAURER_SELECT_BACKUP.bat")

def main():
    print("="*70)
    print("  🔧 CORRECTION CRASH - SELECT.DEF")
    print("  Retire les personnages complexes qui causent des crashs")
    print("="*70)
    print()

    create_safe_select_def()

    print("\n" + "="*70)
    input("Appuyez sur ENTRÉE...")

if __name__ == "__main__":
    main()
