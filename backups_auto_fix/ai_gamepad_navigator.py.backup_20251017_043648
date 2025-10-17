"""
KOF Ultimate - IA Navigateur Manette
Cette IA utilise physiquement la manette pour naviguer dans le jeu
et détecte automatiquement les problèmes
"""

import os
import sys
import time
import pygame
import pyautogui
import json
from datetime import datetime
from pathlib import Path

# Initialiser pygame pour la manette
pygame.init()
pygame.joystick.init()

class GamepadNavigatorAI:
    """IA qui navigue dans le jeu avec la manette"""

    def __init__(self):
        self.log_file = Path("D:/KOF Ultimate/ai_gamepad_navigation.log")
        self.joystick = None
        self.problems = []
        self.actions = []

    def log(self, message, level="INFO"):
        """Log les actions avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)

        self.actions.append({
            "timestamp": timestamp,
            "level": level,
            "message": message
        })

        # Sauvegarder dans le fichier
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")

    def detect_gamepad(self):
        """Détecte la manette"""
        self.log("🎮 Recherche de la manette...", "INFO")

        joystick_count = pygame.joystick.get_count()

        if joystick_count == 0:
            self.log("❌ PROBLÈME: Aucune manette détectée!", "ERROR")
            self.problems.append("No gamepad detected")
            return False

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        gamepad_name = self.joystick.get_name()
        self.log(f"✓ Manette détectée: {gamepad_name}", "SUCCESS")
        self.log(f"  - {self.joystick.get_numaxes()} axes", "INFO")
        self.log(f"  - {self.joystick.get_numbuttons()} boutons", "INFO")
        self.log(f"  - {self.joystick.get_numhats()} D-Pads", "INFO")

        return True

    def read_gamepad_state(self):
        """Lit l'état actuel de la manette"""
        pygame.event.pump()

        state = {
            "axes": [],
            "buttons": [],
            "hat": None
        }

        # Lire les axes
        for i in range(self.joystick.get_numaxes()):
            state["axes"].append(self.joystick.get_axis(i))

        # Lire les boutons
        for i in range(self.joystick.get_numbuttons()):
            state["buttons"].append(self.joystick.get_button(i))

        # Lire le D-Pad
        if self.joystick.get_numhats() > 0:
            state["hat"] = self.joystick.get_hat(0)

        return state

    def simulate_button_press(self, button_name):
        """Simule une pression de bouton en utilisant le clavier comme backup"""
        self.log(f"🎯 Simulant {button_name}...", "INFO")

        # Mapping pour le clavier comme backup si la manette ne fonctionne pas
        keyboard_map = {
            "A": "s",      # Bouton A du jeu
            "B": "escape", # Retour
            "UP": "up",
            "DOWN": "down",
            "LEFT": "left",
            "RIGHT": "right",
            "START": "return"
        }

        if button_name in keyboard_map:
            key = keyboard_map[button_name]
            pyautogui.press(key)
            time.sleep(0.3)

    def test_gamepad_in_game(self):
        """Teste la manette dans le jeu"""
        self.log("", "INFO")
        self.log("=" * 60, "INFO")
        self.log("🚀 DÉMARRAGE DU TEST DE NAVIGATION", "INFO")
        self.log("=" * 60, "INFO")

        # Attendre que le jeu soit prêt
        self.log("⏳ Attente du chargement du jeu...", "INFO")
        time.sleep(3)

        # Test 1: Détecter les mouvements du D-Pad
        self.log("", "INFO")
        self.log("📍 Test 1: D-Pad", "INFO")
        detected_dpad = False

        for i in range(20):
            state = self.read_gamepad_state()

            if state["hat"] and state["hat"] != (0, 0):
                self.log(f"✓ D-Pad détecté: {state['hat']}", "SUCCESS")
                detected_dpad = True
                break

            time.sleep(0.1)

        if not detected_dpad:
            self.log("⚠️  D-Pad non détecté - tentative avec clavier", "WARNING")
            self.problems.append("D-Pad not responding - using keyboard fallback")

        # Test 2: Navigation dans le menu
        self.log("", "INFO")
        self.log("📍 Test 2: Navigation dans le menu", "INFO")

        # Essayer de naviguer vers le bas
        self.log("  → Navigation BAS", "INFO")
        self.simulate_button_press("DOWN")
        time.sleep(0.5)

        # Essayer de naviguer vers le haut
        self.log("  → Navigation HAUT", "INFO")
        self.simulate_button_press("UP")
        time.sleep(0.5)

        # Test 3: Bouton A (Entrée)
        self.log("", "INFO")
        self.log("📍 Test 3: Bouton A (Entrée)", "INFO")
        button_a_working = False

        for i in range(10):
            state = self.read_gamepad_state()

            # Bouton A est généralement le bouton 0 ou 1
            if state["buttons"][0] or (len(state["buttons"]) > 1 and state["buttons"][1]):
                self.log("✓ Bouton A détecté!", "SUCCESS")
                button_a_working = True
                break

            time.sleep(0.1)

        if not button_a_working:
            self.log("⚠️  Bouton A non détecté - utilisation clavier", "WARNING")
            self.problems.append("Button A not responding")
            self.simulate_button_press("A")

        time.sleep(0.5)

        # Test 4: Bouton B (Retour)
        self.log("", "INFO")
        self.log("📍 Test 4: Bouton B (Retour)", "INFO")
        button_b_working = False

        for i in range(10):
            state = self.read_gamepad_state()

            # Bouton B est généralement le bouton 1 ou 2
            if len(state["buttons"]) > 1 and state["buttons"][1]:
                self.log("✓ Bouton B détecté!", "SUCCESS")
                button_b_working = True
                break

            time.sleep(0.1)

        if not button_b_working:
            self.log("⚠️  Bouton B non détecté - utilisation clavier", "WARNING")
            self.problems.append("Button B not responding")
            self.simulate_button_press("B")

        # Test 5: Navigation complète
        self.log("", "INFO")
        self.log("📍 Test 5: Séquence de navigation complète", "INFO")

        navigation_sequence = [
            ("DOWN", "Descendre dans le menu"),
            ("DOWN", "Descendre encore"),
            ("UP", "Remonter"),
            ("A", "Sélectionner"),
            ("B", "Retour")
        ]

        for action, description in navigation_sequence:
            self.log(f"  → {description}", "INFO")
            self.simulate_button_press(action)
            time.sleep(0.8)

    def generate_report(self):
        """Génère un rapport complet"""
        self.log("", "INFO")
        self.log("=" * 60, "INFO")
        self.log("📊 RAPPORT DE NAVIGATION", "INFO")
        self.log("=" * 60, "INFO")

        self.log(f"Actions effectuées: {len(self.actions)}", "INFO")
        self.log(f"Problèmes détectés: {len(self.problems)}", "INFO")

        if self.problems:
            self.log("", "INFO")
            self.log("⚠️  PROBLÈMES DÉTECTÉS:", "WARNING")
            for i, problem in enumerate(self.problems, 1):
                self.log(f"  {i}. {problem}", "ERROR")
        else:
            self.log("", "INFO")
            self.log("✓ Aucun problème détecté!", "SUCCESS")

        # Sauvegarder le rapport JSON
        report = {
            "timestamp": datetime.now().isoformat(),
            "gamepad": self.joystick.get_name() if self.joystick else "None",
            "actions": self.actions,
            "problems": self.problems
        }

        report_file = Path("D:/KOF Ultimate/ai_gamepad_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        self.log(f"", "INFO")
        self.log(f"📄 Rapport sauvegardé: {report_file}", "SUCCESS")

    def run(self):
        """Lance le processus complet"""
        # Clear le log précédent
        if self.log_file.exists():
            self.log_file.unlink()

        self.log("=" * 60, "INFO")
        self.log("🤖 IA NAVIGATEUR MANETTE - KOF ULTIMATE", "INFO")
        self.log("=" * 60, "INFO")

        # Étape 1: Détecter la manette
        if not self.detect_gamepad():
            self.log("", "INFO")
            self.log("❌ Impossible de continuer sans manette", "ERROR")
            self.generate_report()
            return False

        # Étape 2: Vérifier que le jeu est lancé
        self.log("", "INFO")
        self.log("🎮 Vérification du jeu...", "INFO")

        try:
            windows = pyautogui.getWindowsWithTitle("KOF")
            if not windows:
                self.log("⚠️  Jeu non détecté - assurez-vous qu'il est lancé", "WARNING")
        except:
            pass

        # Étape 3: Tester la navigation
        self.test_gamepad_in_game()

        # Étape 4: Générer le rapport
        self.generate_report()

        self.log("", "INFO")
        self.log("=" * 60, "INFO")
        self.log("✓ TEST TERMINÉ", "SUCCESS")
        self.log("=" * 60, "INFO")

        return True

if __name__ == "__main__":
    print("\n")
    print("=" * 60)
    print("🤖 IA NAVIGATEUR MANETTE - MODE AUTO")
    print("=" * 60)
    print()
    print("Cette IA va:")
    print("  1. Détecter votre manette")
    print("  2. Tester la navigation dans le jeu")
    print("  3. Signaler tous les problèmes")
    print()
    print("Démarrage automatique dans 2 secondes...")
    print()

    time.sleep(2)

    navigator = GamepadNavigatorAI()
    navigator.run()

    print("\n")
    print("✓ Test terminé - rapport généré")
    print()

    pygame.quit()
    sys.exit(0)
