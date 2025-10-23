#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SYSTÈME DE TESTS EN CONTINU AUTONOME
Lance des tests automatiques en boucle sans déranger l'utilisateur
"""

import subprocess
import time
import random
import os
from datetime import datetime
from pathlib import Path
import json

try:
    import win32gui
    import win32con
    import win32api
    import win32process
except ImportError:
    os.system("pip install pywin32")
    import win32gui
    import win32con
    import win32api
    import win32process

GAME_EXE = "KOF_Ultimate_Online.exe"
GAME_PATH = Path(__file__).parent
LOGS_DIR = GAME_PATH / "logs" / "tests_continus"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Configuration
CONFIG = {
    "interval_between_tests": 300,  # 5 minutes entre chaque test
    "test_duration": 90,  # Durée d'un test complet
    "max_tests_per_session": 100,  # Max tests avant redémarrage
    "silent_mode": True,  # Mode silencieux
}

VK_CODES = {
    'space': win32con.VK_SPACE,
    'return': win32con.VK_RETURN,
    'escape': win32con.VK_ESCAPE,
    'up': win32con.VK_UP,
    'down': win32con.VK_DOWN,
    'left': win32con.VK_LEFT,
    'right': win32con.VK_RIGHT,
    'a': ord('A'),
    's': ord('S'),
    'z': ord('Z'),
    'x': ord('X'),
}

class ContinuousTester:
    """Testeur continu autonome"""

    def __init__(self):
        self.test_count = 0
        self.total_issues = 0
        self.start_time = datetime.now()
        self.game_hwnd = None
        self.game_process = None

    def log(self, msg, level="INFO"):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] [{level}] {msg}"
        print(log_msg)

        # Sauvegarder dans le log continu
        with open(LOGS_DIR / "continuous.log", 'a', encoding='utf-8') as f:
            f.write(log_msg + "\n")

    def find_game_window(self):
        """Trouve le handle de la fenêtre du jeu"""
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if any(keyword in title for keyword in ["KOF", "Ikemen", "MUGEN", "AI Navigator"]):
                    windows.append(hwnd)
            return True

        windows = []
        win32gui.EnumWindows(callback, windows)
        return windows[0] if windows else None

    def send_key(self, key, hold_time=0.05):
        """Envoie une touche au jeu"""
        if not self.game_hwnd or key not in VK_CODES:
            return False

        try:
            vk_code = VK_CODES[key]
            lparam_down = win32api.MapVirtualKey(vk_code, 0) << 16 | 1
            win32api.SendMessage(self.game_hwnd, win32con.WM_KEYDOWN, vk_code, lparam_down)
            time.sleep(hold_time)
            lparam_up = lparam_down | (0x3 << 30)
            win32api.SendMessage(self.game_hwnd, win32con.WM_KEYUP, vk_code, lparam_up)
            return True
        except:
            return False

    def launch_game(self):
        """Lance le jeu"""
        game_path = GAME_PATH / GAME_EXE
        if not game_path.exists():
            self.log(f"Jeu introuvable: {GAME_EXE}", "ERROR")
            return False

        try:
            self.game_process = subprocess.Popen(
                str(game_path),
                cwd=str(GAME_PATH),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.log(f"Jeu lancé (PID: {self.game_process.pid})")

            # Attendre la fenêtre
            for _ in range(30):
                time.sleep(1)
                self.game_hwnd = self.find_game_window()
                if self.game_hwnd:
                    time.sleep(3)
                    return True

            self.log("Fenêtre du jeu jamais apparue", "ERROR")
            return False

        except Exception as e:
            self.log(f"Erreur lancement: {e}", "ERROR")
            return False

    def close_game(self):
        """Ferme le jeu proprement"""
        if self.game_process:
            try:
                self.game_process.terminate()
                self.game_process.wait(timeout=5)
                self.log("Jeu fermé")
            except:
                try:
                    self.game_process.kill()
                except:
                    pass

    def run_quick_test(self):
        """Lance un test rapide complet"""
        self.test_count += 1
        test_start = datetime.now()
        issues = []

        self.log(f"═══ DÉBUT TEST #{self.test_count} ═══")

        try:
            # Lancer le jeu
            if not self.launch_game():
                issues.append("Échec lancement")
                return issues

            # Écran titre
            time.sleep(10)
            self.send_key('space')
            time.sleep(3)

            # Navigation menu
            for _ in range(7):
                self.send_key('down')
                time.sleep(1)
            for _ in range(7):
                self.send_key('up')
                time.sleep(0.3)

            # Versus
            self.send_key('down')
            time.sleep(0.5)
            self.send_key('return')
            time.sleep(4)

            # Sélection personnage
            for direction in ['right', 'down', 'left', 'right']:
                self.send_key(direction)
                time.sleep(0.5)
            self.send_key('return')
            time.sleep(6)

            # Gameplay court (15s pour aller plus vite)
            keys = ['a', 's', 'z', 'x', 'left', 'right']
            for _ in range(30):
                self.send_key(random.choice(keys))
                time.sleep(0.5)

            # Sortie
            self.send_key('escape')
            time.sleep(2)
            self.send_key('escape')
            time.sleep(2)

        except Exception as e:
            issues.append(f"Erreur: {e}")
            self.log(f"Erreur pendant le test: {e}", "ERROR")

        finally:
            self.close_game()
            time.sleep(3)  # Laisser le jeu se fermer complètement

        # Rapport
        duration = (datetime.now() - test_start).total_seconds()
        self.log(f"Test #{self.test_count} terminé en {duration:.1f}s - {len(issues)} problème(s)")

        self.save_test_report(test_start, duration, issues)
        return issues

    def save_test_report(self, test_start, duration, issues):
        """Sauvegarde le rapport de test"""
        report_file = LOGS_DIR / f"test_{self.test_count:04d}_{test_start.strftime('%Y%m%d_%H%M%S')}.txt"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"TEST AUTOMATIQUE #{self.test_count}\n")
            f.write("="*60 + "\n\n")
            f.write(f"Date: {test_start.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Durée: {duration:.1f}s\n")
            f.write(f"Problèmes: {len(issues)}\n\n")

            if issues:
                f.write("PROBLÈMES:\n")
                for issue in issues:
                    f.write(f"- {issue}\n")
            else:
                f.write("✅ Aucun problème détecté\n")

        # Mettre à jour les stats globales
        self.update_stats(len(issues))

    def update_stats(self, issues_count):
        """Met à jour les statistiques globales"""
        self.total_issues += issues_count

        stats = {
            "total_tests": self.test_count,
            "total_issues": self.total_issues,
            "success_rate": ((self.test_count - self.total_issues) / self.test_count * 100) if self.test_count > 0 else 0,
            "uptime": (datetime.now() - self.start_time).total_seconds(),
            "last_update": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        with open(LOGS_DIR / "stats.json", 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)

    def run_continuous(self):
        """Boucle principale de tests continus"""
        self.log("╔═══════════════════════════════════════════════════════╗")
        self.log("║  🎮 SYSTÈME DE TESTS CONTINUS DÉMARRÉ               ║")
        self.log("║     Tests automatiques en arrière-plan               ║")
        self.log("╚═══════════════════════════════════════════════════════╝")
        self.log(f"Intervalle: {CONFIG['interval_between_tests']}s entre tests")
        self.log(f"Logs: {LOGS_DIR}")
        self.log("")

        try:
            while self.test_count < CONFIG['max_tests_per_session']:
                # Lancer un test
                issues = self.run_quick_test()

                # Attendre avant le prochain test
                wait_time = CONFIG['interval_between_tests']
                self.log(f"Prochain test dans {wait_time}s...")
                self.log("")

                time.sleep(wait_time)

        except KeyboardInterrupt:
            self.log("Arrêt demandé par l'utilisateur", "WARN")
        except Exception as e:
            self.log(f"Erreur critique: {e}", "ERROR")
        finally:
            self.log("╔═══════════════════════════════════════════════════════╗")
            self.log("║  🏁 SYSTÈME DE TESTS ARRÊTÉ                          ║")
            self.log("╚═══════════════════════════════════════════════════════╝")
            self.log(f"Total tests: {self.test_count}")
            self.log(f"Total problèmes: {self.total_issues}")
            self.log(f"Taux de réussite: {((self.test_count - self.total_issues) / self.test_count * 100) if self.test_count > 0 else 0:.1f}%")


if __name__ == "__main__":
    tester = ContinuousTester()
    tester.run_continuous()
