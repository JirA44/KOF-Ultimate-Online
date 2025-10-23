"""
KOF Ultimate Online - Launcher d'Interface Modernisée
Lance les nouvelles interfaces ultra-modernes du jeu
"""

import os
import sys
import webbrowser
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

# Chemin du jeu
GAME_DIR = Path(__file__).parent
LAUNCHER_HTML = GAME_DIR / "GAME_LAUNCHER_ULTIMATE.html"
MULTIPLAYER_HTML = GAME_DIR / "MULTIPLAYER_BATTLENET.html"
GAME_EXE = GAME_DIR / "KOF_Ultimate_Online.exe"
IKEMEN_EXE = GAME_DIR / "Ikemen_GO.exe"


class UltimateInterfaceLauncher:
    """Launcher pour les interfaces modernisées"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KOF Ultimate - Launcher Sélection")
        self.root.geometry("600x400")
        self.root.configure(bg="#0a0e27")
        self.center_window()
        self.setup_ui()

    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Configure l'interface"""
        # Titre
        title = tk.Label(
            self.root,
            text="⚔️ KOF ULTIMATE LAUNCHER ⚔️",
            font=("Arial", 24, "bold"),
            bg="#0a0e27",
            fg="#00d4ff"
        )
        title.pack(pady=30)

        subtitle = tk.Label(
            self.root,
            text="Choisissez votre interface",
            font=("Arial", 14),
            bg="#0a0e27",
            fg="#888"
        )
        subtitle.pack(pady=10)

        # Boutons d'action
        button_frame = tk.Frame(self.root, bg="#0a0e27")
        button_frame.pack(pady=40)

        # Bouton Launcher Ultimate
        self.create_button(
            button_frame,
            "🎮 LAUNCHER ULTIMATE",
            "Interface principale modernisée",
            self.launch_ultimate_interface,
            "#00d4ff"
        ).pack(pady=10)

        # Bouton Multiplayer Battle.net
        self.create_button(
            button_frame,
            "🌐 MULTIPLAYER BATTLE.NET",
            "Interface multijoueur style Battle.net",
            self.launch_multiplayer_interface,
            "#00ff41"
        ).pack(pady=10)

        # Bouton Jeu Direct
        self.create_button(
            button_frame,
            "⚡ LANCER DIRECT",
            "Lancer le jeu directement",
            self.launch_game_direct,
            "#ff4444"
        ).pack(pady=10)

        # Footer
        footer = tk.Label(
            self.root,
            text="Interface créée avec Claude Code | v2.5.0",
            font=("Arial", 9),
            bg="#0a0e27",
            fg="#444"
        )
        footer.pack(side="bottom", pady=20)

    def create_button(self, parent, title, desc, command, color):
        """Crée un bouton stylisé"""
        frame = tk.Frame(parent, bg="#16213e", width=450, height=80)
        frame.pack_propagate(False)

        btn = tk.Button(
            frame,
            text=f"{title}\n{desc}",
            font=("Arial", 12, "bold"),
            bg=color,
            fg="#000",
            activebackground=color,
            activeforeground="#fff",
            cursor="hand2",
            command=command,
            relief="flat",
            bd=0
        )
        btn.pack(fill="both", expand=True, padx=2, pady=2)

        return frame

    def launch_ultimate_interface(self):
        """Lance l'interface principale modernisée"""
        if LAUNCHER_HTML.exists():
            print(f"🚀 Lancement de l'interface Ultimate...")
            webbrowser.open(str(LAUNCHER_HTML))
            self.root.after(1000, self.root.destroy)
        else:
            messagebox.showerror(
                "Erreur",
                f"Fichier introuvable:\n{LAUNCHER_HTML}"
            )

    def launch_multiplayer_interface(self):
        """Lance l'interface multijoueur Battle.net"""
        if MULTIPLAYER_HTML.exists():
            print(f"🌐 Lancement de l'interface Multijoueur...")
            webbrowser.open(str(MULTIPLAYER_HTML))
            self.root.after(1000, self.root.destroy)
        else:
            messagebox.showerror(
                "Erreur",
                f"Fichier introuvable:\n{MULTIPLAYER_HTML}"
            )

    def launch_game_direct(self):
        """Lance le jeu directement"""
        if GAME_EXE.exists():
            print(f"⚡ Lancement direct du jeu...")
            subprocess.Popen([str(GAME_EXE)], cwd=str(GAME_DIR))
            messagebox.showinfo(
                "Jeu lancé",
                "KOF Ultimate Online a été lancé !\n\nBonne partie ! 🎮"
            )
            self.root.destroy()
        elif IKEMEN_EXE.exists():
            print(f"⚡ Lancement direct du jeu (Ikemen)...")
            subprocess.Popen([str(IKEMEN_EXE)], cwd=str(GAME_DIR))
            messagebox.showinfo(
                "Jeu lancé",
                "KOF Ultimate Online (Ikemen) a été lancé !\n\nBonne partie ! 🎮"
            )
            self.root.destroy()
        else:
            messagebox.showerror(
                "Erreur",
                "Aucun exécutable de jeu trouvé!\n\n"
                f"Recherché:\n{GAME_EXE}\n{IKEMEN_EXE}"
            )

    def run(self):
        """Lance l'interface"""
        self.root.mainloop()


def launch_mode(mode="choose"):
    """
    Lance une interface spécifique

    Args:
        mode: "choose", "ultimate", "multiplayer", ou "game"
    """
    if mode == "ultimate":
        # Lancer directement l'interface Ultimate
        if LAUNCHER_HTML.exists():
            print(f"🚀 Lancement de l'interface Ultimate...")
            webbrowser.open(str(LAUNCHER_HTML))
        else:
            print(f"❌ Fichier introuvable: {LAUNCHER_HTML}")

    elif mode == "multiplayer":
        # Lancer directement l'interface Multiplayer
        if MULTIPLAYER_HTML.exists():
            print(f"🌐 Lancement de l'interface Multijoueur...")
            webbrowser.open(str(MULTIPLAYER_HTML))
        else:
            print(f"❌ Fichier introuvable: {MULTIPLAYER_HTML}")

    elif mode == "game":
        # Lancer directement le jeu
        if GAME_EXE.exists():
            print(f"⚡ Lancement direct du jeu...")
            subprocess.Popen([str(GAME_EXE)], cwd=str(GAME_DIR))
        elif IKEMEN_EXE.exists():
            print(f"⚡ Lancement direct du jeu (Ikemen)...")
            subprocess.Popen([str(IKEMEN_EXE)], cwd=str(GAME_DIR))
        else:
            print(f"❌ Aucun exécutable de jeu trouvé")

    else:
        # Afficher le menu de sélection
        app = UltimateInterfaceLauncher()
        app.run()


if __name__ == "__main__":
    # Si lancé avec un argument, utiliser cet argument comme mode
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        launch_mode(mode)
    else:
        # Sinon, afficher le menu de sélection
        launch_mode("choose")
