#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST AVEC SCREENSHOTS AUTOMATIQUES
Capture l'écran du jeu à chaque étape pour analyse visuelle
"""

import subprocess
import time
import random
import os
from datetime import datetime
from pathlib import Path
import json

try:
    import win32gui
    import win32con
    import win32api
    import win32ui
    from PIL import Image
except ImportError:
    print("Installation des dépendances...")
    os.system("pip install pywin32 pillow")
    import win32gui
    import win32con
    import win32api
    import win32ui
    from PIL import Image

GAME_EXE = "KOF_Ultimate_Online.exe"
GAME_PATH = Path(__file__).parent
SCREENSHOTS_DIR = GAME_PATH / "logs" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

VK_CODES = {
    'space': win32con.VK_SPACE,
    'return': win32con.VK_RETURN,
    'escape': win32con.VK_ESCAPE,
    'up': win32con.VK_UP,
    'down': win32con.VK_DOWN,
    'left': win32con.VK_LEFT,
    'right': win32con.VK_RIGHT,
    'a': ord('A'),
    's': ord('S'),
    'z': ord('Z'),
    'x': ord('X'),
}

class VisualTester:
    """Testeur avec captures d'écran"""

    def __init__(self):
        self.issues = []
        self.start_time = datetime.now()
        self.game_hwnd = None
        self.game_process = None
        self.test_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.screenshots = []

        # Dossier pour cette session
        self.session_dir = SCREENSHOTS_DIR / f"test_{self.test_id}"
        self.session_dir.mkdir(exist_ok=True)

    def log(self, msg):
        timestamp = (datetime.now() - self.start_time).total_seconds()
        print(f"[{timestamp:>6.1f}s] {msg}")

    def issue(self, problem):
        self.issues.append(problem)
        self.log(f"⚠️  PROBLÈME: {problem}")

    def find_game_window(self):
        """Trouve la fenêtre du jeu"""
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if any(keyword in title for keyword in ["KOF", "Ikemen", "MUGEN", "AI Navigator"]):
                    windows.append(hwnd)
            return True

        windows = []
        win32gui.EnumWindows(callback, windows)
        return windows[0] if windows else None

    def capture_window(self, step_name):
        """Capture la fenêtre du jeu"""
        if not self.game_hwnd:
            self.log("Pas de fenêtre pour screenshot")
            return None

        try:
            # Obtenir les dimensions de la fenêtre
            left, top, right, bottom = win32gui.GetWindowRect(self.game_hwnd)
            width = right - left
            height = bottom - top

            # Capturer
            hwndDC = win32gui.GetWindowDC(self.game_hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
            saveDC.SelectObject(saveBitMap)

            # BitBlt
            saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

            # Sauvegarder
            timestamp = (datetime.now() - self.start_time).total_seconds()
            filename = f"{int(timestamp):04d}_{step_name}.png"
            filepath = self.session_dir / filename

            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)

            img = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1
            )

            img.save(filepath)

            # Cleanup
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(self.game_hwnd, hwndDC)

            self.screenshots.append({
                'step': step_name,
                'time': timestamp,
                'file': filename,
                'path': str(filepath)
            })

            self.log(f"📸 Screenshot: {filename}")
            return filepath

        except Exception as e:
            self.log(f"Erreur screenshot: {e}")
            return None

    def send_key(self, key, hold_time=0.05):
        """Envoie une touche au jeu"""
        if not self.game_hwnd or key not in VK_CODES:
            return False

        try:
            vk_code = VK_CODES[key]
            lparam_down = win32api.MapVirtualKey(vk_code, 0) << 16 | 1
            win32api.SendMessage(self.game_hwnd, win32con.WM_KEYDOWN, vk_code, lparam_down)
            time.sleep(hold_time)
            lparam_up = lparam_down | (0x3 << 30)
            win32api.SendMessage(self.game_hwnd, win32con.WM_KEYUP, vk_code, lparam_up)
            return True
        except:
            return False

    def check_game_alive(self):
        """Vérifie que le jeu tourne toujours"""
        if not self.game_process:
            return False

        poll = self.game_process.poll()
        if poll is not None:
            self.issue(f"Le jeu s'est fermé (exit code: {poll})")
            return False

        return True

    def test_launch(self):
        """Lance le jeu avec screenshot"""
        self.log("="*60)
        self.log("TEST 1: LANCEMENT")
        self.log("="*60)

        game_path = GAME_PATH / GAME_EXE
        if not game_path.exists():
            self.issue(f"Jeu introuvable: {GAME_EXE}")
            return False

        self.log(f"✓ Exe trouvé: {game_path}")

        try:
            self.game_process = subprocess.Popen(
                str(game_path),
                cwd=str(GAME_PATH)
            )
            self.log(f"Jeu lancé (PID: {self.game_process.pid})")
        except Exception as e:
            self.issue(f"Échec lancement: {e}")
            return False

        # Attendre fenêtre
        for i in range(30):
            time.sleep(1)
            self.game_hwnd = self.find_game_window()
            if self.game_hwnd:
                time.sleep(3)
                self.capture_window("01_lancement")
                return True

        self.issue("Fenêtre jamais apparue")
        return False

    def test_title_screen(self):
        """Test écran titre"""
        self.log("\n" + "="*60)
        self.log("TEST 2: ÉCRAN TITRE")
        self.log("="*60)

        self.log("Attente écran titre...")
        time.sleep(5)

        if not self.check_game_alive():
            return

        self.capture_window("02_ecran_titre")

        self.log("Appui ESPACE...")
        self.send_key('space')
        time.sleep(3)

        if not self.check_game_alive():
            return

        self.capture_window("03_menu_principal")

    def test_menu_navigation(self):
        """Test navigation"""
        self.log("\n" + "="*60)
        self.log("TEST 3: NAVIGATION MENUS")
        self.log("="*60)

        for i in range(3):
            self.send_key('down')
            time.sleep(1)

        if not self.check_game_alive():
            return

        self.capture_window("04_navigation_menu")

        for _ in range(3):
            self.send_key('up')
            time.sleep(0.3)

    def test_versus_mode(self):
        """Test VS mode"""
        self.log("\n" + "="*60)
        self.log("TEST 4: MODE VERSUS")
        self.log("="*60)

        self.send_key('down')
        time.sleep(0.5)
        self.send_key('return')
        time.sleep(4)

        if not self.check_game_alive():
            return

        self.capture_window("05_selection_persos")

    def test_character_selection(self):
        """Test sélection"""
        self.log("\n" + "="*60)
        self.log("TEST 5: SÉLECTION PERSONNAGE")
        self.log("="*60)

        for direction in ['right', 'down']:
            self.send_key(direction)
            time.sleep(0.5)

        if not self.check_game_alive():
            return

        self.capture_window("06_perso_choisi")

        self.log("Sélection...")
        self.send_key('return')
        time.sleep(6)

        if not self.check_game_alive():
            return

        self.capture_window("07_ecran_vs")

    def test_gameplay(self, duration=15):
        """Test gameplay avec screenshots réguliers"""
        self.log("\n" + "="*60)
        self.log(f"TEST 6: GAMEPLAY ({duration}s)")
        self.log("="*60)

        if not self.check_game_alive():
            self.issue("Le jeu est mort AVANT le combat")
            return

        # Screenshot au début du combat
        time.sleep(2)
        if not self.check_game_alive():
            self.issue("Le jeu a crash au chargement du match")
            return

        self.capture_window("08_debut_combat")

        # Gameplay
        keys = ['a', 's', 'z', 'x', 'left', 'right']
        start = time.time()
        screenshot_count = 0

        while time.time() - start < duration:
            # Vérifier que le jeu vit
            if not self.check_game_alive():
                self.issue(f"Le jeu a crash pendant le combat (après {time.time() - start:.1f}s)")
                return

            # Screenshot toutes les 5 secondes
            elapsed = time.time() - start
            if int(elapsed) % 5 == 0 and int(elapsed) != screenshot_count * 5:
                screenshot_count += 1
                self.capture_window(f"09_combat_{int(elapsed)}s")

            # Jouer
            self.send_key(random.choice(keys))
            time.sleep(0.5)

        if self.check_game_alive():
            self.capture_window("10_fin_combat")
            self.log("✓ Combat terminé sans crash!")
        else:
            self.issue("Le jeu a crash à la fin du combat")

    def test_exit(self):
        """Test sortie"""
        self.log("\n" + "="*60)
        self.log("TEST 7: SORTIE")
        self.log("="*60)

        if not self.check_game_alive():
            return

        self.send_key('escape')
        time.sleep(2)

        if self.check_game_alive():
            self.capture_window("11_menu_pause")

    def close_game(self):
        """Ferme le jeu"""
        if self.game_process:
            try:
                self.game_process.terminate()
                self.game_process.wait(timeout=5)
                self.log("Jeu fermé proprement")
            except:
                try:
                    self.game_process.kill()
                    self.log("Jeu tué")
                except:
                    pass

    def generate_html_report(self):
        """Génère un rapport HTML avec toutes les screenshots"""
        html_file = self.session_dir / "rapport.html"

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport Test Visuel - {self.test_id}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: #1a1a1a;
            color: #e0e0e0;
        }}
        h1 {{
            color: #4CAF50;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .info {{
            background: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #2196F3;
        }}
        .problems {{
            background: #3a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #f44336;
        }}
        .screenshot {{
            margin: 30px 0;
            background: #2a2a2a;
            padding: 20px;
            border-radius: 8px;
        }}
        .screenshot img {{
            max-width: 100%;
            border: 2px solid #444;
            border-radius: 4px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }}
        .screenshot h3 {{
            color: #4CAF50;
            margin-top: 0;
        }}
        .time {{
            color: #888;
            font-size: 0.9em;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .grid img {{
            width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
    <h1>🎮 Rapport Test Visuel - KOF Ultimate Online</h1>

    <div class="info">
        <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Durée:</strong> {(datetime.now() - self.start_time).total_seconds():.1f}s</p>
        <p><strong>Screenshots:</strong> {len(self.screenshots)}</p>
        <p><strong>Problèmes détectés:</strong> {len(self.issues)}</p>
    </div>
"""

        if self.issues:
            html += """
    <div class="problems">
        <h2>❌ Problèmes Détectés</h2>
        <ul>
"""
            for issue in self.issues:
                html += f"            <li>{issue}</li>\n"
            html += """
        </ul>
    </div>
"""

        html += """
    <h2>📸 Captures d'Écran Chronologiques</h2>
"""

        for shot in self.screenshots:
            html += f"""
    <div class="screenshot">
        <h3>{shot['step'].replace('_', ' ').title()}</h3>
        <p class="time">⏱️ {shot['time']:.1f}s</p>
        <img src="{shot['file']}" alt="{shot['step']}">
    </div>
"""

        html += """
    <h2>🔍 Vue Grille (Toutes les Captures)</h2>
    <div class="grid">
"""

        for shot in self.screenshots:
            html += f"""
        <div>
            <p style="text-align:center; margin:0; padding:5px; background:#333;">
                {shot['step']} ({shot['time']:.1f}s)
            </p>
            <img src="{shot['file']}" alt="{shot['step']}">
        </div>
"""

        html += """
    </div>
</body>
</html>
"""

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)

        self.log(f"📄 Rapport HTML: {html_file}")
        return html_file

    def run(self):
        """Lance le test complet"""
        print("\n" + "="*70)
        print("  🎮 TEST AVEC SCREENSHOTS AUTOMATIQUES")
        print("  Captures visuelles à chaque étape")
        print("="*70 + "\n")

        print(f"📁 Screenshots: {self.session_dir}\n")

        try:
            if not self.test_launch():
                return

            self.test_title_screen()
            self.test_menu_navigation()
            self.test_versus_mode()
            self.test_character_selection()
            self.test_gameplay(duration=15)
            self.test_exit()

        except Exception as e:
            self.issue(f"Erreur critique: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.close_game()
            time.sleep(2)

            # Rapport
            print("\n" + "="*70)
            print("RAPPORT FINAL")
            print("="*70)
            print(f"\n📸 Screenshots: {len(self.screenshots)}")
            print(f"⚠️  Problèmes: {len(self.issues)}")

            if self.issues:
                print("\n❌ PROBLÈMES DÉTECTÉS:")
                for i, issue in enumerate(self.issues, 1):
                    print(f"   {i}. {issue}")

            # Générer rapport HTML
            html_report = self.generate_html_report()

            print(f"\n✅ Rapport HTML généré!")
            print(f"   📄 {html_report}")
            print(f"\nOuvrez ce fichier dans votre navigateur pour voir tous les screenshots.")

if __name__ == "__main__":
    tester = VisualTester()
    tester.run()

    print("\n" + "="*70)
    time.sleep(2)
