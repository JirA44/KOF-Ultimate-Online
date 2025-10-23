#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LAUNCHER AVEC MANETTE VIRTUELLE
N'utilise PAS votre clavier !
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import webbrowser
from pathlib import Path

try:
    import vgamepad
    GAMEPAD_OK = True
except ImportError:
    GAMEPAD_OK = False

class GamepadLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎮 Joueurs Virtuels (Manette)")
        self.root.geometry("500x550")
        self.root.resizable(False, False)

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
        ).pack(pady=15)

        tk.Label(
            self.root,
            text="Avec Manette Virtuelle",
            font=("Arial", 12),
            bg=self.bg,
            fg="#4caf50"
        ).pack()

        # Info importante
        info_frame = tk.Frame(self.root, bg="#2d2d44", relief="solid", bd=2)
        info_frame.pack(pady=15, padx=30, fill="x")

        tk.Label(
            info_frame,
            text="✅ N'utilise PAS votre clavier !",
            font=("Arial", 11, "bold"),
            bg="#2d2d44",
            fg="#4caf50"
        ).pack(pady=5)

        tk.Label(
            info_frame,
            text="Vous pouvez taper librement",
            font=("Arial", 9),
            bg="#2d2d44",
            fg=self.fg
        ).pack(pady=5)

        # Status vgamepad
        if not GAMEPAD_OK:
            warn_frame = tk.Frame(self.root, bg="#ff5722", relief="solid", bd=2)
            warn_frame.pack(pady=10, padx=30, fill="x")

            tk.Label(
                warn_frame,
                text="⚠️  Manette virtuelle non installée !",
                font=("Arial", 10, "bold"),
                bg="#ff5722",
                fg="white"
            ).pack(pady=5)

            tk.Button(
                warn_frame,
                text="📥 Installer Maintenant",
                command=self.install_gamepad,
                bg="#ffc107",
                fg="black",
                font=("Arial", 9, "bold"),
                cursor="hand2"
            ).pack(pady=5)

        # Options
        tk.Frame(self.root, height=2, bg=self.accent).pack(fill="x", padx=50, pady=15)

        opt_frame = tk.Frame(self.root, bg=self.bg)
        opt_frame.pack(pady=15)

        tk.Label(
            opt_frame,
            text="Nombre de joueurs:",
            font=("Arial", 11),
            bg=self.bg,
            fg=self.fg
        ).grid(row=0, column=0, sticky="e", padx=10, pady=10)

        self.num_var = tk.StringVar(value="3")
        ttk.Combobox(
            opt_frame,
            textvariable=self.num_var,
            values=["1", "2", "3", "5"],
            state="readonly",
            width=8
        ).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(
            opt_frame,
            text="Durée (minutes):",
            font=("Arial", 11),
            bg=self.bg,
            fg=self.fg
        ).grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.dur_var = tk.StringVar(value="120")
        ttk.Combobox(
            opt_frame,
            textvariable=self.dur_var,
            values=["30", "60", "120", "240", "999"],
            state="readonly",
            width=8
        ).grid(row=1, column=1, padx=10, pady=10)

        self.dash_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            opt_frame,
            text="Ouvrir dashboard",
            variable=self.dash_var,
            font=("Arial", 10),
            bg=self.bg,
            fg=self.fg,
            selectcolor="#2d2d44",
            activebackground=self.bg
        ).grid(row=2, column=0, columnspan=2, pady=10)

        # Boutons
        btn_frame = tk.Frame(self.root, bg=self.bg)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="▶️  LANCER",
            command=self.launch,
            font=("Arial", 14, "bold"),
            bg="#4caf50",
            fg="white",
            padx=40,
            pady=15,
            relief="raised",
            bd=3,
            cursor="hand2",
            state="normal" if GAMEPAD_OK else "disabled"
        ).pack(pady=10)

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

        # Status
        self.status = tk.StringVar(value="Prêt" if GAMEPAD_OK else "Installer vgamepad d'abord")
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

    def install_gamepad(self):
        """Lance l'installation de vgamepad"""
        try:
            install_script = self.game_dir / "INSTALL_MANETTE_VIRTUELLE.bat"
            subprocess.Popen([str(install_script)])
            messagebox.showinfo(
                "Installation",
                "📥 Installation lancée!\n\n"
                "Relancez ce launcher après l'installation."
            )
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def launch(self):
        if not GAMEPAD_OK:
            messagebox.showerror(
                "Erreur",
                "Installez vgamepad d'abord!\n\n"
                "Cliquez sur le bouton d'installation."
            )
            return

        num = int(self.num_var.get())
        dur = int(self.dur_var.get())

        # IMPORTANT: Configurer le jeu pour manette
        confirm = messagebox.askyesno(
            "Configuration",
            f"⚠️  IMPORTANT:\n\n"
            f"1. Lancez le jeu\n"
            f"2. Allez dans OPTIONS > CONTROLS\n"
            f"3. Configurez Player 1 en MANETTE\n"
            f"4. Le jeu doit être au menu principal\n\n"
            f"Configuration:\n"
            f"• {num} joueur(s)\n"
            f"• {dur} minutes\n\n"
            f"Prêt ?"
        )

        if not confirm:
            return

        try:
            pythonw = sys.executable.replace("python.exe", "pythonw.exe")
            backend = self.game_dir / "VIRTUAL_PLAYER_GAMEPAD.pyw"

            for i in range(1, num + 1):
                subprocess.Popen(
                    [pythonw, str(backend), str(i), str(dur), str(self.game_dir)],
                    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
                )

            self.status.set(f"✅ {num} joueurs lancés (manette virtuelle)")

            if self.dash_var.get():
                self.open_dashboard()

            messagebox.showinfo(
                "Succès",
                f"✅ {num} joueur(s) lancé(s)!\n\n"
                f"Ils utilisent une MANETTE VIRTUELLE.\n"
                f"Votre clavier est libre !\n\n"
                f"Durée: {dur} min"
            )

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def open_dashboard(self):
        try:
            dash = self.game_dir / "VIRTUAL_PLAYERS_DASHBOARD.html"
            webbrowser.open(str(dash))
            self.status.set("📊 Dashboard ouvert")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GamepadLauncher()
    app.run()
