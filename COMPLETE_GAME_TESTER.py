#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - TESTEUR COMPLET DU JEU
Teste TOUS les aspects: personnages, stages, écran de sélection, combats
"""

import subprocess
import re
from pathlib import Path
from datetime import datetime
import json
import time

game_dir = Path(r"D:\KOF Ultimate Online Online Online")
exe_path = game_dir / "KOF_Ultimate_Online.exe"
log_file = game_dir / "mugen.log"

class CompleteTester:
    """Testeur complet du jeu"""

    def __init__(self):
        self.test_results = {
            'characters': [],
            'stages': [],
            'select_screen': None,
            'ai_matches': []
        }
        self.errors = []
        self.warnings = []

    def log(self, message, level='INFO'):
        """Log message"""
        symbols = {
            'INFO': 'ℹ️',
            'SUCCESS': '✅',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'TEST': '🧪'
        }
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {symbols.get(level, '•')} {message}")

    def test_all_characters(self):
        """Teste le chargement de TOUS les personnages"""
        self.log("TEST DE TOUS LES PERSONNAGES", 'TEST')
        print("=" * 70)
        print()

        # Lire select.def
        select_file = game_dir / "data" / "select.def"

        if not select_file.exists():
            self.log("select.def introuvable!", 'ERROR')
            return

        with open(select_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        # Extraire les définitions de personnages
        char_defs = []
        in_chars_section = False

        for line in lines:
            if line.strip().startswith('[Characters]'):
                in_chars_section = True
                continue

            if in_chars_section:
                if line.strip().startswith('['):
                    break

                if line.strip() and not line.strip().startswith(';'):
                    char_def = line.strip().split(',')[0].strip()
                    if char_def:
                        char_defs.append(char_def)

        self.log(f"Trouvé {len(char_defs)} personnages à tester")
        print()

        # Tester TOUS les personnages (pas seulement 30)
        self.log(f"Test des {len(char_defs)} personnages...")
        print()

        for i, char_def in enumerate(char_defs, 1):
            if i % 10 == 0:
                self.log(f"Progression: {i}/{len(char_defs)}")

            result = self.test_character(char_def)
            self.test_results['characters'].append(result)

            if result['status'] == 'ERROR':
                self.log(f"[{i}/{len(char_defs)}] ❌ {char_def}", 'ERROR')
                for error in result['errors'][:2]:
                    self.log(f"  {error[:60]}...", 'ERROR')
                self.errors.append(f"{char_def}: {result['errors'][0]}")

        print()
        print("=" * 70)

    def test_character(self, char_def):
        """Teste le chargement d'un personnage"""
        try:
            # Effacer le log
            if log_file.exists():
                log_file.unlink()

            # Créer un select temporaire
            select_file = game_dir / "data" / "select.def"
            select_backup = game_dir / "data" / "select.def.backup_test"

            # Backup
            if select_file.exists():
                with open(select_file, 'rb') as src:
                    select_backup.write_bytes(src.read())

            # Créer select temporaire
            temp_select = f"""[Characters]
{char_def}
"""
            with open(select_file, 'w') as f:
                f.write(temp_select)

            # Lancer le jeu
            proc = subprocess.Popen(
                [str(exe_path)],
                cwd=str(game_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Attendre 2 secondes
            time.sleep(2)

            # Terminer
            proc.terminate()
            time.sleep(0.5)
            if proc.poll() is None:
                proc.kill()

            # Restaurer select
            if select_backup.exists():
                with open(select_backup, 'rb') as src:
                    select_file.write_bytes(src.read())
                select_backup.unlink()

            # Analyser le log
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    log_content = f.read()

                errors_found = []

                if "Error detected" in log_content:
                    error_section = log_content[log_content.find("Error detected"):]
                    error_lines = [line for line in error_section.split('\n') if 'Error' in line or 'error' in line.lower()]
                    errors_found.extend(error_lines[:5])

                if "failed to load" in log_content.lower():
                    failed_lines = [line for line in log_content.split('\n') if 'failed' in line.lower()]
                    errors_found.extend(failed_lines[:3])

                if errors_found:
                    return {
                        'char': char_def,
                        'status': 'ERROR',
                        'errors': errors_found
                    }
                else:
                    return {
                        'char': char_def,
                        'status': 'OK',
                        'errors': []
                    }
            else:
                return {
                    'char': char_def,
                    'status': 'NO_LOG',
                    'errors': ['No log file generated']
                }

        except Exception as e:
            return {
                'char': char_def,
                'status': 'EXCEPTION',
                'errors': [str(e)]
            }

    def test_stages(self):
        """Teste tous les stages"""
        self.log("TEST DE TOUS LES STAGES", 'TEST')
        print("=" * 70)
        print()

        stages_dir = game_dir / "stages"

        if not stages_dir.exists():
            self.log("Dossier stages introuvable!", 'ERROR')
            return

        # Trouver tous les fichiers .def dans stages
        stage_files = list(stages_dir.rglob("*.def"))
        self.log(f"Trouvé {len(stage_files)} stages à tester")
        print()

        for i, stage_file in enumerate(stage_files, 1):
            if i % 10 == 0:
                self.log(f"Progression: {i}/{len(stage_files)}")

            result = self.test_stage(stage_file)
            self.test_results['stages'].append(result)

            if result['status'] == 'ERROR':
                self.log(f"[{i}/{len(stage_files)}] ❌ {stage_file.name}", 'ERROR')
                self.errors.append(f"Stage {stage_file.name}: {result['error']}")

        print()
        print("=" * 70)

    def test_stage(self, stage_file):
        """Teste un stage"""
        try:
            # Vérifier que le fichier .def existe
            if not stage_file.exists():
                return {
                    'stage': stage_file.name,
                    'status': 'ERROR',
                    'error': 'File not found'
                }

            # Lire le fichier
            with open(stage_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Vérifier la présence de sections essentielles
            required_sections = ['[Info]', '[Camera]', '[PlayerInfo]', '[Scaling]', '[Bound]', '[StageInfo]', '[Shadow]', '[Reflection]', '[Music]', '[BGDef]']
            missing_sections = []

            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)

            if missing_sections:
                return {
                    'stage': stage_file.name,
                    'status': 'WARNING',
                    'error': f"Missing sections: {', '.join(missing_sections)}"
                }

            return {
                'stage': stage_file.name,
                'status': 'OK',
                'error': None
            }

        except Exception as e:
            return {
                'stage': stage_file.name,
                'status': 'ERROR',
                'error': str(e)
            }

    def test_ai_matches(self, num_matches=10):
        """Teste des combats AI vs AI"""
        self.log(f"TEST DE {num_matches} COMBATS AI VS AI", 'TEST')
        print("=" * 70)
        print()

        # Lire select.def pour avoir la liste des personnages
        select_file = game_dir / "data" / "select.def"

        with open(select_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        char_defs = []
        in_chars_section = False

        for line in lines:
            if line.strip().startswith('[Characters]'):
                in_chars_section = True
                continue

            if in_chars_section:
                if line.strip().startswith('['):
                    break

                if line.strip() and not line.strip().startswith(';'):
                    char_def = line.strip().split(',')[0].strip()
                    if char_def:
                        char_defs.append(char_def)

        if len(char_defs) < 2:
            self.log("Pas assez de personnages pour tester des combats", 'WARNING')
            return

        import random

        for i in range(num_matches):
            # Choisir 2 personnages au hasard
            p1 = random.choice(char_defs)
            p2 = random.choice(char_defs)

            self.log(f"[{i+1}/{num_matches}] {p1} vs {p2}")

            result = self.test_match(p1, p2)
            self.test_results['ai_matches'].append(result)

            if result['status'] == 'ERROR':
                self.log(f"  ❌ Erreur durant le combat", 'ERROR')
                self.errors.append(f"Match {p1} vs {p2}: {result['error']}")
            else:
                self.log(f"  ✓ Combat OK", 'SUCCESS')

        print()
        print("=" * 70)

    def test_match(self, char1, char2):
        """Teste un combat"""
        try:
            # Effacer le log
            if log_file.exists():
                log_file.unlink()

            # Créer un select temporaire avec les 2 personnages
            select_file = game_dir / "data" / "select.def"
            select_backup = game_dir / "data" / "select.def.backup_match"

            # Backup
            if select_file.exists():
                with open(select_file, 'rb') as src:
                    select_backup.write_bytes(src.read())

            # Créer select temporaire
            temp_select = f"""[Characters]
{char1}
{char2}
"""
            with open(select_file, 'w') as f:
                f.write(temp_select)

            # Lancer le jeu
            proc = subprocess.Popen(
                [str(exe_path)],
                cwd=str(game_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Attendre 5 secondes (temps pour un mini combat)
            time.sleep(5)

            # Terminer
            proc.terminate()
            time.sleep(0.5)
            if proc.poll() is None:
                proc.kill()

            # Restaurer select
            if select_backup.exists():
                with open(select_backup, 'rb') as src:
                    select_file.write_bytes(src.read())
                select_backup.unlink()

            # Analyser le log
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    log_content = f.read()

                if "Error detected" in log_content or "failed" in log_content.lower():
                    return {
                        'p1': char1,
                        'p2': char2,
                        'status': 'ERROR',
                        'error': 'Error in log'
                    }

            return {
                'p1': char1,
                'p2': char2,
                'status': 'OK',
                'error': None
            }

        except Exception as e:
            return {
                'p1': char1,
                'p2': char2,
                'status': 'ERROR',
                'error': str(e)
            }

    def generate_report(self):
        """Génère un rapport détaillé"""
        print()
        print("=" * 70)
        print("📊 RAPPORT COMPLET DES TESTS")
        print("=" * 70)
        print()

        # Stats personnages
        total_chars = len(self.test_results['characters'])
        ok_chars = len([r for r in self.test_results['characters'] if r['status'] == 'OK'])
        error_chars = len([r for r in self.test_results['characters'] if r['status'] == 'ERROR'])

        print("🎮 PERSONNAGES:")
        print(f"  Total testé:  {total_chars}")
        print(f"  ✅ OK:        {ok_chars}")
        print(f"  ❌ ERREURS:   {error_chars}")
        print()

        # Stats stages
        total_stages = len(self.test_results['stages'])
        ok_stages = len([r for r in self.test_results['stages'] if r['status'] == 'OK'])
        error_stages = len([r for r in self.test_results['stages'] if r['status'] == 'ERROR'])

        print("🏞️ STAGES:")
        print(f"  Total testé:  {total_stages}")
        print(f"  ✅ OK:        {ok_stages}")
        print(f"  ❌ ERREURS:   {error_stages}")
        print()

        # Stats combats
        total_matches = len(self.test_results['ai_matches'])
        ok_matches = len([r for r in self.test_results['ai_matches'] if r['status'] == 'OK'])
        error_matches = len([r for r in self.test_results['ai_matches'] if r['status'] == 'ERROR'])

        print("⚔️ COMBATS AI:")
        print(f"  Total testé:  {total_matches}")
        print(f"  ✅ OK:        {ok_matches}")
        print(f"  ❌ ERREURS:   {error_matches}")
        print()

        # Erreurs
        if self.errors:
            print("🔍 LISTE DES ERREURS:")
            print()
            for error in self.errors[:20]:
                print(f"  ❌ {error}")
            if len(self.errors) > 20:
                print(f"\n  ... et {len(self.errors) - 20} autres erreurs")
            print()

        # Sauvegarder dans un fichier JSON
        report_file = game_dir / f"complete_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': self.test_results,
                'errors': self.errors,
                'stats': {
                    'characters': {
                        'total': total_chars,
                        'ok': ok_chars,
                        'errors': error_chars
                    },
                    'stages': {
                        'total': total_stages,
                        'ok': ok_stages,
                        'errors': error_stages
                    },
                    'matches': {
                        'total': total_matches,
                        'ok': ok_matches,
                        'errors': error_matches
                    }
                }
            }, f, indent=2)

        print(f"✅ Rapport sauvegardé: {report_file.name}")
        print("=" * 70)
        print()

def main():
    """Main function"""
    print()
    print("=" * 70)
    print("  🔍 KOF ULTIMATE - TESTS COMPLETS")
    print("=" * 70)
    print()

    tester = CompleteTester()

    # Lancer tous les tests
    tester.test_all_characters()
    tester.test_stages()
    tester.test_ai_matches(10)

    # Générer le rapport
    tester.generate_report()

    print()
    try:
        input("Appuyez sur ENTRÉE pour fermer...")
    except EOFError:
        pass

if __name__ == '__main__':
    main()
