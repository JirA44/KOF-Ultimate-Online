#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - AUTO-LAUNCHER SYSTEM
Lance automatiquement les autocheckers au démarrage
"""

import subprocess
import time
import sys
from pathlib import Path

def run_autocheck():
    """Lance l'autocheck system"""
    print("╔═══════════════════════════════════════════════════════╗")
    print("║   KOF ULTIMATE - AUTO-LAUNCHER                        ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print()
    print("🚀 Lancement automatique de l'autocheck system...")
    print()
    
    try:
        # Run AUTOCHECK_SYSTEM.py
        result = subprocess.run(
            [sys.executable, 'AUTOCHECK_SYSTEM.py'],
            cwd=Path(__file__).parent,
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print()
            print("✅ Autocheck terminé avec succès!")
        else:
            print()
            print("⚠️  Autocheck terminé avec des avertissements")
            
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return 1
    
    print()
    print("=" * 60)
    print("Appuyez sur Entrée pour continuer...")
    input()
    
    return 0

if __name__ == '__main__':
    exit(run_autocheck())
