#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur d'animation pour le fond du menu principal de KOF Ultimate
Crée une animation de fond spectaculaire avec des effets modernes
"""

import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math
import random

class MenuAnimationGenerator:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.frames = []
        self.num_frames = 60  # 60 frames pour une animation fluide

    def create_gradient_background(self, frame_num):
        """Crée un fond avec dégradé animé"""
        img = Image.new('RGB', (self.width, self.height), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Dégradé vertical animé du violet au bleu profond
        offset = int((frame_num / self.num_frames) * 50)

        for y in range(self.height):
            # Calcul de la couleur avec animation
            progress = (y + offset) / self.height
            progress = (progress % 1.0)

            # Palette de couleurs cyber/futuriste
            r = int(50 + 100 * math.sin(progress * math.pi))
            g = int(20 + 80 * math.sin(progress * math.pi + 1))
            b = int(100 + 155 * math.sin(progress * math.pi + 2))

            draw.line([(0, y), (self.width, y)], fill=(r, g, b))

        return img

    def add_particles(self, img, frame_num):
        """Ajoute des particules lumineuses animées"""
        draw = ImageDraw.Draw(img)

        # Nombre de particules
        num_particles = 30

        for i in range(num_particles):
            # Position basée sur le frame et l'index de la particule
            seed = i * 12345
            random.seed(seed + frame_num)

            # Mouvement vertical ondulant
            base_x = (i / num_particles) * self.width
            base_y = ((frame_num + i * 10) % (self.height + 100)) - 50

            # Oscillation horizontale
            x = base_x + 30 * math.sin((frame_num + i * 20) * 0.1)
            y = base_y

            # Taille variable (toujours positive)
            size = abs(2 + 3 * math.sin((frame_num + i * 15) * 0.15))
            if size < 1:
                size = 1

            # Couleur variable (bleu à cyan)
            alpha = int(128 + 127 * math.sin((frame_num + i * 5) * 0.2))
            alpha = max(0, min(255, alpha))  # Clamp entre 0 et 255
            color = (100, 150, 255, alpha)

            # Dessiner la particule comme un cercle lumineux
            if 0 <= x < self.width and 0 <= y < self.height:
                # Halo
                for r in range(int(size + 3), 0, -1):
                    if r > 0:  # S'assurer que r est positif
                        alpha_halo = int(alpha * (r / (size + 3)) * 0.5)
                        alpha_halo = max(0, min(255, alpha_halo))
                        x1, y1 = int(x - r), int(y - r)
                        x2, y2 = int(x + r), int(y + r)
                        if x1 < x2 and y1 < y2:  # Vérifier que les coordonnées sont valides
                            draw.ellipse(
                                [(x1, y1), (x2, y2)],
                                fill=(100, 150, 255, alpha_halo)
                            )

                # Centre brillant
                if size > 0:
                    x1, y1 = int(x - size), int(y - size)
                    x2, y2 = int(x + size), int(y + size)
                    if x1 < x2 and y1 < y2:
                        draw.ellipse(
                            [(x1, y1), (x2, y2)],
                            fill=(200, 220, 255, alpha)
                        )

        return img

    def add_energy_lines(self, img, frame_num):
        """Ajoute des lignes d'énergie animées"""
        draw = ImageDraw.Draw(img)

        num_lines = 8

        for i in range(num_lines):
            # Position et longueur de la ligne
            angle = (frame_num + i * (360 / num_lines)) % 360
            angle_rad = math.radians(angle)

            # Point de départ au centre
            cx, cy = self.width // 2, self.height // 2

            # Longueur variable
            length = 100 + 50 * math.sin((frame_num + i * 10) * 0.1)

            # Point d'arrivée
            x2 = cx + length * math.cos(angle_rad)
            y2 = cy + length * math.sin(angle_rad)

            # Couleur avec transparence
            alpha = int(50 + 50 * math.sin((frame_num + i * 5) * 0.2))

            # Dessiner plusieurs lignes pour créer un effet de lumière
            for width in range(3, 0, -1):
                color_alpha = int(alpha * (width / 3))
                draw.line(
                    [(cx, cy), (x2, y2)],
                    fill=(150, 200, 255, color_alpha),
                    width=width
                )

        return img

    def add_grid_pattern(self, img, frame_num):
        """Ajoute une grille cyber animée"""
        draw = ImageDraw.Draw(img)

        grid_size = 40
        offset_y = (frame_num * 2) % grid_size

        # Lignes horizontales
        for y in range(-grid_size, self.height + grid_size, grid_size):
            y_pos = y + offset_y
            # Effet de perspective (lignes plus épaisses en bas)
            alpha = int(30 + 30 * (y_pos / self.height))
            if 0 <= y_pos < self.height:
                draw.line(
                    [(0, y_pos), (self.width, y_pos)],
                    fill=(80, 120, 180, alpha),
                    width=1
                )

        # Lignes verticales avec effet de distorsion
        for x in range(0, self.width + grid_size, grid_size):
            for y in range(0, self.height, 10):
                y2 = y + 10
                # Distorsion sinusoïdale
                x1 = x + 5 * math.sin((y + frame_num * 2) * 0.05)
                x2 = x + 5 * math.sin((y2 + frame_num * 2) * 0.05)

                alpha = int(20 + 20 * (y / self.height))
                draw.line(
                    [(x1, y), (x2, y2)],
                    fill=(80, 120, 180, alpha),
                    width=1
                )

        return img

    def add_title_text(self, img):
        """Ajoute le titre 'KOF ULTIMATE ONLINE'"""
        draw = ImageDraw.Draw(img, 'RGBA')

        # Essayer de charger une police, sinon utiliser la police par défaut
        try:
            # Taille de police grande pour le titre
            font = ImageFont.truetype("arial.ttf", 60)
            font_small = ImageFont.truetype("arial.ttf", 30)
        except:
            # Police par défaut si Arial n'est pas disponible
            font = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Texte principal
        text = "KOF ULTIMATE"
        text2 = "ONLINE"

        # Calculer la position centrée
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except:
            text_width = len(text) * 10
            text_height = 20

        x = (self.width - text_width) // 2
        y = 50

        # Ombre portée
        for offset in range(5, 0, -1):
            alpha = int(50 * (offset / 5))
            draw.text(
                (x + offset, y + offset),
                text,
                fill=(0, 0, 0, alpha),
                font=font
            )

        # Texte principal avec effet de lueur
        draw.text((x, y), text, fill=(100, 200, 255, 255), font=font)

        # Deuxième ligne "ONLINE"
        try:
            bbox2 = draw.textbbox((0, 0), text2, font=font_small)
            text2_width = bbox2[2] - bbox2[0]
        except:
            text2_width = len(text2) * 8

        x2 = (self.width - text2_width) // 2
        y2 = y + text_height + 20

        # Ombre
        for offset in range(3, 0, -1):
            alpha = int(50 * (offset / 3))
            draw.text(
                (x2 + offset, y2 + offset),
                text2,
                fill=(0, 0, 0, alpha),
                font=font_small
            )

        # Texte
        draw.text((x2, y2), text2, fill=(255, 100, 150, 255), font=font_small)

        return img

    def generate_frame(self, frame_num):
        """Génère un frame complet de l'animation"""
        # 1. Fond dégradé
        img = self.create_gradient_background(frame_num)

        # Convertir en RGBA pour supporter la transparence
        img = img.convert('RGBA')

        # 2. Grille cyber
        img = self.add_grid_pattern(img, frame_num)

        # 3. Lignes d'énergie
        img = self.add_energy_lines(img, frame_num)

        # 4. Particules
        img = self.add_particles(img, frame_num)

        # 5. Titre (seulement sur certains frames pour un effet de pulsation)
        if frame_num % 5 == 0:  # Afficher le titre tous les 5 frames
            img = self.add_title_text(img)

        # Ajouter un léger flou pour un effet plus doux
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

        return img

    def generate_all_frames(self):
        """Génère toutes les frames de l'animation"""
        print(f"Génération de {self.num_frames} frames d'animation...")

        for i in range(self.num_frames):
            frame = self.generate_frame(i)
            self.frames.append(frame)

            if (i + 1) % 10 == 0:
                print(f"  Frames {i + 1}/{self.num_frames} générés")

        print(f"✓ Génération terminée!")
        return self.frames

    def save_frames(self, output_dir="data/backgrounds/menu_animation"):
        """Sauvegarde toutes les frames dans un dossier"""
        os.makedirs(output_dir, exist_ok=True)

        print(f"\nSauvegarde des frames dans {output_dir}...")

        for i, frame in enumerate(self.frames):
            # Convertir en RGB pour le format PNG
            rgb_frame = frame.convert('RGB')
            filename = f"frame_{i:03d}.png"
            filepath = os.path.join(output_dir, filename)
            rgb_frame.save(filepath)

            if (i + 1) % 10 == 0:
                print(f"  {i + 1}/{len(self.frames)} frames sauvegardés")

        print(f"✓ Sauvegarde terminée!")
        print(f"\n📁 Frames sauvegardés dans: {os.path.abspath(output_dir)}")

    def save_as_gif(self, filename="menu_animation.gif", duration=50):
        """Sauvegarde l'animation comme un GIF animé"""
        if not self.frames:
            print("Erreur: Aucun frame à sauvegarder")
            return

        print(f"\nCréation du GIF animé...")

        # Convertir les frames en RGB
        rgb_frames = [frame.convert('RGB') for frame in self.frames]

        # Sauvegarder comme GIF
        rgb_frames[0].save(
            filename,
            save_all=True,
            append_images=rgb_frames[1:],
            duration=duration,
            loop=0
        )

        print(f"✓ GIF créé: {os.path.abspath(filename)}")

def main():
    print("=" * 80)
    print("GÉNÉRATEUR D'ANIMATION POUR LE MENU PRINCIPAL")
    print("=" * 80)
    print()

    # Créer le générateur
    generator = MenuAnimationGenerator(width=640, height=480)

    # Générer les frames
    generator.generate_all_frames()

    # Sauvegarder les frames
    generator.save_frames()

    # Sauvegarder comme GIF pour prévisualisation
    generator.save_as_gif("data/backgrounds/menu_animation_preview.gif")

    print("\n" + "=" * 80)
    print("✓ ANIMATION CRÉÉE AVEC SUCCÈS!")
    print("=" * 80)
    print("\nProchaines étapes:")
    print("1. Vérifiez le GIF: data/backgrounds/menu_animation_preview.gif")
    print("2. Les frames individuels sont dans: data/backgrounds/menu_animation/")
    print("3. Pour intégrer dans le jeu, utilisez un outil de conversion .sff")
    print()

if __name__ == '__main__':
    main()
