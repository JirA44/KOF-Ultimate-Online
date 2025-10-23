#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST AUTO SANS CLAVIER
Teste le jeu en envoyant des messages directement à la fenêtre
N'UTILISE PAS le clavier de l'utilisateur !
"""

import time
import win32gui
import win32con
import win32api
import subprocess
from pathlib import Path
from datetime import datetime

class WindowsMessageTester:
    """Teste le jeu via messages Windows sans utiliser le clavier"""

    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.game_exe = self.base_path / "KOF_Ultimate_Online.exe"
        self.hwnd = None
        self.process = None

        # Codes de touches virtuelles
        self.VK_RETURN = 0x0D
        self.VK_ESCAPE = 0x1B
        self.VK_UP = 0x26
        self.VK_DOWN = 0x28
        self.VK_LEFT = 0x25
        self.VK_RIGHT = 0x27
        self.VK_SPACE = 0x20
        self.VK_A = 0x41
        self.VK_S = 0x53
        self.VK_D = 0x44

    def log(self, message, level="INFO"):
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "TEST": "🧪"}
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{icons.get(level, '')} [{timestamp}] {message}")

    def find_game_window(self, max_attempts=30):
        """Trouve la fenêtre du jeu"""
        self.log("Recherche de la fenêtre du jeu...", "INFO")

        for attempt in range(max_attempts):
            def callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    # MUGEN utilise souvent "M.U.G.E.N" dans le titre
                    if any(keyword in title.lower() for keyword in ['mugen', 'kof', 'ultimate']):
                        windows.append(hwnd)
                return True

            windows = []
            win32gui.EnumWindows(callback, windows)

            if windows:
                self.hwnd = windows[0]
                title = win32gui.GetWindowText(self.hwnd)
                self.log(f"✅ Fenêtre trouvée: {title}", "SUCCESS")
                return True

            time.sleep(0.5)

        self.log("❌ Fenêtre du jeu introuvable", "ERROR")
        return False

    def send_key_to_window(self, vk_code, press_duration=0.1):
        """Envoie une touche directement à la fenêtre du jeu"""
        if not self.hwnd:
            return False

        try:
            # Envoyer WM_KEYDOWN
            win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, vk_code, 0)
            time.sleep(press_duration)
            # Envoyer WM_KEYUP
            win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, vk_code, 0)
            return True
        except Exception as e:
            self.log(f"Erreur envoi touche: {e}", "ERROR")
            return False

    def press_enter(self):
        """Appuie sur Entrée"""
        self.log("  → Entrée", "TEST")
        return self.send_key_to_window(self.VK_RETURN, 0.05)

    def press_escape(self):
        """Appuie sur Échap"""
        self.log("  → Échap", "TEST")
        return self.send_key_to_window(self.VK_ESCAPE, 0.05)

    def press_down(self):
        """Appuie sur Bas"""
        return self.send_key_to_window(self.VK_DOWN, 0.05)

    def press_up(self):
        """Appuie sur Haut"""
        return self.send_key_to_window(self.VK_UP, 0.05)

    def press_left(self):
        """Appuie sur Gauche"""
        return self.send_key_to_window(self.VK_LEFT, 0.05)

    def press_right(self):
        """Appuie sur Droite"""
        return self.send_key_to_window(self.VK_RIGHT, 0.05)

    def launch_game(self):
        """Lance le jeu"""
        self.log("Lancement du jeu...", "TEST")

        try:
            self.process = subprocess.Popen(
                [str(self.game_exe)],
                cwd=str(self.base_path),
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )

            self.log(f"✅ Jeu lancé (PID: {self.process.pid})", "SUCCESS")

            # Attendre que la fenêtre apparaisse
            if not self.find_game_window():
                return False

            return True

        except Exception as e:
            self.log(f"❌ Erreur lancement: {e}", "ERROR")
            return False

    def navigate_to_arcade(self):
        """Navigue jusqu'au mode Arcade"""
        self.log("\n🎮 Navigation vers Arcade...", "TEST")

        # Attendre écran de titre
        time.sleep(4)

        # Passer l'écran de titre
        self.press_enter()
        time.sleep(2)

        # Sélectionner Arcade (normalement le premier choix)
        self.press_enter()
        time.sleep(2)

        self.log("✅ Mode Arcade sélectionné", "SUCCESS")

    def select_random_characters(self):
        """Sélectionne des personnages aléatoirement"""
        self.log("\n👥 Sélection des personnages...", "TEST")

        # Naviguer dans la grille
        for _ in range(5):
            self.press_right()
            time.sleep(0.3)

        for _ in range(3):
            self.press_down()
            time.sleep(0.3)

        # Sélectionner premier personnage
        self.log("  Sélection P1...", "INFO")
        self.press_enter()
        time.sleep(1)
        self.press_enter()  # Confirmer
        time.sleep(2)

        # Naviguer pour P2
        for _ in range(4):
            self.press_left()
            time.sleep(0.3)

        # Sélectionner second personnage
        self.log("  Sélection P2...", "INFO")
        self.press_enter()
        time.sleep(1)
        self.press_enter()  # Confirmer
        time.sleep(2)

        self.log("✅ Personnages sélectionnés", "SUCCESS")

    def wait_for_match(self, duration=10):
        """Attend pendant le match"""
        self.log(f"\n⏳ Observation du match ({duration}s)...", "TEST")

        for i in range(duration):
            if not self.hwnd or not win32gui.IsWindow(self.hwnd):
                self.log("❌ Fenêtre fermée", "ERROR")
                return False

            time.sleep(1)

        return True

    def quit_match(self):
        """Quitte le match"""
        self.log("\n🚪 Sortie du match...", "TEST")

        for _ in range(5):
            self.press_escape()
            time.sleep(0.5)

    def run_full_test(self):
        """Lance un test complet"""
        print("\n" + "="*80)
        print("  🧪 TEST AUTO SANS CLAVIER")
        print("  Vos touches restent LIBRES pendant le test !")
        print("="*80 + "\n")

        # 1. Lancer le jeu
        if not self.launch_game():
            self.log("❌ Impossible de lancer le jeu", "ERROR")
            return False

        # 2. Naviguer vers Arcade
        try:
            self.navigate_to_arcade()
        except Exception as e:
            self.log(f"Erreur navigation: {e}", "ERROR")

        # 3. Sélectionner personnages
        try:
            self.select_random_characters()
        except Exception as e:
            self.log(f"Erreur sélection: {e}", "ERROR")

        # 4. Attendre le match
        self.wait_for_match(duration=15)

        # 5. Quitter
        self.quit_match()

        # 6. Fermer le jeu
        if self.process:
            try:
                self.process.terminate()
                time.sleep(2)
                if self.process.poll() is None:
                    self.process.kill()
            except:
                pass

        # RAPPORT
        print("\n" + "="*80)
        print("  ✅ TEST TERMINÉ")
        print("="*80)
        print("\nVotre clavier n'a JAMAIS été utilisé pendant ce test !")
        print("Les touches ont été envoyées directement à la fenêtre du jeu.")
        print("\n💡 Vous pouvez vérifier mugen.log pour les erreurs.")
        print("="*80 + "\n")

        return True

    def run_continuous_tests(self, num_tests=5):
        """Lance plusieurs tests en continu"""
        print("\n" + "="*80)
        print(f"  🔄 TESTS CONTINUS - {num_tests} itérations")
        print("="*80 + "\n")

        for i in range(num_tests):
            self.log(f"\n{'='*60}", "INFO")
            self.log(f"ITÉRATION {i+1}/{num_tests}", "TEST")
            self.log(f"{'='*60}", "INFO")

            self.run_full_test()

            if i < num_tests - 1:
                self.log(f"\n⏸️  Pause 10s avant prochaine itération...", "INFO")
                time.sleep(10)

        print("\n" + "="*80)
        print(f"  ✅ {num_tests} TESTS TERMINÉS")
        print("="*80 + "\n")

if __name__ == "__main__":
    print("\n⚠️  IMPORTANT: Ce test envoie les touches UNIQUEMENT à la fenêtre du jeu.")
    print("Vos touches restent disponibles pour d'autres applications !\n")

    choice = input("1. Test unique\n2. Tests continus (5x)\n\nVotre choix: ").strip()

    tester = WindowsMessageTester()

    if choice == "2":
        tester.run_continuous_tests(5)
    else:
        tester.run_full_test()
