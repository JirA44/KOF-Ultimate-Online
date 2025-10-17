#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - Match IA vs IA
Deux IA s'affrontent dans le même jeu (Player 1 vs Player 2)
"""

import subprocess
import time
import os
import random
from pathlib import Path
from datetime import datetime
import sys
import threading

# Installer dépendances si nécessaire
try:
    import pyautogui
    import win32gui
    import win32con
    from PIL import Image
except ImportError:
    print("Installation des dépendances...")
    os.system(f"{sys.executable} -m pip install pyautogui pywin32 Pillow --quiet")
    import pyautogui
    import win32gui
    import win32con
    from PIL import Image

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class AIPlayer:
    """Une IA qui contrôle un joueur (P1 ou P2)"""

    # Touches pour Player 1
    P1_KEYS = {
        'up': 'up',
        'down': 'down',
        'left': 'left',
        'right': 'right',
        'punch': 'a',
        'kick': 's',
        'heavy': 'd',
        'special': 'space'
    }

    # Touches pour Player 2
    P2_KEYS = {
        'up': 'w',
        'down': 'x',
        'left': 'a',  # Attention: conflit avec P1
        'right': 'd',  # Attention: conflit avec P1
        'punch': 'u',
        'kick': 'i',
        'heavy': 'o',
        'special': 'j'
    }

    def __init__(self, player_num, personality="balanced"):
        self.player_num = player_num  # 1 ou 2
        self.personality = personality
        self.keys = self.P1_KEYS if player_num == 1 else self.P2_KEYS
        self.action_count = 0
        self.is_active = False

        # Patterns selon personnalité
        self.patterns = {
            "aggressive": [
                ['right', 'right', 'punch', 'kick'],
                ['right', 'heavy'],
                ['punch', 'punch', 'kick'],
                ['right', 'down', 'right', 'punch']  # Combo
            ],
            "defensive": [
                ['left', 'down'],
                ['down', 'kick'],
                ['left', 'left'],
                ['down', 'punch']
            ],
            "balanced": [
                ['right', 'punch'],
                ['kick'],
                ['left', 'heavy'],
                ['right', 'right', 'punch']
            ],
            "random": []  # Sera random
        }

    def get_next_action(self):
        """Retourne la prochaine action à effectuer"""
        if self.personality == "random":
            actions = list(self.keys.keys())
            return [random.choice(actions)]

        patterns = self.patterns[self.personality]
        pattern = patterns[self.action_count % len(patterns)]

        self.action_count += 1
        return pattern

    def execute_action(self, action):
        """Exécute une action (touche)"""
        if not self.is_active:
            return

        key = self.keys.get(action)
        if key:
            try:
                pyautogui.press(key)
                time.sleep(random.uniform(0.05, 0.1))
            except:
                pass

class AIMatch:
    """Gère un match entre 2 IA"""

    def __init__(self, game_dir):
        self.game_dir = Path(game_dir)
        self.process = None
        self.window_handle = None

        # Créer les 2 IA
        self.ai_p1 = AIPlayer(1, personality="aggressive")
        self.ai_p2 = AIPlayer(2, personality="defensive")

        self.match_running = False
        self.screenshots_dir = self.game_dir / "ai_match_results" / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)

    def find_window(self):
        """Trouve la fenêtre du jeu"""
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if "mugen" in title.lower() or "kof" in title.lower():
                    windows.append(hwnd)
            return True

        windows = []
        win32gui.EnumWindows(callback, windows)

        if windows:
            self.window_handle = windows[-1]
            return True
        return False

    def launch_game(self):
        """Lance le jeu"""
        print(f"{Colors.CYAN}🎮 Lancement du jeu...{Colors.RESET}")

        exe_path = self.game_dir / "KOF_Ultimate_Online.exe"

        self.process = subprocess.Popen(
            [str(exe_path)],
            cwd=str(self.game_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        time.sleep(3)

        # Trouver la fenêtre
        for _ in range(15):
            if self.find_window():
                print(f"{Colors.GREEN}✓ Fenêtre trouvée (PID: {self.process.pid}){Colors.RESET}")

                # Mettre au premier plan
                try:
                    win32gui.ShowWindow(self.window_handle, win32con.SW_RESTORE)
                    win32gui.SetForegroundWindow(self.window_handle)
                    time.sleep(1)
                except:
                    pass

                return True
            time.sleep(0.5)

        print(f"{Colors.RED}✗ Fenêtre non trouvée{Colors.RESET}")
        return False

    def navigate_to_vs_mode(self):
        """Navigue vers VS MODE"""
        print(f"{Colors.CYAN}📋 Navigation vers VS MODE...{Colors.RESET}")

        # Attendre menu
        time.sleep(8)

        # Passer écran titre
        pyautogui.press('enter')
        time.sleep(2)

        # Descendre à VS MODE (2ème option)
        pyautogui.press('down')
        time.sleep(0.5)

        # Valider
        pyautogui.press('enter')
        time.sleep(3)

        print(f"{Colors.GREEN}✓ En sélection de personnage{Colors.RESET}")

    def select_characters(self):
        """Sélection des personnages"""
        print(f"{Colors.CYAN}🎭 Sélection des personnages...{Colors.RESET}")

        # Player 1 sélectionne (touches flèches)
        moves_p1 = random.randint(2, 8)
        for _ in range(moves_p1):
            direction = random.choice(['up', 'down', 'left', 'right'])
            pyautogui.press(direction)
            time.sleep(0.2)

        # Confirmer P1
        pyautogui.press('enter')
        time.sleep(1)

        print(f"{Colors.GREEN}  ✓ Player 1 sélectionné{Colors.RESET}")

        # Player 2 sélectionne
        time.sleep(1)
        moves_p2 = random.randint(2, 8)
        for _ in range(moves_p2):
            direction = random.choice(['up', 'down', 'left', 'right'])
            pyautogui.press(direction)
            time.sleep(0.2)

        # Confirmer P2
        pyautogui.press('enter')
        time.sleep(1)

        print(f"{Colors.GREEN}  ✓ Player 2 sélectionné{Colors.RESET}")

    def capture_screenshot(self, name):
        """Capture un screenshot"""
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{timestamp}_{name}.png"
        filepath = self.screenshots_dir / filename

        try:
            if self.window_handle:
                rect = win32gui.GetWindowRect(self.window_handle)
                x, y, x2, y2 = rect
                width = x2 - x
                height = y2 - y

                screenshot = pyautogui.screenshot(region=(x, y, width, height))
                screenshot.save(str(filepath))
                return filepath
        except:
            pass
        return None

    def ai_thread_p1(self, duration):
        """Thread pour IA Player 1"""
        start_time = time.time()

        while (time.time() - start_time) < duration and self.match_running:
            # Mettre fenêtre au premier plan
            try:
                win32gui.SetForegroundWindow(self.window_handle)
            except:
                pass

            # Exécuter une action
            actions = self.ai_p1.get_next_action()
            for action in actions:
                self.ai_p1.execute_action(action)

            # Timing selon personnalité
            if self.ai_p1.personality == "aggressive":
                time.sleep(random.uniform(0.15, 0.25))
            else:
                time.sleep(random.uniform(0.2, 0.4))

    def ai_thread_p2(self, duration):
        """Thread pour IA Player 2"""
        start_time = time.time()

        while (time.time() - start_time) < duration and self.match_running:
            # Exécuter une action
            actions = self.ai_p2.get_next_action()
            for action in actions:
                self.ai_p2.execute_action(action)

            # Timing selon personnalité
            if self.ai_p2.personality == "defensive":
                time.sleep(random.uniform(0.3, 0.5))
            else:
                time.sleep(random.uniform(0.2, 0.4))

    def run_match(self, duration=40):
        """Lance le match IA vs IA"""
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}⚔️  MATCH IA VS IA!{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'='*80}{Colors.RESET}\n")

        print(f"{Colors.CYAN}🤖 Player 1 (Rouge): Personnalité AGGRESSIVE{Colors.RESET}")
        print(f"{Colors.BLUE}🤖 Player 2 (Bleu): Personnalité DEFENSIVE{Colors.RESET}\n")

        print(f"{Colors.YELLOW}Durée du match: {duration} secondes{Colors.RESET}\n")

        # Attendre chargement
        time.sleep(5)

        # Activer les IA
        self.ai_p1.is_active = True
        self.ai_p2.is_active = True
        self.match_running = True

        # Capture début
        self.capture_screenshot("00_start")

        # Lancer les 2 IA en threads parallèles
        thread_p1 = threading.Thread(target=self.ai_thread_p1, args=(duration,), daemon=True)
        thread_p2 = threading.Thread(target=self.ai_thread_p2, args=(duration,), daemon=True)

        thread_p1.start()
        thread_p2.start()

        # Captures périodiques
        capture_interval = duration / 5
        for i in range(5):
            time.sleep(capture_interval)
            if self.match_running:
                self.capture_screenshot(f"{i+1:02d}_action")
                print(f"{Colors.CYAN}  📸 Capture {i+1}/5{Colors.RESET}")

        # Attendre fin
        thread_p1.join()
        thread_p2.join()

        self.match_running = False

        # Capture fin
        time.sleep(2)
        self.capture_screenshot("99_end")

        print(f"\n{Colors.GREEN}✓ Match terminé!{Colors.RESET}")
        print(f"\n{Colors.CYAN}Statistiques:{Colors.RESET}")
        print(f"  Player 1 (Aggressive): {self.ai_p1.action_count} actions")
        print(f"  Player 2 (Defensive): {self.ai_p2.action_count} actions")

    def stop(self):
        """Arrête le jeu"""
        print(f"\n{Colors.YELLOW}⏹ Fermeture du jeu...{Colors.RESET}")
        self.match_running = False

        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=3)
                print(f"{Colors.GREEN}✓ Jeu fermé{Colors.RESET}")
            except:
                try:
                    self.process.kill()
                except:
                    pass

    def run_full_session(self, match_duration=40):
        """Lance une session complète"""
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'🎮 SESSION IA vs IA - KOF ULTIMATE 🎮':^80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

        try:
            # 1. Lancer le jeu
            if not self.launch_game():
                print(f"{Colors.RED}✗ Échec lancement{Colors.RESET}")
                return False

            # 2. Navigation
            self.navigate_to_vs_mode()

            # 3. Sélection personnages
            self.select_characters()

            # 4. FIGHT!
            self.run_match(duration=match_duration)

            # 5. Arrêter
            time.sleep(2)
            self.stop()

            # 6. Résumé
            print(f"\n{Colors.CYAN}📁 Screenshots sauvegardés dans:{Colors.RESET}")
            print(f"   {self.screenshots_dir}\n")

            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ SESSION TERMINÉE AVEC SUCCÈS!{Colors.RESET}\n")
            return True

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Session interrompue{Colors.RESET}")
            self.stop()
            return False

        except Exception as e:
            print(f"\n{Colors.RED}✗ Erreur: {e}{Colors.RESET}")
            import traceback
            traceback.print_exc()
            self.stop()
            return False

def main():
    """Point d'entrée"""
    game_dir = r"D:\KOF Ultimate Online"

    print(f"\n{Colors.CYAN}Durée du match:{Colors.RESET}")
    print(f"  1. Court (30s)")
    print(f"  2. Normal (40s) [défaut]")
    print(f"  3. Long (60s)")

    try:
        choice = input(f"\n{Colors.CYAN}Choix: {Colors.RESET}").strip()

        if choice == "1":
            duration = 30
        elif choice == "3":
            duration = 60
        else:
            duration = 40

    except:
        duration = 40

    match = AIMatch(game_dir)
    success = match.run_full_session(match_duration=duration)

    return 0 if success else 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Programme arrêté{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Erreur fatale: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
