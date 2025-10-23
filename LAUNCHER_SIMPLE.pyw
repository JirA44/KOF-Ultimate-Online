#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LAUNCHER 100% GRAPHIQUE - SANS CONSOLE
Double-cliquer pour lancer
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import webbrowser
from pathlib import Path
import os

class SimpleLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎮 Joueurs Virtuels KOF")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # Style
        self.bg = "#1a1a2e"
        self.fg = "#e0e0e0"
        self.accent = "#ffd700"

        self.root.configure(bg=self.bg)

        self.game_dir = Path(r"D:\KOF Ultimate Online")

        self.setup_ui()

    def setup_ui(self):
        # Titre
        tk.Label(
            self.root,
            text="🎮 Joueurs Virtuels",
            font=("Arial", 24, "bold"),
            bg=self.bg,
            fg=self.accent
        ).pack(pady=20)

        tk.Label(
            self.root,
            text="KOF Ultimate Online",
            font=("Arial", 12),
            bg=self.bg,
            fg=self.fg
        ).pack()

        # Séparateur
        tk.Frame(self.root, height=2, bg=self.accent).pack(fill="x", padx=50, pady=20)

        # Frame options
        opt_frame = tk.Frame(self.root, bg=self.bg)
        opt_frame.pack(pady=20)

        # Nombre de joueurs
        tk.Label(
            opt_frame,
            text="Nombre de joueurs:",
            font=("Arial", 11),
            bg=self.bg,
            fg=self.fg
        ).grid(row=0, column=0, sticky="e", padx=10, pady=10)

        self.num_var = tk.StringVar(value="3")
        num_combo = ttk.Combobox(
            opt_frame,
            textvariable=self.num_var,
            values=["1", "2", "3", "5", "10"],
            state="readonly",
            width=8
        )
        num_combo.grid(row=0, column=1, padx=10, pady=10)

        # Durée
        tk.Label(
            opt_frame,
            text="Durée (minutes):",
            font=("Arial", 11),
            bg=self.bg,
            fg=self.fg
        ).grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.dur_var = tk.StringVar(value="120")
        dur_combo = ttk.Combobox(
            opt_frame,
            textvariable=self.dur_var,
            values=["30", "60", "120", "240", "999"],
            state="readonly",
            width=8
        )
        dur_combo.grid(row=1, column=1, padx=10, pady=10)

        # Checkbox dashboard
        self.dash_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            opt_frame,
            text="Ouvrir le dashboard",
            variable=self.dash_var,
            font=("Arial", 10),
            bg=self.bg,
            fg=self.fg,
            selectcolor="#2d2d44",
            activebackground=self.bg,
            activeforeground=self.fg
        ).grid(row=2, column=0, columnspan=2, pady=10)

        # Boutons
        btn_frame = tk.Frame(self.root, bg=self.bg)
        btn_frame.pack(pady=30)

        # LANCER
        tk.Button(
            btn_frame,
            text="▶️  LANCER",
            command=self.launch,
            font=("Arial", 14, "bold"),
            bg="#4caf50",
            fg="white",
            activebackground="#45a049",
            padx=40,
            pady=15,
            relief="raised",
            bd=3,
            cursor="hand2"
        ).pack(pady=10)

        # Dashboard seul
        tk.Button(
            btn_frame,
            text="📊 Dashboard",
            command=self.open_dashboard,
            font=("Arial", 10),
            bg="#2196f3",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2"
        ).pack(pady=5)

        # Documentation
        tk.Button(
            btn_frame,
            text="📖 Documentation",
            command=self.open_docs,
            font=("Arial", 10),
            bg="#ff9800",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2"
        ).pack(pady=5)

        # Status
        self.status = tk.StringVar(value="Prêt")
        tk.Label(
            self.root,
            textvariable=self.status,
            font=("Arial", 9),
            bg="#2d2d44",
            fg=self.fg,
            anchor="w",
            padx=10,
            pady=5
        ).pack(side="bottom", fill="x")

    def launch(self):
        num = int(self.num_var.get())
        dur = int(self.dur_var.get())

        confirm = messagebox.askyesno(
            "Confirmation",
            f"⚠️  AVANT DE CONTINUER:\n\n"
            f"✅ Le jeu doit être lancé\n"
            f"✅ Au menu principal\n"
            f"✅ En mode fenêtré\n\n"
            f"• {num} joueur(s)\n"
            f"• {dur} minutes\n\n"
            f"Lancer ?"
        )

        if not confirm:
            return

        try:
            # Lancer chaque joueur en arrière-plan
            pythonw = sys.executable.replace("python.exe", "pythonw.exe")
            backend_script = self.game_dir / "VIRTUAL_PLAYERS_BACKEND.pyw"

            for i in range(1, num + 1):
                subprocess.Popen(
                    [pythonw, str(backend_script), str(i), str(num), str(dur), str(self.game_dir)],
                    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
                )

            self.status.set(f"✅ {num} joueurs lancés en arrière-plan")

            # Dashboard
            if self.dash_var.get():
                self.open_dashboard()

            messagebox.showinfo(
                "Succès",
                f"✅ {num} joueur(s) lancé(s)!\n\n"
                f"Ils tournent en arrière-plan.\n"
                f"Durée: {dur} min\n\n"
                f"Voir le dashboard pour le suivi."
            )

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur:\n{e}")
            self.status.set("❌ Erreur")

    def open_dashboard(self):
        try:
            dash = self.game_dir / "VIRTUAL_PLAYERS_DASHBOARD.html"
            webbrowser.open(str(dash))
            self.status.set("📊 Dashboard ouvert")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def open_docs(self):
        try:
            doc = self.game_dir / "README_VIRTUAL_PLAYERS.md"
            os.startfile(str(doc))
            self.status.set("📖 Docs ouverte")
        except:
            messagebox.showinfo("Info", "Fichier: README_VIRTUAL_PLAYERS.md")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SimpleLauncher()
    app.run()
