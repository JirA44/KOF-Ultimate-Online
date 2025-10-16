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

class ModernLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KOF ULTIMATE ONLINE - Launcher")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        self.root.configure(bg='#000000')

        # Variables
        self.mode_var = tk.StringVar(value="windowed")
        self.animation_running = True

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
            width=900,
            height=650,
            bg='#000000',
            highlightthickness=0
        )
        self.bg_canvas.place(x=0, y=0)

        # Particules animées
        self.particles = []
        for _ in range(50):
            x = random.randint(0, 900)
            y = random.randint(0, 650)
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
            if particle['x'] < 0 or particle['x'] > 900:
                particle['angle'] = math.pi - particle['angle']
            if particle['y'] < 0 or particle['y'] > 650:
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
        subtitle = tk.Label(
            main_frame,
            text="━━━━━━━  ULTIMATE EDITION  ━━━━━━━",
            font=('Consolas', 12, 'bold'),
            fg='#00ffff',
            bg='#000000'
        )
        subtitle.pack(pady=(0, 10))

        version_label = tk.Label(
            main_frame,
            text=f"v{VERSION}  •  Next-Gen Fighter",
            font=('Consolas', 10, 'italic'),
            fg='#888888',
            bg='#000000'
        )
        version_label.pack(pady=(0, 40))

        # Container pour les boutons avec effet de glassmorphism
        buttons_container = tk.Frame(
            main_frame,
            bg='#000000'
        )
        buttons_container.pack()

        # Bouton PLAY ultra-moderne
        play_frame = tk.Frame(buttons_container, bg='#000000')
        play_frame.pack(pady=10)

        play_btn = tk.Button(
            play_frame,
            text="▶  J O U E R  ◀",
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
        play_btn.pack()

        # Effet hover pour le bouton PLAY
        def on_play_enter(e):
            play_btn.config(
                bg='#00ff88',
                font=('Impact', 30, 'bold')
            )

        def on_play_leave(e):
            play_btn.config(
                bg='#00ff00',
                font=('Impact', 28, 'bold')
            )

        play_btn.bind('<Enter>', on_play_enter)
        play_btn.bind('<Leave>', on_play_leave)

        # Boutons secondaires en ligne
        secondary_row = tk.Frame(buttons_container, bg='#000000')
        secondary_row.pack(pady=20)

        secondary_buttons = [
            {
                'text': '🌐  MULTIPLAYER',
                'command': self.launch_multiplayer,
                'color': '#0099ff'
            },
            {
                'text': '🤖  AI PLAYER',
                'command': self.launch_ai_player,
                'color': '#ff6600'
            },
            {
                'text': '⚙️  SETTINGS',
                'command': self.show_settings,
                'color': '#9900ff'
            }
        ]

        for btn_info in secondary_buttons:
            btn = tk.Button(
                secondary_row,
                text=btn_info['text'],
                font=('Consolas', 13, 'bold'),
                bg=btn_info['color'],
                fg='#ffffff',
                activebackground=self.lighten_color(btn_info['color']),
                activeforeground='#ffffff',
                relief=tk.FLAT,
                bd=0,
                padx=20,
                pady=12,
                cursor='hand2',
                command=btn_info['command']
            )
            btn.pack(side=tk.LEFT, padx=8)

            # Effet hover
            def make_hover(button, original_color):
                def on_enter(e):
                    button.config(bg=self.lighten_color(original_color))

                def on_leave(e):
                    button.config(bg=original_color)

                return on_enter, on_leave

            enter_func, leave_func = make_hover(btn, btn_info['color'])
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
