"""
KOF Ultimate - IA Adversaire en Netplay
Lance une IA qui joue contre vous via internet/réseau comme un vrai joueur
"""

import os
import sys
import time
import subprocess
import pygame
import pyautogui
import random
from pathlib import Path
from datetime import datetime

# Initialiser pygame pour la manette
pygame.init()
pygame.joystick.init()

class NetplayAI:
    """IA qui joue comme un vrai adversaire via netplay"""

    def __init__(self):
        self.joystick = None
        self.running = True
        self.game_started = False
        self.in_match = False
        self.match_start_time = None

        # Patterns de jeu - l'IA joue comme un vrai joueur
        self.combo_patterns = [
            ["down", "right", "a"],  # Hadouken
            ["down", "down", "b"],   # Coup spécial
            ["right", "right", "c"], # Rush
        ]

        self.current_pattern = None
        self.pattern_index = 0
        self.last_action_time = 0
        self.reaction_time = 0.3  # Temps de réaction humain

        # Stats pour jouer naturellement
        self.skill_level = "medium"  # easy, medium, hard
        self.mistake_chance = 0.15  # 15% de chance de faire une erreur
        self.combo_chance = 0.3     # 30% de chance d'essayer un combo

    def log(self, message, level="INFO"):
        """Log les actions"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": "",
            "SUCCESS": "✓ ",
            "ACTION": "🎮 ",
            "ERROR": "❌ "
        }
        prefix = colors.get(level, "")
        print(f"[{timestamp}] {prefix}{message}")

    def detect_gamepad(self):
        """Détecte la manette pour l'IA"""
        self.log("Détection de la manette pour l'IA...", "INFO")

        joystick_count = pygame.joystick.get_count()

        if joystick_count == 0:
            self.log("Aucune manette - utilisation clavier", "INFO")
            return False

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        self.log(f"Manette détectée: {self.joystick.get_name()}", "SUCCESS")
        return True

    def wait_for_match_start(self):
        """Attend le début du match"""
        self.log("En attente du début du match...", "INFO")

        # Attendre 5 secondes pour les menus
        time.sleep(5)

        # Simuler la sélection de personnage aléatoire
        self.log("Sélection d'un personnage...", "ACTION")

        # Quelques mouvements aléatoires dans le menu
        for _ in range(random.randint(3, 8)):
            direction = random.choice(["up", "down", "left", "right"])
            pyautogui.press(direction)
            time.sleep(0.3)

        # Sélectionner
        time.sleep(0.5)
        pyautogui.press("s")  # Bouton A
        time.sleep(1)

        # Confirmer stage
        pyautogui.press("s")
        time.sleep(2)

        self.game_started = True
        self.match_start_time = time.time()
        self.log("Match démarré!", "SUCCESS")

    def decide_action(self):
        """Décide de l'action à faire - comme un vrai joueur"""
        current_time = time.time()

        # Temps de réaction - l'IA ne réagit pas instantanément
        if current_time - self.last_action_time < self.reaction_time:
            return None

        # Faire parfois des erreurs (humain)
        if random.random() < self.mistake_chance:
            # Erreur: action random
            action = random.choice([
                "jump",
                "nothing",
                "wrong_button"
            ])
            self.log("Erreur (humain)", "ACTION")
            if action == "jump":
                pyautogui.press("up")
            elif action == "wrong_button":
                pyautogui.press("d")  # Mauvais bouton
            self.last_action_time = current_time
            return action

        # Essayer un combo?
        if random.random() < self.combo_chance and not self.current_pattern:
            self.current_pattern = random.choice(self.combo_patterns)
            self.pattern_index = 0
            self.log(f"Tentative de combo!", "ACTION")

        # Exécuter le pattern en cours
        if self.current_pattern:
            if self.pattern_index < len(self.current_pattern):
                action = self.current_pattern[self.pattern_index]
                self.execute_action(action)
                self.pattern_index += 1
                self.last_action_time = current_time
                return action
            else:
                self.current_pattern = None
                self.pattern_index = 0

        # Actions normales
        action_type = random.choice([
            "move",
            "attack",
            "block",
            "wait"
        ])

        if action_type == "move":
            direction = random.choice(["left", "right", "up", "down"])
            self.execute_action(direction)
            self.log(f"Mouvement: {direction}", "ACTION")

        elif action_type == "attack":
            button = random.choice(["s", "d", "f"])  # A, B, C
            self.execute_action(button)
            self.log(f"Attaque: {button}", "ACTION")

        elif action_type == "block":
            pyautogui.keyDown("left")
            time.sleep(0.5)
            pyautogui.keyUp("left")
            self.log("Blocage", "ACTION")

        else:  # wait
            time.sleep(0.2)

        self.last_action_time = current_time
        return action_type

    def execute_action(self, action):
        """Exécute une action de jeu"""
        # Mapping des actions
        action_map = {
            "up": "up",
            "down": "down",
            "left": "left",
            "right": "right",
            "a": "s",
            "b": "d",
            "c": "f",
            "nothing": None
        }

        key = action_map.get(action, action)
        if key:
            pyautogui.press(key)
            time.sleep(0.1)

    def play(self):
        """Boucle principale de jeu de l'IA"""
        self.log("", "INFO")
        self.log("=" * 60, "INFO")
        self.log("🤖 IA ADVERSAIRE EN NETPLAY", "INFO")
        self.log("=" * 60, "INFO")
        self.log("", "INFO")
        self.log("Cette IA va jouer contre vous comme un vrai joueur!", "INFO")
        self.log("Niveau de difficulté: {}".format(self.skill_level.upper()), "INFO")
        self.log("", "INFO")

        # Détecter la manette (optionnel)
        self.detect_gamepad()

        # Attendre le début du match
        self.wait_for_match_start()

        self.log("", "INFO")
        self.log("🎮 JEU EN COURS - L'IA joue maintenant!", "INFO")
        self.log("=" * 60, "INFO")
        self.log("", "INFO")

        try:
            while self.running:
                # Lire les événements pygame
                pygame.event.pump()

                # Décider et exécuter une action
                self.decide_action()

                # Petit délai entre les actions
                time.sleep(random.uniform(0.1, 0.3))

        except KeyboardInterrupt:
            self.log("", "INFO")
            self.log("IA arrêtée", "INFO")

        pygame.quit()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="IA Adversaire Netplay pour KOF Ultimate")
    parser.add_argument("--skill", choices=["easy", "medium", "hard"], default="medium",
                        help="Niveau de difficulté de l'IA")
    parser.add_argument("--wait", type=int, default=10,
                        help="Temps d'attente avant de commencer (secondes)")

    args = parser.parse_args()

    print("\n")
    print("=" * 60)
    print("🤖 KOF ULTIMATE - IA ADVERSAIRE NETPLAY")
    print("=" * 60)
    print()
    print("Cette IA va se connecter et jouer contre vous")
    print("comme un vrai joueur humain en ligne!")
    print()
    print(f"Niveau: {args.skill.upper()}")
    print(f"Attente: {args.wait} secondes")
    print()
    print(f"Démarrage dans {args.wait} secondes...")
    print("(Laissez le temps au jeu de démarrer)")
    print()

    time.sleep(args.wait)

    ai = NetplayAI()
    ai.skill_level = args.skill

    # Ajuster les paramètres selon la difficulté
    if args.skill == "easy":
        ai.mistake_chance = 0.35
        ai.combo_chance = 0.15
        ai.reaction_time = 0.5
    elif args.skill == "hard":
        ai.mistake_chance = 0.05
        ai.combo_chance = 0.5
        ai.reaction_time = 0.15

    ai.play()
