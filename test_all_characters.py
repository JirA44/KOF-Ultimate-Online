#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - Testeur Automatique de Personnages
Teste CHAQUE personnage individuellement pour identifier ceux qui causent des crashes
"""

import subprocess
import time
import re
from pathlib import Path
from datetime import datetime
import shutil

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class CharacterTester:
    def __init__(self, game_dir):
        self.game_dir = Path(game_dir)
        self.select_def = self.game_dir / "data" / "select.def"
        self.select_backup = self.game_dir / "data" / "select.def.backup_before_test"
        self.mugen_log = self.game_dir / "mugen.log"

        self.characters = []
        self.results = {
            'ok': [],
            'failed': [],
            'skipped': []
        }

    def backup_select_def(self):
        """Sauvegarde le select.def original"""
        print(f"{Colors.CYAN}💾 Sauvegarde de select.def...{Colors.RESET}")
        shutil.copy2(self.select_def, self.select_backup)
        print(f"{Colors.GREEN}  ✓ Backup créé: {self.select_backup.name}{Colors.RESET}")

    def restore_select_def(self):
        """Restaure le select.def original"""
        if self.select_backup.exists():
            shutil.copy2(self.select_backup, self.select_def)
            print(f"{Colors.GREEN}✓ select.def restauré{Colors.RESET}")

    def parse_select_def(self):
        """Parse le select.def pour extraire la liste des personnages"""
        print(f"\n{Colors.CYAN}📋 Lecture de select.def...{Colors.RESET}")

        with open(self.select_def, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        in_characters_section = False

        for line in lines:
            line = line.strip()

            # Détecter la section [Characters]
            if line == "[Characters]":
                in_characters_section = True
                continue

            # Arrêter à la prochaine section
            if line.startswith("[") and line != "[Characters]":
                break

            # Ignorer les lignes vides, commentaires, et "x"
            if not in_characters_section:
                continue
            if not line or line.startswith(";") or line == "x":
                continue

            # C'est un personnage valide
            self.characters.append(line)

        print(f"{Colors.GREEN}  ✓ {len(self.characters)} personnages trouvés{Colors.RESET}")
        return len(self.characters)

    def create_test_select_def(self, char_name):
        """Crée un select.def temporaire avec UN SEUL personnage"""
        content = f""";Test automatique - 1 personnage
[Characters]
{char_name}

[ExtraStages]

[Options]
arcade.maxmatches = 1,1,1,0,0,0,0,0,0,0
team.maxmatches = 1,1,1,1,0,0,0,0,0,0
"""

        with open(self.select_def, 'w', encoding='utf-8') as f:
            f.write(content)

    def clear_mugen_log(self):
        """Efface le mugen.log"""
        if self.mugen_log.exists():
            self.mugen_log.unlink()

    def test_character(self, char_name):
        """Teste un personnage"""
        print(f"\n{Colors.CYAN}Testing: {char_name}{Colors.RESET}", end=" ")

        # Vérifier que le dossier existe
        char_path = self.game_dir / "chars" / char_name
        if not char_path.exists():
            print(f"{Colors.RED}✗ (Dossier introuvable){Colors.RESET}")
            self.results['skipped'].append({
                'name': char_name,
                'reason': 'Dossier introuvable'
            })
            return False

        # Créer select.def de test
        self.create_test_select_def(char_name)

        # Effacer ancien log
        self.clear_mugen_log()

        # Lancer le jeu
        exe_path = self.game_dir / "KOF_Ultimate_Online.exe"
        process = None

        try:
            process = subprocess.Popen(
                [str(exe_path)],
                cwd=str(self.game_dir),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # Attendre 6 secondes (assez pour charger le personnage)
            time.sleep(6)

            # Fermer le jeu
            try:
                process.terminate()
                process.wait(timeout=3)
            except:
                try:
                    process.kill()
                except:
                    pass

            # Analyser le log
            success, errors = self.analyze_log(char_name)

            if success:
                print(f"{Colors.GREEN}✓{Colors.RESET}")
                self.results['ok'].append(char_name)
                return True
            else:
                print(f"{Colors.RED}✗{Colors.RESET}")
                print(f"    {Colors.YELLOW}Erreurs: {', '.join(errors)}{Colors.RESET}")
                self.results['failed'].append({
                    'name': char_name,
                    'errors': errors
                })
                return False

        except Exception as e:
            print(f"{Colors.RED}✗ (Exception: {e}){Colors.RESET}")

            if process:
                try:
                    process.kill()
                except:
                    pass

            self.results['failed'].append({
                'name': char_name,
                'errors': [str(e)]
            })
            return False

    def analyze_log(self, char_name):
        """Analyse le mugen.log pour détecter les erreurs"""
        if not self.mugen_log.exists():
            return False, ["Log introuvable"]

        with open(self.mugen_log, 'r', encoding='utf-8', errors='ignore') as f:
            log_content = f.read()

        errors = []

        # Patterns d'erreur
        error_patterns = [
            (r'failed to load', 'Failed to load'),
            (r'Error loading', 'Error loading'),
            (r'Error reading character', 'Error reading character'),
            (r'Error in.*\.air', 'Error in .air file'),
            (r'Error in.*\.cns', 'Error in .cns file'),
            (r'Error in.*\.def', 'Error in .def file'),
            (r'Cannot open file', 'Cannot open file'),
        ]

        for pattern, error_msg in error_patterns:
            if re.search(pattern, log_content, re.IGNORECASE):
                errors.append(error_msg)

        # Si aucune erreur détectée
        if not errors:
            return True, []

        return False, errors

    def generate_safe_select_def(self):
        """Génère un nouveau select.def avec SEULEMENT les personnages OK"""
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}📝 Génération de select_safe.def...{Colors.RESET}")

        # Lire l'original pour garder la structure
        with open(self.select_backup, 'r', encoding='utf-8', errors='ignore') as f:
            original_lines = f.readlines()

        safe_lines = []
        in_characters_section = False

        for line in original_lines:
            stripped = line.strip()

            # Copier les en-têtes
            if stripped == "[Characters]":
                in_characters_section = True
                safe_lines.append(line)
                continue

            # Fin de la section Characters
            if stripped.startswith("[") and stripped != "[Characters]":
                in_characters_section = False
                safe_lines.append(line)
                continue

            # Dans la section Characters
            if in_characters_section:
                # Garder les "x" et commentaires
                if stripped == "" or stripped == "x" or stripped.startswith(";"):
                    safe_lines.append(line)
                    continue

                # Vérifier si ce personnage est OK
                if stripped in self.results['ok']:
                    safe_lines.append(line)
                else:
                    # Commenter le personnage problématique
                    safe_lines.append(f"; {line}")
            else:
                # Hors section Characters, copier tel quel
                safe_lines.append(line)

        # Sauvegarder
        safe_path = self.game_dir / "data" / "select_safe.def"
        with open(safe_path, 'w', encoding='utf-8') as f:
            f.writelines(safe_lines)

        print(f"{Colors.GREEN}  ✓ Fichier créé: {safe_path.name}{Colors.RESET}")
        print(f"{Colors.GREEN}  ✓ {len(self.results['ok'])} personnages OK gardés{Colors.RESET}")
        print(f"{Colors.YELLOW}  ⚠ {len(self.results['failed'])} personnages commentés{Colors.RESET}")

    def generate_report(self):
        """Génère un rapport détaillé"""
        report_path = self.game_dir / "characters_test_report.txt"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("KOF ULTIMATE - RAPPORT DE TEST DES PERSONNAGES\n")
            f.write("="*80 + "\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write(f"Total testés: {len(self.characters)}\n")
            f.write(f"✓ OK: {len(self.results['ok'])}\n")
            f.write(f"✗ ÉCHOUÉS: {len(self.results['failed'])}\n")
            f.write(f"⊘ IGNORÉS: {len(self.results['skipped'])}\n")
            f.write("\n" + "="*80 + "\n\n")

            # Personnages OK
            f.write("PERSONNAGES FONCTIONNELS:\n")
            f.write("-" * 80 + "\n")
            for char in self.results['ok']:
                f.write(f"  ✓ {char}\n")

            f.write("\n\n")

            # Personnages échoués
            f.write("PERSONNAGES AVEC ERREURS:\n")
            f.write("-" * 80 + "\n")
            for item in self.results['failed']:
                f.write(f"  ✗ {item['name']}\n")
                for error in item['errors']:
                    f.write(f"      - {error}\n")

            f.write("\n\n")

            # Personnages ignorés
            if self.results['skipped']:
                f.write("PERSONNAGES IGNORÉS:\n")
                f.write("-" * 80 + "\n")
                for item in self.results['skipped']:
                    f.write(f"  ⊘ {item['name']}: {item['reason']}\n")

        print(f"\n{Colors.CYAN}📄 Rapport généré: {report_path.name}{Colors.RESET}")

    def show_summary(self):
        """Affiche un résumé"""
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'RÉSUMÉ DU TEST':^80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

        total = len(self.characters)
        ok = len(self.results['ok'])
        failed = len(self.results['failed'])
        skipped = len(self.results['skipped'])

        ok_pct = (ok / total * 100) if total > 0 else 0
        failed_pct = (failed / total * 100) if total > 0 else 0

        print(f"  Total testés:       {total}")
        print(f"  {Colors.GREEN}✓ OK:               {ok} ({ok_pct:.1f}%){Colors.RESET}")
        print(f"  {Colors.RED}✗ ÉCHOUÉS:          {failed} ({failed_pct:.1f}%){Colors.RESET}")
        print(f"  {Colors.YELLOW}⊘ IGNORÉS:          {skipped}{Colors.RESET}")

        print(f"\n{Colors.CYAN}Fichiers générés:{Colors.RESET}")
        print(f"  • select_safe.def - Personnages fonctionnels seulement")
        print(f"  • characters_test_report.txt - Rapport détaillé")

    def run_full_test(self):
        """Lance le test complet"""
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'TEST AUTOMATIQUE DE TOUS LES PERSONNAGES':^80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

        try:
            # 1. Backup
            self.backup_select_def()

            # 2. Parse
            num_chars = self.parse_select_def()

            if num_chars == 0:
                print(f"{Colors.RED}Aucun personnage trouvé!{Colors.RESET}")
                return

            # 3. Info (pas de confirmation - auto-start)
            print(f"\n{Colors.YELLOW}⚠️  Ce test va prendre environ {num_chars * 7} secondes (~{num_chars * 7 // 60} min){Colors.RESET}")
            print(f"{Colors.CYAN}Le jeu va s'ouvrir et se fermer {num_chars} fois automatiquement.{Colors.RESET}")
            print(f"{Colors.GREEN}Démarrage automatique dans 3 secondes...{Colors.RESET}")
            time.sleep(3)

            # 4. Tester chaque personnage
            print(f"\n{Colors.MAGENTA}{Colors.BOLD}DÉBUT DU TEST...{Colors.RESET}")

            for i, char in enumerate(self.characters, 1):
                print(f"{Colors.CYAN}[{i}/{num_chars}]{Colors.RESET}", end=" ")
                self.test_character(char)

            # 5. Restaurer select.def original
            print(f"\n{Colors.CYAN}Restauration de select.def original...{Colors.RESET}")
            self.restore_select_def()

            # 6. Générer select_safe.def
            self.generate_safe_select_def()

            # 7. Générer rapport
            self.generate_report()

            # 8. Résumé
            self.show_summary()

            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ TEST TERMINÉ!{Colors.RESET}\n")

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Test interrompu par l'utilisateur{Colors.RESET}")
            self.restore_select_def()

        except Exception as e:
            print(f"\n{Colors.RED}Erreur: {e}{Colors.RESET}")
            import traceback
            traceback.print_exc()
            self.restore_select_def()

def main():
    game_dir = r"D:\KOF Ultimate Online Online Online"
    tester = CharacterTester(game_dir)
    tester.run_full_test()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n{Colors.RED}Erreur fatale: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
