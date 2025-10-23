#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VISUALISEUR DE RAPPORTS EN TEMPS RÉEL
Dashboard pour voir les tests continus
"""

import os
import time
import json
from pathlib import Path
from datetime import datetime

LOGS_DIR = Path("logs/tests_continus")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_duration(seconds):
    """Formate une durée en secondes"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def display_dashboard():
    """Affiche le dashboard"""
    clear()

    print("═" * 80)
    print("  🎮 DASHBOARD TESTS CONTINUS - KOF ULTIMATE ONLINE")
    print("  " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("═" * 80)
    print()

    # Stats
    stats_file = LOGS_DIR / "stats.json"
    if stats_file.exists():
        with open(stats_file, 'r') as f:
            stats = json.load(f)

        print("📊 STATISTIQUES GLOBALES")
        print("─" * 80)
        print(f"  Total tests:      {stats['total_tests']}")
        print(f"  Total problèmes:  {stats['total_issues']}")
        print(f"  Taux de réussite: {stats['success_rate']:.1f}%")
        print(f"  Uptime:           {format_duration(stats['uptime'])}")
        print(f"  Dernière MAJ:     {stats['last_update']}")
        print()

    # Derniers tests
    test_files = sorted(LOGS_DIR.glob("test_*.txt"), key=lambda p: p.stat().st_mtime, reverse=True)

    if test_files:
        print("📝 DERNIERS TESTS (5 plus récents)")
        print("─" * 80)

        for i, test_file in enumerate(test_files[:5], 1):
            with open(test_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Extraire info
            test_num = test_file.stem.split('_')[1]
            date_str = ' '.join(test_file.stem.split('_')[2:])

            status = "✅" if "Aucun problème" in ''.join(lines) else "⚠️"

            print(f"  {status} Test #{test_num} - {date_str}")

        print()

    # Log en temps réel
    log_file = LOGS_DIR / "continuous.log"
    if log_file.exists():
        print("📋 LOG EN TEMPS RÉEL (10 dernières lignes)")
        print("─" * 80)

        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[-10:]:
                print(f"  {line.rstrip()}")

        print()

    print("─" * 80)
    print("  Actualisation dans 5s... (Ctrl+C pour quitter)")
    print("─" * 80)

def main():
    """Boucle principale"""
    if not LOGS_DIR.exists():
        print("❌ Aucun log trouvé. Les tests continus ne sont pas lancés.")
        print(f"   Lancez DEMARRER_TESTS_CONTINUS.bat")
        input("\nAppuyez sur ENTRÉE...")
        return

    try:
        while True:
            display_dashboard()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n\n✅ Visualiseur arrêté")

if __name__ == "__main__":
    main()
