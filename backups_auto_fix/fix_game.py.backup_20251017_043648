import os
import shutil
from pathlib import Path

print("=== RÉPARATION DU JEU ===\n")

# Chemin vers le dossier data
data_dir = Path(r"D:\KOF Ultimate\data")
system_def = data_dir / "system.def"

# 1. Restaurer system.def depuis backup
backup = data_dir / "system.def.backup"
if backup.exists():
    print("✓ Restauration system.def depuis backup...")
    shutil.copy2(backup, system_def)
else:
    print("✓ Nettoyage system.def...")
    if system_def.exists():
        content = system_def.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')
        cleaned = []
        for line in lines:
            # Garder les lignes commentées ou sans backgrounds
            if 'data/backgrounds/' not in line or line.strip().startswith(';'):
                cleaned.append(line)
        system_def.write_text('\n'.join(cleaned), encoding='utf-8')

# 2. Nettoyer les fichiers .air dupliqués
print("✓ Nettoyage des fichiers .air...")
chars_dir = data_dir.parent / "chars"
if chars_dir.exists():
    for air_file in chars_dir.rglob("*.air"):
        content = air_file.read_text(encoding='utf-8', errors='ignore')
        # Supprimer les lignes dupliquées
        lines = list(dict.fromkeys(content.split('\n')))
        air_file.write_text('\n'.join(lines), encoding='utf-8')

print("\n✓✓✓ RÉPARATION TERMINÉE ✓✓✓")
print("Le jeu devrait maintenant fonctionner correctement.")
