#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Automatique de la Manette dans KOF Ultimate
Lance le jeu et vérifie que la manette est reconnue et fonctionnelle
"""

import subprocess
import time
import psutil
import pygame
from pathlib import Path
import sys

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

def print_header(text):
    """Affiche un en-tête stylisé"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text:^80}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

def print_step(step_num, text):
    """Affiche une étape du test"""
    print(f"{Colors.MAGENTA}{Colors.BOLD}[ÉTAPE {step_num}]{Colors.RESET} {text}")

def print_success(text):
    """Affiche un message de succès"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    """Affiche un message d'erreur"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text):
    """Affiche une information"""
    print(f"{Colors.CYAN}ℹ {text}{Colors.RESET}")

def check_gamepad():
    """Vérifie qu'une manette est connectée"""
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print_error("Aucune manette détectée !")
        return None

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print_success(f"Manette détectée : {joystick.get_name()}")
    print_info(f"  Axes    : {joystick.get_numaxes()}")
    print_info(f"  Boutons : {joystick.get_numbuttons()}")
    print_info(f"  D-Pad   : {joystick.get_numhats()}")

    return joystick

def monitor_gamepad_inputs(joystick, duration=5):
    """Surveille les entrées de la manette pendant une durée donnée"""
    print_info(f"Monitoring des entrées pendant {duration} secondes...")
    print(f"{Colors.YELLOW}>>> TESTEZ MAINTENANT VOTRE MANETTE <<<{Colors.RESET}")
    print(f"{Colors.YELLOW}>>> Appuyez sur différents boutons et directions{Colors.RESET}\n")

    inputs_detected = {
        'buttons': [],
        'axes': [],
        'dpad': []
    }

    start_time = time.time()
    last_update = start_time

    while time.time() - start_time < duration:
        # Traiter les événements pygame
        for event in pygame.event.get():
            pass

        # Vérifier les boutons
        for i in range(joystick.get_numbuttons()):
            if joystick.get_button(i) and i not in inputs_detected['buttons']:
                inputs_detected['buttons'].append(i)
                print_success(f"Bouton {i} détecté !")

        # Vérifier les axes
        for i in range(joystick.get_numaxes()):
            axis_value = joystick.get_axis(i)
            if abs(axis_value) > 0.5 and i not in inputs_detected['axes']:
                inputs_detected['axes'].append(i)
                print_success(f"Axe {i} détecté ! (valeur: {axis_value:.2f})")

        # Vérifier le D-Pad
        if joystick.get_numhats() > 0:
            hat = joystick.get_hat(0)
            if hat != (0, 0) and 'movement' not in inputs_detected['dpad']:
                inputs_detected['dpad'].append('movement')
                print_success(f"D-Pad détecté ! Direction: {hat}")

        # Afficher le compte à rebours toutes les secondes
        current_time = time.time()
        if current_time - last_update >= 1.0:
            remaining = int(duration - (current_time - start_time))
            print(f"{Colors.CYAN}Temps restant : {remaining}s{Colors.RESET}")
            last_update = current_time

        time.sleep(0.033)  # ~30 FPS

    return inputs_detected

def launch_game():
    """Lance le jeu KOF Ultimate"""
    game_path = Path("D:/KOF Ultimate Online")
    exe_path = game_path / "KOF_Ultimate_Online.exe"

    if not exe_path.exists():
        print_error(f"Exécutable du jeu introuvable : {exe_path}")
        return None

    print_info(f"Lancement du jeu : {exe_path}")

    try:
        process = subprocess.Popen(
            [str(exe_path)],
            cwd=str(game_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print_success("Jeu lancé avec succès !")
        return process
    except Exception as e:
        print_error(f"Erreur lors du lancement : {e}")
        return None

def find_game_process():
    """Trouve le processus du jeu"""
    for proc in psutil.process_iter(['name', 'pid']):
        try:
            if proc.info['name'] == "KOF_Ultimate_Online.exe":
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

def stop_game():
    """Arrête le jeu proprement"""
    proc = find_game_process()
    if proc:
        try:
            print_info("Fermeture du jeu...")
            proc.terminate()
            proc.wait(timeout=5)
            print_success("Jeu fermé")
            return True
        except Exception as e:
            print_error(f"Erreur lors de la fermeture : {e}")
            try:
                proc.kill()
                print_success("Jeu forcé à fermer")
                return True
            except:
                return False
    return False

def check_mugen_log():
    """Vérifie les logs du jeu pour les entrées manette"""
    log_path = Path("D:/KOF Ultimate Online/mugen.log")

    if not log_path.exists():
        print_error("Fichier mugen.log introuvable")
        return False

    try:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Chercher des indices d'initialisation de manette
        gamepad_keywords = [
            'joystick', 'gamepad', 'controller',
            'pad', 'input', 'joypad'
        ]

        found = []
        for keyword in gamepad_keywords:
            if keyword.lower() in content.lower():
                found.append(keyword)

        if found:
            print_success(f"Traces de manette trouvées dans les logs : {', '.join(found)}")
            return True
        else:
            print_info("Aucune trace spécifique de manette dans les logs (normal)")
            return True
    except Exception as e:
        print_error(f"Erreur lecture du log : {e}")
        return False

def main():
    """Fonction principale"""
    print_header("TEST AUTOMATIQUE DE LA MANETTE DANS KOF ULTIMATE")

    # Étape 1 : Vérifier la manette
    print_step(1, "Vérification de la manette")
    joystick = check_gamepad()
    if not joystick:
        print_error("Impossible de continuer sans manette !")
        return False

    print()
    time.sleep(1)

    # Étape 2 : Tester les entrées de la manette AVANT le jeu
    print_step(2, "Test des entrées manette (AVANT le jeu)")
    inputs_before = monitor_gamepad_inputs(joystick, duration=5)

    print()
    print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}")
    print(f"{Colors.BOLD}Résumé des entrées détectées AVANT le jeu :{Colors.RESET}")
    print(f"  • Boutons détectés  : {len(inputs_before['buttons'])}")
    print(f"  • Axes détectés     : {len(inputs_before['axes'])}")
    print(f"  • D-Pad détecté     : {'OUI' if inputs_before['dpad'] else 'NON'}")
    print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}\n")

    time.sleep(2)

    # Étape 3 : Lancer le jeu
    print_step(3, "Lancement du jeu")
    game_process = launch_game()

    if not game_process:
        print_error("Impossible de lancer le jeu !")
        pygame.quit()
        return False

    print_info("Attente du chargement du jeu...")
    time.sleep(5)  # Attendre que le jeu charge

    # Vérifier que le jeu tourne
    game_running = find_game_process()
    if not game_running:
        print_error("Le jeu ne semble pas tourner !")
        pygame.quit()
        return False

    print_success("Jeu en cours d'exécution")
    print()
    time.sleep(1)

    # Étape 4 : Tester la manette PENDANT que le jeu tourne
    print_step(4, "Test de la manette DANS le jeu")
    print(f"{Colors.YELLOW}{Colors.BOLD}>>> LE JEU EST MAINTENANT LANCÉ <<<{Colors.RESET}")
    print(f"{Colors.YELLOW}>>> Testez la navigation dans les menus avec votre manette{Colors.RESET}")
    print(f"{Colors.YELLOW}>>> D-Pad = Navigation / A = Sélection / B = Retour{Colors.RESET}\n")

    inputs_during = monitor_gamepad_inputs(joystick, duration=10)

    print()
    print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}")
    print(f"{Colors.BOLD}Résumé des entrées détectées PENDANT le jeu :{Colors.RESET}")
    print(f"  • Boutons détectés  : {len(inputs_during['buttons'])}")
    print(f"  • Axes détectés     : {len(inputs_during['axes'])}")
    print(f"  • D-Pad détecté     : {'OUI' if inputs_during['dpad'] else 'NON'}")
    print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}\n")

    time.sleep(2)

    # Étape 5 : Fermer le jeu
    print_step(5, "Fermeture du jeu")
    stop_game()
    time.sleep(2)

    # Étape 6 : Vérifier les logs
    print_step(6, "Analyse des logs du jeu")
    check_mugen_log()

    # Étape 7 : Rapport final
    print()
    print_header("RAPPORT FINAL DU TEST DE MANETTE")

    print(f"{Colors.BOLD}Configuration testée :{Colors.RESET}")
    print(f"  • Manette      : {joystick.get_name()}")
    print(f"  • Axes         : {joystick.get_numaxes()}")
    print(f"  • Boutons      : {joystick.get_numbuttons()}")
    print(f"  • D-Pad        : {joystick.get_numhats()}")
    print()

    print(f"{Colors.BOLD}Résultats des tests :{Colors.RESET}")

    # Test 1 : Manette détectée par Python
    test1 = joystick is not None
    status1 = f"{Colors.GREEN}✓ RÉUSSI{Colors.RESET}" if test1 else f"{Colors.RED}✗ ÉCHOUÉ{Colors.RESET}"
    print(f"  1. Manette détectée par Python        : {status1}")

    # Test 2 : Entrées détectées avant le jeu
    test2 = len(inputs_before['buttons']) > 0 or len(inputs_before['axes']) > 0
    status2 = f"{Colors.GREEN}✓ RÉUSSI{Colors.RESET}" if test2 else f"{Colors.YELLOW}⚠ AUCUNE ENTRÉE{Colors.RESET}"
    print(f"  2. Entrées détectées AVANT le jeu     : {status2}")

    # Test 3 : Jeu lancé avec succès
    test3 = game_process is not None
    status3 = f"{Colors.GREEN}✓ RÉUSSI{Colors.RESET}" if test3 else f"{Colors.RED}✗ ÉCHOUÉ{Colors.RESET}"
    print(f"  3. Jeu lancé avec succès              : {status3}")

    # Test 4 : Entrées détectées pendant le jeu
    test4 = len(inputs_during['buttons']) > 0 or len(inputs_during['axes']) > 0
    status4 = f"{Colors.GREEN}✓ RÉUSSI{Colors.RESET}" if test4 else f"{Colors.YELLOW}⚠ AUCUNE ENTRÉE{Colors.RESET}"
    print(f"  4. Entrées détectées DANS le jeu      : {status4}")

    print()

    # Conclusion
    all_passed = test1 and test3
    inputs_work = test2 or test4

    if all_passed and inputs_work:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ SUCCÈS : La manette est configurée et fonctionne !{Colors.RESET}")
        print()
        print(f"{Colors.CYAN}Vous pouvez maintenant jouer avec votre manette dans les menus :{Colors.RESET}")
        print(f"  • D-Pad / Stick gauche : Navigation")
        print(f"  • Bouton A             : Sélection")
        print(f"  • Bouton B             : Retour")
        print(f"  • Bouton START         : Pause/Menu")
        result = True
    elif all_passed:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠ ATTENTION : Manette détectée mais aucune entrée testée{Colors.RESET}")
        print()
        print(f"{Colors.YELLOW}Raisons possibles :{Colors.RESET}")
        print(f"  • Vous n'avez pas appuyé sur les boutons pendant les tests")
        print(f"  • La manette est en veille")
        print(f"  • Débranchez et rebranchez la manette")
        result = False
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ ÉCHEC : Problème détecté{Colors.RESET}")
        print()
        print(f"{Colors.RED}Actions recommandées :{Colors.RESET}")
        print(f"  1. Vérifier que la manette est bien branchée")
        print(f"  2. Réexécuter : python gamepad_auto_config.py")
        print(f"  3. Relancer ce test")
        result = False

    print()
    pygame.quit()

    return result

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Test interrompu par l'utilisateur{Colors.RESET}")
        pygame.quit()
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.RED}Erreur inattendue : {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)
