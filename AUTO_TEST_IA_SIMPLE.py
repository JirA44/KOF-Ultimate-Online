#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test automatique IA vs IA - Version simple
Lance le jeu en boucle et monitore les crashes
"""

import subprocess
import time
import random
import os
import json
from datetime import datetime
import psutil

# Configuration
GAME_EXE = r"D:\KOF Ultimate Online\KOF_Ultimate_Online.exe"
GAME_DIR = r"D:\KOF Ultimate Online"
LOG_FILE = "auto_test_ia_simple.log"
RESULTS_FILE = "test_ia_simple_results.json"
COMBAT_DURATION = 45  # Durée avant de tuer le jeu
PAUSE_BETWEEN = 5

def log(message):
    """Log avec timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    msg = f"[{timestamp}] {message}"
    print(msg)

    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')

def kill_game():
    """Tuer le jeu"""
    killed = False
    for proc in psutil.process_iter(['name']):
        try:
            name = proc.info['name']
            if name and ('KOF' in name or 'Ikemen' in name or 'mugen' in name.lower()):
                proc.kill()
                killed = True
        except:
            pass

    if killed:
        time.sleep(2)

def load_results():
    """Charger résultats"""
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass

    return {
        'total_tests': 0,
        'crashes': 0,
        'successful': 0,
        'start_time': datetime.now().isoformat()
    }

def save_results(results):
    """Sauvegarder résultats"""
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)

def test_game():
    """Lancer le jeu et vérifier"""
    log("🎮 Lancement du jeu...")

    # Tuer processus existants
    kill_game()

    try:
        # Lancer le jeu
        process = subprocess.Popen(
            [GAME_EXE],
            cwd=GAME_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Attendre démarrage
        time.sleep(8)

        # Vérifier crash au démarrage
        if process.poll() is not None:
            log("  ❌ Crash au démarrage")
            return False

        log(f"  ⏳ Jeu lancé, attente {COMBAT_DURATION}s...")

        # Attendre
        start = time.time()
        while time.time() - start < COMBAT_DURATION:
            # Vérifier toujours vivant
            if process.poll() is not None:
                elapsed = int(time.time() - start)
                log(f"  ❌ Crash après {elapsed}s")
                return False

            time.sleep(2)

        # Succès
        log("  ✅ Test réussi!")
        kill_game()
        return True

    except Exception as e:
        log(f"  ❌ Erreur: {e}")
        kill_game()
        return False

def main():
    """Boucle principale"""
    log("=" * 70)
    log("🚀 TEST AUTOMATIQUE IA - VERSION SIMPLE")
    log("=" * 70)
    log("")

    results = load_results()

    try:
        while True:
            results['total_tests'] += 1
            test_num = results['total_tests']

            log(f"🧪 Test #{test_num}")

            # Lancer test
            success = test_game()

            if success:
                results['successful'] += 1
            else:
                results['crashes'] += 1

            # Sauvegarder
            save_results(results)

            # Stats
            crash_rate = (results['crashes'] / results['total_tests'] * 100) if results['total_tests'] > 0 else 0
            log(f"📊 Stats: {results['total_tests']} tests | Crashes: {results['crashes']} ({crash_rate:.1f}%)")
            log("")

            # Pause
            time.sleep(PAUSE_BETWEEN)

    except KeyboardInterrupt:
        log("")
        log("🛑 Arrêt demandé")
        log(f"📊 Total: {results['total_tests']} tests, {results['crashes']} crashes")
        save_results(results)

if __name__ == '__main__':
    main()
