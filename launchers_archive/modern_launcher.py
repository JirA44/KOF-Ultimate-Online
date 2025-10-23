#!/usr/bin/env python3
"""
KOF Ultimate Online - Modern Launcher
Style: Battle.net / AAA Game Launcher
Author: Claude
Date: 2025-10-23
"""

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import subprocess
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import threading
import requests

# Configuration
GAME_EXE = "KOF_Ultimate_Online.exe"
CONFIG_FILE = "launcher_config.json"
NEWS_URL = "https://api.github.com/repos/kof-ultimate/news/releases/latest"  # À remplacer
VERSION_FILE = "version.json"

# Dark theme moderne
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuration fenêtre
        self.title("KOF Ultimate Online Launcher")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        # Centrer la fenêtre
        self.center_window()

        # Variables
        self.current_version = "1.0.0"
        self.latest_version = "1.0.0"
        self.player_stats = self.load_player_stats()
        self.news_data = []

        # Créer l'interface
        self.create_sidebar()
        self.create_main_content()
        self.create_footer()

        # Charger les données
        self.load_news_async()
        self.check_updates_async()

    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_sidebar(self):
        """Crée la sidebar gauche avec navigation"""
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)

        # Logo/Titre
        title_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        title_frame.pack(pady=30, padx=20)

        logo_label = ctk.CTkLabel(
            title_frame,
            text="🎮",
            font=ctk.CTkFont(size=40)
        )
        logo_label.pack()

        title_label = ctk.CTkLabel(
            title_frame,
            text="KOF Ultimate",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack()

        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Online",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitle_label.pack()

        # Séparateur
        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color="gray25")
        separator.pack(fill="x", padx=20, pady=20)

        # Boutons navigation
        nav_buttons = [
            ("🏠 Home", self.show_home),
            ("⚔️ Play", self.show_play),
            ("📊 Profile", self.show_profile),
            ("👥 Social", self.show_social),
            ("🏆 Leaderboard", self.show_leaderboard),
            ("⚙️ Settings", self.show_settings),
        ]

        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=40,
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                hover_color=("gray70", "gray30"),
                anchor="w"
            )
            btn.pack(fill="x", padx=20, pady=5)

        # Spacer
        spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        # Player info en bas
        self.create_player_info()

    def create_player_info(self):
        """Affiche les infos du joueur en bas de sidebar"""
        player_frame = ctk.CTkFrame(self.sidebar)
        player_frame.pack(fill="x", padx=20, pady=20)

        # Avatar
        avatar_label = ctk.CTkLabel(
            player_frame,
            text="👤",
            font=ctk.CTkFont(size=40)
        )
        avatar_label.pack(pady=5)

        # Nom
        name_label = ctk.CTkLabel(
            player_frame,
            text=self.player_stats.get("name", "Player"),
            font=ctk.CTkFont(size=14, weight="bold")
        )
        name_label.pack()

        # Level
        level_label = ctk.CTkLabel(
            player_frame,
            text=f"Level {self.player_stats.get('level', 1)}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        level_label.pack()

        # Rank
        rank_label = ctk.CTkLabel(
            player_frame,
            text=f"🏅 {self.player_stats.get('rank', 'Unranked')}",
            font=ctk.CTkFont(size=12),
            text_color="#FFD700"
        )
        rank_label.pack(pady=2)

    def create_main_content(self):
        """Crée la zone de contenu principale"""
        self.main_content = ctk.CTkFrame(self, corner_radius=0)
        self.main_content.pack(side="left", fill="both", expand=True)

        # Par défaut, afficher Home
        self.show_home()

    def create_footer(self):
        """Crée le footer avec bouton Play principal"""
        self.footer = ctk.CTkFrame(self, height=80, corner_radius=0, fg_color=("gray80", "gray20"))
        self.footer.pack(side="bottom", fill="x")
        self.footer.pack_propagate(False)

        # Container pour centrer le bouton
        button_container = ctk.CTkFrame(self.footer, fg_color="transparent")
        button_container.pack(expand=True)

        # Bouton PLAY principal
        self.play_button = ctk.CTkButton(
            button_container,
            text="▶ PLAY",
            command=self.launch_game,
            width=400,
            height=50,
            font=ctk.CTkFont(size=24, weight="bold"),
            fg_color=("#2CC985", "#2FA572"),
            hover_color=("#24A875", "#27995E")
        )
        self.play_button.pack(side="left", padx=10)

        # Boutons secondaires
        quick_match_btn = ctk.CTkButton(
            button_container,
            text="⚡ Quick Match",
            command=self.quick_match,
            width=150,
            height=50,
            font=ctk.CTkFont(size=14),
            fg_color=("gray70", "gray30")
        )
        quick_match_btn.pack(side="left", padx=5)

    def show_home(self):
        """Affiche l'écran d'accueil avec news"""
        self.clear_main_content()

        # Titre
        title = ctk.CTkLabel(
            self.main_content,
            text="Welcome to KOF Ultimate Online",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(pady=30)

        # Hero image/banner (placeholder)
        hero_frame = ctk.CTkFrame(self.main_content, height=300)
        hero_frame.pack(fill="x", padx=40, pady=20)
        hero_frame.pack_propagate(False)

        hero_label = ctk.CTkLabel(
            hero_frame,
            text="🎮 HERO BANNER\nFeatured Content",
            font=ctk.CTkFont(size=24)
        )
        hero_label.pack(expand=True)

        # News section
        news_title = ctk.CTkLabel(
            self.main_content,
            text="Latest News & Updates",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        news_title.pack(pady=(20, 10), padx=40, anchor="w")

        # News grid
        news_frame = ctk.CTkScrollableFrame(self.main_content)
        news_frame.pack(fill="both", expand=True, padx=40, pady=10)

        self.display_news(news_frame)

    def display_news(self, parent):
        """Affiche les news dans une grille"""
        if not self.news_data:
            # Placeholder news
            placeholder_news = [
                {"title": "Season 2 Update", "date": "2025-10-20", "content": "New characters and balance changes!"},
                {"title": "Tournament Announcement", "date": "2025-10-18", "content": "Join our monthly tournament!"},
                {"title": "Patch 1.5.2", "date": "2025-10-15", "content": "Bug fixes and improvements."},
            ]
            self.news_data = placeholder_news

        for i, news_item in enumerate(self.news_data[:6]):
            news_card = ctk.CTkFrame(parent)
            news_card.pack(fill="x", pady=10)

            # Titre
            title_label = ctk.CTkLabel(
                news_card,
                text=news_item["title"],
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w"
            )
            title_label.pack(fill="x", padx=15, pady=(15, 5))

            # Date
            date_label = ctk.CTkLabel(
                news_card,
                text=news_item["date"],
                font=ctk.CTkFont(size=12),
                text_color="gray",
                anchor="w"
            )
            date_label.pack(fill="x", padx=15, pady=(0, 5))

            # Contenu
            content_label = ctk.CTkLabel(
                news_card,
                text=news_item["content"],
                font=ctk.CTkFont(size=14),
                anchor="w"
            )
            content_label.pack(fill="x", padx=15, pady=(0, 15))

    def show_play(self):
        """Affiche les modes de jeu"""
        self.clear_main_content()

        title = ctk.CTkLabel(
            self.main_content,
            text="Choose Your Mode",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(pady=30)

        # Grid de modes
        modes_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        modes_frame.pack(expand=True, padx=40)

        modes = [
            ("⚔️ Ranked Match", "Competitive ranked mode", self.launch_ranked),
            ("🎮 Quick Play", "Fast casual matches", self.quick_match),
            ("🏠 Custom Lobby", "Create or join custom games", self.launch_custom),
            ("🥋 Training Mode", "Practice and improve", self.launch_training),
            ("👥 Local Versus", "Play with friends locally", self.launch_local),
            ("📹 Replays", "Watch your replays", self.show_replays),
        ]

        # 2x3 grid
        for i, (title_text, desc, command) in enumerate(modes):
            row = i // 3
            col = i % 3

            mode_card = ctk.CTkFrame(modes_frame, width=300, height=150)
            mode_card.grid(row=row, column=col, padx=15, pady=15)
            mode_card.pack_propagate(False)
            mode_card.bind("<Button-1>", lambda e, cmd=command: cmd())

            mode_title = ctk.CTkLabel(
                mode_card,
                text=title_text,
                font=ctk.CTkFont(size=18, weight="bold")
            )
            mode_title.pack(pady=(20, 5))

            mode_desc = ctk.CTkLabel(
                mode_card,
                text=desc,
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            mode_desc.pack()

            mode_btn = ctk.CTkButton(
                mode_card,
                text="Select",
                command=command,
                width=100
            )
            mode_btn.pack(pady=15)

    def show_profile(self):
        """Affiche le profil du joueur"""
        self.clear_main_content()

        title = ctk.CTkLabel(
            self.main_content,
            text="Player Profile",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(pady=30)

        # Stats grid
        stats_frame = ctk.CTkFrame(self.main_content)
        stats_frame.pack(fill="both", expand=True, padx=40, pady=20)

        stats = [
            ("Total Matches", self.player_stats.get("total_matches", 0)),
            ("Wins", self.player_stats.get("wins", 0)),
            ("Losses", self.player_stats.get("losses", 0)),
            ("Win Rate", f"{self.player_stats.get('win_rate', 0):.1f}%"),
            ("MMR", self.player_stats.get("mmr", 1000)),
            ("Rank", self.player_stats.get("rank", "Unranked")),
            ("Favorite Character", self.player_stats.get("fav_char", "N/A")),
            ("Play Time", f"{self.player_stats.get('playtime_hours', 0)}h"),
        ]

        for i, (label_text, value) in enumerate(stats):
            row = i // 4
            col = i % 4

            stat_card = ctk.CTkFrame(stats_frame)
            stat_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            value_label = ctk.CTkLabel(
                stat_card,
                text=str(value),
                font=ctk.CTkFont(size=32, weight="bold")
            )
            value_label.pack(pady=(20, 5))

            label = ctk.CTkLabel(
                stat_card,
                text=label_text,
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            label.pack(pady=(0, 20))

        # Configure grid weights
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)

    def show_social(self):
        """Affiche le système social/friends"""
        self.clear_main_content()

        title = ctk.CTkLabel(
            self.main_content,
            text="Friends & Social",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(pady=30)

        # Placeholder
        placeholder = ctk.CTkLabel(
            self.main_content,
            text="👥\nFriends list coming soon!",
            font=ctk.CTkFont(size=24),
            text_color="gray"
        )
        placeholder.pack(expand=True)

    def show_leaderboard(self):
        """Affiche le leaderboard"""
        self.clear_main_content()

        title = ctk.CTkLabel(
            self.main_content,
            text="Global Leaderboard",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(pady=30)

        # Placeholder
        placeholder = ctk.CTkLabel(
            self.main_content,
            text="🏆\nLeaderboard coming soon!",
            font=ctk.CTkFont(size=24),
            text_color="gray"
        )
        placeholder.pack(expand=True)

    def show_settings(self):
        """Affiche les paramètres"""
        self.clear_main_content()

        title = ctk.CTkLabel(
            self.main_content,
            text="Settings",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(pady=30)

        settings_frame = ctk.CTkFrame(self.main_content)
        settings_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Language
        lang_label = ctk.CTkLabel(settings_frame, text="Language:", font=ctk.CTkFont(size=14))
        lang_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        lang_combo = ctk.CTkComboBox(settings_frame, values=["English", "Français"], width=200)
        lang_combo.grid(row=0, column=1, padx=20, pady=20, sticky="w")
        lang_combo.set("English")

        # Theme
        theme_label = ctk.CTkLabel(settings_frame, text="Theme:", font=ctk.CTkFont(size=14))
        theme_label.grid(row=1, column=0, padx=20, pady=20, sticky="w")

        theme_combo = ctk.CTkComboBox(settings_frame, values=["Dark", "Light", "System"], width=200)
        theme_combo.grid(row=1, column=1, padx=20, pady=20, sticky="w")
        theme_combo.set("Dark")

    def show_replays(self):
        """Affiche les replays"""
        messagebox.showinfo("Replays", "Replay system coming soon!")

    def clear_main_content(self):
        """Efface le contenu principal"""
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def launch_game(self):
        """Lance le jeu principal"""
        game_path = Path(GAME_EXE)
        if game_path.exists():
            self.play_button.configure(text="Launching...", state="disabled")
            threading.Thread(target=self._launch_game_thread, daemon=True).start()
        else:
            messagebox.showerror("Error", f"Game executable not found: {GAME_EXE}")

    def _launch_game_thread(self):
        """Lance le jeu dans un thread séparé"""
        try:
            subprocess.Popen([GAME_EXE])
            self.after(2000, self._reset_play_button)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch game: {e}")
            self._reset_play_button()

    def _reset_play_button(self):
        """Réactive le bouton Play"""
        self.play_button.configure(text="▶ PLAY", state="normal")

    def quick_match(self):
        """Lance un quick match"""
        messagebox.showinfo("Quick Match", "Searching for opponent...")
        # TODO: Implémenter matchmaking

    def launch_ranked(self):
        """Lance un match ranked"""
        messagebox.showinfo("Ranked", "Entering ranked queue...")

    def launch_custom(self):
        """Lance custom lobby"""
        messagebox.showinfo("Custom Lobby", "Custom lobby system coming soon!")

    def launch_training(self):
        """Lance training mode"""
        messagebox.showinfo("Training", "Launching training mode...")

    def launch_local(self):
        """Lance versus local"""
        messagebox.showinfo("Local Versus", "Launching local versus...")

    def load_player_stats(self):
        """Charge les stats du joueur"""
        try:
            stats_path = Path("Ikemen_GO/save/stats.json")
            if stats_path.exists():
                with open(stats_path, 'r') as f:
                    return json.load(f)
        except:
            pass

        # Stats par défaut
        return {
            "name": "Player",
            "level": 1,
            "rank": "Bronze",
            "total_matches": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0.0,
            "mmr": 1000,
            "fav_char": "N/A",
            "playtime_hours": 0
        }

    def load_news_async(self):
        """Charge les news de façon asynchrone"""
        threading.Thread(target=self._load_news_thread, daemon=True).start()

    def _load_news_thread(self):
        """Thread pour charger les news"""
        try:
            # TODO: Implémenter fetch des vraies news
            pass
        except:
            pass

    def check_updates_async(self):
        """Vérifie les mises à jour"""
        threading.Thread(target=self._check_updates_thread, daemon=True).start()

    def _check_updates_thread(self):
        """Thread pour vérifier les updates"""
        try:
            # TODO: Implémenter vérification updates
            pass
        except:
            pass

def main():
    """Point d'entrée principal"""
    app = ModernLauncher()
    app.mainloop()

if __name__ == "__main__":
    main()
