#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE ONLINE - Client Matchmaking Style Battle.net
Client pour se connecter au serveur et jouer en ligne
"""

import asyncio
import json
import time
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading
import websockets
from pathlib import Path

class Colors:
    PRIMARY = "#00d4ff"
    SECONDARY = "#16213e"
    BACKGROUND = "#1a1a2e"
    ACCENT = "#0f3460"
    SUCCESS = "#00ff88"
    ERROR = "#ff0055"
    WARNING = "#ffaa00"


class BattleNetClient:
    """Client pour se connecter au serveur Battle.net"""

    def __init__(self, server_url: str = "ws://localhost:8765"):
        self.server_url = server_url
        self.websocket = None
        self.connected = False
        self.player_data = None
        self.current_match = None

        # Callbacks
        self.on_connected = None
        self.on_disconnected = None
        self.on_match_found = None
        self.on_match_finished = None
        self.on_server_stats = None
        self.on_leaderboard = None
        self.on_error = None

        # Task
        self.receive_task = None

    async def connect(self, username: str, player_data: dict = None):
        """Se connecte au serveur"""
        try:
            self.websocket = await websockets.connect(self.server_url)

            # Envoyer l'authentification
            auth_data = {
                "type": "auth",
                "username": username,
                "player_id": player_data.get("id") if player_data else None,
                "elo": player_data.get("elo", 1000) if player_data else 1000,
                "wins": player_data.get("wins", 0) if player_data else 0,
                "losses": player_data.get("losses", 0) if player_data else 0
            }

            await self.websocket.send(json.dumps(auth_data))

            # Attendre la confirmation
            response = await self.websocket.recv()
            data = json.loads(response)

            if data.get("type") == "auth_success":
                self.connected = True
                self.player_data = data.get("player")

                # Démarrer la réception des messages
                self.receive_task = asyncio.create_task(self._receive_messages())

                if self.on_connected:
                    self.on_connected(self.player_data)

                return True
            else:
                if self.on_error:
                    self.on_error(data.get("message", "Authentication failed"))
                return False

        except Exception as e:
            if self.on_error:
                self.on_error(f"Connection failed: {e}")
            return False

    async def disconnect(self):
        """Se déconnecte du serveur"""
        if self.websocket:
            await self.websocket.close()
            self.connected = False

            if self.on_disconnected:
                self.on_disconnected()

    async def search_match(self):
        """Commence la recherche d'adversaire"""
        if not self.connected:
            return False

        await self.websocket.send(json.dumps({
            "type": "search_match"
        }))
        return True

    async def cancel_search(self):
        """Annule la recherche"""
        if not self.connected:
            return False

        await self.websocket.send(json.dumps({
            "type": "cancel_search"
        }))
        return True

    async def report_match_result(self, winner_id: str):
        """Rapporte le résultat d'une partie"""
        if not self.connected:
            return False

        await self.websocket.send(json.dumps({
            "type": "match_result",
            "winner_id": winner_id
        }))
        return True

    async def get_leaderboard(self):
        """Demande le classement"""
        if not self.connected:
            return False

        await self.websocket.send(json.dumps({
            "type": "get_leaderboard"
        }))
        return True

    async def get_online_players(self):
        """Demande la liste des joueurs en ligne"""
        if not self.connected:
            return False

        await self.websocket.send(json.dumps({
            "type": "get_online_players"
        }))
        return True

    async def _receive_messages(self):
        """Reçoit les messages du serveur"""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                await self._handle_message(data)

        except websockets.exceptions.ConnectionClosed:
            self.connected = False
            if self.on_disconnected:
                self.on_disconnected()
        except Exception as e:
            if self.on_error:
                self.on_error(f"Receive error: {e}")

    async def _handle_message(self, data: dict):
        """Traite un message du serveur"""
        msg_type = data.get("type")

        if msg_type == "match_found":
            self.current_match = data.get("match")
            if self.on_match_found:
                self.on_match_found(data)

        elif msg_type == "match_finished":
            self.current_match = None
            if self.on_match_finished:
                self.on_match_finished(data)

        elif msg_type == "server_stats":
            if self.on_server_stats:
                self.on_server_stats(data)

        elif msg_type == "leaderboard":
            if self.on_leaderboard:
                self.on_leaderboard(data.get("players", []))

        elif msg_type == "error":
            if self.on_error:
                self.on_error(data.get("message", "Unknown error"))


class BattleNetGUI:
    """Interface graphique pour le client Battle.net"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KOF Ultimate Online - Battle.net")
        self.root.geometry("1000x700")
        self.root.configure(bg=Colors.BACKGROUND)

        self.client = BattleNetClient()
        self.client.on_connected = self._on_connected
        self.client.on_disconnected = self._on_disconnected
        self.client.on_match_found = self._on_match_found
        self.client.on_match_finished = self._on_match_finished
        self.client.on_server_stats = self._on_server_stats
        self.client.on_error = self._on_error

        self.searching = False
        self.asyncio_thread = None

        self.create_ui()

        # Démarrer la boucle asyncio dans un thread séparé
        self.start_asyncio_thread()

    def create_ui(self):
        """Crée l'interface utilisateur"""

        # Header
        header = tk.Frame(self.root, bg=Colors.SECONDARY, height=100)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="⚔️ KOF ULTIMATE ONLINE ⚔️",
            font=("Arial", 24, "bold"),
            bg=Colors.SECONDARY,
            fg=Colors.PRIMARY
        )
        title.pack(pady=30)

        # Main container
        main = tk.Frame(self.root, bg=Colors.BACKGROUND)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Left panel - Player info
        left = tk.Frame(main, bg=Colors.ACCENT, width=300)
        left.pack(side="left", fill="both", padx=(0, 10))

        tk.Label(
            left,
            text="VOTRE PROFIL",
            font=("Arial", 14, "bold"),
            bg=Colors.ACCENT,
            fg="white"
        ).pack(pady=15)

        self.profile_frame = tk.Frame(left, bg=Colors.SECONDARY)
        self.profile_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Username input
        tk.Label(
            self.profile_frame,
            text="Nom d'utilisateur:",
            font=("Arial", 10),
            bg=Colors.SECONDARY,
            fg="white"
        ).pack(pady=5)

        self.username_entry = tk.Entry(
            self.profile_frame,
            font=("Arial", 12),
            width=20,
            justify="center"
        )
        self.username_entry.pack(pady=5)
        self.username_entry.insert(0, f"Player{int(time.time() % 10000)}")

        # Connect button
        self.connect_btn = tk.Button(
            self.profile_frame,
            text="Se Connecter",
            font=("Arial", 12, "bold"),
            bg=Colors.SUCCESS,
            fg="white",
            command=self.connect_to_server,
            width=15
        )
        self.connect_btn.pack(pady=15)

        # Player stats
        self.stats_frame = tk.Frame(self.profile_frame, bg=Colors.SECONDARY)
        self.stats_frame.pack(pady=10, fill="both", expand=True)

        # Center panel - Matchmaking
        center = tk.Frame(main, bg=Colors.ACCENT)
        center.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(
            center,
            text="MATCHMAKING",
            font=("Arial", 14, "bold"),
            bg=Colors.ACCENT,
            fg="white"
        ).pack(pady=15)

        # Status
        self.status_label = tk.Label(
            center,
            text="En attente de connexion...",
            font=("Arial", 12),
            bg=Colors.ACCENT,
            fg=Colors.WARNING
        )
        self.status_label.pack(pady=10)

        # Search button
        self.search_btn = tk.Button(
            center,
            text="Rechercher un Adversaire",
            font=("Arial", 14, "bold"),
            bg=Colors.PRIMARY,
            fg="white",
            command=self.toggle_search,
            width=25,
            height=2,
            state="disabled"
        )
        self.search_btn.pack(pady=20)

        # Server stats
        self.server_stats_frame = tk.Frame(center, bg=Colors.SECONDARY)
        self.server_stats_frame.pack(pady=20, fill="x", padx=20)

        tk.Label(
            self.server_stats_frame,
            text="STATISTIQUES DU SERVEUR",
            font=("Arial", 11, "bold"),
            bg=Colors.SECONDARY,
            fg=Colors.PRIMARY
        ).pack(pady=10)

        self.server_stats_text = tk.Label(
            self.server_stats_frame,
            text="",
            font=("Arial", 10),
            bg=Colors.SECONDARY,
            fg="white",
            justify="left"
        )
        self.server_stats_text.pack(pady=5)

        # Right panel - Leaderboard
        right = tk.Frame(main, bg=Colors.ACCENT, width=250)
        right.pack(side="right", fill="both", padx=(10, 0))

        tk.Label(
            right,
            text="CLASSEMENT",
            font=("Arial", 14, "bold"),
            bg=Colors.ACCENT,
            fg="white"
        ).pack(pady=15)

        # Leaderboard list
        self.leaderboard_frame = tk.Frame(right, bg=Colors.SECONDARY)
        self.leaderboard_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.leaderboard_text = tk.Text(
            self.leaderboard_frame,
            font=("Courier", 9),
            bg=Colors.SECONDARY,
            fg="white",
            width=30,
            height=30
        )
        self.leaderboard_text.pack(fill="both", expand=True)

    def start_asyncio_thread(self):
        """Démarre la boucle asyncio dans un thread"""
        def run_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()

        self.asyncio_thread = threading.Thread(target=run_loop, daemon=True)
        self.asyncio_thread.start()

    def connect_to_server(self):
        """Se connecte au serveur"""
        username = self.username_entry.get().strip()

        if not username:
            messagebox.showerror("Erreur", "Veuillez entrer un nom d'utilisateur")
            return

        self.connect_btn.config(state="disabled", text="Connexion...")

        # Connexion asynchrone
        asyncio.run_coroutine_threadsafe(
            self.client.connect(username),
            self.loop
        )

    def toggle_search(self):
        """Active/désactive la recherche"""
        if not self.searching:
            self.searching = True
            self.search_btn.config(text="Annuler la Recherche", bg=Colors.ERROR)
            self.status_label.config(
                text="🔍 Recherche d'adversaire en cours...",
                fg=Colors.WARNING
            )

            asyncio.run_coroutine_threadsafe(
                self.client.search_match(),
                self.loop
            )
        else:
            self.searching = False
            self.search_btn.config(text="Rechercher un Adversaire", bg=Colors.PRIMARY)
            self.status_label.config(
                text="En ligne - Prêt à jouer",
                fg=Colors.SUCCESS
            )

            asyncio.run_coroutine_threadsafe(
                self.client.cancel_search(),
                self.loop
            )

    def _on_connected(self, player_data):
        """Callback: Connecté au serveur"""
        self.root.after(0, lambda: self._update_on_connected(player_data))

    def _update_on_connected(self, player_data):
        """Met à jour l'UI après connexion"""
        self.connect_btn.config(
            state="disabled",
            text="Connecté",
            bg=Colors.SUCCESS
        )

        self.search_btn.config(state="normal")

        self.status_label.config(
            text="En ligne - Prêt à jouer",
            fg=Colors.SUCCESS
        )

        # Afficher les stats du joueur
        self._update_player_stats(player_data)

        # Demander le classement
        asyncio.run_coroutine_threadsafe(
            self.client.get_leaderboard(),
            self.loop
        )

    def _update_player_stats(self, data):
        """Met à jour les stats du joueur"""
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        stats = [
            ("ELO", data.get("elo", 1000)),
            ("Victoires", data.get("wins", 0)),
            ("Défaites", data.get("losses", 0)),
            ("Win Rate", f"{data.get('win_rate', 0):.1f}%")
        ]

        for label, value in stats:
            row = tk.Frame(self.stats_frame, bg=Colors.SECONDARY)
            row.pack(fill="x", pady=2)

            tk.Label(
                row,
                text=f"{label}:",
                font=("Arial", 10),
                bg=Colors.SECONDARY,
                fg="white"
            ).pack(side="left", padx=5)

            tk.Label(
                row,
                text=str(value),
                font=("Arial", 10, "bold"),
                bg=Colors.SECONDARY,
                fg=Colors.PRIMARY
            ).pack(side="right", padx=5)

    def _on_disconnected(self):
        """Callback: Déconnecté du serveur"""
        self.root.after(0, self._update_on_disconnected)

    def _update_on_disconnected(self):
        """Met à jour l'UI après déconnexion"""
        self.connect_btn.config(
            state="normal",
            text="Se Connecter",
            bg=Colors.SUCCESS
        )

        self.search_btn.config(state="disabled")

        self.status_label.config(
            text="Déconnecté",
            fg=Colors.ERROR
        )

    def _on_match_found(self, data):
        """Callback: Match trouvé"""
        self.root.after(0, lambda: self._update_on_match_found(data))

    def _update_on_match_found(self, data):
        """Met à jour l'UI quand un match est trouvé"""
        self.searching = False
        self.search_btn.config(
            state="disabled",
            text="Match en Cours",
            bg=Colors.WARNING
        )

        opponent = data.get("opponent", {})

        self.status_label.config(
            text=f"⚔️ Match contre {opponent.get('username', 'Unknown')}",
            fg=Colors.PRIMARY
        )

        # Afficher une notification
        messagebox.showinfo(
            "Match Trouvé !",
            f"Adversaire: {opponent.get('username')}\n"
            f"ELO: {opponent.get('elo')}\n"
            f"W/L: {opponent.get('wins')}/{opponent.get('losses')}\n\n"
            f"Que le meilleur gagne !"
        )

    def _on_match_finished(self, data):
        """Callback: Match terminé"""
        self.root.after(0, lambda: self._update_on_match_finished(data))

    def _update_on_match_finished(self, data):
        """Met à jour l'UI après un match"""
        self.search_btn.config(
            state="normal",
            text="Rechercher un Adversaire",
            bg=Colors.PRIMARY
        )

        self.status_label.config(
            text="En ligne - Prêt à jouer",
            fg=Colors.SUCCESS
        )

        # Mettre à jour les stats
        new_elo = data.get("your_new_elo", 1000)

        messagebox.showinfo(
            "Match Terminé",
            f"Nouveau ELO: {new_elo}"
        )

    def _on_server_stats(self, data):
        """Callback: Stats du serveur"""
        self.root.after(0, lambda: self._update_server_stats(data))

    def _update_server_stats(self, data):
        """Met à jour les stats du serveur"""
        stats_text = (
            f"Joueurs en ligne: {data.get('online_players', 0)}\n"
            f"En recherche: {data.get('searching_players', 0)}\n"
            f"Matchs actifs: {data.get('active_matches', 0)}\n"
            f"Total matchs: {data.get('total_matches', 0)}"
        )

        self.server_stats_text.config(text=stats_text)

    def _on_error(self, message):
        """Callback: Erreur"""
        self.root.after(0, lambda: messagebox.showerror("Erreur", message))

    def run(self):
        """Lance l'interface"""
        self.root.mainloop()


if __name__ == "__main__":
    app = BattleNetGUI()
    app.run()
