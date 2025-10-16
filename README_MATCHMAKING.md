# KOF Ultimate Online - Système de Matchmaking

## Vue d'ensemble

Système complet de matchmaking en ligne avec:
- **Serveur de matchmaking** avec système MMR (MatchMaking Rating)
- **Launcher avec profils joueurs** (style Warcraft 3)
- **Menu multijoueur** avec recherche de parties
- **Test automatisé** avec 2 IA qui se testent mutuellement

## Architecture du Système

```
┌─────────────────────────────────────────────────────────────┐
│                  KOF Ultimate Online                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐         ┌──────────────────┐             │
│  │   Launcher   │────────▶│  Profile System  │             │
│  │  (GUI Tkinter)│         │   (JSON DB)      │             │
│  └──────┬───────┘         └──────────────────┘             │
│         │                                                    │
│         │ Ouvre                                              │
│         ▼                                                    │
│  ┌──────────────┐                                           │
│  │Multiplayer   │                                           │
│  │   Menu       │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         │ Se connecte via                                   │
│         ▼                                                    │
│  ┌──────────────┐         ┌──────────────────┐             │
│  │  Matchmaking │◀───────▶│  Matchmaking     │             │
│  │    Client    │  Socket │     Server       │             │
│  └──────────────┘         └──────┬───────────┘             │
│                                   │                          │
│                                   │ MMR Algorithm            │
│                                   │ Queue Management         │
│                                   │ Match Creation           │
│                                   │                          │
└───────────────────────────────────┼──────────────────────────┘
                                    │
                              Autres joueurs
```

## Fichiers Principaux

### 1. Système de Profils
- **`player_profile_system.py`** - Gestion des profils avec stats (ELO, niveau, historique)
- **`launcher_with_profiles.py`** - Interface launcher avec sélection de profils

### 2. Système de Matchmaking
- **`matchmaking_server.py`** - Serveur TCP de matchmaking avec MMR
- **`matchmaking_client.py`** - Client de connexion au serveur
- **`online_multiplayer_menu.py`** - Menu multijoueur (UI Tkinter)

### 3. Scripts de Test et Lancement
- **`auto_matchmaking_test.py`** - Test automatique avec 2 IA
- **`START_MATCHMAKING_SYSTEM.bat`** - Lance serveur + launcher automatiquement

## Démarrage Rapide

### Option 1: Démarrage Automatique (Recommandé)

Double-cliquez sur:
```
START_MATCHMAKING_SYSTEM.bat
```

Cela va:
1. Lancer le serveur de matchmaking
2. Lancer le launcher avec système de profils

### Option 2: Démarrage Manuel

**Terminal 1 - Serveur:**
```bash
cd "D:\KOF Ultimate Online"
python matchmaking_server.py
```

**Terminal 2 - Launcher:**
```bash
cd "D:\KOF Ultimate Online"
python launcher_with_profiles.py
```

## Utilisation

### 1. Créer un Profil

1. Lancez le launcher
2. Cliquez sur "Nouveau"
3. Entrez:
   - Nom d'utilisateur
   - Mot de passe
   - Code PIN (4 chiffres)

### 2. Se Connecter

1. Sélectionnez votre profil dans la liste
2. Vos statistiques s'affichent à droite
3. Les boutons "JOUER" et "MULTIJOUEUR" s'activent

### 3. Rechercher un Match

1. Cliquez sur "MULTIJOUEUR"
2. Vérifiez que vous êtes connecté au serveur (✓ Connecté au serveur)
3. Choisissez un mode:
   - **Ranked (Classé)** - Matchmaking basé sur le MMR
   - **Quick Match (Rapide)** - Match rapide sans restriction MMR
   - **Custom Lobby (Perso)** - Lobbies personnalisés (à venir)
4. Cliquez sur "RECHERCHER UNE PARTIE"
5. Attendez qu'un adversaire soit trouvé
6. Acceptez le match quand il est trouvé

## Système MMR (MatchMaking Rating)

### Comment ça marche?

Le serveur utilise un système de matchmaking adaptatif:

1. **Mode Classé (Ranked)**:
   - Les joueurs sont matchés selon leur MMR
   - Différence MMR acceptée: 50 points de base
   - Augmente de 5 points par seconde d'attente
   - Exemple: Après 10s d'attente, différence max = 100 points

2. **Mode Rapide (Quick)**:
   - Pas de restriction MMR
   - Match les 2 premiers joueurs en file d'attente

3. **Calcul du MMR**:
   - MMR de départ: 1000 points
   - Victoire: +20 points
   - Défaite: -10 points
   - XP par victoire: +100
   - XP par défaite: +25
   - Niveau = 1 + (XP total / 1000)

## Test Automatique

Pour tester le système avec 2 IA automatisées:

```bash
# Terminal 1 - Lancer le serveur
python matchmaking_server.py

# Terminal 2 - Lancer le test
python auto_matchmaking_test.py
```

Le test va:
1. Créer 2 profils de test (AI_TestPlayer_1 et AI_TestPlayer_2)
2. Les connecter au serveur
3. Les faire rechercher un match simultanément
4. Afficher le résultat du matchmaking

## Architecture Technique

### Serveur de Matchmaking

**Port**: 9999 (TCP)
**Protocole**: JSON sur socket TCP

**Fonctionnalités**:
- Gestion de connexions multiples (threading)
- File d'attente par mode de jeu
- Algorithme de matchmaking MMR adaptatif
- Notification en temps réel des matchs

**Messages supportés**:
```json
// Connexion
{
  "action": "connect",
  "username": "Player1",
  "player_data": {...}
}

// Recherche de match
{
  "action": "search_match",
  "mode": "ranked"
}

// Annulation
{
  "action": "cancel_search"
}

// Déconnexion
{
  "action": "disconnect",
  "username": "Player1"
}
```

**Notifications serveur**:
```json
// Match trouvé
{
  "event": "match_found",
  "match_id": "match_123",
  "mode": "ranked",
  "opponent": {
    "username": "Player2",
    "mmr": 1050,
    "level": 5,
    "wins": 15,
    "losses": 10
  }
}
```

### Client de Matchmaking

**Classe**: `MatchmakingClient`

**Méthodes**:
- `connect(username, player_data)` - Se connecte au serveur
- `search_match(mode)` - Lance une recherche
- `cancel_search()` - Annule la recherche
- `disconnect()` - Se déconnecte

**Callbacks**:
- `on_match_found(match_data)` - Match trouvé
- `on_connected(response)` - Connexion établie
- `on_disconnected()` - Déconnexion
- `on_error(error)` - Erreur

## Base de Données des Profils

**Fichier**: `profiles/profiles_database.json`

**Structure**:
```json
{
  "profiles": {
    "Player1": {
      "username": "Player1",
      "password_hash": "sha256...",
      "pin_hash": "sha256...",
      "created_at": "2025-10-16T...",
      "last_login": "2025-10-16T...",
      "stats": {
        "total_matches": 25,
        "wins": 15,
        "losses": 10,
        "draws": 0,
        "win_rate": 60.0,
        "total_playtime_minutes": 125,
        "favorite_character": "Kyo",
        "level": 3,
        "experience": 1750,
        "ranking_points": 1100
      },
      "character_stats": {
        "Kyo": {
          "matches": 15,
          "wins": 10,
          "losses": 5
        }
      },
      "match_history": [
        {
          "date": "2025-10-16T...",
          "result": "win",
          "character": "Kyo",
          "opponent": "Player2",
          "duration": 5
        }
      ]
    }
  },
  "last_profile": "Player1",
  "version": "1.0"
}
```

## Sécurité

### Authentification
- Mot de passe hashé avec SHA256
- Code PIN à 4 chiffres hashé avec SHA256
- Double authentification (password + PIN) pour lancer le jeu

### Communication
- Socket TCP non chiffré (localhost par défaut)
- Pour usage en réseau: ajouter TLS/SSL

## Configuration

### Changer le Port du Serveur

**`matchmaking_server.py`**:
```python
server = MatchmakingServer(host='0.0.0.0', port=9999)
```

**`matchmaking_client.py`**:
```python
client = MatchmakingClient(server_host='127.0.0.1', server_port=9999)
```

### Changer le Chemin des Profils

**`player_profile_system.py`**:
```python
def __init__(self, base_path="D:/KOF Ultimate Online"):
```

### Paramètres MMR

**`matchmaking_server.py`** - Méthode `_process_ranked_queue()`:
```python
# Seuil de MMR de base
mmr_threshold = 50 + (avg_wait * 5)
```

- `50` = Différence MMR de base
- `5` = Augmentation par seconde d'attente

## Troubleshooting

### Problème: "Non connecté au serveur"

**Solution**:
1. Vérifiez que le serveur est lancé: `python matchmaking_server.py`
2. Vérifiez le port 9999 n'est pas utilisé
3. Vérifiez le firewall Windows

### Problème: "Impossible de créer le profil"

**Causes possibles**:
- Nom d'utilisateur déjà existant
- PIN pas exactement 4 chiffres
- Problème de permissions d'écriture

**Solution**:
- Choisissez un nom différent
- Vérifiez que le PIN est 4 chiffres
- Vérifiez les permissions du dossier `profiles/`

### Problème: Pas de match trouvé

**Causes**:
- Aucun autre joueur en recherche
- Différence MMR trop grande (mode ranked)

**Solution**:
- Utilisez le mode "Quick Match"
- Lancez plusieurs instances pour tester
- Utilisez le script de test: `python auto_matchmaking_test.py`

## Extensions Futures

### À Implémenter

1. **Chat in-game**
   - Communication entre joueurs
   - Chat de lobby

2. **Replay System**
   - Enregistrement des matchs
   - Partage de replays

3. **Tournois**
   - Système de brackets
   - Tournois automatiques

4. **Classement Global**
   - Leaderboard en ligne
   - Saisons ranked

5. **Anti-Cheat**
   - Détection de triche
   - Système de reports

6. **Spectateur Mode**
   - Observer les matchs en cours
   - Streaming de parties

## Support

Pour toute question ou problème:
- Vérifiez ce README
- Consultez les logs du serveur
- Lancez le test automatique pour diagnostiquer

## Crédits

Développé pour KOF Ultimate Online
Système inspiré de Warcraft 3 et Battle.net
