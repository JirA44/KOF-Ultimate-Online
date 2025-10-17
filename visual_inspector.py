#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - Visual Inspector
Interface graphique pour vérifier animations, menus et sélection de personnages
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import time
from pathlib import Path
from datetime import datetime
import pyautogui
from PIL import Image, ImageTk
import win32gui
import win32con
import psutil
import threading

class VisualInspector:
    """Inspecteur visuel avec interface graphique"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KOF Ultimate - Visual Inspector")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0e27')

        self.game_dir = Path(r"D:\KOF Ultimate")
        self.exe_path = self.game_dir / "KOF BLACK R.exe"
        self.process = None
        self.window_handle = None
        self.screenshots_dir = self.game_dir / "test_screenshots"
        self.screenshots_dir.mkdir(exist_ok=True)

        self.is_running = False
        self.current_screenshot = None

        self.setup_ui()

    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Header
        header = tk.Frame(self.root, bg='#1a1f3a', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="🔍 VISUAL INSPECTOR",
            font=('Consolas', 24, 'bold'),
            fg='#FFD700',
            bg='#1a1f3a'
        )
        title.pack(pady=20)

        # Container principal
        main_container = tk.Frame(self.root, bg='#0a0e27')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Panneau gauche - Contrôles
        left_panel = tk.Frame(main_container, bg='#1b263b', width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)

        # Contrôles du jeu
        control_frame = tk.LabelFrame(
            left_panel,
            text=" 🎮 Contrôle du Jeu ",
            font=('Consolas', 11, 'bold'),
            bg='#1b263b',
            fg='#00d9ff',
            padx=10,
            pady=10
        )
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        self.launch_btn = tk.Button(
            control_frame,
            text="▶ Lancer le Jeu",
            font=('Consolas', 12, 'bold'),
            bg='#00cc44',
            fg='#000000',
            cursor='hand2',
            command=self.launch_game,
            pady=8
        )
        self.launch_btn.pack(fill=tk.X, pady=5)

        self.stop_btn = tk.Button(
            control_frame,
            text="⏹ Arrêter le Jeu",
            font=('Consolas', 12, 'bold'),
            bg='#cc0000',
            fg='#ffffff',
            cursor='hand2',
            command=self.stop_game,
            state=tk.DISABLED,
            pady=8
        )
        self.stop_btn.pack(fill=tk.X, pady=5)

        # Tests automatiques
        test_frame = tk.LabelFrame(
            left_panel,
            text=" 🧪 Tests Automatiques ",
            font=('Consolas', 11, 'bold'),
            bg='#1b263b',
            fg='#00d9ff',
            padx=10,
            pady=10
        )
        test_frame.pack(fill=tk.X, padx=10, pady=10)

        tests = [
            ("📸 Capture Menu Principal", self.test_main_menu),
            ("🎯 Test Navigation Menu", self.test_menu_navigation),
            ("👤 Test Sélection Persos", self.test_char_selection),
            ("🎬 Test Animations Menu", self.test_menu_animations),
            ("🏆 Test Écran Victoire", self.test_victory_screen),
        ]

        for text, command in tests:
            btn = tk.Button(
                test_frame,
                text=text,
                font=('Consolas', 9),
                bg='#2d3561',
                fg='#c0c0c0',
                cursor='hand2',
                command=command,
                pady=5
            )
            btn.pack(fill=tk.X, pady=2)

        # Actions manuelles
        action_frame = tk.LabelFrame(
            left_panel,
            text=" 🎯 Actions Manuelles ",
            font=('Consolas', 11, 'bold'),
            bg='#1b263b',
            fg='#00d9ff',
            padx=10,
            pady=10
        )
        action_frame.pack(fill=tk.X, padx=10, pady=10)

        actions = [
            ("⬆ Haut", lambda: self.send_key('up')),
            ("⬇ Bas", lambda: self.send_key('down')),
            ("⬅ Gauche", lambda: self.send_key('left')),
            ("➡ Droite", lambda: self.send_key('right')),
            ("✓ Entrée", lambda: self.send_key('enter')),
            ("✗ Échap", lambda: self.send_key('escape')),
        ]

        for text, command in actions:
            btn = tk.Button(
                action_frame,
                text=text,
                font=('Consolas', 9),
                bg='#2d3561',
                fg='#c0c0c0',
                cursor='hand2',
                command=command,
                pady=3
            )
            btn.pack(fill=tk.X, pady=2)

        # Panneau droit - Affichage
        right_panel = tk.Frame(main_container, bg='#0d1b2a')
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Zone d'aperçu
        preview_frame = tk.LabelFrame(
            right_panel,
            text=" 📺 Aperçu en Direct ",
            font=('Consolas', 11, 'bold'),
            bg='#0d1b2a',
            fg='#00d9ff',
            padx=10,
            pady=10
        )
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Canvas pour afficher les screenshots
        self.canvas = tk.Canvas(
            preview_frame,
            bg='#000000',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Zone de log
        log_frame = tk.LabelFrame(
            right_panel,
            text=" 📋 Journal ",
            font=('Consolas', 11, 'bold'),
            bg='#0d1b2a',
            fg='#00d9ff',
            padx=10,
            pady=10,
            height=200
        )
        log_frame.pack(fill=tk.X)
        log_frame.pack_propagate(False)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=('Consolas', 9),
            bg='#1a1f3a',
            fg='#00ff88',
            height=10,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="⚡ Prêt",
            font=('Consolas', 10, 'bold'),
            bg='#1a1f3a',
            fg='#00ff88',
            anchor=tk.W,
            padx=15,
            pady=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def log(self, message, level='info'):
        """Ajoute un message au log"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        colors = {
            'info': '#00ff88',
            'warning': '#ffaa00',
            'error': '#ff0000',
            'success': '#00ff00'
        }

        color = colors.get(level, '#ffffff')

        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()

    def update_status(self, message):
        """Met à jour la barre de statut"""
        self.status_bar.config(text=message)
        self.root.update()

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
        self.log("🎮 Lancement du jeu...")
        self.update_status("Lancement du jeu...")

        try:
            self.process = subprocess.Popen(
                [str(self.exe_path)],
                cwd=str(self.game_dir)
            )

            self.log(f"✓ Jeu lancé (PID: {self.process.pid})", 'success')

            # Attendre la fenêtre
            self.log("Recherche de la fenêtre du jeu...")
            for i in range(30):
                time.sleep(0.5)
                if self.find_game_window():
                    self.log("✓ Fenêtre trouvée!", 'success')

                    try:
                        win32gui.ShowWindow(self.window_handle, win32con.SW_RESTORE)
                        win32gui.SetForegroundWindow(self.window_handle)
                    except:
                        pass

                    self.is_running = True
                    self.launch_btn.config(state=tk.DISABLED)
                    self.stop_btn.config(state=tk.NORMAL)
                    self.update_status("✓ Jeu en cours")

                    # Démarrer la capture automatique
                    threading.Thread(target=self.auto_capture_loop, daemon=True).start()
                    return True

            self.log("✗ Fenêtre non trouvée", 'error')
            return False

        except Exception as e:
            self.log(f"✗ Erreur: {e}", 'error')
            return False

    def stop_game(self):
        """Arrête le jeu"""
        self.log("⏹ Arrêt du jeu...")
        self.update_status("Arrêt du jeu...")

        if self.process:
            try:
                process = psutil.Process(self.process.pid)
                process.terminate()
                process.wait(timeout=5)
                self.log("✓ Jeu arrêté", 'success')
            except:
                try:
                    process.kill()
                    self.log("✓ Jeu arrêté (forcé)", 'warning')
                except:
                    pass

        self.is_running = False
        self.launch_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.update_status("⚡ Prêt")

    def send_key(self, key):
        """Envoie une touche au jeu"""
        if not self.is_running:
            self.log("⚠ Le jeu n'est pas lancé", 'warning')
            return

        try:
            if self.window_handle:
                win32gui.SetForegroundWindow(self.window_handle)

            time.sleep(0.1)
            pyautogui.press(key)
            self.log(f"→ Touche envoyée: {key}")

            # Capture après l'action
            time.sleep(0.3)
            self.capture_screen(f"key_{key}")
        except Exception as e:
            self.log(f"✗ Erreur envoi touche: {e}", 'error')

    def capture_screen(self, name):
        """Capture l'écran du jeu"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = self.screenshots_dir / filename

        try:
            if self.window_handle:
                try:
                    rect = win32gui.GetWindowRect(self.window_handle)
                    x, y, x2, y2 = rect
                    width = x2 - x
                    height = y2 - y

                    screenshot = pyautogui.screenshot(region=(x, y, width, height))
                    screenshot.save(str(filepath))

                    # Afficher dans l'interface
                    self.display_screenshot(screenshot)

                    self.log(f"📸 Screenshot: {filename}")
                    return filepath
                except Exception as e:
                    self.log(f"⚠ Erreur capture: {e}", 'warning')

            screenshot = pyautogui.screenshot()
            screenshot.save(str(filepath))
            self.display_screenshot(screenshot)
            return filepath

        except Exception as e:
            self.log(f"✗ Erreur capture: {e}", 'error')
            return None

    def display_screenshot(self, img):
        """Affiche un screenshot dans le canvas"""
        try:
            # Redimensionner l'image pour s'adapter au canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            if canvas_width > 1 and canvas_height > 1:
                img_width, img_height = img.size
                ratio = min(canvas_width / img_width, canvas_height / img_height)
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)

                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img_resized)

                self.canvas.delete("all")
                self.canvas.create_image(
                    canvas_width // 2,
                    canvas_height // 2,
                    image=photo,
                    anchor=tk.CENTER
                )

                # Garder une référence pour éviter le garbage collection
                self.current_screenshot = photo
        except Exception as e:
            print(f"Display error: {e}")

    def auto_capture_loop(self):
        """Boucle de capture automatique"""
        while self.is_running:
            time.sleep(2)
            if self.is_running:
                self.capture_screen("auto")

    def test_main_menu(self):
        """Teste le menu principal"""
        self.log("🧪 Test: Menu Principal", 'info')

        if not self.is_running:
            self.log("⚠ Lancez le jeu d'abord!", 'warning')
            return

        time.sleep(1)
        self.capture_screen("menu_principal")
        self.log("✓ Test menu principal terminé", 'success')

    def test_menu_navigation(self):
        """Teste la navigation dans les menus"""
        self.log("🧪 Test: Navigation Menu", 'info')

        if not self.is_running:
            self.log("⚠ Lancez le jeu d'abord!", 'warning')
            return

        self.log("Navigation dans le menu...")
        for i in range(4):
            self.log(f"→ Navigation {i+1}/4")
            self.send_key('down')
            time.sleep(0.5)

        self.log("✓ Test navigation terminé", 'success')

    def test_char_selection(self):
        """Teste l'écran de sélection de personnages"""
        self.log("🧪 Test: Sélection Personnages", 'info')

        if not self.is_running:
            self.log("⚠ Lancez le jeu d'abord!", 'warning')
            return

        self.log("Accès à la sélection des personnages...")

        # Aller au mode arcade
        for _ in range(3):
            self.send_key('down')
            time.sleep(0.3)

        self.send_key('enter')
        time.sleep(2)

        # Naviguer dans la grille de personnages
        self.log("Navigation dans la grille...")
        for i in range(5):
            self.send_key('right')
            time.sleep(0.5)
            self.capture_screen(f"char_select_{i}")

        self.log("✓ Test sélection personnages terminé", 'success')

    def test_menu_animations(self):
        """Teste les animations du menu"""
        self.log("🧪 Test: Animations Menu", 'info')

        if not self.is_running:
            self.log("⚠ Lancez le jeu d'abord!", 'warning')
            return

        self.log("Capture des animations...")
        for i in range(10):
            self.capture_screen(f"anim_{i}")
            time.sleep(0.5)

        self.log("✓ Test animations terminé", 'success')

    def test_victory_screen(self):
        """Teste l'écran de victoire"""
        self.log("🧪 Test: Écran Victoire", 'info')
        self.log("⚠ Ce test nécessite de terminer un combat", 'warning')

    def run(self):
        """Lance l'inspecteur"""
        self.root.mainloop()

def main():
    """Point d'entrée principal"""
    inspector = VisualInspector()
    inspector.run()

if __name__ == '__main__':
    main()
