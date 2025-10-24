#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST ANTI-CRASH - Vérifie que le jeu ne crash plus après corrections
"""

import subprocess
import time
import random
import psutil
from pathlib import Path
from datetime import datetime

class AntiCrashTester:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.game_exe = self.base_path / "KOF_Ultimate_Online.exe"
        self.tests_passed = 0
        self.tests_failed = 0
        self.crashes_detected = 0
        self.characters_tested = []

    def log(self, msg, level="INFO"):
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "TEST": "🧪", "WARNING": "⚠️"}
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {icons.get(level, '')} {msg}")

    def is_game_running(self):
        """Vérifie si le jeu tourne"""
        for proc in psutil.process_iter(['name']):
            try:
                if 'KOF_Ultimate_Online.exe' in proc.info['name']:
                    return True, proc
            except:
                pass
        return False, None

    def kill_game(self):
        """Ferme le jeu proprement"""
        is_running, proc = self.is_game_running()
        if is_running:
            try:
                proc.terminate()
                time.sleep(2)
                if proc.is_running():
                    proc.kill()
                self.log("Jeu fermé", "INFO")
            except:
                pass

    def check_for_crash(self):
        """Vérifie si un crash est survenu"""
        mugen_log = self.base_path / "mugen.log"
        if not mugen_log.exists():
            return False

        try:
            content = mugen_log.read_text(encoding='utf-8', errors='ignore')

            # Le jeu a crashé s'il a chargé des choses mais ne s'est pas terminé proprement
            if 'Loading character' in content or 'Gameflow' in content:
                if 'Successful program termination' not in content:
                    # Vérifier si le jeu est encore en cours
                    is_running, _ = self.is_game_running()
                    if not is_running:
                        return True  # Crash détecté

            return False
        except:
            return False

    def launch_and_test_match(self, test_num, duration=60):
        """Lance le jeu et teste un match"""
        self.log(f"\n{'='*60}")
        self.log(f"TEST #{test_num}: Lancement et entrée en combat", "TEST")
        self.log(f"{'='*60}")

        # S'assurer que le jeu est fermé
        self.kill_game()
        time.sleep(2)

        # Supprimer l'ancien log
        mugen_log = self.base_path / "mugen.log"
        if mugen_log.exists():
            mugen_log.unlink()

        # Lancer le jeu
        self.log("Lancement du jeu...", "INFO")
        try:
            subprocess.Popen(
                [str(self.game_exe)],
                cwd=str(self.base_path)
            )
        except Exception as e:
            self.log(f"Erreur au lancement: {e}", "ERROR")
            self.tests_failed += 1
            return False

        # Attendre que le jeu démarre
        self.log("Attente démarrage (15s)...", "INFO")
        time.sleep(15)

        # Vérifier que le jeu tourne
        is_running, proc = self.is_game_running()
        if not is_running:
            self.log("Le jeu ne s'est pas lancé!", "ERROR")
            self.tests_failed += 1
            return False

        self.log("✓ Jeu lancé avec succès", "SUCCESS")

        # Attendre écran titre
        self.log("Navigation vers menu (10s)...", "INFO")
        time.sleep(10)

        # Simuler navigation - Espace pour passer le titre
        try:
            import pyautogui
            pyautogui.FAILSAFE = False

            # Passer écran titre
            pyautogui.press('space')
            time.sleep(3)

            # Sélectionner Versus (descendre une fois et valider)
            pyautogui.press('down')
            time.sleep(1)
            pyautogui.press('return')
            time.sleep(5)

            self.log("✓ Navigation menu OK", "SUCCESS")

            # Sélection personnages aléatoires
            self.log("Sélection personnages aléatoires...", "INFO")

            # Joueur 1 - Naviguer aléatoirement
            moves = random.randint(3, 10)
            for _ in range(moves):
                direction = random.choice(['up', 'down', 'left', 'right'])
                pyautogui.press(direction)
                time.sleep(0.3)

            # Sélectionner avec START maintenu (mode manuel)
            pyautogui.keyDown('space')
            time.sleep(0.2)
            pyautogui.press('return')
            time.sleep(0.3)
            pyautogui.keyUp('space')

            self.log("✓ Personnage 1 sélectionné", "SUCCESS")
            time.sleep(3)

            # Vérifier si crash après sélection perso 1
            if self.check_for_crash():
                self.log("CRASH après sélection personnage 1!", "ERROR")
                self.crashes_detected += 1
                self.tests_failed += 1
                self.kill_game()
                return False

            # Joueur 2 - Naviguer aléatoirement
            moves = random.randint(3, 10)
            for _ in range(moves):
                direction = random.choice(['up', 'down', 'left', 'right'])
                pyautogui.press(direction)
                time.sleep(0.3)

            # Sélectionner avec START maintenu
            pyautogui.keyDown('space')
            time.sleep(0.2)
            pyautogui.press('return')
            time.sleep(0.3)
            pyautogui.keyUp('space')

            self.log("✓ Personnage 2 sélectionné", "SUCCESS")
            time.sleep(5)

            # Vérifier si crash après sélection perso 2
            if self.check_for_crash():
                self.log("CRASH après sélection personnage 2!", "ERROR")
                self.crashes_detected += 1
                self.tests_failed += 1
                self.kill_game()
                return False

            # Attendre chargement combat (moment critique)
            self.log("⏳ Attente chargement combat (moment critique)...", "WARNING")
            time.sleep(10)

            # Vérifier si crash pendant chargement
            is_running, _ = self.is_game_running()
            if not is_running or self.check_for_crash():
                self.log("❌ CRASH pendant chargement du combat!", "ERROR")
                self.crashes_detected += 1
                self.tests_failed += 1
                return False

            self.log("✅ COMBAT CHARGÉ SANS CRASH!", "SUCCESS")

            # Combat pendant quelques secondes
            self.log(f"Combat en cours ({duration}s)...", "INFO")
            keys = ['a', 's', 'z', 'x', 'left', 'right']

            start_time = time.time()
            while (time.time() - start_time) < duration:
                key = random.choice(keys)
                pyautogui.press(key)
                time.sleep(random.uniform(0.3, 0.8))

                # Vérifier périodiquement si crash
                if int(time.time() - start_time) % 10 == 0:
                    is_running, _ = self.is_game_running()
                    if not is_running or self.check_for_crash():
                        self.log("CRASH pendant le combat!", "ERROR")
                        self.crashes_detected += 1
                        self.tests_failed += 1
                        return False

            self.log("✅ Combat terminé sans crash!", "SUCCESS")
            self.tests_passed += 1

            # Fermer proprement
            self.kill_game()
            time.sleep(2)

            return True

        except ImportError:
            self.log("pyautogui non disponible - test partiel", "WARNING")
            time.sleep(duration)
            is_running, _ = self.is_game_running()
            if not is_running or self.check_for_crash():
                self.crashes_detected += 1
                self.tests_failed += 1
                return False
            else:
                self.tests_passed += 1
                self.kill_game()
                return True

        except Exception as e:
            self.log(f"Erreur pendant test: {e}", "ERROR")
            self.tests_failed += 1
            self.kill_game()
            return False

    def run_multiple_tests(self, num_tests=3):
        """Lance plusieurs tests"""
        print("\n" + "="*70)
        print("  🧪 TEST ANTI-CRASH - VALIDATION CORRECTIONS")
        print("="*70 + "\n")

        for i in range(1, num_tests + 1):
            success = self.launch_and_test_match(i, duration=30)

            if success:
                self.log(f"✅ Test #{i} RÉUSSI\n", "SUCCESS")
            else:
                self.log(f"❌ Test #{i} ÉCHOUÉ\n", "ERROR")

            # Pause entre les tests
            if i < num_tests:
                self.log("Pause 5s avant prochain test...\n", "INFO")
                time.sleep(5)

        # Rapport final
        print("\n" + "="*70)
        print("  📊 RAPPORT FINAL")
        print("="*70)
        print(f"\n✅ Tests réussis: {self.tests_passed}/{num_tests}")
        print(f"❌ Tests échoués: {self.tests_failed}/{num_tests}")
        print(f"💥 Crashs détectés: {self.crashes_detected}")

        if self.crashes_detected == 0:
            print("\n🎉 SUCCÈS TOTAL - AUCUN CRASH DÉTECTÉ!")
            print("Les corrections ont fonctionné!\n")
        else:
            print(f"\n⚠️  {self.crashes_detected} crashs détectés")
            print("D'autres corrections peuvent être nécessaires.\n")

        print("="*70 + "\n")

if __name__ == "__main__":
    tester = AntiCrashTester()
    tester.run_multiple_tests(num_tests=3)
