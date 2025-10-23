#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Joueur Virtuel avec MANETTE VIRTUELLE
N'utilise PAS le clavier - vous pouvez taper librement !
"""

import sys
import os
from pathlib import Path
import time
import random
import json
from datetime import datetime
from collections import defaultdict

# Supprimer sortie console
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

try:
    import vgamepad as vg
    GAMEPAD_AVAILABLE = True
except ImportError:
    GAMEPAD_AVAILABLE = False

class VirtualGamepadPlayer:
    """Joueur qui utilise une manette virtuelle Xbox 360"""

    def __init__(self, player_id, duration_minutes, game_dir):
        self.player_id = player_id
        self.duration = duration_minutes
        self.game_dir = Path(game_dir)

        self.name = self.generate_name()
        self.personality = ["aggressive", "defensive", "balanced"][player_id % 3]

        # Créer une manette virtuelle Xbox 360
        if GAMEPAD_AVAILABLE:
            self.gamepad = vg.VX360Gamepad()
        else:
            raise ImportError("vgamepad pas installé. Lancez INSTALL_MANETTE_VIRTUELLE.bat")

        self.stats = {
            'player_id': player_id,
            'name': self.name,
            'matches': 0,
            'actions': 0,
            'modes': defaultdict(int),
            'start_time': datetime.now().isoformat()
        }

        self.is_playing = True

        # Dossiers
        self.logs_dir = self.game_dir / f"vp_{player_id}_gamepad"
        self.logs_dir.mkdir(exist_ok=True)

    def generate_name(self):
        prefixes = ["Dark", "Fire", "Ice", "Storm", "Shadow", "Thunder", "Dragon", "Wolf"]
        suffixes = ["Fighter", "Master", "King", "Warrior", "Pro", "Ace", "Slayer", "Champion"]
        return f"{random.choice(prefixes)}{random.choice(suffixes)}{self.player_id}"

    def press_button(self, button, duration=0.1):
        """Presse un bouton de la manette virtuelle"""
        try:
            if button == 'A':
                self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                self.gamepad.update()
                time.sleep(duration)
                self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                self.gamepad.update()

            elif button == 'B':
                self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                self.gamepad.update()
                time.sleep(duration)
                self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                self.gamepad.update()

            elif button == 'X':
                self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
                self.gamepad.update()
                time.sleep(duration)
                self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
                self.gamepad.update()

            elif button == 'Y':
                self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
                self.gamepad.update()
                time.sleep(duration)
                self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
                self.gamepad.update()

            elif button == 'START':
                self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
                self.gamepad.update()
                time.sleep(duration)
                self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
                self.gamepad.update()

            self.stats['actions'] += 1
        except:
            pass

    def move_stick(self, direction, duration=0.1):
        """Bouge le stick analogique"""
        try:
            if direction == 'up':
                self.gamepad.left_joystick_float(0.0, 1.0)
            elif direction == 'down':
                self.gamepad.left_joystick_float(0.0, -1.0)
            elif direction == 'left':
                self.gamepad.left_joystick_float(-1.0, 0.0)
            elif direction == 'right':
                self.gamepad.left_joystick_float(1.0, 0.0)

            self.gamepad.update()
            time.sleep(duration)

            # Reset stick
            self.gamepad.left_joystick_float(0.0, 0.0)
            self.gamepad.update()

            self.stats['actions'] += 1
        except:
            pass

    def press_dpad(self, direction, duration=0.1):
        """Utilise le D-Pad"""
        try:
            if direction == 'up':
                self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            elif direction == 'down':
                self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            elif direction == 'left':
                self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            elif direction == 'right':
                self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)

            self.gamepad.update()
            time.sleep(duration)

            # Release
            if direction == 'up':
                self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            elif direction == 'down':
                self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            elif direction == 'left':
                self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            elif direction == 'right':
                self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)

            self.gamepad.update()
            self.stats['actions'] += 1
        except:
            pass

    def navigate_menu(self):
        """Navigation dans les menus avec D-Pad"""
        modes = ["Arcade", "Versus", "Team", "Survival", "Time Attack"]
        mode = random.choice(modes)
        mode_index = modes.index(mode)

        time.sleep(2)

        # Naviguer vers le mode
        for _ in range(mode_index):
            self.press_dpad('down', 0.2)
            time.sleep(0.15)

        # Confirmer avec A
        self.press_button('A', 0.5)
        time.sleep(1)

        self.stats['modes'][mode] += 1
        return mode

    def select_character(self):
        """Sélection de personnage avec D-Pad"""
        time.sleep(1)

        # Mouvements aléatoires
        moves = random.randint(3, 10)
        for _ in range(moves):
            direction = random.choice(['up', 'down', 'left', 'right'])
            self.press_dpad(direction, 0.1)
            time.sleep(0.08)

        # Confirmer avec A
        self.press_button('A', 0.3)
        time.sleep(0.5)

    def select_stage(self):
        """Sélection de stage"""
        time.sleep(0.5)

        for _ in range(random.randint(1, 4)):
            self.press_dpad(random.choice(['left', 'right']), 0.15)
            time.sleep(0.1)

        self.press_button('A', 0.3)
        time.sleep(1)

    def combat_action(self):
        """Action de combat avec la manette"""
        if self.personality == "aggressive":
            actions = [
                lambda: self.move_stick('right', 0.2),
                lambda: self.press_button('A', 0.1),  # Light punch
                lambda: self.press_button('X', 0.1),  # Heavy punch
                lambda: self.press_button('B', 0.1),  # Light kick
                lambda: self.press_button('Y', 0.1),  # Heavy kick
            ]
        elif self.personality == "defensive":
            actions = [
                lambda: self.move_stick('left', 0.3),
                lambda: self.move_stick('down', 0.2),  # Block
                lambda: self.press_button('B', 0.1),
            ]
        else:
            actions = [
                lambda: self.move_stick('right', 0.15),
                lambda: self.move_stick('left', 0.15),
                lambda: self.move_stick('up', 0.1),  # Jump
                lambda: self.press_button('A', 0.1),
                lambda: self.press_button('B', 0.1),
                lambda: self.press_button('X', 0.1),
                lambda: self.press_button('Y', 0.1),
            ]

        action = random.choice(actions)
        try:
            action()
        except:
            pass

        time.sleep(random.uniform(0.05, 0.2))

    def play_match(self):
        """Joue un match complet"""
        time.sleep(5)

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
            self.press_button('START', 0.5)
            time.sleep(0.8)

        # Retour menu
        if random.random() < 0.3:
            self.press_button('B', 0.5)
            time.sleep(1)
            self.press_button('A', 0.5)
            time.sleep(2)

    def save_stats(self):
        try:
            stats_file = self.logs_dir / "stats.json"
            stats_copy = dict(self.stats)
            stats_copy['modes'] = dict(stats_copy['modes'])
            with open(stats_file, 'w') as f:
                json.dump(stats_copy, f, indent=2)
        except:
            pass

    def run_session(self):
        """Lance la session de jeu"""
        session_end = time.time() + (self.duration * 60)

        # Délai initial
        time.sleep(self.player_id * 3)

        while self.is_playing and time.time() < session_end:
            try:
                mode = self.navigate_menu()

                if mode == "Team":
                    for _ in range(3):
                        self.select_character()
                else:
                    self.select_character()

                self.select_stage()
                self.play_match()

                time.sleep(random.uniform(2, 5))

                if self.stats['matches'] % 3 == 0:
                    self.save_stats()

            except:
                time.sleep(2)
                continue

        self.save_stats()
        self.gamepad.reset()


def main():
    if not GAMEPAD_AVAILABLE:
        return

    if len(sys.argv) < 3:
        return

    player_id = int(sys.argv[1])
    duration = int(sys.argv[2])
    game_dir = sys.argv[3] if len(sys.argv) > 3 else r"D:\KOF Ultimate Online"

    player = VirtualGamepadPlayer(player_id, duration, game_dir)
    player.run_session()


if __name__ == "__main__":
    main()
