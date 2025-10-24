#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DISABLE MORE CHARS - Désactive des personnages supplémentaires connus pour crasher
Basé sur les rapports de crash et logs
"""

from pathlib import Path
from datetime import datetime
import shutil

# Liste des personnages à désactiver basée sur les tests
PROBLEMATIC_CHARS = [
    # Déjà désactivés dans corrections précédentes
    "Reyna",  # Erreur CLSN
    "Magnus",  # Animations manquantes

    # Nouveaux suspects basés sur patterns de crash
    "Daiki_Final(Prototype)",  # Crash détecté test #1
    "Graves",  # Crash détecté test #1
]

base_path = Path(r"D:\KOF Ultimate Online")
select_file = base_path / "data" / "select.def"

# Backup
backup_file = select_file.parent / f"select.def.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
shutil.copy2(select_file, backup_file)
print(f"✅ Backup créé: {backup_file.name}")

# Lire
with open(select_file, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

# Modifier
new_lines = []
disabled_count = 0

for line in lines:
    modified = False

    for char in PROBLEMATIC_CHARS:
        # Chercher le personnage (éviter les doublons)
        if line.strip().startswith(f"{char},") and not line.strip().startswith(';'):
            # Le désactiver
            new_lines.append(f"; {line.lstrip()}  ; DÉSACTIVÉ: Crash détecté pendant tests\n")
            disabled_count += 1
            modified = True
            print(f"❌ Désactivé: {char}")
            break

    if not modified:
        new_lines.append(line)

# Écrire
with open(select_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\n✅ {disabled_count} personnages supplémentaires désactivés")
print(f"📄 Backup: {backup_file.name}")

# Compter personnages actifs
active = sum(1 for line in new_lines
             if line.strip() and ',' in line and not line.strip().startswith(';')
             and not line.strip().startswith('['))

print(f"✅ Personnages actifs restants: {active}")
