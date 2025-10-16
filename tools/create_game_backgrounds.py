"""
Générateur de Backgrounds Spectaculaires pour KOF Ultimate
Crée des fonds magnifiques pour les menus et écrans du jeu
"""

import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
from pathlib import Path
import random
import math

# Configuration
OUTPUT_DIR = Path("D:/KOF Ultimate/data/backgrounds")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class GameBackgroundGenerator:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height

    def create_gradient(self, color1, color2, direction='vertical'):
        """Crée un dégradé"""
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)

        for i in range(self.height if direction == 'vertical' else self.width):
            progress = i / (self.height if direction == 'vertical' else self.width)

            r = int(color1[0] + (color2[0] - color1[0]) * progress)
            g = int(color1[1] + (color2[1] - color1[1]) * progress)
            b = int(color1[2] + (color2[2] - color1[2]) * progress)

            if direction == 'vertical':
                draw.line([(0, i), (self.width, i)], fill=(r, g, b))
            else:
                draw.line([(i, 0), (i, self.height)], fill=(r, g, b))

        return img

    def add_energy_effects(self, img, color=(0, 255, 200)):
        """Ajoute des effets d'énergie"""
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Lignes d'énergie diagonales
        for i in range(0, self.width + self.height, 100):
            x1 = i
            y1 = 0
            x2 = 0
            y2 = i

            for thickness in range(3, 0, -1):
                alpha = 50 - (thickness * 10)
                draw.line([(x1, y1), (x2, y2)],
                         fill=color + (alpha,),
                         width=thickness)

        return Image.alpha_composite(img.convert('RGBA'), overlay)

    def add_particles(self, img, count=100):
        """Ajoute des particules lumineuses"""
        draw = ImageDraw.Draw(img)

        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(2, 6)

            brightness = random.randint(150, 255)
            colors = [
                (brightness, brightness, brightness),  # Blanc
                (brightness, brightness, 0),           # Jaune
                (0, brightness, brightness),           # Cyan
                (brightness, 0, brightness),           # Magenta
            ]

            color = random.choice(colors)

            # Dessiner un cercle avec halo
            for r in range(size, 0, -1):
                alpha = int(255 * (r / size))
                draw.ellipse([x-r, y-r, x+r, y+r],
                           fill=color + (alpha,))

        return img

    def create_title_screen(self):
        """Crée l'écran titre principal"""
        print("Creating TITLE SCREEN...")

        # Fond dégradé noir -> violet foncé -> noir
        img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Dégradé radial du centre
        center_x = self.width // 2
        center_y = self.height // 2
        max_radius = math.sqrt(center_x**2 + center_y**2)

        for y in range(self.height):
            for x in range(self.width):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                progress = distance / max_radius

                # Couleurs du centre vers l'extérieur
                if progress < 0.3:
                    # Centre violet brillant
                    r = int(120 * (1 - progress * 3))
                    g = int(50 * (1 - progress * 3))
                    b = int(180 * (1 - progress * 3))
                elif progress < 0.6:
                    # Milieu bleu foncé
                    r = int(40 * (1 - (progress - 0.3) * 3))
                    g = int(60 * (1 - (progress - 0.3) * 3))
                    b = int(140 * (1 - (progress - 0.3) * 3))
                else:
                    # Bordure noir
                    r = g = b = 0

                img.putpixel((x, y), (r, g, b))

        # Ajouter des étoiles
        for _ in range(200):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.choice([1, 1, 1, 2, 2, 3])
            brightness = random.randint(100, 255)
            draw.ellipse([x, y, x+size, y+size],
                        fill=(brightness, brightness, brightness))

        # Sauvegarder
        output_path = OUTPUT_DIR / "title_screen.png"
        img.save(output_path, 'PNG', optimize=True)
        print(f"Saved: {output_path}")
        return output_path

    def create_character_select(self):
        """Crée le fond de sélection des personnages"""
        print("Creating CHARACTER SELECT screen...")

        # Fond dégradé bleu électrique
        img = self.create_gradient(
            (10, 20, 60),      # Bleu foncé en haut
            (30, 10, 80)       # Violet foncé en bas
        )

        # Convertir en RGBA pour les overlays
        img = img.convert('RGBA')

        # Ajouter des lignes d'énergie
        img = self.add_energy_effects(img, color=(0, 150, 255))

        # Ajouter des hexagones en arrière-plan
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        hex_size = 60
        for row in range(-1, self.height // hex_size + 2):
            for col in range(-1, self.width // hex_size + 2):
                x = col * hex_size * 1.5
                y = row * hex_size * 1.7

                if col % 2:
                    y += hex_size * 0.85

                # Dessiner hexagone
                points = []
                for i in range(6):
                    angle = math.radians(60 * i)
                    px = x + hex_size * 0.5 * math.cos(angle)
                    py = y + hex_size * 0.5 * math.sin(angle)
                    points.append((px, py))

                draw.polygon(points, outline=(50, 100, 200, 30), width=2)

        img = Image.alpha_composite(img, overlay)

        # Appliquer un léger flou
        img = img.filter(ImageFilter.GaussianBlur(radius=1))

        # Sauvegarder
        output_path = OUTPUT_DIR / "character_select.png"
        img = img.convert('RGB')
        img.save(output_path, 'PNG', optimize=True)
        print(f"Saved: {output_path}")
        return output_path

    def create_versus_screen(self):
        """Crée l'écran VS"""
        print("Creating VERSUS screen...")

        # Fond noir avec explosion d'énergie au centre
        img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        center_x = self.width // 2
        center_y = self.height // 2

        # Explosion d'énergie du centre
        for radius in range(500, 0, -10):
            progress = (500 - radius) / 500

            # Jaune au centre, rouge vers l'extérieur
            r = int(255 * (1 - progress * 0.3))
            g = int(255 * (1 - progress * 0.8))
            b = int(50 * (1 - progress))

            alpha = int(100 * progress)

            draw.ellipse(
                [center_x - radius, center_y - radius,
                 center_x + radius, center_y + radius],
                fill=(r, g, b)
            )

        # Convertir en RGBA
        img = img.convert('RGBA')

        # Ajouter des rayons lumineux
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        for angle in range(0, 360, 30):
            rad = math.radians(angle)

            # Points du rayon
            x1 = center_x
            y1 = center_y
            x2 = center_x + self.width * math.cos(rad)
            y2 = center_y + self.height * math.sin(rad)

            # Dessiner le rayon avec dégradé
            draw.line([(x1, y1), (x2, y2)], fill=(255, 200, 0, 100), width=5)

        img = Image.alpha_composite(img, overlay)

        # Appliquer un flou radial (motion blur)
        img = img.filter(ImageFilter.GaussianBlur(radius=3))

        # Sauvegarder
        output_path = OUTPUT_DIR / "versus_screen.png"
        img = img.convert('RGB')
        img.save(output_path, 'PNG', optimize=True)
        print(f"Saved: {output_path}")
        return output_path

    def create_victory_screen(self):
        """Crée l'écran de victoire"""
        print("Creating VICTORY screen...")

        # Fond doré brillant
        img = self.create_gradient(
            (80, 60, 20),      # Or foncé en haut
            (255, 215, 0)      # Or brillant en bas
        )

        img = img.convert('RGBA')

        # Ajouter des particules dorées
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Particules scintillantes
        for _ in range(300):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(2, 8)

            brightness = random.randint(200, 255)

            # Dessiner étoile à 4 branches
            for angle in [0, 90, 180, 270]:
                rad = math.radians(angle)
                x2 = x + size * math.cos(rad)
                y2 = y + size * math.sin(rad)
                draw.line([(x, y), (x2, y2)],
                         fill=(brightness, brightness, 200, 200),
                         width=2)

        img = Image.alpha_composite(img, overlay)

        # Augmenter la luminosité
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.3)

        # Sauvegarder
        output_path = OUTPUT_DIR / "victory_screen.png"
        img = img.convert('RGB')
        img.save(output_path, 'PNG', optimize=True)
        print(f"Saved: {output_path}")
        return output_path

    def create_menu_background(self):
        """Crée le fond du menu principal"""
        print("Creating MENU background...")

        # Fond dégradé sombre élégant
        img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Grille cyberpunk
        grid_spacing = 50
        for x in range(0, self.width, grid_spacing):
            # Lignes verticales
            alpha = int(30 + 20 * math.sin(x / 100))
            draw.line([(x, 0), (x, self.height)],
                     fill=(0, 100, 150), width=1)

        for y in range(0, self.height, grid_spacing):
            # Lignes horizontales
            alpha = int(30 + 20 * math.sin(y / 100))
            draw.line([(0, y), (self.width, y)],
                     fill=(0, 100, 150), width=1)

        # Convertir en RGBA
        img = img.convert('RGBA')

        # Ajouter des points lumineux aux intersections
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        for x in range(0, self.width, grid_spacing):
            for y in range(0, self.height, grid_spacing):
                if random.random() < 0.3:  # 30% de chance
                    size = random.randint(2, 4)
                    brightness = random.randint(100, 200)
                    draw.ellipse([x-size, y-size, x+size, y+size],
                               fill=(0, brightness, 255, 150))

        img = Image.alpha_composite(img, overlay)

        # Sauvegarder
        output_path = OUTPUT_DIR / "menu_background.png"
        img = img.convert('RGB')
        img.save(output_path, 'PNG', optimize=True)
        print(f"Saved: {output_path}")
        return output_path

    def create_loading_screen(self):
        """Crée l'écran de chargement"""
        print("Creating LOADING screen...")

        # Fond noir avec cercles concentriques
        img = Image.new('RGB', (self.width, self.height), (5, 5, 15))
        draw = ImageDraw.Draw(img)

        center_x = self.width // 2
        center_y = self.height // 2

        # Cercles concentriques pulsants
        for i in range(10):
            radius = 50 + i * 40
            thickness = 2 + i
            alpha = 255 - i * 20

            color = (0, 100 + i * 15, 200)

            draw.ellipse(
                [center_x - radius, center_y - radius,
                 center_x + radius, center_y + radius],
                outline=color,
                width=thickness
            )

        # Sauvegarder
        output_path = OUTPUT_DIR / "loading_screen.png"
        img.save(output_path, 'PNG', optimize=True)
        print(f"Saved: {output_path}")
        return output_path

def main():
    """Génère tous les backgrounds du jeu"""
    print("=" * 60)
    print("KOF Ultimate - Game Backgrounds Generator")
    print("=" * 60)
    print()

    generator = GameBackgroundGenerator(1280, 720)

    backgrounds = [
        ("Title Screen", generator.create_title_screen),
        ("Character Select", generator.create_character_select),
        ("Versus Screen", generator.create_versus_screen),
        ("Victory Screen", generator.create_victory_screen),
        ("Menu Background", generator.create_menu_background),
        ("Loading Screen", generator.create_loading_screen),
    ]

    print("Generating backgrounds...")
    print("-" * 60)

    generated = []
    for name, gen_func in backgrounds:
        try:
            path = gen_func()
            generated.append((name, path))
        except Exception as e:
            print(f"Error generating {name}: {e}")

    print()
    print("-" * 60)
    print(f"Successfully generated {len(generated)} backgrounds!")
    print()
    print("Backgrounds saved to:", OUTPUT_DIR)
    print()

    # Créer un index
    print("Generated files:")
    for name, path in generated:
        print(f"  • {name}: {path.name}")

    print()
    print("=" * 60)
    print("DONE! Enjoy your beautiful KOF Ultimate! 🎮✨")
    print("=" * 60)

if __name__ == "__main__":
    main()
