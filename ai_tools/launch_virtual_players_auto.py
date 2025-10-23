#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-Launch Virtual Players - No interaction needed
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from virtual_players_session import MultiplayerSession

def main():
    """Auto-launch with default settings"""
    game_dir = r"D:\KOF Ultimate Online"
    num_players = 2
    duration = 30

    print(f"🚀 Lancement automatique:")
    print(f"   - Joueurs: {num_players}")
    print(f"   - Durée: {duration}s")
    print(f"   - Répertoire: {game_dir}\n")

    session = MultiplayerSession(game_dir, num_players=num_players)
    success = session.run_full_session(match_duration=duration)

    return 0 if success else 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Programme arrêté")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
