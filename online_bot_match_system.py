#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - Système de Match En Ligne avec Bots
Fait jouer des bots IA entre eux (simule un match en ligne)
"""

import subprocess
import time
import random
from pathlib import Path
from datetime import datetime
import threading

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class VirtualPlayer:
    """Représente un joueur virtuel (bot IA)"""

    def __init__(self, player_id, name, skill_level="normal"):
        self.id = player_id
        self.name = name
        self.skill_level = skill_level  # easy, normal, hard
        self.wins = 0
        self.losses = 0
        self.character = None

    def select_character(self):
        """Sélectionne un personnage aléatoirement"""
        characters = [
            "Kyo", "Iori", "Terry", "Andy", "Joe", "Ryo", "Robert",
            "Yuri", "Mai", "King", "Kim", "Chang", "Choi", "Athena",
            "Kensou", "Chin", "Leona", "Ralf", "Clark", "Benimaru"
        ]

        self.character = random.choice(characters)
        return self.character

    def __str__(self):
        return f"{self.name} ({self.character}) [{self.wins}W - {self.losses}L]"

class OnlineBotMatchSystem:
    """Système de matchs en ligne avec des bots"""

    def __init__(self, game_dir):
        self.game_dir = Path(game_dir)
        self.exe_path = self.game_dir / "KOF_Ultimate_Online.exe"
        self.players = []
        self.current_match = None

    def create_virtual_players(self, count=4):
        """Crée des joueurs virtuels"""
        print(f"\n{Colors.CYAN}Création de {count} joueurs virtuels...{Colors.RESET}\n")

        player_names = [
            "DragonFist", "ShadowKing", "ThunderStrike", "PhoenixFlame",
            "IceWarrior", "StormBlade", "CrimsonFury", "GoldenTiger"
        ]

        skill_levels = ["easy", "normal", "hard"]

        for i in range(count):
            name = random.choice(player_names)
            player_names.remove(name)  # Pas de doublons

            skill = random.choice(skill_levels)
            player = VirtualPlayer(i+1, name, skill)
            player.select_character()

            self.players.append(player)

            print(f"{Colors.GREEN}  ✓ Joueur {i+1}: {player.name} - {player.character} ({skill}){Colors.RESET}")

        print()

    def simulate_matchmaking(self):
        """Simule un matchmaking"""
        print(f"\n{Colors.CYAN}🔄 MATCHMAKING EN COURS...{Colors.RESET}\n")

        # Attendre pour simuler la recherche
        for i in range(3):
            print(f"\r  Recherche d'adversaires... {'.' * (i+1)}   ", end='', flush=True)
            time.sleep(1)

        print(f"\r{Colors.GREEN}  ✓ Match trouvé!                    {Colors.RESET}\n")

    def select_random_match(self):
        """Sélectionne 2 joueurs aléatoirement pour un match"""
        if len(self.players) < 2:
            return None

        available_players = self.players.copy()
        random.shuffle(available_players)

        player1 = available_players[0]
        player2 = available_players[1]

        return (player1, player2)

    def display_match_info(self, player1, player2):
        """Affiche les infos du match"""
        print(f"\n{Colors.MAGENTA}{'='*80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'⚔️  MATCH EN LIGNE  ⚔️':^80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'='*80}{Colors.RESET}\n")

        print(f"{Colors.CYAN}  🟦 JOUEUR 1:{Colors.RESET}")
        print(f"     Pseudo: {Colors.BOLD}{player1.name}{Colors.RESET}")
        print(f"     Personnage: {player1.character}")
        print(f"     Niveau: {player1.skill_level.upper()}")
        print(f"     Record: {player1.wins}W - {player1.losses}L\n")

        print(f"{Colors.RED}          VS{Colors.RESET}\n")

        print(f"{Colors.CYAN}  🟥 JOUEUR 2:{Colors.RESET}")
        print(f"     Pseudo: {Colors.BOLD}{player2.name}{Colors.RESET}")
        print(f"     Personnage: {player2.character}")
        print(f"     Niveau: {player2.skill_level.upper()}")
        print(f"     Record: {player2.wins}W - {player2.losses}L\n")

        print(f"{Colors.MAGENTA}{'='*80}{Colors.RESET}\n")

    def launch_ai_vs_ai_match(self, player1, player2):
        """Lance un match IA vs IA"""
        print(f"{Colors.CYAN}🎮 Lancement du match...{Colors.RESET}\n")

        # Note: M.U.G.E.N ne peut pas lancer automatiquement un match IA vs IA
        # Il faudrait créer un script AHK ou utiliser pyautogui pour simuler les inputs
        # Pour l'instant, on simule le résultat

        print(f"{Colors.YELLOW}⚠ Mode simulation activé{Colors.RESET}")
        print(f"{Colors.CYAN}  (Le jeu nécessite des contrôles manuels){Colors.RESET}\n")

        # Simuler le match
        print(f"{Colors.CYAN}Combat en cours...{Colors.RESET}")
        for i in range(5):
            print(f"\r  Round en cours... {'█' * (i+1)}{'░' * (5-i-1)}   ", end='', flush=True)
            time.sleep(1)

        print(f"\r{Colors.GREEN}  Match terminé!                    {Colors.RESET}\n")

        # Déterminer le gagnant basé sur le skill level
        skill_values = {"easy": 1, "normal": 2, "hard": 3}
        skill1 = skill_values.get(player1.skill_level, 2)
        skill2 = skill_values.get(player2.skill_level, 2)

        # Ajouter un facteur aléatoire
        score1 = skill1 * random.uniform(0.8, 1.2)
        score2 = skill2 * random.uniform(0.8, 1.2)

        if score1 > score2:
            winner = player1
            loser = player2
        else:
            winner = player2
            loser = player1

        winner.wins += 1
        loser.losses += 1

        return winner, loser

    def display_match_result(self, winner, loser):
        """Affiche le résultat du match"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}{'🏆  VICTOIRE!  🏆':^80}{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

        print(f"  {Colors.GREEN}{Colors.BOLD}Gagnant: {winner.name} ({winner.character}){Colors.RESET}")
        print(f"  {Colors.YELLOW}Perdant: {loser.name} ({loser.character}){Colors.RESET}\n")

        print(f"{Colors.CYAN}  Nouveau record:{Colors.RESET}")
        print(f"    {winner.name}: {winner.wins}W - {winner.losses}L")
        print(f"    {loser.name}: {loser.wins}W - {loser.losses}L")

        print(f"\n{Colors.GREEN}{'='*80}{Colors.RESET}\n")

    def display_leaderboard(self):
        """Affiche le classement"""
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'🏆  CLASSEMENT GÉNÉRAL  🏆':^80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

        # Trier par victoires
        sorted_players = sorted(self.players, key=lambda p: p.wins, reverse=True)

        print(f"  {'Rang':<6} {'Pseudo':<20} {'Personnage':<15} {'Record':<15}")
        print(f"  {'-'*70}")

        for i, player in enumerate(sorted_players):
            rank = i + 1
            rank_symbol = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "  "

            record = f"{player.wins}W - {player.losses}L"

            color = Colors.GREEN if rank == 1 else Colors.CYAN if rank == 2 else Colors.YELLOW if rank == 3 else Colors.RESET

            print(f"{color}  {rank_symbol} #{rank:<3} {player.name:<20} {player.character:<15} {record:<15}{Colors.RESET}")

        print(f"\n{Colors.MAGENTA}{'='*80}{Colors.RESET}\n")

    def run_online_season(self, num_matches=5):
        """Lance une saison de matchs en ligne"""
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'🌐  SAISON EN LIGNE - KOF ULTIMATE  🌐':^80}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

        print(f"{Colors.CYAN}Nombre de matchs: {num_matches}{Colors.RESET}")
        print(f"{Colors.CYAN}Joueurs en ligne: {len(self.players)}{Colors.RESET}\n")

        input(f"{Colors.YELLOW}Appuyez sur ENTRÉE pour démarrer la saison...{Colors.RESET}")

        for match_num in range(1, num_matches + 1):
            print(f"\n{Colors.CYAN}{Colors.BOLD}───────────────────────────────────────────────────────────────{Colors.RESET}")
            print(f"{Colors.CYAN}{Colors.BOLD}  MATCH {match_num}/{num_matches}{Colors.RESET}")
            print(f"{Colors.CYAN}{Colors.BOLD}───────────────────────────────────────────────────────────────{Colors.RESET}\n")

            # Matchmaking
            self.simulate_matchmaking()

            # Sélectionner 2 joueurs
            match = self.select_random_match()
            if not match:
                print(f"{Colors.RED}✗ Pas assez de joueurs{Colors.RESET}")
                break

            player1, player2 = match

            # Afficher infos du match
            self.display_match_info(player1, player2)

            # Attendre confirmation
            input(f"{Colors.CYAN}Appuyez sur ENTRÉE pour lancer le match...{Colors.RESET}\n")

            # Lancer le match
            winner, loser = self.launch_ai_vs_ai_match(player1, player2)

            # Afficher résultat
            self.display_match_result(winner, loser)

            # Attendre avant le prochain match
            if match_num < num_matches:
                time.sleep(2)

        # Afficher classement final
        self.display_leaderboard()

        print(f"{Colors.GREEN}{Colors.BOLD}✓ Saison terminée!{Colors.RESET}\n")

def main():
    game_dir = r"D:\KOF Ultimate Online Online Online"

    system = OnlineBotMatchSystem(game_dir)

    # Créer des joueurs virtuels
    system.create_virtual_players(count=4)

    # Lancer une saison
    system.run_online_season(num_matches=5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Saison interrompue{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Erreur: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
