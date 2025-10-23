#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF Ultimate - Système de Matchmaking en Équipe
Support pour 2v2, 3v3, et modes équipe personnalisés
"""

import json
import socket
import threading
import time
from pathlib import Path
from datetime import datetime
import random

class Team:
    """Représente une équipe de joueurs"""

    def __init__(self, team_id, players, team_mmr=None):
        self.team_id = team_id
        self.players = players  # Liste de joueurs
        self.team_mmr = team_mmr or self.calculate_team_mmr()
        self.created_at = datetime.now()

    def calculate_team_mmr(self):
        """Calcule le MMR moyen de l'équipe"""
        if not self.players:
            return 1000

        # MMR moyen pondéré (peut être ajusté)
        total_mmr = sum(p.get('mmr', 1000) for p in self.players)
        return int(total_mmr / len(self.players))

    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            'team_id': self.team_id,
            'players': self.players,
            'team_mmr': self.team_mmr,
            'size': len(self.players),
            'created_at': self.created_at.isoformat()
        }

class TeamMatchmakingQueue:
    """File d'attente de matchmaking par équipe"""

    def __init__(self, mode='2v2'):
        self.mode = mode  # 2v2, 3v3, 4v4, etc.
        self.team_size = int(mode[0])  # Extrait 2 de "2v2"
        self.queue = []
        self.matches_made = []
        self.lock = threading.Lock()

    def add_team(self, team):
        """Ajoute une équipe à la file"""
        with self.lock:
            if len(team.players) != self.team_size:
                return False, f"Équipe doit avoir {self.team_size} joueurs (a {len(team.players)})"

            self.queue.append(team)
            print(f"✅ Équipe {team.team_id} ajoutée à la queue {self.mode} (MMR: {team.team_mmr})")

            # Essayer de faire un match
            match = self.try_make_match()
            if match:
                self.matches_made.append(match)
                return True, f"Match trouvé! {match['team1']['team_id']} vs {match['team2']['team_id']}"

            return True, f"En attente... ({len(self.queue)} équipes en queue)"

    def try_make_match(self):
        """Essaie de créer un match entre 2 équipes"""
        if len(self.queue) < 2:
            return None

        # Trier par MMR
        sorted_queue = sorted(self.queue, key=lambda t: t.team_mmr)

        # Trouver les 2 équipes les plus proches en MMR
        best_match = None
        best_diff = float('inf')

        for i in range(len(sorted_queue)):
            for j in range(i+1, len(sorted_queue)):
                team1 = sorted_queue[i]
                team2 = sorted_queue[j]

                mmr_diff = abs(team1.team_mmr - team2.team_mmr)

                # Acceptable si différence < 200 MMR
                if mmr_diff < 200 and mmr_diff < best_diff:
                    best_diff = mmr_diff
                    best_match = (team1, team2)

        if best_match:
            team1, team2 = best_match

            # Retirer de la queue
            self.queue.remove(team1)
            self.queue.remove(team2)

            match = {
                'match_id': f"match_{len(self.matches_made) + 1}",
                'mode': self.mode,
                'team1': team1.to_dict(),
                'team2': team2.to_dict(),
                'mmr_diff': best_diff,
                'created_at': datetime.now().isoformat(),
                'status': 'ready'
            }

            print(f"\n🎮 MATCH CRÉÉ!")
            print(f"   Mode: {self.mode}")
            print(f"   Équipe 1 (MMR {team1.team_mmr}): {[p['name'] for p in team1.players]}")
            print(f"   Équipe 2 (MMR {team2.team_mmr}): {[p['name'] for p in team2.players]}")
            print(f"   Différence MMR: {best_diff}")

            return match

        return None

    def get_queue_status(self):
        """Obtient le statut de la queue"""
        with self.lock:
            return {
                'mode': self.mode,
                'teams_waiting': len(self.queue),
                'matches_made': len(self.matches_made),
                'queue': [t.to_dict() for t in self.queue]
            }

class TeamMatchmakingServer:
    """Serveur de matchmaking multi-modes"""

    def __init__(self, game_dir):
        self.game_dir = Path(game_dir)
        self.queues = {
            '2v2': TeamMatchmakingQueue('2v2'),
            '3v3': TeamMatchmakingQueue('3v3'),
            '4v4': TeamMatchmakingQueue('4v4')
        }
        self.active_matches = []
        self.teams_db_file = self.game_dir / "teams_database.json"
        self.teams_db = self.load_teams_db()

    def load_teams_db(self):
        """Charge la base de données des équipes"""
        if self.teams_db_file.exists():
            with open(self.teams_db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'teams': [], 'permanent_teams': {}}

    def save_teams_db(self):
        """Sauvegarde la base de données des équipes"""
        with open(self.teams_db_file, 'w', encoding='utf-8') as f:
            json.dump(self.teams_db, f, indent=2, ensure_ascii=False)

    def create_team(self, players, team_name=None, permanent=False):
        """Crée une équipe"""
        team_id = f"team_{len(self.teams_db['teams']) + 1}"

        team = Team(team_id, players)

        if permanent and team_name:
            # Équipe permanente (clan/guild)
            self.teams_db['permanent_teams'][team_name] = {
                'team_id': team_id,
                'name': team_name,
                'players': players,
                'created_at': datetime.now().isoformat(),
                'matches_played': 0,
                'wins': 0,
                'losses': 0
            }
            self.save_teams_db()
            print(f"🏆 Équipe permanente créée: {team_name}")

        self.teams_db['teams'].append(team.to_dict())
        self.save_teams_db()

        return team

    def queue_team(self, team, mode='2v2'):
        """Met une équipe en file d'attente"""
        if mode not in self.queues:
            return False, f"Mode {mode} non supporté"

        return self.queues[mode].add_team(team)

    def get_all_queues_status(self):
        """Obtient le statut de toutes les queues"""
        status = {}
        for mode, queue in self.queues.items():
            status[mode] = queue.get_queue_status()
        return status

    def display_queues_status(self):
        """Affiche le statut des queues"""
        print("\n" + "="*70)
        print("📊 STATUT DES QUEUES DE MATCHMAKING")
        print("="*70)

        for mode, queue in self.queues.items():
            status = queue.get_queue_status()
            print(f"\n🎮 Mode {mode}:")
            print(f"   Équipes en attente: {status['teams_waiting']}")
            print(f"   Matchs créés: {status['matches_made']}")

            if status['queue']:
                print(f"   Queue:")
                for team in status['queue']:
                    player_names = [p['name'] for p in team['players']]
                    print(f"      - Équipe {team['team_id']} (MMR {team['team_mmr']}): {', '.join(player_names)}")

        print("="*70)

    def simulate_team_matchmaking(self, num_teams=20, mode='2v2'):
        """Simule le matchmaking d'équipes"""
        print(f"\n🎲 Simulation matchmaking mode {mode} ({num_teams} équipes)...")

        # Générer joueurs virtuels
        player_names = [
            "DragonFist", "ShadowKing", "LightningStrike", "IceQueen",
            "PhoenixRising", "TigerClaw", "StormBreaker", "NightHawk",
            "BlazeFury", "CrystalBlade", "ThunderGod", "MoonlightAssassin",
            "SolarFlare", "FrostBite", "WildFang", "DarkViper",
            "GoldenWarrior", "SilverArrow", "IronFist", "MysticSage",
            "RagingBull", "SwiftEagle", "CrimsonWave", "EmeraldKnight",
            "DiamondShield", "SapphireLance", "RubyFang", "AmethystWing",
            "TopazShield", "OnyxBlade", "QuartzSpear", "JadeArrow",
            "PearlGuardian", "CoralWarrior", "ObsidianKnight", "MarbleFist"
        ]

        team_size = int(mode[0])

        # Créer équipes
        for i in range(num_teams):
            # Sélectionner joueurs aléatoires
            team_players_names = random.sample(player_names, team_size)

            # Créer joueurs avec MMR
            players = []
            for name in team_players_names:
                players.append({
                    'name': name,
                    'mmr': random.randint(800, 1800)
                })

            # Créer et ajouter équipe
            team = self.create_team(players)
            success, message = self.queue_team(team, mode)

            if not success:
                print(f"❌ {message}")

            time.sleep(0.1)  # Petit délai

        # Afficher résultats
        self.display_queues_status()

        print(f"\n✅ Simulation terminée")
        print(f"   Matchs créés: {len(self.queues[mode].matches_made)}")

    def generate_team_matches_report(self, mode='2v2'):
        """Génère un rapport des matchs d'équipe"""
        matches = self.queues[mode].matches_made

        report_file = self.game_dir / f"team_matches_report_{mode}.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# 🏆 Rapport Matchs en Équipe - Mode {mode}\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## 📊 Statistiques\n\n")
            f.write(f"- **Total matchs:** {len(matches)}\n")
            f.write(f"- **Mode:** {mode}\n\n")

            f.write(f"## 🎮 Liste des Matchs\n\n")

            for i, match in enumerate(matches, 1):
                f.write(f"### Match #{i}\n\n")
                f.write(f"**ID:** {match['match_id']}\n\n")

                f.write(f"**Équipe 1** (MMR: {match['team1']['team_mmr']})\n")
                for player in match['team1']['players']:
                    f.write(f"- {player['name']} (MMR: {player['mmr']})\n")

                f.write(f"\n**vs**\n\n")

                f.write(f"**Équipe 2** (MMR: {match['team2']['team_mmr']})\n")
                for player in match['team2']['players']:
                    f.write(f"- {player['name']} (MMR: {player['mmr']})\n")

                f.write(f"\n**Différence MMR:** {match['mmr_diff']}\n")
                f.write(f"**Qualité:** {'Excellente' if match['mmr_diff'] < 50 else 'Bonne' if match['mmr_diff'] < 100 else 'Acceptable'}\n\n")
                f.write("---\n\n")

        print(f"✅ Rapport sauvegardé: {report_file}")
        return report_file

def main():
    """Point d'entrée"""
    game_dir = r"D:\KOF Ultimate Online"

    print("\n🏆 KOF Ultimate - Système de Matchmaking en Équipe")
    print("="*70)

    server = TeamMatchmakingServer(game_dir)

    # Simuler matchmaking pour chaque mode
    print("\n🎮 Test Mode 2v2")
    server.simulate_team_matchmaking(num_teams=12, mode='2v2')

    print("\n\n🎮 Test Mode 3v3")
    server.simulate_team_matchmaking(num_teams=9, mode='3v3')

    # Générer rapports
    for mode in ['2v2', '3v3']:
        if server.queues[mode].matches_made:
            server.generate_team_matches_report(mode)

    print("\n✅ Système de matchmaking en équipe opérationnel!")
    print("📊 Modes supportés: 2v2, 3v3, 4v4")
    print("🎮 Équipes permanentes (clans) supportées")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programme interrompu")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
