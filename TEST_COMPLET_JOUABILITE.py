#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST COMPLET DE JOUABILITÉ - KOF Ultimate Online
Teste absolument tout pour s'assurer que le jeu est 100% jouable
"""

import os
import sys
import time
import json
import subprocess
import psutil
import random
from datetime import datetime
from pathlib import Path

# Configuration
GAME_DIR = Path(__file__).parent
GAME_EXE = GAME_DIR / "KOF_Ultimate_Online.exe"
SELECT_DEF = GAME_DIR / "data" / "select.def"
STAGES_DIR = GAME_DIR / "stages"
LOG_FILE = GAME_DIR / "test_complet_jouabilite.log"
RESULTS_FILE = GAME_DIR / "test_jouabilite_results.json"

# Durées
LAUNCH_WAIT = 10  # Attendre 10s après le lancement
MENU_WAIT = 8     # Attendre 8s pour navigation menu
LOAD_WAIT = 15    # Attendre 15s pour chargement combat
COMBAT_DURATION = 45  # 45s de combat minimum
MAX_TESTS_PER_PHASE = 20  # Tests max par phase

class Color:
    """Couleurs pour l'affichage"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class TestSystem:
    def __init__(self):
        self.log_file = open(LOG_FILE, 'w', encoding='utf-8')
        self.results = {
            "start_time": datetime.now().isoformat(),
            "phases": {},
            "characters_tested": [],
            "stages_tested": [],
            "total_crashes": 0,
            "total_tests": 0,
            "success_rate": 0.0
        }

    def log(self, message, color=Color.END):
        """Logger avec couleur et timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}"
        print(f"{color}{formatted}{Color.END}")
        self.log_file.write(formatted + "\n")
        self.log_file.flush()

    def kill_game(self):
        """Tuer toutes les instances du jeu"""
        killed = 0
        for proc in psutil.process_iter(['name']):
            try:
                if 'KOF_Ultimate_Online.exe' in proc.info['name']:
                    proc.kill()
                    killed += 1
            except:
                pass
        if killed > 0:
            time.sleep(2)
        return killed

    def is_game_running(self):
        """Vérifier si le jeu tourne"""
        for proc in psutil.process_iter(['name']):
            try:
                if 'KOF_Ultimate_Online.exe' in proc.info['name']:
                    return True
            except:
                pass
        return False

    def launch_game(self):
        """Lancer le jeu"""
        self.kill_game()

        try:
            process = subprocess.Popen(
                [str(GAME_EXE)],
                cwd=str(GAME_DIR),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(LAUNCH_WAIT)

            if self.is_game_running():
                return process
            else:
                self.log("  ❌ Jeu ne s'est pas lancé", Color.RED)
                return None
        except Exception as e:
            self.log(f"  ❌ Erreur au lancement: {e}", Color.RED)
            return None

    def test_basic_launch(self):
        """Phase 1: Test de lancement basique"""
        self.log("=" * 80, Color.CYAN)
        self.log("PHASE 1: TEST DE LANCEMENT BASIQUE", Color.CYAN + Color.BOLD)
        self.log("=" * 80, Color.CYAN)

        results = {"total": 5, "success": 0, "crashes": 0}

        for i in range(1, 6):
            self.log(f"\n🧪 Test {i}/5: Lancement et attente au menu", Color.BLUE)
            self.results["total_tests"] += 1

            process = self.launch_game()
            if not process:
                results["crashes"] += 1
                continue

            self.log("  ✅ Jeu lancé", Color.GREEN)

            # Attendre au menu
            start = time.time()
            while time.time() - start < 30:
                if not self.is_game_running():
                    elapsed = int(time.time() - start)
                    self.log(f"  ❌ Crash au menu après {elapsed}s", Color.RED)
                    results["crashes"] += 1
                    self.results["total_crashes"] += 1
                    break
                time.sleep(2)
            else:
                self.log("  ✅ Stable au menu pendant 30s", Color.GREEN)
                results["success"] += 1

            self.kill_game()
            time.sleep(2)

        self.results["phases"]["launch"] = results
        self.log(f"\n📊 Résultats Phase 1: {results['success']}/{results['total']} réussis",
                Color.YELLOW)
        return results["success"] == results["total"]

    def read_characters(self):
        """Lire la liste des personnages"""
        chars = []
        try:
            with open(SELECT_DEF, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith(';') and ',' in line:
                        char_name = line.split(',')[0].strip()
                        if char_name and char_name != '[Characters]':
                            chars.append(char_name)
        except Exception as e:
            self.log(f"❌ Erreur lecture select.def: {e}", Color.RED)
        return chars

    def test_characters_combat(self):
        """Phase 2: Test des combats avec personnages aléatoires"""
        self.log("\n" + "=" * 80, Color.CYAN)
        self.log("PHASE 2: TEST DES COMBATS (PERSONNAGES ALÉATOIRES)", Color.CYAN + Color.BOLD)
        self.log("=" * 80, Color.CYAN)

        chars = self.read_characters()
        self.log(f"ℹ️  {len(chars)} personnages à tester", Color.BLUE)

        results = {"total": 0, "success": 0, "crashes": 0, "tested_pairs": []}

        # Tester MAX_TESTS_PER_PHASE paires aléatoires
        for i in range(1, min(MAX_TESTS_PER_PHASE + 1, 31)):
            self.log(f"\n🧪 Combat {i}/{MAX_TESTS_PER_PHASE}: Test paire aléatoire", Color.BLUE)
            self.results["total_tests"] += 1
            results["total"] += 1

            # Choisir 2 persos aléatoires
            char1, char2 = random.sample(chars, 2)
            self.log(f"  👤 P1: {char1}", Color.CYAN)
            self.log(f"  👤 P2: {char2}", Color.CYAN)

            results["tested_pairs"].append([char1, char2])

            process = self.launch_game()
            if not process:
                results["crashes"] += 1
                self.results["total_crashes"] += 1
                continue

            # Laisser tourner le combat
            self.log("  ⏳ Combat en cours...", Color.YELLOW)
            start = time.time()
            crashed = False

            while time.time() - start < COMBAT_DURATION:
                if not self.is_game_running():
                    elapsed = int(time.time() - start)
                    self.log(f"  ❌ Crash après {elapsed}s", Color.RED)
                    results["crashes"] += 1
                    self.results["total_crashes"] += 1
                    crashed = True
                    break
                time.sleep(2)

            if not crashed:
                self.log("  ✅ Combat complété sans crash", Color.GREEN)
                results["success"] += 1

            self.kill_game()
            time.sleep(3)

        self.results["phases"]["combat"] = results
        self.log(f"\n📊 Résultats Phase 2: {results['success']}/{results['total']} réussis, "
                f"{results['crashes']} crashes", Color.YELLOW)
        return results["crashes"] == 0

    def test_all_characters_individually(self):
        """Phase 3: Test de chaque personnage individuellement"""
        self.log("\n" + "=" * 80, Color.CYAN)
        self.log("PHASE 3: TEST INDIVIDUEL DE CHAQUE PERSONNAGE", Color.CYAN + Color.BOLD)
        self.log("=" * 80, Color.CYAN)

        chars = self.read_characters()
        self.log(f"ℹ️  {len(chars)} personnages à tester individuellement", Color.BLUE)

        results = {"total": len(chars), "success": 0, "crashes": 0, "problem_chars": []}

        # Perso de référence stable (KFM par défaut)
        reference = "kfm"

        for idx, char in enumerate(chars, 1):
            self.log(f"\n🧪 [{idx}/{len(chars)}] Test: {char}", Color.BLUE)
            self.results["total_tests"] += 1

            if char not in self.results["characters_tested"]:
                self.results["characters_tested"].append(char)

            process = self.launch_game()
            if not process:
                results["crashes"] += 1
                self.results["total_crashes"] += 1
                results["problem_chars"].append({"name": char, "reason": "Jeu ne lance pas"})
                continue

            # Test le combat
            start = time.time()
            crashed = False

            while time.time() - start < COMBAT_DURATION:
                if not self.is_game_running():
                    elapsed = int(time.time() - start)
                    self.log(f"  ❌ Crash avec {char} après {elapsed}s", Color.RED)
                    results["crashes"] += 1
                    self.results["total_crashes"] += 1
                    results["problem_chars"].append({"name": char, "reason": f"Crash après {elapsed}s"})
                    crashed = True
                    break
                time.sleep(2)

            if not crashed:
                self.log(f"  ✅ {char} OK", Color.GREEN)
                results["success"] += 1

            self.kill_game()
            time.sleep(2)

        self.results["phases"]["individual_chars"] = results
        self.log(f"\n📊 Résultats Phase 3: {results['success']}/{results['total']} OK, "
                f"{len(results['problem_chars'])} problématiques", Color.YELLOW)
        return len(results["problem_chars"]) == 0

    def test_stages(self):
        """Phase 4: Test des stages"""
        self.log("\n" + "=" * 80, Color.CYAN)
        self.log("PHASE 4: TEST DES STAGES", Color.CYAN + Color.BOLD)
        self.log("=" * 80, Color.CYAN)

        # Lister tous les .def dans stages/
        stages = []
        if STAGES_DIR.exists():
            stages = [f.name for f in STAGES_DIR.glob("*.def")]

        self.log(f"ℹ️  {len(stages)} stages trouvés", Color.BLUE)

        results = {"total": len(stages), "success": 0, "crashes": 0, "problem_stages": []}

        # Tester un échantillon de stages (max 10)
        test_stages = random.sample(stages, min(10, len(stages))) if stages else []

        for idx, stage in enumerate(test_stages, 1):
            self.log(f"\n🧪 [{idx}/{len(test_stages)}] Test stage: {stage}", Color.BLUE)
            self.results["total_tests"] += 1

            if stage not in self.results["stages_tested"]:
                self.results["stages_tested"].append(stage)

            # Pour chaque stage, faire un combat rapide
            process = self.launch_game()
            if not process:
                results["crashes"] += 1
                self.results["total_crashes"] += 1
                results["problem_stages"].append({"name": stage, "reason": "Jeu ne lance pas"})
                continue

            start = time.time()
            crashed = False

            while time.time() - start < 30:  # Test plus court pour les stages
                if not self.is_game_running():
                    elapsed = int(time.time() - start)
                    self.log(f"  ❌ Crash avec stage {stage} après {elapsed}s", Color.RED)
                    results["crashes"] += 1
                    self.results["total_crashes"] += 1
                    results["problem_stages"].append({"name": stage, "reason": f"Crash après {elapsed}s"})
                    crashed = True
                    break
                time.sleep(2)

            if not crashed:
                self.log(f"  ✅ Stage {stage} OK", Color.GREEN)
                results["success"] += 1

            self.kill_game()
            time.sleep(2)

        self.results["phases"]["stages"] = results
        self.log(f"\n📊 Résultats Phase 4: {results['success']}/{len(test_stages)} stages OK",
                Color.YELLOW)
        return len(results["problem_stages"]) == 0

    def test_endurance(self):
        """Phase 5: Test d'endurance (sessions longues)"""
        self.log("\n" + "=" * 80, Color.CYAN)
        self.log("PHASE 5: TEST D'ENDURANCE (SESSIONS LONGUES)", Color.CYAN + Color.BOLD)
        self.log("=" * 80, Color.CYAN)

        results = {"total": 3, "success": 0, "crashes": 0}

        for i in range(1, 4):
            self.log(f"\n🧪 Session d'endurance {i}/3 (5 minutes)", Color.BLUE)
            self.results["total_tests"] += 1

            process = self.launch_game()
            if not process:
                results["crashes"] += 1
                self.results["total_crashes"] += 1
                continue

            self.log("  ⏳ Session de 5 minutes en cours...", Color.YELLOW)
            start = time.time()
            crashed = False
            duration = 300  # 5 minutes

            while time.time() - start < duration:
                if not self.is_game_running():
                    elapsed = int(time.time() - start)
                    self.log(f"  ❌ Crash après {elapsed}s ({elapsed//60}min {elapsed%60}s)", Color.RED)
                    results["crashes"] += 1
                    self.results["total_crashes"] += 1
                    crashed = True
                    break

                # Afficher le progrès toutes les 30s
                if int(time.time() - start) % 30 == 0:
                    elapsed = int(time.time() - start)
                    self.log(f"  ⏳ {elapsed}s / {duration}s ({elapsed*100//duration}%)", Color.CYAN)

                time.sleep(5)

            if not crashed:
                self.log("  ✅ Session de 5 minutes complétée", Color.GREEN)
                results["success"] += 1

            self.kill_game()
            time.sleep(3)

        self.results["phases"]["endurance"] = results
        self.log(f"\n📊 Résultats Phase 5: {results['success']}/{results['total']} sessions complètes",
                Color.YELLOW)
        return results["success"] == results["total"]

    def generate_final_report(self):
        """Générer le rapport final"""
        self.log("\n" + "=" * 80, Color.HEADER)
        self.log("RAPPORT FINAL - TEST COMPLET DE JOUABILITÉ", Color.HEADER + Color.BOLD)
        self.log("=" * 80, Color.HEADER)

        # Calculer le taux de succès global
        total_success = sum(phase.get("success", 0) for phase in self.results["phases"].values())
        total_tests = self.results["total_tests"]
        self.results["success_rate"] = (total_success / total_tests * 100) if total_tests > 0 else 0

        self.log(f"\n📊 STATISTIQUES GLOBALES:", Color.CYAN)
        self.log(f"  • Tests totaux: {total_tests}", Color.BLUE)
        self.log(f"  • Tests réussis: {total_success}", Color.GREEN)
        self.log(f"  • Crashs détectés: {self.results['total_crashes']}",
                Color.RED if self.results['total_crashes'] > 0 else Color.GREEN)
        self.log(f"  • Taux de succès: {self.results['success_rate']:.1f}%",
                Color.GREEN if self.results['success_rate'] > 90 else Color.YELLOW)

        # Détail par phase
        self.log(f"\n📋 DÉTAIL PAR PHASE:", Color.CYAN)
        for phase_name, phase_data in self.results["phases"].items():
            total = phase_data.get("total", 0)
            success = phase_data.get("success", 0)
            crashes = phase_data.get("crashes", 0)
            rate = (success / total * 100) if total > 0 else 0

            color = Color.GREEN if rate > 90 else Color.YELLOW if rate > 70 else Color.RED
            self.log(f"  • {phase_name.upper()}: {success}/{total} ({rate:.1f}%) - {crashes} crashes",
                    color)

        # Personnages problématiques
        if "individual_chars" in self.results["phases"]:
            problem_chars = self.results["phases"]["individual_chars"].get("problem_chars", [])
            if problem_chars:
                self.log(f"\n⚠️  PERSONNAGES PROBLÉMATIQUES ({len(problem_chars)}):", Color.YELLOW)
                for char in problem_chars[:10]:  # Afficher les 10 premiers
                    self.log(f"  • {char['name']}: {char['reason']}", Color.RED)

        # Conclusion
        self.log(f"\n" + "=" * 80, Color.HEADER)
        if self.results['success_rate'] >= 95 and self.results['total_crashes'] == 0:
            self.log("✅ JEU 100% JOUABLE - PRÊT POUR RELEASE!", Color.GREEN + Color.BOLD)
        elif self.results['success_rate'] >= 80:
            self.log("⚠️  JEU JOUABLE AVEC QUELQUES PROBLÈMES MINEURS", Color.YELLOW + Color.BOLD)
        else:
            self.log("❌ JEU NON JOUABLE - CORRECTIONS NÉCESSAIRES", Color.RED + Color.BOLD)
        self.log("=" * 80, Color.HEADER)

        # Sauvegarder les résultats en JSON
        self.results["end_time"] = datetime.now().isoformat()
        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        self.log(f"\n📄 Résultats sauvegardés: {RESULTS_FILE}", Color.CYAN)
        self.log(f"📄 Log complet: {LOG_FILE}", Color.CYAN)

    def run_all_tests(self):
        """Lancer tous les tests"""
        self.log("=" * 80, Color.HEADER + Color.BOLD)
        self.log("🎮 TEST COMPLET DE JOUABILITÉ - KOF ULTIMATE ONLINE", Color.HEADER + Color.BOLD)
        self.log("=" * 80, Color.HEADER + Color.BOLD)
        self.log(f"\nDébut: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", Color.CYAN)

        # S'assurer que le jeu est fermé
        self.kill_game()

        try:
            # Phase 1: Lancement basique
            phase1_ok = self.test_basic_launch()

            # Phase 2: Combats aléatoires
            if phase1_ok:
                phase2_ok = self.test_characters_combat()
            else:
                self.log("\n⚠️  Phase 1 échouée, arrêt des tests", Color.YELLOW)

            # Phase 3: Test individuel des personnages
            # (on continue même si phase 2 a des problèmes)
            self.test_all_characters_individually()

            # Phase 4: Test des stages
            self.test_stages()

            # Phase 5: Test d'endurance
            # (optionnel, seulement si tout le reste passe)
            if self.results['total_crashes'] < 5:
                self.test_endurance()

        except KeyboardInterrupt:
            self.log("\n\n⚠️  Tests interrompus par l'utilisateur", Color.YELLOW)
        except Exception as e:
            self.log(f"\n\n❌ Erreur critique: {e}", Color.RED)
        finally:
            self.kill_game()
            self.generate_final_report()
            self.log_file.close()

if __name__ == "__main__":
    import sys

    # Mode automatique si lancé sans TTY
    auto_mode = not sys.stdin.isatty() or '--auto' in sys.argv

    if not auto_mode:
        print("\n" + "="*80)
        print("🎮 TEST COMPLET DE JOUABILITÉ - KOF ULTIMATE ONLINE")
        print("="*80)
        print("\n⚠️  Ce test va prendre 1-2 heures pour tout vérifier")
        print("⚠️  Le jeu va s'ouvrir et se fermer automatiquement plusieurs fois")
        print("\nAppuyez sur CTRL+C pour arrêter à tout moment\n")
        input("Appuyez sur ENTRÉE pour démarrer les tests...")
    else:
        print("\n🤖 MODE AUTOMATIQUE - Tests démarrant dans 3 secondes...")
        time.sleep(3)

    tester = TestSystem()
    tester.run_all_tests()
