#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - IA Navigator Simple
Navigate dans TOUS les menus pour détecter les erreurs
SANS API - Juste navigation intelligente
"""

import time
import pyautogui
import win32gui
import win32con
import random
from datetime import datetime
from pathlib import Path

class SimpleNavigator:
    """IA qui navigue partout pour détecter les erreurs"""

    def __init__(self):
        self.window_handle = None
        self.actions_performed = 0
        self.errors_detected = []
        self.screenshots_dir = Path(r"D:\KOF Ultimate Online\ia_screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)

    def log(self, message):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def find_game_window(self):
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
            self.window_handle = windows[0]
            return True
        return False

    def focus_window(self):
        """Focus sur la fenêtre du jeu"""
        if self.window_handle:
            try:
                win32gui.ShowWindow(self.window_handle, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(self.window_handle)
                time.sleep(0.2)
                return True
            except:
                return False
        return False

    def take_screenshot(self, name):
        """Prend un screenshot"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = self.screenshots_dir / filename

            screenshot = pyautogui.screenshot()
            screenshot.save(str(filepath))

            self.log(f"📸 Screenshot: {filename}")
            return filepath
        except Exception as e:
            self.log(f"❌ Erreur screenshot: {e}")
            return None

    def press_key(self, key, wait=0.5):
        """Appuie sur une touche"""
        if self.focus_window():
            pyautogui.press(key)
            self.actions_performed += 1
            time.sleep(wait)
            return True
        return False

    def navigate_menu_down(self, times=1):
        """Navigate vers le bas dans un menu"""
        self.log(f"⬇️  Navigation bas x{times}")
        for _ in range(times):
            self.press_key('down', 0.3)

    def navigate_menu_up(self, times=1):
        """Navigate vers le haut dans un menu"""
        self.log(f"⬆️  Navigation haut x{times}")
        for _ in range(times):
            self.press_key('up', 0.3)

    def navigate_menu_right(self, times=1):
        """Navigate vers la droite"""
        self.log(f"➡️  Navigation droite x{times}")
        for _ in range(times):
            self.press_key('right', 0.3)

    def navigate_menu_left(self, times=1):
        """Navigate vers la gauche"""
        self.log(f"⬅️  Navigation gauche x{times}")
        for _ in range(times):
            self.press_key('left', 0.3)

    def confirm_selection(self):
        """Confirme une sélection"""
        self.log("✅ Confirmation")
        self.press_key('enter', 1)

    def go_back(self):
        """Retour en arrière"""
        self.log("🔙 Retour")
        self.press_key('escape', 1)

    def explore_main_menu(self):
        """Explore le menu principal"""
        self.log("\n🎯 EXPLORATION DU MENU PRINCIPAL")
        self.log("=" * 60)

        # Passer l'écran de titre
        self.log("Passage écran de titre...")
        self.press_key('enter', 2)

        menu_options = [
            "Arcade",
            "Versus",
            "Team Arcade",
            "Team Versus",
            "Team Co-op",
            "Survival",
            "Survival Co-op",
            "Training",
            "Watch",
            "Options"
        ]

        # Tester chaque option du menu
        for i, option in enumerate(menu_options):
            self.log(f"\n📋 Test option {i+1}/{len(menu_options)}: {option}")

            # Screenshot avant
            self.take_screenshot(f"menu_{option}_avant")

            # Naviguer jusqu'à l'option
            if i > 0:
                self.navigate_menu_down(1)

            # Screenshot de l'option sélectionnée
            self.take_screenshot(f"menu_{option}_select")

            # Entrer dans l'option
            self.confirm_selection()
            time.sleep(1.5)

            # Screenshot dans l'option
            self.take_screenshot(f"menu_{option}_inside")

            # Retour au menu
            self.go_back()
            time.sleep(1)

        self.log("\n✅ Exploration menu principal terminée")

    def test_character_selection(self):
        """Teste la sélection de personnages"""
        self.log("\n🎯 TEST SÉLECTION PERSONNAGES")
        self.log("=" * 60)

        # Aller en mode Arcade
        self.log("Navigation vers Arcade...")
        self.press_key('enter', 2)  # Passer titre
        self.confirm_selection()  # Entrer dans Arcade
        time.sleep(2)

        # Grille de personnages - naviguer partout
        directions = ['right', 'down', 'left', 'up']

        for round_num in range(5):  # 5 tours de navigation
            self.log(f"\n🔄 Tour {round_num + 1}/5 de la grille")

            for i in range(8):  # 8 mouvements par tour
                direction = random.choice(directions)

                self.log(f"   → Mouvement {i+1}: {direction}")
                self.press_key(direction, 0.4)

                # Screenshot tous les 3 mouvements
                if i % 3 == 0:
                    self.take_screenshot(f"char_grid_r{round_num}_m{i}")

        # Test de sélection
        self.log("\n✅ Test sélection d'un personnage")
        self.confirm_selection()
        time.sleep(1)
        self.take_screenshot("char_selected")

        # Retour
        self.go_back()
        time.sleep(1)

    def test_all_menus_exhaustive(self):
        """Teste TOUS les menus de manière exhaustive"""
        self.log("\n🎯 TEST EXHAUSTIF DE TOUS LES MENUS")
        self.log("=" * 60)

        # Menu Options
        self.log("\n📋 Test du menu Options...")

        # Navigation vers Options (généralement tout en bas)
        self.press_key('enter', 2)  # Passer titre

        for _ in range(10):  # Aller tout en bas
            self.navigate_menu_down(1)

        self.confirm_selection()
        time.sleep(1.5)

        # Dans le menu Options, tester chaque sous-menu
        options_submenus = ["Gameplay", "Video", "Audio", "Input", "Team"]

        for i, submenu in enumerate(options_submenus):
            self.log(f"   Testing {submenu}...")
            self.take_screenshot(f"options_{submenu}")

            self.confirm_selection()
            time.sleep(1)

            # Naviguer dans le sous-menu
            for _ in range(5):
                self.navigate_menu_down(1)
                time.sleep(0.3)

            self.go_back()
            time.sleep(0.5)

            if i < len(options_submenus) - 1:
                self.navigate_menu_down(1)

        # Retour au menu principal
        for _ in range(3):
            self.go_back()
            time.sleep(0.5)

    def stress_test_navigation(self, duration_minutes=5):
        """Stress test: navigation aléatoire intensive"""
        self.log(f"\n🎯 STRESS TEST - {duration_minutes} minutes")
        self.log("=" * 60)

        end_time = time.time() + (duration_minutes * 60)
        iteration = 0

        while time.time() < end_time:
            iteration += 1
            self.log(f"\n🔄 Itération {iteration}")

            # Séquence aléatoire
            actions = [
                ('up', random.randint(1, 3)),
                ('down', random.randint(1, 3)),
                ('left', random.randint(1, 3)),
                ('right', random.randint(1, 3)),
                ('enter', 1),
                ('escape', 1)
            ]

            random.shuffle(actions)

            for action, times in actions[:4]:  # 4 actions aléatoires
                if action in ['up', 'down', 'left', 'right']:
                    getattr(self, f'navigate_menu_{action}')(times)
                elif action == 'enter':
                    self.confirm_selection()
                elif action == 'escape':
                    self.go_back()

                time.sleep(0.3)

            # Screenshot tous les 5 itérations
            if iteration % 5 == 0:
                self.take_screenshot(f"stress_test_iter_{iteration}")

        self.log(f"\n✅ Stress test terminé - {iteration} itérations")

    def run_complete_navigation(self):
        """Lance la navigation complète"""
        self.log("\n" + "=" * 60)
        self.log("  KOF ULTIMATE - IA NAVIGATOR SIMPLE")
        self.log("  Navigation intelligente pour détecter les erreurs")
        self.log("=" * 60)

        # Attendre que le jeu soit lancé
        self.log("\n⏳ Attente du jeu (30s max)...")

        for i in range(30):
            if self.find_game_window():
                self.log(f"✅ Jeu trouvé après {i}s!")
                break
            time.sleep(1)
        else:
            self.log("❌ Jeu non trouvé - Veuillez le lancer manuellement")
            return

        time.sleep(3)  # Attente chargement

        try:
            # Phase 1: Exploration menu principal
            self.explore_main_menu()

            # Phase 2: Test sélection personnages
            self.test_character_selection()

            # Phase 3: Test exhaustif des menus
            self.test_all_menus_exhaustive()

            # Phase 4: Stress test
            self.stress_test_navigation(duration_minutes=2)

        except Exception as e:
            self.log(f"❌ Erreur détectée: {e}")
            self.errors_detected.append(str(e))
            self.take_screenshot("error_detected")

        # Rapport final
        self.log("\n" + "=" * 60)
        self.log("📊 RAPPORT FINAL")
        self.log("=" * 60)
        self.log(f"Actions effectuées: {self.actions_performed}")
        self.log(f"Screenshots pris: {len(list(self.screenshots_dir.glob('*.png')))}")
        self.log(f"Erreurs détectées: {len(self.errors_detected)}")

        if self.errors_detected:
            self.log("\n⚠️  ERREURS:")
            for i, error in enumerate(self.errors_detected, 1):
                self.log(f"   {i}. {error}")
        else:
            self.log("\n✅ Aucune erreur détectée!")

        self.log("\n📁 Screenshots dans: " + str(self.screenshots_dir))
        self.log("=" * 60)

def main():
    """Point d'entrée"""
    navigator = SimpleNavigator()
    navigator.run_complete_navigation()

    print("\n\n✅ Navigation terminée!")
    print("   Vous pouvez consulter les screenshots pour voir tous les tests.\n")

    input("Appuyez sur Entrée pour quitter...")

if __name__ == '__main__':
    main()
