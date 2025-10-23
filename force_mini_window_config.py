#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Force Mini Window Configuration
S'assure que le jeu est TOUJOURS en mode mini-fenêtre 640x480 sans son
À EXÉCUTER AVANT tout lancement de jeu
"""

from pathlib import Path
import re

def force_mini_window_mode(game_dir):
    """Force le mode mini-fenêtre dans toutes les configs"""
    game_dir = Path(game_dir)

    configs_modified = []

    # 1. mugen.cfg (config principale)
    mugen_cfg = game_dir / "data" / "mugen.cfg"
    if mugen_cfg.exists():
        print(f"📝 Configuration de {mugen_cfg}...")

        with open(mugen_cfg, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Sauvegarder l'original
        backup = game_dir / "data" / "mugen.cfg.backup_original"
        if not backup.exists():
            with open(backup, 'w', encoding='utf-8') as f:
                f.write(content)

        # Modifications forcées
        modifications = {
            r'FullScreen\s*=\s*\d+': 'FullScreen = 0',
            r'GameWidth\s*=\s*\d+': 'GameWidth = 640',
            r'GameHeight\s*=\s*\d+': 'GameHeight = 480',
            r'MasterWavVolume\s*=\s*\d+': 'MasterWavVolume = 0',
            r'MasterMIDIVolume\s*=\s*\d+': 'MasterMIDIVolume = 0',
            r'MP3Volume\s*=\s*\d+': 'MP3Volume = 0'
        }

        for pattern, replacement in modifications.items():
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

        # Ajouter si manquant
        if 'FullScreen' not in content:
            content += '\n\n[Video]\nFullScreen = 0\nGameWidth = 640\nGameHeight = 480\n'

        if 'MasterWavVolume' not in content:
            content += '\n\n[Sound]\nMasterWavVolume = 0\nMasterMIDIVolume = 0\nMP3Volume = 0\n'

        with open(mugen_cfg, 'w', encoding='utf-8') as f:
            f.write(content)

        configs_modified.append(str(mugen_cfg))
        print("   ✅ Forcé: 640x480 fenêtré, son = 0")

    # 2. Vérifier Ikemen GO config
    ikemen_config = game_dir / "Ikemen_GO" / "save" / "config.json"
    if ikemen_config.exists():
        import json

        print(f"📝 Configuration de {ikemen_config}...")

        with open(ikemen_config, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Sauvegarder l'original
        backup = game_dir / "Ikemen_GO" / "save" / "config.json.backup_original"
        if not backup.exists():
            with open(backup, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)

        # Forcer paramètres
        if 'System' not in config:
            config['System'] = {}

        config['System']['Fullscreen'] = False
        config['System']['GameWidth'] = 640
        config['System']['GameHeight'] = 480

        if 'Audio' not in config:
            config['Audio'] = {}

        config['Audio']['MasterVolume'] = 0
        config['Audio']['SFXVolume'] = 0
        config['Audio']['BGMVolume'] = 0

        with open(ikemen_config, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

        configs_modified.append(str(ikemen_config))
        print("   ✅ Forcé: 640x480 fenêtré, volumes = 0")

    # Rapport
    print(f"\n{'='*60}")
    print("✅ CONFIGURATION FORCÉE: MODE MINI-FENÊTRE")
    print(f"{'='*60}")
    print("📏 Résolution: 640x480")
    print("🖼️  Mode: Fenêtré")
    print("🔇 Son: Désactivé")
    print(f"\n📝 {len(configs_modified)} fichier(s) modifié(s):")
    for config_file in configs_modified:
        print(f"   - {Path(config_file).name}")

    print(f"\n💾 Backups sauvegardés avec extension .backup_original")
    print(f"{'='*60}\n")

    return configs_modified

if __name__ == '__main__':
    game_dir = r"D:\KOF Ultimate Online"
    force_mini_window_mode(game_dir)
    print("✅ Configuration terminée - Le jeu lancera en mini-fenêtre")
