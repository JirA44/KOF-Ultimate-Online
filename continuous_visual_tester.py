#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - Testeur Visuel Continu
Capture l'écran et vérifie visuellement que tout fonctionne
"""

import subprocess
import time
import os
from pathlib import Path
from datetime import datetime
import pyautogui
from PIL import Image, ImageDraw, ImageFont
import win32gui
import win32con
import win32process
import psutil

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class VisualTester:
    """Testeur visuel pour KOF Ultimate"""

    def __init__(self, game_dir):
        self.game_dir = Path(game_dir)
        self.exe_path = self.game_dir / "KOF_Ultimate_Online.exe"
        self.process = None
        self.window_handle = None
        self.screenshots_dir = self.game_dir / "test_screenshots"
        self.screenshots_dir.mkdir(exist_ok=True)

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

    def launch_game(self):
        """Lance le jeu"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}🎮 LANCEMENT DU JEU{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")

        try:
            # Supprimer l'ancien log
            log_file = self.game_dir / "mugen.log"
            if log_file.exists():
                log_file.unlink()

            # Lancer le jeu
            self.process = subprocess.Popen(
                [str(self.exe_path)],
                cwd=str(self.game_dir)
            )

            print(f"{Colors.GREEN}✓ Jeu lancé (PID: {self.process.pid}){Colors.RESET}")

            # Attendre que la fenêtre apparaisse
            print(f"{Colors.CYAN}Attente de la fenêtre du jeu...{Colors.RESET}")
            for i in range(30):
                time.sleep(0.5)
                if self.find_game_window():
                    print(f"{Colors.GREEN}✓ Fenêtre trouvée!{Colors.RESET}")

                    # Mettre la fenêtre au premier plan
                    try:
                        win32gui.ShowWindow(self.window_handle, win32con.SW_RESTORE)
                        win32gui.SetForegroundWindow(self.window_handle)
                    except:
                        pass

                    return True

            print(f"{Colors.RED}✗ Fenêtre non trouvée{Colors.RESET}")
            return False

        except Exception as e:
            print(f"{Colors.RED}✗ Erreur au lancement: {e}{Colors.RESET}")
            return False

    def capture_screen(self, name):
        """Capture spécifiquement la fenêtre du jeu"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = self.screenshots_dir / filename

        try:
            if self.window_handle:
                # Obtenir les dimensions de la fenêtre du jeu
                try:
                    rect = win32gui.GetWindowRect(self.window_handle)
                    x, y, x2, y2 = rect
                    width = x2 - x
                    height = y2 - y

                    # Capturer uniquement la fenêtre du jeu
                    screenshot = pyautogui.screenshot(region=(x, y, width, height))
                    screenshot.save(str(filepath))
                    print(f"{Colors.GREEN}✓ Screenshot jeu sauvegardé: {filename}{Colors.RESET}")
                    return filepath
                except:
                    # Fallback sur capture complète
                    screenshot = pyautogui.screenshot()
                    screenshot.save(str(filepath))
                    print(f"{Colors.YELLOW}✓ Screenshot écran complet: {filename}{Colors.RESET}")
                    return filepath
            else:
                screenshot = pyautogui.screenshot()
                screenshot.save(str(filepath))
                print(f"{Colors.YELLOW}✓ Screenshot écran complet: {filename}{Colors.RESET}")
                return filepath
        except Exception as e:
            print(f"{Colors.RED}✗ Erreur capture: {e}{Colors.RESET}")
            return None

    def analyze_menu_screen(self, screenshot_path):
        """Analyse le screenshot du menu"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}🔍 ANALYSE DU MENU{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")

        try:
            img = Image.open(screenshot_path)
            pixels = img.load()
            width, height = img.size

            # Vérifier si l'écran est complètement noir
            total_brightness = 0
            sample_size = 1000

            for _ in range(sample_size):
                x = width // 4 + (_ * (width // 2)) // sample_size
                y = height // 4 + (_ * (height // 2)) // sample_size
                pixel = pixels[x, y]
                if isinstance(pixel, tuple):
                    total_brightness += sum(pixel[:3])

            avg_brightness = total_brightness / (sample_size * 3)

            print(f"  Luminosité moyenne: {avg_brightness:.1f}/255")

            if avg_brightness < 10:
                print(f"{Colors.RED}  ✗ PROBLÈME: L'écran est presque noir (pas d'animation visible){Colors.RESET}")
                return False
            elif avg_brightness < 30:
                print(f"{Colors.YELLOW}  ⚠ L'écran est très sombre{Colors.RESET}")
            else:
                print(f"{Colors.GREEN}  ✓ L'écran contient des éléments visuels{Colors.RESET}")

            # Convertir en niveaux de gris pour l'analyse de texte
            gray = img.convert('L')

            # Chercher des zones avec du texte (variations de luminosité)
            text_regions = 0
            for y in range(height // 4, 3 * height // 4, 20):
                for x in range(width // 4, 3 * width // 4, 20):
                    # Vérifier variation dans une petite zone
                    region_pixels = []
                    for dy in range(-5, 5):
                        for dx in range(-5, 5):
                            if 0 <= x+dx < width and 0 <= y+dy < height:
                                region_pixels.append(gray.getpixel((x+dx, y+dy)))

                    if len(region_pixels) > 0:
                        variance = max(region_pixels) - min(region_pixels)
                        if variance > 50:  # Zone avec contraste = probablement du texte
                            text_regions += 1

            print(f"  Régions de texte détectées: {text_regions}")

            if text_regions > 10:
                print(f"{Colors.GREEN}  ✓ Menu avec texte détecté{Colors.RESET}")
                return True
            else:
                print(f"{Colors.YELLOW}  ⚠ Peu de texte détecté - menu peut-être pas chargé{Colors.RESET}")
                return False

        except Exception as e:
            print(f"{Colors.RED}✗ Erreur analyse: {e}{Colors.RESET}")
            return False

    def wait_for_loading(self):
        """Attend que le loading soit terminé et que le menu apparaisse"""
        print(f"\n{Colors.CYAN}⏳ Attente du chargement du jeu...{Colors.RESET}")

        # Attendre 10 secondes pour le loading screen
        for i in range(10, 0, -1):
            print(f"\r  Chargement en cours... {i}s ", end='', flush=True)
            time.sleep(1)
        print()

        print(f"{Colors.GREEN}✓ Chargement terminé{Colors.RESET}")

    def test_menu_navigation(self):
        """Teste la navigation dans le menu"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}🎯 TEST DE NAVIGATION{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")

        screenshots = []

        # Capture initiale
        print(f"{Colors.CYAN}1. Capture du menu initial{Colors.RESET}")
        screen = self.capture_screen("menu_initial")
        if screen:
            screenshots.append(screen)
            time.sleep(1)

        # Naviguer vers le bas 3 fois
        for i in range(3):
            print(f"{Colors.CYAN}{i+2}. Flèche BAS (navigation){Colors.RESET}")
            pyautogui.press('down')
            time.sleep(0.5)
            screen = self.capture_screen(f"menu_nav_{i+1}")
            if screen:
                screenshots.append(screen)

        return screenshots

    def stop_game(self):
        """Arrête le jeu"""
        print(f"\n{Colors.YELLOW}⏹ Arrêt du jeu...{Colors.RESET}")

        if self.process:
            try:
                # Essayer de fermer proprement
                process = psutil.Process(self.process.pid)
                process.terminate()
                process.wait(timeout=5)
                print(f"{Colors.GREEN}✓ Jeu arrêté proprement{Colors.RESET}")
            except:
                try:
                    # Forcer l'arrêt si nécessaire
                    process.kill()
                    print(f"{Colors.YELLOW}✓ Jeu arrêté (forcé){Colors.RESET}")
                except:
                    pass

    def check_log_errors(self):
        """Vérifie les erreurs dans le log"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}📋 ANALYSE DU LOG{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")

        log_file = self.game_dir / "mugen.log"

        if not log_file.exists():
            print(f"{Colors.RED}✗ Fichier log introuvable{Colors.RESET}")
            return

        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        errors = []
        warnings = []

        for line in lines:
            line_lower = line.lower()
            if 'error' in line_lower or 'failed' in line_lower:
                errors.append(line.strip())
            elif 'warning' in line_lower:
                warnings.append(line.strip())

        print(f"  Total de lignes: {len(lines)}")
        print(f"  Erreurs: {len(errors)}")
        print(f"  Avertissements: {len(warnings)}")

        if errors:
            print(f"\n{Colors.RED}Premières erreurs:{Colors.RESET}")
            for error in errors[:5]:
                print(f"  - {error}")

        if not errors:
            print(f"\n{Colors.GREEN}✓ Aucune erreur critique détectée{Colors.RESET}")

    def run_visual_test(self):
        """Lance le test visuel complet"""
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'KOF ULTIMATE - TEST VISUEL AUTOMATIQUE':^80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

        try:
            # 1. Lancer le jeu
            if not self.launch_game():
                print(f"\n{Colors.RED}✗ Échec du lancement{Colors.RESET}")
                return False

            # 2. Attendre le chargement
            self.wait_for_loading()

            # 3. Capturer le menu initial
            print(f"\n{Colors.CYAN}📸 Capture du menu principal{Colors.RESET}")
            screenshot = self.capture_screen("menu_principal")

            # 4. Analyser le screenshot
            if screenshot:
                self.analyze_menu_screen(screenshot)

            # 5. Tester la navigation
            self.test_menu_navigation()

            # 6. Attendre un peu pour observer
            print(f"\n{Colors.CYAN}⏳ Observation du jeu pendant 5 secondes...{Colors.RESET}")
            time.sleep(5)

            # 7. Arrêter le jeu
            self.stop_game()

            # 8. Analyser le log
            time.sleep(2)
            self.check_log_errors()

            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ TEST VISUEL TERMINÉ{Colors.RESET}")
            print(f"\n{Colors.CYAN}📁 Screenshots sauvegardés dans: {self.screenshots_dir}{Colors.RESET}")

            return True

        except Exception as e:
            print(f"\n{Colors.RED}✗ Erreur pendant le test: {e}{Colors.RESET}")
            import traceback
            traceback.print_exc()
            self.stop_game()
            return False

def main():
    game_dir = r"D:\KOF Ultimate Online"

    print(f"\n{Colors.WHITE}Installation des dépendances si nécessaire...{Colors.RESET}")

    # Vérifier et installer les dépendances
    try:
        import pyautogui
        import PIL
        import win32gui
        import psutil
    except ImportError as e:
        print(f"{Colors.YELLOW}Installation de: {str(e).split()[-1]}{Colors.RESET}")
        module = str(e).split()[-1].replace("'", "")

        if module == "pyautogui":
            os.system("python -m pip install pyautogui")
        elif module == "PIL":
            os.system("python -m pip install Pillow")
        elif module == "win32gui":
            os.system("python -m pip install pywin32")
        elif module == "psutil":
            os.system("python -m pip install psutil")

        print(f"{Colors.YELLOW}Veuillez relancer le script{Colors.RESET}")
        return

    tester = VisualTester(game_dir)
    tester.run_visual_test()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interruption par l'utilisateur{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Erreur: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
