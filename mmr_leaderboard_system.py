#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF Ultimate - Système de Classement MMR
Leaderboard avec top joueurs, statistiques, historique
"""

import json
import os
from pathlib import Path
from datetime import datetime
import random

class MMRLeaderboardSystem:
    """Système de classement et leaderboard"""

    def __init__(self, game_dir):
        self.game_dir = Path(game_dir)
        self.leaderboard_file = self.game_dir / "leaderboard.json"
        self.players_file = self.game_dir / "players_stats.json"
        self.matches_file = self.game_dir / "matches_history.json"

        # Charger ou initialiser
        self.players = self.load_players()
        self.matches = self.load_matches()

    def load_players(self):
        """Charge les stats des joueurs"""
        if self.players_file.exists():
            with open(self.players_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_players(self):
        """Sauvegarde les stats des joueurs"""
        with open(self.players_file, 'w', encoding='utf-8') as f:
            json.dump(self.players, f, indent=2, ensure_ascii=False)

    def load_matches(self):
        """Charge l'historique des matchs"""
        if self.matches_file.exists():
            with open(self.matches_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_matches(self):
        """Sauvegarde l'historique des matchs"""
        with open(self.matches_file, 'w', encoding='utf-8') as f:
            json.dump(self.matches, f, indent=2, ensure_ascii=False)

    def register_player(self, player_name, initial_mmr=1000):
        """Enregistre un nouveau joueur"""
        if player_name not in self.players:
            self.players[player_name] = {
                'name': player_name,
                'mmr': initial_mmr,
                'wins': 0,
                'losses': 0,
                'draws': 0,
                'win_streak': 0,
                'best_streak': 0,
                'total_matches': 0,
                'rank': 'Unranked',
                'tier': 'Bronze',
                'registration_date': datetime.now().isoformat(),
                'last_match': None,
                'favorite_character': None,
                'mmr_history': [initial_mmr]
            }
            self.save_players()
            print(f"✅ Joueur enregistré: {player_name} (MMR: {initial_mmr})")

    def calculate_mmr_change(self, winner_mmr, loser_mmr, k_factor=32):
        """Calcule le changement de MMR selon Elo"""
        expected_winner = 1 / (1 + 10 ** ((loser_mmr - winner_mmr) / 400))
        expected_loser = 1 / (1 + 10 ** ((winner_mmr - loser_mmr) / 400))

        winner_change = k_factor * (1 - expected_winner)
        loser_change = k_factor * (0 - expected_loser)

        return int(winner_change), int(loser_change)

    def record_match(self, player1, player2, winner, match_data=None):
        """Enregistre un match et met à jour les MMR"""
        if player1 not in self.players:
            self.register_player(player1)
        if player2 not in self.players:
            self.register_player(player2)

        p1_data = self.players[player1]
        p2_data = self.players[player2]

        # Calculer changement MMR
        if winner == player1:
            mmr_change_p1, mmr_change_p2 = self.calculate_mmr_change(
                p1_data['mmr'], p2_data['mmr']
            )
            p1_data['wins'] += 1
            p2_data['losses'] += 1
            p1_data['win_streak'] += 1
            p2_data['win_streak'] = 0

            if p1_data['win_streak'] > p1_data['best_streak']:
                p1_data['best_streak'] = p1_data['win_streak']

        elif winner == player2:
            mmr_change_p2, mmr_change_p1 = self.calculate_mmr_change(
                p2_data['mmr'], p1_data['mmr']
            )
            p2_data['wins'] += 1
            p1_data['losses'] += 1
            p2_data['win_streak'] += 1
            p1_data['win_streak'] = 0

            if p2_data['win_streak'] > p2_data['best_streak']:
                p2_data['best_streak'] = p2_data['win_streak']

        else:  # Draw
            mmr_change_p1 = 0
            mmr_change_p2 = 0
            p1_data['draws'] += 1
            p2_data['draws'] += 1

        # Appliquer changements MMR
        p1_data['mmr'] += mmr_change_p1
        p2_data['mmr'] += mmr_change_p2
        p1_data['mmr'] = max(0, p1_data['mmr'])  # Minimum 0
        p2_data['mmr'] = max(0, p2_data['mmr'])

        # Historique MMR
        p1_data['mmr_history'].append(p1_data['mmr'])
        p2_data['mmr_history'].append(p2_data['mmr'])

        # Mettre à jour stats
        p1_data['total_matches'] += 1
        p2_data['total_matches'] += 1
        p1_data['last_match'] = datetime.now().isoformat()
        p2_data['last_match'] = datetime.now().isoformat()

        # Mettre à jour tiers
        self.update_tier(player1)
        self.update_tier(player2)

        # Enregistrer le match
        match = {
            'timestamp': datetime.now().isoformat(),
            'player1': player1,
            'player2': player2,
            'winner': winner,
            'p1_mmr_before': p1_data['mmr'] - mmr_change_p1,
            'p2_mmr_before': p2_data['mmr'] - mmr_change_p2,
            'p1_mmr_after': p1_data['mmr'],
            'p2_mmr_after': p2_data['mmr'],
            'p1_mmr_change': mmr_change_p1,
            'p2_mmr_change': mmr_change_p2,
            'match_data': match_data or {}
        }
        self.matches.append(match)

        # Sauvegarder
        self.save_players()
        self.save_matches()

        print(f"\n⚔️  Match enregistré:")
        print(f"   {player1} ({p1_data['mmr']}, {mmr_change_p1:+d}) vs {player2} ({p2_data['mmr']}, {mmr_change_p2:+d})")
        print(f"   Vainqueur: {winner}")

    def update_tier(self, player_name):
        """Met à jour le tier du joueur selon son MMR"""
        mmr = self.players[player_name]['mmr']

        if mmr >= 2400:
            tier = 'Grandmaster'
        elif mmr >= 2200:
            tier = 'Master'
        elif mmr >= 2000:
            tier = 'Diamond'
        elif mmr >= 1800:
            tier = 'Platinum'
        elif mmr >= 1600:
            tier = 'Gold'
        elif mmr >= 1400:
            tier = 'Silver'
        else:
            tier = 'Bronze'

        self.players[player_name]['tier'] = tier

        # Rank dans le tier
        if self.players[player_name]['total_matches'] < 10:
            rank = 'Unranked'
        else:
            rank = tier

        self.players[player_name]['rank'] = rank

    def get_leaderboard(self, top_n=50):
        """Obtient le classement TOP N"""
        # Trier par MMR
        sorted_players = sorted(
            self.players.values(),
            key=lambda p: p['mmr'],
            reverse=True
        )

        # Ajouter position
        for i, player in enumerate(sorted_players, 1):
            player['position'] = i

        return sorted_players[:top_n]

    def display_leaderboard(self, top_n=20):
        """Affiche le leaderboard"""
        print("\n" + "="*80)
        print(f"🏆 TOP {top_n} LEADERBOARD - KOF ULTIMATE ONLINE")
        print("="*80)
        print(f"{'#':<4} {'Joueur':<20} {'MMR':<8} {'Tier':<12} {'W/L':<10} {'Streak':<8} {'Total':<6}")
        print("-"*80)

        leaderboard = self.get_leaderboard(top_n)

        for player in leaderboard:
            pos = player['position']
            name = player['name'][:19]
            mmr = player['mmr']
            tier = player['tier']
            wl = f"{player['wins']}/{player['losses']}"
            streak = player['win_streak']
            total = player['total_matches']

            # Emoji selon tier
            tier_emoji = {
                'Grandmaster': '👑',
                'Master': '💎',
                'Diamond': '💠',
                'Platinum': '🔷',
                'Gold': '🥇',
                'Silver': '🥈',
                'Bronze': '🥉'
            }
            emoji = tier_emoji.get(tier, '🎮')

            print(f"{pos:<4} {name:<20} {mmr:<8} {emoji} {tier:<10} {wl:<10} {streak:<8} {total:<6}")

        print("="*80)

    def save_leaderboard_html(self, filename="leaderboard.html"):
        """Sauvegarde le leaderboard en HTML"""
        leaderboard = self.get_leaderboard(100)

        html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOF Ultimate - Leaderboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            color: #667eea;
            font-size: 3em;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
            font-size: 1.2em;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px;
            text-align: left;
            font-size: 1.1em;
        }
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        tr:hover {
            background: #f5f5f5;
        }
        .rank {
            font-weight: bold;
            font-size: 1.2em;
            color: #667eea;
        }
        .tier {
            padding: 5px 15px;
            border-radius: 15px;
            font-weight: bold;
            display: inline-block;
        }
        .tier-grandmaster { background: linear-gradient(135deg, #ffd700, #ffed4e); color: #333; }
        .tier-master { background: linear-gradient(135deg, #e0e0e0, #ffffff); color: #333; }
        .tier-diamond { background: linear-gradient(135deg, #b9f2ff, #87ceeb); color: #333; }
        .tier-platinum { background: linear-gradient(135deg, #c0c0c0, #e8e8e8); color: #333; }
        .tier-gold { background: linear-gradient(135deg, #ffd700, #ffed4e); color: #333; }
        .tier-silver { background: linear-gradient(135deg, #c0c0c0, #e8e8e8); color: #333; }
        .tier-bronze { background: linear-gradient(135deg, #cd7f32, #b87333); color: white; }
        .top3 {
            font-weight: bold;
            font-size: 1.3em;
        }
        .stats {
            text-align: center;
            margin-top: 40px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏆 LEADERBOARD</h1>
        <p class="subtitle">KOF Ultimate Online - Classement MMR</p>

        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Joueur</th>
                    <th>MMR</th>
                    <th>Tier</th>
                    <th>Victoires</th>
                    <th>Défaites</th>
                    <th>Ratio</th>
                    <th>Streak</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
"""

        for player in leaderboard:
            rank_class = 'top3' if player['position'] <= 3 else ''
            tier_class = f"tier-{player['tier'].lower()}"

            emoji = {
                'Grandmaster': '👑',
                'Master': '💎',
                'Diamond': '💠',
                'Platinum': '🔷',
                'Gold': '🥇',
                'Silver': '🥈',
                'Bronze': '🥉'
            }.get(player['tier'], '🎮')

            winrate = (player['wins'] / player['total_matches'] * 100) if player['total_matches'] > 0 else 0

            html += f"""
                <tr>
                    <td class="rank {rank_class}">{player['position']}</td>
                    <td>{player['name']}</td>
                    <td><strong>{player['mmr']}</strong></td>
                    <td><span class="tier {tier_class}">{emoji} {player['tier']}</span></td>
                    <td>{player['wins']}</td>
                    <td>{player['losses']}</td>
                    <td>{winrate:.1f}%</td>
                    <td>🔥 {player['win_streak']}</td>
                    <td>{player['total_matches']}</td>
                </tr>
"""

        html += """
            </tbody>
        </table>

        <div class="stats">
            <p>Dernière mise à jour: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
            <p>Total joueurs classés: """ + str(len(self.players)) + """</p>
        </div>
    </div>
</body>
</html>
"""

        output_file = self.game_dir / filename
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ Leaderboard HTML sauvegardé: {output_file}")
        return output_file

    def simulate_matches(self, num_matches=50):
        """Simule des matchs pour peupler le leaderboard"""
        print(f"\n🎲 Simulation de {num_matches} matchs...")

        # Créer joueurs virtuels
        player_names = [
            "DragonFist", "ShadowKing", "LightningStrike", "IceQueen", "PhoenixRising",
            "TigerClaw", "StormBreaker", "NightHawk", "BlazeFury", "CrystalBlade",
            "ThunderGod", "MoonlightAssassin", "SolarFlare", "FrostBite", "WildFang",
            "DarkViper", "GoldenWarrior", "SilverArrow", "IronFist", "MysticSage",
            "RagingBull", "SwiftEagle", "CrimsonWave", "EmeraldKnight", "DiamondShield"
        ]

        for name in player_names:
            if name not in self.players:
                self.register_player(name, initial_mmr=random.randint(800, 1200))

        # Simuler matchs
        for i in range(num_matches):
            p1, p2 = random.sample(player_names, 2)

            # Probabilité de victoire basée sur MMR
            mmr1 = self.players[p1]['mmr']
            mmr2 = self.players[p2]['mmr']

            prob_p1_wins = 1 / (1 + 10 ** ((mmr2 - mmr1) / 400))

            if random.random() < prob_p1_wins:
                winner = p1
            else:
                winner = p2

            self.record_match(p1, p2, winner)

        print(f"✅ {num_matches} matchs simulés")

def main():
    """Point d'entrée"""
    game_dir = r"D:\KOF Ultimate Online"

    print("\n🏆 KOF Ultimate - Système de Classement MMR")
    print("="*70)

    leaderboard = MMRLeaderboardSystem(game_dir)

    # Simuler des matchs si pas assez de données
    if len(leaderboard.matches) < 20:
        print("\n📊 Pas assez de données, simulation de matchs...")
        leaderboard.simulate_matches(num_matches=100)

    # Afficher leaderboard
    leaderboard.display_leaderboard(top_n=25)

    # Sauvegarder en HTML
    html_file = leaderboard.save_leaderboard_html()

    print(f"\n✅ Système de classement prêt!")
    print(f"📊 Ouvrez {html_file.name} pour voir le leaderboard complet")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programme interrompu")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
