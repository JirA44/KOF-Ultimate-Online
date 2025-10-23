"""
KOF Ultimate - Modern Launcher
Version 2.0.0 - Ultra Modern Design

Design spectaculaire avec effets visuels avancés
"""

import os
import sys
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance
import random
import math
import time

GAME_PATH = Path(__file__).parent
VERSION = "2.0.0"

# Traductions
TRANSLATIONS = {
    'fr': {
        'title': '⚡ KOF ULTIMATE ONLINE ⚡',
        'subtitle': '━━━━━━━  ULTIMATE EDITION  ━━━━━━━',
        'version': 'v{} • Jeu de Combat Nouvelle Génération',
        'play': '▶  J O U E R  ◀',
        'multiplayer': '🌐  MULTIJOUEUR',
        'ai_player': '🤖  IA JOUEUR',
        'settings': '⚙️  PARAMÈTRES',
        'characters': '🎭 PERSONNAGES DISPONIBLES',
        'char_kyo': 'Kyo Kusanagi',
        'char_iori': 'Iori Yagami',
        'char_terry': 'Terry Bogard',
        'char_mai': 'Mai Shiranui',
        'char_king': 'King',
        'char_ryo': 'Ryo Sakazaki',
        'char_leona': 'Leona Heidern',
        'char_athena': 'Athena Asamiya'
    },
    'en': {
        'title': '⚡ KOF ULTIMATE ONLINE ⚡',
        'subtitle': '━━━━━━━  ULTIMATE EDITION  ━━━━━━━',
        'version': 'v{} • Next-Gen Fighter',
        'play': '▶  P L A Y  ◀',
        'multiplayer': '🌐  MULTIPLAYER',
        'ai_player': '🤖  AI PLAYER',
        'settings': '⚙️  SETTINGS',
        'characters': '🎭 AVAILABLE CHARACTERS',
        'char_kyo': 'Kyo Kusanagi',
        'char_iori': 'Iori Yagami',
        'char_terry': 'Terry Bogard',
        'char_mai': 'Mai Shiranui',
        'char_king': 'King',
        'char_ryo': 'Ryo Sakazaki',
        'char_leona': 'Leona Heidern',
        'char_athena': 'Athena Asamiya'
    }
}

# Personnages disponibles (liste complète du jeu)
CHARACTERS = [
    {'name': 'Kyo Kusanagi', 'icon': '🔥', 'stars': 5},
    {'name': 'Iori Yagami', 'icon': '🌙', 'stars': 5},
    {'name': 'Terry Bogard', 'icon': '⭐', 'stars': 4},
    {'name': 'Mai Shiranui', 'icon': '🌸', 'stars': 4},
    {'name': 'King', 'icon': '👑', 'stars': 4},
    {'name': 'Ryo Sakazaki', 'icon': '🥋', 'stars': 4},
    {'name': 'Leona Heidern', 'icon': '💣', 'stars': 5},
    {'name': 'Athena Asamiya', 'icon': '✨', 'stars': 4},
    {'name': 'Kula Diamond', 'icon': '❄️', 'stars': 5},
    {'name': 'K\'', 'icon': '🔪', 'stars': 5},
    {'name': 'Ash Crimson', 'icon': '💚', 'stars': 4},
    {'name': 'Angel', 'icon': '😈', 'stars': 4},
    {'name': 'Andy Bogard', 'icon': '⚡', 'stars': 4},
    {'name': 'Akuma', 'icon': '👹', 'stars': 5},
    {'name': 'Asura', 'icon': '💪', 'stars': 5},
    {'name': 'Akiha Yagami', 'icon': '🌑', 'stars': 4},
    {'name': 'Alba Meira', 'icon': '⚔️', 'stars': 4},
    {'name': 'Alter Kyo', 'icon': '🔴', 'stars': 5},
    {'name': 'Aika', 'icon': '💃', 'stars': 3},
    {'name': 'Aileen', 'icon': '🎀', 'stars': 3},
    {'name': 'Akari', 'icon': '🌺', 'stars': 3},
    {'name': 'Akira Kazama', 'icon': '🥊', 'stars': 4},
    {'name': 'Alfred', 'icon': '🎩', 'stars': 3},
    {'name': 'Another Scarlet', 'icon': '🩸', 'stars': 4},
    {'name': 'Arctic Emperor', 'icon': '🧊', 'stars': 5},
    {'name': 'Benimaru', 'icon': '⚡', 'stars': 4},
    {'name': 'Billy Kane', 'icon': '🎱', 'stars': 4},
    {'name': 'Blue Mary', 'icon': '💙', 'stars': 4},
    {'name': 'Chang', 'icon': '⚙️', 'stars': 3},
    {'name': 'Choi', 'icon': '🔪', 'stars': 3},
    {'name': 'Chris', 'icon': '🔥', 'stars': 4},
    {'name': 'Clark Still', 'icon': '💪', 'stars': 4},
    {'name': 'Duo Lon', 'icon': '🌫️', 'stars': 4},
    {'name': 'Elisabeth', 'icon': '⚜️', 'stars': 5},
    {'name': 'Gato', 'icon': '🐱', 'stars': 4},
    {'name': 'Geese Howard', 'icon': '👔', 'stars': 5},
    {'name': 'Goenitz', 'icon': '🌪️', 'stars': 5},
    {'name': 'Heidern', 'icon': '🎖️', 'stars': 4},
    {'name': 'Igniz', 'icon': '👼', 'stars': 5},
    {'name': 'Joe Higashi', 'icon': '🥊', 'stars': 4},
    {'name': 'Jhun Hoon', 'icon': '🦵', 'stars': 4},
    {'name': 'Kim Kaphwan', 'icon': '🥋', 'stars': 4},
    {'name': 'Krizalid', 'icon': '🧬', 'stars': 5},
    {'name': 'Kusanagi', 'icon': '🔱', 'stars': 5},
    {'name': 'Kyo-1', 'icon': '🔥', 'stars': 4},
    {'name': 'Kyo-2', 'icon': '🔥', 'stars': 4},
    {'name': 'Lucky Glauber', 'icon': '🏀', 'stars': 3},
    {'name': 'Mature', 'icon': '💜', 'stars': 4},
    {'name': 'Maxima', 'icon': '🤖', 'stars': 4},
    {'name': 'May Lee', 'icon': '🦸', 'stars': 3},
    {'name': 'Mr. Big', 'icon': '🎯', 'stars': 4},
    {'name': 'Orochi', 'icon': '🐍', 'stars': 5},
    {'name': 'Oswald', 'icon': '🃏', 'stars': 4},
    {'name': 'Ralf Jones', 'icon': '💣', 'stars': 4},
    {'name': 'Ramon', 'icon': '🤼', 'stars': 4},
    {'name': 'Robert Garcia', 'icon': '🐉', 'stars': 4},
    {'name': 'Rock Howard', 'icon': '🎸', 'stars': 4},
    {'name': 'Rugal', 'icon': '😈', 'stars': 5},
    {'name': 'Saisyu', 'icon': '👴', 'stars': 4},
    {'name': 'Shermie', 'icon': '💃', 'stars': 4},
    {'name': 'Shingo', 'icon': '📓', 'stars': 3},
    {'name': 'Sho Hayate', 'icon': '🌪️', 'stars': 4},
    {'name': 'Sie Kensou', 'icon': '🥟', 'stars': 4},
    {'name': 'Takuma', 'icon': '👊', 'stars': 4},
    {'name': 'Vice', 'icon': '🖤', 'stars': 4},
    {'name': 'Whip', 'icon': '🔗', 'stars': 4},
    {'name': 'Yamazaki', 'icon': '🔪', 'stars': 4},
    {'name': 'Yashiro', 'icon': '🎸', 'stars': 4},
    {'name': 'Yuki', 'icon': '❄️', 'stars': 3},
    {'name': 'Yuri Sakazaki', 'icon': '🌼', 'stars': 4},
    {'name': 'Zero', 'icon': '0️⃣', 'stars': 5}
]

class ModernLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KOF ULTIMATE ONLINE - Launcher")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)  # Permettre le redimensionnement
        self.root.configure(bg='#000000')

        # Permettre le plein écran avec F11
        self.is_fullscreen = False
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)

        # Variables
        self.mode_var = tk.StringVar(value="windowed")
        self.animation_running = True
        self.current_lang = 'fr'
        self.current_view = 'main'  # 'main' ou 'characters'
        self.main_frame = None
        self.chars_view_frame = None

        # Centrer
        self.center_window()

        # Créer le background animé
        self.create_animated_background()

        # UI
        self.setup_modern_ui()

        # Démarrer l'animation
        self.animate_background()

    def center_window(self):
        """Centre la fenêtre"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_animated_background(self):
        """Crée un fond animé spectaculaire"""
        # Canvas pour l'animation de fond
        self.bg_canvas = tk.Canvas(
            self.root,
            width=1000,
            height=750,
            bg='#000000',
            highlightthickness=0
        )
        self.bg_canvas.place(x=0, y=0)

        # Particules animées
        self.particles = []
        for _ in range(50):
            x = random.randint(0, 1000)
            y = random.randint(0, 750)
            size = random.randint(2, 4)
            speed = random.uniform(0.5, 2.0)
            color = random.choice(['#00ffff', '#ff00ff', '#ffff00', '#00ff00'])

            particle = self.bg_canvas.create_oval(
                x, y, x+size, y+size,
                fill=color,
                outline=''
            )

            self.particles.append({
                'id': particle,
                'x': x,
                'y': y,
                'size': size,
                'speed': speed,
                'angle': random.uniform(0, 2 * math.pi)
            })

    def animate_background(self):
        """Anime le fond"""
        if not self.animation_running:
            return

        for particle in self.particles:
            # Déplacer la particule
            particle['x'] += particle['speed'] * math.cos(particle['angle'])
            particle['y'] += particle['speed'] * math.sin(particle['angle'])

            # Rebondir sur les bords
            if particle['x'] < 0 or particle['x'] > 1000:
                particle['angle'] = math.pi - particle['angle']
            if particle['y'] < 0 or particle['y'] > 750:
                particle['angle'] = -particle['angle']

            # Mettre à jour la position
            self.bg_canvas.coords(
                particle['id'],
                particle['x'],
                particle['y'],
                particle['x'] + particle['size'],
                particle['y'] + particle['size']
            )

        # Continuer l'animation
        self.root.after(30, self.animate_background)

    def setup_modern_ui(self):
        """Configure l'interface ultra-moderne"""
        # Initialiser la liste des labels de personnages
        self.char_labels = []

        # Boutons de langue en haut à droite (position ajustée)
        lang_frame = tk.Frame(self.root, bg='#000000')
        lang_frame.place(x=820, y=60)

        self.lang_fr_btn = tk.Button(
            lang_frame,
            text="🇫🇷 FR",
            font=('Consolas', 11, 'bold'),
            bg='#00ff00',
            fg='#000000',
            activebackground='#00ff88',
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            command=lambda: self.change_language('fr')
        )
        self.lang_fr_btn.pack(side=tk.LEFT, padx=3)

        self.lang_en_btn = tk.Button(
            lang_frame,
            text="🇬🇧 EN",
            font=('Consolas', 11, 'bold'),
            bg='#333333',
            fg='#888888',
            activebackground='#555555',
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            command=lambda: self.change_language('en')
        )
        self.lang_en_btn.pack(side=tk.LEFT, padx=3)

        # Frame principal transparent
        main_frame = tk.Frame(self.root, bg='#000000')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        # MEGA TITRE avec effet néon
        title_canvas = tk.Canvas(
            main_frame,
            width=800,
            height=150,
            bg='#000000',
            highlightthickness=0
        )
        title_canvas.pack(pady=(0, 30))

        # Effet de lueur néon
        colors = ['#ff0080', '#ff00ff', '#8000ff', '#0080ff', '#00ffff']
        for i, color in enumerate(colors):
            title_canvas.create_text(
                400 - i*2, 75 - i*2,
                text="⚡ KOF ULTIMATE ONLINE ⚡",
                font=('Impact', 48, 'bold'),
                fill=color,
                anchor='center'
            )

        # Texte principal (devant)
        title_canvas.create_text(
            400, 75,
            text="⚡ KOF ULTIMATE ONLINE ⚡",
            font=('Impact', 48, 'bold'),
            fill='#ffffff',
            anchor='center'
        )

        # Sous-titre stylé
        self.subtitle_label = tk.Label(
            main_frame,
            text=TRANSLATIONS[self.current_lang]['subtitle'],
            font=('Consolas', 12, 'bold'),
            fg='#00ffff',
            bg='#000000'
        )
        self.subtitle_label.pack(pady=(0, 10))

        self.version_label = tk.Label(
            main_frame,
            text=TRANSLATIONS[self.current_lang]['version'].format(VERSION),
            font=('Consolas', 10, 'italic'),
            fg='#888888',
            bg='#000000'
        )
        self.version_label.pack(pady=(0, 40))

        # Container pour les boutons avec effet de glassmorphism
        buttons_container = tk.Frame(
            main_frame,
            bg='#000000'
        )
        buttons_container.pack()

        # Bouton PLAY ultra-moderne
        play_frame = tk.Frame(buttons_container, bg='#000000')
        play_frame.pack(pady=10)

        self.play_btn = tk.Button(
            play_frame,
            text=TRANSLATIONS[self.current_lang]['play'],
            font=('Impact', 28, 'bold'),
            bg='#00ff00',
            fg='#000000',
            activebackground='#00ff88',
            activeforeground='#000000',
            relief=tk.FLAT,
            bd=0,
            padx=60,
            pady=20,
            cursor='hand2',
            command=self.launch_game
        )
        self.play_btn.pack()

        # Effet hover pour le bouton PLAY
        def on_play_enter(e):
            self.play_btn.config(
                bg='#00ff88',
                font=('Impact', 30, 'bold')
            )

        def on_play_leave(e):
            self.play_btn.config(
                bg='#00ff00',
                font=('Impact', 28, 'bold')
            )

        self.play_btn.bind('<Enter>', on_play_enter)
        self.play_btn.bind('<Leave>', on_play_leave)

        # Boutons secondaires en ligne
        secondary_row = tk.Frame(buttons_container, bg='#000000')
        secondary_row.pack(pady=20)

        # Créer les boutons secondaires et stocker les références
        self.multi_btn = tk.Button(
            secondary_row,
            text=TRANSLATIONS[self.current_lang]['multiplayer'],
            font=('Consolas', 13, 'bold'),
            bg='#0099ff',
            fg='#ffffff',
            activebackground=self.lighten_color('#0099ff'),
            activeforeground='#ffffff',
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=12,
            cursor='hand2',
            command=self.launch_multiplayer
        )
        self.multi_btn.pack(side=tk.LEFT, padx=8)

        self.ai_btn = tk.Button(
            secondary_row,
            text=TRANSLATIONS[self.current_lang]['ai_player'],
            font=('Consolas', 13, 'bold'),
            bg='#ff6600',
            fg='#ffffff',
            activebackground=self.lighten_color('#ff6600'),
            activeforeground='#ffffff',
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=12,
            cursor='hand2',
            command=self.launch_ai_player
        )
        self.ai_btn.pack(side=tk.LEFT, padx=8)

        self.settings_btn = tk.Button(
            secondary_row,
            text=TRANSLATIONS[self.current_lang]['settings'],
            font=('Consolas', 13, 'bold'),
            bg='#9900ff',
            fg='#ffffff',
            activebackground=self.lighten_color('#9900ff'),
            activeforeground='#ffffff',
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=12,
            cursor='hand2',
            command=self.show_settings
        )
        self.settings_btn.pack(side=tk.LEFT, padx=8)

        # Effets hover pour les boutons secondaires
        def make_hover(button, original_color):
            def on_enter(e):
                button.config(bg=self.lighten_color(original_color))

            def on_leave(e):
                button.config(bg=original_color)

            return on_enter, on_leave

        for btn, color in [(self.multi_btn, '#0099ff'), (self.ai_btn, '#ff6600'), (self.settings_btn, '#9900ff')]:
            enter_func, leave_func = make_hover(btn, color)
            btn.bind('<Enter>', enter_func)
            btn.bind('<Leave>', leave_func)

        # Options de mode en bas
        options_frame = tk.Frame(main_frame, bg='#000000')
        options_frame.pack(pady=(30, 0))

        mode_label = tk.Label(
            options_frame,
            text="🎮  MODE DE JEU:",
            font=('Consolas', 10, 'bold'),
            fg='#00ffff',
            bg='#000000'
        )
        mode_label.pack()

        modes_row = tk.Frame(options_frame, bg='#000000')
        modes_row.pack(pady=10)

        # Radio buttons stylisés
        windowed_rb = tk.Radiobutton(
            modes_row,
            text="Fenêtré (800x600)",
            variable=self.mode_var,
            value="windowed",
            font=('Consolas', 10),
            fg='#ffffff',
            bg='#000000',
            activebackground='#000000',
            activeforeground='#00ff00',
            selectcolor='#000000',
            cursor='hand2'
        )
        windowed_rb.pack(side=tk.LEFT, padx=15)

        fullscreen_rb = tk.Radiobutton(
            modes_row,
            text="Plein écran",
            variable=self.mode_var,
            value="fullscreen",
            font=('Consolas', 10),
            fg='#ffffff',
            bg='#000000',
            activebackground='#000000',
            activeforeground='#00ff00',
            selectcolor='#000000',
            cursor='hand2'
        )
        fullscreen_rb.pack(side=tk.LEFT, padx=15)

        # Bouton pour voir les personnages
        view_chars_btn = tk.Button(
            main_frame,
            text="🎭  VOIR LES PERSONNAGES  🎭",
            font=('Consolas', 13, 'bold'),
            bg='#ff00ff',
            fg='#ffffff',
            activebackground='#ff66ff',
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=15,
            cursor='hand2',
            command=self.show_characters_view
        )
        view_chars_btn.pack(pady=(30, 0))

        # Stocker le main_frame pour pouvoir le cacher/afficher
        self.main_frame = main_frame

        # Barre de statut moderne en bas
        status_frame = tk.Frame(self.root, bg='#111111', height=40)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            text="⚡ READY TO FIGHT  •  All systems operational",
            font=('Consolas', 10, 'bold'),
            fg='#00ff88',
            bg='#111111',
            anchor=tk.W,
            padx=20
        )
        self.status_label.pack(fill=tk.X, expand=True)

    def lighten_color(self, color):
        """Éclaircit une couleur hex"""
        # Convertir hex en RGB
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

        # Éclaircir
        r = min(255, int(r * 1.3))
        g = min(255, int(g * 1.3))
        b = min(255, int(b * 1.3))

        return f'#{r:02x}{g:02x}{b:02x}'

    def change_language(self, lang):
        """Change la langue de l'interface"""
        self.current_lang = lang
        t = TRANSLATIONS[lang]

        # Mettre à jour tous les labels stockés
        self.subtitle_label.config(text=t['subtitle'])
        self.version_label.config(text=t['version'].format(VERSION))
        self.play_btn.config(text=t['play'])
        self.multi_btn.config(text=t['multiplayer'])
        self.ai_btn.config(text=t['ai_player'])
        self.settings_btn.config(text=t['settings'])

        # Mettre à jour les boutons de langue
        if lang == 'fr':
            self.lang_fr_btn.config(bg='#00ff00', fg='#000000')
            self.lang_en_btn.config(bg='#333333', fg='#888888')
        else:
            self.lang_en_btn.config(bg='#00ff00', fg='#000000')
            self.lang_fr_btn.config(bg='#333333', fg='#888888')

    def show_characters_view(self):
        """Affiche la vue des personnages avec scrolling"""
        if self.current_view == 'characters':
            return

        # Cacher le menu principal
        if self.main_frame:
            self.main_frame.place_forget()

        # Créer la vue personnages si elle n'existe pas
        if not self.chars_view_frame:
            self.chars_view_frame = tk.Frame(self.root, bg='#000000')

            # Titre
            title_label = tk.Label(
                self.chars_view_frame,
                text="🎭 PERSONNAGES DISPONIBLES 🎭",
                font=('Impact', 28, 'bold'),
                fg='#ff00ff',
                bg='#000000'
            )
            title_label.pack(pady=(20, 10))

            # Bouton Retour
            back_btn = tk.Button(
                self.chars_view_frame,
                text="◀  RETOUR AU MENU",
                font=('Consolas', 12, 'bold'),
                bg='#ff0000',
                fg='#ffffff',
                activebackground='#ff3333',
                relief=tk.FLAT,
                bd=0,
                padx=20,
                pady=10,
                cursor='hand2',
                command=self.show_main_view
            )
            back_btn.pack(pady=(0, 20))

            # Créer un canvas avec scrollbar
            canvas_frame = tk.Frame(self.chars_view_frame, bg='#000000')
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

            # Canvas
            canvas = tk.Canvas(
                canvas_frame,
                bg='#000000',
                highlightthickness=0,
                width=920,
                height=550
            )
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Scrollbar
            scrollbar = tk.Scrollbar(
                canvas_frame,
                orient=tk.VERTICAL,
                command=canvas.yview,
                bg='#333333',
                troughcolor='#111111',
                activebackground='#555555'
            )
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            canvas.configure(yscrollcommand=scrollbar.set)

            # Frame scrollable à l'intérieur du canvas
            scrollable_frame = tk.Frame(canvas, bg='#000000')
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

            # Grille de personnages (5 colonnes)
            for i, char_data in enumerate(CHARACTERS):
                row = i // 5
                col = i % 5

                # Frame pour chaque personnage
                char_card = tk.Frame(
                    scrollable_frame,
                    bg='#1a1a3e',
                    highlightbackground='#00ffff',
                    highlightthickness=2
                )
                char_card.grid(row=row, column=col, padx=8, pady=8)

                # Icône du personnage
                icon_label = tk.Label(
                    char_card,
                    text=char_data['icon'],
                    font=('Segoe UI Emoji', 32),
                    bg='#1a1a3e',
                    fg='#ffffff'
                )
                icon_label.pack(pady=(12, 4))

                # Nom du personnage
                name_label = tk.Label(
                    char_card,
                    text=char_data['name'],
                    font=('Consolas', 10, 'bold'),
                    bg='#1a1a3e',
                    fg='#ffffff',
                    width=15,
                    wraplength=140
                )
                name_label.pack(pady=(0, 4))

                # Étoiles
                stars = '⭐' * char_data['stars']
                stars_label = tk.Label(
                    char_card,
                    text=stars,
                    font=('Segoe UI Emoji', 10),
                    bg='#1a1a3e',
                    fg='#ffdd00'
                )
                stars_label.pack(pady=(0, 12))

            # Mettre à jour la région de scroll
            scrollable_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox('all'))

            # Bind mousewheel pour scrolling
            def on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")

            canvas.bind_all("<MouseWheel>", on_mousewheel)

            # Ajuster la largeur du frame scrollable
            def on_canvas_configure(event):
                canvas.itemconfig(canvas_window, width=event.width)

            canvas.bind('<Configure>', on_canvas_configure)

        # Afficher la vue personnages
        self.chars_view_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.current_view = 'characters'

    def show_main_view(self):
        """Retourne au menu principal"""
        if self.current_view == 'main':
            return

        # Cacher la vue personnages
        if self.chars_view_frame:
            self.chars_view_frame.place_forget()

        # Afficher le menu principal
        if self.main_frame:
            self.main_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.current_view = 'main'

    def toggle_fullscreen(self, event=None):
        """Bascule en mode plein écran (F11)"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)

        if self.is_fullscreen:
            self.update_status("Mode PLEIN ÉCRAN activé (Échap pour quitter)", '#00ff00')
        else:
            self.update_status("Mode fenêtré", '#00ffff')

    def exit_fullscreen(self, event=None):
        """Quitte le mode plein écran (Échap)"""
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes('-fullscreen', False)
            self.update_status("Mode fenêtré", '#00ffff')

    def update_status(self, message, color='#00ff88'):
        """Met à jour le statut"""
        self.status_label.config(text=f"⚡ {message}", fg=color)
        self.root.update()

    def auto_configure_gamepads(self):
        """Configure automatiquement les manettes"""
        self.update_status("Détection des manettes...", '#ffaa00')

        try:
            gamepad_script = GAME_PATH / "gamepad_auto_config.py"

            if gamepad_script.exists():
                result = subprocess.run(
                    [sys.executable, str(gamepad_script)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if "Manettes configurées:" in result.stdout:
                    self.update_status("✓ Manettes configurées automatiquement!", '#00ff00')
                    time.sleep(1)
                    return True

            return True

        except:
            return True

    def launch_game(self):
        """Lance le jeu"""
        self.update_status("Initialisation du système de combat...", '#ffff00')

        # Auto-configurer les manettes
        self.auto_configure_gamepads()

        # Configurer le mode
        mode = self.mode_var.get()
        if mode == "windowed":
            self.set_windowed_mode()
        else:
            self.set_fullscreen_mode()

        # Lancer le jeu
        exe_path = GAME_PATH / "KOF_Ultimate_Online.exe"

        if not exe_path.exists():
            messagebox.showerror(
                "Erreur",
                f"Fichier non trouvé:\n{exe_path}\n\nVérifiez l'installation du jeu."
            )
            self.update_status("ERROR: Game executable not found", '#ff0000')
            return

        try:
            self.update_status("🎮 LAUNCHING GAME...", '#00ff00')
            subprocess.Popen([str(exe_path)], cwd=str(GAME_PATH))

            time.sleep(1)
            self.root.iconify()

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer le jeu:\n{e}")
            self.update_status(f"ERROR: {e}", '#ff0000')

    def set_windowed_mode(self):
        """Configure le mode fenêtré"""
        config_file = GAME_PATH / "data" / "mugen.cfg"

        if not config_file.exists():
            return

        with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        modified = []
        for line in lines:
            if line.strip().startswith('FullScreen'):
                modified.append('FullScreen = 0\n')
            elif line.strip().startswith('Width') and any('Video' in l for l in modified[-15:]):
                modified.append('Width  = 800\n')
            elif line.strip().startswith('Height') and any('Video' in l for l in modified[-15:]):
                modified.append('Height = 600\n')
            else:
                modified.append(line)

        with open(config_file, 'w', encoding='utf-8') as f:
            f.writelines(modified)

    def set_fullscreen_mode(self):
        """Configure le mode plein écran"""
        config_file = GAME_PATH / "data" / "mugen.cfg"

        if not config_file.exists():
            return

        with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        modified = []
        for line in lines:
            if line.strip().startswith('FullScreen'):
                modified.append('FullScreen = 1\n')
            else:
                modified.append(line)

        with open(config_file, 'w', encoding='utf-8') as f:
            f.writelines(modified)

    def launch_multiplayer(self):
        """Lance le mode multijoueur"""
        self.update_status("Opening multiplayer menu...", '#0099ff')

        multi_script = GAME_PATH / "multiplayer_menu.py"

        if multi_script.exists():
            try:
                subprocess.Popen([sys.executable, str(multi_script)])
                self.update_status("✓ Multiplayer menu launched", '#00ff00')
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lancer le multijoueur:\n{e}")
                self.update_status(f"ERROR: {e}", '#ff0000')
        else:
            messagebox.showinfo(
                "Multijoueur",
                "Le mode multijoueur n'est pas encore configuré.\n\n"
                "Consultez GUIDE_MULTIJOUEUR.md pour plus d'informations."
            )
            self.update_status("Multiplayer not configured", '#ffaa00')

    def launch_ai_player(self):
        """Lance le système AI Player"""
        self.update_status("Initializing AI Player system...", '#ff6600')

        ai_script = GAME_PATH / "ai_player_system.py"

        if ai_script.exists():
            try:
                subprocess.Popen(
                    [sys.executable, str(ai_script)],
                    cwd=str(GAME_PATH),
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
                self.update_status("✓ AI Player launched", '#00ff00')

                messagebox.showinfo(
                    "AI Player",
                    "Le système AI Player est maintenant actif!\n\n"
                    "Il va jouer automatiquement et apprendre.\n"
                    "Consultez la console pour voir son activité."
                )

            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lancer AI Player:\n{e}")
                self.update_status(f"ERROR: {e}", '#ff0000')
        else:
            messagebox.showinfo(
                "AI Player",
                "Le système AI Player n'est pas configuré.\n\n"
                "Consultez README_AI_PLAYER.md pour l'installation."
            )
            self.update_status("AI Player not configured", '#ffaa00')

    def show_settings(self):
        """Affiche le menu des paramètres"""
        self.update_status("Opening settings...", '#9900ff')

        settings_win = tk.Toplevel(self.root)
        settings_win.title("⚙️  KOF Ultimate - Settings")
        settings_win.geometry("600x400")
        settings_win.configure(bg='#1a1a2e')
        settings_win.transient(self.root)
        settings_win.grab_set()

        # Centrer la fenêtre
        settings_win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (600 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (400 // 2)
        settings_win.geometry(f'600x400+{x}+{y}')

        # Contenu
        title = tk.Label(
            settings_win,
            text="⚙️  SETTINGS",
            font=('Impact', 24, 'bold'),
            fg='#ffffff',
            bg='#1a1a2e'
        )
        title.pack(pady=30)

        # Options
        options = [
            ("🎮 Configure Gamepads", self.configure_gamepads_manual),
            ("🛠️ Dev Mode", self.launch_dev_mode),
            ("⚖️ Character Balancer", self.launch_balancer),
            ("📖 Open Guide", self.open_guide),
            ("🔄 Check for Updates", self.check_updates),
        ]

        for text, command in options:
            btn = tk.Button(
                settings_win,
                text=text,
                font=('Consolas', 12, 'bold'),
                bg='#2d3561',
                fg='#ffffff',
                activebackground='#3d4571',
                relief=tk.FLAT,
                bd=0,
                padx=30,
                pady=12,
                cursor='hand2',
                command=command
            )
            btn.pack(pady=8, padx=50, fill=tk.X)

        close_btn = tk.Button(
            settings_win,
            text="CLOSE",
            font=('Consolas', 11, 'bold'),
            bg='#666666',
            fg='#ffffff',
            activebackground='#888888',
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            command=settings_win.destroy
        )
        close_btn.pack(side=tk.BOTTOM, pady=20)

    def configure_gamepads_manual(self):
        """Lance la configuration manuelle des manettes"""
        script = GAME_PATH / "gamepad_auto_config.py"
        if script.exists():
            subprocess.Popen([sys.executable, str(script)])

    def launch_dev_mode(self):
        """Lance le mode développement"""
        script = GAME_PATH / "dev_live_window.py"
        if script.exists():
            subprocess.Popen([sys.executable, str(script)])

    def launch_balancer(self):
        """Lance l'équilibreur de personnages"""
        script = GAME_PATH / "character_balancer.py"
        if script.exists():
            subprocess.Popen([sys.executable, str(script)])

    def open_guide(self):
        """Ouvre le guide"""
        guide = GAME_PATH / "GUIDE_MULTIJOUEUR.md"
        if guide.exists():
            os.startfile(str(guide))

    def check_updates(self):
        """Vérifie les mises à jour"""
        messagebox.showinfo(
            "Updates",
            f"Version actuelle: {VERSION}\n\n"
            "Vous utilisez la dernière version!"
        )

    def run(self):
        """Lance le launcher"""
        self.root.mainloop()

    def on_closing(self):
        """Gérer la fermeture"""
        self.animation_running = False
        self.root.destroy()

if __name__ == "__main__":
    # Auto-installer les dépendances si nécessaire
    try:
        from PIL import Image
    except ImportError:
        print("Installing Pillow...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pillow"])
        print("Please restart the launcher")
        input("Press Enter...")
        sys.exit(0)

    launcher = ModernLauncher()
    launcher.root.protocol("WM_DELETE_WINDOW", launcher.on_closing)
    launcher.run()
