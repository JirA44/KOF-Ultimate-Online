#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VÉRIFICATION COMPLÈTE D'INSTALLATION
Vérifie TOUT avant de lancer le jeu
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import json

GAME_PATH = Path(__file__).parent

class InstallationChecker:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.infos = []

    def error(self, msg):
        self.errors.append(msg)
        print(f"❌ ERREUR: {msg}")

    def warn(self, msg):
        self.warnings.append(msg)
        print(f"⚠️  AVERTISSEMENT: {msg}")

    def info(self, msg):
        self.infos.append(msg)
        print(f"ℹ️  INFO: {msg}")

    def ok(self, msg):
        print(f"✅ {msg}")

    def section(self, title):
        print(f"\n{'='*70}")
        print(f"  {title}")
        print('='*70)

    def check_python(self):
        """Vérifie Python"""
        self.section("PYTHON")

        version = sys.version_info
        print(f"Version: {version.major}.{version.minor}.{version.micro}")

        if version.major < 3:
            self.error("Python 3 requis!")
        elif version.minor < 7:
            self.warn("Python 3.7+ recommandé")
        else:
            self.ok("Version Python OK")

    def check_python_packages(self):
        """Vérifie les packages Python"""
        self.section("PACKAGES PYTHON")

        required = {
            'pywin32': 'Tests automatiques (injection inputs)',
            'PIL': 'Screenshots automatiques',
            'requests': 'Matchmaking online',
            'websockets': 'Multiplayer temps réel',
        }

        optional = {
            'numpy': 'IA et analyse',
            'pandas': 'Statistiques avancées',
            'matplotlib': 'Graphiques',
        }

        for package, desc in required.items():
            try:
                __import__(package)
                self.ok(f"{package:15s} - {desc}")
            except ImportError:
                self.error(f"{package} manquant - Nécessaire pour: {desc}")
                self.info(f"   Installation: pip install {package}")

        print("\nPackages optionnels:")
        for package, desc in optional.items():
            try:
                __import__(package)
                self.ok(f"{package:15s} - {desc}")
            except ImportError:
                print(f"⚪ {package:15s} - {desc} (optionnel)")

    def check_game_files(self):
        """Vérifie les fichiers du jeu"""
        self.section("FICHIERS DU JEU")

        # Fichiers critiques
        critical = [
            ("KOF_Ultimate_Online.exe", "Exécutable principal"),
            ("Ikemen_GO.exe", "Moteur de jeu alternatif"),
            ("data/mugen.cfg", "Configuration principale"),
            ("data/select.def", "Liste des personnages"),
            ("data/system.def", "Définition système"),
        ]

        for file, desc in critical:
            path = GAME_PATH / file
            if path.exists():
                size = path.stat().st_size
                self.ok(f"{file:30s} ({size/1024:.1f} KB)")
            else:
                self.error(f"{file} manquant - {desc}")

        # Dossiers critiques
        print("\nDossiers:")
        critical_dirs = [
            ("chars", "Personnages"),
            ("stages", "Stages/arènes"),
            ("data", "Configuration"),
            ("sound", "Sons et musiques"),
            ("font", "Polices de texte"),
        ]

        for dir_name, desc in critical_dirs:
            path = GAME_PATH / dir_name
            if path.exists() and path.is_dir():
                count = len(list(path.iterdir()))
                self.ok(f"{dir_name:15s} - {count} fichiers - {desc}")
            else:
                self.error(f"{dir_name}/ manquant - {desc}")

    def check_characters(self):
        """Vérifie les personnages"""
        self.section("PERSONNAGES")

        chars_dir = GAME_PATH / "chars"
        if not chars_dir.exists():
            self.error("Dossier chars/ manquant!")
            return

        chars = [d for d in chars_dir.iterdir() if d.is_dir()]
        print(f"Total personnages: {len(chars)}")

        if len(chars) == 0:
            self.error("Aucun personnage installé!")
            return
        elif len(chars) < 2:
            self.error("Moins de 2 personnages - impossible de jouer en VS")
        elif len(chars) < 10:
            self.warn(f"Seulement {len(chars)} personnages - un peu limité")
        else:
            self.ok(f"{len(chars)} personnages disponibles")

        # Vérifier intégrité
        print("\nVérification intégrité (10 premiers):")
        valid = 0
        invalid = 0

        for char in chars[:10]:
            # Chercher fichier .def
            def_files = list(char.glob("*.def"))
            if not def_files:
                print(f"  ⚠️  {char.name:30s} - Pas de fichier .def")
                invalid += 1
            else:
                print(f"  ✅ {char.name:30s}")
                valid += 1

        if invalid > 0:
            self.warn(f"{invalid} personnages ont des problèmes")

    def check_stages(self):
        """Vérifie les stages"""
        self.section("STAGES")

        stages_dir = GAME_PATH / "stages"
        if not stages_dir.exists():
            self.error("Dossier stages/ manquant!")
            return

        stages = list(stages_dir.glob("*.def"))
        print(f"Total stages: {len(stages)}")

        if len(stages) == 0:
            self.error("Aucun stage - Le jeu va crasher!")
        elif len(stages) < 3:
            self.warn(f"Seulement {len(stages)} stages - très limité")
        else:
            self.ok(f"{len(stages)} stages disponibles")

        # Vérifier intégrité
        print("\nVérification intégrité (5 premiers):")
        for stage in stages[:5]:
            try:
                with open(stage, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if len(content) < 100:
                    print(f"  ⚠️  {stage.name:30s} - Fichier suspect (trop petit)")
                elif 'spr' not in content.lower():
                    print(f"  ⚠️  {stage.name:30s} - Pas de sprite défini")
                else:
                    print(f"  ✅ {stage.name:30s}")
            except:
                print(f"  ❌ {stage.name:30s} - Illisible")

    def check_select_def(self):
        """Vérifie select.def en détail"""
        self.section("SELECT.DEF (LISTE PERSONNAGES)")

        select_file = GAME_PATH / "data" / "select.def"
        if not select_file.exists():
            self.error("select.def manquant!")
            return

        try:
            with open(select_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Compter personnages
            char_lines = [l for l in lines if l.strip() and not l.strip().startswith(';') and not l.strip().startswith('[') and ',' in l]
            print(f"Personnages listés: {len(char_lines)}")

            if len(char_lines) == 0:
                self.error("Aucun personnage dans select.def!")
            elif len(char_lines) < 2:
                self.error("Moins de 2 personnages - VS impossible")
            else:
                self.ok(f"{len(char_lines)} personnages configurés")

            # Vérifier existence des fichiers
            print("\nVérification existence (20 premiers):")
            missing = 0
            found = 0

            for line in char_lines[:20]:
                parts = line.split(',')
                if len(parts) > 0:
                    char_name = parts[0].strip()
                    char_path = GAME_PATH / "chars" / char_name

                    if char_path.exists():
                        print(f"  ✅ {char_name}")
                        found += 1
                    else:
                        print(f"  ❌ {char_name} - Fichier manquant!")
                        missing += 1

            if missing > 0:
                self.error(f"{missing} personnages listés mais fichiers manquants!")
                self.info("Utilisez CORRIGER_CRASH.bat pour nettoyer")

        except Exception as e:
            self.error(f"Erreur lecture select.def: {e}")

    def check_config(self):
        """Vérifie mugen.cfg"""
        self.section("CONFIGURATION (mugen.cfg)")

        cfg_file = GAME_PATH / "data" / "mugen.cfg"
        if not cfg_file.exists():
            self.error("mugen.cfg manquant!")
            return

        try:
            with open(cfg_file, 'r', encoding='utf-8', errors='ignore') as f:
                config = f.read()

            # Vérifier settings importants
            checks = [
                ("GameWidth", "Résolution largeur", True),
                ("GameHeight", "Résolution hauteur", True),
                ("FullScreen", "Mode plein écran", False),
                ("RenderMode", "Mode de rendu", False),
                ("MaxPlayerCache", "Cache personnages", False),
            ]

            for key, desc, required in checks:
                if key.lower() in config.lower():
                    # Extraire valeur
                    for line in config.split('\n'):
                        if key.lower() in line.lower() and '=' in line:
                            value = line.split('=')[1].strip()
                            print(f"  ✅ {key:20s} = {value:15s} ({desc})")
                            break
                else:
                    if required:
                        self.error(f"{key} non configuré - {desc}")
                    else:
                        self.warn(f"{key} non trouvé - {desc}")

        except Exception as e:
            self.error(f"Erreur lecture config: {e}")

    def check_runtime_dependencies(self):
        """Vérifie dépendances système (DirectX, VC++, etc.)"""
        self.section("DÉPENDANCES SYSTÈME")

        print("Recherche de dépendances Windows...")

        # DirectX
        dx_paths = [
            Path("C:/Windows/System32/d3d9.dll"),
            Path("C:/Windows/System32/d3dx9_43.dll"),
        ]

        has_dx = False
        for path in dx_paths:
            if path.exists():
                has_dx = True
                break

        if has_dx:
            self.ok("DirectX détecté")
        else:
            self.warn("DirectX peut-être manquant - Téléchargez DirectX End-User Runtime")
            self.info("   https://www.microsoft.com/en-us/download/details.aspx?id=35")

        # Visual C++ Runtime
        vcr_paths = [
            Path("C:/Windows/System32/vcruntime140.dll"),
            Path("C:/Windows/System32/msvcp140.dll"),
        ]

        has_vcr = False
        for path in vcr_paths:
            if path.exists():
                has_vcr = True
                break

        if has_vcr:
            self.ok("Visual C++ Runtime détecté")
        else:
            self.warn("Visual C++ Runtime peut-être manquant")
            self.info("   Installez: Visual C++ Redistributable 2015-2022")
            self.info("   https://aka.ms/vs/17/release/vc_redist.x64.exe")

    def check_logs(self):
        """Vérifie les logs existants pour erreurs connues"""
        self.section("LOGS PRÉCÉDENTS")

        log_file = GAME_PATH / "mugen.log"
        if not log_file.exists():
            print("Aucun log (normal si jamais lancé)")
            return

        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Chercher erreurs communes
            error_patterns = {
                'error': "Erreur générale",
                'exception': "Exception",
                'crash': "Crash",
                'failed': "Échec",
                'not found': "Fichier manquant",
                'corrupt': "Fichier corrompu",
            }

            errors_found = {}
            for pattern, desc in error_patterns.items():
                matching = [l for l in lines if pattern in l.lower()]
                if matching:
                    errors_found[desc] = len(matching)

            if errors_found:
                print("\n⚠️  Erreurs dans mugen.log:")
                for desc, count in errors_found.items():
                    print(f"   {desc}: {count} occurrence(s)")
                self.warn(f"{len(errors_found)} types d'erreurs dans le log")
            else:
                self.ok("Pas d'erreurs dans le log")

        except Exception as e:
            self.warn(f"Impossible de lire mugen.log: {e}")

    def generate_report(self):
        """Génère rapport final"""
        self.section("RAPPORT FINAL")

        print(f"\n❌ ERREURS CRITIQUES:  {len(self.errors)}")
        for i, err in enumerate(self.errors, 1):
            print(f"   {i}. {err}")

        print(f"\n⚠️  AVERTISSEMENTS:     {len(self.warnings)}")
        for i, warn in enumerate(self.warnings, 1):
            print(f"   {i}. {warn}")

        # Verdict
        print(f"\n{'='*70}")
        if len(self.errors) == 0 and len(self.warnings) == 0:
            print("✅ INSTALLATION PARFAITE!")
            print("   Le jeu devrait fonctionner sans problème.")
            verdict = "PARFAIT"
        elif len(self.errors) == 0:
            print("⚠️  INSTALLATION OK AVEC AVERTISSEMENTS")
            print("   Le jeu peut fonctionner mais avec problèmes possibles.")
            verdict = "OK_WARNINGS"
        else:
            print("❌ INSTALLATION INCOMPLÈTE")
            print("   Des problèmes DOIVENT être corrigés avant de lancer.")
            verdict = "ERRORS"

        print(f"{'='*70}\n")

        # Sauvegarder rapport
        report = {
            'date': datetime.now().isoformat(),
            'verdict': verdict,
            'errors': self.errors,
            'warnings': self.warnings,
            'infos': self.infos,
        }

        report_file = GAME_PATH / "logs" / "verif_installation.json"
        report_file.parent.mkdir(exist_ok=True)

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"📄 Rapport sauvegardé: {report_file}")

        # Instructions
        if len(self.errors) > 0:
            print(f"\n{'='*70}")
            print("ÉTAPES SUIVANTES:")
            print('='*70)
            print("\n1. Corrigez les ERREURS CRITIQUES (en rouge)")
            print("2. Relancez cette vérification")
            print("3. Une fois 0 erreur, vous pouvez tester le jeu")

        return verdict

    def run(self):
        """Lance toutes les vérifications"""
        print("\n" + "="*70)
        print("  🔍 VÉRIFICATION COMPLÈTE D'INSTALLATION")
        print("  KOF Ultimate Online")
        print("="*70)

        self.check_python()
        self.check_python_packages()
        self.check_game_files()
        self.check_characters()
        self.check_stages()
        self.check_select_def()
        self.check_config()
        self.check_runtime_dependencies()
        self.check_logs()

        return self.generate_report()

if __name__ == "__main__":
    checker = InstallationChecker()
    verdict = checker.run()

    print("\n" + "="*70)
    input("Appuyez sur ENTRÉE pour fermer...")

    # Code de sortie
    sys.exit(0 if verdict == "PARFAIT" else (1 if verdict == "OK_WARNINGS" else 2))
