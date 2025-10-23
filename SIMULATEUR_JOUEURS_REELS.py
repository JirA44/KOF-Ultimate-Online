#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMULATEUR DE JOUEURS RÉELS - KOF Ultimate Online
Simule de vrais joueurs qui parcourent les menus et jouent
"""

import subprocess
import time
import random
import json
import os
from datetime import datetime
import pyautogui
import threading
from pathlib import Path

# Configuration
GAME_EXE = "KOF_Ultimate_Online.exe"
GAME_PATH = Path(__file__).parent
LOG_DIR = GAME_PATH / "logs" / "player_simulation"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Profils de joueurs simulés
PLAYER_PROFILES = {
    "debutant_curieux": {
        "name": "Débutant Curieux",
        "behavior": "explore_menus",
        "skill": "beginner",
        "patience": "low",  # Abandonne si trop compliqué
        "actions_per_minute": 5,
        "menu_exploration_time": 60,  # 1 minute à explorer
        "play_duration": 180,  # 3 minutes de jeu
    },
    "casual_player": {
        "name": "Joueur Casual",
        "behavior": "quick_play",
        "skill": "intermediate",
        "patience": "medium",
        "actions_per_minute": 10,
        "menu_exploration_time": 20,
        "play_duration": 600,  # 10 minutes
    },
    "competitive_player": {
        "name": "Joueur Compétitif",
        "behavior": "ranked_focused",
        "skill": "advanced",
        "patience": "high",
        "actions_per_minute": 15,
        "menu_exploration_time": 10,
        "play_duration": 1800,  # 30 minutes
    },
    "button_masher": {
        "name": "Button Masher",
        "behavior": "spam_everything",
        "skill": "none",
        "patience": "very_low",
        "actions_per_minute": 30,  # Spam rapide
        "menu_exploration_time": 5,
        "play_duration": 300,
    }
}

class PlayerSimulator:
    """Simule un joueur réel"""

    def __init__(self, profile_name):
        self.profile = PLAYER_PROFILES[profile_name]
        self.profile_name = profile_name
        self.log_file = LOG_DIR / f"{profile_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.issues_found = []
        self.session_data = {
            "player_profile": profile_name,
            "start_time": datetime.now().isoformat(),
            "actions_performed": [],
            "errors_encountered": [],
            "ux_issues": [],
            "menu_navigation": [],
            "gameplay_events": []
        }

    def log(self, message, level="INFO"):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] [{level}] {self.profile['name']}: {message}"
        print(log_msg)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_msg + "\n")

    def report_issue(self, issue_type, description):
        """Rapporte un problème UX ou bug"""
        issue = {
            "time": datetime.now().isoformat(),
            "type": issue_type,
            "description": description,
            "player_profile": self.profile_name
        }
        self.issues_found.append(issue)
        self.session_data["ux_issues"].append(issue)
        self.log(f"ISSUE - {issue_type}: {description}", "WARNING")

    def wait_for_game_window(self, timeout=30):
        """Attend que la fenêtre du jeu apparaisse"""
        self.log("Attente de la fenêtre du jeu...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # Cherche la fenêtre Ikemen
                windows = pyautogui.getAllTitles()
                for window in windows:
                    if "KOF" in window or "Ikemen" in window or "MUGEN" in window:
                        self.log(f"✓ Fenêtre trouvée: {window}")
                        time.sleep(2)  # Attendre que la fenêtre soit prête
                        return True
            except:
                pass
            time.sleep(1)

        self.report_issue("LAUNCH_FAILURE", "Fenêtre du jeu introuvable après 30s")
        return False

    def navigate_menu(self, direction, times=1):
        """Navigue dans les menus"""
        key_map = {
            "down": "down",
            "up": "up",
            "left": "left",
            "right": "right",
            "select": "return",
            "back": "escape"
        }

        key = key_map.get(direction, direction)
        for _ in range(times):
            pyautogui.press(key)
            self.session_data["menu_navigation"].append({
                "time": datetime.now().isoformat(),
                "action": direction
            })
            time.sleep(random.uniform(0.3, 0.8))  # Délai humain

    def explore_menus_as_beginner(self):
        """Explore les menus comme un débutant"""
        self.log("=== EXPLORATION DES MENUS (Débutant) ===")

        # Attendre l'écran titre
        time.sleep(5)
        self.log("Écran titre visible?")

        # Appuyer sur START pour entrer
        pyautogui.press('space')
        time.sleep(2)

        self.log("Exploration du menu principal...")

        # Explorer chaque option du menu principal
        menu_options = ["Arcade", "Versus", "Team Arcade", "Team Versus",
                       "Team Co-op", "Survival", "Training", "Watch",
                       "Network", "Options"]

        for i, option in enumerate(menu_options):
            self.log(f"Navigation vers: {option}")

            # Descendre au menu suivant
            self.navigate_menu("down")
            time.sleep(random.uniform(1, 3))  # Temps de lecture

            # Comportement débutant: parfois se perdre
            if random.random() < 0.2:  # 20% chance
                self.log("Confusion - retour en arrière")
                self.navigate_menu("up", random.randint(1, 3))
                time.sleep(1)

    def explore_menus_as_casual(self):
        """Explore rapidement pour aller jouer"""
        self.log("=== NAVIGATION RAPIDE VERS JEU ===")

        time.sleep(5)
        pyautogui.press('space')  # Skip titre
        time.sleep(1)

        # Va directement à Versus
        self.log("Recherche du mode Versus...")
        self.navigate_menu("down", 1)
        time.sleep(0.5)
        self.navigate_menu("select")
        time.sleep(2)

        self.log("Écran de sélection des personnages")

    def spam_buttons_test(self):
        """Test de spam de boutons (stress test)"""
        self.log("=== TEST SPAM BOUTONS ===")

        time.sleep(5)

        # Spam rapide
        buttons = ['space', 'return', 'up', 'down', 'left', 'right', 'escape']

        self.log("Spam de 50 touches aléatoires...")
        for _ in range(50):
            btn = random.choice(buttons)
            pyautogui.press(btn)
            time.sleep(random.uniform(0.05, 0.2))  # Très rapide

        self.log("Test spam terminé - jeu toujours stable?")

    def select_character(self):
        """Sélectionne un personnage"""
        self.log("Sélection de personnage...")

        # Navigation aléatoire dans la grille
        moves = random.randint(5, 15)
        for _ in range(moves):
            direction = random.choice(["up", "down", "left", "right"])
            self.navigate_menu(direction)

        # Maintenir START + ENTER pour forcer mode manuel
        self.log("Sélection (avec START pour mode manuel)")

        # Simuler maintien de START
        pyautogui.keyDown('space')
        time.sleep(0.3)
        pyautogui.press('return')
        time.sleep(0.5)
        pyautogui.keyUp('space')

        time.sleep(3)  # Attendre chargement

    def play_match(self, duration):
        """Simule un match"""
        self.log(f"=== DÉBUT DU MATCH ({duration}s) ===")

        start_time = time.time()
        action_count = 0

        # Touches de combat
        combat_keys = ['a', 's', 'z', 'x', 'up', 'down', 'left', 'right']

        while time.time() - start_time < duration:
            # Simulation de gameplay
            skill = self.profile['skill']

            if skill == "beginner":
                # Débutant: boutons aléatoires
                key = random.choice(combat_keys)
                pyautogui.press(key)
                time.sleep(random.uniform(0.5, 1.5))

            elif skill == "intermediate":
                # Casual: quelques combos simples
                if random.random() < 0.3:
                    # Combo simple
                    pyautogui.press('a')
                    time.sleep(0.1)
                    pyautogui.press('s')
                    time.sleep(0.1)
                else:
                    key = random.choice(combat_keys)
                    pyautogui.press(key)
                    time.sleep(random.uniform(0.3, 0.8))

            elif skill == "advanced":
                # Compétitif: combos complexes
                if random.random() < 0.5:
                    combo = ['down', 'right', 'a', 's']
                    for key in combo:
                        pyautogui.press(key)
                        time.sleep(0.08)
                else:
                    key = random.choice(combat_keys)
                    pyautogui.press(key)
                    time.sleep(random.uniform(0.2, 0.5))
            else:
                # Button masher
                key = random.choice(combat_keys)
                pyautogui.press(key)
                time.sleep(random.uniform(0.05, 0.15))

            action_count += 1

            # Log périodique
            if action_count % 50 == 0:
                self.log(f"Actions effectuées: {action_count}")

        self.log(f"Match terminé - {action_count} actions effectuées")
        self.session_data["gameplay_events"].append({
            "duration": duration,
            "actions": action_count,
            "apm": action_count / (duration / 60)
        })

    def test_pause_menu(self):
        """Test du menu pause"""
        self.log("Test menu pause...")

        pyautogui.press('escape')
        time.sleep(1)
        self.navigate_menu("down", 2)
        time.sleep(1)
        pyautogui.press('escape')  # Retour
        time.sleep(1)

    def run_session(self):
        """Lance une session complète de test"""
        self.log("="*60)
        self.log(f"DÉBUT SESSION - Profil: {self.profile['name']}")
        self.log("="*60)

        try:
            # Lancer le jeu
            self.log("Lancement du jeu...")
            game_path = GAME_PATH / GAME_EXE

            if not game_path.exists():
                self.report_issue("CRITICAL", f"Exécutable introuvable: {game_path}")
                return

            subprocess.Popen(str(game_path), cwd=str(GAME_PATH))

            # Attendre fenêtre
            if not self.wait_for_game_window():
                return

            # Phase d'exploration menus
            behavior = self.profile['behavior']

            if behavior == "explore_menus":
                self.explore_menus_as_beginner()
            elif behavior == "quick_play":
                self.explore_menus_as_casual()
            elif behavior == "spam_everything":
                self.spam_buttons_test()
            else:
                self.explore_menus_as_casual()

            # Phase de jeu
            if behavior != "explore_menus":  # Débutant reste dans les menus
                self.log("Lancement d'un match...")
                self.select_character()
                time.sleep(5)  # Attendre écran VS

                # Jouer
                play_time = self.profile['play_duration']

                # Match complet
                self.play_match(play_time)

                # Test pause
                if random.random() < 0.5:
                    self.test_pause_menu()

            # Retour menu
            self.log("Retour au menu principal...")
            pyautogui.press('escape')
            time.sleep(2)

        except Exception as e:
            self.log(f"ERREUR: {str(e)}", "ERROR")
            self.report_issue("CRASH", str(e))

        finally:
            self.save_session_data()

    def save_session_data(self):
        """Sauvegarde les données de session"""
        self.session_data["end_time"] = datetime.now().isoformat()
        self.session_data["issues_found"] = len(self.issues_found)

        json_file = LOG_DIR / f"{self.profile_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, indent=2, ensure_ascii=False)

        self.log(f"Session data sauvegardée: {json_file}")


class MultiPlayerSimulation:
    """Gère plusieurs joueurs simultanés"""

    def __init__(self, num_players=4):
        self.num_players = num_players
        self.simulators = []
        self.report_file = LOG_DIR / f"RAPPORT_MULTI_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    def run_concurrent_tests(self, rounds=3):
        """Lance plusieurs rounds de tests"""
        print("="*80)
        print("SIMULATION MULTI-JOUEURS - KOF ULTIMATE ONLINE")
        print("="*80)

        for round_num in range(1, rounds + 1):
            print(f"\n{'='*80}")
            print(f"ROUND {round_num}/{rounds}")
            print(f"{'='*80}\n")

            # Créer les joueurs pour ce round
            profiles = list(PLAYER_PROFILES.keys())

            for i in range(self.num_players):
                profile = profiles[i % len(profiles)]
                simulator = PlayerSimulator(profile)

                print(f"\n🎮 Joueur {i+1}: {simulator.profile['name']}")
                print(f"   Comportement: {simulator.profile['behavior']}")
                print(f"   Patience: {simulator.profile['patience']}")

                # Lancer avec délai
                simulator.run_session()

                # Attendre avant le joueur suivant
                wait_time = random.randint(10, 30)
                print(f"\n⏳ Pause de {wait_time}s avant le joueur suivant...\n")
                time.sleep(wait_time)

                self.simulators.append(simulator)

            # Pause entre rounds
            if round_num < rounds:
                print(f"\n{'='*80}")
                print(f"Pause de 60s entre les rounds...")
                print(f"{'='*80}\n")
                time.sleep(60)

        self.generate_report()

    def generate_report(self):
        """Génère le rapport final"""
        print(f"\n{'='*80}")
        print("GÉNÉRATION DU RAPPORT...")
        print(f"{'='*80}\n")

        all_issues = []
        for sim in self.simulators:
            all_issues.extend(sim.issues_found)

        # Grouper par type
        issues_by_type = {}
        for issue in all_issues:
            issue_type = issue['type']
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append(issue)

        # Générer rapport markdown
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write("# 🎮 RAPPORT DE TEST MULTI-JOUEURS\n")
            f.write(f"## KOF Ultimate Online - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write("---\n\n")

            f.write(f"## 📊 Résumé\n\n")
            f.write(f"- **Joueurs simulés**: {len(self.simulators)}\n")
            f.write(f"- **Problèmes trouvés**: {len(all_issues)}\n")
            f.write(f"- **Types de problèmes**: {len(issues_by_type)}\n\n")

            f.write("## 🎯 Profils Testés\n\n")
            profile_counts = {}
            for sim in self.simulators:
                profile = sim.profile_name
                profile_counts[profile] = profile_counts.get(profile, 0) + 1

            for profile, count in profile_counts.items():
                f.write(f"- **{PLAYER_PROFILES[profile]['name']}**: {count} session(s)\n")

            f.write("\n## ⚠️ Problèmes Identifiés\n\n")

            if not all_issues:
                f.write("✅ **Aucun problème détecté!**\n\n")
            else:
                for issue_type, issues in issues_by_type.items():
                    f.write(f"### {issue_type} ({len(issues)})\n\n")
                    for issue in issues:
                        f.write(f"- **{issue['player_profile']}** ({issue['time']})\n")
                        f.write(f"  - {issue['description']}\n\n")

            f.write("## 📁 Fichiers de Log\n\n")
            for sim in self.simulators:
                f.write(f"- `{sim.log_file.name}`\n")

            f.write("\n---\n\n")
            f.write("*Rapport généré automatiquement par le simulateur de joueurs*\n")

        print(f"✅ Rapport généré: {self.report_file}")


def main():
    """Point d'entrée"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║  SIMULATEUR DE JOUEURS RÉELS - KOF ULTIMATE ONLINE          ║
║                                                              ║
║  Simule de vrais joueurs qui explorent et jouent            ║
╚══════════════════════════════════════════════════════════════╝
    """)

    print("\n⚠️  IMPORTANT:")
    print("   - NE PAS toucher la souris/clavier pendant les tests")
    print("   - Le jeu va se lancer automatiquement")
    print("   - Les tests peuvent durer 30+ minutes\n")

    input("Appuyez sur ENTRÉE pour commencer...")

    # Lancer simulation
    simulation = MultiPlayerSimulation(num_players=4)
    simulation.run_concurrent_tests(rounds=3)

    print("\n" + "="*80)
    print("✅ SIMULATION TERMINÉE!")
    print("="*80)
    print(f"\nRapport: {simulation.report_file}")
    print(f"Logs: {LOG_DIR}\n")


if __name__ == "__main__":
    main()
