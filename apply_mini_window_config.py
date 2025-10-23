#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour appliquer la configuration mini-fenêtre
Usage: python apply_mini_window_config.py [width] [height]
Par défaut: 800x600
"""

import sys
import re
from pathlib import Path

def apply_mini_window_config(width=800, height=600):
    """Applique la config mini-fenêtre"""

    config_file = Path("data/mugen.cfg")

    if not config_file.exists():
        print("[ERROR] mugen.cfg introuvable!")
        return False

    # Lire la config
    with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
        config = f.read()

    # Appliquer les changements
    config = re.sub(r'fullscreen\s*=\s*\d+', 'fullscreen = 0', config)
    config = re.sub(r'(?<=\[Video\]\n(?:.*\n)*?)width\s*=\s*\d+', f'width = {width}', config, flags=re.MULTILINE)
    config = re.sub(r'(?<=\[Video\]\n(?:.*\n)*?)height\s*=\s*\d+', f'height = {height}', config, flags=re.MULTILINE)
    config = re.sub(r'vretrace\s*=\s*\d+', 'vretrace = 0', config)

    # Version simple qui fonctionne toujours
    config = config.replace('fullscreen = 1', 'fullscreen = 0')
    if 'vretrace = 1' in config:
        config = config.replace('vretrace = 1', 'vretrace = 0')

    # Modifier la section [Video] spécifiquement
    lines = config.split('\n')
    in_video_section = False
    result = []

    for line in lines:
        if line.strip() == '[Video]':
            in_video_section = True
            result.append(line)
        elif in_video_section and line.strip().startswith('['):
            in_video_section = False
            result.append(line)
        elif in_video_section:
            if line.strip().startswith('width'):
                result.append(f'width = {width}')
            elif line.strip().startswith('height'):
                result.append(f'height = {height}')
            else:
                result.append(line)
        else:
            result.append(line)

    config = '\n'.join(result)

    # Écrire la nouvelle config
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config)

    print(f'[OK] Mini-fenêtre configurée: {width}x{height}')
    return True

if __name__ == "__main__":
    width = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    height = int(sys.argv[2]) if len(sys.argv) > 2 else 600

    success = apply_mini_window_config(width, height)
    sys.exit(0 if success else 1)
