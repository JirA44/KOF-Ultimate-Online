#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entraînement IA Continu - Mode Mini-Fenêtre Sans Son
Lance des sessions d'entraînement en arrière-plan de façon non-intrusive
"""

import subprocess
import time
import os
import sys
from pathlib import Path
from datetime import datetime

class AITrainingSystem:
    """Système d'entraînement automatique des IAs"""

    def __init__(self, game_dir):
        self.game_dir = Path(game_dir)
        self.sessions_count = 0
        self.training_log = []

    def configure_mini_window_mode(self):
        """Configure le jeu en mode mini-fenêtre sans son"""
        mugen_cfg = self.game_dir / "data" / "mugen.cfg"

        if mugen_cfg.exists():
            print("📝 Configuration mode mini-fenêtre + sans son...")

            with open(mugen_cfg, 'r', encoding='utf-8') as f:
                content = f.read()

            # Forcer mode fenêtré petit
            content = content.replace('FullScreen = 1', 'FullScreen = 0')
            content = content.replace('GameWidth = 1280', 'GameWidth = 640')
            content = content.replace('GameHeight = 720', 'GameHeight = 480')

            # Désactiver le son
            if 'MasterWavVolume' in content:
                import re
                content = re.sub(r'MasterWavVolume\s*=\s*\d+', 'MasterWavVolume = 0', content)

            if 'MasterMIDIVolume' in content:
                import re
                content = re.sub(r'MasterMIDIVolume\s*=\s*\d+', 'MasterMIDIVolume = 0', content)

            with open(mugen_cfg, 'w', encoding='utf-8') as f:
                f.write(content)

            print("✅ Configuration appliquée: 640x480 fenêtré, son = 0")

    def launch_training_session(self, session_id, duration=60):
        """Lance une session d'entraînement"""
        print(f"\n{'='*60}")
        print(f"🤖 SESSION #{session_id} - Entraînement IA")
        print(f"{'='*60}")
        print(f"⏱️  Durée: {duration}s")
        print(f"🖼️  Mode: Mini-fenêtre 640x480")
        print(f"🔇 Son: Désactivé")
        print(f"⏰ Début: {datetime.now().strftime('%H:%M:%S')}\n")

        # Lancer le jeu en mode auto avec IA
        exe_path = self.game_dir / "KOF_Ultimate_Online.exe"

        try:
            process = subprocess.Popen(
                [str(exe_path)],
                cwd=str(self.game_dir),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            print(f"✅ Processus lancé (PID: {process.pid})")
            print(f"⏳ Entraînement en cours...")

            # Attendre la durée de la session
            time.sleep(duration)

            # Terminer proprement
            process.terminate()
            time.sleep(2)

            if process.poll() is None:
                process.kill()

            print(f"✅ Session #{session_id} terminée")

            # Logger
            self.training_log.append({
                'session': session_id,
                'duration': duration,
                'timestamp': datetime.now(),
                'status': 'completed'
            })

            return True

        except Exception as e:
            print(f"❌ Erreur session #{session_id}: {e}")
            return False

    def run_continuous_training(self, num_sessions=10, session_duration=60, pause_between=30):
        """Lance plusieurs sessions d'entraînement"""
        print(f"\n{'='*60}")
        print(f"🚀 DÉMARRAGE ENTRAÎNEMENT CONTINU")
        print(f"{'='*60}")
        print(f"📊 Nombre de sessions: {num_sessions}")
        print(f"⏱️  Durée par session: {session_duration}s")
        print(f"⏸️  Pause entre sessions: {pause_between}s")
        print(f"{'='*60}\n")

        # Configurer d'abord
        self.configure_mini_window_mode()

        time.sleep(2)

        # Lancer les sessions
        for i in range(1, num_sessions + 1):
            success = self.launch_training_session(i, session_duration)
            self.sessions_count += 1

            if success and i < num_sessions:
                print(f"\n⏸️  Pause {pause_between}s avant prochaine session...\n")
                time.sleep(pause_between)

        # Rapport final
        self.show_training_report()

    def show_training_report(self):
        """Affiche le rapport d'entraînement"""
        print(f"\n{'='*60}")
        print(f"📊 RAPPORT D'ENTRAÎNEMENT")
        print(f"{'='*60}")
        print(f"✅ Sessions complétées: {len([s for s in self.training_log if s['status'] == 'completed'])}")
        print(f"📈 Total sessions: {self.sessions_count}")
        print(f"⏰ Terminé: {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}\n")

        # Sauvegarder le log
        log_file = self.game_dir / "training_sessions.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            for session in self.training_log:
                f.write(f"{session['timestamp']} - Session {session['session']}: {session['status']}\n")

        print(f"📝 Logs sauvegardés: {log_file}")

def main():
    """Point d'entrée"""
    game_dir = r"D:\KOF Ultimate Online"

    print("\n🤖 Système d'Entraînement IA - Mode Non-Intrusif")
    print("=" * 60)

    trainer = AITrainingSystem(game_dir)

    # Configuration par défaut: 5 sessions de 60s, pause 20s
    # Mode discret: mini-fenêtre + sans son
    trainer.run_continuous_training(
        num_sessions=5,
        session_duration=60,
        pause_between=20
    )

    print("\n✅ Entraînement terminé avec succès!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Entraînement interrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
