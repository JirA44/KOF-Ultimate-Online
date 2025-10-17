"""
KOF Ultimate - Launcher Officiel
Version 1.0.0

Fonctionnalités:
- Auto-update
- Gestion des versions
- Modes de lancement (Fenêtré/Plein écran)
- Vérification des fichiers
- Multijoueur
- Auto-installation des dépendances
"""
import os
import sys
import json
import subprocess
import hashlib
import urllib.request
import zipfile
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import webbrowser

# Auto-installer les dépendances manquantes
def check_and_install_dependencies():
    """Vérifie et installe automatiquement les dépendances manquantes"""
    required_packages = {
        'pillow': 'PIL',
        'anthropic': 'anthropic',
        'pyautogui': 'pyautogui',
        'opencv-python': 'cv2',
        'numpy': 'numpy',
        'keyboard': 'keyboard',
        'mouse': 'mouse',
        'python-dotenv': 'dotenv',
        'requests': 'requests'
    }

    missing = []
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"Installing missing packages: {', '.join(missing)}")
        for package in missing:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])
                print(f"✓ Installed {package}")
            except Exception as e:
                print(f"✗ Failed to install {package}: {e}")

        if missing:
            print("Some dependencies were installed. Please restart the launcher.")
            return False

    return True

# Vérifier les dépendances au démarrage
if __name__ == "__main__":
    if not check_and_install_dependencies():
        input("Press Enter to exit...")
        sys.exit(0)

# Configuration
VERSION = "1.0.0"
UPDATE_URL = "https://raw.githubusercontent.com/votre-repo/kof-ultimate/main/version.json"
GAME_PATH = Path(__file__).parent

class UpdateChecker:
    """Vérifie et applique les mises à jour"""

    def __init__(self, current_version):
        self.current_version = current_version
        self.update_available = False
        self.latest_version = None
        self.download_url = None

    def check_for_updates(self):
        """Vérifie si une mise à jour est disponible"""
        try:
            # Télécharger les informations de version
            response = urllib.request.urlopen(UPDATE_URL, timeout=5)
            data = json.loads(response.read().decode('utf-8'))

            self.latest_version = data.get('version')
            self.download_url = data.get('download_url')
            changelog = data.get('changelog', [])

            # Comparer les versions
            if self.latest_version and self._compare_versions(self.latest_version, self.current_version) > 0:
                self.update_available = True
                return {
                    'available': True,
                    'version': self.latest_version,
                    'changelog': changelog,
                    'url': self.download_url
                }

            return {'available': False}

        except Exception as e:
            print(f"Erreur vérification update: {e}")
            return {'available': False, 'error': str(e)}

    def _compare_versions(self, v1, v2):
        """Compare deux versions (format: X.Y.Z)"""
        v1_parts = [int(x) for x in v1.split('.')]
        v2_parts = [int(x) for x in v2.split('.')]

        for i in range(max(len(v1_parts), len(v2_parts))):
            p1 = v1_parts[i] if i < len(v1_parts) else 0
            p2 = v2_parts[i] if i < len(v2_parts) else 0

            if p1 > p2:
                return 1
            elif p1 < p2:
                return -1

        return 0

    def download_update(self, progress_callback=None):
        """Télécharge et installe la mise à jour"""
        if not self.download_url:
            return False

        try:
            # Créer dossier temporaire
            temp_dir = GAME_PATH / "temp_update"
            temp_dir.mkdir(exist_ok=True)

            zip_path = temp_dir / "update.zip"

            # Télécharger
            def report_progress(block_num, block_size, total_size):
                downloaded = block_num * block_size
                percent = min(100, (downloaded / total_size) * 100)
                if progress_callback:
                    progress_callback(percent)

            urllib.request.urlretrieve(
                self.download_url,
                str(zip_path),
                reporthook=report_progress
            )

            # Extraire
            if progress_callback:
                progress_callback(100, "Extraction...")

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Copier les fichiers
            if progress_callback:
                progress_callback(100, "Installation...")

            for item in temp_dir.iterdir():
                if item.name != 'update.zip':
                    if item.is_dir():
                        shutil.copytree(item, GAME_PATH / item.name, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, GAME_PATH / item.name)

            # Nettoyer
            shutil.rmtree(temp_dir)

            # Mettre à jour le fichier de version locale
            version_file = GAME_PATH / "version.json"
            with open(version_file, 'w') as f:
                json.dump({'version': self.latest_version}, f)

            return True

        except Exception as e:
            print(f"Erreur téléchargement: {e}")
            return False

class GameLauncher:
    """Interface principale du launcher"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"KOF Ultimate Launcher v{VERSION}")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # Centrer la fenêtre
        self.center_window()

        # Variables
        self.mode_var = tk.StringVar(value="windowed")
        self.updater = UpdateChecker(VERSION)

        # UI
        self.setup_ui()

        # Vérifier les updates au démarrage
        self.check_updates_async()

    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Style personnalisé
        self.root.configure(bg='#0a0e27')

        # Header avec dégradé visuel
        header_frame = tk.Frame(self.root, bg='#1a1f3a', height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Titre principal avec effet
        title_label = tk.Label(
            header_frame,
            text="⚡ KOF ULTIMATE ⚡",
            font=('Consolas', 32, 'bold'),
            fg='#FFD700',
            bg='#1a1f3a'
        )
        title_label.pack(pady=(25, 5))

        # Sous-titre stylisé
        subtitle_label = tk.Label(
            header_frame,
            text="━━━━━ THE ULTIMATE FIGHTING EXPERIENCE ━━━━━",
            font=('Consolas', 8),
            fg='#4a9eff',
            bg='#1a1f3a'
        )
        subtitle_label.pack(pady=(0, 5))

        version_label = tk.Label(
            header_frame,
            text=f"v{VERSION}",
            font=('Consolas', 9, 'italic'),
            fg='#888',
            bg='#1a1f3a'
        )
        version_label.pack()

        # Main content avec nouveau style
        content_frame = tk.Frame(self.root, bg='#0d1b2a', padx=40, pady=25)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Mode de lancement avec nouveau style
        mode_frame = tk.LabelFrame(
            content_frame,
            text=" 🎮  MODE DE LANCEMENT  🎮 ",
            font=('Consolas', 11, 'bold'),
            bg='#1b263b',
            fg='#00d9ff',
            padx=15,
            pady=12,
            relief=tk.RIDGE,
            bd=2
        )
        mode_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Radiobutton(
            mode_frame,
            text="Fenêtré (800x600) - Recommandé pour développement",
            variable=self.mode_var,
            value="windowed"
        ).pack(anchor=tk.W, pady=2)

        ttk.Radiobutton(
            mode_frame,
            text="Plein écran - Mode de jeu normal",
            variable=self.mode_var,
            value="fullscreen"
        ).pack(anchor=tk.W, pady=2)

        # Boutons principaux
        buttons_frame = tk.Frame(content_frame, bg='#0d1b2a')
        buttons_frame.pack(fill=tk.X, pady=10)

        # Bouton Jouer avec effet amélioré
        play_btn = tk.Button(
            buttons_frame,
            text="▶▶▶  JOUER  ◀◀◀",
            font=('Consolas', 18, 'bold'),
            bg='#00cc44',
            fg='#000000',
            activebackground='#00ff55',
            activeforeground='#000000',
            relief=tk.RAISED,
            bd=4,
            cursor='hand2',
            padx=20,
            pady=12,
            command=self.launch_game
        )
        play_btn.pack(fill=tk.X, pady=8)

        # Effets de survol pour le bouton JOUER
        def on_play_enter(e):
            play_btn.config(bg='#00ff55', relief=tk.RIDGE, bd=5)
        def on_play_leave(e):
            play_btn.config(bg='#00cc44', relief=tk.RAISED, bd=4)
        play_btn.bind('<Enter>', on_play_enter)
        play_btn.bind('<Leave>', on_play_leave)

        # Bouton Multijoueur amélioré
        multi_btn = tk.Button(
            buttons_frame,
            text="🌐  MULTIJOUEUR ONLINE  🌐",
            font=('Consolas', 14, 'bold'),
            bg='#0066cc',
            fg='#ffffff',
            activebackground='#0088ff',
            activeforeground='#ffffff',
            relief=tk.RAISED,
            bd=3,
            cursor='hand2',
            padx=15,
            pady=10,
            command=self.launch_multiplayer
        )
        multi_btn.pack(fill=tk.X, pady=6)

        # Effets de survol pour MULTIJOUEUR
        def on_multi_enter(e):
            multi_btn.config(bg='#0088ff', relief=tk.RIDGE)
        def on_multi_leave(e):
            multi_btn.config(bg='#0066cc', relief=tk.RAISED)
        multi_btn.bind('<Enter>', on_multi_enter)
        multi_btn.bind('<Leave>', on_multi_leave)

        # Bouton AI Player amélioré
        ai_btn = tk.Button(
            buttons_frame,
            text="🤖  AI PLAYER  •  Auto-Play & Test",
            font=('Consolas', 13, 'bold'),
            bg='#cc3300',
            fg='#ffff00',
            activebackground='#ff4400',
            activeforeground='#ffff00',
            relief=tk.RAISED,
            bd=3,
            cursor='hand2',
            padx=15,
            pady=10,
            command=self.launch_ai_player
        )
        ai_btn.pack(fill=tk.X, pady=6)

        # Effets de survol pour AI PLAYER
        def on_ai_enter(e):
            ai_btn.config(bg='#ff4400', relief=tk.RIDGE)
        def on_ai_leave(e):
            ai_btn.config(bg='#cc3300', relief=tk.RAISED)
        ai_btn.bind('<Enter>', on_ai_enter)
        ai_btn.bind('<Leave>', on_ai_leave)

        # Boutons secondaires (2 colonnes) améliorés
        secondary_frame = tk.Frame(buttons_frame, bg='#0d1b2a')
        secondary_frame.pack(fill=tk.X, pady=10)

        # Colonne gauche
        left_col = tk.Frame(secondary_frame, bg='#0d1b2a')
        left_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        dev_btn = tk.Button(
            left_col,
            text="🛠  Mode Dev",
            font=('Consolas', 10, 'bold'),
            bg='#2d3561',
            fg='#c0c0c0',
            activebackground='#3d4571',
            cursor='hand2',
            relief=tk.RAISED,
            bd=2,
            pady=8,
            command=self.launch_dev_mode
        )
        dev_btn.pack(fill=tk.X, pady=3)
        dev_btn.bind('<Enter>', lambda e: dev_btn.config(bg='#3d4571', fg='#ffffff'))
        dev_btn.bind('<Leave>', lambda e: dev_btn.config(bg='#2d3561', fg='#c0c0c0'))

        balance_btn = tk.Button(
            left_col,
            text="⚖  Équilibrage",
            font=('Consolas', 10, 'bold'),
            bg='#2d3561',
            fg='#c0c0c0',
            activebackground='#3d4571',
            cursor='hand2',
            relief=tk.RAISED,
            bd=2,
            pady=8,
            command=self.launch_balancer
        )
        balance_btn.pack(fill=tk.X, pady=3)
        balance_btn.bind('<Enter>', lambda e: balance_btn.config(bg='#3d4571', fg='#ffffff'))
        balance_btn.bind('<Leave>', lambda e: balance_btn.config(bg='#2d3561', fg='#c0c0c0'))

        chars_btn = tk.Button(
            left_col,
            text="👤  Personnages",
            font=('Consolas', 10, 'bold'),
            bg='#2d3561',
            fg='#c0c0c0',
            activebackground='#3d4571',
            cursor='hand2',
            relief=tk.RAISED,
            bd=2,
            pady=8,
            command=self.launch_character_dashboard
        )
        chars_btn.pack(fill=tk.X, pady=3)
        chars_btn.bind('<Enter>', lambda e: chars_btn.config(bg='#3d4571', fg='#ffffff'))
        chars_btn.bind('<Leave>', lambda e: chars_btn.config(bg='#2d3561', fg='#c0c0c0'))

        # Colonne droite
        right_col = tk.Frame(secondary_frame, bg='#0d1b2a')
        right_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0))

        guide_btn = tk.Button(
            right_col,
            text="📖  Guide",
            font=('Consolas', 10, 'bold'),
            bg='#2d3561',
            fg='#c0c0c0',
            activebackground='#3d4571',
            cursor='hand2',
            relief=tk.RAISED,
            bd=2,
            pady=8,
            command=self.open_guide
        )
        guide_btn.pack(fill=tk.X, pady=3)
        guide_btn.bind('<Enter>', lambda e: guide_btn.config(bg='#3d4571', fg='#ffffff'))
        guide_btn.bind('<Leave>', lambda e: guide_btn.config(bg='#2d3561', fg='#c0c0c0'))

        update_btn = tk.Button(
            right_col,
            text="🔄  Vérifier MAJ",
            font=('Consolas', 10, 'bold'),
            bg='#2d3561',
            fg='#c0c0c0',
            activebackground='#3d4571',
            cursor='hand2',
            relief=tk.RAISED,
            bd=2,
            pady=8,
            command=self.check_updates_async
        )
        update_btn.pack(fill=tk.X, pady=3)
        update_btn.bind('<Enter>', lambda e: update_btn.config(bg='#3d4571', fg='#ffffff'))
        update_btn.bind('<Leave>', lambda e: update_btn.config(bg='#2d3561', fg='#c0c0c0'))

        inspector_btn = tk.Button(
            right_col,
            text="🔍  Inspecteur Visuel",
            font=('Consolas', 10, 'bold'),
            bg='#2d3561',
            fg='#c0c0c0',
            activebackground='#3d4571',
            cursor='hand2',
            relief=tk.RAISED,
            bd=2,
            pady=8,
            command=self.launch_visual_inspector
        )
        inspector_btn.pack(fill=tk.X, pady=3)
        inspector_btn.bind('<Enter>', lambda e: inspector_btn.config(bg='#3d4571', fg='#ffffff'))
        inspector_btn.bind('<Leave>', lambda e: inspector_btn.config(bg='#2d3561', fg='#c0c0c0'))

        # Status bar améliorée
        self.status_bar = tk.Label(
            self.root,
            text="⚡ Prêt  •  Ready to fight!",
            font=('Consolas', 10, 'bold'),
            bg='#1a1f3a',
            fg='#00ff88',
            anchor=tk.W,
            padx=15,
            pady=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Progress bar (cachée par défaut)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.root,
            variable=self.progress_var,
            maximum=100
        )

    def update_status(self, message):
        """Met à jour la barre de statut"""
        self.status_bar.config(text=message)
        self.root.update()

    def auto_configure_gamepads(self):
        """Détecte et configure automatiquement les manettes"""
        self.update_status("Détection des manettes...")

        try:
            # Lancer la configuration automatique
            gamepad_script = GAME_PATH / "gamepad_auto_config.py"

            if gamepad_script.exists():
                # Lancer en mode silencieux
                result = subprocess.run(
                    [sys.executable, str(gamepad_script)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if "Manettes configurées:" in result.stdout:
                    self.update_status("✓ Manettes configurées automatiquement")
                    return True
                elif "Aucune manette" in result.stdout:
                    self.update_status("Info: Aucune manette détectée")
                    return True

            return True

        except Exception as e:
            print(f"Gamepad config error: {e}")
            # Ne pas bloquer le lancement même si la config échoue
            return True

    def launch_game(self):
        """Lance le jeu"""
        self.update_status("Préparation du lancement...")

        # Auto-configurer les manettes AVANT de lancer le jeu
        self.auto_configure_gamepads()

        self.update_status("Lancement du jeu...")

        # Déterminer le mode
        mode = self.mode_var.get()

        # Modifier la config si nécessaire
        if mode == "windowed":
            self.set_windowed_mode()
        else:
            self.set_fullscreen_mode()

        # Lancer le jeu
        exe_path = GAME_PATH / "KOF_Ultimate_Online.exe"

        if not exe_path.exists():
            messagebox.showerror(
                "Erreur",
                f"Executable non trouvé:\n{exe_path}\n\nAssurez-vous que le jeu est correctement installé."
            )
            self.update_status("Erreur: Executable non trouvé")
            return

        try:
            subprocess.Popen([str(exe_path)], cwd=str(GAME_PATH))
            self.update_status("✓ Jeu lancé")

            # Minimiser le launcher
            self.root.iconify()

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer le jeu:\n{e}")
            self.update_status(f"Erreur: {e}")

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
            elif line.strip().startswith('Width') and any('Video' in l for l in modified[-15:]):
                modified.append('Width  = 640\n')
            elif line.strip().startswith('Height') and any('Video' in l for l in modified[-15:]):
                modified.append('Height = 480\n')
            else:
                modified.append(line)

        with open(config_file, 'w', encoding='utf-8') as f:
            f.writelines(modified)

    def launch_multiplayer(self):
        """Lance le menu multijoueur amélioré"""
        self.update_status("Ouverture du menu multijoueur...")

        # Lancer le nouveau menu multijoueur
        multi_script = GAME_PATH / "multiplayer_menu.py"

        if multi_script.exists():
            try:
                subprocess.Popen([sys.executable, str(multi_script)])
                self.update_status("✓ Menu multijoueur lancé")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lancer le menu multijoueur:\n{e}")
                self.update_status(f"Erreur: {e}")
        else:
            # Fallback vers l'ancienne méthode
            self.launch_multiplayer_legacy()

    def launch_multiplayer_legacy(self):
        """Lance le mode multijoueur (ancienne méthode)"""
        # Vérifier si Ikemen GO est installé
        ikemen_path = Path("D:/KOF Ultimate Online/Ikemen_GO.exe")

        if ikemen_path.exists():
            try:
                subprocess.Popen([str(ikemen_path)], cwd=str(ikemen_path.parent))
                self.update_status("✓ Mode multijoueur lancé")
                self.root.iconify()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lancement multijoueur:\n{e}")
        else:
            # Proposer l'installation
            response = messagebox.askyesno(
                "Multijoueur non installé",
                "Le mode multijoueur nécessite Ikemen GO.\n\n"
                "Voulez-vous l'installer maintenant?\n"
                "(Cela prendra quelques minutes)"
            )

            if response:
                self.install_ikemen_go()
            else:
                self.update_status("Installation annulée")

    def install_ikemen_go(self):
        """Guide d'installation d'Ikemen GO"""
        info = """
Installation d'Ikemen GO:

1. Le téléchargement va démarrer dans votre navigateur
2. Extrayez le fichier dans: D:\\KOF Ultimate Online\\
3. Relancez ce launcher et cliquez sur "MULTIJOUEUR"

Le guide complet est disponible dans GUIDE_MULTIJOUEUR.md
        """

        messagebox.showinfo("Installation Ikemen GO", info)
        webbrowser.open("https://github.com/ikemen-engine/Ikemen-GO/releases/latest")
        self.update_status("Guide d'installation affiché")

    def launch_dev_mode(self):
        """Lance la fenêtre de développement"""
        self.update_status("Ouverture du mode développement...")

        dev_script = GAME_PATH / "dev_live_window.py"

        if dev_script.exists():
            try:
                subprocess.Popen([sys.executable, str(dev_script)])
                self.update_status("✓ Mode dev lancé")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lancer le mode dev:\n{e}")
        else:
            messagebox.showerror(
                "Erreur",
                f"Script non trouvé:\n{dev_script}"
            )
            self.update_status("Erreur: Script dev non trouvé")

    def launch_balancer(self):
        """Lance l'outil d'équilibrage"""
        self.update_status("Ouverture de l'équilibreur...")

        balance_script = GAME_PATH / "character_balancer.py"

        if balance_script.exists():
            try:
                subprocess.Popen([sys.executable, str(balance_script)])
                self.update_status("✓ Équilibreur lancé")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lancer l'équilibreur:\n{e}")
        else:
            messagebox.showerror(
                "Erreur",
                f"Script non trouvé:\n{balance_script}"
            )
            self.update_status("Erreur: Script balancer non trouvé")

    def launch_character_dashboard(self):
        """Lance le dashboard des personnages"""
        self.update_status("Ouverture du dashboard personnages...")

        dashboard_script = GAME_PATH / "character_dashboard.py"

        if dashboard_script.exists():
            try:
                subprocess.Popen([sys.executable, str(dashboard_script)])
                self.update_status("✓ Dashboard personnages lancé")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lancer le dashboard:\n{e}")
        else:
            messagebox.showerror(
                "Erreur",
                f"Script non trouvé:\n{dashboard_script}"
            )
            self.update_status("Erreur: Script dashboard non trouvé")

    def launch_visual_inspector(self):
        """Lance l'inspecteur visuel"""
        self.update_status("Ouverture de l'inspecteur visuel...")

        inspector_script = GAME_PATH / "visual_inspector.py"

        if inspector_script.exists():
            try:
                subprocess.Popen([sys.executable, str(inspector_script)])
                self.update_status("✓ Inspecteur visuel lancé")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lancer l'inspecteur:\n{e}")
        else:
            messagebox.showerror(
                "Erreur",
                f"Script non trouvé:\n{inspector_script}"
            )
            self.update_status("Erreur: Script inspecteur non trouvé")

    def open_guide(self):
        """Ouvre le guide multijoueur"""
        guide_file = GAME_PATH / "GUIDE_MULTIJOUEUR.md"

        if guide_file.exists():
            try:
                os.startfile(str(guide_file))
                self.update_status("✓ Guide ouvert")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ouvrir le guide:\n{e}")
        else:
            messagebox.showerror("Erreur", "Guide non trouvé")

    def launch_ai_player(self):
        """Lance le système de joueur IA"""
        self.update_status("Lancement du système AI Player...")

        ai_script = GAME_PATH / "ai_player_system.py"

        if not ai_script.exists():
            response = messagebox.askyesno(
                "AI Player non configuré",
                "Le système AI Player nécessite:\n"
                "• Python avec les dépendances installées\n"
                "• Une clé API Anthropic\n\n"
                "Voulez-vous voir le guide d'installation?"
            )
            if response:
                messagebox.showinfo(
                    "Installation AI Player",
                    "1. Installez les dépendances:\n"
                    "   pip install -r requirements_ai.txt\n\n"
                    "2. Configurez votre clé API Anthropic:\n"
                    "   set ANTHROPIC_API_KEY=votre_clé\n\n"
                    "3. Relancez ce launcher et cliquez sur 'AI PLAYER'"
                )
            self.update_status("AI Player non configuré")
            return

        # Vérifier les dépendances
        try:
            import pyautogui
            import anthropic
        except ImportError:
            response = messagebox.askyesno(
                "Dépendances manquantes",
                "Certaines dépendances Python sont manquantes.\n\n"
                "Voulez-vous les installer maintenant?\n"
                "(Cela peut prendre quelques minutes)"
            )
            if response:
                self.install_ai_dependencies()
            else:
                self.update_status("Installation annulée")
            return

        # Lancer le système IA
        try:
            subprocess.Popen(
                [sys.executable, str(ai_script)],
                cwd=str(GAME_PATH),
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            self.update_status("✓ AI Player lancé")

            messagebox.showinfo(
                "AI Player démarré",
                "Le système AI Player est maintenant actif!\n\n"
                "Il va:\n"
                "• Explorer automatiquement les menus\n"
                "• Jouer des matchs en autonome\n"
                "• Apprendre et s'améliorer\n"
                "• Détecter les bugs\n\n"
                "Consultez la console pour voir son activité."
            )

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer AI Player:\n{e}")
            self.update_status(f"Erreur: {e}")

    def install_ai_dependencies(self):
        """Installe les dépendances pour AI Player"""
        requirements_file = GAME_PATH / "requirements_ai.txt"

        if not requirements_file.exists():
            messagebox.showerror(
                "Erreur",
                f"Fichier requirements_ai.txt introuvable:\n{requirements_file}"
            )
            return

        self.update_status("Installation des dépendances AI...")

        # Afficher la barre de progression
        self.progress_bar.pack(before=self.status_bar, fill=tk.X)
        self.progress_var.set(0)

        def install():
            try:
                # Installer les dépendances
                process = subprocess.Popen(
                    [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )

                for line in process.stdout:
                    print(line.strip())
                    self.progress_var.set((self.progress_var.get() + 10) % 100)
                    self.root.update()

                process.wait()

                if process.returncode == 0:
                    self.root.after(0, lambda: self.handle_ai_install_complete(True))
                else:
                    self.root.after(0, lambda: self.handle_ai_install_complete(False))

            except Exception as e:
                print(f"Installation error: {e}")
                self.root.after(0, lambda: self.handle_ai_install_complete(False))

        Thread(target=install, daemon=True).start()

    def handle_ai_install_complete(self, success):
        """Traite la fin de l'installation AI"""
        self.progress_bar.pack_forget()

        if success:
            messagebox.showinfo(
                "Installation réussie",
                "Les dépendances AI Player ont été installées!\n\n"
                "Vous pouvez maintenant lancer le système AI Player."
            )
            self.update_status("✓ Dépendances AI installées")
        else:
            messagebox.showerror(
                "Erreur d'installation",
                "L'installation des dépendances a échoué.\n\n"
                "Essayez manuellement:\n"
                "pip install -r requirements_ai.txt"
            )
            self.update_status("Erreur installation AI")

    def check_updates_async(self):
        """Vérifie les mises à jour dans un thread séparé"""
        self.update_status("Vérification des mises à jour...")

        def check():
            result = self.updater.check_for_updates()

            # Revenir au thread principal
            self.root.after(0, lambda: self.handle_update_result(result))

        Thread(target=check, daemon=True).start()

    def handle_update_result(self, result):
        """Traite le résultat de la vérification de mise à jour"""
        if result.get('error'):
            self.update_status("Vérification des MAJ impossible (hors ligne?)")
            return

        if result['available']:
            version = result['version']
            changelog = '\n'.join(result.get('changelog', []))

            response = messagebox.askyesno(
                "Mise à jour disponible!",
                f"Version {version} disponible!\n"
                f"Votre version: {VERSION}\n\n"
                f"Nouveautés:\n{changelog}\n\n"
                f"Installer maintenant?"
            )

            if response:
                self.download_update()
            else:
                self.update_status(f"MAJ {version} disponible (ignorée)")
        else:
            self.update_status(f"✓ À jour (v{VERSION})")
            messagebox.showinfo("À jour", f"Vous utilisez la dernière version ({VERSION})")

    def download_update(self):
        """Télécharge et installe la mise à jour"""
        # Afficher la barre de progression
        self.progress_bar.pack(before=self.status_bar, fill=tk.X)
        self.update_status("Téléchargement de la mise à jour...")

        def progress_callback(percent, message=""):
            self.progress_var.set(percent)
            if message:
                self.update_status(message)
            self.root.update()

        def download():
            success = self.updater.download_update(progress_callback)

            # Revenir au thread principal
            self.root.after(0, lambda: self.handle_update_complete(success))

        Thread(target=download, daemon=True).start()

    def handle_update_complete(self, success):
        """Traite la fin du téléchargement"""
        self.progress_bar.pack_forget()

        if success:
            messagebox.showinfo(
                "Mise à jour réussie!",
                f"KOF Ultimate a été mis à jour vers la version {self.updater.latest_version}.\n\n"
                "Le launcher va redémarrer."
            )

            # Redémarrer le launcher
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            messagebox.showerror(
                "Erreur",
                "La mise à jour a échoué.\n"
                "Réessayez plus tard ou téléchargez manuellement."
            )
            self.update_status("Erreur lors de la mise à jour")

    def run(self):
        """Lance le launcher"""
        self.root.mainloop()

if __name__ == "__main__":
    app = GameLauncher()
    app.run()
