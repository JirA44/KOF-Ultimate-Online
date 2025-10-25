#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test automatique continu des combats KOF
Teste tous les personnages sans intervention
"""

import subprocess
import time
import random
import os
import json
from datetime import datetime
import pyautogui
import psutil

# Configuration
GAME_EXE = r"D:\KOF Ultimate Online\KOF_Ultimate_Online.exe"
LOG_FILE = "auto_test_combats.log"
RESULTS_FILE = "test_combats_results.json"
TEST_DURATION = 30  # Secondes par combat
PAUSE_BETWEEN_TESTS = 2

# Charger la liste des personnages
with open('data/select.def', 'r', encoding='utf-8') as f:
    content = f.read()

characters = []
for line in content.split('\n'):
    line = line.strip()
    if line and not line.startswith(';') and not line.startswith('['):
        if ',' in line:
            char_name = line.split(',')[0].strip()
            if char_name and char_name not in ['randomselect', 'chars', 'stages']:
                characters.append(char_name)

print(f"📋 {len(characters)} personnages à tester")

# Charger les résultats précédents
if os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
        results = json.load(f)
else:
    results = {
        'tested': {},
        'crashes': [],
        'working': [],
        'total_tests': 0,
        'start_time': datetime.now().isoformat()
    }

def log(message):
    """Log message avec timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)

    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

def save_results():
    """Sauvegarder les résultats"""
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

def kill_game():
    """Tuer le processus du jeu"""
    for proc in psutil.process_iter(['name']):
        try:
            if 'KOF_Ultimate_Online' in proc.info['name'] or 'Ikemen' in proc.info['name']:
                proc.kill()
                time.sleep(1)
        except:
            pass

def test_character_pair(char1, char2):
    """Tester un combat entre 2 personnages"""
    log(f"🎮 Test: {char1} vs {char2}")

    # Tuer tout processus existant
    kill_game()
    time.sleep(1)

    # Lancer le jeu
    try:
        process = subprocess.Popen([GAME_EXE], cwd=os.path.dirname(GAME_EXE))
        time.sleep(5)  # Attendre chargement

        # Vérifier si le jeu a crashé au démarrage
        if process.poll() is not None:
            log(f"❌ Crash au démarrage avec {char1} vs {char2}")
            results['crashes'].append({
                'char1': char1,
                'char2': char2,
                'type': 'startup_crash',
                'time': datetime.now().isoformat()
            })
            return False

        # Navigation automatique vers Versus
        time.sleep(3)

        # Appuyer sur ENTER pour menu principal
        pyautogui.press('return')
        time.sleep(0.5)

        # Aller à Versus (flèche bas x1)
        pyautogui.press('down')
        time.sleep(0.3)
        pyautogui.press('return')
        time.sleep(2)

        # Sélection P1 - Position aléatoire puis SPACE pour sélectionner
        for _ in range(random.randint(0, len(characters) - 1)):
            pyautogui.press('right')
            time.sleep(0.05)

        pyautogui.press('space')  # Sélection manuelle P1
        time.sleep(1)

        # Sélection P2 - Position aléatoire puis SPACE
        for _ in range(random.randint(0, len(characters) - 1)):
            pyautogui.press('right')
            time.sleep(0.05)

        pyautogui.press('space')  # Sélection manuelle P2
        time.sleep(2)

        # Vérifier crash après sélection
        if process.poll() is not None:
            log(f"❌ Crash après sélection: {char1} vs {char2}")
            results['crashes'].append({
                'char1': char1,
                'char2': char2,
                'type': 'selection_crash',
                'time': datetime.now().isoformat()
            })
            return False

        # Laisser le combat se dérouler
        log(f"⏳ Combat en cours... ({TEST_DURATION}s)")

        # Simuler des inputs aléatoires pendant le combat
        start_time = time.time()
        while time.time() - start_time < TEST_DURATION:
            if process.poll() is not None:
                log(f"❌ Crash pendant combat: {char1} vs {char2}")
                results['crashes'].append({
                    'char1': char1,
                    'char2': char2,
                    'type': 'combat_crash',
                    'time': datetime.now().isoformat()
                })
                return False

            # Input aléatoire
            if random.random() < 0.3:
                key = random.choice(['a', 's', 'd', 'z', 'x', 'c'])
                pyautogui.press(key)

            time.sleep(0.5)

        # Combat réussi
        log(f"✅ Combat OK: {char1} vs {char2}")
        results['working'].append({
            'char1': char1,
            'char2': char2,
            'time': datetime.now().isoformat()
        })

        # Tuer le jeu
        kill_game()
        return True

    except Exception as e:
        log(f"❌ Erreur: {e}")
        kill_game()
        return False

    finally:
        time.sleep(PAUSE_BETWEEN_TESTS)

def main():
    """Boucle principale de test"""
    log("=" * 70)
    log("🚀 DÉMARRAGE TEST AUTOMATIQUE CONTINU")
    log(f"📊 {len(characters)} personnages à tester")
    log(f"⏱️  {TEST_DURATION}s par combat")
    log("=" * 70)

    test_count = 0

    try:
        while True:
            # Sélectionner 2 personnages aléatoires
            char1 = random.choice(characters)
            char2 = random.choice(characters)

            # Éviter de tester un perso contre lui-même
            while char2 == char1:
                char2 = random.choice(characters)

            # Créer clé unique pour ce combat
            pair_key = f"{char1}__vs__{char2}"

            # Marquer comme testé
            if pair_key not in results['tested']:
                results['tested'][pair_key] = {
                    'attempts': 0,
                    'successes': 0,
                    'failures': 0
                }

            results['tested'][pair_key]['attempts'] += 1

            # Tester le combat
            success = test_character_pair(char1, char2)

            if success:
                results['tested'][pair_key]['successes'] += 1
            else:
                results['tested'][pair_key]['failures'] += 1

            # Incrémenter compteur
            test_count += 1
            results['total_tests'] = test_count

            # Sauvegarder résultats
            save_results()

            # Stats
            crash_rate = len(results['crashes']) / test_count * 100 if test_count > 0 else 0
            log(f"📊 Stats: {test_count} tests | {len(results['working'])} OK | {len(results['crashes'])} crashes ({crash_rate:.1f}%)")

            # Pause entre tests
            time.sleep(PAUSE_BETWEEN_TESTS)

    except KeyboardInterrupt:
        log("\n🛑 Arrêt demandé par l'utilisateur")
        log(f"📊 Tests effectués: {test_count}")
        log(f"✅ Réussis: {len(results['working'])}")
        log(f"❌ Crashes: {len(results['crashes'])}")
        save_results()

        # Générer rapport
        log("\n📋 RAPPORT FINAL:")
        log(f"   Total tests: {test_count}")
        log(f"   Combats OK: {len(results['working'])}")
        log(f"   Crashes: {len(results['crashes'])}")

        if results['crashes']:
            log("\n❌ Personnages problématiques:")
            crash_chars = {}
            for crash in results['crashes']:
                for char in [crash['char1'], crash['char2']]:
                    crash_chars[char] = crash_chars.get(char, 0) + 1

            for char, count in sorted(crash_chars.items(), key=lambda x: x[1], reverse=True)[:10]:
                log(f"   {char}: {count} crashes")

if __name__ == '__main__':
    main()
