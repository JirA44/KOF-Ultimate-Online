"""
KOF Ultimate - Menu Multijoueur Avancé
Menu moderne et complet pour le mode multijoueur
"""
import os
import sys
import json
import socket
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from threading import Thread
import webbrowser

# Configuration
GAME_PATH = Path(r"D:\KOF Ultimate Online Online Online")
IKEMEN_PATH = Path(r"D:\KOF Ultimate Online Online Online")
CONFIG_FILE = GAME_PATH / "multiplayer_config.json"

class MultiplayerConfig:
    """Gestion de la configuration multijoueur"""

    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        """Charge la configuration"""
        default_config = {
            "last_player_name": "Player1",
            "last_ip": "localhost",
            "last_port": 7500,
            "auto_save": True,
            "enable_chat": True,
            "favorite_characters": [],
            "network_quality": "high"
        }

        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
            except Exception as e:
                print(f"Error loading config: {e}")

        return default_config

    def save_config(self):
        """Sauvegarde la configuration"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        if self.config.get("auto_save", True):
            self.save_config()


class MultiplayerMenu:
    """Menu multijoueur principal"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KOF Ultimate - Multiplayer Menu")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        self.config = MultiplayerConfig()
        self.ikemen_installed = self.check_ikemen()

        # Variables
        self.mode_var = tk.StringVar(value="local")
        self.player_name_var = tk.StringVar(value=self.config.get("last_player_name"))
        self.ip_var = tk.StringVar(value=self.config.get("last_ip"))
        self.port_var = tk.IntVar(value=self.config.get("last_port"))

        self.setup_ui()
        self.center_window()

    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def check_ikemen(self):
        """Vérifie si Ikemen GO est installé"""
        ikemen_exe = IKEMEN_PATH / "Ikemen_GO.exe"
        return ikemen_exe.exists()

    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Header avec gradient
        header_frame = tk.Frame(self.root, bg='#0f3460', height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="MULTIJOUEUR",
            font=('Arial', 32, 'bold'),
            fg='#00d9ff',
            bg='#0f3460'
        )
        title_label.pack(pady=15)

        subtitle = tk.Label(
            header_frame,
            text="Affrontez vos amis en local ou en ligne!",
            font=('Arial', 12),
            fg='#aaa',
            bg='#0f3460'
        )
        subtitle.pack()

        # Status Ikemen
        status_text = "Ikemen GO installé" if self.ikemen_installed else "Ikemen GO non installé (requis pour réseau)"
        status_color = '#00ff00' if self.ikemen_installed else '#ff6b35'

        status_label = tk.Label(
            header_frame,
            text=f"● {status_text}",
            font=('Arial', 9),
            fg=status_color,
            bg='#0f3460'
        )
        status_label.pack(pady=5)

        # Main content area
        content_frame = tk.Frame(self.root, bg='#16213e', padx=40, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Notebook pour les onglets
        style = ttk.Style()
        style.configure('TNotebook', background='#16213e')
        style.configure('TNotebook.Tab', padding=[20, 10])

        notebook = ttk.Notebook(content_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Onglet 1: Jeu Local
        local_frame = tk.Frame(notebook, bg='#16213e')
        notebook.add(local_frame, text="🎮 Local (2 joueurs)")
        self.setup_local_tab(local_frame)

        # Onglet 2: Réseau
        network_frame = tk.Frame(notebook, bg='#16213e')
        notebook.add(network_frame, text="🌐 Réseau")
        self.setup_network_tab(network_frame)

        # Onglet 3: Configuration
        config_frame = tk.Frame(notebook, bg='#16213e')
        notebook.add(config_frame, text="⚙ Configuration")
        self.setup_config_tab(config_frame)

        # Onglet 4: Aide
        help_frame = tk.Frame(notebook, bg='#16213e')
        notebook.add(help_frame, text="📖 Aide")
        self.setup_help_tab(help_frame)

        # Footer avec bouton retour
        footer_frame = tk.Frame(self.root, bg='#0f3460', height=50)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        back_btn = tk.Button(
            footer_frame,
            text="← Retour au launcher",
            font=('Arial', 11),
            bg='#16213e',
            fg='#eee',
            cursor='hand2',
            command=self.root.destroy,
            bd=0,
            padx=20,
            pady=10
        )
        back_btn.pack(side=tk.LEFT, padx=20, pady=10)

    def setup_local_tab(self, parent):
        """Configure l'onglet jeu local"""
        # Description
        desc_label = tk.Label(
            parent,
            text="Mode 2 joueurs sur le même PC\nJoueur 1 utilise le clavier, Joueur 2 utilise la manette ou un second clavier",
            font=('Arial', 11),
            fg='#ccc',
            bg='#16213e',
            justify=tk.LEFT
        )
        desc_label.pack(pady=20, padx=20)

        # Configuration des contrôles
        controls_frame = tk.LabelFrame(
            parent,
            text="Configuration des Contrôles",
            font=('Arial', 12, 'bold'),
            bg='#16213e',
            fg='#00d9ff',
            padx=15,
            pady=15
        )
        controls_frame.pack(fill=tk.X, padx=20, pady=10)

        # Joueur 1
        p1_frame = tk.Frame(controls_frame, bg='#16213e')
        p1_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            p1_frame,
            text="Joueur 1:",
            font=('Arial', 11, 'bold'),
            fg='#00ff41',
            bg='#16213e'
        ).pack(anchor=tk.W)

        tk.Label(
            p1_frame,
            text="Flèches directionnelles + A/S/D/F/G/H pour les actions",
            font=('Arial', 10),
            fg='#aaa',
            bg='#16213e'
        ).pack(anchor=tk.W, padx=20)

        # Joueur 2
        p2_frame = tk.Frame(controls_frame, bg='#16213e')
        p2_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            p2_frame,
            text="Joueur 2:",
            font=('Arial', 11, 'bold'),
            fg='#0099ff',
            bg='#16213e'
        ).pack(anchor=tk.W)

        tk.Label(
            p2_frame,
            text="Q/W/E/R pour directions + T/Y/U/I/O/P pour les actions",
            font=('Arial', 10),
            fg='#aaa',
            bg='#16213e'
        ).pack(anchor=tk.W, padx=20)

        # Bouton de lancement
        launch_frame = tk.Frame(parent, bg='#16213e')
        launch_frame.pack(pady=30)

        local_btn = tk.Button(
            launch_frame,
            text="▶ LANCER MODE LOCAL",
            font=('Arial', 16, 'bold'),
            bg='#00ff41',
            fg='#000',
            activebackground='#00cc33',
            cursor='hand2',
            command=self.launch_local_multiplayer,
            relief=tk.RAISED,
            bd=3,
            padx=40,
            pady=15
        )
        local_btn.pack()

        # Tips
        tips_text = """
💡 Conseils:
• Assurez-vous que les deux joueurs connaissent leurs contrôles
• Testez les contrôles dans le training mode d'abord
• Pour manettes: configurez-les dans les options du jeu
        """

        tips_label = tk.Label(
            parent,
            text=tips_text,
            font=('Arial', 9),
            fg='#888',
            bg='#16213e',
            justify=tk.LEFT
        )
        tips_label.pack(pady=10)

    def setup_network_tab(self, parent):
        """Configure l'onglet réseau"""
        if not self.ikemen_installed:
            # Message d'installation
            warning_frame = tk.Frame(parent, bg='#ff6b35', padx=20, pady=15)
            warning_frame.pack(fill=tk.X, padx=20, pady=20)

            tk.Label(
                warning_frame,
                text="⚠ Ikemen GO non installé",
                font=('Arial', 14, 'bold'),
                fg='#fff',
                bg='#ff6b35'
            ).pack()

            tk.Label(
                warning_frame,
                text="Le mode réseau nécessite Ikemen GO pour fonctionner",
                font=('Arial', 10),
                fg='#fff',
                bg='#ff6b35'
            ).pack(pady=5)

            install_btn = tk.Button(
                parent,
                text="📥 Installer Ikemen GO",
                font=('Arial', 12, 'bold'),
                bg='#00d9ff',
                fg='#000',
                cursor='hand2',
                command=self.install_ikemen_go,
                padx=30,
                pady=10
            )
            install_btn.pack(pady=20)

            return

        # Configuration du joueur
        player_frame = tk.LabelFrame(
            parent,
            text="Votre Profil",
            font=('Arial', 12, 'bold'),
            bg='#16213e',
            fg='#00d9ff',
            padx=15,
            pady=15
        )
        player_frame.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(
            player_frame,
            text="Nom du joueur:",
            font=('Arial', 10),
            fg='#ccc',
            bg='#16213e'
        ).grid(row=0, column=0, sticky=tk.W, pady=5)

        name_entry = tk.Entry(
            player_frame,
            textvariable=self.player_name_var,
            font=('Arial', 11),
            width=25
        )
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Mode de connexion
        mode_frame = tk.LabelFrame(
            parent,
            text="Mode de Connexion",
            font=('Arial', 12, 'bold'),
            bg='#16213e',
            fg='#00d9ff',
            padx=15,
            pady=15
        )
        mode_frame.pack(fill=tk.X, padx=20, pady=15)

        # Héberger
        host_subframe = tk.Frame(mode_frame, bg='#16213e')
        host_subframe.pack(fill=tk.X, pady=10)

        tk.Radiobutton(
            host_subframe,
            text="🖥 Héberger une partie",
            variable=self.mode_var,
            value="host",
            font=('Arial', 11),
            fg='#00ff41',
            bg='#16213e',
            selectcolor='#16213e',
            activebackground='#16213e',
            activeforeground='#00ff41'
        ).pack(anchor=tk.W)

        tk.Label(
            host_subframe,
            text="Les autres joueurs se connectent à votre IP",
            font=('Arial', 9),
            fg='#888',
            bg='#16213e'
        ).pack(anchor=tk.W, padx=25)

        # Rejoindre
        join_subframe = tk.Frame(mode_frame, bg='#16213e')
        join_subframe.pack(fill=tk.X, pady=10)

        tk.Radiobutton(
            join_subframe,
            text="🔗 Rejoindre une partie",
            variable=self.mode_var,
            value="join",
            font=('Arial', 11),
            fg='#0099ff',
            bg='#16213e',
            selectcolor='#16213e',
            activebackground='#16213e',
            activeforeground='#0099ff'
        ).pack(anchor=tk.W)

        # IP/Port pour rejoindre
        connection_frame = tk.Frame(join_subframe, bg='#16213e')
        connection_frame.pack(anchor=tk.W, padx=25, pady=5)

        tk.Label(
            connection_frame,
            text="IP:",
            font=('Arial', 10),
            fg='#ccc',
            bg='#16213e'
        ).grid(row=0, column=0, padx=5)

        ip_entry = tk.Entry(
            connection_frame,
            textvariable=self.ip_var,
            font=('Arial', 10),
            width=20
        )
        ip_entry.grid(row=0, column=1, padx=5)

        tk.Label(
            connection_frame,
            text="Port:",
            font=('Arial', 10),
            fg='#ccc',
            bg='#16213e'
        ).grid(row=0, column=2, padx=5)

        port_entry = tk.Entry(
            connection_frame,
            textvariable=self.port_var,
            font=('Arial', 10),
            width=8
        )
        port_entry.grid(row=0, column=3, padx=5)

        # Boutons d'action
        action_frame = tk.Frame(parent, bg='#16213e')
        action_frame.pack(pady=20)

        connect_btn = tk.Button(
            action_frame,
            text="🌐 SE CONNECTER",
            font=('Arial', 14, 'bold'),
            bg='#00d9ff',
            fg='#000',
            cursor='hand2',
            command=self.launch_network_multiplayer,
            relief=tk.RAISED,
            bd=3,
            padx=30,
            pady=12
        )
        connect_btn.pack()

        # Info IP locale
        local_ip = self.get_local_ip()
        ip_info = tk.Label(
            parent,
            text=f"💡 Votre IP locale: {local_ip}",
            font=('Arial', 10),
            fg='#888',
            bg='#16213e'
        )
        ip_info.pack(pady=10)

    def setup_config_tab(self, parent):
        """Configure l'onglet configuration"""
        # Qualité réseau
        quality_frame = tk.LabelFrame(
            parent,
            text="Qualité Réseau",
            font=('Arial', 12, 'bold'),
            bg='#16213e',
            fg='#00d9ff',
            padx=15,
            pady=15
        )
        quality_frame.pack(fill=tk.X, padx=20, pady=15)

        quality_var = tk.StringVar(value=self.config.get("network_quality"))

        qualities = [
            ("Haute (LAN/Fibre)", "high"),
            ("Moyenne (ADSL)", "medium"),
            ("Basse (3G/4G)", "low")
        ]

        for text, value in qualities:
            tk.Radiobutton(
                quality_frame,
                text=text,
                variable=quality_var,
                value=value,
                font=('Arial', 10),
                fg='#ccc',
                bg='#16213e',
                selectcolor='#16213e',
                command=lambda v=value: self.config.set("network_quality", v)
            ).pack(anchor=tk.W, pady=3)

        # Options diverses
        options_frame = tk.LabelFrame(
            parent,
            text="Options",
            font=('Arial', 12, 'bold'),
            bg='#16213e',
            fg='#00d9ff',
            padx=15,
            pady=15
        )
        options_frame.pack(fill=tk.X, padx=20, pady=15)

        auto_save_var = tk.BooleanVar(value=self.config.get("auto_save"))
        tk.Checkbutton(
            options_frame,
            text="Sauvegarder automatiquement la configuration",
            variable=auto_save_var,
            font=('Arial', 10),
            fg='#ccc',
            bg='#16213e',
            selectcolor='#16213e',
            command=lambda: self.config.set("auto_save", auto_save_var.get())
        ).pack(anchor=tk.W, pady=3)

        chat_var = tk.BooleanVar(value=self.config.get("enable_chat"))
        tk.Checkbutton(
            options_frame,
            text="Activer le chat en jeu",
            variable=chat_var,
            font=('Arial', 10),
            fg='#ccc',
            bg='#16213e',
            selectcolor='#16213e',
            command=lambda: self.config.set("enable_chat", chat_var.get())
        ).pack(anchor=tk.W, pady=3)

        # Bouton réinitialiser
        reset_btn = tk.Button(
            parent,
            text="Réinitialiser la configuration",
            font=('Arial', 10),
            bg='#ff6b35',
            fg='#fff',
            cursor='hand2',
            command=self.reset_config,
            padx=20,
            pady=8
        )
        reset_btn.pack(pady=20)

    def setup_help_tab(self, parent):
        """Configure l'onglet aide"""
        # Zone de texte avec scroll
        help_text = scrolledtext.ScrolledText(
            parent,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg='#0a0e27',
            fg='#00ff41',
            height=20
        )
        help_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        help_content = """
═══════════════════════════════════════════════════════════════
                    GUIDE MULTIJOUEUR KOF ULTIMATE
═══════════════════════════════════════════════════════════════

🎮 MODE LOCAL (2 joueurs sur le même PC)
────────────────────────────────────────────────────────────────
• Nécessite: Rien de spécial!
• Comment jouer:
  1. Cliquez sur l'onglet "Local"
  2. Configurez les contrôles si nécessaire
  3. Cliquez sur "LANCER MODE LOCAL"
  4. Sélectionnez vos personnages
  5. Combattez!

• Contrôles par défaut:
  - Joueur 1: Flèches + A/S/D/F/G/H
  - Joueur 2: Q/W/E/R + T/Y/U/I/O/P
  - Ou utilisez des manettes

🌐 MODE RÉSEAU (En ligne/LAN)
────────────────────────────────────────────────────────────────
• Nécessite: Ikemen GO installé
• Comment installer Ikemen GO:
  1. Télécharger: github.com/ikemen-engine/Ikemen-GO/releases
  2. Extraire dans: D:\\KOF Ultimate Online\\
  3. Relancer ce menu

• Pour HÉBERGER une partie:
  1. Onglet "Réseau"
  2. Entrez votre nom de joueur
  3. Sélectionnez "Héberger une partie"
  4. Donnez votre IP locale aux autres joueurs
  5. Cliquez sur "SE CONNECTER"
  6. Attendez que les joueurs rejoignent

• Pour REJOINDRE une partie:
  1. Onglet "Réseau"
  2. Entrez votre nom de joueur
  3. Sélectionnez "Rejoindre une partie"
  4. Entrez l'IP de l'hôte
  5. Cliquez sur "SE CONNECTER"

⚙ CONFIGURATION
────────────────────────────────────────────────────────────────
• Qualité réseau:
  - Haute: Pour connexions LAN ou fibre
  - Moyenne: Pour ADSL standard
  - Basse: Pour connexions mobiles

• Options:
  - Sauvegarde auto: Garde vos paramètres
  - Chat: Active le chat textuel pendant les parties

🔧 DÉPANNAGE
────────────────────────────────────────────────────────────────
• Problème: "Ikemen GO non installé"
  → Solution: Installez Ikemen GO (voir section réseau)

• Problème: "Impossible de se connecter"
  → Vérifiez:
    - L'IP est correcte
    - Le port est ouvert (7500 par défaut)
    - Le pare-feu autorise la connexion
    - L'hôte a lancé le jeu

• Problème: "Lag/latence"
  → Solutions:
    - Réduisez la qualité réseau
    - Fermez les autres programmes
    - Vérifiez votre connexion internet

📝 NOTES IMPORTANTES
────────────────────────────────────────────────────────────────
• Le mode local fonctionne avec le moteur MUGEN standard
• Le mode réseau nécessite Ikemen GO (moteur amélioré)
• Pour jouer en ligne: configurez le port forwarding (7500)
• Discord recommandé pour la communication vocale

═══════════════════════════════════════════════════════════════
        """

        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)

        # Boutons de liens utiles
        links_frame = tk.Frame(parent, bg='#16213e')
        links_frame.pack(pady=10)

        tk.Button(
            links_frame,
            text="📥 Télécharger Ikemen GO",
            font=('Arial', 10),
            bg='#00d9ff',
            fg='#000',
            cursor='hand2',
            command=lambda: webbrowser.open("https://github.com/ikemen-engine/Ikemen-GO/releases"),
            padx=15,
            pady=5
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            links_frame,
            text="📖 Guide Complet (MD)",
            font=('Arial', 10),
            bg='#00ff41',
            fg='#000',
            cursor='hand2',
            command=self.open_full_guide,
            padx=15,
            pady=5
        ).pack(side=tk.LEFT, padx=5)

    def launch_local_multiplayer(self):
        """Lance le mode multijoueur local"""
        # Sauvegarder la config
        self.config.set("last_player_name", self.player_name_var.get())

        # Lancer le jeu MUGEN en mode versus
        exe_path = GAME_PATH / "KOF_Ultimate_Online.exe"

        if not exe_path.exists():
            messagebox.showerror(
                "Erreur",
                f"Executable non trouvé:\n{exe_path}"
            )
            return

        try:
            # Configurer le mode versus dans mugen.cfg si possible
            self.configure_versus_mode()

            # Lancer le jeu
            subprocess.Popen([str(exe_path)], cwd=str(GAME_PATH))

            messagebox.showinfo(
                "Jeu lancé",
                "Le jeu a été lancé en mode multijoueur local!\n\n"
                "Sélectionnez 'Versus Mode' dans le menu principal."
            )

            # Minimiser la fenêtre
            self.root.iconify()

        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Impossible de lancer le jeu:\n{e}"
            )

    def launch_network_multiplayer(self):
        """Lance le mode multijoueur réseau"""
        if not self.ikemen_installed:
            messagebox.showerror(
                "Erreur",
                "Ikemen GO n'est pas installé!\n\n"
                "Installez-le depuis l'onglet Réseau."
            )
            return

        # Sauvegarder la config
        self.config.set("last_player_name", self.player_name_var.get())
        self.config.set("last_ip", self.ip_var.get())
        self.config.set("last_port", self.port_var.get())

        # Lancer Ikemen GO
        ikemen_exe = IKEMEN_PATH / "Ikemen_GO.exe"

        try:
            subprocess.Popen([str(ikemen_exe)], cwd=str(IKEMEN_PATH))

            mode = self.mode_var.get()
            if mode == "host":
                msg = f"Ikemen GO lancé en mode hébergement!\n\n" \
                      f"Votre IP: {self.get_local_ip()}\n" \
                      f"Port: {self.port_var.get()}\n\n" \
                      f"Communiquez ces informations aux autres joueurs."
            else:
                msg = f"Ikemen GO lancé!\n\n" \
                      f"Connectez-vous à: {self.ip_var.get()}:{self.port_var.get()}\n\n" \
                      f"Dans le menu du jeu:\n" \
                      f"1. Sélectionnez 'Network'\n" \
                      f"2. Entrez l'IP et le port\n" \
                      f"3. Rejoignez la partie"

            messagebox.showinfo("Jeu lancé", msg)
            self.root.iconify()

        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Impossible de lancer Ikemen GO:\n{e}"
            )

    def configure_versus_mode(self):
        """Configure le mode versus dans mugen.cfg"""
        config_file = GAME_PATH / "data" / "mugen.cfg"

        if not config_file.exists():
            return

        try:
            with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # S'assurer que P2 utilise un contrôleur (clavier ou joystick)
            modified = []
            for line in lines:
                if line.strip().startswith('P2.UseKeyboard'):
                    modified.append('P2.UseKeyboard = 1\n')
                else:
                    modified.append(line)

            with open(config_file, 'w', encoding='utf-8') as f:
                f.writelines(modified)

        except Exception as e:
            print(f"Error configuring versus mode: {e}")

    def install_ikemen_go(self):
        """Guide d'installation d'Ikemen GO"""
        response = messagebox.askyesno(
            "Installation Ikemen GO",
            "Ikemen GO est nécessaire pour le mode réseau.\n\n"
            "Étapes:\n"
            "1. Le téléchargement va démarrer\n"
            "2. Extrayez dans: D:\\KOF Ultimate Online\\\n"
            "3. Relancez ce menu\n\n"
            "Ouvrir la page de téléchargement?"
        )

        if response:
            webbrowser.open("https://github.com/ikemen-engine/Ikemen-GO/releases/latest")

    def get_local_ip(self):
        """Récupère l'IP locale"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def reset_config(self):
        """Réinitialise la configuration"""
        response = messagebox.askyesno(
            "Confirmation",
            "Réinitialiser toute la configuration?\n\n"
            "Cette action ne peut pas être annulée."
        )

        if response:
            if CONFIG_FILE.exists():
                CONFIG_FILE.unlink()
            self.config = MultiplayerConfig()
            messagebox.showinfo("Succès", "Configuration réinitialisée!")
            self.root.destroy()

    def open_full_guide(self):
        """Ouvre le guide complet en markdown"""
        guide_file = GAME_PATH / "GUIDE_MULTIJOUEUR.md"
        if guide_file.exists():
            os.startfile(str(guide_file))
        else:
            messagebox.showwarning(
                "Guide non trouvé",
                f"Le guide complet n'a pas été trouvé:\n{guide_file}"
            )

    def run(self):
        """Lance le menu"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MultiplayerMenu()
    app.run()
