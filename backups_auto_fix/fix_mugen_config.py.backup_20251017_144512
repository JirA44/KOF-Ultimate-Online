"""
Répare mugen.cfg pour supprimer les doublons d'options plugin
"""
import re
from pathlib import Path

config_path = Path(r"D:\KOF Ultimate Online\data\mugen.cfg")

print("Réparation de mugen.cfg...")

# Lire le fichier
content = config_path.read_text(encoding='utf-8', errors='ignore')

# Créer un backup
backup_path = config_path.with_suffix('.cfg.backup')
if not backup_path.exists():
    backup_path.write_text(content, encoding='utf-8')
    print(f"✓ Backup créé: {backup_path}")

# Parser manuellement pour garder qu'un seul plugin
lines = content.split('\n')
new_lines = []
in_music_section = False
plugin_found = False

for line in lines:
    # Détecter début de section
    if line.strip().startswith('[Music]'):
        in_music_section = True
        plugin_found = False
        new_lines.append(line)
        continue

    # Détecter début d'une autre section
    if line.strip().startswith('[') and not line.strip().startswith('[Music]'):
        in_music_section = False
        plugin_found = False

    # Dans la section Music, commenter les plugins après le premier
    if in_music_section and line.strip().startswith('plugin ='):
        if not plugin_found:
            new_lines.append(line)
            plugin_found = True
        else:
            # Commenter les plugins supplémentaires
            new_lines.append('; ' + line.lstrip())
    else:
        new_lines.append(line)

# Écrire le fichier réparé
config_path.write_text('\n'.join(new_lines), encoding='utf-8')
print("✓ mugen.cfg réparé - seul le premier plugin est actif")
print("  Les autres plugins sont commentés")
