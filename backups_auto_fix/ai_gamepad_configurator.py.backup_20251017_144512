"""
KOF Ultimate - Configurateur IA de Manette
Détecte et configure automatiquement votre manette pour KOF Ultimate
"""

import os
import sys
import time
import pygame
import configparser
from pathlib import Path

# Initialiser pygame pour la détection de manette
pygame.init()
pygame.joystick.init()

class AIGamepadConfigurator:
    """IA qui configure automatiquement la manette"""

    def __init__(self):
        self.config_path = Path("D:/KOF Ultimate Online/data/mugen.cfg")
        self.joystick = None

    def detect_gamepad(self):
        """Détecte la manette connectée"""
        print("\n🎮 Détection de la manette...")
        print("=" * 60)

        joystick_count = pygame.joystick.get_count()
        print(f"Nombre de manettes détectées: {joystick_count}")

        if joystick_count == 0:
            print("❌ Aucune manette détectée!")
            print("\nAssurez-vous que:")
            print("  1. La manette est branchée")
            print("  2. Les drivers sont installés")
            print("  3. La manette fonctionne dans Windows")
            return False

        # Initialiser la première manette
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        print(f"\n✓ Manette détectée: {self.joystick.get_name()}")
        print(f"  - Axes: {self.joystick.get_numaxes()}")
        print(f"  - Boutons: {self.joystick.get_numbuttons()}")
        print(f"  - Hats (D-Pad): {self.joystick.get_numhats()}")

        return True

    def test_gamepad_input(self):
        """Teste les entrées de la manette"""
        print("\n🧪 Test de la manette...")
        print("=" * 60)
        print("Bougez les sticks et appuyez sur les boutons!")
        print("(Appuyez sur Start ou attendez 10 secondes pour continuer)\n")

        start_time = time.time()
        button_pressed = [False] * self.joystick.get_numbuttons()
        axes_moved = [False] * self.joystick.get_numaxes()
        hat_moved = False

        while time.time() - start_time < 10:
            pygame.event.pump()

            # Tester les axes
            for i in range(self.joystick.get_numaxes()):
                axis_value = self.joystick.get_axis(i)
                if abs(axis_value) > 0.5 and not axes_moved[i]:
                    print(f"  ✓ Axe {i}: {axis_value:.2f}")
                    axes_moved[i] = True

            # Tester les boutons
            for i in range(self.joystick.get_numbuttons()):
                if self.joystick.get_button(i) and not button_pressed[i]:
                    print(f"  ✓ Bouton {i} pressé")
                    button_pressed[i] = True

                    # Si bouton Start (généralement 7 ou 9)
                    if i in [7, 9]:
                        print("\n✓ Bouton Start détecté - Test terminé!")
                        return True

            # Tester le D-Pad
            for i in range(self.joystick.get_numhats()):
                hat = self.joystick.get_hat(i)
                if hat != (0, 0) and not hat_moved:
                    print(f"  ✓ D-Pad {i}: {hat}")
                    hat_moved = True

            time.sleep(0.1)

        print("\n✓ Test terminé!")
        return True

    def configure_mugen(self):
        """Configure automatiquement MUGEN pour la manette"""
        print("\n⚙️  Configuration automatique de MUGEN...")
        print("=" * 60)

        try:
            # Lire le fichier de configuration
            config = configparser.ConfigParser()
            config.read(self.config_path, encoding='utf-8')

            # Activer la manette pour P1
            if 'Input' not in config:
                config['Input'] = {}

            print("Configuration de Player 1...")
            config['Input']['P1.UseKeyboard'] = '1'  # Garder le clavier aussi
            config['Input']['P1.Joystick.type'] = '1'  # Auto-detect
            config['Input']['p1.joystick'] = '1'  # Activer joystick 1

            # Configuration des axes (stick analogique gauche)
            config['Input']['p1.up'] = '~JOY_YAXIS'
            config['Input']['p1.down'] = 'JOY_YAXIS'
            config['Input']['p1.left'] = '~JOY_XAXIS'
            config['Input']['p1.right'] = 'JOY_XAXIS'

            # Configuration des boutons (layout Xbox)
            config['Input']['p1.a'] = 'JOY_1'  # Bouton A (Xbox B)
            config['Input']['p1.b'] = 'JOY_2'  # Bouton B (Xbox A)
            config['Input']['p1.c'] = 'JOY_4'  # Bouton Y
            config['Input']['p1.x'] = 'JOY_1'  # Bouton A
            config['Input']['p1.y'] = 'JOY_3'  # Bouton X
            config['Input']['p1.z'] = 'JOY_5'  # LB
            config['Input']['p1.start'] = 'JOY_8'  # Start
            config['Input']['p1.pause'] = 'JOY_8'  # Start

            # Configuration alternative avec D-Pad (P1 Joystick section)
            if 'P1 Joystick' not in config:
                config['P1 Joystick'] = {}

            print("Configuration D-Pad et boutons...")
            config['P1 Joystick']['Jump'] = '~0'  # D-Pad Up
            config['P1 Joystick']['Crouch'] = '0'  # D-Pad Down
            config['P1 Joystick']['Left'] = '~1'  # D-Pad Left
            config['P1 Joystick']['Right'] = '1'  # D-Pad Right
            config['P1 Joystick']['A'] = '0'  # Bouton A
            config['P1 Joystick']['B'] = '1'  # Bouton B
            config['P1 Joystick']['C'] = '3'  # Bouton Y
            config['P1 Joystick']['X'] = '0'  # Bouton A
            config['P1 Joystick']['Y'] = '2'  # Bouton X
            config['P1 Joystick']['Z'] = '4'  # LB
            config['P1 Joystick']['Start'] = '7'  # Start

            # Sauvegarder la configuration
            with open(self.config_path, 'w', encoding='utf-8') as f:
                config.write(f)

            print("✓ Configuration sauvegardée!")

            return True

        except Exception as e:
            print(f"❌ Erreur lors de la configuration: {e}")
            return False

    def run(self):
        """Lance le processus complet de configuration"""
        print("\n" + "=" * 60)
        print("🤖 CONFIGURATEUR IA DE MANETTE")
        print("=" * 60)

        # Étape 1: Détecter la manette
        if not self.detect_gamepad():
            print("\n❌ Impossible de continuer sans manette")
            return False

        # Étape 2: Tester la manette
        time.sleep(1)
        self.test_gamepad_input()

        # Étape 3: Configurer MUGEN
        time.sleep(1)
        if not self.configure_mugen():
            return False

        # Étape 4: Instructions finales
        print("\n" + "=" * 60)
        print("✓ CONFIGURATION TERMINÉE!")
        print("=" * 60)
        print("\n📋 Instructions:")
        print("  1. Lancez KOF Ultimate")
        print("  2. Testez la manette dans le jeu")
        print("  3. Si ça ne fonctionne pas, utilisez l'option 'Config' du launcher")
        print("\n💡 Mapping des boutons (Xbox):")
        print("  - Stick gauche / D-Pad: Mouvements")
        print("  - A (vert): Coup léger")
        print("  - B (rouge): Coup moyen")
        print("  - X (bleu): Coup fort")
        print("  - Y (jaune): Coup spécial")
        print("  - LB: Action supplémentaire")
        print("  - Start: Pause/Menu")
        print()

        return True

if __name__ == "__main__":
    configurator = AIGamepadConfigurator()
    success = configurator.run()

    if success:
        print("✓ La manette est maintenant configurée!")
        print("  Appuyez sur Entrée pour quitter...")
    else:
        print("❌ La configuration a échoué")
        print("  Appuyez sur Entrée pour quitter...")

    input()
    pygame.quit()
