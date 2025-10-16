#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de tests automatisés pour KOF Ultimate
Vérifie la configuration sans interface graphique
"""

import os
import re
from pathlib import Path
from collections import defaultdict

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class AutoTestSystem:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.tests_passed = 0
        self.tests_failed = 0
        self.tests_warnings = 0
        self.issues = []

    def print_header(self, text):
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{text:^80}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

    def print_section(self, text):
        print(f"\n{Colors.BLUE}{Colors.BOLD}▶ {text}{Colors.RESET}")
        print(f"{Colors.BLUE}{'─'*78}{Colors.RESET}")

    def test_ok(self, message):
        print(f"{Colors.GREEN}  ✓ {message}{Colors.RESET}")
        self.tests_passed += 1

    def test_fail(self, message, issue=None):
        print(f"{Colors.RED}  ✗ {message}{Colors.RESET}")
        self.tests_failed += 1
        if issue:
            self.issues.append(issue)

    def test_warn(self, message):
        print(f"{Colors.YELLOW}  ⚠ {message}{Colors.RESET}")
        self.tests_warnings += 1

    def test_info(self, message):
        print(f"{Colors.WHITE}    {message}{Colors.RESET}")

    def test_file_syntax(self, file_path, file_type):
        """Teste la syntaxe d'un fichier de configuration"""
        self.print_section(f"Test de syntaxe: {file_path.name}")

        if not file_path.exists():
            self.test_fail(f"{file_path.name} n'existe pas", f"Fichier manquant: {file_path}")
            return False

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            self.test_ok(f"Fichier lisible: {len(lines)} lignes")

            # Vérifications spécifiques selon le type
            if file_type == 'def':
                return self.validate_def_file(file_path, lines)
            elif file_type == 'cfg':
                return self.validate_cfg_file(file_path, lines)

            return True

        except Exception as e:
            self.test_fail(f"Erreur de lecture: {e}", f"Erreur: {file_path} - {e}")
            return False

    def validate_def_file(self, file_path, lines):
        """Valide un fichier .def"""
        sections = []
        current_section = None
        section_line = 0

        for i, line in enumerate(lines, 1):
            line = line.strip()

            # Détecter les sections
            if line.startswith('[') and line.endswith(']'):
                section_name = line[1:-1]
                sections.append((section_name, i))
                current_section = section_name
                section_line = i

            # Vérifier les lignes de configuration
            elif '=' in line and not line.startswith(';'):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()

                    # Vérifier que la clé n'est pas vide
                    if not key:
                        self.test_warn(f"Clé vide à la ligne {i}")

        self.test_ok(f"Trouvé {len(sections)} sections")

        # Afficher quelques sections pour info
        if sections:
            self.test_info(f"Sections: {', '.join([s[0] for s in sections[:5]])}")
            if len(sections) > 5:
                self.test_info(f"... et {len(sections) - 5} autres sections")

        return True

    def validate_cfg_file(self, file_path, lines):
        """Valide un fichier .cfg"""
        sections = []

        for i, line in enumerate(lines, 1):
            line = line.strip()

            if line.startswith('[') and line.endswith(']'):
                section_name = line[1:-1]
                sections.append(section_name)

        self.test_ok(f"Trouvé {len(sections)} sections de configuration")

        return True

    def test_character_integrity(self):
        """Teste l'intégrité des personnages"""
        self.print_section("Test d'intégrité des personnages")

        # Lire select.def
        select_def = self.base_dir / 'data' / 'select.def'

        if not select_def.exists():
            self.test_fail("select.def introuvable", "select.def manquant")
            return

        chars_in_select = []
        with open(select_def, 'r', encoding='utf-8', errors='ignore') as f:
            in_chars = False
            for line in f:
                line = line.strip()
                if line.startswith('[Characters]'):
                    in_chars = True
                    continue
                elif line.startswith('['):
                    in_chars = False
                    continue

                if in_chars and line and not line.startswith(';') and line.lower() != 'x':
                    char_name = line.split(',')[0].strip()
                    chars_in_select.append(char_name)

        self.test_info(f"Trouvé {len(chars_in_select)} personnages dans select.def")

        # Vérifier les dossiers
        chars_dir = self.base_dir / 'chars'
        if not chars_dir.exists():
            self.test_fail("Dossier 'chars' introuvable", "Dossier chars manquant")
            return

        missing_chars = []
        found_chars = 0

        for char in chars_in_select[:50]:  # Vérifier les 50 premiers
            char_path = chars_dir / char
            if char_path.exists() and char_path.is_dir():
                # Vérifier qu'il y a un fichier .def
                def_files = list(char_path.glob('*.def'))
                if def_files:
                    found_chars += 1
                else:
                    missing_chars.append(f"{char} (pas de .def)")
            else:
                missing_chars.append(char)

        if found_chars > 0:
            self.test_ok(f"{found_chars}/{min(50, len(chars_in_select))} premiers personnages vérifiés OK")

        if missing_chars:
            self.test_warn(f"{len(missing_chars)} personnages manquants ou incomplets")
            for char in missing_chars[:5]:
                self.test_info(f"  - {char}")
            if len(missing_chars) > 5:
                self.test_info(f"  ... et {len(missing_chars) - 5} autres")

    def test_stage_integrity(self):
        """Teste l'intégrité des stages"""
        self.print_section("Test d'intégrité des stages")

        stages_dir = self.base_dir / 'stages'

        if not stages_dir.exists():
            self.test_fail("Dossier 'stages' introuvable", "Dossier stages manquant")
            return

        # Compter les fichiers .def
        stage_defs = list(stages_dir.glob('*.def'))
        self.test_ok(f"Trouvé {len(stage_defs)} fichiers .def de stages")

        # Vérifier quelques stages
        valid_stages = 0
        for stage_def in stage_defs[:10]:  # Vérifier les 10 premiers
            try:
                with open(stage_def, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Vérifier que le fichier a du contenu
                    if len(content) > 100:
                        valid_stages += 1
            except:
                pass

        if valid_stages > 0:
            self.test_ok(f"{valid_stages}/{min(10, len(stage_defs))} premiers stages vérifiés OK")

    def test_system_configuration(self):
        """Teste la configuration système"""
        self.print_section("Test de configuration système")

        # Vérifier system.def
        system_def = self.base_dir / 'data' / 'system.def'
        if system_def.exists():
            self.test_file_syntax(system_def, 'def')
        else:
            self.test_fail("system.def manquant", "Fichier système manquant")

        # Vérifier mugen.cfg
        mugen_cfg = self.base_dir / 'data' / 'mugen.cfg'
        if mugen_cfg.exists():
            self.test_file_syntax(mugen_cfg, 'cfg')

            # Vérifier des paramètres importants
            with open(mugen_cfg, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Vérifier la résolution
                if 'GameWidth' in content and 'GameHeight' in content:
                    self.test_ok("Résolution configurée")
                else:
                    self.test_warn("Résolution non trouvée dans la config")

                # Vérifier le mode fenêtré/plein écran
                if 'FullScreen' in content:
                    self.test_ok("Mode d'affichage configuré")

        else:
            self.test_fail("mugen.cfg manquant", "Configuration MUGEN manquante")

    def test_assets_integrity(self):
        """Teste l'intégrité des assets"""
        self.print_section("Test d'intégrité des assets")

        data_dir = self.base_dir / 'data'

        required_assets = {
            'system.sff': 'Sprites système',
            'system.snd': 'Sons système',
            'fight.sff': 'Sprites de combat',
            'fight.snd': 'Sons de combat',
            'fightfx.sff': 'Effets de combat'
        }

        for asset, description in required_assets.items():
            asset_path = data_dir / asset
            if asset_path.exists():
                size_mb = asset_path.stat().st_size / (1024 * 1024)
                self.test_ok(f"{asset} ({description}) - {size_mb:.2f} MB")
            else:
                self.test_fail(f"{asset} manquant", f"Asset manquant: {asset}")

    def test_fonts_integrity(self):
        """Teste l'intégrité des polices"""
        self.print_section("Test d'intégrité des polices")

        font_dir = self.base_dir / 'font'

        if not font_dir.exists():
            self.test_fail("Dossier 'font' introuvable", "Dossier font manquant")
            return

        font_files = list(font_dir.glob('*.fnt')) + list(font_dir.glob('*.ttf'))

        if font_files:
            self.test_ok(f"Trouvé {len(font_files)} fichiers de polices")
        else:
            self.test_warn("Aucun fichier de police trouvé")

    def test_sound_integrity(self):
        """Teste l'intégrité des sons"""
        self.print_section("Test d'intégrité des sons")

        sound_dir = self.base_dir / 'sound'

        if not sound_dir.exists():
            self.test_warn("Dossier 'sound' introuvable (optionnel)")
            return

        sound_files = list(sound_dir.glob('*.mp3')) + list(sound_dir.glob('*.ogg')) + list(sound_dir.glob('*.wav'))

        if sound_files:
            self.test_ok(f"Trouvé {len(sound_files)} fichiers audio")
        else:
            self.test_info("Aucun fichier audio trouvé (optionnel)")

    def test_multiplayer_config(self):
        """Teste la configuration multijoueur"""
        self.print_section("Test de configuration multijoueur")

        mp_config = self.base_dir / 'multiplayer_config.json'

        if mp_config.exists():
            try:
                import json
                with open(mp_config, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                self.test_ok("Fichier de configuration multijoueur valide")

                if 'server' in config:
                    self.test_info(f"Serveur: {config.get('server', {}).get('host', 'N/A')}")

            except json.JSONDecodeError as e:
                self.test_fail(f"Erreur JSON: {e}", "Configuration multijoueur invalide")
            except Exception as e:
                self.test_warn(f"Erreur de lecture: {e}")
        else:
            self.test_info("Pas de configuration multijoueur (optionnel)")

    def test_scripts_integrity(self):
        """Teste l'intégrité des scripts Python"""
        self.print_section("Test d'intégrité des scripts")

        scripts = [
            'launcher_modern.py',
            'gamepad_hotplug_monitor.py',
            'launcher_ai_navigator.py',
            'gamepad_auto_config.py'
        ]

        for script in scripts:
            script_path = self.base_dir / script
            if script_path.exists():
                # Vérifier que le script est syntaxiquement valide
                try:
                    with open(script_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Vérification basique de syntaxe Python
                    compile(content, script, 'exec')
                    self.test_ok(f"{script} - Syntaxe valide")

                except SyntaxError as e:
                    self.test_fail(f"{script} - Erreur de syntaxe: {e}", f"Erreur syntaxe: {script}")
                except Exception as e:
                    self.test_warn(f"{script} - Avertissement: {e}")
            else:
                self.test_warn(f"{script} - Fichier manquant (optionnel)")

    def generate_final_report(self):
        """Génère le rapport final"""
        self.print_header("RAPPORT FINAL DES TESTS")

        total_tests = self.tests_passed + self.tests_failed + self.tests_warnings

        print(f"{Colors.BOLD}Résumé des tests:{Colors.RESET}")
        print(f"  {Colors.GREEN}✓ Tests réussis: {self.tests_passed}{Colors.RESET}")

        if self.tests_failed > 0:
            print(f"  {Colors.RED}✗ Tests échoués: {self.tests_failed}{Colors.RESET}")

        if self.tests_warnings > 0:
            print(f"  {Colors.YELLOW}⚠ Avertissements: {self.tests_warnings}{Colors.RESET}")

        # Score
        if total_tests > 0:
            success_rate = (self.tests_passed / total_tests) * 100
            print(f"\n{Colors.BOLD}Score de santé: ", end='')

            if success_rate >= 90:
                print(f"{Colors.GREEN}{success_rate:.1f}% - EXCELLENT{Colors.RESET}")
            elif success_rate >= 75:
                print(f"{Colors.YELLOW}{success_rate:.1f}% - BON{Colors.RESET}")
            elif success_rate >= 50:
                print(f"{Colors.YELLOW}{success_rate:.1f}% - MOYEN{Colors.RESET}")
            else:
                print(f"{Colors.RED}{success_rate:.1f}% - PROBLÈMES DÉTECTÉS{Colors.RESET}")

        # Problèmes critiques
        if self.issues:
            print(f"\n{Colors.BOLD}Problèmes critiques détectés:{Colors.RESET}")
            for i, issue in enumerate(self.issues[:10], 1):
                print(f"{Colors.RED}  {i}. {issue}{Colors.RESET}")

            if len(self.issues) > 10:
                print(f"{Colors.YELLOW}  ... et {len(self.issues) - 10} autres problèmes{Colors.RESET}")

        # Recommandations
        print(f"\n{Colors.BOLD}Recommandations:{Colors.RESET}")

        if self.tests_failed == 0 and self.tests_warnings == 0:
            print(f"{Colors.GREEN}  ✓ Tous les tests sont passés - Le jeu est prêt!{Colors.RESET}")
        elif self.tests_failed == 0:
            print(f"{Colors.YELLOW}  ⚠ Quelques avertissements - Le jeu devrait fonctionner{Colors.RESET}")
        else:
            print(f"{Colors.RED}  ✗ Corrections nécessaires avant de lancer le jeu{Colors.RESET}")

        print()

    def run_all_tests(self):
        """Lance tous les tests"""
        self.print_header("SYSTÈME DE TESTS AUTOMATISÉS - KOF ULTIMATE")

        # Lancer tous les tests
        self.test_system_configuration()
        self.test_assets_integrity()
        self.test_fonts_integrity()
        self.test_sound_integrity()
        self.test_character_integrity()
        self.test_stage_integrity()
        self.test_multiplayer_config()
        self.test_scripts_integrity()

        # Rapport final
        self.generate_final_report()

def main():
    tester = AutoTestSystem()
    tester.run_all_tests()

if __name__ == '__main__':
    main()
