#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - Session de Joueurs Virtuels
Lance plusieurs IA qui naviguent dans les menus et jouent ensemble
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

class VirtualPlayer:
    """Un joueur virtuel IA qui peut naviguer et jouer"""

    def __init__(self, player_id, game_dir, personality="balanced"):
        self.player_id = player_id
        self.game_dir = Path(game_dir)
        self.personality = personality  # aggressive, defensive, balanced, random
        self.process = None
        self.window_handle = None
        self.actions_log = []
        self.is_active = False

        # Patterns de jeu selon personnalité
        self.move_patterns = {
            "aggressive": ["right", "right", "a", "s", "d", "right"],
            "defensive": ["left", "down", "left", "a", "up"],
            "balanced": ["right", "left", "a", "s", "right", "d"],
            "random": []  # Will be random
        }

    def find_window(self):
        """Trouve la fenêtre du jeu"""
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if "mugen" in title.lower() or "kof" in title.lower() or "ikemen" in title.lower():
                    windows.append(hwnd)
            return True

        windows = []
        win32gui.EnumWindows(callback, windows)

        # Trouver LA fenêtre de ce joueur (par timestamp de création proche)
        if windows:
            self.window_handle = windows[-1]  # Dernier créé = ce joueur
            return True
        return False

    def launch_game(self, use_ikemen=True):
        """Lance le jeu"""
        print(f"{Colors.CYAN}🎮 Joueur {self.player_id}: Lancement du jeu...{Colors.RESET}")

        if use_ikemen:
            exe_path = self.game_dir / "Ikemen_GO" / "Ikemen_GO.exe"
            if not exe_path.exists():
                print(f"{Colors.RED}  ✗ Ikemen GO introuvable, utilisation M.U.G.E.N{Colors.RESET}")
                exe_path = self.game_dir / "KOF_Ultimate_Online.exe"
        else:
            exe_path = self.game_dir / "KOF_Ultimate_Online.exe"

        self.process = subprocess.Popen(
            [str(exe_path)],
            cwd=str(exe_path.parent),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        time.sleep(3)  # Attendre démarrage

        # Trouver la fenêtre
        for _ in range(10):
            if self.find_window():
                print(f"{Colors.GREEN}  ✓ Joueur {self.player_id}: Fenêtre trouvée (PID: {self.process.pid}){Colors.RESET}")

                # Mettre au premier plan
                try:
                    win32gui.ShowWindow(self.window_handle, win32con.SW_RESTORE)
                    win32gui.SetForegroundWindow(self.window_handle)
                    time.sleep(0.5)
                except:
                    pass

                self.is_active = True
                return True
            time.sleep(0.5)

        print(f"{Colors.RED}  ✗ Joueur {self.player_id}: Fenêtre non trouvée{Colors.RESET}")
        return False

    def press_key(self, key, duration=0.1):
        """Simule une pression de touche"""
        if not self.is_active:
            return

        try:
            # Mettre fenêtre au premier plan
            win32gui.SetForegroundWindow(self.window_handle)
            time.sleep(0.05)

            # Presser la touche
            pyautogui.press(key)
            time.sleep(duration)

            self.actions_log.append({
                'time': datetime.now(),
                'action': f'press_{key}'
            })
        except:
            pass

    def navigate_to_vs_mode(self):
        """Navigue vers le mode VS"""
        print(f"{Colors.CYAN}  Joueur {self.player_id}: Navigation vers VS MODE...{Colors.RESET}")

        # Attendre menu principal
        time.sleep(5)

        # Appuyer sur Enter pour passer écran titre
        self.press_key('enter')
        time.sleep(2)

        # Descendre à VS MODE (2ème option généralement)
        self.press_key('down')
        time.sleep(0.5)

        # Valider
        self.press_key('enter')
        time.sleep(2)

        print(f"{Colors.GREEN}  ✓ Joueur {self.player_id}: En sélection de personnage{Colors.RESET}")

    def select_random_character(self):
        """Sélectionne un personnage au hasard"""
        print(f"{Colors.CYAN}  Joueur {self.player_id}: Sélection personnage...{Colors.RESET}")

        # Navigation aléatoire dans la grille
        moves = random.randint(3, 10)
        for _ in range(moves):
            direction = random.choice(['up', 'down', 'left', 'right'])
            self.press_key(direction, 0.2)

        # Confirmer sélection
        self.press_key('enter')
        time.sleep(1)

        print(f"{Colors.GREEN}  ✓ Joueur {self.player_id}: Personnage sélectionné{Colors.RESET}")

    def fight_ai(self, duration=30):
        """Combat avec IA basique"""
        print(f"{Colors.MAGENTA}  ⚔️  Joueur {self.player_id}: COMBAT! (Personnalité: {self.personality}){Colors.RESET}")

        start_time = time.time()
        action_count = 0

        while (time.time() - start_time) < duration:
            if not self.is_active:
                break

            # Choisir action selon personnalité
            if self.personality == "random":
                actions = ['left', 'right', 'down', 'up', 'a', 's', 'd', 'space']
                action = random.choice(actions)
            else:
                pattern = self.move_patterns[self.personality]
                action = pattern[action_count % len(pattern)]

            # Exécuter action
            self.press_key(action, random.uniform(0.05, 0.15))

            # Variabilité selon personnalité
            if self.personality == "aggressive":
                time.sleep(random.uniform(0.1, 0.2))  # Rapide
            elif self.personality == "defensive":
                time.sleep(random.uniform(0.3, 0.5))  # Prudent
            else:
                time.sleep(random.uniform(0.15, 0.3))  # Équilibré

            action_count += 1

            # Parfois un combo spécial
            if random.random() < 0.1:
                combo = ['down', 'down', 'right', 'a']
                for move in combo:
                    self.press_key(move, 0.05)

        print(f"{Colors.GREEN}  ✓ Joueur {self.player_id}: Combat terminé! ({action_count} actions){Colors.RESET}")

    def stop(self):
        """Arrête le joueur"""
        print(f"{Colors.YELLOW}  ⏹ Joueur {self.player_id}: Fermeture...{Colors.RESET}")
        self.is_active = False

        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=3)
            except:
                try:
                    self.process.kill()
                except:
                    pass

class MultiplayerSession:
    """Gère une session multijoueur avec plusieurs joueurs virtuels"""

    def __init__(self, game_dir, num_players=2):
        self.game_dir = Path(game_dir)
        self.num_players = num_players
        self.players = []
        self.session_log = []

    def create_players(self):
        """Crée les joueurs virtuels"""
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'🤖 CRÉATION DES JOUEURS VIRTUELS':^80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

        personalities = ["aggressive", "defensive", "balanced", "random"]

        for i in range(self.num_players):
            personality = personalities[i % len(personalities)]
            player = VirtualPlayer(i + 1, self.game_dir, personality)
            self.players.append(player)

            print(f"{Colors.CYAN}✨ Joueur {i + 1} créé: Personnalité '{personality}'{Colors.RESET}")

        print(f"\n{Colors.GREEN}✓ {self.num_players} joueurs virtuels créés!{Colors.RESET}")

    def launch_all_players(self, use_ikemen=True):
        """Lance tous les joueurs"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}🚀 LANCEMENT DES JOUEURS{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")

        for player in self.players:
            player.launch_game(use_ikemen)
            time.sleep(2)  # Décalage pour éviter conflits

        # Vérifier que tous sont lancés
        active_players = [p for p in self.players if p.is_active]
        print(f"\n{Colors.GREEN}✓ {len(active_players)}/{self.num_players} joueurs actifs{Colors.RESET}")

        return len(active_players) == self.num_players

    def run_menu_navigation_test(self):
        """Test de navigation dans les menus"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}📋 TEST NAVIGATION MENUS{Colors.RESET}")
        print(f"{Colors.BLUE}{'='*80}{Colors.RESET}\n")

        threads = []

        for player in self.players:
            if not player.is_active:
                continue

            # Chaque joueur navigue dans son propre thread
            thread = threading.Thread(
                target=player.navigate_to_vs_mode,
                daemon=True
            )
            threads.append(thread)
            thread.start()
            time.sleep(1)  # Décalage

        # Attendre fin navigation
        for thread in threads:
            thread.join(timeout=15)

        print(f"\n{Colors.GREEN}✓ Navigation terminée pour tous les joueurs{Colors.RESET}")

    def run_character_selection(self):
        """Sélection de personnages"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}🎭 SÉLECTION PERSONNAGES{Colors.RESET}")
        print(f"{Colors.BLUE}{'='*80}{Colors.RESET}\n")

        threads = []

        for player in self.players:
            if not player.is_active:
                continue

            thread = threading.Thread(
                target=player.select_random_character,
                daemon=True
            )
            threads.append(thread)
            thread.start()
            time.sleep(0.5)  # Petit décalage

        for thread in threads:
            thread.join(timeout=10)

        print(f"\n{Colors.GREEN}✓ Tous les personnages sélectionnés{Colors.RESET}")

    def run_multiplayer_match(self, duration=30):
        """Lance un match multijoueur"""
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}⚔️  MATCH MULTIJOUEUR!{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'='*80}{Colors.RESET}\n")

        print(f"{Colors.YELLOW}Durée du match: {duration} secondes{Colors.RESET}\n")

        # Attendre chargement du match
        time.sleep(5)

        # Tous les joueurs combattent simultanément
        threads = []

        for player in self.players:
            if not player.is_active:
                continue

            thread = threading.Thread(
                target=player.fight_ai,
                args=(duration,),
                daemon=True
            )
            threads.append(thread)
            thread.start()

        # Attendre fin du match
        for thread in threads:
            thread.join()

        print(f"\n{Colors.GREEN}✓ Match terminé!{Colors.RESET}")

    def show_statistics(self):
        """Affiche les statistiques de la session"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}📊 STATISTIQUES SESSION{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")

        for player in self.players:
            print(f"{Colors.CYAN}Joueur {player.player_id} ({player.personality}):{Colors.RESET}")
            print(f"  Actions effectuées: {len(player.actions_log)}")
            print(f"  Statut: {'✓ Actif' if player.is_active else '✗ Inactif'}")

            if player.process:
                try:
                    print(f"  PID: {player.process.pid}")
                except:
                    pass

            print()

    def stop_all_players(self):
        """Arrête tous les joueurs"""
        print(f"\n{Colors.YELLOW}⏹ ARRÊT DE TOUS LES JOUEURS{Colors.RESET}")

        for player in self.players:
            player.stop()

        time.sleep(2)
        print(f"{Colors.GREEN}✓ Tous les joueurs arrêtés{Colors.RESET}")

    def run_full_session(self, match_duration=30):
        """Lance une session complète"""
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'🎮 SESSION MULTIJOUEUR VIRTUELLE 🎮':^80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

        try:
            # 1. Créer joueurs
            self.create_players()

            # 2. Lancer tous les jeux
            if not self.launch_all_players(use_ikemen=False):  # M.U.G.E.N plus simple pour test
                print(f"{Colors.RED}✗ Échec lancement joueurs{Colors.RESET}")
                return False

            # 3. Navigation menus
            self.run_menu_navigation_test()

            # 4. Sélection personnages
            self.run_character_selection()

            # 5. Match!
            self.run_multiplayer_match(duration=match_duration)

            # 6. Statistiques
            time.sleep(2)
            self.show_statistics()

            # 7. Arrêter
            self.stop_all_players()

            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ SESSION TERMINÉE AVEC SUCCÈS!{Colors.RESET}\n")
            return True

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Session interrompue par l'utilisateur{Colors.RESET}")
            self.stop_all_players()
            return False

        except Exception as e:
            print(f"\n{Colors.RED}✗ Erreur: {e}{Colors.RESET}")
            import traceback
            traceback.print_exc()
            self.stop_all_players()
            return False

def main():
    """Point d'entrée principal"""
    game_dir = r"D:\KOF Ultimate Online Online Online"

    print(f"{Colors.CYAN}Options:{Colors.RESET}")
    print(f"  1. Session 2 joueurs (rapide - 30s)")
    print(f"  2. Session 2 joueurs (normale - 60s)")
    print(f"  3. Session 4 joueurs (chaos - 45s)")
    print(f"  4. Custom")

    try:
        choice = input(f"\n{Colors.CYAN}Choix (défaut=1): {Colors.RESET}").strip()

        if choice == "3":
            num_players = 4
            duration = 45
        elif choice == "2":
            num_players = 2
            duration = 60
        elif choice == "4":
            num_players = int(input("Nombre de joueurs: "))
            duration = int(input("Durée match (secondes): "))
        else:
            num_players = 2
            duration = 30

    except:
        num_players = 2
        duration = 30

    session = MultiplayerSession(game_dir, num_players=num_players)
    success = session.run_full_session(match_duration=duration)

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
