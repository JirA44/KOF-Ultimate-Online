#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - Auto Clicker
Clique automatiquement pour éviter les erreurs et passer les écrans
Sans besoin de clé API
"""

import time
import pyautogui
import win32gui
import win32con
import subprocess
from pathlib import Path

class KOFAutoClicker:
    """Auto-clicker pour KOF Ultimate"""

    def __init__(self):
        self.game_dir = Path(r"D:\KOF Ultimate Online")
        self.exe_path = self.game_dir / "KOF_Ultimate_Online.exe"
        self.process = None
        self.window_handle = None
        self.is_running = False

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

    def focus_game_window(self):
        """Met le focus sur la fenêtre du jeu"""
        if self.window_handle:
            try:
                win32gui.ShowWindow(self.window_handle, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(self.window_handle)
                time.sleep(0.2)
                return True
            except:
                return False
        return False

    def launch_game(self):
        """Lance le jeu"""
        print("🎮 Lancement du jeu...")

        if not self.exe_path.exists():
            print(f"❌ Exécutable non trouvé: {self.exe_path}")
            return False

        try:
            # Lancer le jeu
            self.process = subprocess.Popen(
                [str(self.exe_path)],
                cwd=str(self.game_dir)
            )

            print(f"✅ Jeu lancé (PID: {self.process.pid})")

            # Attendre que la fenêtre apparaisse
            print("⏳ Attente de la fenêtre du jeu...")
            for i in range(30):
                time.sleep(0.5)
                if self.find_game_window():
                    print("✅ Fenêtre trouvée!")
                    self.is_running = True
                    return True

            print("❌ Fenêtre non trouvée")
            return False

        except Exception as e:
            print(f"❌ Erreur au lancement: {e}")
            return False

    def auto_click_sequence(self):
        """Séquence de clics automatiques pour passer les écrans"""
        print("\n🖱️  AUTO-CLICKER ACTIF")
        print("=" * 60)

        # Attendre le chargement initial
        print("\n[1/6] Attente chargement initial (10s)...")
        time.sleep(10)

        # Séquence de navigation dans les menus
        actions = [
            ("Clic Entrée (passer écran de titre)", "enter", 2),
            ("Clic Entrée (confirmer)", "enter", 1.5),
            ("Navigation vers Arcade Mode", "down", 0.5),
            ("Sélection Arcade Mode", "enter", 2),
            ("Attente écran sélection", None, 2),
            ("Sélection personnage (Entrée)", "enter", 1.5),
            ("Confirmation équipe", "enter", 2),
        ]

        for i, (description, key, wait) in enumerate(actions, 2):
            print(f"\n[{i}/6] {description}...")

            if self.focus_game_window():
                if key:
                    pyautogui.press(key)
                    print(f"   ✓ Touche '{key}' appuyée")
            else:
                print("   ⚠ Focus perdu, tentative de récupération...")
                self.find_game_window()

            time.sleep(wait)

        print("\n" + "=" * 60)
        print("✅ Séquence terminée! Le jeu devrait être lancé.")
        print("\n💡 CONSEIL: Le jeu est maintenant en mode combat.")
        print("   Vous pouvez jouer normalement!")

    def monitor_and_click(self, duration_minutes=30):
        """Surveille et clique périodiquement pendant X minutes"""
        print(f"\n🔄 Mode surveillance activé pour {duration_minutes} minutes")
        print("   Clics automatiques toutes les 5 secondes...")

        end_time = time.time() + (duration_minutes * 60)

        while time.time() < end_time and self.is_running:
            # Vérifier si le jeu tourne toujours
            if not self.find_game_window():
                print("\n⚠ Fenêtre du jeu perdue!")
                break

            # Cliquer périodiquement pour éviter les timeouts
            if self.focus_game_window():
                # Alterner entre différentes touches
                keys = ["enter", "space", "escape"]
                key = keys[int(time.time()) % len(keys)]

                pyautogui.press(key)
                print(f"⏱️  {time.strftime('%H:%M:%S')} - Clic: {key}", end='\r')

            time.sleep(5)

        print("\n\n✅ Surveillance terminée")

    def run_complete_sequence(self):
        """Lance le jeu avec auto-clicker complet"""
        print("\n" + "=" * 60)
        print("  KOF ULTIMATE - AUTO CLICKER")
        print("  Évite les erreurs et lance le jeu automatiquement")
        print("=" * 60)

        # Lancer le jeu
        if not self.launch_game():
            print("\n❌ Impossible de lancer le jeu")
            return

        # Séquence de clics
        self.auto_click_sequence()

        # Mode surveillance (optionnel)
        print("\n" + "=" * 60)
        print("Mode surveillance désactivé pour l'instant.")
        print("Le jeu est lancé et prêt!")
        print("=" * 60)

def main():
    """Point d'entrée"""
    try:
        # Vérifier les dépendances
        import pyautogui
        import win32gui
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("\n📥 Installation...")

        module = str(e).split()[-1].replace("'", "")
        if "pyautogui" in module:
            import subprocess
            subprocess.run([
                "python", "-m", "pip", "install", "pyautogui"
            ])
        elif "win32gui" in module:
            import subprocess
            subprocess.run([
                "python", "-m", "pip", "install", "pywin32"
            ])

        print("\n✅ Dépendances installées!")
        print("⚠️  Veuillez relancer ce script.\n")
        input("Appuyez sur Entrée pour quitter...")
        return

    clicker = KOFAutoClicker()
    clicker.run_complete_sequence()

    print("\n\n🎮 Le jeu tourne maintenant!")
    print("   Vous pouvez fermer cette fenêtre.\n")

    input("Appuyez sur Entrée pour quitter l'auto-clicker...")

if __name__ == '__main__':
    main()
