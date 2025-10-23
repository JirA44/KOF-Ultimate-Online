#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST RAPIDE - Joueur Virtuel
Test de 2 minutes pour vérifier que tout fonctionne
"""

import sys
sys.path.insert(0, r'D:\KOF Ultimate Online')

from VIRTUAL_PLAYERS_CONTINUOUS import VirtualPlayer
from pathlib import Path
import time

def quick_test():
    print("\n" + "="*70)
    print("  🧪 TEST RAPIDE - JOUEUR VIRTUEL")
    print("="*70 + "\n")

    game_dir = r"D:\KOF Ultimate Online"

    print("Configuration du test:")
    print(f"  • Durée: 2 minutes")
    print(f"  • Joueur: TestPlayer1")
    print(f"  • Personnalité: Balanced")
    print()

    # Créer un joueur virtuel
    player = VirtualPlayer(
        player_id=999,
        name="TestPlayer1",
        game_dir=game_dir,
        personality="balanced"
    )

    print("✅ Joueur virtuel créé!")
    print()

    input("▶️  Le jeu doit être lancé et au menu principal. Appuyez sur ENTRÉE pour commencer le test...")

    try:
        print("\n🎮 Démarrage du test...\n")

        # Test 1: Navigation vers un mode
        print("Test 1: Navigation menu...")
        player.navigate_to_mode_from_menu("Versus")
        time.sleep(2)

        # Test 2: Sélection de personnage
        print("Test 2: Sélection personnage...")
        player.select_characters(1)
        time.sleep(2)

        # Test 3: Sélection de stage
        print("Test 3: Sélection stage...")
        player.select_stage()
        time.sleep(2)

        # Test 4: Combat pendant 30 secondes
        print("Test 4: Combat (30 secondes)...")
        player.play_match(30)

        # Test 5: Post-match
        print("Test 5: Gestion post-match...")
        player.handle_post_match()

        print("\n" + "="*70)
        print("✅ TEST TERMINÉ AVEC SUCCÈS!")
        print("="*70)

        # Afficher les stats
        player.print_summary()

        # Sauvegarder
        player.save_stats()

    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu")
    except Exception as e:
        print(f"\n❌ Erreur pendant le test: {e}")
        import traceback
        traceback.print_exc()

    print("\nFichiers générés:")
    print(f"  • Logs: {player.logs_dir}")
    print(f"  • Screenshots: {player.screenshots_dir}")
    print()

if __name__ == "__main__":
    quick_test()
