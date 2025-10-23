#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SYSTÈME IA MULTI-MODES AUTONOME
Les IA jouent automatiquement dans tous les modes de jeu sans intervention
Modes: Arcade, Versus, Team, Survival, Time Attack, Training
"""

import pyautogui
import time
import random
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import json
import logging

# Configuration du logging silencieux
logging.basicConfig(
    filename='ai_multi_mode.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GameMode:
    """Définition des modes de jeu"""
    ARCADE = "arcade"
    VERSUS = "versus"
    TEAM = "team"
    SURVIVAL = "survival"
    TIME_ATTACK = "time_attack"
    TRAINING = "training"
    TEAM_VERSUS = "team_versus"

    ALL_MODES = [ARCADE, VERSUS, TEAM, SURVIVAL, TIME_ATTACK, TRAINING, TEAM_VERSUS]

class AIMultiModePlayer:
    """IA qui joue dans différents modes automatiquement"""

    def __init__(self, player_id, game_dir, personality="balanced", mode_rotation=True):
        self.player_id = player_id
        self.game_dir = Path(game_dir)
        self.game_exe = self.game_dir / "KOF_Ultimate_Online.exe"
        self.personality = personality
        self.mode_rotation = mode_rotation

        # Stats
        self.stats = {
            'matches_played': 0,
            'modes_played': {},
            'session_start': datetime.now().isoformat(),
            'player_id': player_id
        }

        # Dossiers de logs
        self.logs_dir = self.game_dir / "ai_logs"
        self.logs_dir.mkdir(exist_ok=True)

        self.screenshots_dir = self.game_dir / f"ai_screenshots_p{player_id}"
        self.screenshots_dir.mkdir(exist_ok=True)

        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.05

        # Configuration de la navigation des menus
        self.menu_navigation = {
            GameMode.ARCADE: {'moves': ['down', 'return'], 'delay': 2},
            GameMode.VERSUS: {'moves': ['return'], 'delay': 2},
            GameMode.TEAM: {'moves': ['down', 'down', 'return'], 'delay': 2},
            GameMode.SURVIVAL: {'moves': ['down', 'down', 'down', 'return'], 'delay': 2},
            GameMode.TIME_ATTACK: {'moves': ['down', 'down', 'down', 'down', 'return'], 'delay': 2},
            GameMode.TRAINING: {'moves': ['down', 'down', 'down', 'down', 'down', 'return'], 'delay': 2},
            GameMode.TEAM_VERSUS: {'moves': ['down', 'down', 'down', 'down', 'down', 'down', 'return'], 'delay': 2}
        }

        self.current_mode = None
        self.is_running = False

    def log(self, message, level="INFO"):
        """Log avec niveau"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[P{self.player_id}] {message}"

        if level == "INFO":
            logging.info(log_msg)
        elif level == "WARNING":
            logging.warning(log_msg)
        elif level == "ERROR":
            logging.error(log_msg)

        # Affichage console minimal
        print(f"{timestamp} [P{self.player_id}] {message}")

    def take_screenshot(self, name=""):
        """Prend un screenshot silencieusement"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            mode = self.current_mode or "menu"
            filename = f"{timestamp}_{mode}_{name}.png"
            filepath = self.screenshots_dir / filename
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            return filepath
        except Exception as e:
            self.log(f"Screenshot error: {e}", "WARNING")
            return None

    def press_key(self, key, duration=0.1):
        """Presse une touche"""
        try:
            pyautogui.press(key)
            time.sleep(duration)
        except Exception as e:
            self.log(f"Key press error: {e}", "WARNING")

    def hold_key(self, key, duration=0.3):
        """Maintient une touche"""
        try:
            pyautogui.keyDown(key)
            time.sleep(duration)
            pyautogui.keyUp(key)
        except Exception as e:
            self.log(f"Key hold error: {e}", "WARNING")

    def start_game(self):
        """Lance le jeu en arrière-plan"""
        self.log("Lancement du jeu...")
        try:
            # Lancer le jeu minimisé
            subprocess.Popen(
                [str(self.game_exe)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            time.sleep(10)  # Attendre que le jeu charge
            self.take_screenshot("game_start")
            self.log("Jeu lancé avec succès")
            return True
        except Exception as e:
            self.log(f"Erreur lancement jeu: {e}", "ERROR")
            return False

    def choose_mode(self):
        """Choisit un mode de jeu"""
        if self.mode_rotation:
            # Rotation: choisir un mode pas encore joué ou aléatoire
            available_modes = [m for m in GameMode.ALL_MODES
                             if self.stats['modes_played'].get(m, 0) < 5]
            if not available_modes:
                available_modes = GameMode.ALL_MODES

            mode = random.choice(available_modes)
        else:
            mode = random.choice(GameMode.ALL_MODES)

        self.current_mode = mode
        self.log(f"Mode sélectionné: {mode.upper()}")
        return mode

    def navigate_to_mode(self, mode):
        """Navigue vers le mode choisi depuis le menu principal"""
        self.log(f"Navigation vers {mode}...")

        # Attendre le menu principal
        time.sleep(3)
        self.take_screenshot("main_menu")

        # Récupérer la navigation pour ce mode
        nav = self.menu_navigation.get(mode, {'moves': ['return'], 'delay': 2})

        # Exécuter les mouvements
        for move in nav['moves']:
            self.press_key(move, 0.3)
            time.sleep(0.2)

        time.sleep(nav['delay'])
        self.take_screenshot(f"{mode}_selected")
        self.log(f"Mode {mode} sélectionné")

    def select_random_character(self, num_chars=1):
        """Sélectionne des personnages aléatoirement"""
        self.log(f"Sélection de {num_chars} personnage(s)...")

        for i in range(num_chars):
            # Attendre l'écran de sélection
            time.sleep(2)

            # Mouvements aléatoires dans la grille
            moves = random.randint(5, 15)
            for _ in range(moves):
                direction = random.choice(['up', 'down', 'left', 'right'])
                self.press_key(direction, 0.15)
                time.sleep(0.1)

            # Confirmer la sélection
            self.press_key('a', 0.5)
            time.sleep(1)

            self.log(f"Personnage {i+1}/{num_chars} sélectionné")

        self.take_screenshot("characters_selected")

    def select_random_stage(self):
        """Sélectionne un stage aléatoirement"""
        time.sleep(1)

        # Mouvements aléatoires
        moves = random.randint(2, 8)
        for _ in range(moves):
            direction = random.choice(['left', 'right'])
            self.press_key(direction, 0.2)
            time.sleep(0.1)

        # Confirmer
        self.press_key('a', 0.5)
        time.sleep(2)
        self.take_screenshot("stage_selected")

    def perform_combat_action(self):
        """Effectue une action de combat selon la personnalité"""
        actions = {
            "aggressive": [
                lambda: self.press_key('right'),
                lambda: self.press_key('a'),
                lambda: self.press_key('s'),
                lambda: self.press_key('d'),
                lambda: [self.press_key('down'), time.sleep(0.05),
                        self.press_key('right'), time.sleep(0.05),
                        self.press_key('a')]  # Special move
            ],
            "defensive": [
                lambda: self.hold_key('left', 0.3),
                lambda: self.hold_key('down', 0.2),
                lambda: self.press_key('s'),
                lambda: [self.press_key('left'), self.press_key('left')]  # Back dash
            ],
            "balanced": [
                lambda: self.press_key('right'),
                lambda: self.press_key('left'),
                lambda: self.press_key('a'),
                lambda: self.press_key('s'),
                lambda: self.press_key('d'),
                lambda: self.press_key('up')  # Jump
            ]
        }

        personality_actions = actions.get(self.personality, actions["balanced"])
        action = random.choice(personality_actions)

        try:
            if callable(action):
                action()
            else:
                for a in action:
                    if callable(a):
                        a()
        except Exception as e:
            self.log(f"Action error: {e}", "WARNING")

        time.sleep(random.uniform(0.1, 0.3))

    def play_match(self, mode, duration=180):
        """Joue un match complet"""
        self.log(f"Début du match en mode {mode}")

        # Attendre que le match commence
        time.sleep(5)
        self.take_screenshot("match_start")

        # Jouer pendant la durée spécifiée
        start_time = time.time()
        action_count = 0
        screenshot_interval = 30  # Screenshot toutes les 30 secondes
        last_screenshot = start_time

        while time.time() - start_time < duration:
            # Effectuer une action
            self.perform_combat_action()
            action_count += 1

            # Screenshot périodique
            if time.time() - last_screenshot > screenshot_interval:
                self.take_screenshot(f"combat_{action_count}")
                last_screenshot = time.time()

            # Petite pause aléatoire pour plus de réalisme
            if random.random() < 0.05:  # 5% de chance
                time.sleep(random.uniform(0.5, 1.5))

        self.take_screenshot("match_end")
        self.log(f"Match terminé - {action_count} actions effectuées")

        # Mettre à jour les stats
        self.stats['matches_played'] += 1
        self.stats['modes_played'][mode] = self.stats['modes_played'].get(mode, 0) + 1

        # Sauvegarder les stats
        self.save_stats()

    def handle_post_match(self):
        """Gère l'écran après le match"""
        self.log("Gestion post-match...")
        time.sleep(5)

        # Appuyer sur des touches pour passer les écrans
        for _ in range(5):
            self.press_key('return', 1)
            time.sleep(1)

        # Revenir au menu principal ou continuer
        if random.random() < 0.3:  # 30% de chance de retour au menu
            self.press_key('esc', 1)
            time.sleep(2)
            self.press_key('return', 1)
            self.log("Retour au menu principal")
            return True  # Retour au menu
        else:
            self.log("Continue dans le mode actuel")
            return False  # Continue dans le mode

    def play_session(self, num_matches=5):
        """Joue une session complète avec plusieurs matches"""
        self.log(f"=== DÉBUT SESSION: {num_matches} matches ===")
        self.is_running = True

        # Lancer le jeu
        if not self.start_game():
            self.log("Échec du lancement du jeu", "ERROR")
            return

        matches_completed = 0

        while matches_completed < num_matches and self.is_running:
            try:
                # Choisir un mode
                mode = self.choose_mode()

                # Naviguer vers le mode
                self.navigate_to_mode(mode)

                # Sélectionner personnage(s)
                if mode in [GameMode.TEAM, GameMode.TEAM_VERSUS]:
                    self.select_random_character(3)  # 3 personnages pour team
                else:
                    self.select_random_character(1)

                # Sélectionner stage (si applicable)
                if mode not in [GameMode.TRAINING]:
                    self.select_random_stage()

                # Jouer le match
                match_duration = random.randint(120, 240)  # 2-4 minutes
                self.play_match(mode, match_duration)

                # Gérer post-match
                return_to_menu = self.handle_post_match()

                matches_completed += 1
                self.log(f"Match {matches_completed}/{num_matches} terminé")

                # Pause entre les matches
                time.sleep(random.uniform(3, 8))

            except Exception as e:
                self.log(f"Erreur pendant le match: {e}", "ERROR")
                # Essayer de revenir au menu
                for _ in range(3):
                    self.press_key('esc', 1)
                    time.sleep(1)

        self.log(f"=== SESSION TERMINÉE: {matches_completed} matches ===")
        self.is_running = False

    def save_stats(self):
        """Sauvegarde les statistiques"""
        stats_file = self.logs_dir / f"stats_player_{self.player_id}.json"
        try:
            with open(stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            self.log(f"Erreur sauvegarde stats: {e}", "WARNING")

    def stop(self):
        """Arrête l'IA"""
        self.log("Arrêt de l'IA...")
        self.is_running = False
        self.save_stats()

def main():
    """Point d'entrée principal"""
    print("\n" + "="*60)
    print("  🤖 SYSTÈME IA MULTI-MODES AUTONOME")
    print("="*60 + "\n")

    game_dir = r"D:\KOF Ultimate Online"

    # Paramètres
    player_id = 1
    personality = random.choice(["aggressive", "defensive", "balanced"])
    num_matches = 10  # Nombre de matches à jouer

    print(f"Configuration:")
    print(f"  Player ID: {player_id}")
    print(f"  Personnalité: {personality}")
    print(f"  Matches: {num_matches}")
    print(f"  Rotation modes: Activée")
    print()

    # Créer l'IA
    ai = AIMultiModePlayer(
        player_id=player_id,
        game_dir=game_dir,
        personality=personality,
        mode_rotation=True
    )

    # Lancer la session
    try:
        ai.play_session(num_matches=num_matches)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption utilisateur")
        ai.stop()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        ai.stop()

    print("\n" + "="*60)
    print("  ✅ SESSION TERMINÉE")
    print("="*60)
    print(f"\nLogs: {ai.logs_dir}")
    print(f"Screenshots: {ai.screenshots_dir}")
    print()

if __name__ == "__main__":
    main()
