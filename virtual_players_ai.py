"""
Joueurs Virtuels IA - KOF Ultimate Online
Crée des joueurs virtuels intelligents qui s'améliorent en continu
"""

import json
import random
import time
import socket
from datetime import datetime
from collections import defaultdict
import os

class VirtualPlayerAI:
    """IA d'un joueur virtuel qui apprend et s'améliore"""

    def __init__(self, player_id, skill_level='intermediate'):
        self.player_id = player_id
        self.name = self.generate_name()
        self.skill_level = skill_level  # beginner, intermediate, advanced, expert, master

        # Profil du joueur
        self.profile = {
            'player_id': player_id,
            'name': self.name,
            'created_at': datetime.now().isoformat(),
            'stats': {
                'level': 1,
                'ranking_points': self.initial_mmr(),
                'wins': 0,
                'losses': 0,
                'draws': 0,
                'total_matches': 0,
                'winrate': 0.0,
                'current_streak': 0,
                'best_streak': 0
            },
            'preferences': {
                'favorite_characters': [],
                'favorite_stages': [],
                'playstyle': self.generate_playstyle()
            },
            'ai_brain': {
                'aggression': random.uniform(0.3, 0.9),
                'defense': random.uniform(0.3, 0.9),
                'combo_skill': random.uniform(0.3, 0.9),
                'reaction_time': random.uniform(0.1, 0.5),
                'adaptation': random.uniform(0.3, 0.8),
                'learning_rate': random.uniform(0.01, 0.05)
            },
            'match_history': [],
            'skill_evolution': []  # Historique de l'évolution des compétences
        }

        # État actuel
        self.status = 'offline'
        self.current_match = None
        self.socket = None
        self.server_address = ('127.0.0.1', 9999)

    def generate_name(self):
        """Génère un nom aléatoire de joueur"""
        prefixes = ['Dark', 'Shadow', 'Fire', 'Ice', 'Thunder', 'Dragon', 'Wolf', 'Tiger',
                   'Phoenix', 'Viper', 'Ryu', 'Ken', 'Akuma', 'Sagat', 'Guile', 'Chun',
                   'Deadly', 'Silent', 'Swift', 'Mighty', 'Cyber', 'Neon', 'Blade', 'Storm']
        suffixes = ['Warrior', 'Fighter', 'Master', 'Legend', 'Pro', 'King', 'Queen', 'Ace',
                   'Slayer', 'Hunter', 'Champion', 'Ninja', 'Samurai', 'Ronin', 'Shogun',
                   'Striker', 'Crusher', 'Breaker', 'Destroyer', '2000', '3000', 'X', 'Z']

        return f"{random.choice(prefixes)}{random.choice(suffixes)}{random.randint(1, 999)}"

    def initial_mmr(self):
        """Détermine le MMR initial basé sur le niveau de compétence"""
        mmr_ranges = {
            'beginner': (800, 1000),
            'intermediate': (1000, 1200),
            'advanced': (1200, 1400),
            'expert': (1400, 1600),
            'master': (1600, 2000)
        }

        min_mmr, max_mmr = mmr_ranges.get(self.skill_level, (1000, 1200))
        return random.randint(min_mmr, max_mmr)

    def generate_playstyle(self):
        """Génère un style de jeu"""
        styles = ['aggressive', 'defensive', 'balanced', 'rushdown', 'zoner', 'grappler',
                 'mixup', 'technical', 'footsies', 'pressure']
        return random.choice(styles)

    def connect_to_server(self):
        """Se connecte au serveur de matchmaking"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.server_address)

            # Envoyer les infos de connexion
            connect_data = {
                'action': 'connect',
                'username': self.name,
                'player_data': self.profile
            }

            self.socket.send(json.dumps(connect_data).encode('utf-8'))

            # Recevoir confirmation
            response = self.socket.recv(4096).decode('utf-8')
            response_data = json.loads(response)

            if response_data.get('status') == 'success':
                self.status = 'online'
                print(f"✅ {self.name} connecté au serveur (MMR: {self.profile['stats']['ranking_points']})")
                return True
            else:
                print(f"❌ {self.name} - échec de connexion")
                return False

        except Exception as e:
            print(f"❌ {self.name} - erreur de connexion: {e}")
            self.status = 'offline'
            return False

    def search_match(self, mode='ranked'):
        """Recherche un match"""
        if self.status != 'online':
            return False

        try:
            search_data = {
                'action': 'search_match',
                'mode': mode
            }

            self.socket.send(json.dumps(search_data).encode('utf-8'))
            self.status = 'searching'
            print(f"🔍 {self.name} recherche un match ({mode})...")
            return True

        except Exception as e:
            print(f"❌ {self.name} - erreur recherche: {e}")
            return False

    def simulate_match(self, opponent_data):
        """Simule un match contre un adversaire"""
        print(f"\n⚔️  {self.name} vs {opponent_data['username']}")

        # Calculer les probabilités de victoire basées sur les compétences
        my_skill = self.calculate_skill_score()
        opponent_mmr = opponent_data.get('mmr', 1000)

        # La différence de MMR influence les chances
        mmr_diff = self.profile['stats']['ranking_points'] - opponent_mmr
        win_probability = 0.5 + (mmr_diff / 400)  # Formule ELO simplifiée

        # Ajouter un facteur aléatoire
        win_probability += random.uniform(-0.1, 0.1)
        win_probability = max(0.1, min(0.9, win_probability))  # Clamp entre 10% et 90%

        # Simuler le match
        time.sleep(random.uniform(5, 15))  # Durée du match

        won = random.random() < win_probability

        # Enregistrer le résultat
        match_result = {
            'opponent': opponent_data['username'],
            'opponent_mmr': opponent_mmr,
            'timestamp': datetime.now().isoformat(),
            'won': won,
            'rounds_won': random.randint(2, 3) if won else random.randint(0, 1),
            'rounds_lost': random.randint(0, 1) if won else random.randint(2, 3),
            'damage_dealt': random.randint(5000, 15000),
            'damage_taken': random.randint(5000, 15000),
            'combos_landed': random.randint(5, 20),
            'specials_used': random.randint(10, 30)
        }

        self.update_stats(match_result)
        self.learn_from_match(match_result)

        return match_result

    def calculate_skill_score(self):
        """Calcule le score de compétence global"""
        brain = self.profile['ai_brain']
        return (brain['aggression'] + brain['defense'] + brain['combo_skill'] +
                brain['adaptation']) / 4

    def update_stats(self, match_result):
        """Met à jour les statistiques après un match"""
        stats = self.profile['stats']

        stats['total_matches'] += 1

        if match_result['won']:
            stats['wins'] += 1
            stats['current_streak'] += 1
            stats['best_streak'] = max(stats['best_streak'], stats['current_streak'])
            print(f"   🏆 {self.name} GAGNE! (+{match_result['rounds_won']}-{match_result['rounds_lost']})")
        else:
            stats['losses'] += 1
            stats['current_streak'] = 0
            print(f"   💀 {self.name} perd... ({match_result['rounds_won']}-{match_result['rounds_lost']})")

        # Calculer winrate
        stats['winrate'] = stats['wins'] / max(stats['total_matches'], 1)

        # Progression de niveau
        stats['level'] = 1 + (stats['total_matches'] // 10)

        # Ajouter à l'historique
        self.profile['match_history'].append(match_result)

        # Garder seulement les 50 derniers matchs
        if len(self.profile['match_history']) > 50:
            self.profile['match_history'] = self.profile['match_history'][-50:]

    def learn_from_match(self, match_result):
        """Apprend et s'améliore après chaque match (ML simplifié)"""
        brain = self.profile['ai_brain']
        learning_rate = brain['learning_rate']

        if match_result['won']:
            # Renforcer les stratégies gagnantes
            brain['aggression'] = min(1.0, brain['aggression'] + learning_rate * 0.1)
            brain['combo_skill'] = min(1.0, brain['combo_skill'] + learning_rate * 0.15)
            brain['adaptation'] = min(1.0, brain['adaptation'] + learning_rate * 0.05)
        else:
            # Ajuster après une défaite
            if match_result['damage_taken'] > match_result['damage_dealt']:
                # Améliorer la défense
                brain['defense'] = min(1.0, brain['defense'] + learning_rate * 0.2)
                brain['reaction_time'] = max(0.05, brain['reaction_time'] - learning_rate * 0.1)
            else:
                # Améliorer l'attaque
                brain['aggression'] = min(1.0, brain['aggression'] + learning_rate * 0.15)
                brain['combo_skill'] = min(1.0, brain['combo_skill'] + learning_rate * 0.1)

        # Enregistrer l'évolution
        skill_snapshot = {
            'timestamp': datetime.now().isoformat(),
            'match_number': self.profile['stats']['total_matches'],
            'skills': dict(brain),
            'mmr': self.profile['stats']['ranking_points']
        }

        self.profile['skill_evolution'].append(skill_snapshot)

        # Garder seulement les 100 derniers snapshots
        if len(self.profile['skill_evolution']) > 100:
            self.profile['skill_evolution'] = self.profile['skill_evolution'][-100:]

    def save_profile(self):
        """Sauvegarde le profil du joueur"""
        filename = f"player_profiles/player_{self.player_id}.json"

        os.makedirs('player_profiles', exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.profile, f, indent=2, ensure_ascii=False)

    def load_profile(self):
        """Charge un profil sauvegardé"""
        filename = f"player_profiles/player_{self.player_id}.json"

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.profile = json.load(f)
                self.name = self.profile['name']
                print(f"📁 Profil chargé : {self.name}")
                return True
        except FileNotFoundError:
            print(f"ℹ️  Nouveau joueur : {self.name}")
            return False

    def get_summary(self):
        """Retourne un résumé du joueur"""
        stats = self.profile['stats']
        brain = self.profile['ai_brain']

        return {
            'name': self.name,
            'mmr': stats['ranking_points'],
            'level': stats['level'],
            'wins': stats['wins'],
            'losses': stats['losses'],
            'winrate': f"{stats['winrate']*100:.1f}%",
            'matches': stats['total_matches'],
            'skill_score': f"{self.calculate_skill_score()*100:.1f}",
            'playstyle': self.profile['preferences']['playstyle']
        }


class VirtualPlayersManager:
    """Gère une flotte de joueurs virtuels"""

    def __init__(self, num_players=20):
        self.num_players = num_players
        self.players = []
        self.active = False

    def create_players(self):
        """Crée tous les joueurs virtuels"""
        print(f"\n🤖 Création de {self.num_players} joueurs virtuels...")

        skill_distribution = {
            'beginner': 0.20,      # 20%
            'intermediate': 0.35,  # 35%
            'advanced': 0.25,      # 25%
            'expert': 0.15,        # 15%
            'master': 0.05         # 5%
        }

        for i in range(self.num_players):
            # Déterminer le niveau de compétence selon la distribution
            rand = random.random()
            cumulative = 0
            skill_level = 'intermediate'

            for skill, prob in skill_distribution.items():
                cumulative += prob
                if rand <= cumulative:
                    skill_level = skill
                    break

            player = VirtualPlayerAI(i, skill_level)

            # Essayer de charger un profil existant
            player.load_profile()

            self.players.append(player)
            print(f"   ✓ {player.name} ({skill_level}, MMR: {player.profile['stats']['ranking_points']})")

        print(f"\n✅ {len(self.players)} joueurs créés!\n")

    def connect_all(self):
        """Connecte tous les joueurs au serveur"""
        print("🔌 Connexion des joueurs au serveur...\n")

        connected = 0
        for player in self.players:
            if player.connect_to_server():
                connected += 1
                time.sleep(0.5)  # Petit délai entre chaque connexion

        print(f"\n✅ {connected}/{len(self.players)} joueurs connectés\n")
        return connected

    def start_matchmaking(self):
        """Lance la recherche de matchs pour tous les joueurs"""
        print("🎮 Lancement du matchmaking automatique...\n")

        self.active = True

        while self.active:
            # Chaque joueur en ligne recherche un match
            for player in self.players:
                if player.status == 'online':
                    player.search_match('ranked')

            # Attendre un peu avant le prochain cycle
            time.sleep(random.uniform(10, 30))

    def save_all_profiles(self):
        """Sauvegarde tous les profils"""
        print("\n💾 Sauvegarde des profils...")
        for player in self.players:
            player.save_profile()
        print("✅ Profils sauvegardés!\n")

    def get_leaderboard(self):
        """Retourne le classement des joueurs"""
        sorted_players = sorted(
            self.players,
            key=lambda p: p.profile['stats']['ranking_points'],
            reverse=True
        )

        return [p.get_summary() for p in sorted_players[:10]]

    def print_statistics(self):
        """Affiche les statistiques globales"""
        total_matches = sum(p.profile['stats']['total_matches'] for p in self.players)
        total_wins = sum(p.profile['stats']['wins'] for p in self.players)
        avg_mmr = sum(p.profile['stats']['ranking_points'] for p in self.players) / len(self.players)

        print("\n" + "="*60)
        print("📊 STATISTIQUES GLOBALES")
        print("="*60)
        print(f"Total joueurs:    {len(self.players)}")
        print(f"Total matchs:     {total_matches}")
        print(f"MMR moyen:        {avg_mmr:.0f}")
        print(f"\n🏆 TOP 10:")

        for i, player_summary in enumerate(self.get_leaderboard(), 1):
            print(f"{i:2}. {player_summary['name']:20} | MMR: {player_summary['mmr']:4.0f} | "
                  f"W/L: {player_summary['wins']}/{player_summary['losses']} | "
                  f"WR: {player_summary['winrate']}")

        print("="*60 + "\n")


def main():
    """Programme principal"""
    print("\n" + "="*60)
    print("  KOF ULTIMATE ONLINE - JOUEURS VIRTUELS IA")
    print("="*60)

    # Créer le gestionnaire de joueurs
    manager = VirtualPlayersManager(num_players=20)

    # Créer les joueurs
    manager.create_players()

    # Connecter au serveur
    manager.connect_all()

    try:
        # Démarrer le matchmaking
        print("▶️  Appuyez sur Ctrl+C pour arrêter\n")
        manager.start_matchmaking()

    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt des joueurs virtuels...")
        manager.save_all_profiles()
        manager.print_statistics()
        print("✅ Arrêt terminé!\n")


if __name__ == "__main__":
    main()
