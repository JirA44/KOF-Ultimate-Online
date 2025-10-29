#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE ONLINE - LAUNCHER ULTIMATE
Lance tous les systèmes: Détection bugs, Serveur Battle.net, Client, Jeu
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import time
import os
import sys
from pathlib import Path
from datetime import datetime

class Colors:
    PRIMARY = "#00d4ff"
    SECONDARY = "#16213e"
    BACKGROUND = "#0a0e27"
    ACCENT = "#1e3a8a"
    SUCCESS = "#10b981"
    ERROR = "#ef4444"
    WARNING = "#f59e0b"
    INFO = "#3b82f6"


class ProcessManager:
    """Gestionnaire de processus"""

    def __init__(self):
        self.processes = {}

    def start(self, name, command, cwd=None):
        """Démarre un processus"""
        if name in self.processes and self.processes[name].poll() is None:
            return False, "Déjà en cours"

        try:
            process = subprocess.Popen(
                command,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
            )

            self.processes[name] = process
            return True, f"Démarré (PID: {process.pid})"

        except Exception as e:
            return False, str(e)

    def stop(self, name):
        """Arrête un processus"""
        if name not in self.processes:
            return False, "Processus non trouvé"

        process = self.processes[name]

        if process.poll() is not None:
            return False, "Déjà arrêté"

        try:
            process.terminate()
            process.wait(timeout=5)
            return True, "Arrêté"
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            return True, "Arrêté (forcé)"
        except Exception as e:
            return False, str(e)

    def is_running(self, name):
        """Vérifie si un processus est en cours"""
        if name not in self.processes:
            return False

        return self.processes[name].poll() is None

    def stop_all(self):
        """Arrête tous les processus"""
        for name in list(self.processes.keys()):
            self.stop(name)


class KOFUOLauncher:
    """Launcher principal pour KOF Ultimate Online"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KOF Ultimate Online - Launcher Ultimate")
        self.root.geometry("1200x800")
        self.root.configure(bg=Colors.BACKGROUND)

        self.game_dir = Path("D:/KOF Ultimate Online")
        self.process_manager = ProcessManager()

        self.create_ui()

        # Vérifier l'installation
        self.check_installation()

    def create_ui(self):
        """Crée l'interface utilisateur"""

        # Header
        header = tk.Frame(self.root, bg=Colors.SECONDARY, height=120)
        header.pack(fill="x")

        # Logo/Titre
        title_frame = tk.Frame(header, bg=Colors.SECONDARY)
        title_frame.pack(expand=True)

        title = tk.Label(
            title_frame,
            text="⚔️ KOF ULTIMATE ONLINE ⚔️",
            font=("Arial", 28, "bold"),
            bg=Colors.SECONDARY,
            fg=Colors.PRIMARY
        )
        title.pack()

        subtitle = tk.Label(
            title_frame,
            text="Launcher Ultimate - Système Complet",
            font=("Arial", 12),
            bg=Colors.SECONDARY,
            fg="white"
        )
        subtitle.pack()

        # Main container
        main = tk.Frame(self.root, bg=Colors.BACKGROUND)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Left panel - Actions rapides
        left = tk.Frame(main, bg=Colors.ACCENT, width=350)
        left.pack(side="left", fill="both", padx=(0, 10))
        left.pack_propagate(False)

        tk.Label(
            left,
            text="ACTIONS RAPIDES",
            font=("Arial", 14, "bold"),
            bg=Colors.ACCENT,
            fg="white"
        ).pack(pady=15)

        # Boutons d'actions
        self.create_action_button(
            left,
            "🎮 Lancer le Jeu (Solo)",
            self.launch_game,
            Colors.SUCCESS
        )

        self.create_action_button(
            left,
            "⚔️ Jouer en Ligne (Battle.net)",
            self.launch_online,
            Colors.PRIMARY
        )

        self.create_action_button(
            left,
            "🔍 Détecter les Bugs",
            self.launch_bug_detector,
            Colors.WARNING
        )

        self.create_action_button(
            left,
            "🖥️ Lancer Serveur Battle.net",
            self.launch_server,
            Colors.INFO
        )

        tk.Frame(left, bg=Colors.ACCENT, height=20).pack()

        # Séparateur
        tk.Label(
            left,
            text="OUTILS",
            font=("Arial", 12, "bold"),
            bg=Colors.ACCENT,
            fg="white"
        ).pack(pady=10)

        self.create_action_button(
            left,
            "📝 Optimiser Select.def",
            self.optimize_select_def,
            Colors.INFO
        )

        self.create_action_button(
            left,
            "📊 Voir les Rapports",
            self.view_reports,
            Colors.INFO
        )

        self.create_action_button(
            left,
            "⚙️ Configuration",
            self.open_config,
            Colors.ACCENT
        )

        # Bouton quitter en bas
        quit_frame = tk.Frame(left, bg=Colors.ACCENT)
        quit_frame.pack(side="bottom", pady=20)

        tk.Button(
            quit_frame,
            text="❌ Quitter et Tout Arrêter",
            font=("Arial", 11, "bold"),
            bg=Colors.ERROR,
            fg="white",
            command=self.quit_all,
            width=28,
            height=2
        ).pack()

        # Center/Right panel - Statut et logs
        right = tk.Frame(main, bg=Colors.ACCENT)
        right.pack(side="right", fill="both", expand=True)

        # Status panel
        status_header = tk.Frame(right, bg=Colors.SECONDARY)
        status_header.pack(fill="x", padx=2, pady=2)

        tk.Label(
            status_header,
            text="STATUT DES SERVICES",
            font=("Arial", 14, "bold"),
            bg=Colors.SECONDARY,
            fg="white"
        ).pack(pady=10)

        # Status indicators
        self.status_frame = tk.Frame(right, bg=Colors.ACCENT)
        self.status_frame.pack(fill="x", padx=10, pady=10)

        self.status_indicators = {}
        services = [
            ("Jeu", "game"),
            ("Serveur Battle.net", "server"),
            ("Client Battle.net", "client"),
            ("Détecteur de Bugs", "detector")
        ]

        for name, key in services:
            self.create_status_indicator(self.status_frame, name, key)

        # Log panel
        log_header = tk.Frame(right, bg=Colors.SECONDARY)
        log_header.pack(fill="x", padx=2, pady=2)

        tk.Label(
            log_header,
            text="JOURNAL D'ACTIVITÉ",
            font=("Arial", 12, "bold"),
            bg=Colors.SECONDARY,
            fg="white"
        ).pack(pady=8)

        # Log text
        log_frame = tk.Frame(right, bg=Colors.BACKGROUND)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Courier", 9),
            bg="#0a0a0a",
            fg="#00ff00",
            insertbackground="white",
            height=20
        )
        self.log_text.pack(fill="both", expand=True)

        # Log initial
        self.log("✅ Launcher Ultimate démarré")
        self.log(f"📁 Répertoire du jeu: {self.game_dir}")

    def create_action_button(self, parent, text, command, color):
        """Crée un bouton d'action"""
        btn = tk.Button(
            parent,
            text=text,
            font=("Arial", 11, "bold"),
            bg=color,
            fg="white",
            command=command,
            width=30,
            height=2,
            relief="raised",
            bd=2
        )
        btn.pack(pady=5, padx=10)

        # Hover effect
        def on_enter(e):
            btn.config(relief="sunken")

        def on_leave(e):
            btn.config(relief="raised")

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def create_status_indicator(self, parent, name, key):
        """Crée un indicateur de statut"""
        frame = tk.Frame(parent, bg=Colors.SECONDARY)
        frame.pack(fill="x", pady=5, padx=5)

        label = tk.Label(
            frame,
            text=name,
            font=("Arial", 10),
            bg=Colors.SECONDARY,
            fg="white",
            width=20,
            anchor="w"
        )
        label.pack(side="left", padx=10)

        status = tk.Label(
            frame,
            text="● Arrêté",
            font=("Arial", 10, "bold"),
            bg=Colors.SECONDARY,
            fg="#6b7280",
            width=15,
            anchor="w"
        )
        status.pack(side="left", padx=5)

        self.status_indicators[key] = status

        return frame

    def update_status(self, key, running):
        """Met à jour le statut d'un service"""
        if key in self.status_indicators:
            indicator = self.status_indicators[key]

            if running:
                indicator.config(text="● En cours", fg=Colors.SUCCESS)
            else:
                indicator.config(text="● Arrêté", fg="#6b7280")

    def log(self, message):
        """Ajoute un message au journal"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")

    def check_installation(self):
        """Vérifie l'installation"""
        self.log("🔍 Vérification de l'installation...")

        # Vérifier le répertoire du jeu
        if not self.game_dir.exists():
            self.log(f"❌ ERREUR: Répertoire non trouvé: {self.game_dir}")
            messagebox.showerror(
                "Erreur",
                f"Répertoire du jeu non trouvé:\n{self.game_dir}\n\n"
                f"Veuillez vérifier l'installation."
            )
            return

        # Vérifier les fichiers essentiels
        essential_files = [
            "KOF_Ultimate_Online.exe",
            "AUTO_BUG_DETECTOR.py",
            "BATTLENET_SERVER.py",
            "BATTLENET_CLIENT.py"
        ]

        missing = []
        for file in essential_files:
            if not (self.game_dir / file).exists():
                missing.append(file)

        if missing:
            self.log(f"⚠️ Fichiers manquants: {', '.join(missing)}")
        else:
            self.log("✅ Installation complète")

    def launch_game(self):
        """Lance le jeu en solo"""
        self.log("🎮 Lancement du jeu...")

        exe_path = self.game_dir / "KOF_Ultimate_Online.exe"

        if not exe_path.exists():
            self.log("❌ Exécutable du jeu non trouvé")
            messagebox.showerror("Erreur", "KOF_Ultimate_Online.exe non trouvé")
            return

        success, msg = self.process_manager.start(
            "game",
            [str(exe_path)],
            cwd=str(self.game_dir)
        )

        if success:
            self.log(f"✅ Jeu lancé: {msg}")
            self.update_status("game", True)

            # Vérifier le statut après 5 secondes
            threading.Timer(5.0, lambda: self.check_game_status()).start()
        else:
            self.log(f"❌ Erreur lancement jeu: {msg}")
            messagebox.showerror("Erreur", f"Impossible de lancer le jeu:\n{msg}")

    def check_game_status(self):
        """Vérifie si le jeu est toujours en cours"""
        if self.process_manager.is_running("game"):
            self.log("✅ Jeu en cours d'exécution")
        else:
            self.log("⚠️ Le jeu s'est arrêté")
            self.update_status("game", False)

    def launch_online(self):
        """Lance le client Battle.net"""
        self.log("⚔️ Lancement du client Battle.net...")

        python_path = sys.executable
        client_path = self.game_dir / "BATTLENET_CLIENT.py"

        if not client_path.exists():
            self.log("❌ Client Battle.net non trouvé")
            messagebox.showerror("Erreur", "BATTLENET_CLIENT.py non trouvé")
            return

        success, msg = self.process_manager.start(
            "client",
            [python_path, str(client_path)],
            cwd=str(self.game_dir)
        )

        if success:
            self.log(f"✅ Client lancé: {msg}")
            self.update_status("client", True)
        else:
            self.log(f"❌ Erreur lancement client: {msg}")
            messagebox.showerror("Erreur", f"Impossible de lancer le client:\n{msg}")

    def launch_server(self):
        """Lance le serveur Battle.net"""
        self.log("🖥️ Lancement du serveur Battle.net...")

        python_path = sys.executable
        server_path = self.game_dir / "BATTLENET_SERVER.py"

        if not server_path.exists():
            self.log("❌ Serveur Battle.net non trouvé")
            messagebox.showerror("Erreur", "BATTLENET_SERVER.py non trouvé")
            return

        success, msg = self.process_manager.start(
            "server",
            [python_path, str(server_path)],
            cwd=str(self.game_dir)
        )

        if success:
            self.log(f"✅ Serveur lancé: {msg}")
            self.log("🌐 Serveur accessible sur ws://localhost:8765")
            self.update_status("server", True)
        else:
            self.log(f"❌ Erreur lancement serveur: {msg}")
            messagebox.showerror("Erreur", f"Impossible de lancer le serveur:\n{msg}")

    def launch_bug_detector(self):
        """Lance le détecteur de bugs"""
        self.log("🔍 Lancement du détecteur de bugs...")

        python_path = sys.executable
        detector_path = self.game_dir / "AUTO_BUG_DETECTOR.py"

        if not detector_path.exists():
            self.log("❌ Détecteur de bugs non trouvé")
            messagebox.showerror("Erreur", "AUTO_BUG_DETECTOR.py non trouvé")
            return

        success, msg = self.process_manager.start(
            "detector",
            [python_path, str(detector_path)],
            cwd=str(self.game_dir)
        )

        if success:
            self.log(f"✅ Détecteur lancé: {msg}")
            self.log("⏳ Le scan peut prendre plusieurs minutes...")
            self.update_status("detector", True)
        else:
            self.log(f"❌ Erreur lancement détecteur: {msg}")
            messagebox.showerror("Erreur", f"Impossible de lancer le détecteur:\n{msg}")

    def optimize_select_def(self):
        """Optimise le select.def"""
        self.log("📝 Optimisation du select.def...")

        # Vérifier si un rapport existe
        report_file = self.game_dir / "bug_report.json"

        if not report_file.exists():
            messagebox.showinfo(
                "Information",
                "Aucun rapport de bugs trouvé.\n\n"
                "Veuillez d'abord lancer le Détecteur de Bugs."
            )
            return

        # Copier le select_optimal.def vers select.def
        select_optimal = self.game_dir / "data" / "select_optimal.def"
        select_def = self.game_dir / "data" / "select.def"

        if select_optimal.exists():
            try:
                import shutil
                shutil.copy(select_optimal, select_def)
                self.log("✅ select.def optimisé")
                messagebox.showinfo(
                    "Succès",
                    "Le fichier select.def a été optimisé avec les personnages stables."
                )
            except Exception as e:
                self.log(f"❌ Erreur: {e}")
                messagebox.showerror("Erreur", f"Impossible d'optimiser:\n{e}")
        else:
            messagebox.showinfo(
                "Information",
                "Aucun select_optimal.def trouvé.\n\n"
                "Veuillez d'abord lancer le Détecteur de Bugs."
            )

    def view_reports(self):
        """Ouvre les rapports"""
        self.log("📊 Ouverture des rapports...")

        # Chercher les rapports
        reports = list(self.game_dir.glob("*RAPPORT*.md"))

        if not reports:
            messagebox.showinfo("Information", "Aucun rapport trouvé")
            return

        # Ouvrir le dernier rapport
        latest = max(reports, key=lambda p: p.stat().st_mtime)

        try:
            os.startfile(str(latest))
            self.log(f"✅ Rapport ouvert: {latest.name}")
        except Exception as e:
            self.log(f"❌ Erreur: {e}")

    def open_config(self):
        """Ouvre la configuration"""
        messagebox.showinfo(
            "Configuration",
            "La configuration sera implémentée prochainement.\n\n"
            "Pour l'instant, modifiez directement:\n"
            "- data/mugen.cfg (config du jeu)\n"
            "- data/select.def (personnages)"
        )

    def quit_all(self):
        """Quitte et arrête tous les processus"""
        if messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment quitter et arrêter tous les services ?"
        ):
            self.log("🛑 Arrêt de tous les services...")

            self.process_manager.stop_all()

            self.log("👋 Au revoir !")

            time.sleep(1)
            self.root.quit()

    def run(self):
        """Lance l'interface"""
        self.root.protocol("WM_DELETE_WINDOW", self.quit_all)
        self.root.mainloop()


if __name__ == "__main__":
    launcher = KOFUOLauncher()
    launcher.run()
