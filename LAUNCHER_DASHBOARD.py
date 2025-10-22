#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LAUNCHER DASHBOARD - Launcher Principal KOF Ultimate Online
Avec accès direct au Dashboard HTML
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

class KOFLauncherDashboard:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.window = tk.Tk()
        self.window.title("KOF Ultimate Online - Launcher")
        self.window.geometry("800x600")
        self.window.resizable(False, False)

        # Couleurs
        self.bg_color = "#1a1a2e"
        self.accent_color = "#667eea"
        self.text_color = "#eaeaea"
        self.card_color = "#0f3460"

        self.setup_ui()

    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')

        # Arrière-plan principal
        self.window.configure(bg=self.bg_color)

        # Header
        header_frame = tk.Frame(self.window, bg=self.accent_color, height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🎮 KOF ULTIMATE ONLINE",
            font=("Segoe UI", 28, "bold"),
            bg=self.accent_color,
            fg="white"
        )
        title_label.pack(pady=30)

        # Container principal
        main_frame = tk.Frame(self.window, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Grid de boutons
        buttons_config = [
            ("🎮 Lancer le Jeu", self.launch_game, 0, 0, 2),
            ("📊 Dashboard", self.open_dashboard, 1, 0, 1),
            ("🧪 Test Auto", self.launch_auto_test, 1, 1, 1),
            ("⚔️ Test Matchmaking", self.launch_matchmaking_test, 2, 0, 1),
            ("🔍 Scanner Erreurs", self.scan_errors, 2, 1, 1),
            ("📖 Guides", self.open_guides, 3, 0, 1),
            ("⚙️ Configuration", self.open_config, 3, 1, 1),
        ]

        for text, command, row, col, colspan in buttons_config:
            btn = tk.Button(
                main_frame,
                text=text,
                command=command,
                font=("Segoe UI", 14, "bold"),
                bg=self.card_color,
                fg=self.text_color,
                activebackground=self.accent_color,
                activeforeground="white",
                relief=tk.FLAT,
                cursor="hand2",
                height=3
            )
            btn.grid(row=row, column=col, columnspan=colspan,
                    sticky="nsew", padx=5, pady=5)

        # Configurer les poids des lignes/colonnes
        for i in range(4):
            main_frame.grid_rowconfigure(i, weight=1)
        for i in range(2):
            main_frame.grid_columnconfigure(i, weight=1)

        # Status bar
        status_frame = tk.Frame(self.window, bg=self.card_color, height=40)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            text="✓ Prêt à jouer",
            font=("Segoe UI", 10),
            bg=self.card_color,
            fg=self.text_color
        )
        self.status_label.pack(pady=10)

    def set_status(self, text):
        """Met à jour le texte de status"""
        self.status_label.config(text=text)
        self.window.update()

    def launch_game(self):
        """Lance le jeu"""
        self.set_status("🎮 Lancement du jeu...")
        try:
            game_exe = self.base_path / "KOF_Ultimate_Online.exe"
            if game_exe.exists():
                subprocess.Popen([str(game_exe)], cwd=str(self.base_path))
                self.set_status("✓ Jeu lancé!")
            else:
                messagebox.showerror("Erreur", "Fichier KOF_Ultimate_Online.exe introuvable!")
                self.set_status("❌ Erreur de lancement")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer le jeu: {e}")
            self.set_status("❌ Erreur")

    def open_dashboard(self):
        """Ouvre le dashboard HTML"""
        self.set_status("📊 Ouverture du dashboard...")
        try:
            dashboard = self.base_path / "DASHBOARD_KOF.html"
            if dashboard.exists():
                webbrowser.open(str(dashboard))
                self.set_status("✓ Dashboard ouvert!")
            else:
                messagebox.showerror("Erreur", "Dashboard non trouvé!")
                self.set_status("❌ Dashboard introuvable")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le dashboard: {e}")
            self.set_status("❌ Erreur")

    def launch_auto_test(self):
        """Lance le test automatique"""
        self.set_status("🧪 Lancement test auto...")
        try:
            test_bat = self.base_path / "TEST_AUTO_SIMPLE.bat"
            if test_bat.exists():
                subprocess.Popen([str(test_bat)], cwd=str(self.base_path),
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
                self.set_status("✓ Test auto lancé!")
            else:
                messagebox.showerror("Erreur", "Script de test introuvable!")
                self.set_status("❌ Script introuvable")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer le test: {e}")
            self.set_status("❌ Erreur")

    def launch_matchmaking_test(self):
        """Lance le test de matchmaking"""
        self.set_status("⚔️ Test matchmaking en cours...")
        try:
            script = self.base_path / "TEST_MATCHMAKING_INTELLIGENT.py"
            if script.exists():
                subprocess.Popen([sys.executable, str(script), "15"],
                               cwd=str(self.base_path),
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
                self.set_status("✓ Test matchmaking lancé!")
                messagebox.showinfo("Test Matchmaking",
                                  "Le test va simuler 15 rounds de matchmaking.\n"
                                  "Le rapport HTML s'ouvrira automatiquement à la fin.")
            else:
                messagebox.showerror("Erreur", "Script de test introuvable!")
                self.set_status("❌ Script introuvable")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer le test: {e}")
            self.set_status("❌ Erreur")

    def scan_errors(self):
        """Lance le scanner d'erreurs"""
        self.set_status("🔍 Scan des erreurs...")
        try:
            script = self.base_path / "FIND_ALL_ERRORS.py"
            if script.exists():
                subprocess.Popen([sys.executable, str(script)],
                               cwd=str(self.base_path),
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
                self.set_status("✓ Scanner lancé!")
            else:
                messagebox.showerror("Erreur", "Scanner introuvable!")
                self.set_status("❌ Scanner introuvable")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer le scanner: {e}")
            self.set_status("❌ Erreur")

    def open_guides(self):
        """Ouvre la page des guides"""
        self.set_status("📖 Ouverture des guides...")
        try:
            guides = self.base_path / "RAPPORTS_JOURNALIERS.html"
            if guides.exists():
                webbrowser.open(str(guides))
                self.set_status("✓ Guides ouverts!")
            else:
                messagebox.showinfo("Guides",
                                  "Guides disponibles:\n"
                                  "- COMMENT_JOUER.md\n"
                                  "- GUIDE_LAUNCHERS.md\n"
                                  "- GUIDE_NETPLAY.md\n"
                                  "- README_MATCHMAKING.md")
                self.set_status("ℹ️ Consultez le dossier")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {e}")
            self.set_status("❌ Erreur")

    def open_config(self):
        """Ouvre la configuration"""
        self.set_status("⚙️ Configuration...")
        messagebox.showinfo("Configuration",
                          "Configuration du jeu:\n\n"
                          "• Mode fenêtré: 640x480 (test)\n"
                          "• Restaurer plein écran: Copier mugen.cfg.mini_backup\n"
                          "• Fichiers de config: data/mugen.cfg, system.def\n\n"
                          "Pour modifier, éditer les fichiers dans data/")
        self.set_status("ℹ️ Info configuration")

    def run(self):
        """Lance l'interface"""
        self.window.mainloop()

if __name__ == "__main__":
    launcher = KOFLauncherDashboard()
    launcher.run()
