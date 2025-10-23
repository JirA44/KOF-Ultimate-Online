#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend silencieux pour joueurs virtuels
Tourne en arrière-plan SANS console
"""

import sys
import os

# Supprimer toute sortie console
if sys.platform == 'win32':
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Rediriger stdout/stderr vers null
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

# Importer après redirection
from pathlib import Path
import time
import random
import pyautogui
import json
from datetime import datetime
from collections import defaultdict

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.05

class SilentVirtualPlayer:
    """Joueur virtuel 100% silencieux"""

    def __init__(self, player_id, num_players, duration_minutes, game_dir):
        self.player_id = player_id
        self.num_players = num_players
        self.duration = duration_minutes
        self.game_dir = Path(game_dir)

        self.name = self.generate_name()
        self.personality = ["aggressive", "defensive", "balanced"][player_id % 3]

        self.stats = {
            'player_id': player_id,
            'name': self.name,
            'matches': 0,
            'actions': 0,
            'modes': defaultdict(int),
            'start_time': datetime.now().isoformat()
        }

        self.is_playing = True

        # Créer dossiers
        self.logs_dir = self.game_dir / f"vp_{player_id}_data"
        self.logs_dir.mkdir(exist_ok=True)

    def generate_name(self):
        prefixes = ["Dark", "Fire", "Ice", "Storm", "Shadow", "Thunder"]
        suffixes = ["Fighter", "Master", "King", "Warrior", "Pro", "Ace"]
        return f"{random.choice(prefixes)}{random.choice(suffixes)}{self.player_id}"

    def press_key(self, key, duration=0.1):
        try:
            pyautogui.press(key)
            time.sleep(duration)
            self.stats['actions'] += 1
        except:
            pass

    def navigate_to_mode(self):
        modes = ["Arcade", "Versus", "Team", "Survival", "Time Attack"]
        mode = random.choice(modes)

        mode_index = ["Arcade", "Versus", "Team", "Survival", "Time Attack"].index(mode)

        time.sleep(2)
        for _ in range(mode_index):
            self.press_key('down', 0.2)
            time.sleep(0.1)

        self.press_key('return', 0.5)
        time.sleep(1)

        self.stats['modes'][mode] += 1
        return mode

    def select_character(self):
        time.sleep(1)
        moves = random.randint(3, 10)
        for _ in range(moves):
            direction = random.choice(['up', 'down', 'left', 'right'])
            self.press_key(direction, 0.1)
            time.sleep(0.08)

        self.press_key('a', 0.3)
        time.sleep(0.5)

    def select_stage(self):
        time.sleep(0.5)
        for _ in range(random.randint(1, 4)):
            self.press_key(random.choice(['left', 'right']), 0.15)
            time.sleep(0.1)
        self.press_key('return', 0.3)
        time.sleep(1)

    def combat_action(self):
        if self.personality == "aggressive":
            actions = ['right', 'a', 's', 'd', 'j', 'k']
        elif self.personality == "defensive":
            actions = ['left', 'down', 's', 'j']
        else:
            actions = ['right', 'left', 'a', 's', 'd', 'j', 'k', 'up']

        self.press_key(random.choice(actions), 0.1)
        time.sleep(random.uniform(0.05, 0.2))

    def play_match(self):
        time.sleep(5)  # Attendre début match

        duration = random.randint(90, 150)
        start = time.time()

        while (time.time() - start) < duration:
            self.combat_action()
            if random.random() < 0.03:
                time.sleep(random.uniform(0.3, 0.8))

        self.stats['matches'] += 1

        # Post-match
        time.sleep(3)
        for _ in range(6):
            self.press_key('return', 0.5)
            time.sleep(0.8)

        # Retour menu parfois
        if random.random() < 0.3:
            self.press_key('esc', 0.5)
            time.sleep(1)
            self.press_key('return', 0.5)
            time.sleep(2)

    def save_stats(self):
        try:
            stats_file = self.logs_dir / "stats.json"
            # Convertir defaultdict en dict
            stats_copy = dict(self.stats)
            stats_copy['modes'] = dict(stats_copy['modes'])
            with open(stats_file, 'w') as f:
                json.dump(stats_copy, f, indent=2)
        except:
            pass

    def run_session(self):
        session_end = time.time() + (self.duration * 60)

        # Délai initial selon player_id pour éviter la collision
        time.sleep(self.player_id * 3)

        while self.is_playing and time.time() < session_end:
            try:
                mode = self.navigate_to_mode()

                if mode == "Team":
                    for _ in range(3):
                        self.select_character()
                else:
                    self.select_character()

                self.select_stage()
                self.play_match()

                time.sleep(random.uniform(2, 5))

                # Sauvegarder périodiquement
                if self.stats['matches'] % 3 == 0:
                    self.save_stats()

            except:
                time.sleep(2)
                continue

        self.save_stats()


def main():
    # Lire la config depuis arguments
    if len(sys.argv) < 4:
        return

    player_id = int(sys.argv[1])
    num_players = int(sys.argv[2])
    duration = int(sys.argv[3])
    game_dir = sys.argv[4] if len(sys.argv) > 4 else r"D:\KOF Ultimate Online"

    # Créer et lancer le joueur
    player = SilentVirtualPlayer(player_id, num_players, duration, game_dir)
    player.run_session()


if __name__ == "__main__":
    main()
