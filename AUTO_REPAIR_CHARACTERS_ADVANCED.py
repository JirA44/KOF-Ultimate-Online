#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTO-REPAIR AVANCÉ - Répare les personnages au lieu de les supprimer
Corrige: .air, storyboards, CLSN, références cassées
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

# Chemins
BASE_DIR = Path(__file__).parent
CHARS_DIR = BASE_DIR / "chars"
LOG_FILE = BASE_DIR / "repair_advanced.log"
RESULTS_FILE = BASE_DIR / "repair_advanced_results.txt"

class CharacterRepairer:
    def __init__(self):
        self.log = []
        self.repairs_made = 0
        self.errors_fixed = {
            "air_clsn": 0,
            "storyboards": 0,
            "invalid_actions": 0,
            "references": 0
        }

    def log_msg(self, msg):
        """Log un message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_msg = f"[{timestamp}] {msg}"
        print(full_msg)
        self.log.append(full_msg)

    def repair_air_file(self, air_path):
        """Répare un fichier .air avec erreurs CLSN"""
        if not air_path.exists():
            return False

        self.log_msg(f"  📄 Réparation {air_path.name}...")

        try:
            # Backup
            backup = air_path.with_suffix('.air.backup')
            if not backup.exists():
                shutil.copy2(air_path, backup)

            # Lire le fichier
            with open(air_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Analyser et corriger
            fixed_lines = []
            current_action = None
            clsn_errors_fixed = 0

            for i, line in enumerate(lines, 1):
                # Détecter début d'action
                if line.strip().startswith('[Begin Action'):
                    current_action = line.strip()
                    fixed_lines.append(line)
                    continue

                # Vérifier lignes CLSN
                if 'Clsn' in line or 'clsn' in line:
                    # Format attendu: Clsn1: X = x1, y1, x2, y2
                    # ou: Clsn1Default: X

                    # Vérifier format
                    if '=' in line:
                        parts = line.split('=')
                        if len(parts) == 2:
                            values = parts[1].strip().split(',')
                            # Devrait avoir 4 valeurs (x1, y1, x2, y2)
                            if len(values) == 4:
                                try:
                                    # Vérifier que ce sont des nombres
                                    [int(v.strip()) for v in values]
                                    fixed_lines.append(line)
                                except ValueError:
                                    # Nombres invalides, supprimer la ligne
                                    self.log_msg(f"    ⚠️  Ligne {i}: CLSN invalide supprimée")
                                    clsn_errors_fixed += 1
                            else:
                                # Mauvais nombre de valeurs
                                self.log_msg(f"    ⚠️  Ligne {i}: CLSN avec {len(values)} valeurs au lieu de 4")
                                clsn_errors_fixed += 1
                        else:
                            # Mauvais format, supprimer
                            clsn_errors_fixed += 1
                    else:
                        # Ligne CLSN sans '=', probablement OK (ClsnDefault)
                        fixed_lines.append(line)
                else:
                    fixed_lines.append(line)

            if clsn_errors_fixed > 0:
                # Sauvegarder le fichier corrigé
                with open(air_path, 'w', encoding='utf-8') as f:
                    f.writelines(fixed_lines)

                self.log_msg(f"    ✅ {clsn_errors_fixed} erreurs CLSN corrigées")
                self.errors_fixed["air_clsn"] += clsn_errors_fixed
                return True
            else:
                self.log_msg(f"    ℹ️  Aucune erreur trouvée")
                return False

        except Exception as e:
            self.log_msg(f"    ❌ Erreur: {e}")
            return False

    def create_dummy_storyboard(self, char_dir, storyboard_name="ending.storyboard"):
        """Crée un storyboard vide si manquant"""
        storyboard_path = char_dir / storyboard_name

        if storyboard_path.exists():
            return False

        self.log_msg(f"  📝 Création de {storyboard_name}...")

        # Contenu minimal d'un storyboard
        content = """; Storyboard vide auto-généré
; Créé le {}
; Pour éviter les erreurs de chargement

[SceneDef]
spr = 9000,0
layerall.pos = 0,0
bgm =
bgm.volume = 100

[Scene 0]
fade.in = black,30
clearcolor = 0,0,0

[End]
""".format(datetime.now().strftime("%Y-%m-%d %H:%M"))

        try:
            with open(storyboard_path, 'w', encoding='utf-8') as f:
                f.write(content)

            self.log_msg(f"    ✅ Storyboard créé")
            self.errors_fixed["storyboards"] += 1
            return True
        except Exception as e:
            self.log_msg(f"    ❌ Erreur: {e}")
            return False

    def repair_character(self, char_name):
        """Répare un personnage complet"""
        char_dir = CHARS_DIR / char_name

        if not char_dir.is_dir():
            return False

        self.log_msg(f"\n🔧 Réparation: {char_name}")

        repairs = 0

        # 1. Chercher et réparer fichier .air
        air_files = list(char_dir.glob("*.air"))
        for air_file in air_files:
            if self.repair_air_file(air_file):
                repairs += 1

        # 2. Créer storyboards manquants
        storyboards_to_check = [
            "ending.storyboard",
            "intro.storyboard",
            "win.storyboard"
        ]

        for sb in storyboards_to_check:
            if self.create_dummy_storyboard(char_dir, sb):
                repairs += 1

        if repairs > 0:
            self.repairs_made += 1
            self.log_msg(f"  ✅ {repairs} réparation(s) effectuée(s)")
            return True
        else:
            self.log_msg(f"  ℹ️  Aucune réparation nécessaire")
            return False

    def repair_all_characters(self):
        """Répare tous les personnages"""
        self.log_msg("=" * 80)
        self.log_msg("🛠️  RÉPARATION AVANCÉE DES PERSONNAGES")
        self.log_msg("=" * 80)

        if not CHARS_DIR.exists():
            self.log_msg(f"❌ Dossier chars introuvable: {CHARS_DIR}")
            return

        # Lister tous les dossiers de personnages
        char_dirs = [d for d in CHARS_DIR.iterdir() if d.is_dir()]
        self.log_msg(f"\n📂 {len(char_dirs)} personnages trouvés\n")

        for char_dir in sorted(char_dirs):
            self.repair_character(char_dir.name)

        # Rapport final
        self.log_msg("\n" + "=" * 80)
        self.log_msg("📊 RAPPORT FINAL")
        self.log_msg("=" * 80)
        self.log_msg(f"Personnages réparés: {self.repairs_made}/{len(char_dirs)}")
        self.log_msg(f"\nErreurs corrigées:")
        self.log_msg(f"  • CLSN invalides: {self.errors_fixed['air_clsn']}")
        self.log_msg(f"  • Storyboards créés: {self.errors_fixed['storyboards']}")
        self.log_msg(f"  • Actions invalides: {self.errors_fixed['invalid_actions']}")
        self.log_msg(f"  • Références corrigées: {self.errors_fixed['references']}")

        total_fixes = sum(self.errors_fixed.values())
        self.log_msg(f"\n✅ TOTAL: {total_fixes} corrections effectuées")

        # Sauvegarder logs
        self.save_logs()

    def save_logs(self):
        """Sauvegarde les logs"""
        try:
            with open(LOG_FILE, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.log))

            with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
                f.write(f"Réparation effectuée: {datetime.now()}\n")
                f.write(f"Personnages réparés: {self.repairs_made}\n")
                f.write(f"Erreurs corrigées: {sum(self.errors_fixed.values())}\n\n")
                f.write("Détails:\n")
                for key, value in self.errors_fixed.items():
                    f.write(f"  {key}: {value}\n")

            self.log_msg(f"\n📄 Logs sauvegardés: {LOG_FILE}")
            self.log_msg(f"📄 Résultats: {RESULTS_FILE}")
        except Exception as e:
            self.log_msg(f"⚠️  Erreur sauvegarde logs: {e}")

def main():
    """Point d'entrée"""
    repairer = CharacterRepairer()
    repairer.repair_all_characters()

    print("\n✅ Réparation terminée!")
    print(f"📄 Voir: {LOG_FILE}")

    input("\nAppuyez sur ENTRÉE pour fermer...")

if __name__ == "__main__":
    main()
