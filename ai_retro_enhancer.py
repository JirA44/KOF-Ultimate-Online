#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - AI Retro Anime Style Enhancer
Transforme les sprites en style rétro anime 80-90 (aquarelle)
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import numpy as np
import struct
import io

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class MugenSFFReader:
    """Lecteur de fichiers .sff (Sprite File Format) de MUGEN"""

    def __init__(self, sff_path):
        self.sff_path = Path(sff_path)
        self.sprites = {}
        self.header = None

    def read(self):
        """Lit le fichier SFF et extrait tous les sprites"""
        print(f"{Colors.CYAN}Lecture de {self.sff_path.name}...{Colors.RESET}")

        with open(self.sff_path, 'rb') as f:
            # Lire le header
            signature = f.read(12)
            if signature[:11] != b'ElecbyteSpr':
                print(f"{Colors.RED}❌ Fichier SFF invalide{Colors.RESET}")
                return False

            version = struct.unpack('<B', f.read(1))[0]
            print(f"  Version SFF: {version}")

            # Version 1.x (SFF v1)
            if version == 1:
                f.seek(16)  # Skip to sprite count
                groups_count = struct.unpack('<I', f.read(4))[0]
                images_count = struct.unpack('<I', f.read(4))[0]
                subfile_offset = struct.unpack('<I', f.read(4))[0]
                subfile_length = struct.unpack('<I', f.read(4))[0]
                palette_type = struct.unpack('<B', f.read(1))[0]

                print(f"  {images_count} sprites, {groups_count} groupes")

                # Lire les informations des sprites
                f.seek(512)  # Position du premier sprite

                for i in range(images_count):
                    try:
                        next_offset = struct.unpack('<I', f.read(4))[0]
                        length = struct.unpack('<I', f.read(4))[0]
                        x = struct.unpack('<h', f.read(2))[0]
                        y = struct.unpack('<h', f.read(2))[0]
                        group = struct.unpack('<H', f.read(2))[0]
                        index = struct.unpack('<H', f.read(2))[0]
                        linked_index = struct.unpack('<H', f.read(2))[0]
                        use_palette = struct.unpack('<B', f.read(1))[0]
                        f.read(13)  # Padding

                        # Stocker les infos
                        self.sprites[(group, index)] = {
                            'offset': next_offset,
                            'length': length,
                            'x': x,
                            'y': y,
                            'group': group,
                            'index': index
                        }

                        # Limite pour test
                        if i > 0 and i % 100 == 0:
                            print(f"  {i} sprites lus...")

                    except Exception as e:
                        print(f"  Erreur lecture sprite {i}: {e}")
                        break

                print(f"{Colors.GREEN}✓ {len(self.sprites)} sprites extraits{Colors.RESET}")
                return True

            else:
                print(f"{Colors.RED}❌ Version SFF non supportée: {version}{Colors.RESET}")
                return False

class RetroAnimeStyler:
    """Applique le style rétro anime 80-90 aux images"""

    def __init__(self):
        self.style_config = {
            'color_boost': 1.3,      # Boost des couleurs
            'saturation': 1.4,       # Saturation accrue
            'contrast': 1.15,        # Contraste légèrement augmenté
            'brightness': 1.05,      # Légère augmentation de luminosité
            'watercolor_blur': 1.2,  # Flou pour effet aquarelle
            'edge_enhance': 1.5,     # Renforcement des contours
            'grain_amount': 15,      # Quantité de grain
            'pastel_shift': 20       # Décalage vers couleurs pastel
        }

    def apply_retro_anime_style(self, image):
        """
        Applique le style rétro anime 80-90 à une image PIL
        Style aquarelle, couleurs vibrantes, grain de film
        """
        if image is None or image.size[0] == 0:
            return image

        # Convertir en RGBA si nécessaire
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # 1. Sauvegarder le canal alpha
        alpha = image.split()[3]

        # 2. Travailler sur RGB
        rgb_image = image.convert('RGB')

        # 3. Effet aquarelle - Flou léger + renforcement des bords
        watercolor = rgb_image.filter(ImageFilter.GaussianBlur(self.style_config['watercolor_blur']))
        watercolor = watercolor.filter(ImageFilter.EDGE_ENHANCE)

        # 4. Augmenter la saturation (couleurs vives)
        enhancer = ImageEnhance.Color(watercolor)
        saturated = enhancer.enhance(self.style_config['saturation'])

        # 5. Boost du contraste
        enhancer = ImageEnhance.Contrast(saturated)
        contrasted = enhancer.enhance(self.style_config['contrast'])

        # 6. Légère augmentation de luminosité
        enhancer = ImageEnhance.Brightness(contrasted)
        brightened = enhancer.enhance(self.style_config['brightness'])

        # 7. Décalage vers couleurs pastel (réduction légère de l'intensité)
        img_array = np.array(brightened)
        img_array = img_array.astype(np.float32)

        # Décalage vers pastel en ajoutant du blanc
        pastel_shift = self.style_config['pastel_shift']
        img_array = img_array + (255 - img_array) * (pastel_shift / 100)
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)

        result = Image.fromarray(img_array, 'RGB')

        # 8. Ajouter du grain de film (style rétro)
        result = self.add_film_grain(result, self.style_config['grain_amount'])

        # 9. Restaurer le canal alpha
        result = result.convert('RGBA')
        result.putalpha(alpha)

        return result

    def add_film_grain(self, image, amount=15):
        """Ajoute du grain de film pour effet rétro"""
        img_array = np.array(image)
        noise = np.random.normal(0, amount, img_array.shape)
        noisy = img_array + noise
        noisy = np.clip(noisy, 0, 255).astype(np.uint8)
        return Image.fromarray(noisy)

    def apply_cel_shading(self, image, levels=4):
        """Applique un effet de cel-shading (posterization)"""
        # Réduire le nombre de couleurs pour effet anime
        img_array = np.array(image)

        # Posterize each channel
        for i in range(3):  # RGB
            channel = img_array[:, :, i]
            step = 256 // levels
            channel = (channel // step) * step
            img_array[:, :, i] = channel

        return Image.fromarray(img_array)

class CharacterEnhancer:
    """Améliore les sprites d'un personnage"""

    def __init__(self, char_dir):
        self.char_dir = Path(char_dir)
        self.styler = RetroAnimeStyler()
        self.output_dir = self.char_dir / "enhanced_retro"
        self.output_dir.mkdir(exist_ok=True)

    def find_sff_files(self):
        """Trouve tous les fichiers .sff du personnage"""
        sff_files = list(self.char_dir.glob("*.sff"))
        return sff_files

    def enhance_character(self):
        """Améliore tous les sprites du personnage"""
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}▶ Amélioration du personnage: {self.char_dir.name}{Colors.RESET}")
        print(f"{Colors.BLUE}{'─'*70}{Colors.RESET}")

        sff_files = self.find_sff_files()

        if not sff_files:
            print(f"{Colors.YELLOW}⚠ Aucun fichier .sff trouvé{Colors.RESET}")
            return False

        print(f"  Fichiers .sff trouvés: {len(sff_files)}")

        for sff_file in sff_files:
            print(f"\n  Traitement de {sff_file.name}...")

            # Pour l'instant, on va juste lire le fichier
            # La modification complète nécessiterait un éditeur SFF
            reader = MugenSFFReader(sff_file)
            if reader.read():
                print(f"  {Colors.GREEN}✓ Fichier SFF lu avec succès{Colors.RESET}")
                print(f"  {Colors.YELLOW}Note: L'amélioration des sprites nécessite un outil externe{Colors.RESET}")
                print(f"  {Colors.CYAN}→ Extraction manuelle recommandée via MCM (MUGEN Character Manager){Colors.RESET}")

        return True

    def test_style_on_sample(self, sample_image_path):
        """Teste le style sur une image exemple"""
        print(f"\n{Colors.CYAN}Test du style sur image exemple...{Colors.RESET}")

        try:
            img = Image.open(sample_image_path)
            print(f"  Image source: {img.size[0]}x{img.size[1]}")

            # Appliquer le style
            enhanced = self.styler.apply_retro_anime_style(img)

            # Sauvegarder
            output_path = self.output_dir / f"test_retro_anime_{Path(sample_image_path).name}"
            enhanced.save(output_path)

            print(f"{Colors.GREEN}✓ Style appliqué!{Colors.RESET}")
            print(f"  Résultat: {output_path}")

            return True

        except Exception as e:
            print(f"{Colors.RED}❌ Erreur: {e}{Colors.RESET}")
            return False

def print_header():
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'KOF ULTIMATE - AI RETRO ANIME ENHANCER':^80}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

    print(f"{Colors.WHITE}Style: Rétro Anime 80-90 (Aquarelle){Colors.RESET}")
    print(f"{Colors.WHITE}Caractéristiques:{Colors.RESET}")
    print(f"  • Couleurs vibrantes et saturées")
    print(f"  • Effet aquarelle avec contours marqués")
    print(f"  • Grain de film rétro")
    print(f"  • Teintes pastel douces")
    print(f"  • Ombrage cel-shading")
    print()

def main():
    print_header()

    base_dir = Path(r"D:\KOF Ultimate")
    chars_dir = base_dir / "chars"

    if not chars_dir.exists():
        print(f"{Colors.RED}❌ Dossier chars introuvable{Colors.RESET}")
        return

    # Mode de fonctionnement
    print(f"{Colors.BOLD}Modes disponibles:{Colors.RESET}")
    print(f"  1. Analyser un personnage spécifique")
    print(f"  2. Tester le style sur une image")
    print(f"  3. Générer des exemples de style")
    print()

    choice = input(f"{Colors.CYAN}Votre choix (1-3): {Colors.RESET}")

    if choice == '1':
        # Liste des personnages
        char_folders = [d for d in chars_dir.iterdir() if d.is_dir() and d.name != 'x']
        print(f"\n{Colors.WHITE}Personnages disponibles: {len(char_folders)}{Colors.RESET}")

        # Prendre les 10 premiers pour demo
        for i, char in enumerate(char_folders[:10]):
            print(f"  {i+1}. {char.name}")

        char_choice = input(f"\n{Colors.CYAN}Numéro du personnage (1-10): {Colors.RESET}")
        try:
            char_idx = int(char_choice) - 1
            selected_char = char_folders[char_idx]

            enhancer = CharacterEnhancer(selected_char)
            enhancer.enhance_character()

        except (ValueError, IndexError):
            print(f"{Colors.RED}❌ Choix invalide{Colors.RESET}")

    elif choice == '2':
        # Test sur une image
        test_img = input(f"{Colors.CYAN}Chemin de l'image de test: {Colors.RESET}")
        if os.path.exists(test_img):
            enhancer = CharacterEnhancer(base_dir)
            enhancer.test_style_on_sample(test_img)
        else:
            print(f"{Colors.RED}❌ Image introuvable{Colors.RESET}")

    elif choice == '3':
        # Générer des exemples
        print(f"\n{Colors.MAGENTA}Génération d'exemples de style...{Colors.RESET}")
        generate_style_examples(base_dir)

    else:
        print(f"{Colors.RED}❌ Choix invalide{Colors.RESET}")

def generate_style_examples(base_dir):
    """Génère des exemples visuels du style rétro anime"""
    output_dir = base_dir / "ai_enhanced_examples"
    output_dir.mkdir(exist_ok=True)

    styler = RetroAnimeStyler()

    # Créer une image de démonstration avec des couleurs
    print(f"\n{Colors.CYAN}Création d'exemples de palette de couleurs...{Colors.RESET}")

    # Palette de couleurs rétro anime
    colors = [
        (255, 105, 180),  # Rose vif
        (135, 206, 250),  # Bleu ciel
        (255, 218, 185),  # Pêche
        (221, 160, 221),  # Prune
        (152, 251, 152),  # Vert pastel
        (255, 228, 196),  # Bisque
        (176, 224, 230),  # Bleu poudre
        (255, 182, 193),  # Rose clair
    ]

    # Créer une image avec ces couleurs
    img = Image.new('RGB', (800, 400), (240, 240, 240))
    draw = ImageDraw.Draw(img)

    square_size = 100
    for i, color in enumerate(colors):
        x = (i % 4) * 200
        y = (i // 4) * 200
        draw.rectangle([x, y, x + square_size, y + square_size], fill=color)

    # Appliquer le style
    styled = styler.apply_retro_anime_style(img)

    # Sauvegarder
    output_path = output_dir / "retro_anime_palette_example.png"
    styled.save(output_path)

    print(f"{Colors.GREEN}✓ Exemple sauvegardé: {output_path}{Colors.RESET}")

    # Créer un guide de style
    create_style_guide(output_dir, styler)

def create_style_guide(output_dir, styler):
    """Crée un guide visuel du style"""
    guide_path = output_dir / "STYLE_GUIDE_RETRO_ANIME.txt"

    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("  KOF ULTIMATE - GUIDE DU STYLE RÉTRO ANIME 80-90\n")
        f.write("="*80 + "\n\n")

        f.write("CARACTÉRISTIQUES PRINCIPALES:\n\n")

        f.write("1. COULEURS\n")
        f.write("   • Palette vive mais douce (aquarelle)\n")
        f.write("   • Saturation augmentée de 40%\n")
        f.write("   • Décalage vers teintes pastel\n")
        f.write("   • Couleurs inspirées: rose vif, bleu ciel, pêche, prune\n\n")

        f.write("2. TEXTURE\n")
        f.write("   • Effet aquarelle avec léger flou\n")
        f.write("   • Grain de film rétro (15 unités)\n")
        f.write("   • Contours renforcés pour clarté\n\n")

        f.write("3. OMBRAGE\n")
        f.write("   • Cel-shading (4 niveaux de couleur)\n")
        f.write("   • Ombres douces avec transitions\n")
        f.write("   • Reflets pastel\n\n")

        f.write("4. RÉFÉRENCES VISUELLES\n")
        f.write("   • Akira (1988) - couleurs néon vibrantes\n")
        f.write("   • Bubblegum Crisis (1987) - style cyberpunk doux\n")
        f.write("   • City Hunter (1987) - palette urbaine\n")
        f.write("   • Kimagure Orange Road (1987) - teintes pastel\n\n")

        f.write("PARAMÈTRES TECHNIQUES:\n")
        f.write(f"  - Boost couleur: {styler.style_config['color_boost']}\n")
        f.write(f"  - Saturation: {styler.style_config['saturation']}\n")
        f.write(f"  - Contraste: {styler.style_config['contrast']}\n")
        f.write(f"  - Luminosité: {styler.style_config['brightness']}\n")
        f.write(f"  - Flou aquarelle: {styler.style_config['watercolor_blur']}px\n")
        f.write(f"  - Grain: {styler.style_config['grain_amount']}\n")
        f.write(f"  - Décalage pastel: {styler.style_config['pastel_shift']}%\n\n")

        f.write("="*80 + "\n")
        f.write("Pour appliquer ce style, utilisez: python ai_retro_enhancer.py\n")
        f.write("="*80 + "\n")

    print(f"{Colors.GREEN}✓ Guide de style créé: {guide_path}{Colors.RESET}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interruption par l'utilisateur{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Erreur: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
