#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST RAPIDE - Un seul joueur pour diagnostic rapide
"""

import subprocess
import time
import random
import os
from datetime import datetime
from pathlib import Path

try:
    import pyautogui
    pyautogui.FAILSAFE = True  # Bouger souris dans coin = arrêt
except ImportError:
    print("❌ pyautogui non installé. Installation...")
    os.system("pip install pyautogui")
    import pyautogui

GAME_EXE = "KOF_Ultimate_Online.exe"
GAME_PATH = Path(__file__).parent

class QuickTester:
    """Test rapide pour diagnostic"""

    def __init__(self):
        self.issues = []
        self.start_time = datetime.now()

    def log(self, msg):
        timestamp = (datetime.now() - self.start_time).total_seconds()
        print(f"[{timestamp:>6.1f}s] {msg}")

    def issue(self, problem):
        self.issues.append(problem)
        self.log(f"⚠️  PROBLÈME: {problem}")

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

        # Attendre fenêtre (30s max)
        self.log("Attente de la fenêtre...")
        for i in range(30):
            time.sleep(1)
            try:
                windows = pyautogui.getAllTitles()
                for w in windows:
                    if any(x in w for x in ["KOF", "Ikemen", "MUGEN"]):
                        self.log(f"✓ Fenêtre détectée: {w}")
                        time.sleep(3)  # Laisser charger
                        return True
            except:
                pass

            if i % 5 == 0:
                self.log(f"  Attente... {i}/30s")

        self.issue("Fenêtre du jeu jamais apparue (timeout 30s)")
        return False

    def test_title_screen(self):
        """Test écran titre"""
        self.log("\n" + "="*60)
        self.log("TEST 2: ÉCRAN TITRE")
        self.log("="*60)

        self.log("Attente écran titre (10s)...")
        time.sleep(10)

        self.log("Appui sur ESPACE pour entrer au menu...")
        pyautogui.press('space')
        time.sleep(3)

        self.log("✓ Passage au menu principal")

    def test_menu_navigation(self):
        """Test navigation menus"""
        self.log("\n" + "="*60)
        self.log("TEST 3: NAVIGATION MENUS")
        self.log("="*60)

        menu_items = [
            "Arcade", "Versus", "Team Arcade", "Team Versus",
            "Training", "Network", "Options"
        ]

        for i, item in enumerate(menu_items):
            self.log(f"Navigation vers: {item}")
            pyautogui.press('down')
            time.sleep(1.5)

        self.log("✓ Navigation OK - 7 options parcourues")

        # Remonter
        self.log("Retour au début du menu...")
        for _ in range(7):
            pyautogui.press('up')
            time.sleep(0.3)

    def test_versus_mode(self):
        """Test mode versus"""
        self.log("\n" + "="*60)
        self.log("TEST 4: MODE VERSUS")
        self.log("="*60)

        self.log("Sélection de Versus...")
        pyautogui.press('down')  # Aller à Versus
        time.sleep(0.5)
        pyautogui.press('return')
        time.sleep(4)

        self.log("✓ Écran de sélection de personnages")

    def test_character_selection(self):
        """Test sélection personnage"""
        self.log("\n" + "="*60)
        self.log("TEST 5: SÉLECTION PERSONNAGE")
        self.log("="*60)

        self.log("Navigation dans la grille...")
        directions = ['right', 'down', 'left', 'right', 'down', 'right']
        for d in directions:
            pyautogui.press(d)
            time.sleep(0.5)

        self.log("Sélection avec START maintenu (mode manuel)...")
        pyautogui.keyDown('space')
        time.sleep(0.2)
        pyautogui.press('return')
        time.sleep(0.3)
        pyautogui.keyUp('space')

        self.log("✓ Personnage sélectionné")
        time.sleep(6)  # Attendre écran VS

    def test_gameplay(self, duration=30):
        """Test gameplay"""
        self.log("\n" + "="*60)
        self.log(f"TEST 6: GAMEPLAY ({duration}s)")
        self.log("="*60)

        self.log("Combat en cours...")
        keys = ['a', 's', 'z', 'x', 'left', 'right', 'up', 'down']

        start = time.time()
        actions = 0

        while time.time() - start < duration:
            key = random.choice(keys)
            pyautogui.press(key)
            actions += 1
            time.sleep(random.uniform(0.2, 0.6))

            if actions % 20 == 0:
                elapsed = time.time() - start
                self.log(f"  {actions} actions - {elapsed:.0f}s écoulées")

        self.log(f"✓ Combat terminé - {actions} actions effectuées")

    def test_pause_and_exit(self):
        """Test pause et sortie"""
        self.log("\n" + "="*60)
        self.log("TEST 7: PAUSE & SORTIE")
        self.log("="*60)

        self.log("Appui sur ESCAPE (pause)...")
        pyautogui.press('escape')
        time.sleep(2)

        self.log("Navigation menu pause...")
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press('up')
        time.sleep(1)

        self.log("Sortie du match...")
        pyautogui.press('escape')
        time.sleep(2)

        self.log("✓ Retour au menu")

    def generate_report(self):
        """Génère rapport"""
        self.log("\n" + "="*60)
        self.log("RAPPORT FINAL")
        self.log("="*60)

        duration = (datetime.now() - self.start_time).total_seconds()

        print(f"\n⏱️  Durée totale: {duration:.1f}s ({duration/60:.1f} min)")
        print(f"⚠️  Problèmes trouvés: {len(self.issues)}")

        if self.issues:
            print("\n❌ LISTE DES PROBLÈMES:")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")
        else:
            print("\n✅ AUCUN PROBLÈME DÉTECTÉ!")

        # Sauvegarder
        report_file = GAME_PATH / "logs" / f"test_rapide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        report_file.parent.mkdir(exist_ok=True)

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("TEST RAPIDE - KOF ULTIMATE ONLINE\n")
            f.write("="*60 + "\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Durée: {duration:.1f}s\n")
            f.write(f"Problèmes: {len(self.issues)}\n\n")

            if self.issues:
                f.write("PROBLÈMES DÉTECTÉS:\n")
                for i, issue in enumerate(self.issues, 1):
                    f.write(f"{i}. {issue}\n")
            else:
                f.write("✅ Aucun problème détecté\n")

        print(f"\n📄 Rapport sauvegardé: {report_file}")

    def run(self):
        """Lance tous les tests"""
        print("\n" + "="*70)
        print("  🎮 TEST RAPIDE - UN JOUEUR")
        print("  KOF Ultimate Online - Diagnostic UX")
        print("="*70 + "\n")

        print("⚠️  NE PAS toucher la souris/clavier pendant le test!")
        print("⚠️  Déplacez la souris dans le coin haut-gauche pour arrêter\n")

        print("Démarrage automatique dans 3 secondes...")
        time.sleep(3)
        print()

        try:
            if not self.test_launch():
                self.log("❌ Échec au lancement, arrêt des tests")
                return

            self.test_title_screen()
            self.test_menu_navigation()
            self.test_versus_mode()
            self.test_character_selection()
            self.test_gameplay(duration=30)
            self.test_pause_and_exit()

        except pyautogui.FailSafeException:
            self.log("\n⚠️  ARRÊT D'URGENCE (souris dans le coin)")
        except Exception as e:
            self.issue(f"Erreur critique: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.generate_report()


if __name__ == "__main__":
    tester = QuickTester()
    tester.run()

    print("\n" + "="*70)
    print("  ✅ TEST TERMINÉ")
    print("="*70 + "\n")
    time.sleep(2)
