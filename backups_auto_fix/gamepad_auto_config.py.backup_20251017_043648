"""
KOF Ultimate - Auto-Configuration des Manettes
Détecte et configure automatiquement les manettes Xbox et PlayStation
"""

import os
import sys
from pathlib import Path
import configparser
import subprocess

GAME_PATH = Path("D:/KOF Ultimate")
CONFIG_FILE = GAME_PATH / "data" / "mugen.cfg"

# Configurations prédéfinies pour les manettes populaires
GAMEPAD_CONFIGS = {
    "xbox": {
        "name": "Xbox Controller",
        "up": "JOY_YAXIS",
        "down": "JOY_YAXIS",
        "left": "JOY_XAXIS",
        "right": "JOY_XAXIS",
        "a": "JOY_1",      # A button
        "b": "JOY_2",      # B button
        "x": "JOY_3",      # X button
        "y": "JOY_4",      # Y button
        "lb": "JOY_5",     # Left bumper
        "rb": "JOY_6",     # Right bumper
        "start": "JOY_8",  # Start
        "select": "JOY_7"  # Back/Select
    },
    "playstation": {
        "name": "PlayStation Controller",
        "up": "JOY_YAXIS",
        "down": "JOY_YAXIS",
        "left": "JOY_XAXIS",
        "right": "JOY_XAXIS",
        "cross": "JOY_2",    # X (Cross)
        "circle": "JOY_3",   # O (Circle)
        "square": "JOY_1",   # Square
        "triangle": "JOY_4", # Triangle
        "l1": "JOY_5",       # L1
        "r1": "JOY_6",       # R1
        "start": "JOY_10",   # Start
        "select": "JOY_9"    # Select
    }
}

class GamepadConfigurator:
    """Configure automatiquement les manettes"""

    def __init__(self):
        self.config_file = CONFIG_FILE

    def detect_gamepads(self):
        """Détecte les manettes connectées"""
        print("🎮 Détection des manettes...")

        try:
            # Utiliser pygame pour détecter les manettes
            import pygame
            pygame.init()
            pygame.joystick.init()

            joystick_count = pygame.joystick.get_count()

            if joystick_count == 0:
                print("❌ Aucune manette détectée")
                return []

            gamepads = []
            for i in range(joystick_count):
                joy = pygame.joystick.Joystick(i)
                joy.init()

                gamepad_info = {
                    "index": i,
                    "name": joy.get_name(),
                    "axes": joy.get_numaxes(),
                    "buttons": joy.get_numbuttons(),
                    "hats": joy.get_numhats()
                }

                gamepads.append(gamepad_info)

                print(f"✓ Manette {i+1}: {gamepad_info['name']}")
                print(f"  - Axes: {gamepad_info['axes']}")
                print(f"  - Boutons: {gamepad_info['buttons']}")

            pygame.quit()
            return gamepads

        except ImportError:
            print("⚠️  Module pygame non installé")
            print("Installation automatique...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pygame"])
            print("✓ pygame installé! Relancez le script.")
            return None

        except Exception as e:
            print(f"❌ Erreur détection: {e}")
            return []

    def identify_gamepad_type(self, gamepad_name):
        """Identifie le type de manette"""
        name_lower = gamepad_name.lower()

        if "xbox" in name_lower or "x360" in name_lower or "xone" in name_lower:
            return "xbox"
        elif "playstation" in name_lower or "ps2" in name_lower or "ps3" in name_lower or "ps4" in name_lower or "ps5" in name_lower or "dualshock" in name_lower or "dualsense" in name_lower:
            return "playstation"
        else:
            return "generic"

    def backup_config(self):
        """Sauvegarde la configuration actuelle"""
        if self.config_file.exists():
            backup_path = self.config_file.with_suffix('.cfg.backup')
            import shutil
            shutil.copy2(self.config_file, backup_path)
            print(f"💾 Backup créé: {backup_path.name}")

    def configure_player(self, player_num, gamepad_type):
        """Configure un joueur avec une manette"""
        if not self.config_file.exists():
            print(f"❌ Fichier de configuration non trouvé: {self.config_file}")
            return False

        print(f"\n⚙️  Configuration du Joueur {player_num} ({gamepad_type})...")

        try:
            # Lire la configuration
            config = configparser.ConfigParser()
            config.optionxform = str  # Préserver la casse
            config.read(self.config_file, encoding='utf-8')

            # Section de configuration
            input_section = f"Input"

            if input_section not in config:
                config.add_section(input_section)

            # Mapping selon le type de manette
            if gamepad_type == "xbox":
                mappings = {
                    f"p{player_num}.joystick": "1",  # Activer joystick
                    f"p{player_num}.up": "~JOY_YAXIS",
                    f"p{player_num}.down": "JOY_YAXIS",
                    f"p{player_num}.left": "~JOY_XAXIS",
                    f"p{player_num}.right": "JOY_XAXIS",
                    f"p{player_num}.a": "JOY_1",       # Coup léger (A)
                    f"p{player_num}.b": "JOY_2",       # Coup moyen (B)
                    f"p{player_num}.c": "JOY_4",       # Coup fort (Y)
                    f"p{player_num}.x": "JOY_1",       # Pied léger (A)
                    f"p{player_num}.y": "JOY_3",       # Pied moyen (X)
                    f"p{player_num}.z": "JOY_5",       # Pied fort (LB)
                    f"p{player_num}.start": "JOY_8",   # Start
                    f"p{player_num}.pause": "JOY_8",   # Start (pause)
                }

                print("  Type: Xbox Controller")
                print("  Mapping:")
                print("    Directions: D-Pad / Stick gauche")
                print("    Coups: A (léger), B (moyen), Y (fort)")
                print("    Pieds: A (léger), X (moyen), LB (fort)")
                print("    Start: Start button")

            elif gamepad_type == "playstation":
                mappings = {
                    f"p{player_num}.joystick": "1",
                    f"p{player_num}.up": "~JOY_YAXIS",
                    f"p{player_num}.down": "JOY_YAXIS",
                    f"p{player_num}.left": "~JOY_XAXIS",
                    f"p{player_num}.right": "JOY_XAXIS",
                    f"p{player_num}.a": "JOY_3",       # Coup léger (Circle)
                    f"p{player_num}.b": "JOY_2",       # Coup moyen (Cross)
                    f"p{player_num}.c": "JOY_4",       # Coup fort (Triangle)
                    f"p{player_num}.x": "JOY_1",       # Pied léger (Square)
                    f"p{player_num}.y": "JOY_3",       # Pied moyen (Circle)
                    f"p{player_num}.z": "JOY_5",       # Pied fort (L1)
                    f"p{player_num}.start": "JOY_10",  # Start
                    f"p{player_num}.pause": "JOY_10",  # Start (pause)
                }

                print("  Type: PlayStation Controller")
                print("  Mapping:")
                print("    Directions: D-Pad / Stick gauche")
                print("    Coups: O (léger), X (moyen), △ (fort)")
                print("    Pieds: □ (léger), O (moyen), L1 (fort)")
                print("    Start: Start button")

            else:
                print("  ⚠️  Type de manette non reconnu, configuration générique")
                mappings = {
                    f"p{player_num}.joystick": "1",
                    f"p{player_num}.up": "~JOY_YAXIS",
                    f"p{player_num}.down": "JOY_YAXIS",
                    f"p{player_num}.left": "~JOY_XAXIS",
                    f"p{player_num}.right": "JOY_XAXIS",
                    f"p{player_num}.a": "JOY_1",
                    f"p{player_num}.b": "JOY_2",
                    f"p{player_num}.c": "JOY_3",
                    f"p{player_num}.x": "JOY_4",
                    f"p{player_num}.y": "JOY_5",
                    f"p{player_num}.z": "JOY_6",
                    f"p{player_num}.start": "JOY_8",
                    f"p{player_num}.pause": "JOY_8",
                }

            # Appliquer les mappings
            for key, value in mappings.items():
                config.set(input_section, key, value)

            # Sauvegarder
            with open(self.config_file, 'w', encoding='utf-8') as f:
                config.write(f, space_around_delimiters=True)

            print(f"✓ Joueur {player_num} configuré avec succès!")
            return True

        except Exception as e:
            print(f"❌ Erreur configuration: {e}")
            return False

    def auto_configure_all(self):
        """Configure automatiquement toutes les manettes détectées"""
        print("=" * 60)
        print("KOF Ultimate - Auto-Configuration des Manettes")
        print("=" * 60)
        print()

        # Sauvegarder la config actuelle
        self.backup_config()

        # Détecter les manettes
        gamepads = self.detect_gamepads()

        if gamepads is None:
            print("\n⚠️  Veuillez relancer le script après l'installation de pygame")
            return False

        if not gamepads:
            print("\n❌ Aucune manette à configurer")
            print("\nConseil: Branchez votre manette et relancez ce script")
            return False

        print()
        print("-" * 60)

        # Configurer chaque manette détectée
        for gamepad in gamepads:
            player_num = gamepad["index"] + 1
            gamepad_type = self.identify_gamepad_type(gamepad["name"])

            print(f"\nManette {player_num}: {gamepad['name']}")
            self.configure_player(player_num, gamepad_type)

        print()
        print("-" * 60)
        print("✓ Configuration terminée!")
        print()
        print("📋 Résumé:")
        print(f"  - Manettes configurées: {len(gamepads)}")
        print(f"  - Backup sauvegardé: {self.config_file.with_suffix('.cfg.backup').name}")
        print()
        print("🎮 Vous pouvez maintenant jouer avec vos manettes!")
        print("=" * 60)

        return True

def main():
    """Point d'entrée principal"""
    configurator = GamepadConfigurator()
    result = configurator.auto_configure_all()

    # Ne pas bloquer si lancé en arrière-plan
    if sys.stdin.isatty():
        print()
        input("Appuyez sur Entrée pour quitter...")

    return result

if __name__ == "__main__":
    main()
