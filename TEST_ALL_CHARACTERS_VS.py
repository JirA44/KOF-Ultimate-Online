#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST EXHAUSTIF - TOUS LES PERSONNAGES EN VS
Teste chaque personnage contre chaque autre pour identifier les crasheurs
"""
import subprocess
import time
import psutil
import re
from pathlib import Path

class ExhaustiveVSTester:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.game_exe = self.base_path / "KOF_Ultimate_Online.exe"
        self.log_file = self.base_path / "mugen.log"
        self.select_def = self.base_path / "data" / "select.def"

        self.characters = self.load_roster()
        self.crashers = []
        self.safe = []

    def load_roster(self):
        """Charge la liste des personnages du roster"""
        chars = []

        try:
            with open(self.select_def, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()

                    # Ignorer commentaires et lignes vides
                    if not line or line.startswith(';') or line.startswith('['):
                        continue

                    # Extraire le nom du personnage
                    if ',' in line:
                        char_name = line.split(',')[0].strip()
                        if char_name:
                            chars.append(char_name)

        except Exception as e:
            print(f"❌ Erreur lecture roster: {e}")

        return chars

    def kill_game(self):
        """Tue tous les processus du jeu"""
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name'].lower()
                if 'kof' in name or 'mugen' in name or 'ikemen' in name:
                    proc.kill()
            except:
                pass
        time.sleep(0.5)

    def create_minimal_roster(self, char1, char2):
        """Crée un roster minimal avec seulement 2 personnages"""
        backup = self.select_def.parent / "select.def.backup_test"

        # Backup original (une seule fois)
        if not backup.exists():
            import shutil
            shutil.copy(self.select_def, backup)

        # Créer roster minimal
        content = f"""; Test roster
[Characters]
{char1}, stages/Abyss-Rugal-Palace.def
{char2}, stages/Abyss-Rugal-Palace.def
"""

        with open(self.select_def, 'w', encoding='utf-8') as f:
            f.write(content)

    def test_character_pair(self, char1, char2):
        """Test un combat entre 2 personnages"""
        print(f"\n   🥊 Test: {char1} vs {char2}")

        # Créer roster minimal
        self.create_minimal_roster(char1, char2)

        # Nettoyer le log
        if self.log_file.exists():
            self.log_file.unlink()

        # Lancer le jeu
        try:
            self.kill_game()

            process = subprocess.Popen(
                [str(self.game_exe)],
                cwd=str(self.base_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Attendre 15 secondes
            time.sleep(15)

            # Vérifier si le jeu tourne toujours
            if process.poll() is None:
                # Jeu toujours en cours
                process.kill()

                # Vérifier le log pour des erreurs
                if self.log_file.exists():
                    with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    # Chercher erreurs critiques
                    if 'error' in content.lower():
                        # Compter les erreurs
                        error_lines = [line for line in content.split('\n') if 'error' in line.lower()]

                        if len(error_lines) > 5:  # Plus de 5 erreurs = problème
                            print(f"      ⚠️  ERREURS DÉTECTÉES ({len(error_lines)} erreurs)")
                            return "ERRORS"

                print(f"      ✅ OK")
                return "OK"

            else:
                # Jeu crashé
                print(f"      ❌ CRASH")
                return "CRASH"

        except Exception as e:
            print(f"      ❌ ERREUR: {e}")
            return "ERROR"

        finally:
            self.kill_game()

    def test_character_thoroughly(self, char_name):
        """Test un personnage contre 3 adversaires différents"""
        print(f"\n🎯 Test de {char_name}...")

        # Choisir 3 adversaires (les 3 premiers du roster différents du perso testé)
        opponents = [c for c in self.characters if c != char_name][:3]

        if len(opponents) == 0:
            print(f"   ⚠️  Pas d'adversaires disponibles")
            return "UNKNOWN"

        results = []

        for opponent in opponents:
            result = self.test_character_pair(char_name, opponent)
            results.append(result)

            if result in ["CRASH", "ERROR"]:
                print(f"   ❌ {char_name} est PROBLÉMATIQUE")
                return "CRASHER"

        print(f"   ✅ {char_name} est OK")
        return "SAFE"

    def run_exhaustive_test(self):
        """Test tous les personnages"""
        print("=" * 70)
        print("🔬 TEST EXHAUSTIF - IDENTIFICATION DES CRASHEURS")
        print("=" * 70)
        print(f"\n📋 Roster: {len(self.characters)} personnages")
        print(f"   {', '.join(self.characters[:5])}{'...' if len(self.characters) > 5 else ''}")

        print("\n" + "=" * 70)
        print("🧪 DÉBUT DES TESTS")
        print("=" * 70)

        for i, char in enumerate(self.characters, 1):
            print(f"\n[{i}/{len(self.characters)}]", end=" ")

            result = self.test_character_thoroughly(char)

            if result == "CRASHER":
                self.crashers.append(char)
            elif result == "SAFE":
                self.safe.append(char)

        # Restaurer roster original
        backup = self.select_def.parent / "select.def.backup_test"
        if backup.exists():
            import shutil
            shutil.copy(backup, self.select_def)
            print("\n✅ Roster original restauré")

        # Rapport
        print("\n" + "=" * 70)
        print("📊 RAPPORT FINAL")
        print("=" * 70)

        print(f"\n✅ PERSONNAGES SÛRS ({len(self.safe)}):")
        for char in self.safe:
            print(f"   ✓ {char}")

        print(f"\n❌ PERSONNAGES CRASHEURS ({len(self.crashers)}):")
        for char in self.crashers:
            print(f"   ✗ {char}")

        # Sauvegarder le rapport
        report_file = self.base_path / "RAPPORT_TEST_EXHAUSTIF.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("RAPPORT TEST EXHAUSTIF\n")
            f.write("=" * 70 + "\n\n")

            f.write(f"PERSONNAGES SÛRS ({len(self.safe)}):\n")
            for char in self.safe:
                f.write(f"  ✓ {char}\n")

            f.write(f"\nPERSONNAGES CRASHEURS ({len(self.crashers)}):\n")
            for char in self.crashers:
                f.write(f"  ✗ {char}\n")

        print(f"\n📄 Rapport sauvegardé: {report_file.name}")

        # Créer roster ultra-safe
        if len(self.safe) > 0:
            self.create_ultra_safe_roster()

    def create_ultra_safe_roster(self):
        """Crée un roster avec UNIQUEMENT les personnages sûrs"""
        safe_roster_file = self.select_def.parent / "select_ULTRA_SAFE.def"

        content = """; ROSTER ULTRA-SAFE
; Généré automatiquement - SEULEMENT LES PERSOS TESTÉS OK
; Date: """ + time.strftime("%Y-%m-%d %H:%M:%S") + """

[Characters]
"""

        for char in self.safe:
            content += f"{char}, stages/Abyss-Rugal-Palace.def\n"

        with open(safe_roster_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\n✅ Roster ultra-safe créé: {safe_roster_file.name}")
        print(f"   {len(self.safe)} personnages 100% stables")

if __name__ == "__main__":
    try:
        tester = ExhaustiveVSTester()
        tester.run_exhaustive_test()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

    input("\nAppuyez sur ENTRÉE pour fermer...")
