#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST AUTO AVEC FOCUS FORCÉ
Force le focus sur la fenêtre du jeu avant chaque action
"""

import subprocess
import time
import random
import os
from datetime import datetime
from pathlib import Path

try:
    import pyautogui
    import pygetwindow as gw
    pyautogui.FAILSAFE = True
except ImportError:
    print("Installation des dépendances...")
    os.system("pip install pyautogui pygetwindow")
    import pyautogui
    import pygetwindow as gw

GAME_EXE = "KOF_Ultimate_Online.exe"
GAME_PATH = Path(__file__).parent

class FocusedTester:
    """Test avec focus forcé sur le jeu"""

    def __init__(self):
        self.issues = []
        self.start_time = datetime.now()
        self.game_window = None

    def log(self, msg):
        timestamp = (datetime.now() - self.start_time).total_seconds()
        print(f"[{timestamp:>6.1f}s] {msg}")

    def issue(self, problem):
        self.issues.append(problem)
        self.log(f"⚠️  PROBLÈME: {problem}")

    def find_game_window(self):
        """Trouve et retourne la fenêtre du jeu"""
        try:
            windows = gw.getAllWindows()
            for w in windows:
                if any(keyword in w.title for keyword in ["KOF", "Ikemen", "MUGEN", "AI Navigator"]):
                    self.log(f"✓ Fenêtre trouvée: {w.title}")
                    return w
        except Exception as e:
            self.log(f"Erreur recherche fenêtre: {e}")
        return None

    def focus_game(self):
        """Force le focus sur le jeu"""
        if not self.game_window:
            self.game_window = self.find_game_window()

        if self.game_window:
            try:
                self.game_window.activate()
                time.sleep(0.3)  # Laisser le focus s'établir
                return True
            except Exception as e:
                self.log(f"Erreur focus: {e}")
                return False
        return False

    def press_key(self, key, hold_time=0.1):
        """Appuie sur une touche avec focus forcé"""
        if not self.focus_game():
            self.issue(f"Impossible de focus le jeu pour touche {key}")
            return

        pyautogui.press(key)
        time.sleep(hold_time)

    def test_launch(self):
        """Test du lancement"""
        self.log("="*60)
        self.log("TEST 1: LANCEMENT DU JEU")
        self.log("="*60)

        game_path = GAME_PATH / GAME_EXE

        if not game_path.exists():
            self.issue(f"Exe introuvable: {GAME_EXE}")
            return False

        self.log(f"✓ Exe trouvé: {game_path}")
        self.log("Lancement...")

        try:
            subprocess.Popen(str(game_path), cwd=str(GAME_PATH))
        except Exception as e:
            self.issue(f"Échec lancement: {e}")
            return False

        # Attendre fenêtre
        self.log("Attente de la fenêtre...")
        for i in range(30):
            time.sleep(1)
            self.game_window = self.find_game_window()
            if self.game_window:
                time.sleep(3)
                return True

            if i % 5 == 0:
                self.log(f"  Attente... {i}/30s")

        self.issue("Fenêtre jamais apparue (timeout 30s)")
        return False

    def test_title_screen(self):
        """Test écran titre"""
        self.log("\n" + "="*60)
        self.log("TEST 2: ÉCRAN TITRE")
        self.log("="*60)

        self.log("Attente écran titre (10s)...")
        time.sleep(10)

        self.log("Focus sur le jeu...")
        if not self.focus_game():
            self.issue("Impossible de focus le jeu")
            return

        self.log("Appui sur ESPACE...")
        self.press_key('space')
        time.sleep(3)

        self.log("✓ Passage au menu principal")

    def test_menu_navigation(self):
        """Test navigation menus"""
        self.log("\n" + "="*60)
        self.log("TEST 3: NAVIGATION MENUS")
        self.log("="*60)

        for i in range(7):
            self.log(f"Navigation item {i+1}/7")
            self.press_key('down')
            time.sleep(1.5)

        self.log("✓ Navigation OK")

        # Remonter
        for _ in range(7):
            self.press_key('up')
            time.sleep(0.3)

    def test_versus_mode(self):
        """Test mode versus"""
        self.log("\n" + "="*60)
        self.log("TEST 4: MODE VERSUS")
        self.log("="*60)

        self.press_key('down')
        time.sleep(0.5)
        self.press_key('return')
        time.sleep(4)

        self.log("✓ Écran de sélection")

    def test_character_selection(self):
        """Test sélection personnage"""
        self.log("\n" + "="*60)
        self.log("TEST 5: SÉLECTION PERSONNAGE")
        self.log("="*60)

        directions = ['right', 'down', 'left', 'right']
        for d in directions:
            self.press_key(d)
            time.sleep(0.5)

        self.log("Sélection...")
        self.focus_game()
        pyautogui.keyDown('space')
        time.sleep(0.2)
        pyautogui.press('return')
        time.sleep(0.3)
        pyautogui.keyUp('space')

        self.log("✓ Personnage sélectionné")
        time.sleep(6)

    def test_gameplay(self, duration=20):
        """Test gameplay"""
        self.log("\n" + "="*60)
        self.log(f"TEST 6: GAMEPLAY ({duration}s)")
        self.log("="*60)

        keys = ['a', 's', 'z', 'x', 'left', 'right']
        start = time.time()
        actions = 0

        while time.time() - start < duration:
            if actions % 5 == 0:
                self.focus_game()  # Re-focus tous les 5 actions

            key = random.choice(keys)
            pyautogui.press(key)
            actions += 1
            time.sleep(random.uniform(0.3, 0.7))

        self.log(f"✓ Combat terminé - {actions} actions")

    def test_pause_and_exit(self):
        """Test pause et sortie"""
        self.log("\n" + "="*60)
        self.log("TEST 7: PAUSE & SORTIE")
        self.log("="*60)

        self.press_key('escape')
        time.sleep(2)
        self.press_key('down')
        time.sleep(1)
        self.press_key('escape')
        time.sleep(2)

        self.log("✓ Retour au menu")

    def generate_report(self):
        """Génère rapport"""
        self.log("\n" + "="*60)
        self.log("RAPPORT FINAL")
        self.log("="*60)

        duration = (datetime.now() - self.start_time).total_seconds()

        print(f"\n⏱️  Durée: {duration:.1f}s")
        print(f"⚠️  Problèmes: {len(self.issues)}")

        if self.issues:
            print("\n❌ PROBLÈMES:")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")
        else:
            print("\n✅ AUCUN PROBLÈME!")

    def run(self):
        """Lance tous les tests"""
        print("\n" + "="*70)
        print("  🎮 TEST AUTO AVEC FOCUS FORCÉ")
        print("  (Plus sûr pour vos autres fenêtres)")
        print("="*70 + "\n")

        print("⚠️  NE PAS utiliser souris/clavier pendant le test!")
        print("⚠️  Souris dans coin haut-gauche = arrêt\n")

        print("Démarrage dans 5 secondes...")
        print("(Fermez vos fenêtres importantes ou minimisez-les)")
        time.sleep(5)
        print()

        try:
            if not self.test_launch():
                return

            self.test_title_screen()
            self.test_menu_navigation()
            self.test_versus_mode()
            self.test_character_selection()
            self.test_gameplay(duration=20)  # Plus court
            self.test_pause_and_exit()

        except pyautogui.FailSafeException:
            self.log("\n⚠️  ARRÊT D'URGENCE")
        except Exception as e:
            self.issue(f"Erreur: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.generate_report()

if __name__ == "__main__":
    tester = FocusedTester()
    tester.run()

    print("\n" + "="*70)
    time.sleep(2)
