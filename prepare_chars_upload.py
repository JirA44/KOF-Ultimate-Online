#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - Préparation Upload chars/
Compresse, splitte et prépare le dossier chars/ pour upload sur cloud
"""

import os
import zipfile
import hashlib
from pathlib import Path
from datetime import datetime
import json

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def get_dir_size(path):
    """Calcule la taille d'un dossier"""
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += get_dir_size(entry.path)
    return total

def format_size(bytes_size):
    """Formate une taille en bytes vers format lisible"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def calculate_md5(filepath):
    """Calcule le MD5 d'un fichier"""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def compress_chars(chars_dir, output_dir, split_size_mb=2000):
    """Compresse le dossier chars/ et le splitte en parties"""

    print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'PRÉPARATION UPLOAD CHARS/':^80}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

    chars_path = Path(chars_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    if not chars_path.exists():
        print(f"{Colors.RED}✗ Dossier chars/ introuvable: {chars_path}{Colors.RESET}")
        return False

    # Analyse du dossier
    print(f"{Colors.CYAN}{Colors.BOLD}Étape 1/5: Analyse{Colors.RESET}")

    char_folders = [d for d in chars_path.iterdir() if d.is_dir()]
    print(f"  Nombre de personnages: {len(char_folders)}")

    total_size = get_dir_size(chars_path)
    print(f"  Taille totale: {format_size(total_size)}")

    split_size_bytes = split_size_mb * 1024 * 1024
    estimated_parts = (total_size // split_size_bytes) + 1
    print(f"  Parties estimées ({split_size_mb}MB chacune): {estimated_parts}\n")

    # Création de l'archive
    print(f"{Colors.CYAN}{Colors.BOLD}Étape 2/5: Compression{Colors.RESET}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"KOF_Ultimate_chars_{timestamp}.zip"
    archive_path = output_path / archive_name

    print(f"  Archive: {archive_name}")
    print(f"  Compression en cours...\n")

    processed_size = 0
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=5) as zipf:
        for char_folder in char_folders:
            print(f"  Ajout: {char_folder.name}...", end='', flush=True)

            for file in char_folder.rglob('*'):
                if file.is_file():
                    arcname = file.relative_to(chars_path.parent)
                    zipf.write(file, arcname)
                    processed_size += file.stat().st_size

                    # Afficher progression
                    percent = (processed_size / total_size) * 100
                    print(f"\r  Progression: {percent:.1f}% ({format_size(processed_size)} / {format_size(total_size)})",
                          end='', flush=True)

    compressed_size = archive_path.stat().st_size
    compression_ratio = (1 - compressed_size / total_size) * 100

    print(f"\n\n{Colors.GREEN}  ✓ Compression terminée{Colors.RESET}")
    print(f"  Taille originale: {format_size(total_size)}")
    print(f"  Taille compressée: {format_size(compressed_size)}")
    print(f"  Ratio compression: {compression_ratio:.1f}%\n")

    # Split si nécessaire
    parts_info = []

    if compressed_size > split_size_bytes:
        print(f"{Colors.CYAN}{Colors.BOLD}Étape 3/5: Découpage{Colors.RESET}")
        print(f"  Découpage en parties de {split_size_mb}MB...\n")

        with open(archive_path, 'rb') as f:
            part_num = 1
            while True:
                chunk = f.read(split_size_bytes)
                if not chunk:
                    break

                part_name = f"{archive_name}.part{part_num:03d}"
                part_path = output_path / part_name

                with open(part_path, 'wb') as part_file:
                    part_file.write(chunk)

                print(f"{Colors.GREEN}  ✓ Partie {part_num}: {part_name} ({format_size(len(chunk))}){Colors.RESET}")

                parts_info.append({
                    'name': part_name,
                    'size': len(chunk),
                    'size_formatted': format_size(len(chunk))
                })

                part_num += 1

        # Supprimer archive complète
        archive_path.unlink()
        print(f"\n{Colors.GREEN}  ✓ Découpage terminé: {part_num - 1} parties{Colors.RESET}\n")
    else:
        print(f"{Colors.CYAN}{Colors.BOLD}Étape 3/5: Découpage{Colors.RESET}")
        print(f"{Colors.GREEN}  ✓ Pas de découpage nécessaire (fichier < {split_size_mb}MB){Colors.RESET}\n")

        parts_info.append({
            'name': archive_name,
            'size': compressed_size,
            'size_formatted': format_size(compressed_size)
        })

    # Calcul checksums
    print(f"{Colors.CYAN}{Colors.BOLD}Étape 4/5: Génération checksums{Colors.RESET}")

    checksums = {}
    for part in parts_info:
        part_path = output_path / part['name']
        print(f"  Calcul MD5: {part['name']}...", end='', flush=True)
        md5 = calculate_md5(part_path)
        checksums[part['name']] = md5
        print(f"\r{Colors.GREEN}  ✓ {part['name']}: {md5}{Colors.RESET}")

    print()

    # Création instructions
    print(f"{Colors.CYAN}{Colors.BOLD}Étape 5/5: Génération instructions{Colors.RESET}")

    instructions = {
        'project': 'KOF ULTIMATE ONLINE',
        'component': 'chars',
        'version': open(Path(r"D:\KOF Ultimate\VERSION.txt")).read().strip(),
        'timestamp': timestamp,
        'original_size': total_size,
        'original_size_formatted': format_size(total_size),
        'compressed_size': compressed_size if len(parts_info) == 1 else sum(p['size'] for p in parts_info),
        'compressed_size_formatted': format_size(compressed_size if len(parts_info) == 1 else sum(p['size'] for p in parts_info)),
        'compression_ratio': f"{compression_ratio:.1f}%",
        'character_count': len(char_folders),
        'parts': parts_info,
        'checksums': checksums
    }

    # Sauvegarder JSON
    json_path = output_path / f"chars_upload_info_{timestamp}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(instructions, f, indent=2, ensure_ascii=False)

    print(f"{Colors.GREEN}  ✓ Fichier info: {json_path.name}{Colors.RESET}")

    # Générer README pour les utilisateurs
    readme_content = f"""# KOF ULTIMATE - Installation des Personnages

## 📦 Informations

- **Version:** {instructions['version']}
- **Date:** {datetime.now().strftime('%d/%m/%Y %H:%M')}
- **Nombre de personnages:** {instructions['character_count']}
- **Taille totale:** {instructions['original_size_formatted']}

## 📥 Téléchargement

"""

    if len(parts_info) > 1:
        readme_content += f"""### Fichiers à télécharger

Téléchargez TOUTES les parties suivantes:

"""
        for i, part in enumerate(parts_info, 1):
            readme_content += f"{i}. **{part['name']}** - {part['size_formatted']}\n"

        readme_content += f"""
### Vérification (MD5 Checksums)

Après téléchargement, vérifiez l'intégrité des fichiers:

"""
        for name, md5 in checksums.items():
            readme_content += f"- `{name}`: `{md5}`\n"

        readme_content += """
## 🔧 Installation

### Étape 1: Télécharger toutes les parties

Assurez-vous d'avoir téléchargé TOUTES les parties listées ci-dessus.

### Étape 2: Reconstituer l'archive

**Windows:**
```batch
copy /b *.part001 + *.part002 + *.part003 [...] KOF_Ultimate_chars.zip
```

**Linux/Mac:**
```bash
cat *.part* > KOF_Ultimate_chars.zip
```

### Étape 3: Vérifier l'intégrité

Utilisez un outil MD5 pour vérifier que les checksums correspondent.

### Étape 4: Extraire

Décompressez l'archive dans le dossier racine de KOF Ultimate:

```
D:\\KOF Ultimate\\chars\\
```

### Étape 5: Vérifier

Lancez le jeu et vérifiez que tous les personnages sont disponibles.

"""
    else:
        readme_content += f"""### Fichier unique

Téléchargez le fichier:

- **{parts_info[0]['name']}** - {parts_info[0]['size_formatted']}

**MD5 Checksum:** `{checksums[parts_info[0]['name']]}`

## 🔧 Installation

1. Téléchargez le fichier
2. Vérifiez le checksum MD5
3. Décompressez dans le dossier racine de KOF Ultimate
4. Le dossier `chars/` sera créé automatiquement
5. Lancez le jeu!

"""

    readme_content += """
## ❓ Problèmes Courants

### Erreur "Archive corrompue"
- Vérifiez les checksums MD5
- Re-téléchargez les parties manquantes/corrompues

### Personnages ne s'affichent pas
- Assurez-vous que le dossier `chars/` est à la racine de KOF Ultimate
- Structure correcte: `D:\\KOF Ultimate\\chars\\[nom_personnage]\\[nom_personnage].def`

### Erreurs au lancement
- Lancez `python auto_repair_system.py` pour réparer automatiquement
- Consultez `mugen.log` pour plus de détails

## 📧 Support

Pour toute aide, consultez le README principal du projet.

---

**Bon jeu! 🎮**
"""

    readme_path = output_path / "README_CHARS_INSTALLATION.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"{Colors.GREEN}  ✓ Instructions: {readme_path.name}{Colors.RESET}\n")

    # Résumé final
    print(f"{Colors.GREEN}{Colors.BOLD}{'='*80}{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}{'✓ PRÉPARATION TERMINÉE':^80}{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

    print(f"{Colors.CYAN}Fichiers créés dans: {output_path}{Colors.RESET}\n")

    for part in parts_info:
        print(f"  📦 {part['name']} ({part['size_formatted']})")

    print(f"\n  📄 {json_path.name}")
    print(f"  📄 {readme_path.name}\n")

    print(f"{Colors.YELLOW}Prochaines étapes:{Colors.RESET}")
    print(f"  1. Uploadez tous les fichiers .part* (ou .zip) sur Google Drive/MEGA")
    print(f"  2. Uploadez aussi README_CHARS_INSTALLATION.md")
    print(f"  3. Créez un lien de partage public")
    print(f"  4. Mettez à jour README.md avec le lien\n")

    return True

def main():
    chars_dir = r"D:\KOF Ultimate\chars"
    output_dir = r"D:\KOF Ultimate\chars_upload_package"

    try:
        compress_chars(chars_dir, output_dir, split_size_mb=2000)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Opération annulée{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Erreur: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
