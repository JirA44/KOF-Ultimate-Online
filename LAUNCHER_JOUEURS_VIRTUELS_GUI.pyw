#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LAUNCHER GRAPHIQUE - Joueurs Virtuels
Double-cliquer pour lancer (pas de console)
Extension .pyw = pas de fenêtre console
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import webbrowser
from pathlib import Path
import threading

class VirtualPlayersLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎮 Joueurs Virtuels - KOF Ultimate Online")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Couleurs
        self.bg_color = "#1a1a2e"
        self.fg_color = "#e0e0e0"
        self.accent_color = "#ffd700"
        self.button_color = "#2d2d44"

        self.root.configure(bg=self.bg_color)

        self.game_dir = Path(r"D:\KOF Ultimate Online")

        self.create_widgets()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(pady=20)

        title = tk.Label(
            header_frame,
            text="🎮 Joueurs Virtuels Autonomes",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title.pack()

        subtitle = tk.Label(
            header_frame,
            text="KOF Ultimate Online - Lancement Simplifié",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color
        )
        subtitle.pack()

        # Séparateur
        separator = tk.Frame(self.root, height=2, bg=self.accent_color)
        separator.pack(fill="x", padx=50, pady=10)

        # Options
        options_frame = tk.Frame(self.root, bg=self.bg_color)
        options_frame.pack(pady=20)

        # Nombre de joueurs
        tk.Label(
            options_frame,
            text="Nombre de joueurs:",
            font=("Arial", 11),
            bg=self.bg_color,
            fg=self.fg_color
        ).grid(row=0, column=0, sticky="w", padx=20, pady=10)

        self.num_players = tk.StringVar(value="3")
        players_combo = ttk.Combobox(
            options_frame,
            textvariable=self.num_players,
            values=["1", "2", "3", "4", "5", "10"],
            state="readonly",
            width=10,
            font=("Arial", 10)
        )
        players_combo.grid(row=0, column=1, padx=20, pady=10)

        # Durée session
        tk.Label(
            options_frame,
            text="Durée session (minutes):",
            font=("Arial", 11),
            bg=self.bg_color,
            fg=self.fg_color
        ).grid(row=1, column=0, sticky="w", padx=20, pady=10)

        self.duration = tk.StringVar(value="120")
        duration_combo = ttk.Combobox(
            options_frame,
            textvariable=self.duration,
            values=["30", "60", "120", "240", "480", "∞"],
            state="readonly",
            width=10,
            font=("Arial", 10)
        )
        duration_combo.grid(row=1, column=1, padx=20, pady=10)

        # Options supplémentaires
        self.show_dashboard = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Ouvrir le dashboard automatiquement",
            variable=self.show_dashboard,
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor=self.button_color,
            activebackground=self.bg_color,
            activeforeground=self.fg_color
        ).grid(row=2, column=0, columnspan=2, pady=10)

        # Boutons principaux
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(pady=30)

        # Bouton Lancer
        launch_btn = tk.Button(
            buttons_frame,
            text="▶️  LANCER LES JOUEURS VIRTUELS",
            command=self.launch_players,
            font=("Arial", 12, "bold"),
            bg="#4caf50",
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            relief="raised",
            bd=3,
            padx=20,
            pady=15,
            cursor="hand2"
        )
        launch_btn.pack(pady=5)

        # Bouton Dashboard seul
        dashboard_btn = tk.Button(
            buttons_frame,
            text="📊  OUVRIR DASHBOARD SEULEMENT",
            command=self.open_dashboard,
            font=("Arial", 10),
            bg="#2196f3",
            fg="white",
            activebackground="#0b7dda",
            activeforeground="white",
            relief="raised",
            bd=2,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        dashboard_btn.pack(pady=5)

        # Bouton Documentation
        doc_btn = tk.Button(
            buttons_frame,
            text="📖  VOIR LA DOCUMENTATION",
            command=self.open_docs,
            font=("Arial", 10),
            bg="#ff9800",
            fg="white",
            activebackground="#e68900",
            activeforeground="white",
            relief="raised",
            bd=2,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        doc_btn.pack(pady=5)

        # Bouton Test Rapide
        test_btn = tk.Button(
            buttons_frame,
            text="🧪  TEST RAPIDE (2 min)",
            command=self.run_quick_test,
            font=("Arial", 10),
            bg="#9c27b0",
            fg="white",
            activebackground="#7b1fa2",
            activeforeground="white",
            relief="raised",
            bd=2,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        test_btn.pack(pady=5)

        # Footer
        footer = tk.Label(
            self.root,
            text="🤖 Créé avec Claude Code | v1.0",
            font=("Arial", 8),
            bg=self.bg_color,
            fg="#666"
        )
        footer.pack(side="bottom", pady=10)

        # Status bar
        self.status_var = tk.StringVar(value="Prêt à lancer")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Arial", 9),
            bg=self.button_color,
            fg=self.fg_color,
            anchor="w",
            padx=10,
            pady=5
        )
        status_bar.pack(side="bottom", fill="x")

    def launch_players(self):
        """Lance les joueurs virtuels"""
        num = self.num_players.get()
        duration = self.duration.get()

        # Vérifier que le jeu est lancé
        response = messagebox.askyesno(
            "Confirmation",
            f"⚠️  Avant de continuer, assurez-vous que:\n\n"
            f"✅ KOF Ultimate Online est lancé\n"
            f"✅ Le jeu est au menu principal\n"
            f"✅ Le jeu est en mode fenêtré (pas fullscreen)\n\n"
            f"Configuration:\n"
            f"• {num} joueur(s) virtuel(s)\n"
            f"• Session de {duration} minutes\n\n"
            f"Continuer ?"
        )

        if not response:
            return

        try:
            self.status_var.set(f"🚀 Lancement de {num} joueurs...")

            # Créer un script temporaire avec la config
            script_path = self.game_dir / "temp_launch_config.py"

            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(f'''
import sys
sys.path.insert(0, r"{self.game_dir}")

from VIRTUAL_PLAYERS_CONTINUOUS import VirtualPlayersOrchestrator

orchestrator = VirtualPlayersOrchestrator(r"{self.game_dir}", num_players={num})
orchestrator.create_players()

duration = {"9999" if duration == "∞" else duration}

print("\\n" + "="*70)
print(f"  🎮 LANCEMENT DE {num} JOUEURS VIRTUELS")
print("="*70)
print(f"\\nDurée: {duration} minutes")
print("\\nLes joueurs sont actifs! Appuyez sur Ctrl+C pour arrêter.\\n")

try:
    orchestrator.start_all_players(int(duration))
    orchestrator.wait_for_completion()
except KeyboardInterrupt:
    print("\\n\\n⚠️  Arrêt demandé...")
finally:
    for player in orchestrator.players:
        player.save_stats()
    orchestrator.print_global_stats()
    print("\\n✅ Session terminée!\\n")
''')

            # Lancer le script dans une nouvelle fenêtre minimisée
            subprocess.Popen(
                [sys.executable, str(script_path)],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )

            # Ouvrir le dashboard si demandé
            if self.show_dashboard.get():
                self.open_dashboard()

            self.status_var.set(f"✅ {num} joueurs lancés! Voir la console séparée.")

            messagebox.showinfo(
                "Succès",
                f"✅ {num} joueur(s) virtuel(s) lancé(s)!\n\n"
                f"Une nouvelle console s'est ouverte avec les joueurs.\n"
                f"{'Le dashboard a été ouvert automatiquement.' if self.show_dashboard.get() else ''}\n\n"
                f"Pour arrêter: Ctrl+C dans la console des joueurs."
            )

        except Exception as e:
            self.status_var.set("❌ Erreur lors du lancement")
            messagebox.showerror(
                "Erreur",
                f"Erreur lors du lancement:\n\n{str(e)}"
            )

    def open_dashboard(self):
        """Ouvre le dashboard"""
        try:
            dashboard_path = self.game_dir / "VIRTUAL_PLAYERS_DASHBOARD.html"
            webbrowser.open(str(dashboard_path))
            self.status_var.set("📊 Dashboard ouvert dans le navigateur")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le dashboard:\n{e}")

    def open_docs(self):
        """Ouvre la documentation"""
        try:
            doc_path = self.game_dir / "README_VIRTUAL_PLAYERS.md"
            subprocess.Popen(['notepad', str(doc_path)])
            self.status_var.set("📖 Documentation ouverte")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir la doc:\n{e}")

    def run_quick_test(self):
        """Lance le test rapide"""
        response = messagebox.askyesno(
            "Test Rapide",
            "🧪 Test rapide de 2 minutes\n\n"
            "Ce test va:\n"
            "• Naviguer dans un menu\n"
            "• Sélectionner un personnage\n"
            "• Jouer 30 secondes\n\n"
            "Le jeu doit être au menu principal.\n\n"
            "Continuer ?"
        )

        if not response:
            return

        try:
            test_script = self.game_dir / "TEST_VIRTUAL_PLAYER_QUICK.py"

            subprocess.Popen(
                [sys.executable, str(test_script)],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )

            self.status_var.set("🧪 Test rapide lancé")

            messagebox.showinfo(
                "Test Lancé",
                "🧪 Test rapide lancé!\n\n"
                "Voir la console séparée pour le résultat."
            )
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur test:\n{e}")

    def run(self):
        """Lance l'interface"""
        self.root.mainloop()


if __name__ == "__main__":
    app = VirtualPlayersLauncher()
    app.run()
