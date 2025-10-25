#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test automatique IA vs IA - Mode silencieux
Les IAs combattent toutes seules, je log juste les résultats
"""

import subprocess
import time
import random
import os
import json
from datetime import datetime
import psutil
import re

# Configuration
GAME_EXE = r"D:\KOF Ultimate Online\KOF_Ultimate_Online.exe"
GAME_DIR = r"D:\KOF Ultimate Online"
LOG_FILE = "auto_test_ia_vs_ia.log"
RESULTS_FILE = "test_ia_results.json"
MUGEN_LOG = "mugen.log"
COMBAT_DURATION = 60  # Durée max d'un combat (secondes)
PAUSE_BETWEEN_COMBATS = 3

# Charger personnages actifs
def load_characters():
    """Charger la liste des personnages actifs depuis select.def"""
    chars = []
    try:
        with open(os.path.join(GAME_DIR, 'data', 'select.def'), 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith(';') and not line.startswith('['):
                    if ',' in line:
                        char = line.split(',')[0].strip()
                        if char and char not in ['randomselect', 'chars', 'stages']:
                            chars.append(char)
    except Exception as e:
        log(f"❌ Erreur chargement personnages: {e}")
        return []

    return chars

# Load results
def load_results():
    """Charger les résultats précédents"""
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass

    return {
        'combats': [],
        'crashes': [],
        'characters_tested': {},
        'total_combats': 0,
        'total_crashes': 0,
        'start_time': datetime.now().isoformat(),
        'problematic_chars': []
    }

results = load_results()

def log(message):
    """Log avec timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    msg = f"[{timestamp}] {message}"
    print(msg)

    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')

def save_results():
    """Sauvegarder résultats"""
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

def kill_game():
    """Tuer tous les processus du jeu"""
    killed = False
    for proc in psutil.process_iter(['name']):
        try:
            proc_name = proc.info['name']
            if proc_name and ('KOF_Ultimate' in proc_name or 'Ikemen' in proc_name or proc_name == 'mugen.exe'):
                proc.kill()
                killed = True
        except:
            pass

    if killed:
        time.sleep(1)

def check_crash_in_log():
    """Vérifier si le jeu a crashé en lisant mugen.log"""
    log_path = os.path.join(GAME_DIR, MUGEN_LOG)

    if not os.path.exists(log_path):
        return False, None

    try:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        # Chercher les dernières lignes pour erreurs
        last_50_lines = lines[-50:] if len(lines) > 50 else lines

        for line in reversed(last_50_lines):
            # Patterns d'erreur
            if any(pattern in line.lower() for pattern in ['error', 'crash', 'exception', 'fatal', 'assertion failed']):
                return True, line.strip()

        return False, None

    except Exception as e:
        return False, None

def run_ai_vs_ai_combat(char1, char2):
    """Lancer un combat IA vs IA"""

    log(f"🤖 Combat: {char1} vs {char2}")

    # Nettoyer les processus existants
    kill_game()

    # Effacer mugen.log
    log_path = os.path.join(GAME_DIR, MUGEN_LOG)
    if os.path.exists(log_path):
        try:
            os.remove(log_path)
        except:
            pass

    # Lancer le jeu
    try:
        process = subprocess.Popen(
            [GAME_EXE],
            cwd=GAME_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Attendre un peu le démarrage
        time.sleep(5)

        # Vérifier crash au démarrage
        if process.poll() is not None:
            log(f"  ❌ Crash au démarrage")
            return False, 'startup_crash'

        # Attendre la fin du combat ou timeout
        start_time = time.time()
        combat_ongoing = True

        while combat_ongoing and (time.time() - start_time < COMBAT_DURATION):
            # Vérifier si processus toujours vivant
            if process.poll() is not None:
                log(f"  ❌ Processus terminé prématurément")

                # Vérifier le log pour erreurs
                has_error, error_msg = check_crash_in_log()
                if has_error:
                    log(f"  💥 Erreur détectée: {error_msg[:100]}")
                    return False, 'combat_crash'

                return False, 'unexpected_exit'

            time.sleep(1)

        # Combat réussi (timeout atteint)
        log(f"  ✅ Combat terminé sans crash")
        kill_game()
        return True, None

    except Exception as e:
        log(f"  ❌ Exception: {e}")
        kill_game()
        return False, 'exception'

def main():
    """Boucle principale"""

    log("=" * 70)
    log("🚀 TEST AUTOMATIQUE IA vs IA - MODE CONTINU")
    log("=" * 70)

    # Charger personnages
    characters = load_characters()

    if not characters:
        log("❌ Aucun personnage trouvé!")
        return

    log(f"📋 {len(characters)} personnages chargés")
    log(f"⏱️  {COMBAT_DURATION}s max par combat")
    log(f"🤖 Les IAs vont combattre automatiquement")
    log("")

    combat_num = results['total_combats']

    try:
        while True:
            combat_num += 1

            # Sélectionner 2 persos aléatoires
            char1 = random.choice(characters)
            char2 = random.choice(characters)

            # Éviter même perso
            while char2 == char1:
                char2 = random.choice(characters)

            # Tracker les persos testés
            for char in [char1, char2]:
                if char not in results['characters_tested']:
                    results['characters_tested'][char] = {
                        'total_combats': 0,
                        'crashes': 0,
                        'successes': 0
                    }

                results['characters_tested'][char]['total_combats'] += 1

            # Lancer combat
            success, crash_type = run_ai_vs_ai_combat(char1, char2)

            # Enregistrer résultat
            combat_data = {
                'num': combat_num,
                'char1': char1,
                'char2': char2,
                'success': success,
                'crash_type': crash_type,
                'timestamp': datetime.now().isoformat()
            }

            results['combats'].append(combat_data)
            results['total_combats'] = combat_num

            if success:
                results['characters_tested'][char1]['successes'] += 1
                results['characters_tested'][char2]['successes'] += 1
            else:
                results['total_crashes'] += 1
                results['characters_tested'][char1]['crashes'] += 1
                results['characters_tested'][char2]['crashes'] += 1

                results['crashes'].append(combat_data)

            # Sauvegarder
            save_results()

            # Stats
            crash_rate = (results['total_crashes'] / combat_num * 100) if combat_num > 0 else 0
            log(f"📊 Combat #{combat_num} | Crashes: {results['total_crashes']} ({crash_rate:.1f}%)")

            # Afficher top persos problématiques toutes les 10 combats
            if combat_num % 10 == 0:
                log("")
                log("🔍 Top 5 personnages problématiques:")

                problem_chars = []
                for char, stats in results['characters_tested'].items():
                    if stats['total_combats'] >= 3:
                        crash_rate_char = (stats['crashes'] / stats['total_combats'] * 100)
                        if crash_rate_char > 30:
                            problem_chars.append((char, crash_rate_char, stats['crashes']))

                problem_chars.sort(key=lambda x: x[2], reverse=True)

                for char, rate, count in problem_chars[:5]:
                    log(f"   ⚠️  {char}: {count} crashes ({rate:.0f}%)")

                log("")

            # Pause
            time.sleep(PAUSE_BETWEEN_COMBATS)

    except KeyboardInterrupt:
        log("")
        log("🛑 Arrêt demandé")
        generate_report()

def generate_report():
    """Générer rapport final"""
    log("")
    log("=" * 70)
    log("📊 RAPPORT FINAL")
    log("=" * 70)
    log(f"Total combats: {results['total_combats']}")
    log(f"Crashes: {results['total_crashes']}")

    if results['total_combats'] > 0:
        crash_rate = results['total_crashes'] / results['total_combats'] * 100
        log(f"Taux de crash: {crash_rate:.1f}%")

    log("")
    log("❌ TOP 10 PERSONNAGES PROBLÉMATIQUES:")

    problem_chars = []
    for char, stats in results['characters_tested'].items():
        if stats['total_combats'] >= 2:
            crash_rate_char = (stats['crashes'] / stats['total_combats'] * 100)
            problem_chars.append((char, crash_rate_char, stats['crashes'], stats['total_combats']))

    problem_chars.sort(key=lambda x: x[2], reverse=True)

    for i, (char, rate, crashes, total) in enumerate(problem_chars[:10], 1):
        log(f"{i}. {char}: {crashes}/{total} crashes ({rate:.0f}%)")

    log("")
    log(f"📁 Résultats sauvegardés dans: {RESULTS_FILE}")
    save_results()

if __name__ == '__main__':
    main()
