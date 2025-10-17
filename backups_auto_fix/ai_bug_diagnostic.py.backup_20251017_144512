# -*- coding: utf-8 -*-
"""
Diagnostic Complet des Bugs avec Communication AI
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

class AIBugDiagnostic:
    def __init__(self):
        self.base_dir = Path(r'D:\KOF Ultimate Online')
        self.bugs_found = []
        self.fixes_applied = []

    def print_header(self, text):
        print(f"\n{'='*80}")
        print(f"  {text}")
        print(f"{'='*80}\n")

    def log_bug(self, category, description, severity="MEDIUM"):
        bug = {
            'timestamp': datetime.now().isoformat(),
            'category': category,
            'severity': severity,
            'description': description
        }
        self.bugs_found.append(bug)

        severity_emoji = {
            'HIGH': '🔴',
            'MEDIUM': '🟡',
            'LOW': '🟢'
        }

        print(f"{severity_emoji.get(severity, '⚪')} [{severity}] {category}: {description}")

    def check_visualizer_cors_issue(self):
        """Vérifie le problème CORS du visualiseur"""
        self.print_header("🌐 DIAGNOSTIC: Visualiseur HTML")

        visualizer = self.base_dir / 'VISUALISEUR_PERSONNAGES.html'

        if not visualizer.exists():
            self.log_bug('VISUALISEUR', 'Fichier VISUALISEUR_PERSONNAGES.html manquant', 'HIGH')
            return False

        with open(visualizer, 'r', encoding='utf-8') as f:
            content = f.read()

        # Vérifie si utilise fetch() (problème CORS)
        if 'fetch(' in content:
            self.log_bug(
                'VISUALISEUR',
                'Utilise fetch() qui ne fonctionne pas avec file:// (CORS)',
                'HIGH'
            )
            print("  → Solution: Créer version avec données embarquées")
            return False

        return True

    def check_character_sheets(self):
        """Vérifie les fiches personnages"""
        self.print_header("📄 DIAGNOSTIC: Fiches Personnages")

        fiches_dir = self.base_dir / 'FICHES_PERSONNAGES'

        if not fiches_dir.exists():
            self.log_bug('FICHES', 'Dossier FICHES_PERSONNAGES manquant', 'HIGH')
            return False

        md_files = list(fiches_dir.glob('*.md'))
        md_files = [f for f in md_files if f.name != 'INDEX.md']

        print(f"✓ {len(md_files)} fiches trouvées")

        # Vérifie quelques fiches aléatoirement
        broken_files = []
        for md_file in md_files[:10]:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if len(content) < 100:
                        broken_files.append(md_file.name)
            except:
                broken_files.append(md_file.name)

        if broken_files:
            self.log_bug(
                'FICHES',
                f'{len(broken_files)} fiches potentiellement corrompues',
                'MEDIUM'
            )

        return len(broken_files) == 0

    def check_ai_agents_paths(self):
        """Vérifie les chemins dans les agents IA"""
        self.print_header("🤖 DIAGNOSTIC: Chemins Agents IA")

        files_to_check = [
            'game_monitor.py',
            'launcher_ai_navigator.py',
            'realtime_error_monitor.py'
        ]

        wrong_paths_found = []

        for filename in files_to_check:
            filepath = self.base_dir / filename
            if not filepath.exists():
                print(f"⚠️  {filename} non trouvé")
                continue

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Vérifie les mauvais chemins
            if 'KOF_Ultimate_Online.exe' in content:
                wrong_paths_found.append(f'{filename}: "KOF_Ultimate_Online.exe"')

            if 'D:/KOF Ultimate Online"' in content and 'D:/KOF Ultimate Online' not in content:
                wrong_paths_found.append(f'{filename}: "D:/KOF Ultimate Online"')

        if wrong_paths_found:
            for path_issue in wrong_paths_found:
                self.log_bug('AI_AGENTS', f'Mauvais chemin: {path_issue}', 'HIGH')
        else:
            print("✓ Tous les chemins sont corrects")

        return len(wrong_paths_found) == 0

    def check_game_status(self):
        """Vérifie l'état du jeu"""
        self.print_header("🎮 DIAGNOSTIC: État du Jeu")

        log_file = self.base_dir / 'mugen.log'

        if not log_file.exists():
            self.log_bug('GAME', 'Jeu pas encore lancé (pas de mugen.log)', 'LOW')
            return False

        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            log_content = f.read()

        # Cherche les erreurs
        error_lines = []
        for line in log_content.split('\n'):
            if 'error' in line.lower() or 'fatal' in line.lower():
                error_lines.append(line.strip())

        if error_lines:
            self.log_bug(
                'GAME',
                f'{len(error_lines)} erreurs trouvées dans mugen.log',
                'HIGH'
            )
            for err in error_lines[:5]:  # Montre les 5 premières
                print(f"  → {err}")
        else:
            print("✓ Aucune erreur dans le log du jeu")

        return len(error_lines) == 0

    def check_animation_files(self):
        """Vérifie les fichiers .air"""
        self.print_header("🎨 DIAGNOSTIC: Fichiers Animation")

        chars_dir = self.base_dir / 'chars'

        if not chars_dir.exists():
            self.log_bug('ANIMATIONS', 'Dossier chars/ manquant', 'HIGH')
            return False

        # Compte les fichiers .air
        air_files = list(chars_dir.glob('**/*.air'))
        print(f"✓ {len(air_files)} fichiers .air trouvés")

        # Vérifie quelques fichiers pour erreurs courantes
        issues_found = 0
        for air_file in air_files[:20]:  # Vérifie les 20 premiers
            try:
                with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Cherche erreurs courantes
                if 'Clsn2 [' in content or 'Clsn1 [' in content:
                    issues_found += 1

            except:
                pass

        if issues_found > 0:
            self.log_bug(
                'ANIMATIONS',
                f'{issues_found}/20 fichiers ont encore des espaces dans Clsn',
                'MEDIUM'
            )
        else:
            print("✓ Échantillon de fichiers .air propre")

        return issues_found == 0

    def generate_report(self):
        """Génère le rapport complet"""
        self.print_header("📊 RAPPORT COMPLET DE DIAGNOSTIC")

        total_bugs = len(self.bugs_found)
        high_severity = len([b for b in self.bugs_found if b['severity'] == 'HIGH'])
        medium_severity = len([b for b in self.bugs_found if b['severity'] == 'MEDIUM'])
        low_severity = len([b for b in self.bugs_found if b['severity'] == 'LOW'])

        print(f"Total bugs trouvés: {total_bugs}")
        print(f"  🔴 Haute priorité: {high_severity}")
        print(f"  🟡 Moyenne priorité: {medium_severity}")
        print(f"  🟢 Basse priorité: {low_severity}")
        print()

        if total_bugs == 0:
            print("✅ AUCUN BUG TROUVÉ - SYSTÈME CLEAN!")
        else:
            print("🔧 BUGS PAR CATÉGORIE:")
            categories = {}
            for bug in self.bugs_found:
                cat = bug['category']
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(bug)

            for cat, bugs in categories.items():
                print(f"\n  📁 {cat} ({len(bugs)} bugs)")
                for bug in bugs:
                    print(f"     - {bug['description']}")

        # Sauvegarde le rapport
        report_file = self.base_dir / 'ai_bug_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_bugs': total_bugs,
                'severity_breakdown': {
                    'high': high_severity,
                    'medium': medium_severity,
                    'low': low_severity
                },
                'bugs': self.bugs_found,
                'fixes_applied': self.fixes_applied
            }, f, indent=2, ensure_ascii=False)

        print(f"\n📄 Rapport sauvegardé: {report_file}")

    def run_full_diagnostic(self):
        """Lance le diagnostic complet"""
        print("\n" + "="*80)
        print("  🤖 DIAGNOSTIC COMPLET DES BUGS - COMMUNICATION AI")
        print("="*80)

        # Exécute tous les diagnostics
        self.check_visualizer_cors_issue()
        self.check_character_sheets()
        self.check_ai_agents_paths()
        self.check_game_status()
        self.check_animation_files()

        # Génère le rapport
        self.generate_report()

def main():
    diagnostic = AIBugDiagnostic()
    diagnostic.run_full_diagnostic()

    print("\n" + "="*80)
    input("Appuyez sur Entrée pour fermer...")

if __name__ == '__main__':
    main()
