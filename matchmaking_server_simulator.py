"""
Serveur de Matchmaking Simulé - KOF Ultimate Online
Simule un serveur de matchmaking avec joueurs virtuels
"""

import asyncio
import json
import time
import random
from datetime import datetime
from pathlib import Path
import http.server
import socketserver
import threading

# Configuration
PORT_MATCHMAKING = 8765
PORT_DASHBOARD = 8501
GAME_PATH = Path(__file__).parent

class MatchmakingServer:
    def __init__(self):
        self.players_online = {}
        self.players_in_queue = []
        self.active_matches = []
        self.match_history = []
        self.match_id_counter = 0

        # Statistiques
        self.stats = {
            'total_players': 0,
            'total_matches': 0,
            'total_queue_time': 0,
            'avg_queue_time': 0
        }

    def add_player(self, player_id, player_data):
        """Ajoute un joueur en ligne"""
        self.players_online[player_id] = {
            **player_data,
            'connected_at': time.time(),
            'status': 'online'
        }
        self.stats['total_players'] += 1
        print(f"🎮 Joueur connecté: {player_data['username']} (Total: {len(self.players_online)})")

    def remove_player(self, player_id):
        """Retire un joueur"""
        if player_id in self.players_online:
            player = self.players_online[player_id]
            print(f"👋 Joueur déconnecté: {player['username']}")
            del self.players_online[player_id]

            # Retirer de la queue si présent
            self.players_in_queue = [p for p in self.players_in_queue if p['player_id'] != player_id]

    def add_to_queue(self, player_id):
        """Ajoute un joueur à la file d'attente"""
        if player_id in self.players_online:
            player = self.players_online[player_id]
            queue_entry = {
                'player_id': player_id,
                'username': player['username'],
                'rank': player['rank'],
                'joined_queue_at': time.time()
            }
            self.players_in_queue.append(queue_entry)
            player['status'] = 'searching'
            print(f"🔍 {player['username']} recherche un match... (Queue: {len(self.players_in_queue)})")

    def try_matchmaking(self):
        """Essaie de créer des matchs avec les joueurs en queue"""
        matches_created = 0

        while len(self.players_in_queue) >= 2:
            # Prendre les 2 premiers joueurs (FIFO)
            player1 = self.players_in_queue.pop(0)
            player2 = self.players_in_queue.pop(0)

            # Créer le match
            match = self.create_match(player1, player2)
            matches_created += 1

        return matches_created

    def create_match(self, player1_queue, player2_queue):
        """Crée un match entre 2 joueurs"""
        self.match_id_counter += 1

        player1_id = player1_queue['player_id']
        player2_id = player2_queue['player_id']

        # Calculer temps d'attente
        queue_time_p1 = time.time() - player1_queue['joined_queue_at']
        queue_time_p2 = time.time() - player2_queue['joined_queue_at']
        avg_queue_time = (queue_time_p1 + queue_time_p2) / 2

        match = {
            'match_id': self.match_id_counter,
            'player1': {
                'player_id': player1_id,
                'username': player1_queue['username'],
                'rank': player1_queue['rank']
            },
            'player2': {
                'player_id': player2_id,
                'username': player2_queue['username'],
                'rank': player2_queue['rank']
            },
            'started_at': time.time(),
            'queue_time': avg_queue_time,
            'status': 'in_progress'
        }

        self.active_matches.append(match)
        self.stats['total_matches'] += 1
        self.stats['total_queue_time'] += avg_queue_time
        self.stats['avg_queue_time'] = self.stats['total_queue_time'] / self.stats['total_matches']

        # Mettre à jour le statut des joueurs
        self.players_online[player1_id]['status'] = 'in_match'
        self.players_online[player2_id]['status'] = 'in_match'

        print(f"⚔️  MATCH #{self.match_id_counter}: {player1_queue['username']} VS {player2_queue['username']}")
        print(f"   Temps d'attente: {avg_queue_time:.1f}s")

        return match

    def finish_match(self, match_id, winner_id):
        """Termine un match"""
        match = next((m for m in self.active_matches if m['match_id'] == match_id), None)

        if match:
            match['finished_at'] = time.time()
            match['duration'] = match['finished_at'] - match['started_at']
            match['winner_id'] = winner_id
            match['status'] = 'finished'

            # Déterminer le gagnant
            if winner_id == match['player1']['player_id']:
                winner = match['player1']['username']
                loser = match['player2']['username']
            else:
                winner = match['player2']['username']
                loser = match['player1']['username']

            print(f"🏆 MATCH #{match_id} terminé: {winner} bat {loser} ({match['duration']:.1f}s)")

            # Déplacer vers l'historique
            self.match_history.append(match)
            self.active_matches.remove(match)

            # Remettre les joueurs en ligne
            if match['player1']['player_id'] in self.players_online:
                self.players_online[match['player1']['player_id']]['status'] = 'online'
            if match['player2']['player_id'] in self.players_online:
                self.players_online[match['player2']['player_id']]['status'] = 'online'

    def get_status(self):
        """Retourne le statut complet du serveur"""
        return {
            'timestamp': time.time(),
            'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'players_online': len(self.players_online),
            'players_in_queue': len(self.players_in_queue),
            'active_matches': len(self.active_matches),
            'total_matches': self.stats['total_matches'],
            'avg_queue_time': self.stats['avg_queue_time'],
            'players': list(self.players_online.values()),
            'queue': self.players_in_queue,
            'matches': self.active_matches,
            'history': self.match_history[-20:]  # Derniers 20 matchs
        }

    def save_status(self):
        """Sauvegarde le statut dans un fichier JSON"""
        status_file = GAME_PATH / "matchmaking_status.json"
        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump(self.get_status(), f, indent=2)


class DashboardHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """Handler HTTP pour le dashboard"""

    def __init__(self, *args, server_instance=None, **kwargs):
        self.server_instance = server_instance
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Gère les requêtes GET"""
        if self.path == '/api/status':
            # API JSON pour le statut
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            status = self.server_instance.matchmaking_server.get_status()
            self.wfile.write(json.dumps(status).encode())
        else:
            # Fichiers statiques
            super().do_GET()


def run_dashboard_server(matchmaking_server):
    """Lance le serveur HTTP du dashboard"""

    class DashboardServer(socketserver.TCPServer):
        allow_reuse_address = True

        def __init__(self, *args, **kwargs):
            self.matchmaking_server = matchmaking_server
            super().__init__(*args, **kwargs)

    handler = lambda *args, **kwargs: DashboardHTTPHandler(*args, server_instance=matchmaking_server, **kwargs)

    with DashboardServer(("", PORT_DASHBOARD), handler) as httpd:
        print(f"📊 Dashboard démarré sur http://localhost:{PORT_DASHBOARD}")
        httpd.serve_forever()


async def main():
    """Fonction principale"""
    print("="*60)
    print("🎮 KOF ULTIMATE - SERVEUR DE MATCHMAKING SIMULÉ")
    print("="*60)
    print()

    server = MatchmakingServer()

    # Lancer le serveur HTTP du dashboard dans un thread séparé
    dashboard_thread = threading.Thread(target=run_dashboard_server, args=(server,), daemon=True)
    dashboard_thread.start()

    print(f"🌐 Serveur de matchmaking prêt")
    print(f"📊 Dashboard: http://localhost:{PORT_DASHBOARD}")
    print()
    print("Appuyez sur Ctrl+C pour arrêter")
    print("="*60)
    print()

    # Boucle principale
    try:
        while True:
            # Sauvegarder le statut toutes les secondes
            server.save_status()

            # Essayer de créer des matchs
            matches_created = server.try_matchmaking()

            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt du serveur...")
        print(f"📊 Statistiques finales:")
        print(f"   • Total joueurs: {server.stats['total_players']}")
        print(f"   • Total matchs: {server.stats['total_matches']}")
        print(f"   • Temps d'attente moyen: {server.stats['avg_queue_time']:.1f}s")


if __name__ == "__main__":
    asyncio.run(main())
