#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONITEUR DE TESTS EN TEMPS RÉEL
Affiche l'état actuel des tests automatiques
"""

import os
import time
from pathlib import Path
from datetime import datetime
import json

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_latest_log():
    """Trouve le dernier log de test"""
    logs_dir = Path("logs")
    if not logs_dir.exists():
        return None

    log_files = list(logs_dir.glob("test_*.txt"))
    if not log_files:
        return None

    return max(log_files, key=lambda p: p.stat().st_mtime)

def display_log_content(log_file):
    """Affiche le contenu du dernier log"""
    if not log_file or not log_file.exists():
        return "Aucun log trouvé"

    with open(log_file, 'r', encoding='utf-8') as f:
        return f.read()

def check_game_running():
    """Vérifie si le jeu tourne"""
    try:
        if os.name == 'nt':
            result = os.popen('tasklist /FI "IMAGENAME eq KOF_Ultimate_Online.exe" /FO CSV').read()
            return "KOF_Ultimate_Online.exe" in result
        else:
            result = os.popen('ps aux | grep -i ikemen').read()
            return 'ikemen' in result.lower()
    except:
        return False

def main():
    """Boucle principale de monitoring"""
    print("\n" + "="*70)
    print("  🎮 MONITEUR DE TESTS EN TEMPS RÉEL")
    print("  KOF Ultimate Online")
    print("="*70 + "\n")
    print("Appuyez sur Ctrl+C pour arrêter\n")

    iteration = 0

    try:
        while True:
            clear_screen()

            print("="*70)
            print(f"  🎮 MONITEUR DE TESTS - Actualisation #{iteration}")
            print(f"  {datetime.now().strftime('%H:%M:%S')}")
            print("="*70 + "\n")

            # État du jeu
            game_running = check_game_running()
            status_icon = "🟢" if game_running else "🔴"
            status_text = "EN COURS" if game_running else "ARRÊTÉ"

            print(f"{status_icon} Jeu: {status_text}\n")

            # Dernier log
            latest_log = get_latest_log()
            if latest_log:
                print(f"📄 Dernier rapport: {latest_log.name}")
                mod_time = datetime.fromtimestamp(latest_log.stat().st_mtime)
                age = (datetime.now() - mod_time).total_seconds()
                print(f"   Modifié il y a {age:.0f}s\n")

                print("─" * 70)
                print("CONTENU DU RAPPORT:")
                print("─" * 70)
                content = display_log_content(latest_log)
                # Limiter à 40 lignes
                lines = content.split('\n')
                if len(lines) > 40:
                    print('\n'.join(lines[:40]))
                    print(f"\n... ({len(lines) - 40} lignes supplémentaires)")
                else:
                    print(content)
            else:
                print("📄 Aucun rapport de test disponible")

            print("\n" + "─" * 70)
            print("Actualisation dans 5s... (Ctrl+C pour arrêter)")

            time.sleep(5)
            iteration += 1

    except KeyboardInterrupt:
        print("\n\n✅ Monitoring arrêté")

if __name__ == "__main__":
    main()
