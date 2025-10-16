#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - Batch Sprite Enhancer
Améliore en masse les sprites extraits en style rétro anime 80-90
"""

import os
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
from tqdm import tqdm

class RetroAnime80sStyler:
    """Style rétro anime 80-90 avec effet aquarelle"""

    def __init__(self, intensity='normal'):
        # Configurations de style
        self.profiles = {
            'light': {
                'saturation': 1.2,
                'contrast': 1.1,
                'brightness': 1.03,
                'watercolor_blur': 0.8,
                'grain': 10,
                'pastel_shift': 15
            },
            'normal': {
                'saturation': 1.4,
                'contrast': 1.15,
                'brightness': 1.05,
                'watercolor_blur': 1.2,
                'grain': 15,
                'pastel_shift': 20
            },
            'heavy': {
                'saturation': 1.6,
                'contrast': 1.2,
                'brightness': 1.08,
                'watercolor_blur': 1.5,
                'grain': 20,
                'pastel_shift': 25
            }
        }

        self.config = self.profiles.get(intensity, self.profiles['normal'])

    def enhance(self, image):
        """Applique le style complet"""
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # Sauvegarder alpha
        alpha = image.split()[3]
        rgb = image.convert('RGB')

        # Pipeline d'amélioration
        result = rgb

        # 1. Effet aquarelle (flou + edge enhance)
        result = result.filter(ImageFilter.GaussianBlur(self.config['watercolor_blur']))
        result = result.filter(ImageFilter.EDGE_ENHANCE_MORE)

        # 2. Boost saturation
        result = ImageEnhance.Color(result).enhance(self.config['saturation'])

        # 3. Ajuster contraste
        result = ImageEnhance.Contrast(result).enhance(self.config['contrast'])

        # 4. Ajuster luminosité
        result = ImageEnhance.Brightness(result).enhance(self.config['brightness'])

        # 5. Décalage pastel
        arr = np.array(result, dtype=np.float32)
        pastel = arr + (255 - arr) * (self.config['pastel_shift'] / 100)
        pastel = np.clip(pastel, 0, 255).astype(np.uint8)
        result = Image.fromarray(pastel)

        # 6. Grain de film
        arr = np.array(result, dtype=np.float32)
        noise = np.random.normal(0, self.config['grain'], arr.shape)
        grain = arr + noise
        grain = np.clip(grain, 0, 255).astype(np.uint8)
        result = Image.fromarray(grain)

        # Restaurer alpha
        result = result.convert('RGBA')
        result.putalpha(alpha)

        return result

def enhance_directory(input_dir, output_dir, intensity='normal'):
    """Améliore tous les PNG/BMP d'un dossier"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    styler = RetroAnime80sStyler(intensity)

    # Trouver toutes les images
    extensions = ['*.png', '*.PNG', '*.bmp', '*.BMP', '*.jpg', '*.JPG']
    images = []
    for ext in extensions:
        images.extend(input_path.glob(ext))

    if not images:
        print(f"Aucune image trouvée dans {input_dir}")
        return

    print(f"\n{'='*70}")
    print(f"  Amélioration en style Rétro Anime 80-90")
    print(f"  Intensité: {intensity.upper()}")
    print(f"  {len(images)} images à traiter")
    print(f"{'='*70}\n")

    # Traiter chaque image
    success = 0
    for img_path in tqdm(images, desc="Traitement"):
        try:
            img = Image.open(img_path)
            enhanced = styler.enhance(img)

            # Sauvegarder avec le même nom
            output_file = output_path / img_path.name
            enhanced.save(output_file, 'PNG')

            success += 1

        except Exception as e:
            print(f"\n❌ Erreur sur {img_path.name}: {e}")

    print(f"\n✓ {success}/{len(images)} images améliorées")
    print(f"  Dossier de sortie: {output_path}")

def create_demo_comparison(output_dir):
    """Crée une démo visuelle du style"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Créer une image de test avec des formes colorées
    width, height = 800, 600
    img = Image.new('RGBA', (width, height), (255, 255, 255, 255))

    # Dessiner des formes colorées (simulant un sprite)
    from PIL import ImageDraw

    draw = ImageDraw.Draw(img)

    # Palette rétro anime
    colors = [
        (255, 105, 180, 255),  # Rose vif
        (135, 206, 250, 255),  # Bleu ciel
        (255, 218, 185, 255),  # Pêche
        (221, 160, 221, 255),  # Prune
        (152, 251, 152, 255),  # Vert pastel
        (255, 228, 196, 255),  # Bisque
    ]

    # Dessiner des cercles
    for i, color in enumerate(colors):
        x = (i % 3) * 250 + 125
        y = (i // 3) * 250 + 125
        draw.ellipse([x-80, y-80, x+80, y+80], fill=color)

    # Sauvegarder l'original
    img.save(output_path / "demo_original.png")

    # Créer 3 versions avec différentes intensités
    for intensity in ['light', 'normal', 'heavy']:
        styler = RetroAnime80sStyler(intensity)
        enhanced = styler.enhance(img)
        enhanced.save(output_path / f"demo_retro_{intensity}.png")

    print(f"\n✓ Démonstrations créées dans: {output_path}")
    print(f"  - demo_original.png")
    print(f"  - demo_retro_light.png")
    print(f"  - demo_retro_normal.png")
    print(f"  - demo_retro_heavy.png")

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("\nUtilisation:")
        print(f"  {sys.argv[0]} demo              - Créer des démos")
        print(f"  {sys.argv[0]} <dossier_input>   - Améliorer un dossier")
        print(f"  {sys.argv[0]} <input> <output>  - Spécifier entrée/sortie")
        print(f"  {sys.argv[0]} <input> <output> <intensity>  - Avec intensité")
        print()
        print("Intensités disponibles: light, normal, heavy")
        sys.exit(1)

    if sys.argv[1] == 'demo':
        create_demo_comparison(r"D:\KOF Ultimate\ai_enhanced_demos")
    elif len(sys.argv) == 2:
        input_dir = sys.argv[1]
        output_dir = os.path.join(input_dir, "enhanced_retro")
        enhance_directory(input_dir, output_dir)
    elif len(sys.argv) == 3:
        enhance_directory(sys.argv[1], sys.argv[2])
    else:
        enhance_directory(sys.argv[1], sys.argv[2], sys.argv[3])
