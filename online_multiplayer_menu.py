"""
KOF Ultimate Online - Menu Multijoueur En Ligne
Système de matchmaking et recherche de parties
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
from pathlib import Path
from player_profile_system import PlayerProfileSystem
from matchmaking_client import MatchmakingClient


class OnlineMultiplayerMenu:
    """Menu multijoueur en ligne avec matchmaking"""

    def __init__(self, parent, profile_system, current_profile):
        self.parent = parent
        self.profile_system = profile_system
        self.current_profile = current_profile

        self.window = tk.Toplevel(parent)
        self.window.title("Multijoueur En Ligne")
        self.window.geometry("900x650")
        self.window.configure(bg="#1a1a2e")
        self.window.grab_set()

        self.searching = False
        self.search_thread = None

        # Client de matchmaking
        self.matchmaking_client = MatchmakingClient()
        self.matchmaking_client.on_match_found = self._on_match_found
        self.matchmaking_client.on_connected = self._on_server_connected
        self.matchmaking_client.on_disconnected = self._on_server_disconnected
        self.matchmaking_client.on_error = self._on_server_error

        self.create_ui()

        # Se connecter au serveur
        self._connect_to_server()

    def create_ui(self):
        """Crée l'interface du menu multijoueur"""

        # En-tête
        header = tk.Frame(self.window, bg="#16213e", height=80)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="MULTIJOUEUR EN LIGNE",
            font=("Arial", 20, "bold"),
            bg="#16213e",
            fg="#00d4ff"
        )
        title.pack(pady=25)

        # Corps principal
        main_frame = tk.Frame(self.window, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Panel gauche - Profil du joueur
        left_panel = tk.Frame(main_frame, bg="#0f3460", width=300)
        left_panel.pack(side="left", fill="both", padx=(0, 10))

        tk.Label(
            left_panel,
            text="VOTRE PROFIL",
            font=("Arial", 14, "bold"),
            bg="#0f3460",
            fg="#ffffff"
        ).pack(pady=10)

        # Carte de profil
        profile_card = tk.Frame(left_panel, bg="#16213e")
        profile_card.pack(padx=10, pady=10, fill="both", expand=True)

        # Nom du joueur
        tk.Label(
            profile_card,
            text=self.current_profile["username"],
            font=("Arial", 16, "bold"),
            bg="#16213e",
            fg="#00d4ff"
        ).pack(pady=15)

        # Stats du joueur
        stats = self.current_profile["stats"]

        stats_frame = tk.Frame(profile_card, bg="#16213e")
        stats_frame.pack(pady=10)

        self._add_stat_row(stats_frame, "Niveau:", f"{stats['level']}")
        self._add_stat_row(stats_frame, "Ranking:", f"{stats['ranking_points']} pts")
        self._add_stat_row(stats_frame, "Victoires:", f"{stats['wins']}")
        self._add_stat_row(stats_frame, "Défaites:", f"{stats['losses']}")
        self._add_stat_row(stats_frame, "Win Rate:", f"{stats['win_rate']:.1f}%")

        # Statut de connexion
        status_frame = tk.Frame(left_panel, bg="#0f3460")
        status_frame.pack(pady=10)

        tk.Label(
            status_frame,
            text="● En ligne",
            font=("Arial", 11),
            bg="#0f3460",
            fg="#00ff00"
        ).pack()

        # Panel droit - Matchmaking
        right_panel = tk.Frame(main_frame, bg="#0f3460")
        right_panel.pack(side="right", fill="both", expand=True)

        tk.Label(
            right_panel,
            text="RECHERCHE DE PARTIE",
            font=("Arial", 14, "bold"),
            bg="#0f3460",
            fg="#ffffff"
        ).pack(pady=10)

        # Zone de recherche
        search_frame = tk.Frame(right_panel, bg="#16213e")
        search_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Mode de jeu
        mode_frame = tk.Frame(search_frame, bg="#16213e")
        mode_frame.pack(pady=20)

        tk.Label(
            mode_frame,
            text="Mode de jeu:",
            font=("Arial", 12),
            bg="#16213e",
            fg="#ffffff"
        ).pack(pady=5)

        self.mode_var = tk.StringVar(value="ranked")

        modes = [
            ("Ranked (Classé)", "ranked"),
            ("Quick Match (Rapide)", "quick"),
            ("Custom Lobby (Perso)", "custom")
        ]

        for text, value in modes:
            rb = tk.Radiobutton(
                mode_frame,
                text=text,
                variable=self.mode_var,
                value=value,
                bg="#16213e",
                fg="#ffffff",
                selectcolor="#0f3460",
                activebackground="#16213e",
                activeforeground="#00d4ff",
                font=("Arial", 11)
            )
            rb.pack(anchor="w", padx=20)

        # Bouton de recherche
        self.btn_search = self._create_button(
            search_frame,
            "RECHERCHER UNE PARTIE",
            self.start_search,
            width=25,
            height=2,
            font=("Arial", 12, "bold")
        )
        self.btn_search.pack(pady=20)

        # Zone d'état de recherche
        self.search_status_frame = tk.Frame(search_frame, bg="#16213e")
        self.search_status_frame.pack(pady=10, fill="both", expand=True)

        self.status_label = tk.Label(
            self.search_status_frame,
            text="En attente...",
            font=("Arial", 11),
            bg="#16213e",
            fg="#888888"
        )
        self.status_label.pack(pady=10)

        # Barre de progression (cachée au début)
        self.progress = ttk.Progressbar(
            self.search_status_frame,
            mode='indeterminate',
            length=300
        )

        # Liste des joueurs en ligne (simulée)
        online_frame = tk.Frame(search_frame, bg="#16213e")
        online_frame.pack(pady=10, fill="both", expand=True)

        tk.Label(
            online_frame,
            text="Joueurs en ligne: 127",
            font=("Arial", 10),
            bg="#16213e",
            fg="#00d4ff"
        ).pack()

    def _add_stat_row(self, parent, label, value):
        """Ajoute une ligne de statistique"""
        row = tk.Frame(parent, bg="#16213e")
        row.pack(fill="x", pady=3)

        tk.Label(
            row,
            text=label,
            font=("Arial", 11),
            bg="#16213e",
            fg="#888888",
            width=12,
            anchor="w"
        ).pack(side="left", padx=10)

        tk.Label(
            row,
            text=value,
            font=("Arial", 11, "bold"),
            bg="#16213e",
            fg="#ffffff",
            anchor="e"
        ).pack(side="right", padx=10)

    def _create_button(self, parent, text, command, width=10, height=1, font=("Arial", 10)):
        """Crée un bouton stylisé"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg="#00d4ff",
            fg="#000000",
            font=font,
            width=width,
            height=height,
            relief="flat",
            cursor="hand2"
        )
        return btn

    def start_search(self):
        """Démarre la recherche de partie"""
        if self.searching:
            self.stop_search()
            return

        # Vérifier la connexion au serveur
        if not self.matchmaking_client.connected:
            messagebox.showerror(
                "Erreur",
                "Non connecté au serveur!\n\nLancez d'abord le serveur de matchmaking:\npython matchmaking_server.py"
            )
            return

        self.searching = True
        self.btn_search.config(
            text="ANNULER LA RECHERCHE",
            bg="#ff4444"
        )

        # Afficher la barre de progression
        self.progress.pack(pady=10)
        self.progress.start(10)

        mode = self.mode_var.get()
        mode_text = {
            "ranked": "Classé",
            "quick": "Rapide",
            "custom": "Personnalisé"
        }[mode]

        self.status_label.config(
            text=f"Recherche d'adversaires ({mode_text})...",
            fg="#00d4ff"
        )

        # Lancer la recherche sur le serveur
        success = self.matchmaking_client.search_match(mode)

        if not success:
            self.stop_search()
            messagebox.showerror("Erreur", "Impossible de lancer la recherche")

    def stop_search(self):
        """Arrête la recherche"""
        self.searching = False
        self.progress.stop()
        self.progress.pack_forget()

        self.btn_search.config(
            text="RECHERCHER UNE PARTIE",
            bg="#00d4ff"
        )

        self.status_label.config(
            text="Recherche annulée",
            fg="#ff8800"
        )

        # Annuler sur le serveur
        if self.matchmaking_client.connected:
            self.matchmaking_client.cancel_search()

    def _connect_to_server(self):
        """Se connecte au serveur de matchmaking"""
        # Lancer la connexion dans un thread pour ne pas bloquer l'UI
        connection_thread = threading.Thread(target=self._do_connect, daemon=True)
        connection_thread.start()

    def _do_connect(self):
        """Effectue la connexion au serveur"""
        success = self.matchmaking_client.connect(
            self.current_profile["username"],
            self.current_profile
        )

        if not success:
            # Afficher erreur dans l'UI
            self.window.after(0, lambda: self.status_label.config(
                text="⚠️ Serveur inaccessible (mode hors ligne)",
                fg="#ff8800"
            ))

    def _on_server_connected(self, response):
        """Callback quand connecté au serveur"""
        self.window.after(0, lambda: self.status_label.config(
            text="✓ Connecté au serveur",
            fg="#00ff00"
        ))

        # Mettre à jour le compteur de joueurs en ligne
        stats = response.get("server_stats", {})
        players_online = stats.get("players_online", 0)

        # Trouver et mettre à jour le label des joueurs en ligne
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for label in child.winfo_children():
                            if isinstance(label, tk.Label) and "Joueurs en ligne" in label.cget("text"):
                                label.config(text=f"Joueurs en ligne: {players_online}")

    def _on_server_disconnected(self):
        """Callback quand déconnecté du serveur"""
        self.window.after(0, lambda: self.status_label.config(
            text="⚠️ Déconnecté du serveur",
            fg="#ff8800"
        ))

    def _on_server_error(self, error):
        """Callback en cas d'erreur serveur"""
        self.window.after(0, lambda: messagebox.showerror(
            "Erreur Serveur",
            f"Erreur de connexion:\n{error}\n\nLancez le serveur avec:\npython matchmaking_server.py"
        ))

    def _on_match_found(self, match_data):
        """Callback quand un match est trouvé"""
        self.searching = False

        # Mettre à jour l'UI dans le thread principal
        self.window.after(0, lambda: self._handle_match_found(match_data))

    def _handle_match_found(self, match_data):
        """Gère l'affichage du match trouvé"""
        self.progress.stop()
        self.progress.pack_forget()

        opponent = match_data.get("opponent", {})
        opponent_name = opponent.get("username", "Unknown")
        opponent_mmr = opponent.get("mmr", 0)

        self.status_label.config(
            text=f"Match trouvé contre {opponent_name} ({opponent_mmr} pts)!",
            fg="#00ff00"
        )

        self.btn_search.config(
            text="RECHERCHER UNE PARTIE",
            bg="#00d4ff"
        )

        # Dialog de confirmation
        self.window.after(500, lambda: self._show_match_dialog(opponent_name, opponent_mmr))

    def _show_match_dialog(self, opponent, opponent_rank):
        """Affiche le dialog de confirmation de match"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Match Trouvé!")
        dialog.geometry("400x300")
        dialog.configure(bg="#1a1a2e")
        dialog.grab_set()

        tk.Label(
            dialog,
            text="MATCH TROUVÉ!",
            font=("Arial", 16, "bold"),
            bg="#1a1a2e",
            fg="#00ff00"
        ).pack(pady=20)

        # Info adversaire
        info_frame = tk.Frame(dialog, bg="#16213e")
        info_frame.pack(pady=10, padx=20, fill="both")

        tk.Label(
            info_frame,
            text="Adversaire:",
            font=("Arial", 12),
            bg="#16213e",
            fg="#888888"
        ).pack(pady=5)

        tk.Label(
            info_frame,
            text=opponent,
            font=("Arial", 14, "bold"),
            bg="#16213e",
            fg="#00d4ff"
        ).pack(pady=5)

        tk.Label(
            info_frame,
            text=f"Ranking: {opponent_rank} pts",
            font=("Arial", 11),
            bg="#16213e",
            fg="#ffffff"
        ).pack(pady=5)

        # Boutons
        btn_frame = tk.Frame(dialog, bg="#1a1a2e")
        btn_frame.pack(pady=20)

        self._create_button(
            btn_frame,
            "ACCEPTER",
            lambda: self._accept_match(dialog, opponent),
            width=12,
            height=2
        ).pack(side="left", padx=10)

        self._create_button(
            btn_frame,
            "REFUSER",
            dialog.destroy,
            width=12,
            height=2
        ).pack(side="left", padx=10)

        # Timer de 10 secondes
        self._match_timer(dialog, 10)

    def _match_timer(self, dialog, seconds):
        """Timer pour accepter le match"""
        if seconds > 0 and dialog.winfo_exists():
            dialog.title(f"Match Trouvé! ({seconds}s)")
            dialog.after(1000, lambda: self._match_timer(dialog, seconds - 1))
        elif dialog.winfo_exists():
            messagebox.showwarning("Temps écoulé", "Vous n'avez pas accepté le match à temps.")
            dialog.destroy()

    def _accept_match(self, dialog, opponent):
        """Accepte le match et lance le jeu"""
        dialog.destroy()

        messagebox.showinfo(
            "Match Accepté",
            f"Lancement du match contre {opponent}...\n\nBonne chance!"
        )

        # Ici on pourrait lancer le jeu avec les paramètres du match
        # Pour l'instant, on ferme juste le menu
        self.window.destroy()


def show_online_menu(parent, profile_system, current_profile):
    """Fonction helper pour afficher le menu multijoueur"""
    OnlineMultiplayerMenu(parent, profile_system, current_profile)


if __name__ == "__main__":
    # Test standalone
    root = tk.Tk()
    root.withdraw()

    # Créer un profil de test
    system = PlayerProfileSystem()

    test_profile = {
        "username": "TestPlayer",
        "stats": {
            "level": 5,
            "ranking_points": 1050,
            "wins": 15,
            "losses": 10,
            "win_rate": 60.0
        }
    }

    menu = OnlineMultiplayerMenu(root, system, test_profile)
    root.mainloop()
