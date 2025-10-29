#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE ONLINE - Détecteur Automatique de Bugs
Teste tous les personnages, détecte les bugs, et génère un rapport
"""

import os
import sys
import time
import json
import subprocess
import psutil
from pathlib import Path
from datetime import datetime
import threading

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class BugDetector:
    """Détecteur automatique de bugs Mugen"""

    def __init__(self):
        self.game_dir = Path("D:/KOF Ultimate Online")
        self.chars_dir = self.game_dir / "chars"
        self.select_def = self.game_dir / "data" / "select.def"
        self.mugen_log = self.game_dir / "mugen.log"
        self.exe_path = self.game_dir / "KOF_Ultimate_Online.exe"

        self.bugs_found = []
        self.tested_chars = []
        self.stable_chars = []
        self.problematic_chars = []

    def print_header(self):
        """Affiche l'en-tête"""
        print(f"\n{Colors.CYAN}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}  KOF ULTIMATE - DÉTECTEUR AUTOMATIQUE DE BUGS{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")

    def scan_characters(self):
        """Scanne tous les personnages disponibles"""
        print(f"{Colors.YELLOW}[SCAN] Recherche des personnages...{Colors.RESET}")

        chars = []
        for char_dir in self.chars_dir.iterdir():
            if char_dir.is_dir():
                # Chercher le fichier .def principal
                def_files = list(char_dir.glob("*.def"))
                if def_files:
                    main_def = def_files[0]
                    chars.append({
                        "name": char_dir.name,
                        "path": f"chars/{char_dir.name}/{main_def.name}",
                        "dir": char_dir
                    })

        print(f"{Colors.GREEN}[SCAN] {len(chars)} personnages trouvés{Colors.RESET}\n")
        return chars

    def test_character(self, char_info):
        """Teste un personnage spécifique"""
        char_name = char_info["name"]
        print(f"{Colors.CYAN}[TEST] Test de {char_name}...{Colors.RESET}")

        # Créer un select.def temporaire avec ce personnage
        self._create_test_select_def(char_info["path"])

        # Supprimer l'ancien log
        if self.mugen_log.exists():
            try:
                os.remove(self.mugen_log)
            except:
                pass

        # Lancer le jeu
        try:
            process = subprocess.Popen(
                [str(self.exe_path)],
                cwd=str(self.game_dir),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # Attendre 10 secondes
            time.sleep(10)

            # Vérifier si le processus est toujours en cours
            is_running = psutil.pid_exists(process.pid)

            # Arrêter le jeu
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                    process.wait()
                except:
                    pass

            # Analyser le log
            bugs = self._analyze_log(char_name)

            if bugs:
                print(f"{Colors.RED}[BUG] {char_name}: {len(bugs)} bug(s) détecté(s){Colors.RESET}")
                self.problematic_chars.append(char_name)
                self.bugs_found.extend(bugs)
            else:
                print(f"{Colors.GREEN}[OK] {char_name}: Aucun bug détecté{Colors.RESET}")
                self.stable_chars.append(char_name)

            self.tested_chars.append(char_name)
            return len(bugs) == 0

        except Exception as e:
            print(f"{Colors.RED}[ERREUR] {char_name}: {str(e)}{Colors.RESET}")
            self.problematic_chars.append(char_name)
            return False

    def _create_test_select_def(self, char_path):
        """Crée un select.def temporaire pour tester un personnage"""
        content = f"""; Test select.def
[Characters]
{char_path}
{char_path}

[ExtraStages]
stages/Abyss-Rugal-Palace.def

[Options]
arcade.rematches = 0
team.loseondraw = 1
"""
        with open(self.select_def, 'w', encoding='utf-8') as f:
            f.write(content)

    def _analyze_log(self, char_name):
        """Analyse le log pour détecter les bugs"""
        if not self.mugen_log.exists():
            return [{"char": char_name, "type": "NO_LOG", "message": "Log non créé"}]

        bugs = []

        with open(self.mugen_log, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')

        # Vérifier si le personnage a échoué à charger
        if "failed to load" in content.lower():
            bugs.append({
                "char": char_name,
                "type": "LOAD_FAILED",
                "message": "Échec de chargement du personnage"
            })

        # Vérifier les erreurs de fichiers manquants
        if "cannot open" in content.lower() or "not found" in content.lower():
            bugs.append({
                "char": char_name,
                "type": "FILE_MISSING",
                "message": "Fichier manquant"
            })

        # Vérifier les temps de chargement excessifs
        for line in lines:
            if "Load time:" in line and "ms" in line:
                try:
                    time_str = line.split("Load time:")[1].split("ms")[0].strip()
                    load_time = float(time_str)
                    if load_time > 5000:  # Plus de 5 secondes
                        bugs.append({
                            "char": char_name,
                            "type": "SLOW_LOAD",
                            "message": f"Chargement lent: {load_time}ms"
                        })
                except:
                    pass

        # Vérifier les expressions excessives
        for line in lines:
            if "expressions" in line.lower():
                try:
                    if any(str(x) in line for x in range(20000, 100000)):
                        bugs.append({
                            "char": char_name,
                            "type": "TOO_COMPLEX",
                            "message": "Trop d'expressions (>20000)"
                        })
                except:
                    pass

        return bugs

    def run_full_test(self):
        """Exécute un test complet de tous les personnages"""
        self.print_header()

        # Scanner les personnages
        chars = self.scan_characters()

        if not chars:
            print(f"{Colors.RED}[ERREUR] Aucun personnage trouvé{Colors.RESET}")
            return

        # Tester chaque personnage
        print(f"{Colors.YELLOW}[TEST] Test de {len(chars)} personnages...{Colors.RESET}\n")

        for i, char in enumerate(chars, 1):
            print(f"\n{Colors.BOLD}[{i}/{len(chars)}]{Colors.RESET} ", end="")
            self.test_character(char)
            time.sleep(2)  # Pause entre les tests

        # Générer le rapport
        self.generate_report()

    def generate_report(self):
        """Génère un rapport détaillé"""
        print(f"\n{Colors.CYAN}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}  RAPPORT DE TEST{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")

        print(f"{Colors.WHITE}Personnages testés: {len(self.tested_chars)}{Colors.RESET}")
        print(f"{Colors.GREEN}Personnages stables: {len(self.stable_chars)}{Colors.RESET}")
        print(f"{Colors.RED}Personnages problématiques: {len(self.problematic_chars)}{Colors.RESET}")
        print(f"{Colors.YELLOW}Bugs détectés: {len(self.bugs_found)}{Colors.RESET}\n")

        if self.stable_chars:
            print(f"{Colors.GREEN}{'='*70}{Colors.RESET}")
            print(f"{Colors.GREEN}PERSONNAGES STABLES (Recommandés):{Colors.RESET}\n")
            for char in self.stable_chars:
                print(f"  {Colors.GREEN}✓{Colors.RESET} {char}")
            print()

        if self.problematic_chars:
            print(f"{Colors.RED}{'='*70}{Colors.RESET}")
            print(f"{Colors.RED}PERSONNAGES PROBLÉMATIQUES (À éviter):{Colors.RESET}\n")
            for char in self.problematic_chars:
                print(f"  {Colors.RED}✗{Colors.RESET} {char}")
            print()

        # Sauvegarder le rapport JSON
        report_data = {
            "date": datetime.now().isoformat(),
            "tested": len(self.tested_chars),
            "stable": self.stable_chars,
            "problematic": self.problematic_chars,
            "bugs": self.bugs_found
        }

        report_file = self.game_dir / "bug_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        print(f"{Colors.CYAN}Rapport sauvegardé: {report_file}{Colors.RESET}")

        # Générer un select.def optimal
        self.generate_optimal_select_def()

    def generate_optimal_select_def(self):
        """Génère un select.def avec uniquement les personnages stables"""
        if not self.stable_chars:
            print(f"\n{Colors.RED}[ERREUR] Aucun personnage stable trouvé !{Colors.RESET}")
            return

        print(f"\n{Colors.YELLOW}[GÉNÉRATION] Création du select.def optimal...{Colors.RESET}")

        # Créer le contenu
        lines = [
            "; IKEMEN GO Select.def - OPTIMAL",
            "; Généré automatiquement par AUTO_BUG_DETECTOR",
            f"; Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"; {len(self.stable_chars)} personnages stables",
            ";",
            "",
            "[Characters]",
            ";"
        ]

        # Ajouter les personnages stables
        for char in self.stable_chars:
            # Trouver le .def du personnage
            char_dir = self.chars_dir / char
            def_files = list(char_dir.glob("*.def"))
            if def_files:
                main_def = def_files[0]
                char_path = f"chars/{char}/{main_def.name}"
                lines.append(f"{char_path}")

        lines.extend([
            "",
            "[ExtraStages]",
            ";------------------------------",
            "",
            "stages/Abyss-Rugal-Palace.def",
            "",
            "[Options]",
            ";------------------------------",
            "",
            "arcade.rematches = 0",
            "team.loseondraw = 1",
            ""
        ])

        # Sauvegarder
        select_optimal = self.game_dir / "data" / "select_optimal.def"
        with open(select_optimal, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print(f"{Colors.GREEN}[OK] select_optimal.def créé avec {len(self.stable_chars)} personnages{Colors.RESET}")
        print(f"{Colors.CYAN}Fichier: {select_optimal}{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Pour l'utiliser:{Colors.RESET}")
        print(f"  copy {select_optimal} {self.select_def}")

if __name__ == "__main__":
    detector = BugDetector()

    try:
        detector.run_full_test()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[ARRÊT] Test interrompu par l'utilisateur{Colors.RESET}")
    except Exception as e:
        print(f"\n\n{Colors.RED}[ERREUR] {str(e)}{Colors.RESET}")
        import traceback
        traceback.print_exc()
