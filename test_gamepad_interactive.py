#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Interactif de Manette pour KOF Ultimate Online
Affiche en temps réel toutes les entrées de la manette
"""

import pygame
import sys
import time
from pathlib import Path

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def clear_screen():
    """Efface l'écran (compatible Windows/Linux)"""
    print('\033[2J\033[H', end='')

def draw_button_state(name, is_pressed):
    """Dessine l'état d'un bouton"""
    if is_pressed:
        return f"{Colors.GREEN}[{name}]{Colors.RESET}"
    else:
        return f"{Colors.WHITE}[ {' ' * len(name)} ]{Colors.RESET}"

def draw_axis_bar(value, width=20):
    """Dessine une barre pour visualiser un axe"""
    # Convertir value de [-1, 1] à [0, width]
    normalized = int((value + 1) * width / 2)
    bar = '█' * normalized + '░' * (width - normalized)

    if abs(value) < 0.1:
        color = Colors.WHITE
    elif abs(value) < 0.5:
        color = Colors.YELLOW
    else:
        color = Colors.GREEN

    return f"{color}{bar}{Colors.RESET} {value:+.2f}"

def test_gamepad():
    """Test interactif de la manette"""

    print(f"{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'TEST INTERACTIF DE MANETTE - KOF ULTIMATE ONLINE':^80}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

    # Initialiser pygame
    pygame.init()
    pygame.joystick.init()

    # Vérifier qu'une manette est connectée
    if pygame.joystick.get_count() == 0:
        print(f"{Colors.RED}✗ Aucune manette détectée !{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Veuillez :{Colors.RESET}")
        print(f"  1. Connecter votre manette")
        print(f"  2. Attendre que Windows la détecte")
        print(f"  3. Relancer ce script")
        return False

    # Initialiser la première manette
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Informations sur la manette
    print(f"{Colors.GREEN}✓ Manette détectée :{Colors.RESET} {joystick.get_name()}")
    print(f"{Colors.CYAN}  Axes        : {joystick.get_numaxes()}{Colors.RESET}")
    print(f"{Colors.CYAN}  Boutons     : {joystick.get_numbuttons()}{Colors.RESET}")
    print(f"{Colors.CYAN}  Chapeaux    : {joystick.get_numhats()}{Colors.RESET}")
    print()

    print(f"{Colors.YELLOW}Instructions :{Colors.RESET}")
    print(f"  • Testez tous les boutons et directions de votre manette")
    print(f"  • Les boutons pressés s'affichent en {Colors.GREEN}VERT{Colors.RESET}")
    print(f"  • Bougez les sticks pour voir les axes")
    print(f"  • Appuyez sur {Colors.RED}START + SELECT{Colors.RESET} pour quitter")
    print()
    print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}\n")

    time.sleep(2)

    # Mapping des boutons Xbox
    button_names = [
        "A", "B", "X", "Y",
        "LB", "RB", "SELECT", "START",
        "L3", "R3", "GUIDE"
    ]

    axis_names = [
        "Stick G X", "Stick G Y",
        "Stick D X", "Stick D Y",
        "LT", "RT"
    ]

    running = True
    frame_count = 0
    start_time = time.time()

    try:
        while running:
            frame_count += 1
            elapsed = time.time() - start_time

            # Traiter les événements pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Effacer l'écran
            clear_screen()

            # En-tête
            print(f"{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}")
            print(f"{Colors.CYAN}{Colors.BOLD}{'TEST INTERACTIF DE MANETTE':^80}{Colors.RESET}")
            print(f"{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

            print(f"{Colors.WHITE}Manette : {Colors.GREEN}{joystick.get_name()}{Colors.RESET}")
            print(f"{Colors.WHITE}Temps   : {elapsed:.1f}s  |  Frames : {frame_count}{Colors.RESET}")
            print()

            # Afficher les boutons
            print(f"{Colors.MAGENTA}{Colors.BOLD}BOUTONS :{Colors.RESET}")
            button_states = []
            for i in range(min(joystick.get_numbuttons(), len(button_names))):
                is_pressed = joystick.get_button(i)
                button_states.append((button_names[i] if i < len(button_names) else f"B{i}", is_pressed))

            # Afficher 4 boutons par ligne
            for row_start in range(0, len(button_states), 4):
                row = button_states[row_start:row_start+4]
                line = "  "
                for name, pressed in row:
                    line += draw_button_state(f"{name:^6}", pressed) + "  "
                print(line)

            print()

            # Afficher les axes
            print(f"{Colors.MAGENTA}{Colors.BOLD}AXES / STICKS :{Colors.RESET}")
            for i in range(min(joystick.get_numaxes(), len(axis_names))):
                axis_value = joystick.get_axis(i)
                axis_name = axis_names[i] if i < len(axis_names) else f"Axis {i}"
                print(f"  {axis_name:12} : {draw_axis_bar(axis_value)}")

            print()

            # Afficher le D-Pad (chapeaux)
            if joystick.get_numhats() > 0:
                print(f"{Colors.MAGENTA}{Colors.BOLD}D-PAD :{Colors.RESET}")
                hat = joystick.get_hat(0)
                dpad_display = "  "

                # Haut
                if hat[1] == 1:
                    dpad_display += f"{Colors.GREEN}↑{Colors.RESET} "
                else:
                    dpad_display += f"{Colors.WHITE}·{Colors.RESET} "

                # Bas
                if hat[1] == -1:
                    dpad_display += f"{Colors.GREEN}↓{Colors.RESET} "
                else:
                    dpad_display += f"{Colors.WHITE}·{Colors.RESET} "

                # Gauche
                if hat[0] == -1:
                    dpad_display += f"{Colors.GREEN}←{Colors.RESET} "
                else:
                    dpad_display += f"{Colors.WHITE}·{Colors.RESET} "

                # Droite
                if hat[0] == 1:
                    dpad_display += f"{Colors.GREEN}→{Colors.RESET}"
                else:
                    dpad_display += f"{Colors.WHITE}·{Colors.RESET}"

                print(dpad_display)
                print()

            # Instructions de sortie
            print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}")
            print(f"{Colors.YELLOW}Appuyez sur START + SELECT pour quitter{Colors.RESET}")

            # Vérifier si START + SELECT sont pressés
            if joystick.get_numbuttons() >= 8:
                if joystick.get_button(6) and joystick.get_button(7):  # SELECT + START
                    print(f"\n{Colors.GREEN}✓ Sortie détectée !{Colors.RESET}")
                    running = False

            # Limiter à ~30 FPS
            time.sleep(0.033)

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Test interrompu par l'utilisateur{Colors.RESET}")

    finally:
        # Nettoyer
        pygame.quit()

        print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}✓ Test terminé !{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")

        print(f"{Colors.WHITE}Statistiques :{Colors.RESET}")
        print(f"  • Durée totale  : {elapsed:.1f} secondes")
        print(f"  • Frames testés : {frame_count}")
        print(f"  • FPS moyen     : {frame_count/elapsed:.1f}")
        print()

        return True

if __name__ == "__main__":
    success = test_gamepad()
    sys.exit(0 if success else 1)
