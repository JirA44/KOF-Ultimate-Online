"""
KOF Ultimate - Agent IA Navigateur
Version 1.0.0

Cet agent navigue automatiquement sur le launcher en parallèle
pour détecter et signaler tous les problèmes.
"""

import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import pyautogui
import anthropic
from PIL import Image, ImageDraw, ImageFont
import threading

# Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("⚠️  ANTHROPIC_API_KEY not found in environment variables")
    print("Please set it with: set ANTHROPIC_API_KEY=your_key_here")
    print("Continuing with limited functionality (basic checks only)...")

GAME_PATH = Path("D:/KOF Ultimate")
LOG_FILE = GAME_PATH / "launcher_ai_log.json"

class LauncherAINavigator:
    """Agent IA qui navigue sur le launcher et détecte les problèmes"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None
        self.problems_detected = []
        self.navigation_log = []
        self.running = True

        # Interface de monitoring
        self.root = tk.Tk()
        self.root.title("🤖 KOF Ultimate - AI Navigator")
        self.root.geometry("500x700")
        self.root.configure(bg='#1a1f3a')

        self.setup_ui()

    def setup_ui(self):
        """Configure l'interface de l'agent"""
        # Header
        header = tk.Frame(self.root, bg='#0d1b2a', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="🤖  AI NAVIGATOR",
            font=('Consolas', 20, 'bold'),
            fg='#00ff88',
            bg='#0d1b2a'
        )
        title.pack(pady=20)

        # Status
        self.status_frame = tk.Frame(self.root, bg='#1a1f3a', padx=20, pady=10)
        self.status_frame.pack(fill=tk.X)

        self.status_label = tk.Label(
            self.status_frame,
            text="⚡ Status: Initializing...",
            font=('Consolas', 11, 'bold'),
            fg='#ffff00',
            bg='#1a1f3a',
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X)

        # Statistiques
        stats_frame = tk.LabelFrame(
            self.root,
            text=" 📊  STATISTICS ",
            font=('Consolas', 10, 'bold'),
            fg='#00d9ff',
            bg='#1b263b',
            padx=15,
            pady=10
        )
        stats_frame.pack(fill=tk.X, padx=20, pady=10)

        self.stats_text = tk.Text(
            stats_frame,
            height=5,
            font=('Consolas', 9),
            bg='#0d1b2a',
            fg='#c0c0c0',
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        self.stats_text.pack(fill=tk.BOTH)
        self.update_stats()

        # Log de navigation
        log_frame = tk.LabelFrame(
            self.root,
            text=" 🗺️  NAVIGATION LOG ",
            font=('Consolas', 10, 'bold'),
            fg='#00d9ff',
            bg='#1b263b',
            padx=15,
            pady=10
        )
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Scrollbar pour le log
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_text = tk.Text(
            log_frame,
            font=('Consolas', 9),
            bg='#0d1b2a',
            fg='#00ff88',
            relief=tk.FLAT,
            yscrollcommand=scrollbar.set,
            padx=10,
            pady=5
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)

        # Problèmes détectés
        problems_frame = tk.LabelFrame(
            self.root,
            text=" ⚠️  PROBLEMS DETECTED ",
            font=('Consolas', 10, 'bold'),
            fg='#ff4444',
            bg='#1b263b',
            padx=15,
            pady=10
        )
        problems_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        problems_scrollbar = tk.Scrollbar(problems_frame)
        problems_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.problems_text = tk.Text(
            problems_frame,
            font=('Consolas', 9),
            bg='#0d1b2a',
            fg='#ff6666',
            relief=tk.FLAT,
            yscrollcommand=problems_scrollbar.set,
            padx=10,
            pady=5
        )
        self.problems_text.pack(fill=tk.BOTH, expand=True)
        problems_scrollbar.config(command=self.problems_text.yview)

        # Boutons de contrôle
        controls = tk.Frame(self.root, bg='#1a1f3a', padx=20, pady=10)
        controls.pack(fill=tk.X)

        self.start_btn = tk.Button(
            controls,
            text="▶ START MONITORING",
            font=('Consolas', 11, 'bold'),
            bg='#00cc44',
            fg='#000000',
            command=self.start_monitoring,
            padx=20,
            pady=8,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2'
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(
            controls,
            text="⏹ STOP",
            font=('Consolas', 11, 'bold'),
            bg='#cc0000',
            fg='#ffffff',
            command=self.stop_monitoring,
            padx=20,
            pady=8,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2',
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        save_btn = tk.Button(
            controls,
            text="💾 SAVE LOG",
            font=('Consolas', 10, 'bold'),
            bg='#0066cc',
            fg='#ffffff',
            command=self.save_log,
            padx=15,
            pady=8,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2'
        )
        save_btn.pack(side=tk.RIGHT, padx=5)

    def log_message(self, message, level="INFO"):
        """Ajoute un message au log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": "#00ff88",
            "WARNING": "#ffaa00",
            "ERROR": "#ff4444",
            "SUCCESS": "#00ff00"
        }

        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }
        self.navigation_log.append(log_entry)

        # Afficher dans l'interface
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.log_text.insert(tk.END, f"{level}: ", level)
        self.log_text.insert(tk.END, f"{message}\n", "message")

        # Configuration des tags
        self.log_text.tag_config("timestamp", foreground="#888888")
        self.log_text.tag_config(level, foreground=colors.get(level, "#ffffff"))
        self.log_text.tag_config("message", foreground="#c0c0c0")

        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def add_problem(self, problem_description, severity="MEDIUM"):
        """Ajoute un problème détecté"""
        problem = {
            "timestamp": datetime.now().isoformat(),
            "severity": severity,
            "description": problem_description
        }
        self.problems_detected.append(problem)

        # Afficher dans l'interface
        self.problems_text.config(state=tk.NORMAL)
        severity_emoji = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟡"}
        self.problems_text.insert(
            tk.END,
            f"{severity_emoji.get(severity, '⚪')} [{severity}] {problem_description}\n\n"
        )
        self.problems_text.see(tk.END)
        self.problems_text.config(state=tk.DISABLED)

        self.update_stats()

    def update_stats(self):
        """Met à jour les statistiques"""
        stats = f"""
Actions effectuées:  {len(self.navigation_log)}
Problèmes détectés:  {len(self.problems_detected)}
Temps d'exécution:   {self.get_runtime()}
Statut IA:          {'✓ Connected' if self.client else '✗ Not connected'}
        """

        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats)
        self.stats_text.config(state=tk.DISABLED)

    def get_runtime(self):
        """Calcule le temps d'exécution"""
        if not hasattr(self, 'start_time'):
            return "00:00:00"

        elapsed = int(time.time() - self.start_time)
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def capture_screen(self):
        """Capture l'écran actuel"""
        try:
            screenshot = pyautogui.screenshot()
            return screenshot
        except Exception as e:
            self.log_message(f"Failed to capture screen: {e}", "ERROR")
            return None

    def analyze_with_claude(self, screenshot):
        """Analyse le screenshot avec Claude"""
        if not self.client:
            return "Claude API not available"

        try:
            # Sauvegarder temporairement l'image
            temp_path = GAME_PATH / "temp_screenshot.png"
            screenshot.save(temp_path)

            # Lire l'image en base64
            import base64
            with open(temp_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode()

            # Analyser avec Claude
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_data
                            }
                        },
                        {
                            "type": "text",
                            "text": """Analyse cette capture d'écran du launcher KOF Ultimate.

Identifie :
1. Tous les boutons visibles et leurs états
2. Les problèmes potentiels (messages d'erreur, éléments manquants, etc.)
3. L'état actuel de l'interface
4. Les actions recommandées

Réponds en français de manière concise."""
                        }
                    ]
                }]
            )

            # Nettoyer
            temp_path.unlink()

            return message.content[0].text

        except Exception as e:
            self.log_message(f"Claude analysis failed: {e}", "ERROR")
            return f"Analysis error: {e}"

    def check_launcher_window(self):
        """Vérifie si la fenêtre du launcher est ouverte"""
        try:
            windows = pyautogui.getWindowsWithTitle("KOF Ultimate Launcher")
            return len(windows) > 0
        except:
            return False

    def start_monitoring(self):
        """Démarre le monitoring"""
        self.start_time = time.time()
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="⚡ Status: Monitoring active...", fg="#00ff00")

        # Démarrer dans un thread séparé
        thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        thread.start()

    def stop_monitoring(self):
        """Arrête le monitoring"""
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="⚡ Status: Stopped", fg="#ffaa00")
        self.log_message("Monitoring stopped by user", "INFO")

    def monitoring_loop(self):
        """Boucle principale de monitoring"""
        self.log_message("Starting AI navigation monitoring", "SUCCESS")

        iteration = 0
        while self.running:
            iteration += 1
            self.log_message(f"--- Iteration {iteration} ---", "INFO")

            # Vérifier si le launcher est ouvert
            if not self.check_launcher_window():
                self.log_message("Launcher window not found", "WARNING")
                self.add_problem("Launcher window is not open", "LOW")
                time.sleep(5)
                continue

            # Capturer l'écran
            self.log_message("Capturing screen...", "INFO")
            screenshot = self.capture_screen()

            if screenshot:
                # Analyser avec Claude (si disponible)
                if self.client:
                    self.log_message("Analyzing with Claude AI...", "INFO")
                    analysis = self.analyze_with_claude(screenshot)
                    self.log_message(f"Analysis result: {analysis[:100]}...", "SUCCESS")

                    # Détecter les problèmes dans l'analyse
                    if "erreur" in analysis.lower() or "error" in analysis.lower():
                        self.add_problem(f"Detected error in UI: {analysis[:200]}", "HIGH")
                    elif "warning" in analysis.lower() or "attention" in analysis.lower():
                        self.add_problem(f"Warning detected: {analysis[:200]}", "MEDIUM")
                else:
                    self.log_message("Claude API not available, basic checks only", "WARNING")

                # Vérifications basiques
                self.perform_basic_checks()

            # Mettre à jour les stats
            self.root.after(0, self.update_stats)

            # Attendre avant la prochaine itération
            time.sleep(10)

        self.log_message("Monitoring loop ended", "INFO")

    def perform_basic_checks(self):
        """Effectue des vérifications basiques sans IA"""
        # Vérifier les fichiers essentiels
        essential_files = [
            GAME_PATH / "KOF BLACK R.exe",
            GAME_PATH / "data" / "mugen.cfg",
            GAME_PATH / "launcher.py"
        ]

        for file_path in essential_files:
            if not file_path.exists():
                self.add_problem(f"Missing essential file: {file_path.name}", "HIGH")
                self.log_message(f"Missing file: {file_path}", "ERROR")

    def save_log(self):
        """Sauvegarde le log complet"""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "runtime": self.get_runtime(),
            "navigation_log": self.navigation_log,
            "problems_detected": self.problems_detected
        }

        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)

        self.log_message(f"Log saved to {LOG_FILE}", "SUCCESS")

    def run(self):
        """Lance l'interface"""
        self.log_message("AI Navigator initialized", "SUCCESS")
        self.log_message("Ready to monitor launcher", "INFO")
        self.root.mainloop()

if __name__ == "__main__":
    print("=" * 60)
    print("KOF Ultimate - AI Navigator")
    print("=" * 60)
    print()
    print("This AI agent will monitor the launcher in parallel")
    print("and detect all potential issues automatically.")
    print()

    navigator = LauncherAINavigator()
    navigator.run()
