#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE ONLINE - Serveur Matchmaking Style Battle.net
Serveur central pour gérer les parties multijoueurs
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Set
import logging
import websockets
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Player:
    """Représente un joueur connecté"""

    def __init__(self, websocket, player_id: str):
        self.websocket = websocket
        self.id = player_id
        self.username = None
        self.elo = 1000
        self.status = "online"  # online, searching, in_game
        self.current_match = None
        self.connected_at = datetime.now()
        self.wins = 0
        self.losses = 0
        self.ping = 0

    @property
    def win_rate(self):
        total = self.wins + self.losses
        return (self.wins / total * 100) if total > 0 else 0

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "elo": self.elo,
            "status": self.status,
            "wins": self.wins,
            "losses": self.losses,
            "win_rate": self.win_rate,
            "ping": self.ping
        }


class Match:
    """Représente une partie en cours"""

    def __init__(self, match_id: str, player1: Player, player2: Player):
        self.id = match_id
        self.player1 = player1
        self.player2 = player2
        self.created_at = datetime.now()
        self.started_at = None
        self.ended_at = None
        self.winner = None
        self.status = "waiting"  # waiting, active, finished

    def start(self):
        """Démarre la partie"""
        self.started_at = datetime.now()
        self.status = "active"
        self.player1.status = "in_game"
        self.player2.status = "in_game"
        self.player1.current_match = self.id
        self.player2.current_match = self.id

    def finish(self, winner_id: str):
        """Termine la partie"""
        self.ended_at = datetime.now()
        self.status = "finished"
        self.winner = winner_id

        # Mettre à jour les stats
        if winner_id == self.player1.id:
            self.player1.wins += 1
            self.player2.losses += 1
        else:
            self.player2.wins += 1
            self.player1.losses += 1

        # Calculer le nouveau ELO
        self._update_elo(winner_id)

        # Réinitialiser les statuts
        self.player1.status = "online"
        self.player2.status = "online"
        self.player1.current_match = None
        self.player2.current_match = None

    def _update_elo(self, winner_id: str):
        """Calcule et met à jour l'ELO selon le système Battle.net"""
        K = 32  # Facteur K (sensibilité du changement)

        winner = self.player1 if winner_id == self.player1.id else self.player2
        loser = self.player2 if winner_id == self.player1.id else self.player1

        # Probabilité de victoire attendue
        expected_winner = 1 / (1 + 10 ** ((loser.elo - winner.elo) / 400))
        expected_loser = 1 - expected_winner

        # Nouveau ELO
        winner.elo = int(winner.elo + K * (1 - expected_winner))
        loser.elo = int(loser.elo + K * (0 - expected_loser))

        # Empêcher l'ELO de descendre en dessous de 0
        winner.elo = max(0, winner.elo)
        loser.elo = max(0, loser.elo)

    def to_dict(self):
        return {
            "id": self.id,
            "player1": self.player1.to_dict(),
            "player2": self.player2.to_dict(),
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "winner": self.winner
        }


class BattleNetServer:
    """Serveur principal style Battle.net"""

    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        self.host = host
        self.port = port

        # Collections
        self.players: Dict[str, Player] = {}
        self.matches: Dict[str, Match] = {}
        self.searching_players: List[Player] = []

        # Stats
        self.total_matches = 0
        self.total_players_connected = 0

        # Tasks
        self.matchmaking_task = None

    async def start(self):
        """Démarre le serveur"""
        logger.info(f"🚀 Serveur Battle.net démarré sur {self.host}:{self.port}")

        # Démarrer le matchmaking en arrière-plan
        self.matchmaking_task = asyncio.create_task(self.matchmaking_loop())

        # Démarrer le serveur WebSocket
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()  # Run forever

    async def handle_client(self, websocket, path):
        """Gère la connexion d'un client"""
        player_id = None

        try:
            # Recevoir l'authentification
            auth_msg = await websocket.recv()
            auth_data = json.loads(auth_msg)

            if auth_data.get("type") != "auth":
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Authentication required"
                }))
                return

            # Créer le joueur
            player_id = auth_data.get("player_id", f"player_{len(self.players)}")
            player = Player(websocket, player_id)
            player.username = auth_data.get("username", f"Player{len(self.players)}")

            # Charger les stats si disponibles
            if "elo" in auth_data:
                player.elo = auth_data["elo"]
            if "wins" in auth_data:
                player.wins = auth_data["wins"]
            if "losses" in auth_data:
                player.losses = auth_data["losses"]

            self.players[player_id] = player
            self.total_players_connected += 1

            logger.info(f"✅ {player.username} connecté (ELO: {player.elo})")

            # Envoyer la confirmation
            await websocket.send(json.dumps({
                "type": "auth_success",
                "player": player.to_dict()
            }))

            # Envoyer les stats du serveur
            await self.send_server_stats(player)

            # Boucle de communication
            async for message in websocket:
                await self.handle_message(player, message)

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"❌ {player_id} déconnecté")
        except Exception as e:
            logger.error(f"Erreur client {player_id}: {e}")
        finally:
            # Nettoyage
            if player_id and player_id in self.players:
                player = self.players[player_id]

                # Retirer de la recherche
                if player in self.searching_players:
                    self.searching_players.remove(player)

                # Abandonner la partie en cours
                if player.current_match:
                    await self.handle_disconnect_during_match(player)

                del self.players[player_id]

    async def handle_message(self, player: Player, message: str):
        """Traite un message d'un joueur"""
        try:
            data = json.loads(message)
            msg_type = data.get("type")

            if msg_type == "search_match":
                await self.start_search(player)

            elif msg_type == "cancel_search":
                await self.cancel_search(player)

            elif msg_type == "match_result":
                await self.handle_match_result(player, data)

            elif msg_type == "ping":
                await player.websocket.send(json.dumps({
                    "type": "pong",
                    "timestamp": time.time()
                }))

            elif msg_type == "get_leaderboard":
                await self.send_leaderboard(player)

            elif msg_type == "get_online_players":
                await self.send_online_players(player)

        except Exception as e:
            logger.error(f"Erreur traitement message de {player.username}: {e}")

    async def start_search(self, player: Player):
        """Commence la recherche d'adversaire"""
        if player.status != "online":
            await player.websocket.send(json.dumps({
                "type": "error",
                "message": "Cannot search while in game"
            }))
            return

        player.status = "searching"
        self.searching_players.append(player)

        logger.info(f"🔍 {player.username} recherche un adversaire (ELO: {player.elo})")

        await player.websocket.send(json.dumps({
            "type": "search_started",
            "message": "Recherche d'adversaire en cours..."
        }))

    async def cancel_search(self, player: Player):
        """Annule la recherche d'adversaire"""
        if player in self.searching_players:
            self.searching_players.remove(player)
            player.status = "online"

            await player.websocket.send(json.dumps({
                "type": "search_cancelled"
            }))

    async def matchmaking_loop(self):
        """Boucle de matchmaking (comme Battle.net)"""
        while True:
            try:
                await asyncio.sleep(1)

                if len(self.searching_players) < 2:
                    continue

                # Trier par ELO
                self.searching_players.sort(key=lambda p: p.elo)

                # Essayer de matcher des joueurs avec des ELO proches
                matched = []

                for i in range(len(self.searching_players) - 1):
                    p1 = self.searching_players[i]
                    p2 = self.searching_players[i + 1]

                    # Vérifier la différence d'ELO (max 200 points)
                    elo_diff = abs(p1.elo - p2.elo)

                    if elo_diff <= 200:
                        await self.create_match(p1, p2)
                        matched.extend([p1, p2])

                # Retirer les joueurs matchés
                for player in matched:
                    self.searching_players.remove(player)

            except Exception as e:
                logger.error(f"Erreur matchmaking: {e}")

    async def create_match(self, player1: Player, player2: Player):
        """Crée une nouvelle partie"""
        match_id = f"match_{self.total_matches}"
        self.total_matches += 1

        match = Match(match_id, player1, player2)
        self.matches[match_id] = match
        match.start()

        logger.info(f"⚔️ Match créé: {player1.username} vs {player2.username} (ID: {match_id})")

        # Notifier les deux joueurs
        match_data = {
            "type": "match_found",
            "match": match.to_dict()
        }

        await player1.websocket.send(json.dumps({
            **match_data,
            "opponent": player2.to_dict()
        }))

        await player2.websocket.send(json.dumps({
            **match_data,
            "opponent": player1.to_dict()
        }))

    async def handle_match_result(self, player: Player, data: dict):
        """Traite le résultat d'une partie"""
        match_id = player.current_match

        if not match_id or match_id not in self.matches:
            return

        match = self.matches[match_id]
        winner_id = data.get("winner_id")

        match.finish(winner_id)

        logger.info(f"🏆 Match terminé: {match.winner} a gagné (Match ID: {match_id})")

        # Notifier les deux joueurs
        result_data = {
            "type": "match_finished",
            "match": match.to_dict(),
            "your_new_elo": player.elo
        }

        await match.player1.websocket.send(json.dumps(result_data))
        await match.player2.websocket.send(json.dumps(result_data))

    async def handle_disconnect_during_match(self, player: Player):
        """Gère la déconnexion pendant une partie"""
        match_id = player.current_match

        if not match_id or match_id not in self.matches:
            return

        match = self.matches[match_id]
        opponent = match.player2 if match.player1.id == player.id else match.player1

        # Le joueur déconnecté perd
        match.finish(opponent.id)

        logger.warning(f"⚠️ {player.username} s'est déconnecté pendant le match")

        # Notifier l'adversaire
        await opponent.websocket.send(json.dumps({
            "type": "opponent_disconnected",
            "message": "Votre adversaire s'est déconnecté. Vous gagnez par forfait.",
            "your_new_elo": opponent.elo
        }))

    async def send_server_stats(self, player: Player):
        """Envoie les statistiques du serveur"""
        stats = {
            "type": "server_stats",
            "online_players": len(self.players),
            "searching_players": len(self.searching_players),
            "active_matches": sum(1 for m in self.matches.values() if m.status == "active"),
            "total_matches": self.total_matches,
            "total_players": self.total_players_connected
        }

        await player.websocket.send(json.dumps(stats))

    async def send_leaderboard(self, player: Player):
        """Envoie le classement"""
        # Trier les joueurs par ELO
        sorted_players = sorted(
            self.players.values(),
            key=lambda p: p.elo,
            reverse=True
        )

        leaderboard = {
            "type": "leaderboard",
            "players": [p.to_dict() for p in sorted_players[:100]]  # Top 100
        }

        await player.websocket.send(json.dumps(leaderboard))

    async def send_online_players(self, player: Player):
        """Envoie la liste des joueurs en ligne"""
        online = {
            "type": "online_players",
            "players": [p.to_dict() for p in self.players.values()]
        }

        await player.websocket.send(json.dumps(online))


async def main():
    """Point d'entrée principal"""
    server = BattleNetServer(host="0.0.0.0", port=8765)
    await server.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n🛑 Serveur arrêté")
