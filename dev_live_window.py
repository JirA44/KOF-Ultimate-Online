"""
KOF Ultimate - Live Development Window
Fenêtre de développement en temps réel pour tester les modifications
"""
import os
import sys
import time
import subprocess
import json
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import ttk, scrolledtext

class GameDevMonitor(FileSystemEventHandler):
    """Surveille les modifications de fichiers du jeu"""

    def __init__(self, callback):
        self.callback = callback
        self.last_modified = {}

    def on_modified(self, event):
        if event.is_directory:
            return

        file_ext = Path(event.src_path).suffix.lower()
        if file_ext in ['.def', '.cns', '.air', '.cmd', '.st']:
            # Éviter les doubles déclenchements
            current_time = time.time()
            if event.src_path in self.last_modified:
                if current_time - self.last_modified[event.src_path] < 1:
                    return

            self.last_modified[event.src_path] = current_time
            self.callback(event.src_path)

class DevWindow:
    """Fenêtre de développement principale"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KOF Ultimate - Dev Window")
        self.root.geometry("800x600")

        self.game_process = None
        self.observer = None
        self.game_path = Path(r"D:\KOF Ultimate Online Online Online")

        self.setup_ui()
        self.start_monitoring()

    def setup_ui(self):
        """Configure l'interface"""
        # Frame supérieur - Contrôles
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)

        ttk.Button(control_frame, text="▶ Lancer le jeu", command=self.start_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="⟳ Recharger", command=self.reload_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="■ Arrêter", command=self.stop_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="⚖ Équilibrer", command=self.open_balancer).pack(side=tk.LEFT, padx=5)

        # Séparateur
        ttk.Separator(self.root, orient='horizontal').pack(fill=tk.X, pady=5)

        # Frame notebook pour les onglets
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Onglet 1: Console/Logs
        log_frame = ttk.Frame(notebook)
        notebook.add(log_frame, text="📋 Console")

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Onglet 2: Stats des personnages
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="📊 Stats Personnages")

        self.stats_tree = ttk.Treeview(stats_frame, columns=('Character', 'Life', 'Attack', 'Defense'), show='headings')
        self.stats_tree.heading('Character', text='Personnage')
        self.stats_tree.heading('Life', text='Vie')
        self.stats_tree.heading('Attack', text='Attaque')
        self.stats_tree.heading('Defense', text='Défense')
        self.stats_tree.pack(fill=tk.BOTH, expand=True)

        # Onglet 3: Fichiers surveillés
        watch_frame = ttk.Frame(notebook)
        notebook.add(watch_frame, text="👁 Fichiers surveillés")

        self.watch_text = scrolledtext.ScrolledText(watch_frame, wrap=tk.WORD, height=20)
        self.watch_text.pack(fill=tk.BOTH, expand=True)

        # Onglet 4: Multijoueur
        multi_frame = ttk.Frame(notebook)
        notebook.add(multi_frame, text="🌐 Multijoueur")

        ttk.Label(multi_frame, text="Configuration réseau", font=('Arial', 12, 'bold')).pack(pady=10)
        ttk.Button(multi_frame, text="Héberger une partie", command=self.host_game).pack(pady=5)
        ttk.Button(multi_frame, text="Rejoindre une partie", command=self.join_game).pack(pady=5)
        ttk.Button(multi_frame, text="Installer Ikemen GO", command=self.install_ikemen).pack(pady=5)

        # Barre de statut
        self.status_bar = ttk.Label(self.root, text="Prêt", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def log(self, message):
        """Ajoute un message au log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    def start_monitoring(self):
        """Démarre la surveillance des fichiers"""
        self.log("🔍 Démarrage de la surveillance des fichiers...")

        event_handler = GameDevMonitor(self.on_file_changed)
        self.observer = Observer()

        # Surveiller les dossiers importants
        watch_dirs = ['data', 'chars', 'stages']
        for dir_name in watch_dirs:
            dir_path = self.game_path / dir_name
            if dir_path.exists():
                self.observer.schedule(event_handler, str(dir_path), recursive=True)
                self.log(f"✓ Surveillance: {dir_name}/")

        self.observer.start()
        self.status_bar.config(text="✓ Surveillance active")

    def on_file_changed(self, file_path):
        """Appelé quand un fichier est modifié"""
        file_name = Path(file_path).name
        self.log(f"📝 Modification détectée: {file_name}")
        self.watch_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {file_path}\n")
        self.watch_text.see(tk.END)

        # Auto-reload si le jeu tourne
        if self.game_process and self.game_process.poll() is None:
            self.log("⟳ Rechargement automatique...")
            # Note: MUGEN ne supporte pas le hot-reload,
            # mais on peut ajouter ça avec Ikemen GO

    def start_game(self):
        """Lance le jeu"""
        if self.game_process and self.game_process.poll() is None:
            self.log("⚠ Le jeu est déjà en cours d'exécution")
            return

        exe_path = self.game_path / "KOF_Ultimate_Online.exe"
        if not exe_path.exists():
            self.log("❌ Executable non trouvé!")
            return

        self.log("▶ Lancement du jeu...")
        try:
            # Lancer en mode fenêtré si possible
            self.game_process = subprocess.Popen([str(exe_path)], cwd=str(self.game_path))
            self.status_bar.config(text="▶ Jeu en cours")
            self.log("✓ Jeu lancé avec succès")
        except Exception as e:
            self.log(f"❌ Erreur au lancement: {e}")

    def reload_game(self):
        """Recharge le jeu"""
        self.log("⟳ Rechargement du jeu...")
        self.stop_game()
        time.sleep(1)
        self.start_game()

    def stop_game(self):
        """Arrête le jeu"""
        if self.game_process and self.game_process.poll() is None:
            self.log("■ Arrêt du jeu...")
            self.game_process.terminate()
            self.game_process.wait(timeout=5)
            self.status_bar.config(text="■ Jeu arrêté")
            self.log("✓ Jeu arrêté")

    def open_balancer(self):
        """Ouvre l'outil d'équilibrage"""
        self.log("⚖ Ouverture de l'outil d'équilibrage...")
        # Lancer le script d'équilibrage
        balance_script = self.game_path / "character_balancer.py"
        if balance_script.exists():
            subprocess.Popen([sys.executable, str(balance_script)])
        else:
            self.log("⚠ Script d'équilibrage non trouvé")

    def host_game(self):
        """Héberge une partie multijoueur"""
        self.log("🌐 Configuration du mode hébergement...")
        self.log("ℹ Nécessite Ikemen GO - Cliquez sur 'Installer Ikemen GO'")

    def join_game(self):
        """Rejoint une partie"""
        self.log("🌐 Mode rejoindre une partie...")
        self.log("ℹ Nécessite Ikemen GO")

    def install_ikemen(self):
        """Guide d'installation Ikemen GO"""
        install_info = """
=== Installation Ikemen GO ===

1. Télécharger: github.com/ikemen-engine/Ikemen-GO/releases
2. Extraire dans: D:\\KOF Ultimate Online\\
3. Copier les fichiers du jeu actuel
4. Configuration automatique disponible

Voulez-vous que j'ouvre le guide complet?
"""
        self.log(install_info)

    def run(self):
        """Lance la fenêtre"""
        self.log("🎮 KOF Ultimate - Fenêtre de développement")
        self.log("=" * 50)
        self.log("✓ Système prêt")
        self.log("ℹ Modifiez vos fichiers, les changements seront détectés")
        self.root.mainloop()

    def cleanup(self):
        """Nettoyage à la fermeture"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
        self.stop_game()

if __name__ == "__main__":
    try:
        # Installer watchdog si nécessaire
        try:
            import watchdog
        except ImportError:
            print("Installation de watchdog...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "watchdog"])
            print("✓ Watchdog installé. Relancez le script.")
            sys.exit(0)

        app = DevWindow()
        app.run()
        app.cleanup()
    except KeyboardInterrupt:
        print("\n✓ Arrêt propre")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
