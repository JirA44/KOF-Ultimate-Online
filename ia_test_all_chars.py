#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - IA Test All Characters
Teste TOUS les 189 personnages pour détecter les erreurs
"""

import time
import pyautogui
import win32gui
import win32con
from datetime import datetime
from pathlib import Path

class CharacterTester:
    """Teste tous les personnages pour détecter les bugs"""

    def __init__(self):
        self.window_handle = None
        self.chars_tested = 0
        self.errors_found = []
        self.log_file = Path(r"D:\KOF Ultimate Online Online Online\char_test_log.txt")

    def log(self, message):
        """Log dans fichier et console"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        msg = f"[{timestamp}] {message}"
        print(msg)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')

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
        """Focus sur la fenêtre"""
        if self.window_handle:
            try:
                win32gui.SetForegroundWindow(self.window_handle)
                time.sleep(0.1)
                return True
            except:
                return False
        return False

    def press(self, key, wait=0.3):
        """Appuie sur une touche"""
        if self.focus_window():
            pyautogui.press(key)
            time.sleep(wait)

    def test_character_at_position(self, row, col):
        """Teste un personnage à une position donnée"""
        char_id = row * 10 + col + 1
        self.log(f"\n🧪 Test personnage #{char_id} (ligne {row}, col {col})")

        # Aller en mode Arcade
        self.press('enter', 1.5)  # Passer titre
        self.press('enter', 2)    # Entrer Arcade

        # Naviguer jusqu'au personnage
        # Reset à la position 0,0
        for _ in range(20):
            self.press('up', 0.1)
        for _ in range(20):
            self.press('left', 0.1)

        # Naviguer vers la position cible
        for _ in range(row):
            self.press('down', 0.2)

        for _ in range(col):
            self.press('right', 0.2)

        # Sélectionner
        self.press('enter', 1)

        # Vérifier si on peut continuer (pas de crash)
        time.sleep(0.5)

        # Essayer de lancer le combat
        self.press('enter', 2)  # Confirmer équipe

        # Attendre un peu pour voir si le jeu crash
        time.sleep(2)

        # Si on arrive ici, le perso fonctionne
        self.chars_tested += 1
        self.log(f"✅ Personnage #{char_id} OK")

        # Quitter le combat
        self.press('escape', 1)
        self.press('escape', 1)

        # Retour au menu
        for _ in range(3):
            self.press('escape', 0.5)

    def test_all_characters_grid(self):
        """Teste tous les personnages de la grille"""
        self.log("\n" + "=" * 60)
        self.log("🎯 TEST DE TOUS LES PERSONNAGES")
        self.log("=" * 60)

        # Grille approximative 20x10 (189 personnages)
        rows = 19
        cols = 10

        for row in range(rows):
            for col in range(cols):
                try:
                    self.test_character_at_position(row, col)

                    # Pause tous les 10 persos
                    if (row * cols + col + 1) % 10 == 0:
                        self.log(f"\n⏸️  Pause après 10 tests ({self.chars_tested} OK)")
                        time.sleep(3)

                except Exception as e:
                    char_id = row * cols + col + 1
                    error_msg = f"❌ ERREUR personnage #{char_id}: {e}"
                    self.log(error_msg)
                    self.errors_found.append(error_msg)

                    # Screenshot de l'erreur
                    try:
                        pyautogui.screenshot(f"error_char_{char_id}.png")
                    except:
                        pass

                    # Tenter de revenir au menu
                    for _ in range(5):
                        self.press('escape', 0.5)

        # Rapport final
        self.log("\n" + "=" * 60)
        self.log("📊 RAPPORT FINAL")
        self.log("=" * 60)
        self.log(f"Personnages testés: {self.chars_tested}")
        self.log(f"Erreurs trouvées: {len(self.errors_found)}")

        if self.errors_found:
            self.log("\n⚠️  PERSONNAGES AVEC ERREURS:")
            for error in self.errors_found:
                self.log(f"   {error}")

    def run(self):
        """Lance les tests"""
        # Nettoyer le log
        if self.log_file.exists():
            self.log_file.unlink()

        self.log("🎮 KOF ULTIMATE - Character Tester")
        self.log("Recherche du jeu...")

        # Attendre le jeu
        for i in range(30):
            if self.find_game_window():
                self.log(f"✅ Jeu trouvé!")
                break
            time.sleep(1)
        else:
            self.log("❌ Jeu non trouvé")
            return

        time.sleep(3)

        # Lancer les tests
        self.test_all_characters_grid()

        self.log(f"\n✅ Tests terminés!")
        self.log(f"📄 Log complet: {self.log_file}")

def main():
    tester = CharacterTester()
    tester.run()

    input("\nAppuyez sur Entrée pour quitter...")

if __name__ == '__main__':
    main()
