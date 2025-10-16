"""
KOF Ultimate - Mapper Manette vers Clavier
Solution ultime: Mappe la manette directement au clavier en temps réel
"""

import pygame
import pyautogui
import time
import sys

# Initialiser pygame
pygame.init()
pygame.joystick.init()

class GamepadMapper:
    """Mappe la manette au clavier en temps réel"""

    def __init__(self):
        self.joystick = None
        self.running = True

        # Mapping manette -> clavier pour KOF
        self.button_mapping = {
            0: 's',      # A -> S (coup léger)
            1: 'd',      # B -> D (coup moyen)
            2: 'f',      # X -> F (coup fort)
            3: 'g',      # Y -> G (spécial)
            7: 'return', # Start -> Entrée
            6: 'escape', # Back -> Échap
        }

        self.last_button_state = {}
        self.last_axis_state = {}

    def initialize_gamepad(self):
        """Initialise la manette"""
        joystick_count = pygame.joystick.get_count()

        if joystick_count == 0:
            print("❌ Aucune manette détectée!")
            return False

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        print(f"✓ Manette connectée: {self.joystick.get_name()}")
        print(f"  - {self.joystick.get_numbuttons()} boutons")
        print(f"  - {self.joystick.get_numaxes()} axes")

        # Initialiser les états
        for i in range(self.joystick.get_numbuttons()):
            self.last_button_state[i] = False

        return True

    def handle_axes(self):
        """Gère les axes (mouvements)"""
        # Stick gauche
        left_x = self.joystick.get_axis(0)
        left_y = self.joystick.get_axis(1)

        # D-Pad (si disponible)
        if self.joystick.get_numhats() > 0:
            hat = self.joystick.get_hat(0)

            # D-Pad prioritaire
            if hat[0] == -1:  # Gauche
                pyautogui.keyDown('left')
                if self.last_axis_state.get('right', False):
                    pyautogui.keyUp('right')
                self.last_axis_state['left'] = True
            elif hat[0] == 1:  # Droite
                pyautogui.keyDown('right')
                if self.last_axis_state.get('left', False):
                    pyautogui.keyUp('left')
                self.last_axis_state['right'] = True
            else:
                # Relâcher gauche/droite
                if self.last_axis_state.get('left', False):
                    pyautogui.keyUp('left')
                    self.last_axis_state['left'] = False
                if self.last_axis_state.get('right', False):
                    pyautogui.keyUp('right')
                    self.last_axis_state['right'] = False

            if hat[1] == -1:  # Bas
                pyautogui.keyDown('down')
                if self.last_axis_state.get('up', False):
                    pyautogui.keyUp('up')
                self.last_axis_state['down'] = True
            elif hat[1] == 1:  # Haut
                pyautogui.keyDown('up')
                if self.last_axis_state.get('down', False):
                    pyautogui.keyUp('down')
                self.last_axis_state['up'] = True
            else:
                # Relâcher haut/bas
                if self.last_axis_state.get('up', False):
                    pyautogui.keyUp('up')
                    self.last_axis_state['up'] = False
                if self.last_axis_state.get('down', False):
                    pyautogui.keyUp('down')
                    self.last_axis_state['down'] = False
        else:
            # Utiliser le stick analogique
            threshold = 0.5

            # Horizontal
            if left_x < -threshold:  # Gauche
                pyautogui.keyDown('left')
                if self.last_axis_state.get('right', False):
                    pyautogui.keyUp('right')
                self.last_axis_state['left'] = True
            elif left_x > threshold:  # Droite
                pyautogui.keyDown('right')
                if self.last_axis_state.get('left', False):
                    pyautogui.keyUp('left')
                self.last_axis_state['right'] = True
            else:
                if self.last_axis_state.get('left', False):
                    pyautogui.keyUp('left')
                    self.last_axis_state['left'] = False
                if self.last_axis_state.get('right', False):
                    pyautogui.keyUp('right')
                    self.last_axis_state['right'] = False

            # Vertical
            if left_y < -threshold:  # Haut
                pyautogui.keyDown('up')
                if self.last_axis_state.get('down', False):
                    pyautogui.keyUp('down')
                self.last_axis_state['up'] = True
            elif left_y > threshold:  # Bas
                pyautogui.keyDown('down')
                if self.last_axis_state.get('up', False):
                    pyautogui.keyUp('up')
                self.last_axis_state['down'] = True
            else:
                if self.last_axis_state.get('up', False):
                    pyautogui.keyUp('up')
                    self.last_axis_state['up'] = False
                if self.last_axis_state.get('down', False):
                    pyautogui.keyUp('down')
                    self.last_axis_state['down'] = False

    def handle_buttons(self):
        """Gère les boutons"""
        for i in range(self.joystick.get_numbuttons()):
            button_pressed = self.joystick.get_button(i)

            # Détection des changements d'état
            if button_pressed and not self.last_button_state[i]:
                # Bouton vient d'être pressé
                if i in self.button_mapping:
                    key = self.button_mapping[i]
                    pyautogui.keyDown(key)
                    print(f"→ Bouton {i} → {key}")
            elif not button_pressed and self.last_button_state[i]:
                # Bouton vient d'être relâché
                if i in self.button_mapping:
                    key = self.button_mapping[i]
                    pyautogui.keyUp(key)

            self.last_button_state[i] = button_pressed

    def run(self):
        """Boucle principale"""
        if not self.initialize_gamepad():
            return

        print("\n" + "=" * 60)
        print("🎮 MAPPER ACTIF - Manette → Clavier")
        print("=" * 60)
        print()
        print("Mapping:")
        print("  D-Pad/Stick : Flèches directionnelles")
        print("  A (0)       : S")
        print("  B (1)       : D")
        print("  X (2)       : F")
        print("  Y (3)       : G")
        print("  Start (7)   : Entrée")
        print("  Back (6)    : Échap")
        print()
        print("Appuyez sur Ctrl+C pour arrêter")
        print("=" * 60)
        print()

        try:
            while self.running:
                # Lire les événements pygame
                pygame.event.pump()

                # Gérer les axes
                self.handle_axes()

                # Gérer les boutons
                self.handle_buttons()

                # Petit délai pour éviter la surcharge CPU
                time.sleep(0.01)

        except KeyboardInterrupt:
            print("\n")
            print("✓ Mapper arrêté")

            # Relâcher toutes les touches
            for key in ['up', 'down', 'left', 'right', 's', 'd', 'f', 'g', 'return', 'escape']:
                try:
                    pyautogui.keyUp(key)
                except:
                    pass

        pygame.quit()

if __name__ == "__main__":
    print("\n")
    print("=" * 60)
    print("🎮 MAPPER MANETTE → CLAVIER pour KOF ULTIMATE")
    print("=" * 60)
    print()
    print("Ce programme convertit votre manette en entrées clavier")
    print("en temps réel pour que vous puissiez ENFIN jouer!")
    print()

    mapper = GamepadMapper()
    mapper.run()
