#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SYSTÈME DE JOUEURS VIRTUELS EN CONTINU
Les joueurs virtuels naviguent dans les menus, sélectionnent des persos et jouent en continu
"""

import pyautogui
import time
import random
import subprocess
import sys
import threading
import json
from pathlib import Path
from datetime import datetime
import logging
from collections import defaultdict

# Désactiver le failsafe
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.05

# Configuration du logging
logging.basicConfig(
    filename='virtual_players_continuous.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class GameModes:
    """Tous les modes de jeu disponibles"""
    ARCADE = "Arcade"
    VERSUS = "Versus"
    TEAM = "Team Battle"
    SURVIVAL = "Survival"
    TIME_ATTACK = "Time Attack"
    TRAINING = "Training"
    ONLINE = "Online"

    ALL = [ARCADE, VERSUS, TEAM, SURVIVAL, TIME_ATTACK, TRAINING]

class VirtualPlayer:
    """Un joueur virtuel autonome qui joue en continu"""

    def __init__(self, player_id, name, game_dir, personality="balanced"):
        self.player_id = player_id
        self.name = name
        self.game_dir = Path(game_dir)
        self.personality = personality

        # Statistiques
        self.stats = {
            'player_id': player_id,
            'name': name,
            'matches_played': 0,
            'modes_played': defaultdict(int),
            'characters_used': defaultdict(int),
            'stages_played': defaultdict(int),
            'session_start': datetime.now().isoformat(),
            'total_playtime': 0,
            'actions_performed': 0
        }

        # État
        self.is_playing = False
        self.current_mode = None
        self.current_match_start = None

        # Dossiers
        self.logs_dir = self.game_dir / f"virtual_player_{player_id}_logs"
        self.logs_dir.mkdir(exist_ok=True)

        self.screenshots_dir = self.game_dir / f"virtual_player_{player_id}_screenshots"
        self.screenshots_dir.mkdir(exist_ok=True)

        # Logger personnel
        self.logger = logging.getLogger(f"Player{player_id}")
        handler = logging.FileHandler(self.logs_dir / f"player_{player_id}.log")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log(self, message, level="INFO"):
        """Log avec niveau"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{self.name}] {message}"

        if level == "INFO":
            self.logger.info(log_msg)
        elif level == "WARNING":
            self.logger.warning(log_msg)
        elif level == "ERROR":
            self.logger.error(log_msg)

        print(f"{timestamp} {log_msg}")

    def press_key(self, key, duration=0.1):
        """Presse une touche"""
        try:
            pyautogui.press(key)
            time.sleep(duration)
            self.stats['actions_performed'] += 1
        except Exception as e:
            self.log(f"Erreur pression touche {key}: {e}", "WARNING")

    def navigate_to_mode_from_menu(self, mode):
        """Navigue vers un mode depuis le menu principal"""
        self.log(f"Navigation vers {mode}...")

        # Attendre le menu principal
        time.sleep(2)

        # Navigation selon le mode
        mode_navigation = {
            GameModes.ARCADE: 0,      # Premier choix
            GameModes.VERSUS: 1,      # Deuxième
            GameModes.TEAM: 2,        # Troisième
            GameModes.SURVIVAL: 3,    # Quatrième
            GameModes.TIME_ATTACK: 4, # Cinquième
            GameModes.TRAINING: 5,    # Sixième
        }

        moves = mode_navigation.get(mode, 0)

        # Descendre jusqu'au mode voulu
        for _ in range(moves):
            self.press_key('down', 0.2)
            time.sleep(0.15)

        # Confirmer
        self.press_key('return', 0.5)
        time.sleep(1)

        self.current_mode = mode
        self.stats['modes_played'][mode] += 1
        self.log(f"Mode {mode} sélectionné")

    def select_characters(self, num_chars=1):
        """Sélectionne des personnages aléatoirement"""
        self.log(f"Sélection de {num_chars} personnage(s)...")

        characters_selected = []

        for i in range(num_chars):
            time.sleep(1)

            # Mouvements aléatoires dans la grille de sélection
            moves = random.randint(3, 12)
            for _ in range(moves):
                direction = random.choice(['up', 'down', 'left', 'right'])
                self.press_key(direction, 0.1)
                time.sleep(0.08)

            # Confirmer avec A ou punch
            confirm_key = random.choice(['a', 'j', 'return'])
            self.press_key(confirm_key, 0.3)
            time.sleep(0.5)

            char_name = f"Character_{random.randint(1, 50)}"
            characters_selected.append(char_name)
            self.stats['characters_used'][char_name] += 1

            self.log(f"  ✓ Personnage {i+1}/{num_chars} sélectionné")

        time.sleep(1)
        return characters_selected

    def select_stage(self):
        """Sélectionne un stage aléatoirement"""
        time.sleep(0.5)

        # Mouvements aléatoires
        moves = random.randint(1, 5)
        for _ in range(moves):
            direction = random.choice(['left', 'right'])
            self.press_key(direction, 0.15)
            time.sleep(0.1)

        # Confirmer
        self.press_key('return', 0.3)
        time.sleep(1)

        stage_name = f"Stage_{random.randint(1, 20)}"
        self.stats['stages_played'][stage_name] += 1
        self.log(f"Stage sélectionné: {stage_name}")

    def perform_combat_action(self):
        """Effectue une action de combat selon la personnalité"""

        # Actions selon personnalité
        if self.personality == "aggressive":
            actions = [
                lambda: self.press_key('right', 0.2),  # Avancer
                lambda: self.press_key('a', 0.1),      # Punch léger
                lambda: self.press_key('s', 0.1),      # Punch moyen
                lambda: self.press_key('d', 0.1),      # Punch fort
                lambda: [self.press_key('down', 0.05), self.press_key('right', 0.05), self.press_key('a', 0.1)],  # Special
                lambda: self.press_key('j', 0.1),      # Kick léger
                lambda: self.press_key('k', 0.1),      # Kick moyen
            ]
        elif self.personality == "defensive":
            actions = [
                lambda: self.press_key('left', 0.3),   # Reculer
                lambda: self.press_key('down', 0.2),   # Bloquer
                lambda: self.press_key('s', 0.1),      # Contre
                lambda: [self.press_key('left', 0.1), self.press_key('left', 0.1)],  # Backdash
                lambda: self.press_key('j', 0.1),      # Kick défensif
            ]
        else:  # balanced
            actions = [
                lambda: self.press_key('right', 0.15),
                lambda: self.press_key('left', 0.15),
                lambda: self.press_key('a', 0.1),
                lambda: self.press_key('s', 0.1),
                lambda: self.press_key('d', 0.1),
                lambda: self.press_key('j', 0.1),
                lambda: self.press_key('k', 0.1),
                lambda: self.press_key('l', 0.1),
                lambda: self.press_key('up', 0.1),     # Jump
                lambda: [self.press_key('down', 0.05), self.press_key('right', 0.05), self.press_key('s', 0.1)],
            ]

        # Choisir et exécuter une action
        action = random.choice(actions)
        try:
            result = action()
            if isinstance(result, list):
                for a in result:
                    if callable(a):
                        a()
        except Exception as e:
            self.log(f"Erreur action combat: {e}", "WARNING")

        # Pause aléatoire entre actions
        time.sleep(random.uniform(0.05, 0.25))

    def play_match(self, duration=120):
        """Joue un match complet"""
        self.log(f"🎮 Début du match ({duration}s)")
        self.current_match_start = time.time()

        # Attendre que le match commence
        time.sleep(5)

        # Jouer pendant la durée spécifiée
        start_time = time.time()
        actions_count = 0

        while (time.time() - start_time) < duration:
            self.perform_combat_action()
            actions_count += 1

            # Pause occasionnelle pour réalisme
            if random.random() < 0.03:  # 3% chance
                time.sleep(random.uniform(0.3, 1.0))

        match_duration = time.time() - self.current_match_start
        self.stats['total_playtime'] += match_duration
        self.stats['matches_played'] += 1

        self.log(f"✓ Match terminé - {actions_count} actions en {match_duration:.1f}s")

    def handle_post_match(self):
        """Gère les écrans après le match"""
        self.log("Gestion post-match...")
        time.sleep(3)

        # Appuyer sur plusieurs touches pour passer tous les écrans
        for _ in range(6):
            self.press_key('return', 0.5)
            time.sleep(0.8)

        # Décider si on continue ou retourne au menu
        continue_mode = random.random() < 0.7  # 70% de chance de continuer

        if not continue_mode:
            self.log("Retour au menu principal")
            self.press_key('esc', 0.5)
            time.sleep(1)
            self.press_key('return', 0.5)
            time.sleep(2)
            self.current_mode = None
            return False
        else:
            self.log("Continue dans le mode actuel")
            return True

    def play_continuous_session(self, duration_minutes=60):
        """Joue en continu pendant une durée donnée"""
        self.log(f"═══ DÉBUT SESSION CONTINUE: {duration_minutes} minutes ═══")
        self.is_playing = True

        session_start = time.time()
        session_end = session_start + (duration_minutes * 60)

        while self.is_playing and time.time() < session_end:
            try:
                # Choisir un mode aléatoire
                mode = random.choice(GameModes.ALL)

                # Naviguer vers le mode
                self.navigate_to_mode_from_menu(mode)

                # Sélectionner personnages selon le mode
                if mode == GameModes.TEAM:
                    self.select_characters(3)  # 3 persos pour team
                else:
                    self.select_characters(1)

                # Sélectionner stage (sauf en training)
                if mode != GameModes.TRAINING:
                    self.select_stage()

                # Jouer le match
                match_duration = random.randint(90, 180)  # 1.5-3 min
                self.play_match(match_duration)

                # Post-match
                continue_in_mode = self.handle_post_match()

                # Pause entre matches
                pause_time = random.uniform(2, 6)
                self.log(f"Pause de {pause_time:.1f}s...")
                time.sleep(pause_time)

            except KeyboardInterrupt:
                self.log("Interruption utilisateur")
                break
            except Exception as e:
                self.log(f"Erreur: {e}", "ERROR")
                # Essayer de revenir au menu
                for _ in range(3):
                    self.press_key('esc', 0.5)
                    time.sleep(0.5)
                time.sleep(2)

        self.is_playing = False
        self.save_stats()
        self.log(f"═══ SESSION TERMINÉE ═══")
        self.print_summary()

    def save_stats(self):
        """Sauvegarde les statistiques"""
        stats_file = self.logs_dir / f"stats_{self.player_id}.json"
        try:
            # Convertir defaultdict en dict normal pour JSON
            stats_copy = dict(self.stats)
            stats_copy['modes_played'] = dict(stats_copy['modes_played'])
            stats_copy['characters_used'] = dict(stats_copy['characters_used'])
            stats_copy['stages_played'] = dict(stats_copy['stages_played'])

            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats_copy, f, indent=2, ensure_ascii=False)

            self.log(f"Stats sauvegardées: {stats_file}")
        except Exception as e:
            self.log(f"Erreur sauvegarde stats: {e}", "ERROR")

    def print_summary(self):
        """Affiche un résumé de la session"""
        print(f"\n{'='*70}")
        print(f"RÉSUMÉ SESSION - {self.name}")
        print(f"{'='*70}")
        print(f"Matches joués:       {self.stats['matches_played']}")
        print(f"Actions effectuées:  {self.stats['actions_performed']}")
        print(f"Temps de jeu:        {self.stats['total_playtime']/60:.1f} min")
        print(f"\nModes joués:")
        for mode, count in self.stats['modes_played'].items():
            print(f"  • {mode}: {count}")
        print(f"{'='*70}\n")


class VirtualPlayersOrchestrator:
    """Orchestre plusieurs joueurs virtuels en parallèle"""

    def __init__(self, game_dir, num_players=3):
        self.game_dir = Path(game_dir)
        self.num_players = num_players
        self.players = []
        self.threads = []

    def create_players(self):
        """Crée tous les joueurs virtuels"""
        print(f"\n🤖 Création de {self.num_players} joueurs virtuels...\n")

        personalities = ["aggressive", "defensive", "balanced"]

        for i in range(self.num_players):
            personality = personalities[i % len(personalities)]
            name = self.generate_player_name(i)

            player = VirtualPlayer(
                player_id=i+1,
                name=name,
                game_dir=self.game_dir,
                personality=personality
            )

            self.players.append(player)
            print(f"  ✓ {name} créé (Personnalité: {personality})")

        print(f"\n✅ {len(self.players)} joueurs créés!\n")

    def generate_player_name(self, index):
        """Génère un nom de joueur"""
        prefixes = ["Dark", "Fire", "Ice", "Storm", "Shadow", "Thunder", "Dragon", "Wolf"]
        suffixes = ["Fighter", "Master", "King", "Warrior", "Slayer", "Champion", "Pro", "Ace"]

        return f"{random.choice(prefixes)}{random.choice(suffixes)}{index+1}"

    def start_all_players(self, duration_minutes=60):
        """Lance tous les joueurs en parallèle"""
        print(f"\n🚀 Lancement de tous les joueurs virtuels...\n")
        print(f"Durée de session: {duration_minutes} minutes")
        print(f"{'='*70}\n")

        # Créer un thread pour chaque joueur
        for player in self.players:
            thread = threading.Thread(
                target=player.play_continuous_session,
                args=(duration_minutes,),
                name=player.name
            )
            thread.daemon = True
            self.threads.append(thread)

        # Démarrer tous les threads avec un petit délai
        for i, thread in enumerate(self.threads):
            thread.start()
            print(f"  ▶️  {self.players[i].name} lancé")
            time.sleep(2)  # Délai entre chaque joueur

        print(f"\n{'='*70}")
        print(f"✅ Tous les joueurs virtuels sont actifs!")
        print(f"{'='*70}\n")

    def wait_for_completion(self):
        """Attend que tous les joueurs terminent"""
        try:
            for thread in self.threads:
                thread.join()
        except KeyboardInterrupt:
            print("\n\n⚠️  Interruption - Arrêt de tous les joueurs...\n")
            for player in self.players:
                player.is_playing = False
            time.sleep(3)

    def print_global_stats(self):
        """Affiche les statistiques globales"""
        print(f"\n{'='*70}")
        print(f"STATISTIQUES GLOBALES")
        print(f"{'='*70}")

        total_matches = sum(p.stats['matches_played'] for p in self.players)
        total_actions = sum(p.stats['actions_performed'] for p in self.players)
        total_playtime = sum(p.stats['total_playtime'] for p in self.players)

        print(f"Joueurs actifs:      {len(self.players)}")
        print(f"Matches totaux:      {total_matches}")
        print(f"Actions totales:     {total_actions}")
        print(f"Temps de jeu total:  {total_playtime/60:.1f} min")

        print(f"\nTop joueurs par matches:")
        sorted_players = sorted(self.players, key=lambda p: p.stats['matches_played'], reverse=True)
        for i, player in enumerate(sorted_players[:5], 1):
            print(f"  {i}. {player.name}: {player.stats['matches_played']} matches")

        print(f"{'='*70}\n")


def main():
    """Point d'entrée principal"""
    print("\n" + "="*70)
    print("  🎮 SYSTÈME DE JOUEURS VIRTUELS EN CONTINU")
    print("  KOF Ultimate Online")
    print("="*70)

    game_dir = r"D:\KOF Ultimate Online"

    # Configuration
    num_players = 3
    session_duration = 120  # minutes (2 heures)

    print(f"\nConfiguration:")
    print(f"  • Nombre de joueurs: {num_players}")
    print(f"  • Durée session: {session_duration} min")
    print(f"  • Répertoire jeu: {game_dir}")

    # Créer l'orchestrateur
    orchestrator = VirtualPlayersOrchestrator(game_dir, num_players)

    # Créer les joueurs
    orchestrator.create_players()

    input("\n▶️  Appuyez sur ENTRÉE pour lancer tous les joueurs virtuels...")

    try:
        # Lancer tous les joueurs
        orchestrator.start_all_players(session_duration)

        # Attendre la fin
        print("\n⏳ Les joueurs virtuels sont en action...")
        print("   Appuyez sur Ctrl+C pour arrêter\n")

        orchestrator.wait_for_completion()

    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt demandé...")
    finally:
        # Sauvegarder toutes les stats
        for player in orchestrator.players:
            player.save_stats()

        # Afficher stats globales
        orchestrator.print_global_stats()

    print("\n✅ Programme terminé!\n")


if __name__ == "__main__":
    main()
