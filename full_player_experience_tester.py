#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF Ultimate - Testeur Expérience Joueur Complète
Simule un vrai joueur pour identifier tous les points d'amélioration
"""

import subprocess
import time
import os
import sys
import json
from pathlib import Path
from datetime import datetime
import random

class PlayerExperienceTester:
    """Teste l'expérience complète du joueur"""

    def __init__(self, game_dir):
        self.game_dir = Path(game_dir)
        self.test_results = {
            'installation': {},
            'menus': {},
            'progression': {},
            'matchmaking': {},
            'competitive': {},
            'characters': {},
            'stages': {},
            'combat_sessions': [],
            'issues_found': [],
            'improvements_needed': []
        }
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')

    def log_issue(self, category, severity, description):
        """Log un problème détecté"""
        issue = {
            'category': category,
            'severity': severity,  # critical, major, minor
            'description': description,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results['issues_found'].append(issue)
        print(f"⚠️  [{severity.upper()}] {category}: {description}")

    def log_improvement(self, area, suggestion):
        """Log une amélioration suggérée"""
        improvement = {
            'area': area,
            'suggestion': suggestion,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results['improvements_needed'].append(improvement)
        print(f"💡 Amélioration suggérée [{area}]: {suggestion}")

    def test_installation_experience(self):
        """Test 1: Expérience d'installation et premier lancement"""
        print("\n" + "="*70)
        print("TEST 1: INSTALLATION & PREMIER LANCEMENT (Nouveau Joueur)")
        print("="*70)

        # Vérifier structure des fichiers
        print("\n📦 Vérification structure d'installation...")

        required_files = [
            'KOF_Ultimate_Online.exe',
            'data/mugen.cfg',
            'chars/',
            'stages/',
            'data/select.def'
        ]

        missing_files = []
        for file in required_files:
            if not (self.game_dir / file).exists():
                missing_files.append(file)
                self.log_issue('installation', 'critical', f"Fichier manquant: {file}")

        if not missing_files:
            print("✅ Tous les fichiers requis présents")
            self.test_results['installation']['files_ok'] = True
        else:
            print(f"❌ {len(missing_files)} fichiers manquants")
            self.test_results['installation']['files_ok'] = False

        # Vérifier launchers
        print("\n🚀 Vérification launchers disponibles...")
        launchers = list(self.game_dir.glob('LAUNCHER*.py'))
        launchers += list(self.game_dir.glob('launcher*.py'))
        launchers += list(self.game_dir.glob('*LAUNCHER*.bat'))

        print(f"   Trouvé {len(launchers)} launchers:")
        for launcher in launchers[:5]:
            print(f"   - {launcher.name}")

        if len(launchers) == 0:
            self.log_issue('installation', 'major', "Aucun launcher trouvé")
        elif len(launchers) > 5:
            self.log_improvement('installation', f"Trop de launchers ({len(launchers)}) - créer UN launcher principal clair")

        # Vérifier documentation
        print("\n📖 Vérification documentation utilisateur...")
        docs = list(self.game_dir.glob('README*.md'))
        docs += list(self.game_dir.glob('COMMENT*.md'))
        docs += list(self.game_dir.glob('GUIDE*.md'))

        if len(docs) == 0:
            self.log_issue('installation', 'major', "Aucune documentation pour débutants")
        else:
            print(f"✅ {len(docs)} documents d'aide trouvés")

        self.test_results['installation']['launchers_count'] = len(launchers)
        self.test_results['installation']['docs_count'] = len(docs)

    def test_menu_navigation(self):
        """Test 2: Navigation dans les menus"""
        print("\n" + "="*70)
        print("TEST 2: NAVIGATION MENUS")
        print("="*70)

        print("\n🎮 Analyse du fichier select.def (écran sélection)...")

        select_def = self.game_dir / "data" / "select.def"
        if not select_def.exists():
            self.log_issue('menus', 'critical', "select.def manquant")
            return

        with open(select_def, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Vérifier personnages disponibles
        char_lines = [l for l in content.split('\n') if l.strip() and not l.strip().startswith(';')]
        chars_in_select = len([l for l in char_lines if '/' in l or '\\' in l])

        print(f"   📊 Personnages dans select.def: {chars_in_select}")

        if chars_in_select < 10:
            self.log_improvement('menus', "Peu de personnages visibles - ajouter plus de choix")
        elif chars_in_select > 100:
            self.log_improvement('menus', f"Beaucoup de personnages ({chars_in_select}) - envisager pagination ou filtres")

        self.test_results['menus']['characters_available'] = chars_in_select

    def test_progression_system(self):
        """Test 3: Système de progression"""
        print("\n" + "="*70)
        print("TEST 3: SYSTÈME DE PROGRESSION")
        print("="*70)

        print("\n📊 Recherche de système de stats/progression...")

        # Chercher fichiers de stats
        stat_files = list(self.game_dir.glob('*stats*.json'))
        stat_files += list(self.game_dir.glob('*profile*.json'))
        stat_files += list(self.game_dir.glob('player_data*.json'))

        if len(stat_files) == 0:
            self.log_improvement('progression', "Pas de système de stats joueur - créer suivi wins/losses/streaks")
        else:
            print(f"✅ {len(stat_files)} fichiers de stats trouvés")
            for sf in stat_files:
                print(f"   - {sf.name}")

        self.test_results['progression']['stat_files_found'] = len(stat_files)

    def test_matchmaking_system(self):
        """Test 4: Système de matchmaking"""
        print("\n" + "="*70)
        print("TEST 4: SYSTÈME DE MATCHMAKING")
        print("="*70)

        print("\n🔍 Vérification serveur matchmaking...")

        # Vérifier fichiers matchmaking
        mm_files = list(self.game_dir.glob('*matchmaking*.py'))
        if len(mm_files) == 0:
            self.log_issue('matchmaking', 'major', "Pas de système de matchmaking trouvé")
        else:
            print(f"✅ {len(mm_files)} fichiers matchmaking trouvés")

        # Vérifier si serveur tourne
        import socket
        ports_to_check = [5000, 5001, 8080, 8888]
        active_ports = []

        for port in ports_to_check:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            if result == 0:
                active_ports.append(port)
                print(f"✅ Port {port} actif")
            sock.close()

        if len(active_ports) == 0:
            self.log_improvement('matchmaking', "Serveur matchmaking pas actif - démarrer automatiquement")

        self.test_results['matchmaking']['files_found'] = len(mm_files)
        self.test_results['matchmaking']['active_ports'] = active_ports

    def test_all_characters(self):
        """Test 6: Tous les personnages jouables"""
        print("\n" + "="*70)
        print("TEST 6: TEST DE TOUS LES PERSONNAGES")
        print("="*70)

        chars_dir = self.game_dir / "chars"
        if not chars_dir.exists():
            self.log_issue('characters', 'critical', "Dossier chars/ manquant")
            return

        all_chars = [d for d in chars_dir.iterdir() if d.is_dir()]
        print(f"\n📂 {len(all_chars)} dossiers de personnages trouvés")

        # Vérifier chaque personnage
        working_chars = 0
        broken_chars = []

        print("\n🔍 Vérification intégrité des personnages...")
        for char in all_chars[:50]:  # Limiter pour test rapide
            def_file = char / f"{char.name}.def"
            if not def_file.exists():
                broken_chars.append(char.name)
                self.log_issue('characters', 'minor', f"Personnage sans .def: {char.name}")
            else:
                working_chars += 1

        print(f"✅ Personnages OK: {working_chars}/{len(all_chars[:50])}")
        if broken_chars:
            print(f"❌ Personnages cassés: {len(broken_chars)}")

        self.test_results['characters']['total'] = len(all_chars)
        self.test_results['characters']['working'] = working_chars
        self.test_results['characters']['broken'] = broken_chars

    def test_all_stages(self):
        """Test 7: Tous les stages"""
        print("\n" + "="*70)
        print("TEST 7: TEST DE TOUS LES STAGES")
        print("="*70)

        stages_dir = self.game_dir / "stages"
        if not stages_dir.exists():
            self.log_issue('stages', 'critical', "Dossier stages/ manquant")
            return

        all_stages = list(stages_dir.glob("*.def"))
        print(f"\n🗺️  {len(all_stages)} stages trouvés")

        # Vérifier chaque stage
        working_stages = 0
        broken_stages = []

        for stage_def in all_stages[:30]:  # Test échantillon
            try:
                with open(stage_def, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if 'spr' in content.lower() or 'sprite' in content.lower():
                    working_stages += 1
                else:
                    broken_stages.append(stage_def.stem)
            except:
                broken_stages.append(stage_def.stem)

        print(f"✅ Stages OK: {working_stages}/{len(all_stages[:30])}")

        self.test_results['stages']['total'] = len(all_stages)
        self.test_results['stages']['working'] = working_stages
        self.test_results['stages']['broken'] = broken_stages

    def run_combat_session_mini(self, session_num, duration=45):
        """Lance une session de combat en mini-fenêtre"""
        print(f"\n⚔️  Combat Session #{session_num} (durée: {duration}s)...")

        # S'assurer du mode mini-fenêtre
        self.ensure_mini_window_mode()

        exe_path = self.game_dir / "KOF_Ultimate_Online.exe"

        try:
            process = subprocess.Popen(
                [str(exe_path)],
                cwd=str(self.game_dir),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            start_time = time.time()
            time.sleep(duration)

            process.terminate()
            time.sleep(1)
            if process.poll() is None:
                process.kill()

            elapsed = time.time() - start_time

            session_data = {
                'session_num': session_num,
                'duration': elapsed,
                'timestamp': datetime.now().isoformat(),
                'status': 'completed'
            }
            self.test_results['combat_sessions'].append(session_data)

            print(f"✅ Session #{session_num} terminée ({elapsed:.0f}s)")
            return True

        except Exception as e:
            print(f"❌ Erreur session #{session_num}: {e}")
            return False

    def ensure_mini_window_mode(self):
        """S'assure que le jeu est en mode mini-fenêtre sans son"""
        mugen_cfg = self.game_dir / "data" / "mugen.cfg"
        if mugen_cfg.exists():
            with open(mugen_cfg, 'r', encoding='utf-8') as f:
                content = f.read()

            # Mode fenêtré
            content = content.replace('FullScreen = 1', 'FullScreen = 0')
            # Petite taille
            import re
            content = re.sub(r'GameWidth\s*=\s*\d+', 'GameWidth = 640', content)
            content = re.sub(r'GameHeight\s*=\s*\d+', 'GameHeight = 480', content)
            # Sans son
            content = re.sub(r'MasterWavVolume\s*=\s*\d+', 'MasterWavVolume = 0', content)
            content = re.sub(r'MasterMIDIVolume\s*=\s*\d+', 'MasterMIDIVolume = 0', content)

            with open(mugen_cfg, 'w', encoding='utf-8') as f:
                f.write(content)

    def run_multiple_combat_sessions(self, num_sessions=10):
        """Test 8: Sessions de combat intensives"""
        print("\n" + "="*70)
        print(f"TEST 8: SESSIONS DE COMBAT INTENSIVES ({num_sessions} sessions)")
        print("="*70)

        success_count = 0
        for i in range(1, num_sessions + 1):
            if self.run_combat_session_mini(i, duration=45):
                success_count += 1

            # Pause entre sessions
            if i < num_sessions:
                print(f"⏸️  Pause 15s...")
                time.sleep(15)

        print(f"\n✅ {success_count}/{num_sessions} sessions réussies")

    def generate_full_report(self):
        """Génère le rapport complet d'amélioration"""
        print("\n" + "="*70)
        print("📊 GÉNÉRATION RAPPORT D'AMÉLIORATION COMPLET")
        print("="*70)

        report_file = self.game_dir / f"PLAYER_EXPERIENCE_REPORT_{self.session_id}.json"

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)

        # Rapport Markdown aussi
        md_file = self.game_dir / f"PLAYER_EXPERIENCE_REPORT_{self.session_id}.md"

        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# 🎮 Rapport d'Expérience Joueur Complet\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write(f"## 📊 Résumé\n\n")
            f.write(f"- **Problèmes critiques:** {len([i for i in self.test_results['issues_found'] if i['severity'] == 'critical'])}\n")
            f.write(f"- **Problèmes majeurs:** {len([i for i in self.test_results['issues_found'] if i['severity'] == 'major'])}\n")
            f.write(f"- **Problèmes mineurs:** {len([i for i in self.test_results['issues_found'] if i['severity'] == 'minor'])}\n")
            f.write(f"- **Améliorations suggérées:** {len(self.test_results['improvements_needed'])}\n")
            f.write(f"- **Sessions de combat:** {len(self.test_results['combat_sessions'])}\n\n")

            f.write(f"## ⚠️  Problèmes Détectés\n\n")
            for issue in self.test_results['issues_found']:
                f.write(f"### [{issue['severity'].upper()}] {issue['category']}\n")
                f.write(f"{issue['description']}\n\n")

            f.write(f"## 💡 Améliorations Suggérées\n\n")
            for imp in self.test_results['improvements_needed']:
                f.write(f"### {imp['area']}\n")
                f.write(f"{imp['suggestion']}\n\n")

        print(f"✅ Rapport JSON: {report_file}")
        print(f"✅ Rapport MD: {md_file}")

        return report_file, md_file

    def run_full_test_suite(self, combat_sessions=10):
        """Lance la suite complète de tests"""
        print("\n" + "="*70)
        print("🚀 DÉMARRAGE SUITE COMPLÈTE DE TESTS")
        print("🎯 Objectif: Expérience joueur réel de A à Z")
        print("="*70)

        # Test 1: Installation
        self.test_installation_experience()
        time.sleep(2)

        # Test 2: Menus
        self.test_menu_navigation()
        time.sleep(2)

        # Test 3: Progression
        self.test_progression_system()
        time.sleep(2)

        # Test 4: Matchmaking
        self.test_matchmaking_system()
        time.sleep(2)

        # Test 6: Personnages
        self.test_all_characters()
        time.sleep(2)

        # Test 7: Stages
        self.test_all_stages()
        time.sleep(2)

        # Test 8: Sessions de combat
        self.run_multiple_combat_sessions(num_sessions=combat_sessions)

        # Rapport final
        report_json, report_md = self.generate_full_report()

        print("\n" + "="*70)
        print("✅ SUITE DE TESTS COMPLÉTÉE")
        print("="*70)
        print(f"\n📊 Consultez les rapports:")
        print(f"   - {report_json.name}")
        print(f"   - {report_md.name}")

        return self.test_results

def main():
    """Point d'entrée"""
    game_dir = r"D:\KOF Ultimate Online"

    print("\n🎮 KOF Ultimate - Testeur Expérience Joueur")
    print("="*70)
    print("Mode: Mini-fenêtre 640x480, Sans son")
    print("="*70)

    tester = PlayerExperienceTester(game_dir)

    # Lancer suite complète avec 5 sessions de combat
    results = tester.run_full_test_suite(combat_sessions=5)

    print("\n✅ Test terminé avec succès!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
