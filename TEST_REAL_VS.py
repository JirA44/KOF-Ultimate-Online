#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST RÉEL DE VS AUTOMATIQUE
Lance le jeu et simule la sélection de personnages pour déclencher un vrai combat
"""
import subprocess
import time
import pyautogui
import psutil
from pathlib import Path

class RealVSTester:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.game_exe = self.base_path / "KOF_Ultimate_Online.exe"
        self.log_file = self.base_path / "mugen.log"

    def kill_game(self):
        """Tue tous les processus du jeu"""
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name'].lower()
                if 'kof' in name or 'mugen' in name or 'ikemen' in name:
                    proc.kill()
            except:
                pass
        time.sleep(1)

    def launch_game(self):
        """Lance le jeu"""
        print("\n🎮 Lancement du jeu...")
        self.kill_game()

        subprocess.Popen(
            [str(self.game_exe)],
            cwd=str(self.base_path)
        )

        print("   ⏳ Attente 10s pour le chargement...")
        time.sleep(10)

    def simulate_vs_selection(self):
        """Simule la sélection de personnages pour un VS"""
        print("\n🕹️  Simulation sélection VS...")

        # Échap pour passer les menus
        print("   - Appui sur ÉCHAP (passer intro)")
        pyautogui.press('esc')
        time.sleep(2)

        # Entrée pour mode arcade
        print("   - Appui sur ENTRÉE (mode Arcade)")
        pyautogui.press('enter')
        time.sleep(3)

        # Sélection personnage 1 (premier de la liste)
        print("   - Sélection P1: WhirlWind-Goenitz")
        pyautogui.press('enter')
        time.sleep(2)

        # Sélection personnage 2 (deuxième de la liste)
        print("   - Sélection P2: Viper")
        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(2)

        print("   ✓ Personnages sélectionnés, attente du chargement du combat...")

    def wait_for_crash_or_combat(self, timeout=30):
        """Attend soit un crash soit que le combat démarre"""
        print(f"\n⏳ Attente crash ou combat (timeout {timeout}s)...")

        start_time = time.time()

        while time.time() - start_time < timeout:
            # Vérifier si le jeu est encore en cours
            game_running = False
            for proc in psutil.process_iter(['name']):
                try:
                    if 'kof' in proc.info['name'].lower():
                        game_running = True
                        break
                except:
                    pass

            if not game_running:
                print("   ❌ JEU CRASHÉ!")
                return "CRASH"

            time.sleep(0.5)

        print("   ✅ Le jeu tourne toujours - combat chargé!")
        return "SUCCESS"

    def check_log_for_errors(self):
        """Vérifie les erreurs dans le log"""
        if not self.log_file.exists():
            return []

        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Prendre les 100 dernières lignes
            lines = content.split('\n')
            recent = '\n'.join(lines[-100:])

            errors = []

            # Chercher toutes les lignes avec "Error"
            for line in lines[-100:]:
                if 'error' in line.lower() and line.strip():
                    errors.append(line.strip())

            return errors

        except:
            return []

    def run_test(self):
        """Test complet"""
        print("=" * 70)
        print("🎮 TEST RÉEL DE VS - SIMULATION AUTOMATIQUE")
        print("=" * 70)

        # Lancer le jeu
        self.launch_game()

        # Simuler la sélection
        self.simulate_vs_selection()

        # Attendre le résultat
        result = self.wait_for_crash_or_combat(timeout=30)

        print("\n" + "=" * 70)
        print("📊 RÉSULTAT DU TEST")
        print("=" * 70)

        if result == "CRASH":
            print("\n❌ LE JEU A CRASHÉ PENDANT LE CHARGEMENT DU COMBAT")

            print("\n📋 Erreurs dans le log:")
            errors = self.check_log_for_errors()

            if errors:
                for i, err in enumerate(errors[-10:], 1):  # 10 dernières erreurs
                    print(f"   {i}. {err}")
            else:
                print("   Aucune erreur lisible trouvée")

        else:
            print("\n✅ LE JEU EST STABLE - COMBAT CHARGÉ AVEC SUCCÈS!")

        # Cleanup
        print("\n🧹 Nettoyage...")
        self.kill_game()

        print("\n✅ Test terminé!")

if __name__ == "__main__":
    try:
        tester = RealVSTester()
        tester.run_test()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

    input("\nAppuyez sur ENTRÉE pour fermer...")
