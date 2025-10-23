"""
ML Continuous Improver - KOF Ultimate Online
Lance l'amélioration continue des joueurs virtuels
"""

import time
import os
import json
from datetime import datetime
from ml_improvement_system import MLImprovementSystem
from virtual_players_ai import VirtualPlayerAI

def load_all_players():
    """Charge tous les joueurs virtuels depuis les profils sauvegardés"""
    players = []

    if not os.path.exists('player_profiles'):
        print("⚠️  Aucun profil de joueur trouvé")
        return players

    profile_files = [f for f in os.listdir('player_profiles') if f.endswith('.json')]

    print(f"\n📁 Chargement de {len(profile_files)} profils de joueurs...")

    for filename in profile_files:
        try:
            filepath = os.path.join('player_profiles', filename)

            with open(filepath, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)

            # Créer un joueur virtuel et charger son profil
            player_id = profile_data.get('player_id', 0)
            player = VirtualPlayerAI(player_id)
            player.profile = profile_data
            player.name = profile_data['name']

            players.append(player)

        except Exception as e:
            print(f"❌ Erreur lors du chargement de {filename}: {e}")

    print(f"✅ {len(players)} joueurs chargés\n")
    return players


def main():
    """Programme principal d'amélioration continue"""
    print("\n" + "="*60)
    print("  🧠 SYSTÈME D'AMÉLIORATION CONTINUE ML")
    print("="*60)
    print("\n  Ce système analyse et améliore automatiquement")
    print("  les joueurs virtuels toutes les 30 minutes\n")
    print("="*60 + "\n")

    # Créer le système ML
    ml_system = MLImprovementSystem()
    ml_system.load_meta()

    # Attendre que les profils de joueurs soient créés
    print("⏳ Attente de la création des profils de joueurs...")
    time.sleep(15)  # Attendre 15 secondes

    try:
        while True:
            # Charger tous les joueurs
            players = load_all_players()

            if len(players) == 0:
                print("⚠️  Aucun joueur trouvé, attente de 60 secondes...")
                time.sleep(60)
                continue

            # Exécuter un cycle d'apprentissage
            print(f"\n🎓 Exécution du cycle d'apprentissage sur {len(players)} joueurs...")
            session = ml_system.run_learning_cycle(players)

            # Sauvegarder les profils améliorés
            print("\n💾 Sauvegarde des profils améliorés...")
            for player in players:
                player.save_profile()

            # Sauvegarder les métadonnées
            ml_system.save_meta()

            # Afficher le rapport
            print(ml_system.generate_improvement_report())

            # Attendre 30 minutes avant le prochain cycle
            print("\n⏳ Prochain cycle dans 30 minutes...")
            print("   (Appuyez sur Ctrl+C pour arrêter)\n")
            time.sleep(30 * 60)  # 30 minutes

    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt du système d'amélioration continue...")
        ml_system.save_meta()
        print("✅ Métadonnées sauvegardées!")
        print("\n👋 Au revoir!\n")


if __name__ == "__main__":
    main()
