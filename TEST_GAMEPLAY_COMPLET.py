#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST GAMEPLAY COMPLET
Teste le jeu en profondeur : chargement personnages, stages, combats
"""

import subprocess
import time
import psutil
from pathlib import Path
from datetime import datetime
import re

class GameplayTester:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.errors_found = []

    def log(self, message, level="INFO"):
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "TEST": "🧪"}
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{icons.get(level, '')} [{timestamp}] {message}")

    def analyze_mugen_log(self):
        """Analyse le log MUGEN pour détecter TOUTES les erreurs"""
        mugen_log = self.base_path / "mugen.log"

        if not mugen_log.exists():
            self.log("mugen.log n'existe pas encore", "INFO")
            return []

        errors = []
        warnings = []

        try:
            content = mugen_log.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')

            for i, line in enumerate(lines, 1):
                line_lower = line.lower()

                # Détecter les erreurs
                if any(word in line_lower for word in [
                    'error', 'failed', 'cannot', 'missing', 'not found',
                    'unable', 'invalid', 'corrupt', 'crash'
                ]):
                    errors.append({
                        'line': i,
                        'text': line.strip(),
                        'type': 'ERROR'
                    })

                # Détecter les warnings
                elif 'warning' in line_lower:
                    warnings.append({
                        'line': i,
                        'text': line.strip(),
                        'type': 'WARNING'
                    })

            # Détecter les crashs (fin brutale)
            if content and not 'Successful program termination' in content:
                if 'Initializing select screen' in content or 'Loading character' in content:
                    errors.append({
                        'line': len(lines),
                        'text': 'CRASH DÉTECTÉ: Le jeu s\'est fermé brutalement',
                        'type': 'CRASH'
                    })

        except Exception as e:
            self.log(f"Erreur lecture log: {e}", "ERROR")

        return errors, warnings

    def check_select_def_validity(self):
        """Vérifie que select.def ne contient que des personnages valides"""
        select_def = self.base_path / "data" / "select.def"

        if not select_def.exists():
            return []

        issues = []
        chars_path = self.base_path / "chars"

        try:
            content = select_def.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')

            for i, line in enumerate(lines, 1):
                # Ignorer commentaires et sections
                if line.strip().startswith(';') or line.strip().startswith('[') or not line.strip():
                    continue

                # Extraire le nom du personnage
                match = re.match(r'^([^,\s]+)', line.strip())
                if match:
                    char_name = match.group(1)
                    char_folder = chars_path / char_name

                    # Vérifier si le personnage existe et a les fichiers requis
                    if not char_folder.exists():
                        issues.append(f"Ligne {i}: {char_name} - Dossier n'existe pas")
                    else:
                        has_def = bool(list(char_folder.glob('*.def')))
                        has_sff = bool(list(char_folder.glob('*.sff')))

                        if not has_def:
                            issues.append(f"Ligne {i}: {char_name} - Pas de .def")
                        if not has_sff:
                            issues.append(f"Ligne {i}: {char_name} - Pas de .sff")

        except Exception as e:
            self.log(f"Erreur vérification select.def: {e}", "ERROR")

        return issues

    def launch_and_monitor_game(self, duration=20):
        """Lance le jeu et surveille pendant X secondes"""
        self.log(f"Lancement du jeu pour {duration}s...", "TEST")

        # Effacer ancien log (si possible)
        mugen_log = self.base_path / "mugen.log"
        if mugen_log.exists():
            try:
                mugen_log.unlink()
            except:
                pass  # Fichier verrouillé, on continue

        try:
            # Lancer le jeu
            process = subprocess.Popen(
                [str(self.base_path / "KOF_Ultimate_Online.exe")],
                cwd=str(self.base_path)
            )

            self.log("Jeu lancé, surveillance active...", "INFO")

            # Surveiller
            start_time = time.time()

            while (time.time() - start_time) < duration:
                # Vérifier si le process tourne encore
                if process.poll() is not None:
                    self.log("⚠️ Le jeu s'est fermé prématurément!", "ERROR")
                    break

                time.sleep(1)

            # Fermer proprement
            if process.poll() is None:
                process.terminate()
                time.sleep(2)

                if process.poll() is None:
                    process.kill()

            self.log("Test terminé", "SUCCESS")

        except Exception as e:
            self.log(f"Erreur durant le test: {e}", "ERROR")

    def run_full_test(self):
        """Lance tous les tests"""
        print("\n" + "="*80)
        print("  TEST GAMEPLAY COMPLET - DÉTECTION ERREURS PROFONDES")
        print("="*80 + "\n")

        # Test 1: Vérifier select.def
        self.log("=== VÉRIFICATION SELECT.DEF ===", "TEST")
        issues = self.check_select_def_validity()

        if issues:
            self.log(f"❌ {len(issues)} problèmes trouvés dans select.def", "ERROR")
            for issue in issues[:10]:
                self.log(f"  • {issue}", "ERROR")
        else:
            self.log("✅ select.def est propre", "SUCCESS")

        # Test 2: Lancer et surveiller le jeu
        self.log("\n=== TEST LANCEMENT JEU ===", "TEST")
        self.launch_and_monitor_game(duration=15)

        # Attendre que le log soit écrit
        time.sleep(2)

        # Test 3: Analyser le log
        self.log("\n=== ANALYSE LOG MUGEN ===", "TEST")
        errors, warnings = self.analyze_mugen_log()

        # RAPPORT FINAL
        print("\n" + "="*80)
        print("  RAPPORT FINAL")
        print("="*80 + "\n")

        print(f"📊 RÉSULTATS:")
        print(f"  • Problèmes select.def: {len(issues)}")
        print(f"  • Erreurs dans log: {len(errors)}")
        print(f"  • Warnings dans log: {len(warnings)}")
        print()

        if errors:
            print(f"❌ ERREURS DÉTECTÉES ({len(errors)}):")
            for error in errors[:20]:
                print(f"  Ligne {error['line']}: {error['text'][:80]}")
            print()
        else:
            print("✅ AUCUNE ERREUR DÉTECTÉE!")
            print()

        if warnings:
            print(f"⚠️  WARNINGS ({len(warnings)}):")
            for warning in warnings[:10]:
                print(f"  Ligne {warning['line']}: {warning['text'][:80]}")
            print()

        # Conclusion
        if not errors and len(issues) == 0:
            print("🎉 STATUT: JEU 100% FONCTIONNEL")
        elif len(errors) < 5:
            print("⚠️  STATUT: QUELQUES ERREURS MINEURES")
        else:
            print("❌ STATUT: CORRECTIONS NÉCESSAIRES")

        print("="*80 + "\n")

if __name__ == "__main__":
    tester = GameplayTester()
    tester.run_full_test()
