#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SYSTÈME DE MONITORING ET CORRECTION EN TEMPS RÉEL
Surveille mugen.log, détecte les erreurs et les corrige automatiquement
"""

import re
import time
import subprocess
from pathlib import Path
import shutil
import psutil

class RealtimeMonitor:
    def __init__(self, game_dir):
        self.game_dir = Path(game_dir)
        self.mugen_log = self.game_dir / "mugen.log"
        self.chars_dir = self.game_dir / "chars"
        self.game_exe = self.game_dir / "KOF_Ultimate_Online.exe"

        self.errors_detected = []
        self.errors_fixed = []
        self.last_log_size = 0

    def is_game_running(self):
        """Vérifie si le jeu est en cours d'exécution"""
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'KOF_Ultimate_Online.exe':
                return True
        return False

    def wait_for_game_to_close(self):
        """Attend que le jeu se ferme"""
        while self.is_game_running():
            time.sleep(0.5)

    def scan_log_for_errors(self):
        """Scanne le log pour trouver de nouvelles erreurs"""
        if not self.mugen_log.exists():
            return []

        try:
            with open(self.mugen_log, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Trouver toutes les erreurs .air
            pattern = r'Error in ([^\s:]+\.air):(\d+)'
            matches = re.findall(pattern, content)

            new_errors = []
            for air_file, line_num in matches:
                error_key = f"{air_file}:{line_num}"
                if error_key not in self.errors_detected:
                    new_errors.append((air_file, line_num))
                    self.errors_detected.append(error_key)

            return new_errors

        except Exception as e:
            print(f"❌ Erreur lecture log: {e}")
            return []

    def fix_air_file(self, air_filename):
        """Corrige un fichier .air"""
        matches = list(self.chars_dir.glob(f"**/{air_filename}"))

        for file_path in matches:
            print(f"  🔧 Correction de {file_path.name}...")
            try:
                # Lire le fichier
                content = None
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                            content = f.read()
                        break
                    except:
                        continue

                if content is None:
                    continue

                # Backup
                backup_path = file_path.with_suffix('.air.backup_rtfix')
                if not backup_path.exists():
                    shutil.copy2(file_path, backup_path)

                # Corriger les erreurs Clsn
                fixed = self.fix_clsn_in_content(content)

                # Sauvegarder
                with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(fixed)

                print(f"    ✅ {file_path.name} corrigé!")
                self.errors_fixed.append(air_filename)
                return True

            except Exception as e:
                print(f"    ❌ Erreur: {e}")
                continue

        return False

    def fix_clsn_in_content(self, content):
        """Corrige les erreurs Clsn dans le contenu"""
        lines = content.split('\n')
        new_lines = []

        i = 0
        while i < len(lines):
            line = lines[i]

            # Détecter [Begin Action XXX]
            if line.strip().startswith('[Begin Action'):
                new_lines.append(line)
                i += 1

                # Chercher Clsn: 0
                while i < len(lines) and not lines[i].strip().startswith('['):
                    current = lines[i].strip()

                    # Si Clsn: 0 suivi d'une image
                    if re.match(r'(Clsn[12]):\s*0\s*$', current):
                        if i + 1 < len(lines):
                            next_line = lines[i + 1].strip()
                            if re.match(r'^\d+,', next_line):
                                clsn_type = re.match(r'(Clsn[12]):', current).group(1)
                                new_lines.append(f"{clsn_type}: 1")
                                new_lines.append(f"{clsn_type}[0] = -10, -90, 10, 0")
                                i += 1
                                continue

                    # Si Clsn avec Loopstart mal placé
                    if 'Loopstart' in current or 'LoopStart' in current:
                        cleaned = re.sub(r'\s*(Loopstart|LoopStart)\s*', '', current, flags=re.IGNORECASE)
                        if cleaned:
                            new_lines.append(cleaned)
                        new_lines.append("Loopstart")
                        i += 1
                        continue

                    new_lines.append(lines[i])
                    i += 1
                continue

            new_lines.append(line)
            i += 1

        return '\n'.join(new_lines)

    def run_monitoring(self, duration=1800):
        """Lance le monitoring en temps réel"""
        print("=" * 80)
        print(" " * 15 + "🔍 MONITORING TEMPS RÉEL DES ERREURS .AIR")
        print("=" * 80)
        print()
        print(f"⏱️  Durée: {duration}s (~{duration // 60} minutes)")
        print(f"📁 Dossier: {self.game_dir}")
        print(f"📋 Log: {self.mugen_log.name}")
        print()
        print("🚀 Monitoring démarré! Lancez le jeu ou les tests.")
        print("   Les erreurs seront détectées et corrigées automatiquement.")
        print()

        start_time = time.time()
        last_check = 0

        while time.time() - start_time < duration:
            # Scanner toutes les 2 secondes
            if time.time() - last_check >= 2:
                errors = self.scan_log_for_errors()

                if errors:
                    print(f"\n⚠️  {len(errors)} nouvelles erreurs détectées!")
                    for air_file, line_num in errors:
                        print(f"  • {air_file}:{line_num}")
                        self.fix_air_file(air_file)

                last_check = time.time()

            time.sleep(0.5)

        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ DU MONITORING")
        print("=" * 80)
        print(f"Erreurs détectées: {len(self.errors_detected)}")
        print(f"Fichiers corrigés: {len(set(self.errors_fixed))}")
        print()
        print("✅ MONITORING TERMINÉ!")

def main():
    game_dir = r"D:\KOF Ultimate Online"
    monitor = RealtimeMonitor(game_dir)

    # Lancer en mode monitoring pendant 30 minutes
    monitor.run_monitoring(duration=1800)

if __name__ == '__main__':
    main()
