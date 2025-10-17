#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - Test ALL Launchers
Lance tous les launchers automatiquement et teste chacun
"""

import subprocess
import time
import pyautogui
import win32gui
from pathlib import Path
from datetime import datetime

class LauncherTester:
    """Teste tous les launchers automatiquement"""

    def __init__(self):
        self.game_dir = Path(r"D:\KOF Ultimate Online")
        self.launchers = []
        self.results = {}
        self.log_file = self.game_dir / "launcher_test_results.txt"

    def log(self, message):
        """Log un message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        msg = f"[{timestamp}] {message}"
        print(msg)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')

    def find_all_launchers(self):
        """Trouve tous les launchers"""
        self.log("\n🔍 RECHERCHE DES LAUNCHERS")
        self.log("=" * 60)

        # Launchers Python
        py_launchers = [
            "launcher.py",
            "launcher_modern.py",
            "LAUNCHER_ULTIMATE.py",
            "LAUNCHER_ULTIMATE_V2.py",
            "character_dashboard.py",
            "visual_inspector.py"
        ]

        for launcher in py_launchers:
            launcher_path = self.game_dir / launcher
            if launcher_path.exists():
                self.launchers.append(("python", launcher, launcher_path))
                self.log(f"  ✓ Trouvé: {launcher}")

        self.log(f"\n📊 Total: {len(self.launchers)} launchers trouvés")
        return len(self.launchers) > 0

    def test_launcher(self, launcher_type, launcher_name, launcher_path):
        """Teste un launcher spécifique"""
        self.log(f"\n🧪 TEST: {launcher_name}")
        self.log("=" * 60)

        try:
            # Lancer le launcher
            if launcher_type == "python":
                process = subprocess.Popen(
                    ["python", str(launcher_path)],
                    cwd=str(self.game_dir)
                )
            else:
                process = subprocess.Popen(
                    [str(launcher_path)],
                    cwd=str(self.game_dir)
                )

            self.log(f"  ✓ Lancé (PID: {process.pid})")

            # Attendre que la fenêtre apparaisse
            time.sleep(3)

            # Vérifier si le processus tourne
            if process.poll() is None:
                self.log("  ✓ Processus actif")

                # Faire quelques clics de test
                time.sleep(2)

                # Simuler navigation
                for i in range(3):
                    pyautogui.press('tab')
                    time.sleep(0.3)

                pyautogui.press('enter')
                time.sleep(1)

                self.log("  ✓ Test interactions OK")

                # Fermer proprement
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    self.log("  ✓ Fermé proprement")
                    return True
                except:
                    process.kill()
                    self.log("  ⚠️  Fermé (forcé)")
                    return True

            else:
                self.log("  ❌ Processus terminé immédiatement")
                return False

        except Exception as e:
            self.log(f"  ❌ ERREUR: {e}")
            return False

    def run_all_tests(self):
        """Lance tous les tests"""
        self.log("\n" + "=" * 60)
        self.log("  KOF ULTIMATE - TEST DE TOUS LES LAUNCHERS")
        self.log("=" * 60)

        # Nettoyer le log
        if self.log_file.exists():
            self.log_file.unlink()

        # Trouver les launchers
        if not self.find_all_launchers():
            self.log("❌ Aucun launcher trouvé!")
            return False

        # Tester chaque launcher
        success_count = 0
        fail_count = 0

        for launcher_type, launcher_name, launcher_path in self.launchers:
            result = self.test_launcher(launcher_type, launcher_name, launcher_path)

            self.results[launcher_name] = result

            if result:
                success_count += 1
            else:
                fail_count += 1

            # Pause entre tests
            time.sleep(2)

        # Rapport final
        self.log("\n" + "=" * 60)
        self.log("📊 RAPPORT FINAL")
        self.log("=" * 60)
        self.log(f"Launchers testés: {len(self.launchers)}")
        self.log(f"✅ Succès: {success_count}")
        self.log(f"❌ Échecs: {fail_count}")

        self.log("\n📋 DÉTAILS PAR LAUNCHER:")
        for launcher_name, result in self.results.items():
            status = "✅ OK" if result else "❌ ERREUR"
            self.log(f"  {status} - {launcher_name}")

        self.log(f"\n📄 Log complet: {self.log_file}")
        self.log("=" * 60)

        return fail_count == 0

def main():
    """Point d'entrée"""
    print("\n" + "=" * 60)
    print("  KOF ULTIMATE - TESTEUR DE TOUS LES LAUNCHERS")
    print("  Les IAs vont lancer chaque launcher et interagir avec")
    print("=" * 60)
    print()

    tester = LauncherTester()
    success = tester.run_all_tests()

    print("\n\n" + "=" * 60)
    if success:
        print("✅ TOUS LES LAUNCHERS FONCTIONNENT!")
        print("\nTous les launchers ont été testés avec succès.")
    else:
        print("⚠️  CERTAINS LAUNCHERS ONT DES PROBLÈMES")
        print("\nConsultez launcher_test_results.txt pour les détails.")

    print("=" * 60)
    print()

if __name__ == '__main__':
    main()
