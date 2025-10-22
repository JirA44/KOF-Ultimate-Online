#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LAUNCH MINI WINDOW TEST - Lance le jeu en mini-fenêtre pour test continu
"""

import os
import sys
import time
import subprocess
from pathlib import Path
import shutil

class MiniWindowLauncher:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.mugen_cfg = self.base_path / "data" / "mugen.cfg"

    def log(self, message):
        print(f"✓ {message}")

    def configure_mini_window(self):
        """Configure le jeu en mode mini-fenêtre"""
        self.log("Configuration du mode mini-fenêtre...")

        if not self.mugen_cfg.exists():
            print("❌ mugen.cfg non trouvé!")
            return False

        # Backup
        backup = self.mugen_cfg.with_suffix('.cfg.mini_backup')
        if not backup.exists():
            shutil.copy2(self.mugen_cfg, backup)
            self.log(f"Backup créé: {backup.name}")

        # Lire le fichier
        content = self.mugen_cfg.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')

        # Modifications pour mini-fenêtre
        changes = {
            'GameWidth': '640',      # Petite résolution
            'GameHeight': '480',
            'FullScreen': '0',       # Mode fenêtré
            'RenderMode': 'OpenGL',
            'VRetrace': '0',
        }

        in_video = False
        for i, line in enumerate(lines):
            if '[Video]' in line:
                in_video = True
                continue
            elif line.startswith('['):
                in_video = False

            if in_video:
                for key, value in changes.items():
                    if line.strip().startswith(key):
                        lines[i] = f'{key} = {value}'
                        self.log(f"Modifié: {key} = {value}")

        # Sauvegarder
        self.mugen_cfg.write_text('\n'.join(lines), encoding='utf-8')
        self.log("Configuration mini-fenêtre appliquée!")
        return True

    def launch_test_instance(self, instance_id):
        """Lance une instance de test"""
        self.log(f"Lancement instance #{instance_id}...")

        # Créer un fichier batch temporaire pour cette instance
        batch_file = self.base_path / f"test_instance_{instance_id}.bat"

        batch_content = f"""@echo off
title KOF Test Instance #{instance_id}
cd /d "D:\\KOF Ultimate Online"

echo ═══════════════════════════════════════
echo   KOF ULTIMATE - Test Instance #{instance_id}
echo ═══════════════════════════════════════
echo.
echo Test en cours...
echo Fenêtre de test automatique - Ne pas fermer
echo.

timeout /t 2 /nobreak >nul
start /MIN "" "KOF_Ultimate_Online.exe"

timeout /t 60 /nobreak >nul
echo Instance #{instance_id} terminée.
"""

        batch_file.write_text(batch_content, encoding='utf-8')

        # Lancer en arrière-plan minimisé
        subprocess.Popen(
            ['cmd', '/c', str(batch_file)],
            creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW
        )

        return True

    def run(self):
        """Lance le système de test en mini-fenêtres"""
        print("\n" + "="*70)
        print("  🪟 MINI WINDOW TEST - KOF ULTIMATE")
        print("="*70 + "\n")

        # Configurer
        if not self.configure_mini_window():
            return False

        print("\n" + "="*70)
        print("  ✓ CONFIGURATION APPLIQUÉE")
        print("="*70 + "\n")

        print("Le jeu est maintenant configuré en mode mini-fenêtre (640x480).")
        print("Vous pouvez le lancer normalement, il apparaîtra en petite fenêtre.")
        print("\nPour restaurer la configuration normale, utilisez le backup:")
        print("  mugen.cfg.mini_backup")

        return True

if __name__ == "__main__":
    launcher = MiniWindowLauncher()
    launcher.run()
