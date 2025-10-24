#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFY SELECT SCREEN - Vérifie qu'il n'y a plus de cases vides
"""

import subprocess
import time
import psutil
from pathlib import Path
from datetime import datetime

class SelectScreenVerifier:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.game_exe = self.base_path / "KOF_Ultimate_Online.exe"
        self.select_file = self.base_path / "data" / "select.def"

    def log(self, msg, level="INFO"):
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "TEST": "🧪"}
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {icons.get(level, '')} {msg}")

    def analyze_select_def(self):
        """Analyse le fichier select.def"""
        self.log("\n" + "="*60)
        self.log("ANALYSE FICHIER SELECT.DEF", "TEST")
        self.log("="*60)

        with open(self.select_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        active_chars = []
        disabled_chars = []
        in_chars_section = False

        for line in lines:
            stripped = line.strip()

            if '[Characters]' in line:
                in_chars_section = True
                continue

            if stripped.startswith('[') and in_chars_section:
                break  # Fin section Characters

            if in_chars_section and stripped:
                if stripped.startswith(';'):
                    # Ligne commentée
                    if ',' in stripped:
                        char_name = stripped.lstrip(';').split(',')[0].strip()
                        if char_name and not char_name.startswith('='):
                            disabled_chars.append(char_name)
                elif ',' in stripped:
                    char_name = stripped.split(',')[0].strip()
                    if char_name:
                        active_chars.append(char_name)

        self.log(f"\n✅ Personnages actifs: {len(active_chars)}", "SUCCESS")
        self.log(f"⏸️  Personnages désactivés: {len(disabled_chars)}", "INFO")

        return active_chars, disabled_chars

    def verify_character_folders(self, char_names):
        """Vérifie que tous les personnages actifs ont un dossier"""
        self.log("\n" + "="*60)
        self.log("VÉRIFICATION DOSSIERS PERSONNAGES", "TEST")
        self.log("="*60 + "\n")

        chars_dir = self.base_path / "chars"
        missing = []
        found = []

        for char_name in char_names:
            char_path = chars_dir / char_name
            if char_path.exists():
                found.append(char_name)
            else:
                missing.append(char_name)
                self.log(f"❌ MANQUANT: {char_name}", "ERROR")

        self.log(f"\n✅ Personnages trouvés: {len(found)}/{len(char_names)}", "SUCCESS")

        if missing:
            self.log(f"❌ Personnages manquants: {len(missing)}", "ERROR")
            return False
        else:
            self.log("✅ Tous les personnages actifs existent!", "SUCCESS")
            return True

    def launch_and_check_grid(self):
        """Lance le jeu et vérifie visuellement la grille"""
        self.log("\n" + "="*60)
        self.log("VÉRIFICATION VISUELLE GRILLE", "TEST")
        self.log("="*60 + "\n")

        # Fermer jeu si ouvert
        for proc in psutil.process_iter(['name']):
            try:
                if 'KOF_Ultimate_Online.exe' in proc.info['name']:
                    proc.terminate()
                    time.sleep(2)
            except:
                pass

        # Lancer le jeu
        self.log("Lancement du jeu...", "INFO")
        try:
            subprocess.Popen([str(self.game_exe)], cwd=str(self.base_path))
            time.sleep(15)
        except Exception as e:
            self.log(f"Erreur: {e}", "ERROR")
            return False

        # Navigation vers écran sélection
        try:
            import pyautogui
            pyautogui.FAILSAFE = False

            self.log("Navigation vers écran sélection...", "INFO")
            time.sleep(5)

            # Passer titre
            pyautogui.press('space')
            time.sleep(3)

            # Aller vers Versus
            pyautogui.press('down')
            time.sleep(1)
            pyautogui.press('return')
            time.sleep(5)

            self.log("\n" + "="*60)
            self.log("✅ ÉCRAN DE SÉLECTION AFFICHÉ", "SUCCESS")
            self.log("="*60)
            self.log("\n⚠️  VÉRIFICATION MANUELLE REQUISE:", "INFO")
            self.log("1. Regardez l'écran du jeu", "INFO")
            self.log("2. Parcourez la grille avec les flèches", "INFO")
            self.log("3. Vérifiez qu'il n'y a AUCUNE case vide", "INFO")
            self.log("4. Tous les portraits doivent être visibles", "INFO")
            self.log("\n⏱️  Temps pour vérification: 60 secondes", "INFO")
            self.log("\nAppuyez ESC dans le jeu pour quitter\n", "INFO")

            # Laisser 60s pour vérification manuelle
            time.sleep(60)

            # Fermer jeu
            for proc in psutil.process_iter(['name']):
                try:
                    if 'KOF_Ultimate_Online.exe' in proc.info['name']:
                        proc.terminate()
                except:
                    pass

            return True

        except ImportError:
            self.log("pyautogui non disponible", "WARNING")
            self.log("Le jeu est lancé - vérifiez manuellement", "INFO")
            self.log("Appuyez sur Entrée quand vous avez terminé...", "INFO")
            input()
            return True

    def run(self):
        """Lance la vérification complète"""
        print("\n" + "="*70)
        print("  📋 VÉRIFICATION GRILLE DE SÉLECTION")
        print("="*70 + "\n")

        # Analyser select.def
        active_chars, disabled_chars = self.analyze_select_def()

        # Vérifier dossiers
        folders_ok = self.verify_character_folders(active_chars)

        # Vérification visuelle
        if folders_ok:
            self.launch_and_check_grid()

        # Rapport final
        print("\n" + "="*70)
        print("  📊 RAPPORT VÉRIFICATION GRILLE")
        print("="*70)
        print(f"\n✅ Personnages actifs: {len(active_chars)}")
        print(f"⏸️  Personnages désactivés: {len(disabled_chars)}")
        print(f"✅ Tous les dossiers existent: {'OUI' if folders_ok else 'NON'}")
        print("\n✅ Si aucune case vide n'a été observée à l'écran,")
        print("   le problème est RÉSOLU!\n")
        print("="*70 + "\n")

if __name__ == "__main__":
    verifier = SelectScreenVerifier()
    verifier.run()
