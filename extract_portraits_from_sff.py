#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXTRACTEUR DE PORTRAITS depuis fichiers .sff MUGEN
Extrait les portraits de l'écran de sélection
"""
import os
import struct
from pathlib import Path
from PIL import Image
import io

def read_sff_v1(file_path):
    """Lit un fichier SFF version 1.x"""
    portraits = []

    with open(file_path, 'rb') as f:
        # Lire l'en-tête
        signature = f.read(12)
        if not signature.startswith(b'ElecbyteSpr'):
            print(f"  ❌ Pas un fichier SFF valide: {file_path}")
            return []

        # Lire les versions
        verhi = struct.unpack('B', f.read(1))[0]
        verlo1 = struct.unpack('B', f.read(1))[0]
        verlo2 = struct.unpack('B', f.read(1))[0]
        verlo3 = struct.unpack('B', f.read(1))[0]

        print(f"  📄 SFF v{verhi}.{verlo1}.{verlo2}.{verlo3}")

        # Lire le nombre de groupes et images
        group_total = struct.unpack('<I', f.read(4))[0]
        image_total = struct.unpack('<I', f.read(4))[0]
        next_subfile = struct.unpack('<I', f.read(4))[0]
        subfile_header_length = struct.unpack('<I', f.read(4))[0]

        print(f"  📊 {group_total} groupes, {image_total} images")

        # Sauter le reste de l'en-tête (palette type + reserved + padding)
        f.read(480)

        # Position actuelle
        current_pos = 512  # Taille de l'en-tête SFF v1

        # Lire tous les sous-fichiers
        for i in range(image_total):
            try:
                # Aller à la position du sous-fichier
                f.seek(current_pos)

                # Lire l'en-tête du sous-fichier
                next_subfile_offset = struct.unpack('<I', f.read(4))[0]
                length = struct.unpack('<I', f.read(4))[0]
                axisx = struct.unpack('<H', f.read(2))[0]
                axisy = struct.unpack('<H', f.read(2))[0]
                groupno = struct.unpack('<H', f.read(2))[0]
                imageno = struct.unpack('<H', f.read(2))[0]
                index = struct.unpack('<H', f.read(2))[0]
                palette = struct.unpack('B', f.read(1))[0]

                # Sauter les 13 bytes de padding
                f.read(13)

                # Lire les données de l'image
                image_data_length = length - 32
                if image_data_length <= 0:
                    continue
                image_data = f.read(image_data_length)

                # Les portraits sont généralement dans le groupe 9000
                if groupno == 9000:
                    portraits.append({
                        'group': groupno,
                        'image': imageno,
                        'axisx': axisx,
                        'axisy': axisy,
                        'data': image_data,
                        'palette': palette,
                        'index': index
                    })
                    print(f"    ✓ Trouvé portrait: groupe={groupno}, image={imageno}")

                # Aller au prochain sous-fichier
                if next_subfile_offset == 0:
                    break
                current_pos = next_subfile_offset

            except Exception as e:
                print(f"    ⚠️ Erreur lecture image {i}: {e}")
                break

    return portraits

def extract_pcx_from_data(data):
    """Extrait une image PCX depuis les données brutes"""
    try:
        # Les données sont souvent en format PCX
        img = Image.open(io.BytesIO(data))
        return img
    except Exception as e:
        print(f"    ⚠️ Erreur extraction PCX: {e}")
        return None

def main():
    print("=" * 60)
    print("📸  EXTRACTION PORTRAITS depuis .sff")
    print("=" * 60)

    base_path = Path(r"D:\KOF Ultimate Online")
    data_path = base_path / "data"
    output_path = base_path / "portraits_extracted"
    output_path.mkdir(exist_ok=True)

    # Chercher tous les fichiers .sff
    sff_files = list(data_path.glob("*.sff"))

    if not sff_files:
        print("❌ Aucun fichier .sff trouvé dans data/")
        return

    print(f"\n✓ Trouvé {len(sff_files)} fichiers .sff:")
    for sff_file in sff_files:
        print(f"  - {sff_file.name}")

    # Extraire les portraits de system.sff (portraits de sélection)
    system_sff = data_path / "system.sff"
    if system_sff.exists():
        print(f"\n🎯 Extraction depuis {system_sff.name}...")
        portraits = read_sff_v1(system_sff)

        if portraits:
            print(f"\n✓ {len(portraits)} portraits trouvés!")
            print("\n🖼️  Conversion en PNG...")

            for idx, portrait in enumerate(portraits):
                try:
                    img = extract_pcx_from_data(portrait['data'])
                    if img:
                        # Nom du fichier
                        filename = f"portrait_{portrait['group']}_{portrait['image']}.png"
                        output_file = output_path / filename

                        # Sauvegarder
                        img.save(output_file, 'PNG')
                        print(f"  ✓ Sauvegardé: {filename}")
                except Exception as e:
                    print(f"  ⚠️ Erreur conversion portrait {idx}: {e}")
        else:
            print("❌ Aucun portrait trouvé (groupe 9000)")
    else:
        print("❌ system.sff non trouvé")

    # Essayer aussi d'extraire depuis les chars/*/sprite.sff
    print("\n" + "=" * 60)
    print("🔍 Recherche portraits dans chars/*/sprite.sff")
    print("=" * 60)

    chars_path = base_path / "chars"
    if chars_path.exists():
        # Chercher tous les fichiers .sff dans les dossiers de personnages
        all_sff_patterns = ["*/sprite.sff", "*/*.sff", "*/sprites.sff"]
        sprite_files = []
        for pattern in all_sff_patterns:
            sprite_files.extend(chars_path.glob(pattern))

        # Dédupliquer
        sprite_files = list(set(sprite_files))

        print(f"\n✓ Trouvé {len(sprite_files)} fichiers .sff dans chars/")

        for sprite_file in sprite_files:
            char_name = sprite_file.parent.name
            print(f"\n📂 {char_name}...")

            try:
                portraits = read_sff_v1(sprite_file)

                if portraits:
                    for portrait in portraits[:1]:  # Prendre seulement le premier portrait
                        try:
                            img = extract_pcx_from_data(portrait['data'])
                            if img:
                                filename = f"{char_name}_portrait.png"
                                output_file = output_path / filename
                                img.save(output_file, 'PNG')
                                print(f"  ✓ Sauvegardé: {filename}")
                                break
                        except Exception as e:
                            print(f"  ⚠️ Erreur: {e}")
            except Exception as e:
                print(f"  ⚠️ Erreur lecture: {e}")

    print("\n" + "=" * 60)
    print(f"✅ EXTRACTION TERMINÉE!")
    print(f"📁 Dossier: {output_path}")
    print("=" * 60)

    input("\nAppuyez sur ENTRÉE pour fermer...")

if __name__ == "__main__":
    main()
