#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IA JOUE EN DIRECT
L'IA joue un match VS en direct avec screenshots en temps réel
"""

import pyautogui
import time
import random
from pathlib import Path
from datetime import datetime
import subprocess

class AIPlayer:
    def __init__(self, game_dir):
        self.game_dir = Path(game_dir)
        self.game_exe = self.game_dir / "KOF_Ultimate_Online.exe"
        self.screenshots_dir = self.game_dir / "live_gameplay"
        self.screenshots_dir.mkdir(exist_ok=True)

        # Désactiver le failsafe
        pyautogui.FAILSAFE = False

    def take_screenshot(self, name=""):
        """Prend un screenshot"""
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{timestamp}_{name}.png" if name else f"{timestamp}.png"
        filepath = self.screenshots_dir / filename
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        print(f"📸 Screenshot: {filename}")
        return filepath

    def press_key(self, key, duration=0.1):
        """Appuie sur une touche"""
        pyautogui.press(key)
        time.sleep(duration)

    def hold_key(self, key, duration=0.3):
        """Maintient une touche appuyée"""
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)

    def start_game(self):
        """Lance le jeu"""
        print("🎮 Lancement du jeu...")
        subprocess.Popen([str(self.game_exe)])
        time.sleep(8)
        self.take_screenshot("01_game_started")

    def navigate_to_vs(self):
        """Navigue vers le mode VS"""
        print("\n📍 Navigation vers le mode VS...")
        time.sleep(2)

        # Appuyer sur Entrée pour passer le titre
        print("  → Passer l'écran titre")
        self.press_key('return', 1)
        self.take_screenshot("02_title_screen")
        time.sleep(1)

        # Sélectionner Arcade/VS (généralement premier choix)
        print("  → Sélectionner mode Arcade")
        self.press_key('return', 1)
        self.take_screenshot("03_mode_select")
        time.sleep(1)

    def select_random_character(self, player_num):
        """Sélectionne un personnage aléatoirement"""
        print(f"\n🎯 Sélection du personnage P{player_num}...")

        # Naviguer aléatoirement dans la grille
        moves = random.randint(3, 8)
        for i in range(moves):
            direction = random.choice(['up', 'down', 'left', 'right'])
            self.press_key(direction, 0.2)
            time.sleep(0.1)

        # Prendre un screenshot de la sélection
        self.take_screenshot(f"04_P{player_num}_selection")

        # Confirmer
        print(f"  → Confirmer P{player_num}")
        self.press_key('a', 0.5)
        time.sleep(1)

    def perform_random_action(self):
        """Effectue une action de combat aléatoire"""
        action = random.choice([
            'attack_light',
            'attack_medium',
            'attack_heavy',
            'move_forward',
            'move_backward',
            'jump',
            'crouch',
            'special_move',
            'block',
            'dash_forward',
            'dash_backward'
        ])

        if action == 'attack_light':
            self.press_key('a')
        elif action == 'attack_medium':
            self.press_key('s')
        elif action == 'attack_heavy':
            self.press_key('d')
        elif action == 'move_forward':
            self.hold_key('right', 0.3)
        elif action == 'move_backward':
            self.hold_key('left', 0.3)
        elif action == 'jump':
            self.press_key('up')
        elif action == 'crouch':
            self.hold_key('down', 0.2)
        elif action == 'special_move':
            # QCF + punch (down, down-forward, forward + A)
            self.press_key('down')
            time.sleep(0.05)
            self.press_key('right')
            time.sleep(0.05)
            self.press_key('a')
        elif action == 'block':
            self.hold_key('left', 0.5)
        elif action == 'dash_forward':
            self.press_key('right')
            time.sleep(0.05)
            self.press_key('right')
        elif action == 'dash_backward':
            self.press_key('left')
            time.sleep(0.05)
            self.press_key('left')

    def play_match(self, duration=60):
        """Joue un match pendant X secondes"""
        print(f"\n⚔️  DÉBUT DU COMBAT ! (durée: {duration}s)")
        print("=" * 60)

        start_time = time.time()
        action_count = 0
        screenshot_interval = 5  # Screenshot toutes les 5 secondes
        last_screenshot = time.time()

        while time.time() - start_time < duration:
            # Effectuer une action
            self.perform_random_action()
            action_count += 1

            # Screenshot périodique
            if time.time() - last_screenshot >= screenshot_interval:
                elapsed = int(time.time() - start_time)
                self.take_screenshot(f"05_fight_{elapsed}s")
                last_screenshot = time.time()
                print(f"  ⚡ Actions effectuées: {action_count} | Temps: {elapsed}s")

            # Petite pause entre les actions
            time.sleep(random.uniform(0.1, 0.3))

        print(f"\n✅ Match terminé! {action_count} actions effectuées")
        self.take_screenshot("06_match_end")

    def play_full_session(self):
        """Session complète de jeu"""
        print("=" * 70)
        print(" " * 20 + "🎮 IA JOUE EN DIRECT 🎮")
        print("=" * 70)
        print()

        # 1. Lancer le jeu
        self.start_game()

        # 2. Naviguer vers VS
        self.navigate_to_vs()

        # 3. Sélectionner les personnages
        self.select_random_character(1)
        self.select_random_character(2)

        # Screenshot du VS screen
        print("\n📺 VS SCREEN")
        time.sleep(2)
        self.take_screenshot("04_vs_screen")
        time.sleep(3)

        # 4. Jouer le match
        self.play_match(duration=60)

        # 5. Après le match
        print("\n🏁 Fin du match")
        time.sleep(3)
        self.take_screenshot("07_results")

        # Retour au menu
        print("\n🔙 Retour aux menus...")
        for _ in range(5):
            self.press_key('return', 0.5)

        print("\n" + "=" * 70)
        print("📁 Screenshots sauvegardés dans:", self.screenshots_dir)
        print("✅ SESSION TERMINÉE!")
        print("=" * 70)

def main():
    game_dir = r"D:\KOF Ultimate Online"
    ai = AIPlayer(game_dir)
    ai.play_full_session()

if __name__ == '__main__':
    main()
