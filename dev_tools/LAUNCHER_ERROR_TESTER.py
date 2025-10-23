#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - TESTEUR D'ERREURS DES LAUNCHERS
Capture TOUTES les erreurs des launchers quand on clique sur les boutons
"""

import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
import threading
import queue

game_dir = Path(r"D:\KOF Ultimate Online Online Online")

class LauncherErrorTester:
    """Testeur d'erreurs de launcher"""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.output_queue = queue.Queue()

    def log(self, message, level='INFO'):
        """Log message"""
        symbols = {
            'INFO': 'ℹ️',
            'SUCCESS': '✅',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'TEST': '🧪'
        }
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {symbols.get(level, '•')} {message}")

    def read_output(self, pipe, stream_name):
        """Lit la sortie d'un pipe dans un thread"""
        try:
            for line in iter(pipe.readline, ''):
                if line:
                    self.output_queue.put((stream_name, line.strip()))
        except:
            pass

    def test_launcher(self, launcher_name):
        """Teste un launcher en capturant toutes les erreurs"""
        self.log(f"TEST DU LAUNCHER: {launcher_name}", 'TEST')
        print("=" * 70)
        print()

        launcher_path = game_dir / launcher_name

        if not launcher_path.exists():
            self.log(f"Launcher introuvable: {launcher_name}", 'ERROR')
            return

        try:
            # Lancer le launcher
            self.log("Lancement du launcher...")

            proc = subprocess.Popen(
                [sys.executable, str(launcher_path)],
                cwd=str(game_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            # Threads pour lire stdout et stderr
            stdout_thread = threading.Thread(
                target=self.read_output,
                args=(proc.stdout, 'STDOUT'),
                daemon=True
            )
            stderr_thread = threading.Thread(
                target=self.read_output,
                args=(proc.stderr, 'STDERR'),
                daemon=True
            )

            stdout_thread.start()
            stderr_thread.start()

            # Attendre un peu que le launcher démarre
            time.sleep(3)

            self.log("Launcher démarré, capture de la sortie...")
            print()

            # Simuler des interactions (appuyer sur les touches du menu)
            interactions = [
                ('1', 'Choix 1 - JOUER'),
                ('', 'ENTER'),
                ('2', 'Choix 2 - Vérifier mises à jour'),
                ('', 'ENTER'),
                ('3', 'Choix 3 - Auto-réparation'),
                ('', 'ENTER'),
                ('4', 'Choix 4 - Diagnostic'),
                ('', 'ENTER'),
                ('0', 'Choix 0 - Quitter')
            ]

            for choice, description in interactions:
                try:
                    self.log(f"  → {description}")
                    if choice:
                        proc.stdin.write(choice + '\n')
                    else:
                        proc.stdin.write('\n')
                    proc.stdin.flush()
                    time.sleep(2)

                    # Capturer la sortie
                    self.capture_output(5)

                except Exception as e:
                    self.log(f"  Erreur interaction: {e}", 'ERROR')
                    self.errors.append(f"{launcher_name} - {description}: {e}")

            # Terminer proprement
            try:
                proc.stdin.write('0\n')
                proc.stdin.flush()
                time.sleep(1)
            except:
                pass

            # Attendre la fin ou forcer l'arrêt
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.terminate()
                time.sleep(1)
                if proc.poll() is None:
                    proc.kill()

            # Capturer la sortie finale
            self.capture_output(2)

            print()
            print("=" * 70)
            print()

        except Exception as e:
            self.log(f"Erreur lors du test: {e}", 'ERROR')
            self.errors.append(f"{launcher_name}: {e}")

    def capture_output(self, timeout=1):
        """Capture et affiche la sortie pendant un certain temps"""
        start = time.time()

        while time.time() - start < timeout:
            try:
                stream_name, line = self.output_queue.get(timeout=0.1)

                # Détecter les erreurs
                if any(keyword in line.lower() for keyword in ['error', 'erreur', 'exception', 'traceback', 'failed', 'échec']):
                    self.log(f"  {stream_name}: {line}", 'ERROR')
                    self.errors.append(line)
                elif any(keyword in line.lower() for keyword in ['warning', 'avertissement', 'attention']):
                    self.log(f"  {stream_name}: {line}", 'WARNING')
                    self.warnings.append(line)
                else:
                    # Afficher toute la sortie pour debug
                    print(f"  {stream_name}: {line}")

            except queue.Empty:
                pass

    def test_all_launchers(self):
        """Teste tous les launchers"""
        self.log("DÉBUT DES TESTS DE TOUS LES LAUNCHERS", 'TEST')
        print("=" * 70)
        print()

        launchers = [
            'launcher.py',
            'launcher_modern.py',
            'LAUNCHER_ULTIMATE.py',
            'LAUNCHER_ULTIMATE_V2.py'
        ]

        for launcher in launchers:
            self.test_launcher(launcher)
            time.sleep(2)

        self.generate_report()

    def generate_report(self):
        """Génère un rapport des erreurs"""
        print()
        print("=" * 70)
        print("📊 RAPPORT DES ERREURS DES LAUNCHERS")
        print("=" * 70)
        print()

        print(f"Total d'erreurs détectées: {len(self.errors)}")
        print(f"Total d'avertissements: {len(self.warnings)}")
        print()

        if self.errors:
            print("🔍 ERREURS DÉTECTÉES:")
            print()
            for i, error in enumerate(self.errors, 1):
                print(f"{i}. ❌ {error}")
            print()

        if self.warnings:
            print("⚠️  AVERTISSEMENTS:")
            print()
            for i, warning in enumerate(self.warnings, 1):
                print(f"{i}. ⚠️ {warning}")
            print()

        # Sauvegarder dans un fichier
        report_file = game_dir / f"launcher_errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("RAPPORT DES ERREURS DES LAUNCHERS\n")
            f.write("=" * 70 + "\n\n")

            f.write(f"Total d'erreurs: {len(self.errors)}\n")
            f.write(f"Total d'avertissements: {len(self.warnings)}\n\n")

            if self.errors:
                f.write("ERREURS:\n")
                for i, error in enumerate(self.errors, 1):
                    f.write(f"{i}. {error}\n")
                f.write("\n")

            if self.warnings:
                f.write("AVERTISSEMENTS:\n")
                for i, warning in enumerate(self.warnings, 1):
                    f.write(f"{i}. {warning}\n")
                f.write("\n")

        self.log(f"Rapport sauvegardé: {report_file.name}", 'SUCCESS')
        print("=" * 70)
        print()

def main():
    """Main function"""
    print()
    print("=" * 70)
    print("  🔍 KOF ULTIMATE - TESTEUR D'ERREURS LAUNCHERS")
    print("=" * 70)
    print()

    tester = LauncherErrorTester()
    tester.test_all_launchers()

    print()
    try:
        input("Appuyez sur ENTRÉE pour fermer...")
    except EOFError:
        pass

if __name__ == '__main__':
    main()
