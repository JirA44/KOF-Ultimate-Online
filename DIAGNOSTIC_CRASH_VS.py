#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNOSTIC APPROFONDI DU CRASH EN MODE VS
Vérifie TOUT ce qui peut causer un crash
"""

import os
import subprocess
import time
from pathlib import Path
from datetime import datetime

GAME_PATH = Path(__file__).parent
GAME_EXE = "KOF_Ultimate_Online.exe"

class CrashDiagnostic:
    def __init__(self):
        self.issues = []
        self.warnings = []

    def log_issue(self, issue):
        self.issues.append(issue)
        print(f"❌ PROBLÈME: {issue}")

    def log_warning(self, warning):
        self.warnings.append(warning)
        print(f"⚠️  AVERTISSEMENT: {warning}")

    def log_ok(self, msg):
        print(f"✅ {msg}")

    def check_game_files(self):
        """Vérifie les fichiers critiques"""
        print("\n" + "="*70)
        print("VÉRIFICATION DES FICHIERS")
        print("="*70)

        # Exe
        if not (GAME_PATH / GAME_EXE).exists():
            self.log_issue(f"{GAME_EXE} manquant")
        else:
            self.log_ok(f"{GAME_EXE} présent")

        # Fichiers critiques
        critical_files = [
            "data/mugen.cfg",
            "data/select.def",
            "data/system.def"
        ]

        for f in critical_files:
            path = GAME_PATH / f
            if not path.exists():
                self.log_issue(f"Fichier critique manquant: {f}")
            else:
                self.log_ok(f"{f} présent")

    def check_characters(self):
        """Vérifie les personnages"""
        print("\n" + "="*70)
        print("VÉRIFICATION DES PERSONNAGES")
        print("="*70)

        chars_dir = GAME_PATH / "chars"
        if not chars_dir.exists():
            self.log_issue("Dossier chars/ manquant")
            return

        chars = list(chars_dir.iterdir())
        print(f"Personnages trouvés: {len(chars)}")

        if len(chars) == 0:
            self.log_issue("Aucun personnage installé!")
        elif len(chars) < 2:
            self.log_warning("Moins de 2 personnages (nécessaire pour VS)")
        else:
            self.log_ok(f"{len(chars)} personnages disponibles")

        # Vérifier def files
        for char_dir in chars[:5]:  # Premiers 5
            if char_dir.is_dir():
                def_file = char_dir / f"{char_dir.name}.def"
                if not def_file.exists():
                    self.log_warning(f"Fichier .def manquant pour {char_dir.name}")

    def check_stages(self):
        """Vérifie les stages"""
        print("\n" + "="*70)
        print("VÉRIFICATION DES STAGES")
        print("="*70)

        stages_dir = GAME_PATH / "stages"
        if not stages_dir.exists():
            self.log_issue("Dossier stages/ manquant")
            return

        stages = list(stages_dir.glob("*.def"))
        print(f"Stages trouvés: {len(stages)}")

        if len(stages) == 0:
            self.log_issue("Aucun stage disponible! Le jeu va crasher.")
        else:
            self.log_ok(f"{len(stages)} stages disponibles")

        # Vérifier stages corrompus
        for stage in stages[:10]:
            try:
                with open(stage, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if len(content) < 50:
                        self.log_warning(f"Stage suspect (trop petit): {stage.name}")
            except:
                self.log_warning(f"Stage illisible: {stage.name}")

    def check_config(self):
        """Vérifie la configuration"""
        print("\n" + "="*70)
        print("VÉRIFICATION CONFIGURATION")
        print("="*70)

        cfg_file = GAME_PATH / "data" / "mugen.cfg"
        if not cfg_file.exists():
            self.log_issue("mugen.cfg manquant")
            return

        try:
            with open(cfg_file, 'r', encoding='utf-8') as f:
                config = f.read()

            # Vérifier settings critiques
            checks = [
                ("GameWidth", "Résolution largeur"),
                ("GameHeight", "Résolution hauteur"),
                ("Team.1.VS.2", "Configuration VS"),
            ]

            for key, desc in checks:
                if key.lower() not in config.lower():
                    self.log_warning(f"Config {desc} ({key}) non trouvée")
                else:
                    self.log_ok(f"Config {desc} présente")

        except Exception as e:
            self.log_issue(f"Erreur lecture config: {e}")

    def check_select_def(self):
        """Vérifie select.def"""
        print("\n" + "="*70)
        print("VÉRIFICATION SELECT.DEF")
        print("="*70)

        select_file = GAME_PATH / "data" / "select.def"
        if not select_file.exists():
            self.log_issue("select.def manquant - Le jeu ne peut pas démarrer!")
            return

        try:
            with open(select_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Compter les personnages listés
            char_lines = [l for l in lines if l.strip() and not l.strip().startswith(';') and ',' in l]
            print(f"Personnages listés dans select.def: {len(char_lines)}")

            if len(char_lines) == 0:
                self.log_issue("Aucun personnage dans select.def!")
            elif len(char_lines) < 2:
                self.log_warning("Moins de 2 personnages dans select.def")
            else:
                self.log_ok(f"{len(char_lines)} personnages configurés")

            # Vérifier que les fichiers existent
            missing = 0
            for line in char_lines[:20]:  # Premiers 20
                parts = line.split(',')
                if len(parts) > 0:
                    char_name = parts[0].strip()
                    char_path = GAME_PATH / "chars" / char_name
                    if not char_path.exists():
                        missing += 1

            if missing > 0:
                self.log_warning(f"{missing} personnages listés mais fichiers manquants")

        except Exception as e:
            self.log_issue(f"Erreur lecture select.def: {e}")

    def check_logs(self):
        """Vérifie les logs existants"""
        print("\n" + "="*70)
        print("VÉRIFICATION DES LOGS PRÉCÉDENTS")
        print("="*70)

        log_file = GAME_PATH / "mugen.log"
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                # Chercher erreurs
                errors = [l for l in lines if any(x in l.lower() for x in ['error', 'crash', 'fail', 'exception'])]

                if errors:
                    print(f"\n⚠️  {len(errors)} erreurs trouvées dans mugen.log:")
                    for err in errors[-10:]:  # 10 dernières
                        print(f"   {err.strip()}")
                else:
                    self.log_ok("Aucune erreur dans mugen.log")

            except Exception as e:
                self.log_warning(f"Impossible de lire mugen.log: {e}")
        else:
            print("Aucun mugen.log trouvé (normal si premier lancement)")

    def generate_report(self):
        """Génère le rapport final"""
        print("\n" + "="*70)
        print("RAPPORT FINAL - DIAGNOSTIC CRASH VS")
        print("="*70)

        print(f"\n❌ PROBLÈMES CRITIQUES: {len(self.issues)}")
        for i, issue in enumerate(self.issues, 1):
            print(f"   {i}. {issue}")

        print(f"\n⚠️  AVERTISSEMENTS: {len(self.warnings)}")
        for i, warning in enumerate(self.warnings, 1):
            print(f"   {i}. {warning}")

        # Verdict
        print("\n" + "="*70)
        if len(self.issues) == 0 and len(self.warnings) == 0:
            print("✅ VERDICT: Configuration semble OK")
            print("   Le crash vient probablement d'autre chose (bug moteur, etc.)")
        elif len(self.issues) > 0:
            print("❌ VERDICT: Problèmes CRITIQUES trouvés")
            print("   Ces problèmes DOIVENT être corrigés")
        else:
            print("⚠️  VERDICT: Avertissements trouvés")
            print("   Peuvent causer des problèmes occasionnels")

        # Sauvegarder
        report_file = GAME_PATH / "logs" / f"diagnostic_crash_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        report_file.parent.mkdir(exist_ok=True)

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("DIAGNOSTIC CRASH MODE VS\n")
            f.write("="*70 + "\n\n")
            f.write(f"Date: {datetime.now()}\n\n")
            f.write(f"PROBLÈMES CRITIQUES: {len(self.issues)}\n")
            for issue in self.issues:
                f.write(f"- {issue}\n")
            f.write(f"\nAVERTISSEMENTS: {len(self.warnings)}\n")
            for warning in self.warnings:
                f.write(f"- {warning}\n")

        print(f"\n📄 Rapport sauvegardé: {report_file}")

    def run(self):
        """Lance le diagnostic complet"""
        print("\n" + "="*70)
        print("  🔍 DIAGNOSTIC APPROFONDI - CRASH MODE VS")
        print("  KOF Ultimate Online")
        print("="*70)

        self.check_game_files()
        self.check_characters()
        self.check_stages()
        self.check_config()
        self.check_select_def()
        self.check_logs()
        self.generate_report()

if __name__ == "__main__":
    diagnostic = CrashDiagnostic()
    diagnostic.run()

    print("\n" + "="*70)
    input("Appuyez sur ENTRÉE pour fermer...")
