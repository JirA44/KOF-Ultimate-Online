"""
KOF Ultimate Online - Test Automatique du Matchmaking
Lance 2 sessions IA qui testent le système de matchmaking
"""

import time
import threading
import random
from player_profile_system import PlayerProfileSystem
from matchmaking_client import MatchmakingClient


class AITestSession:
    """Session de test IA pour le matchmaking"""

    def __init__(self, session_id, username, password, pin):
        self.session_id = session_id
        self.username = username
        self.password = password
        self.pin = pin

        self.profile_system = PlayerProfileSystem()
        self.matchmaking_client = None
        self.profile = None
        self.match_found = False
        self.opponent_info = None

    def run(self):
        """Lance la session de test"""
        print(f"\n{'='*60}")
        print(f"  SESSION IA {self.session_id} - {self.username}")
        print(f"{'='*60}\n")

        # Étape 1: Créer ou charger le profil
        print(f"[IA {self.session_id}] 📝 Création/connexion au profil...")
        self._setup_profile()

        # Étape 2: Se connecter au serveur de matchmaking
        print(f"[IA {self.session_id}] 🔌 Connexion au serveur de matchmaking...")
        if not self._connect_to_server():
            print(f"[IA {self.session_id}] ❌ Échec de connexion au serveur")
            return

        # Étape 3: Attendre un peu avant de lancer la recherche
        wait_time = random.uniform(1, 3)
        print(f"[IA {self.session_id}] ⏱️  Attente de {wait_time:.1f}s avant la recherche...")
        time.sleep(wait_time)

        # Étape 4: Lancer la recherche de match
        print(f"[IA {self.session_id}] 🔍 Lancement de la recherche de match...")
        self._start_search()

        # Étape 5: Attendre qu'un match soit trouvé
        print(f"[IA {self.session_id}] ⏳ En attente d'un adversaire...")
        timeout = 30  # 30 secondes max
        elapsed = 0

        while not self.match_found and elapsed < timeout:
            time.sleep(1)
            elapsed += 1

            if elapsed % 5 == 0:
                print(f"[IA {self.session_id}] ⏳ Recherche en cours... ({elapsed}s)")

        # Étape 6: Vérifier si un match a été trouvé
        if self.match_found:
            print(f"\n[IA {self.session_id}] ✅ MATCH TROUVÉ!")
            print(f"[IA {self.session_id}] 🎮 Adversaire: {self.opponent_info['username']}")
            print(f"[IA {self.session_id}] 📊 MMR adversaire: {self.opponent_info['mmr']}")
            print(f"[IA {self.session_id}] 🏆 Niveau adversaire: {self.opponent_info['level']}")
            print(f"[IA {self.session_id}] 📈 Record: {self.opponent_info['wins']}W - {self.opponent_info['losses']}L")

            # Simuler l'acceptation du match
            time.sleep(2)
            print(f"[IA {self.session_id}] ✓ Match accepté!")

        else:
            print(f"[IA {self.session_id}] ⏱️  Timeout: Aucun match trouvé")

        # Étape 7: Se déconnecter
        time.sleep(2)
        print(f"[IA {self.session_id}] 👋 Déconnexion...")
        self._disconnect()

        print(f"\n[IA {self.session_id}] ✓ Session terminée\n")

    def _setup_profile(self):
        """Configure le profil du joueur"""
        # Vérifier si le profil existe
        existing_profile = self.profile_system.get_profile(self.username)

        if existing_profile:
            print(f"[IA {self.session_id}] ✓ Profil existant trouvé")
            self.profile = existing_profile
        else:
            # Créer un nouveau profil
            print(f"[IA {self.session_id}] 🆕 Création d'un nouveau profil")
            self.profile = self.profile_system.create_profile(
                self.username,
                self.password,
                self.pin
            )

            if not self.profile:
                print(f"[IA {self.session_id}] ❌ Échec de création du profil")
                return

        # Connexion au profil
        if self.profile_system.login(self.username, self.password, self.pin):
            print(f"[IA {self.session_id}] ✓ Connecté au profil")
            print(f"[IA {self.session_id}] 📊 MMR: {self.profile['stats']['ranking_points']}")
            print(f"[IA {self.session_id}] 🏆 Niveau: {self.profile['stats']['level']}")
        else:
            print(f"[IA {self.session_id}] ❌ Échec de connexion au profil")

    def _connect_to_server(self):
        """Se connecte au serveur de matchmaking"""
        self.matchmaking_client = MatchmakingClient()

        # Définir les callbacks
        self.matchmaking_client.on_match_found = self._on_match_found
        self.matchmaking_client.on_connected = self._on_connected
        self.matchmaking_client.on_disconnected = self._on_disconnected
        self.matchmaking_client.on_error = self._on_error

        # Se connecter
        success = self.matchmaking_client.connect(self.username, self.profile)

        if success:
            print(f"[IA {self.session_id}] ✓ Connecté au serveur")
            return True
        else:
            print(f"[IA {self.session_id}] ❌ Échec de connexion au serveur")
            return False

    def _start_search(self):
        """Lance la recherche de match"""
        mode = random.choice(["ranked", "quick"])
        success = self.matchmaking_client.search_match(mode)

        if success:
            print(f"[IA {self.session_id}] ✓ Recherche lancée (mode: {mode})")
        else:
            print(f"[IA {self.session_id}] ❌ Échec du lancement de la recherche")

    def _disconnect(self):
        """Se déconnecte du serveur"""
        if self.matchmaking_client:
            self.matchmaking_client.disconnect()

    # Callbacks
    def _on_match_found(self, match_data):
        """Callback quand un match est trouvé"""
        self.match_found = True
        self.opponent_info = match_data.get("opponent", {})

    def _on_connected(self, response):
        """Callback de connexion"""
        pass

    def _on_disconnected(self):
        """Callback de déconnexion"""
        pass

    def _on_error(self, error):
        """Callback d'erreur"""
        print(f"[IA {self.session_id}] ❌ Erreur: {error}")


def run_test():
    """Lance le test avec 2 sessions IA"""
    print("\n" + "="*60)
    print("   KOF ULTIMATE ONLINE - TEST AUTOMATIQUE MATCHMAKING")
    print("="*60)
    print("\n⚠️  PRÉREQUIS: Le serveur de matchmaking doit être lancé!")
    print("   Commande: python matchmaking_server.py\n")

    input("Appuyez sur Entrée pour lancer le test...")

    # Créer 2 sessions IA
    print("\n🤖 Création des sessions IA...\n")

    ai1 = AITestSession(
        session_id=1,
        username="AI_TestPlayer_1",
        password="test123",
        pin="1234"
    )

    ai2 = AITestSession(
        session_id=2,
        username="AI_TestPlayer_2",
        password="test456",
        pin="5678"
    )

    # Lancer les sessions dans des threads séparés
    print("🚀 Lancement des sessions de test...\n")

    thread1 = threading.Thread(target=ai1.run, daemon=False)
    thread2 = threading.Thread(target=ai2.run, daemon=False)

    thread1.start()
    thread2.start()

    # Attendre que les threads se terminent
    thread1.join()
    thread2.join()

    # Résumé
    print("\n" + "="*60)
    print("   RÉSUMÉ DU TEST")
    print("="*60)

    if ai1.match_found and ai2.match_found:
        print("✅ TEST RÉUSSI!")
        print(f"✓ {ai1.username} et {ai2.username} se sont connectés")

        if ai1.opponent_info and ai2.opponent_info:
            if ai1.opponent_info["username"] == ai2.username and ai2.opponent_info["username"] == ai1.username:
                print(f"✓ Les deux joueurs se sont trouvés mutuellement!")
            else:
                print(f"⚠️  Les joueurs ont été matchés avec d'autres adversaires")
                print(f"   {ai1.username} vs {ai1.opponent_info['username']}")
                print(f"   {ai2.username} vs {ai2.opponent_info['username']}")
    else:
        print("❌ TEST ÉCHOUÉ")
        print(f"   {ai1.username}: {'✓ Match trouvé' if ai1.match_found else '❌ Aucun match'}")
        print(f"   {ai2.username}: {'✓ Match trouvé' if ai2.match_found else '❌ Aucun match'}")

    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    run_test()
