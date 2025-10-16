"""
KOF Ultimate - Gamepad Hot-Plug Monitor
Surveille en temps réel les branchements/débranchements de manettes
et reconfigure automatiquement le jeu
"""

import os
import sys
import time
import subprocess
from pathlib import Path
import configparser

try:
    import pygame
except ImportError:
    print("Installation de pygame...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pygame"])
    print("✓ pygame installé!")
    import pygame

GAME_PATH = Path("D:/KOF Ultimate")
CONFIG_FILE = GAME_PATH / "data" / "mugen.cfg"
CHECK_INTERVAL = 2  # Vérifier toutes les 2 secondes

class GamepadHotplugMonitor:
    """Surveille les manettes en temps réel"""

    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        self.current_gamepads = {}
        self.running = True

        print("=" * 60)
        print("KOF Ultimate - Gamepad Hot-Plug Monitor")
        print("=" * 60)
        print()
        print("⚡ Service actif!")
        print("   Ce service surveille les manettes en temps réel")
        print("   et les configure automatiquement.")
        print()
        print("🎮 État initial:")
        self.scan_gamepads()
        print()
        print("👁️  Surveillance active... (Ctrl+C pour arrêter)")
        print("-" * 60)
        print()

    def identify_gamepad_type(self, name):
        """Identifie le type de manette"""
        name_lower = name.lower()

        if "xbox" in name_lower or "x360" in name_lower or "xone" in name_lower:
            return "xbox"
        elif any(x in name_lower for x in ["playstation", "ps2", "ps3", "ps4", "ps5", "dualshock", "dualsense"]):
            return "playstation"
        else:
            return "generic"

    def configure_gamepad(self, player_num, gamepad_type, gamepad_name):
        """Configure une manette en temps réel"""
        if not CONFIG_FILE.exists():
            return False

        try:
            config = configparser.ConfigParser()
            config.optionxform = str
            config.read(CONFIG_FILE, encoding='utf-8')

            input_section = "Input"
            if input_section not in config:
                config.add_section(input_section)

            # Mappings selon le type
            if gamepad_type == "xbox":
                mappings = {
                    f"p{player_num}.joystick": "1",
                    f"p{player_num}.up": "~JOY_YAXIS",
                    f"p{player_num}.down": "JOY_YAXIS",
                    f"p{player_num}.left": "~JOY_XAXIS",
                    f"p{player_num}.right": "JOY_XAXIS",
                    f"p{player_num}.a": "JOY_1",
                    f"p{player_num}.b": "JOY_2",
                    f"p{player_num}.c": "JOY_4",
                    f"p{player_num}.x": "JOY_1",
                    f"p{player_num}.y": "JOY_3",
                    f"p{player_num}.z": "JOY_5",
                    f"p{player_num}.start": "JOY_8",
                    f"p{player_num}.pause": "JOY_8",
                }
            elif gamepad_type == "playstation":
                mappings = {
                    f"p{player_num}.joystick": "1",
                    f"p{player_num}.up": "~JOY_YAXIS",
                    f"p{player_num}.down": "JOY_YAXIS",
                    f"p{player_num}.left": "~JOY_XAXIS",
                    f"p{player_num}.right": "JOY_XAXIS",
                    f"p{player_num}.a": "JOY_3",
                    f"p{player_num}.b": "JOY_2",
                    f"p{player_num}.c": "JOY_4",
                    f"p{player_num}.x": "JOY_1",
                    f"p{player_num}.y": "JOY_3",
                    f"p{player_num}.z": "JOY_5",
                    f"p{player_num}.start": "JOY_10",
                    f"p{player_num}.pause": "JOY_10",
                }
            else:
                # Generic
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

            # Appliquer
            for key, value in mappings.items():
                config.set(input_section, key, value)

            # Sauvegarder
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                config.write(f, space_around_delimiters=True)

            return True

        except Exception as e:
            print(f"   ❌ Erreur configuration: {e}")
            return False

    def scan_gamepads(self):
        """Scanne les manettes actuellement connectées"""
        pygame.joystick.quit()
        pygame.joystick.init()

        current_count = pygame.joystick.get_count()
        new_gamepads = {}

        for i in range(current_count):
            try:
                joy = pygame.joystick.Joystick(i)
                joy.init()

                gamepad_id = f"{i}_{joy.get_name()}"
                new_gamepads[gamepad_id] = {
                    'index': i,
                    'name': joy.get_name(),
                    'type': self.identify_gamepad_type(joy.get_name())
                }

            except:
                pass

        return new_gamepads

    def monitor_loop(self):
        """Boucle de monitoring"""
        while self.running:
            try:
                # Scanner les manettes
                new_gamepads = self.scan_gamepads()

                # Détecter les changements
                added = set(new_gamepads.keys()) - set(self.current_gamepads.keys())
                removed = set(self.current_gamepads.keys()) - set(new_gamepads.keys())

                # Manettes ajoutées
                for gamepad_id in added:
                    gamepad = new_gamepads[gamepad_id]
                    player_num = gamepad['index'] + 1

                    print(f"🔌 BRANCHÉE: {gamepad['name']}")
                    print(f"   Type: {gamepad['type'].upper()}")
                    print(f"   Joueur: P{player_num}")
                    print("   Configuration automatique...")

                    if self.configure_gamepad(player_num, gamepad['type'], gamepad['name']):
                        print("   ✓ Configurée! Prête à l'emploi.")
                    else:
                        print("   ⚠️  Configuration partielle.")

                    print()

                # Manettes retirées
                for gamepad_id in removed:
                    gamepad = self.current_gamepads[gamepad_id]
                    print(f"🔌 DÉBRANCHÉE: {gamepad['name']}")
                    print()

                # Mettre à jour l'état actuel
                self.current_gamepads = new_gamepads

                # Attendre avant le prochain check
                time.sleep(CHECK_INTERVAL)

            except KeyboardInterrupt:
                print()
                print("-" * 60)
                print("🛑 Arrêt du monitoring...")
                self.running = False
                break

            except Exception as e:
                print(f"⚠️  Erreur: {e}")
                time.sleep(CHECK_INTERVAL)

        pygame.quit()
        print("✓ Service arrêté")
        print("=" * 60)

    def run(self):
        """Lance le monitoring"""
        self.monitor_loop()

def main():
    """Point d'entrée"""
    monitor = GamepadHotplugMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
