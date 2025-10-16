"""
Générateur de Backgrounds Spatiaux pour KOF Ultimate
Crée des fonds d'écran de type galaxie, planètes, nébuleuses, univers
"""

import os
import random
import math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from pathlib import Path

# Configuration
OUTPUT_DIR = Path("D:/KOF Ultimate/stages/space_backgrounds")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class SpaceBackgroundGenerator:
    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height

    def create_starfield(self, num_stars=500, colors=None):
        """Crée un champ d'étoiles"""
        if colors is None:
            colors = ['white', '#ffffaa', '#aaaaff', '#ffaaaa']

        img = Image.new('RGB', (self.width, self.height), 'black')
        draw = ImageDraw.Draw(img)

        for _ in range(num_stars):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.choice([1, 1, 1, 2, 2, 3])
            color = random.choice(colors)
            brightness = random.randint(150, 255)

            if color == 'white':
                color = (brightness, brightness, brightness)

            draw.ellipse([x, y, x+size, y+size], fill=color)

        return img

    def create_nebula(self, colors):
        """Crée un effet nébuleuse"""
        img = Image.new('RGB', (self.width, self.height), 'black')
        draw = ImageDraw.Draw(img)

        # Créer plusieurs "nuages" de nébuleuse
        num_clouds = random.randint(5, 10)
        for _ in range(num_clouds):
            x = random.randint(-200, self.width + 200)
            y = random.randint(-200, self.height + 200)
            radius = random.randint(200, 500)

            color = random.choice(colors)
            alpha = random.randint(30, 80)

            # Dessiner un cercle flou
            for i in range(3):
                r = radius - (i * 50)
                draw.ellipse(
                    [x-r, y-r, x+r, y+r],
                    fill=color
                )

        # Appliquer un flou gaussien pour l'effet nébuleuse
        img = img.filter(ImageFilter.GaussianBlur(radius=50))

        return img

    def create_planet(self, x, y, radius, color, has_rings=False):
        """Crée une planète"""
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Dessiner la planète
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)

        # Ajouter de l'ombre pour l'effet 3D
        shadow_color = tuple([max(0, c - 50) for c in color[:3]])
        for i in range(10):
            offset = i * 2
            alpha = int(255 * (1 - i/10))
            shadow = tuple(list(shadow_color) + [alpha])
            draw.ellipse(
                [x-radius+offset, y-radius, x+radius+offset, y+radius],
                fill=shadow
            )

        # Ajouter des anneaux si demandé
        if has_rings:
            ring_color = (200, 180, 150, 150)
            for i in range(3):
                ring_radius = radius + 20 + (i * 15)
                draw.ellipse(
                    [x-ring_radius, y-5, x+ring_radius, y+5],
                    outline=ring_color,
                    width=8-i*2
                )

        return img

    def create_galaxy_spiral(self):
        """Crée une galaxie spirale"""
        img = Image.new('RGB', (self.width, self.height), 'black')
        draw = ImageDraw.Draw(img)

        center_x = self.width // 2
        center_y = self.height // 2

        # Créer les bras spiraux
        for arm in range(3):
            angle_offset = arm * (2 * math.pi / 3)
            num_points = 200

            for i in range(num_points):
                t = i / num_points
                angle = angle_offset + t * 4 * math.pi
                radius = t * min(self.width, self.height) * 0.4

                x = int(center_x + radius * math.cos(angle))
                y = int(center_y + radius * math.sin(angle))

                # Variation de taille et luminosité
                size = random.randint(1, 4)
                brightness = int(255 * (1 - t * 0.5))
                color = (brightness, brightness, int(brightness * 0.8))

                if 0 <= x < self.width and 0 <= y < self.height:
                    draw.ellipse([x, y, x+size, y+size], fill=color)

        # Ajouter un centre lumineux
        glow_radius = 80
        for i in range(10):
            r = glow_radius - i*8
            alpha = int(255 * (1 - i/10))
            color = (255, 230, 200, alpha)
            draw.ellipse(
                [center_x-r, center_y-r, center_x+r, center_y+r],
                fill=color[:3]
            )

        # Appliquer un léger flou
        img = img.filter(ImageFilter.GaussianBlur(radius=2))

        return img

    def generate_deep_space(self, name="deep_space"):
        """Génère un fond d'espace profond avec étoiles"""
        print(f"Generating {name}...")

        # Fond noir avec étoiles
        img = self.create_starfield(num_stars=800)

        # Ajouter de la nébuleuse violette/bleue
        nebula = self.create_nebula([
            (80, 20, 120),
            (40, 20, 100),
            (60, 10, 140)
        ])
        img = Image.blend(img, nebula, alpha=0.6)

        # Sauvegarder
        output_path = OUTPUT_DIR / f"{name}.png"
        img.save(output_path, 'PNG', optimize=True)
        print(f"Saved: {output_path}")
        return output_path

    def generate_nebula_purple(self, name="nebula_purple"):
        """Génère une nébuleuse violette/rose"""
        print(f"Generating {name}...")

        # Fond noir avec étoiles
        img = self.create_starfield(num_stars=600)

        # Nébuleuse colorée
        nebula = self.create_nebula([
            (180, 50, 180),
            (220, 80, 180),
            (150, 30, 150),
            (200, 100, 200)
        ])
        img = Image.blend(img, nebula, alpha=0.7)

        output_path = OUTPUT_DIR / f"{name}.png"
        img.save(output_path, 'PNG', optimize=True)
        print(f"Saved: {output_path}")
        return output_path

    def generate_planet_scene(self, name="planet_scene"):
        """Génère une scène avec une grosse planète"""
        print(f"Generating {name}...")

        # Fond avec étoiles
        img = self.create_starfield(num_stars=500)

        # Nébuleuse en arrière-plan
        nebula = self.create_nebula([
            (50, 100, 150),
            (30, 80, 130),
            (70, 120, 170)
        ])
        img = Image.blend(img, nebula, alpha=0.5)

        # Ajouter une grande planète
        planet = self.create_planet(
            x=self.width // 4,
            y=self.height * 2 // 3,
            radius=300,
            color=(100, 150, 200),
            has_rings=True
        )
        img.paste(planet, (0, 0), planet)

        # Ajouter une petite lune
        moon = self.create_planet(
            x=self.width * 3 // 4,
            y=self.height // 3,
            radius=80,
            color=(180, 180, 160),
            has_rings=False
        )
        img.paste(moon, (0, 0), moon)

        output_path = OUTPUT_DIR / f"{name}.png"
        img.save(output_path, 'PNG', optimize=True)
        print(f"Saved: {output_path}")
        return output_path

    def generate_galaxy_view(self, name="galaxy_spiral"):
        """Génère une vue de galaxie spirale"""
        print(f"Generating {name}...")

        # Fond avec étoiles lointaines
        img = self.create_starfield(num_stars=300)

        # Galaxie spirale
        galaxy = self.create_galaxy_spiral()
        img = Image.blend(img, galaxy, alpha=0.9)

        output_path = OUTPUT_DIR / f"{name}.png"
        img.save(output_path, 'PNG', optimize=True)
        print(f"Saved: {output_path}")
        return output_path

    def generate_binary_star(self, name="binary_stars"):
        """Génère une scène avec deux soleils"""
        print(f"Generating {name}...")

        # Fond noir avec étoiles
        img = self.create_starfield(num_stars=400)
        draw = ImageDraw.Draw(img)

        # Premier soleil (rouge)
        sun1_x = self.width // 3
        sun1_y = self.height // 4
        for i in range(20):
            r = 150 - i*7
            alpha = 255 - i*12
            color = (255, max(0, 100 - i*5), 0)
            draw.ellipse(
                [sun1_x-r, sun1_y-r, sun1_x+r, sun1_y+r],
                fill=color
            )

        # Deuxième soleil (bleu)
        sun2_x = self.width * 2 // 3
        sun2_y = self.height // 3
        for i in range(18):
            r = 120 - i*6
            alpha = 255 - i*14
            color = (0, max(0, 150 - i*8), 255)
            draw.ellipse(
                [sun2_x-r, sun2_y-r, sun2_x+r, sun2_y+r],
                fill=color
            )

        # Appliquer un flou
        img = img.filter(ImageFilter.GaussianBlur(radius=3))

        output_path = OUTPUT_DIR / f"{name}.png"
        img.save(output_path, 'PNG', optimize=True)
        print(f"Saved: {output_path}")
        return output_path

    def generate_cosmic_void(self, name="cosmic_void"):
        """Génère un vide cosmique mystérieux"""
        print(f"Generating {name}...")

        # Fond très sombre
        img = Image.new('RGB', (self.width, self.height), (5, 5, 15))

        # Peu d'étoiles, très espacées
        img = Image.blend(img, self.create_starfield(num_stars=150), alpha=0.8)

        # Nébuleuse très sombre
        nebula = self.create_nebula([
            (20, 10, 40),
            (10, 5, 30),
            (30, 15, 50)
        ])
        img = Image.blend(img, nebula, alpha=0.4)

        output_path = OUTPUT_DIR / f"{name}.png"
        img.save(output_path, 'PNG', optimize=True)
        print(f"Saved: {output_path}")
        return output_path

def create_stage_def(stage_name, display_name, image_filename):
    """Crée un fichier .def pour un stage"""
    def_content = f"""[Info]
name = "{stage_name}"
displayname = "{display_name}"
mugenversion = 1.0
author = "KOF Ultimate - Space Pack"

[Camera]
startx = 0
starty = 0
boundleft = -139
boundright = 139
boundhigh = -25
boundlow = 0
verticalfollow = 0.8
floortension = 100
tension = 100

[PlayerInfo]
p1startx = -70
p1starty = 0
p1startz = 0
p1facing = 1
p2startx = 70
p2starty = 0
p2startz = 0
p2facing = -1
leftbound  = -1000
rightbound = 1000
topbound  = 0
botbound  = 0

[Bound]
screenleft = 15
screenright = 15

[StageInfo]
zoffset = 240
zoffsetlink = -1
autoturn = 1
resetBG = 0
Hires = 1

[Shadow]
intensity = 128
color = 0,0,0
yscale = 0.4
fade.range = 0,0

[Reflection]
intensity = 0

[Music]
bgmusic = sound/space_ambient.ogg
bgvolume = 180

[BGdef]
spr = stages/space_backgrounds/{stage_name}.sff
debugbg = 0

; Fond spatial principal
[BG MainSpace]
type = normal
spriteno = 0, 0
start = 0, 0
delta = 0.5, 0.5
trans = none
mask = 0

; Étoiles lointaines (parallaxe lent)
[BG DistantStars]
type = normal
spriteno = 0, 1
start = 0, 0
delta = 0.3, 0.3
trans = add
mask = 0

; Étoiles proches (parallaxe rapide)
[BG CloseStars]
type = normal
spriteno = 0, 2
start = 0, 0
delta = 1.2, 1.2
trans = add
mask = 0
"""

    def_path = Path(f"D:/KOF Ultimate/stages/{stage_name}.def")
    with open(def_path, 'w', encoding='utf-8') as f:
        f.write(def_content)

    print(f"Created: {def_path}")
    return def_path

def main():
    """Génère tous les backgrounds spatiaux"""
    print("=" * 60)
    print("KOF Ultimate - Space Backgrounds Generator")
    print("=" * 60)
    print()

    generator = SpaceBackgroundGenerator(1920, 1080)

    # Générer tous les fonds
    backgrounds = [
        ("space_deep", "Deep Space", generator.generate_deep_space),
        ("space_nebula_purple", "Purple Nebula", generator.generate_nebula_purple),
        ("space_planet", "Planet View", generator.generate_planet_scene),
        ("space_galaxy", "Spiral Galaxy", generator.generate_galaxy_view),
        ("space_binary", "Binary Stars", generator.generate_binary_star),
        ("space_void", "Cosmic Void", generator.generate_cosmic_void),
    ]

    print("\nGenerating backgrounds...")
    print("-" * 60)

    generated = []
    for stage_name, display_name, gen_func in backgrounds:
        try:
            image_path = gen_func(stage_name)
            generated.append((stage_name, display_name, image_path))
        except Exception as e:
            print(f"Error generating {stage_name}: {e}")

    print()
    print("-" * 60)
    print(f"Successfully generated {len(generated)} backgrounds!")
    print()

    # Créer les fichiers .def
    print("Creating stage definition files...")
    print("-" * 60)

    for stage_name, display_name, image_path in generated:
        try:
            create_stage_def(stage_name, display_name, image_path.name)
        except Exception as e:
            print(f"Error creating .def for {stage_name}: {e}")

    print()
    print("=" * 60)
    print("DONE!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Convert PNG images to SFF format using Fighter Factory")
    print("2. Place .sff files in: D:/KOF Ultimate/stages/space_backgrounds/")
    print("3. Add stages to data/select.def")
    print()
    print("Images saved to:", OUTPUT_DIR)
    print()

if __name__ == "__main__":
    main()
