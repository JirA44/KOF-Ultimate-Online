"""
KOF Ultimate Online - Client de Matchmaking
Client pour se connecter au serveur de matchmaking
"""

import socket
import json
import threading


class MatchmakingClient:
    """Client de connexion au serveur de matchmaking"""

    def __init__(self, server_host='127.0.0.1', server_port=9999):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None
        self.connected = False
        self.username = None
        self.player_data = None

        # Callback pour les événements
        self.on_match_found = None
        self.on_connected = None
        self.on_disconnected = None
        self.on_error = None

        # Thread de réception
        self.receive_thread = None

    def connect(self, username, player_data):
        """Se connecte au serveur de matchmaking"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))

            self.username = username
            self.player_data = player_data

            # Envoyer les données de connexion
            request = {
                "action": "connect",
                "username": username,
                "player_data": player_data
            }

            self.socket.send(json.dumps(request).encode('utf-8'))

            # Recevoir la confirmation
            response_data = self.socket.recv(4096).decode('utf-8')
            response = json.loads(response_data)

            if response.get("status") == "success":
                self.connected = True
                print(f"✓ Connecté au serveur de matchmaking")

                # Démarrer le thread de réception
                self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
                self.receive_thread.start()

                if self.on_connected:
                    self.on_connected(response)

                return True
            else:
                print(f"❌ Échec de connexion: {response.get('message')}")
                return False

        except ConnectionRefusedError:
            print(f"❌ Impossible de se connecter au serveur {self.server_host}:{self.server_port}")
            print(f"⚠️  Assurez-vous que le serveur est démarré!")
            if self.on_error:
                self.on_error("Serveur inaccessible")
            return False
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            if self.on_error:
                self.on_error(str(e))
            return False

    def disconnect(self):
        """Se déconnecte du serveur"""
        if not self.connected:
            return

        try:
            request = {
                "action": "disconnect",
                "username": self.username
            }
            self.socket.send(json.dumps(request).encode('utf-8'))
        except:
            pass

        self.connected = False

        if self.socket:
            self.socket.close()

        if self.on_disconnected:
            self.on_disconnected()

        print("👋 Déconnecté du serveur")

    def search_match(self, mode="ranked"):
        """Lance une recherche de match"""
        if not self.connected:
            print("❌ Non connecté au serveur")
            return False

        try:
            request = {
                "action": "search_match",
                "mode": mode
            }
            self.socket.send(json.dumps(request).encode('utf-8'))

            # Recevoir la confirmation
            response_data = self.socket.recv(4096).decode('utf-8')
            response = json.loads(response_data)

            if response.get("status") == "success":
                print(f"🔍 Recherche lancée ({mode})")
                return True
            else:
                print(f"❌ Échec de la recherche")
                return False

        except Exception as e:
            print(f"❌ Erreur recherche: {e}")
            return False

    def cancel_search(self):
        """Annule la recherche en cours"""
        if not self.connected:
            return False

        try:
            request = {
                "action": "cancel_search"
            }
            self.socket.send(json.dumps(request).encode('utf-8'))

            # Recevoir la confirmation
            response_data = self.socket.recv(4096).decode('utf-8')
            response = json.loads(response_data)

            if response.get("status") == "success":
                print("❌ Recherche annulée")
                return True

        except Exception as e:
            print(f"❌ Erreur annulation: {e}")
            return False

    def get_server_stats(self):
        """Récupère les statistiques du serveur"""
        if not self.connected:
            return None

        try:
            request = {
                "action": "get_stats"
            }
            self.socket.send(json.dumps(request).encode('utf-8'))

            response_data = self.socket.recv(4096).decode('utf-8')
            response = json.loads(response_data)

            if response.get("status") == "success":
                return response

        except Exception as e:
            print(f"❌ Erreur stats: {e}")
            return None

    def _receive_loop(self):
        """Boucle de réception des messages du serveur"""
        while self.connected:
            try:
                data = self.socket.recv(4096).decode('utf-8')
                if not data:
                    break

                message = json.loads(data)
                self._handle_server_message(message)

            except Exception as e:
                if self.connected:
                    print(f"❌ Erreur réception: {e}")
                break

        # Connexion perdue
        self.connected = False
        if self.on_disconnected:
            self.on_disconnected()

    def _handle_server_message(self, message):
        """Gère les messages du serveur"""
        event = message.get("event")

        if event == "match_found":
            print(f"✅ Match trouvé!")
            if self.on_match_found:
                self.on_match_found(message)

        else:
            print(f"📩 Message serveur: {message}")
