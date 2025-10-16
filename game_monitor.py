#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de monitoring pour KOF Ultimate
Lance le jeu et surveille les logs, erreurs et performances
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path
import threading
import re

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class GameMonitor:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.log_file = self.base_dir / "game_monitor.log"
        self.mugen_log = self.base_dir / "mugen.log"
        self.ai_player_log = self.base_dir / "ai_player.log"
        self.processes = []
        self.start_time = None
        self.errors = []
        self.warnings = []
        self.events = []

    def log(self, message, level="INFO", color=Colors.WHITE):
        """Log un message avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] [{level}] {message}"

        # Afficher dans le terminal avec couleur
        print(f"{color}{log_msg}{Colors.RESET}")

        # Sauvegarder dans le fichier de log
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')

    def log_error(self, message):
        """Log une erreur"""
        self.errors.append(message)
        self.log(message, "ERROR", Colors.RED)

    def log_warning(self, message):
        """Log un avertissement"""
        self.warnings.append(message)
        self.log(message, "WARN", Colors.YELLOW)

    def log_success(self, message):
        """Log un succès"""
        self.log(message, "OK", Colors.GREEN)

    def log_event(self, message):
        """Log un événement"""
        self.events.append(message)
        self.log(message, "EVENT", Colors.CYAN)

    def print_header(self):
        """Affiche l'en-tête"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'KOF ULTIMATE - SYSTÈME DE MONITORING':^80}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

    def check_files(self):
        """Vérifie que les fichiers nécessaires existent"""
        self.log("Vérification des fichiers...", color=Colors.BLUE)

        required_files = [
            "KOF_Ultimate_Online.exe",
            "data/system.def",
            "data/select.def",
            "data/mugen.cfg"
        ]

        all_ok = True
        for file_path in required_files:
            full_path = self.base_dir / file_path
            if full_path.exists():
                self.log_success(f"✓ {file_path}")
            else:
                self.log_error(f"✗ {file_path} - MANQUANT")
                all_ok = False

        return all_ok

    def monitor_log_file(self, log_path, stop_event):
        """Surveille un fichier de log en temps réel"""
        if not log_path.exists():
            return

        self.log(f"Monitoring: {log_path.name}", color=Colors.BLUE)

        # Lire le fichier depuis la fin
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            # Aller à la fin du fichier
            f.seek(0, 2)

            while not stop_event.is_set():
                line = f.readline()

                if line:
                    line = line.strip()

                    # Détecter les erreurs
                    if re.search(r'error|erreur|failed|échec', line, re.IGNORECASE):
                        self.log_error(f"{log_path.name}: {line}")

                    # Détecter les avertissements
                    elif re.search(r'warn|warning|avertissement', line, re.IGNORECASE):
                        self.log_warning(f"{log_path.name}: {line}")

                    # Log normal
                    else:
                        self.log(f"{log_path.name}: {line}", color=Colors.WHITE)

                else:
                    # Attendre un peu avant de relire
                    time.sleep(0.1)

    def launch_game(self):
        """Lance le jeu"""
        self.log_event("Lancement du jeu...")

        exe_path = self.base_dir / "KOF_Ultimate_Online.exe"

        if not exe_path.exists():
            self.log_error("Exécutable du jeu non trouvé!")
            return None

        try:
            # Lancer le jeu
            process = subprocess.Popen(
                [str(exe_path)],
                cwd=str(self.base_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
            )

            self.processes.append(process)
            self.log_success(f"✓ Jeu lancé (PID: {process.pid})")

            return process

        except Exception as e:
            self.log_error(f"Erreur lors du lancement: {e}")
            return None

    def monitor_game_process(self, process, stop_event):
        """Surveille le processus du jeu"""
        while not stop_event.is_set() and process.poll() is None:
            time.sleep(1)

        if process.poll() is not None:
            return_code = process.returncode

            if return_code == 0:
                self.log_success(f"✓ Le jeu s'est terminé normalement (code: {return_code})")
            else:
                self.log_error(f"✗ Le jeu s'est terminé avec une erreur (code: {return_code})")

    def generate_report(self):
        """Génère un rapport final"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'RAPPORT FINAL':^80}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

        # Durée de la session
        if self.start_time:
            duration = time.time() - self.start_time
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            self.log(f"Durée de la session: {minutes}m {seconds}s", color=Colors.BLUE)

        # Statistiques
        print(f"\n{Colors.BOLD}Statistiques:{Colors.RESET}")
        self.log(f"Erreurs détectées: {len(self.errors)}", color=Colors.RED if self.errors else Colors.GREEN)
        self.log(f"Avertissements: {len(self.warnings)}", color=Colors.YELLOW if self.warnings else Colors.GREEN)
        self.log(f"Événements: {len(self.events)}", color=Colors.CYAN)

        # Afficher les erreurs si présentes
        if self.errors:
            print(f"\n{Colors.BOLD}Erreurs détaillées:{Colors.RESET}")
            for i, error in enumerate(self.errors[:10], 1):  # Limiter à 10 erreurs
                print(f"{Colors.RED}  {i}. {error}{Colors.RESET}")

            if len(self.errors) > 10:
                print(f"{Colors.YELLOW}  ... et {len(self.errors) - 10} autres erreurs{Colors.RESET}")

        # Recommandations
        print(f"\n{Colors.BOLD}Recommandations:{Colors.RESET}")

        if not self.errors and not self.warnings:
            print(f"{Colors.GREEN}  ✓ Aucun problème détecté - Le jeu fonctionne parfaitement!{Colors.RESET}")
        elif self.errors:
            print(f"{Colors.RED}  ⚠ Des erreurs ont été détectées - Consultez les logs pour plus de détails{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}  ⚠ Quelques avertissements détectés - Le jeu devrait fonctionner normalement{Colors.RESET}")

        print(f"\n{Colors.BLUE}Logs complets sauvegardés dans: {self.log_file}{Colors.RESET}")

    def run(self, duration=None):
        """Lance le monitoring"""
        self.print_header()
        self.start_time = time.time()

        # Initialiser le fichier de log
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"=== MONITORING KOF ULTIMATE - {datetime.now()} ===\n\n")

        # Vérifier les fichiers
        if not self.check_files():
            self.log_error("Fichiers manquants - Arrêt du monitoring")
            return

        # Lancer le jeu
        game_process = self.launch_game()

        if not game_process:
            return

        # Créer un événement pour arrêter les threads
        stop_event = threading.Event()

        # Lancer les threads de monitoring des logs
        log_threads = []

        for log_path in [self.mugen_log, self.ai_player_log]:
            if log_path.exists():
                thread = threading.Thread(
                    target=self.monitor_log_file,
                    args=(log_path, stop_event)
                )
                thread.daemon = True
                thread.start()
                log_threads.append(thread)

        # Lancer le thread de monitoring du processus
        process_thread = threading.Thread(
            target=self.monitor_game_process,
            args=(game_process, stop_event)
        )
        process_thread.daemon = True
        process_thread.start()

        try:
            # Si une durée est spécifiée, attendre ce temps
            if duration:
                self.log(f"Monitoring pendant {duration} secondes...", color=Colors.CYAN)
                time.sleep(duration)
            else:
                # Sinon, attendre que le jeu se ferme
                self.log("Monitoring actif - Appuyez sur Ctrl+C pour arrêter", color=Colors.CYAN)
                process_thread.join()

        except KeyboardInterrupt:
            self.log_event("\nArrêt du monitoring demandé par l'utilisateur")

        finally:
            # Arrêter tous les threads
            stop_event.set()

            # Attendre un peu que les threads se terminent
            time.sleep(1)

            # Générer le rapport final
            self.generate_report()

            print(f"\n{Colors.BOLD}Monitoring terminé.{Colors.RESET}\n")

def main():
    monitor = GameMonitor()
    monitor.run()

if __name__ == '__main__':
    main()
