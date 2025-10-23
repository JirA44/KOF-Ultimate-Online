#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE ONLINE - BATTLE.NET INTERFACE
Interface complète type Battle.net de Warcraft 3
Avec lobbies, chat, ladder, rooms
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import socket
import json
from datetime import datetime
from pathlib import Path
import subprocess
import sys

class BattleNetInterface:
    """Interface Battle.net complète pour KOF Ultimate Online"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KOF Ultimate Online - Battle.net")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        # Connexion au serveur
        self.server_socket = None
        self.connected = False
        self.username = ""
        self.player_data = {}

        # Données en temps réel
        self.online_players = []
        self.open_games = []
        self.ladder_data = []
        self.chat_messages = []

        # Couleurs Battle.net
        self.bg_color = "#0a0a1a"
        self.panel_color = "#151530"
        self.accent_color = "#2d5ca8"
        self.text_color = "#e0e0e0"
        self.gold_color = "#ffd700"

        self.setup_ui()

    def setup_ui(self):
        """Configure l'interface Battle.net"""
        self.root.configure(bg=self.bg_color)

        # =============================================================
        # HEADER - Logo et status
        # =============================================================
        header_frame = tk.Frame(self.root, bg=self.accent_color, height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Logo
        logo_label = tk.Label(
            header_frame,
            text="⚔️ KOF ULTIMATE ONLINE",
            font=("Arial", 24, "bold"),
            bg=self.accent_color,
            fg="white"
        )
        logo_label.pack(side=tk.LEFT, padx=20, pady=20)

        # Status serveur
        self.status_label = tk.Label(
            header_frame,
            text="● Déconnecté",
            font=("Arial", 12),
            bg=self.accent_color,
            fg="#ff4444"
        )
        self.status_label.pack(side=tk.RIGHT, padx=20)

        # Nom du joueur
        self.player_label = tk.Label(
            header_frame,
            text="",
            font=("Arial", 14, "bold"),
            bg=self.accent_color,
            fg=self.gold_color
        )
        self.player_label.pack(side=tk.RIGHT, padx=20)

        # =============================================================
        # MAIN CONTAINER - 3 colonnes style Battle.net
        # =============================================================
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configure grid
        main_container.grid_columnconfigure(0, weight=1)  # Gauche
        main_container.grid_columnconfigure(1, weight=2)  # Centre
        main_container.grid_columnconfigure(2, weight=1)  # Droite
        main_container.grid_rowconfigure(0, weight=1)

        # =============================================================
        # COLONNE GAUCHE - Joueurs en ligne + Ladder
        # =============================================================
        left_frame = tk.Frame(main_container, bg=self.panel_color)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Titre Joueurs en ligne
        players_title = tk.Label(
            left_frame,
            text="👥 JOUEURS EN LIGNE",
            font=("Arial", 12, "bold"),
            bg=self.panel_color,
            fg=self.gold_color
        )
        players_title.pack(fill=tk.X, pady=5)

        # Liste des joueurs
        players_frame = tk.Frame(left_frame, bg=self.panel_color)
        players_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.players_listbox = tk.Listbox(
            players_frame,
            bg="#0f0f20",
            fg=self.text_color,
            font=("Consolas", 10),
            selectbackground=self.accent_color,
            borderwidth=0,
            highlightthickness=0
        )
        self.players_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        players_scroll = ttk.Scrollbar(players_frame, command=self.players_listbox.yview)
        players_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.players_listbox.config(yscrollcommand=players_scroll.set)

        # Boutons actions joueurs
        players_actions = tk.Frame(left_frame, bg=self.panel_color)
        players_actions.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(
            players_actions,
            text="Inviter à jouer",
            command=self.invite_player,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 9),
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            players_actions,
            text="Voir profil",
            command=self.view_profile,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 9),
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=2)

        # Séparateur
        tk.Frame(left_frame, bg=self.accent_color, height=2).pack(fill=tk.X, pady=10)

        # Ladder
        ladder_title = tk.Label(
            left_frame,
            text="🏆 CLASSEMENT",
            font=("Arial", 12, "bold"),
            bg=self.panel_color,
            fg=self.gold_color
        )
        ladder_title.pack(fill=tk.X, pady=5)

        ladder_frame = tk.Frame(left_frame, bg=self.panel_color)
        ladder_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.ladder_listbox = tk.Listbox(
            ladder_frame,
            bg="#0f0f20",
            fg=self.text_color,
            font=("Consolas", 10),
            selectbackground=self.accent_color,
            borderwidth=0,
            highlightthickness=0
        )
        self.ladder_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ladder_scroll = ttk.Scrollbar(ladder_frame, command=self.ladder_listbox.yview)
        ladder_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.ladder_listbox.config(yscrollcommand=ladder_scroll.set)

        # =============================================================
        # COLONNE CENTRE - Liste des parties + Création
        # =============================================================
        center_frame = tk.Frame(main_container, bg=self.panel_color)
        center_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Titre
        games_title = tk.Label(
            center_frame,
            text="🎮 PARTIES DISPONIBLES",
            font=("Arial", 14, "bold"),
            bg=self.panel_color,
            fg=self.gold_color
        )
        games_title.pack(fill=tk.X, pady=10)

        # Boutons de filtrage
        filter_frame = tk.Frame(center_frame, bg=self.panel_color)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            filter_frame,
            text="Mode:",
            bg=self.panel_color,
            fg=self.text_color,
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)

        self.filter_mode = tk.StringVar(value="Tous")
        for mode in ["Tous", "Classé", "Rapide", "Custom"]:
            tk.Radiobutton(
                filter_frame,
                text=mode,
                variable=self.filter_mode,
                value=mode,
                bg=self.panel_color,
                fg=self.text_color,
                selectcolor=self.accent_color,
                font=("Arial", 9),
                command=self.refresh_games_list
            ).pack(side=tk.LEFT, padx=5)

        # Liste des parties
        games_frame = tk.Frame(center_frame, bg=self.panel_color)
        games_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Table style Battle.net
        columns = ("Nom", "Hôte", "Mode", "MMR", "Statut")
        self.games_tree = ttk.Treeview(games_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.games_tree.heading(col, text=col)
            self.games_tree.column(col, width=100 if col != "Nom" else 200)

        self.games_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        games_scroll = ttk.Scrollbar(games_frame, command=self.games_tree.yview)
        games_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.games_tree.config(yscrollcommand=games_scroll.set)

        # Boutons de contrôle
        control_frame = tk.Frame(center_frame, bg=self.panel_color)
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(
            control_frame,
            text="⚔️ CRÉER UNE PARTIE",
            command=self.create_game,
            bg="#2a7f2a",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            control_frame,
            text="🎯 REJOINDRE",
            command=self.join_game,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            control_frame,
            text="🔄 RECHERCHE AUTO",
            command=self.quick_match,
            bg="#d97706",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)

        # =============================================================
        # COLONNE DROITE - Chat + Infos
        # =============================================================
        right_frame = tk.Frame(main_container, bg=self.panel_color)
        right_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        # Titre Chat
        chat_title = tk.Label(
            right_frame,
            text="💬 CHAT GÉNÉRAL",
            font=("Arial", 12, "bold"),
            bg=self.panel_color,
            fg=self.gold_color
        )
        chat_title.pack(fill=tk.X, pady=5)

        # Zone de chat
        self.chat_display = scrolledtext.ScrolledText(
            right_frame,
            bg="#0f0f20",
            fg=self.text_color,
            font=("Consolas", 9),
            wrap=tk.WORD,
            borderwidth=0,
            highlightthickness=0,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Tag colors pour le chat
        self.chat_display.tag_config("system", foreground="#888888", font=("Consolas", 9, "italic"))
        self.chat_display.tag_config("username", foreground=self.gold_color, font=("Consolas", 9, "bold"))
        self.chat_display.tag_config("message", foreground=self.text_color)
        self.chat_display.tag_config("timestamp", foreground="#666666", font=("Consolas", 8))

        # Input chat
        chat_input_frame = tk.Frame(right_frame, bg=self.panel_color)
        chat_input_frame.pack(fill=tk.X, padx=5, pady=5)

        self.chat_input = tk.Entry(
            chat_input_frame,
            bg="#0f0f20",
            fg=self.text_color,
            font=("Arial", 10),
            insertbackground=self.text_color,
            borderwidth=1,
            relief=tk.SOLID
        )
        self.chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.chat_input.bind("<Return>", lambda e: self.send_chat_message())

        tk.Button(
            chat_input_frame,
            text="Envoyer",
            command=self.send_chat_message,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.RIGHT)

        # Séparateur
        tk.Frame(right_frame, bg=self.accent_color, height=2).pack(fill=tk.X, pady=10)

        # Infos profil
        profile_title = tk.Label(
            right_frame,
            text="📊 MON PROFIL",
            font=("Arial", 12, "bold"),
            bg=self.panel_color,
            fg=self.gold_color
        )
        profile_title.pack(fill=tk.X, pady=5)

        self.profile_info = tk.Text(
            right_frame,
            bg="#0f0f20",
            fg=self.text_color,
            font=("Consolas", 9),
            height=10,
            borderwidth=0,
            highlightthickness=0,
            state=tk.DISABLED
        )
        self.profile_info.pack(fill=tk.X, padx=5, pady=5)

        # =============================================================
        # BOTTOM BAR - Actions rapides
        # =============================================================
        bottom_frame = tk.Frame(self.root, bg=self.panel_color, height=50)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)
        bottom_frame.pack_propagate(False)

        tk.Button(
            bottom_frame,
            text="⚙️ Paramètres",
            command=self.open_settings,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Button(
            bottom_frame,
            text="📖 Aide",
            command=self.open_help,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Button(
            bottom_frame,
            text="🚪 Déconnexion",
            command=self.disconnect,
            bg="#b91c1c",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.RIGHT, padx=10, pady=10)

    def add_chat_message(self, username, message, msg_type="normal"):
        """Ajoute un message au chat"""
        self.chat_display.config(state=tk.NORMAL)

        timestamp = datetime.now().strftime("%H:%M")

        if msg_type == "system":
            self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
            self.chat_display.insert(tk.END, f"● {message}\n", "system")
        else:
            self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
            self.chat_display.insert(tk.END, f"{username}: ", "username")
            self.chat_display.insert(tk.END, f"{message}\n", "message")

        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def send_chat_message(self):
        """Envoie un message dans le chat"""
        message = self.chat_input.get().strip()
        if not message:
            return

        if not self.connected:
            messagebox.showwarning("Non connecté", "Vous devez être connecté au serveur pour chatter.")
            return

        # TODO: Envoyer au serveur
        self.add_chat_message(self.username, message)
        self.chat_input.delete(0, tk.END)

    def update_profile_display(self):
        """Met à jour l'affichage du profil"""
        self.profile_info.config(state=tk.NORMAL)
        self.profile_info.delete(1.0, tk.END)

        if self.player_data:
            stats = self.player_data.get('stats', {})
            info = f"""
Niveau: {stats.get('level', 1)}
MMR: {stats.get('ranking_points', 1000)}

Parties jouées: {stats.get('total_matches', 0)}
Victoires: {stats.get('wins', 0)}
Défaites: {stats.get('losses', 0)}
Ratio: {stats.get('win_rate', 0):.1f}%

Temps de jeu: {stats.get('total_playtime_minutes', 0)} min
Personnage favori: {stats.get('favorite_character', 'N/A')}
"""
            self.profile_info.insert(1.0, info)

        self.profile_info.config(state=tk.DISABLED)

    def create_game(self):
        """Ouvre la fenêtre de création de partie"""
        # TODO: Implémenter dialog de création
        messagebox.showinfo("Créer une partie", "Fonctionnalité à implémenter:\n- Choix du nom\n- Mode de jeu\n- Paramètres")

    def join_game(self):
        """Rejoint la partie sélectionnée"""
        selection = self.games_tree.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une partie à rejoindre.")
            return

        # TODO: Rejoindre la partie
        messagebox.showinfo("Rejoindre", "Connexion à la partie...")

    def quick_match(self):
        """Lance une recherche automatique"""
        if not self.connected:
            messagebox.showwarning("Non connecté", "Connectez-vous d'abord au serveur.")
            return

        # TODO: Lancer recherche
        messagebox.showinfo("Recherche", "Recherche d'un adversaire en cours...")

    def invite_player(self):
        """Invite un joueur sélectionné"""
        # TODO: Implémenter
        pass

    def view_profile(self):
        """Affiche le profil d'un joueur"""
        # TODO: Implémenter
        pass

    def refresh_games_list(self):
        """Rafraîchit la liste des parties"""
        # TODO: Récupérer du serveur
        pass

    def open_settings(self):
        """Ouvre les paramètres"""
        # TODO: Implémenter
        messagebox.showinfo("Paramètres", "Fenêtre de paramètres à implémenter")

    def open_help(self):
        """Ouvre l'aide"""
        messagebox.showinfo("Aide", "Documentation KOF Ultimate Online\n\nConsultez le README pour plus d'infos.")

    def disconnect(self):
        """Déconnexion du serveur"""
        if messagebox.askyesno("Déconnexion", "Voulez-vous vraiment vous déconnecter ?"):
            self.root.quit()

    def run(self):
        """Lance l'interface"""
        # Message de bienvenue
        self.add_chat_message("", "Bienvenue sur KOF Ultimate Online!", "system")
        self.add_chat_message("", "Connectez-vous pour commencer à jouer.", "system")

        self.root.mainloop()


if __name__ == "__main__":
    app = BattleNetInterface()
    app.run()
