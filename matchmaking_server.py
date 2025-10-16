"""
KOF Ultimate Online - Serveur de Matchmaking
Serveur de matchmaking avec système MMR (MatchMaking Rating)
"""

import socket
import threading
import json
import time
from datetime import datetime
from collections import deque


class MatchmakingServer:
    """Serveur de matchmaking avec système MMR"""

    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False

        # File d'attente des joueurs par mode de jeu
        self.ranked_queue = deque()      # Mode classé
        self.quick_queue = deque()       # Match rapide
        self.custom_lobbies = {}         # Lobbies personnalisés

        # Joueurs connectés
        self.connected_players = {}  # {username: player_data}

        # Matchs en cours
        self.active_matches = []

        # Lock pour thread-safety
        self.queue_lock = threading.Lock()
        self.players_lock = threading.Lock()

        # Statistiques du serveur
        self.stats = {
            "total_connections": 0,
            "total_matches": 0,
            "players_online": 0
        }

    def start(self):
        """Démarre le serveur"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(50)
            self.running = True

            print(f"🚀 Serveur de matchmaking démarré sur {self.host}:{self.port}")
            print(f"✓ En attente de connexions...")

            # Thread pour le matchmaking automatique
            matchmaking_thread = threading.Thread(target=self._matchmaking_loop, daemon=True)
            matchmaking_thread.start()

            # Boucle principale d'acceptation des connexions
            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    self.stats["total_connections"] += 1

                    # Gérer chaque client dans un thread séparé
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, address),
                        daemon=True
                    )
                    client_thread.start()

                except Exception as e:
                    if self.running:
                        print(f"❌ Erreur d'acceptation: {e}")

        except Exception as e:
            print(f"❌ Erreur de démarrage du serveur: {e}")
        finally:
            self.stop()

    def stop(self):
        """Arrête le serveur"""
        print("\n🛑 Arrêt du serveur...")
        self.running = False

        if self.server_socket:
            self.server_socket.close()

        print("✓ Serveur arrêté")

    def _handle_client(self, client_socket, address):
        """Gère la connexion d'un client"""
        username = None

        try:
            # Recevoir les données du joueur
            data = client_socket.recv(4096).decode('utf-8')
            if not data:
                return

            request = json.loads(data)
            action = request.get("action")

            if action == "connect":
                # Connexion d'un joueur
                username = request.get("username")
                player_data = request.get("player_data")

                with self.players_lock:
                    self.connected_players[username] = {
                        "username": username,
                        "socket": client_socket,
                        "address": address,
                        "stats": player_data.get("stats"),
                        "connected_at": datetime.now().isoformat(),
                        "status": "online"
                    }
                    self.stats["players_online"] = len(self.connected_players)

                print(f"✓ {username} connecté ({address[0]}:{address[1]}) - MMR: {player_data['stats']['ranking_points']}")

                # Envoyer confirmation
                response = {
                    "status": "success",
                    "message": "Connexion réussie",
                    "server_stats": self.stats
                }
                client_socket.send(json.dumps(response).encode('utf-8'))

                # Garder la connexion ouverte pour recevoir d'autres commandes
                self._handle_player_commands(client_socket, username)

            elif action == "disconnect":
                username = request.get("username")
                self._disconnect_player(username)

        except json.JSONDecodeError:
            print(f"❌ Données JSON invalides de {address}")
        except Exception as e:
            print(f"❌ Erreur client {address}: {e}")
        finally:
            if username:
                self._disconnect_player(username)
            try:
                client_socket.close()
            except:
                pass

    def _handle_player_commands(self, client_socket, username):
        """Gère les commandes d'un joueur connecté"""
        try:
            while self.running:
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break

                request = json.loads(data)
                action = request.get("action")

                if action == "search_match":
                    mode = request.get("mode", "ranked")
                    self._add_to_queue(username, mode)

                    response = {
                        "status": "success",
                        "message": "Recherche lancée",
                        "mode": mode
                    }
                    client_socket.send(json.dumps(response).encode('utf-8'))

                elif action == "cancel_search":
                    self._remove_from_queue(username)

                    response = {
                        "status": "success",
                        "message": "Recherche annulée"
                    }
                    client_socket.send(json.dumps(response).encode('utf-8'))

                elif action == "get_stats":
                    response = {
                        "status": "success",
                        "stats": self.stats,
                        "queue_size": {
                            "ranked": len(self.ranked_queue),
                            "quick": len(self.quick_queue)
                        }
                    }
                    client_socket.send(json.dumps(response).encode('utf-8'))

                elif action == "disconnect":
                    break

        except Exception as e:
            print(f"❌ Erreur commande pour {username}: {e}")

    def _add_to_queue(self, username, mode):
        """Ajoute un joueur à la file d'attente"""
        with self.players_lock:
            if username not in self.connected_players:
                return

            player = self.connected_players[username]
            player["status"] = "searching"
            player["search_mode"] = mode
            player["search_started"] = time.time()

        with self.queue_lock:
            queue_entry = {
                "username": username,
                "mmr": player["stats"]["ranking_points"],
                "joined_at": time.time()
            }

            if mode == "ranked":
                self.ranked_queue.append(queue_entry)
            elif mode == "quick":
                self.quick_queue.append(queue_entry)

        print(f"🔍 {username} recherche un match ({mode}) - MMR: {player['stats']['ranking_points']}")

    def _remove_from_queue(self, username):
        """Retire un joueur de la file d'attente"""
        with self.queue_lock:
            # Retirer de ranked
            self.ranked_queue = deque([p for p in self.ranked_queue if p["username"] != username])

            # Retirer de quick
            self.quick_queue = deque([p for p in self.quick_queue if p["username"] != username])

        with self.players_lock:
            if username in self.connected_players:
                self.connected_players[username]["status"] = "online"

        print(f"❌ {username} a annulé sa recherche")

    def _matchmaking_loop(self):
        """Boucle de matchmaking automatique"""
        print("🎮 Système de matchmaking activé")

        while self.running:
            try:
                # Matchmaking pour mode classé (MMR strict)
                self._process_ranked_queue()

                # Matchmaking pour mode rapide (MMR flexible)
                self._process_quick_queue()

                time.sleep(1)  # Vérifier toutes les secondes

            except Exception as e:
                print(f"❌ Erreur matchmaking: {e}")

    def _process_ranked_queue(self):
        """Traite la file d'attente classée avec MMR strict"""
        with self.queue_lock:
            if len(self.ranked_queue) < 2:
                return

            # Trier par MMR
            sorted_queue = sorted(self.ranked_queue, key=lambda x: x["mmr"])

            i = 0
            while i < len(sorted_queue) - 1:
                player1 = sorted_queue[i]
                player2 = sorted_queue[i + 1]

                # Calculer la différence de MMR
                mmr_diff = abs(player1["mmr"] - player2["mmr"])

                # Temps d'attente (plus on attend, plus on accepte un écart de MMR)
                wait_time1 = time.time() - player1["joined_at"]
                wait_time2 = time.time() - player2["joined_at"]
                avg_wait = (wait_time1 + wait_time2) / 2

                # Seuil de MMR adaptatif
                mmr_threshold = 50 + (avg_wait * 5)  # 50 de base, +5 par seconde d'attente

                if mmr_diff <= mmr_threshold:
                    # Match trouvé!
                    self._create_match(player1["username"], player2["username"], "ranked")

                    # Retirer de la file
                    self.ranked_queue.remove(player1)
                    self.ranked_queue.remove(player2)

                    # Ne pas incrémenter i car on a retiré des éléments
                else:
                    i += 1

    def _process_quick_queue(self):
        """Traite la file d'attente rapide (MMR flexible)"""
        with self.queue_lock:
            if len(self.quick_queue) < 2:
                return

            # Match rapide: prendre les 2 premiers joueurs
            player1 = self.quick_queue.popleft()
            player2 = self.quick_queue.popleft()

            self._create_match(player1["username"], player2["username"], "quick")

    def _create_match(self, username1, username2, mode):
        """Crée un match entre deux joueurs"""
        with self.players_lock:
            if username1 not in self.connected_players or username2 not in self.connected_players:
                return

            player1 = self.connected_players[username1]
            player2 = self.connected_players[username2]

            # Créer le match
            match = {
                "match_id": f"match_{self.stats['total_matches']}",
                "mode": mode,
                "player1": username1,
                "player2": username2,
                "player1_mmr": player1["stats"]["ranking_points"],
                "player2_mmr": player2["stats"]["ranking_points"],
                "created_at": datetime.now().isoformat()
            }

            self.active_matches.append(match)
            self.stats["total_matches"] += 1

            # Mettre à jour le statut des joueurs
            player1["status"] = "in_match"
            player2["status"] = "in_match"

            print(f"✅ MATCH TROUVÉ! {username1} ({player1['stats']['ranking_points']}) vs {username2} ({player2['stats']['ranking_points']})")

            # Notifier les joueurs
            self._notify_match_found(player1, player2, match)
            self._notify_match_found(player2, player1, match)

    def _notify_match_found(self, player, opponent, match):
        """Notifie un joueur qu'un match a été trouvé"""
        try:
            notification = {
                "event": "match_found",
                "match_id": match["match_id"],
                "mode": match["mode"],
                "opponent": {
                    "username": opponent["username"],
                    "mmr": opponent["stats"]["ranking_points"],
                    "level": opponent["stats"]["level"],
                    "wins": opponent["stats"]["wins"],
                    "losses": opponent["stats"]["losses"]
                }
            }

            player["socket"].send(json.dumps(notification).encode('utf-8'))

        except Exception as e:
            print(f"❌ Erreur notification pour {player['username']}: {e}")

    def _disconnect_player(self, username):
        """Déconnecte un joueur"""
        # Retirer de la file d'attente
        self._remove_from_queue(username)

        # Retirer des joueurs connectés
        with self.players_lock:
            if username in self.connected_players:
                del self.connected_players[username]
                self.stats["players_online"] = len(self.connected_players)

        print(f"👋 {username} déconnecté")

    def get_status(self):
        """Retourne le statut du serveur"""
        return {
            "running": self.running,
            "stats": self.stats,
            "queue_sizes": {
                "ranked": len(self.ranked_queue),
                "quick": len(self.quick_queue)
            },
            "active_matches": len(self.active_matches)
        }


def main():
    """Lance le serveur"""
    server = MatchmakingServer(host='0.0.0.0', port=9999)

    try:
        print("=" * 60)
        print("   KOF ULTIMATE ONLINE - SERVEUR DE MATCHMAKING")
        print("=" * 60)
        print("")

        server.start()

    except KeyboardInterrupt:
        print("\n\n⚠️  Arrêt demandé par l'utilisateur")
        server.stop()


if __name__ == "__main__":
    main()
