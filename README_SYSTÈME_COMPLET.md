# 🎮 KOF ULTIMATE ONLINE - SYSTÈME COMPLET

## 📋 Vue d'ensemble

**KOF Ultimate Online** est maintenant un système complet avec :
- ✅ Détection automatique des bugs Mugen
- ✅ Système multijoueur style Battle.net
- ✅ Matchmaking avec ELO
- ✅ Launcher unifié pour tout gérer
- ✅ Optimisation automatique des personnages

---

## 🚀 DÉMARRAGE RAPIDE

### Option 1 : Launcher Ultimate (RECOMMANDÉ)

Double-cliquez sur : **`LAUNCH_ULTIMATE.bat`**

Le Launcher Ultimate vous permet de :
- 🎮 Lancer le jeu en solo
- ⚔️ Jouer en ligne avec matchmaking
- 🔍 Détecter et corriger les bugs automatiquement
- 🖥️ Héberger un serveur Battle.net

### Option 2 : Lancement manuel

#### Jouer en Solo
```batch
KOF_Ultimate_Online.exe
```

#### Jouer en Ligne
1. Lancer le serveur :
   ```bash
   python BATTLENET_SERVER.py
   ```

2. Lancer le client :
   ```bash
   python BATTLENET_CLIENT.py
   ```

---

## 📦 COMPOSANTS DU SYSTÈME

### 1. 🔍 AUTO_BUG_DETECTOR.py

**Fonction :** Détecte automatiquement les bugs dans les personnages Mugen.

**Utilisation :**
```bash
python AUTO_BUG_DETECTOR.py
```

**Ce qu'il fait :**
- Scanne tous les personnages du dossier `chars/`
- Teste chaque personnage individuellement
- Détecte les bugs : fichiers manquants, chargement lent, complexité excessive
- Génère un rapport JSON : `bug_report.json`
- Crée un `select_optimal.def` avec uniquement les personnages stables

**Résultats :**
- Liste des personnages stables (recommandés)
- Liste des personnages problématiques (à éviter)
- Rapport détaillé des bugs trouvés

---

### 2. 🖥️ BATTLENET_SERVER.py

**Fonction :** Serveur de matchmaking style Battle.net pour jouer en ligne.

**Utilisation :**
```bash
python BATTLENET_SERVER.py
```

**Fonctionnalités :**
- ⚔️ **Matchmaking automatique** : Trouve des adversaires avec ELO proche
- 📊 **Système ELO** : Classement compétitif comme Battle.net
- 🏆 **Leaderboard** : Classement des meilleurs joueurs
- 👥 **Multi-joueurs** : Supporte plusieurs parties simultanées
- 📡 **WebSocket** : Communication temps réel

**Ports :**
- Serveur : `ws://localhost:8765`

**Protocole :**
Le serveur utilise des messages JSON via WebSocket :

```json
{
  "type": "auth",
  "username": "Player1",
  "elo": 1000
}
```

Types de messages :
- `auth` : Authentification
- `search_match` : Rechercher un adversaire
- `cancel_search` : Annuler la recherche
- `match_found` : Match trouvé (envoyé par le serveur)
- `match_result` : Rapporter le résultat
- `get_leaderboard` : Demander le classement

---

### 3. 💻 BATTLENET_CLIENT.py

**Fonction :** Client graphique pour se connecter au serveur et jouer en ligne.

**Utilisation :**
```bash
python BATTLENET_CLIENT.py
```

**Interface :**
- 📊 **Profil joueur** : ELO, victoires, défaites, win rate
- 🔍 **Recherche d'adversaire** : Matchmaking automatique
- 🏆 **Classement** : Voir les meilleurs joueurs
- 📈 **Stats serveur** : Joueurs en ligne, matchs en cours

**Workflow :**
1. Entrer votre pseudo
2. Se connecter au serveur
3. Cliquer sur "Rechercher un Adversaire"
4. Attendre le match (max 30 secondes)
5. Jouer la partie
6. Le système met à jour votre ELO automatiquement

---

### 4. 🎯 KOFUO_LAUNCHER_ULTIMATE.py

**Fonction :** Launcher principal qui centralise tous les systèmes.

**Utilisation :**
```bash
python KOFUO_LAUNCHER_ULTIMATE.py
```

**Ou via le fichier batch :**
```batch
LAUNCH_ULTIMATE.bat
```

**Fonctionnalités :**
- 🎮 Lancer le jeu en solo
- ⚔️ Lancer le client Battle.net
- 🖥️ Lancer le serveur Battle.net
- 🔍 Lancer le détecteur de bugs
- 📝 Optimiser le select.def
- 📊 Voir les rapports
- 🛑 Arrêter tous les services

**Interface :**
- Indicateurs de statut pour chaque service
- Journal d'activité en temps réel
- Boutons d'action rapide

---

## 🎮 COMMENT JOUER EN LIGNE

### Scénario 1 : Jouer avec des amis (LAN/Internet)

#### Sur l'ordinateur serveur :
1. Lancer `LAUNCH_ULTIMATE.bat`
2. Cliquer sur "🖥️ Lancer Serveur Battle.net"
3. Attendre "Serveur accessible sur ws://localhost:8765"
4. Noter votre adresse IP :
   ```bash
   ipconfig
   ```

#### Sur chaque ordinateur client :
1. Modifier `BATTLENET_CLIENT.py` ligne 265 :
   ```python
   self.client = BattleNetClient(server_url="ws://ADRESSE_IP_SERVEUR:8765")
   ```
2. Lancer `LAUNCH_ULTIMATE.bat`
3. Cliquer sur "⚔️ Jouer en Ligne (Battle.net)"
4. Entrer votre pseudo et se connecter
5. Cliquer sur "Rechercher un Adversaire"

### Scénario 2 : Jouer en local (même PC)

1. Lancer `LAUNCH_ULTIMATE.bat`
2. Cliquer sur "🖥️ Lancer Serveur Battle.net"
3. Cliquer sur "⚔️ Jouer en Ligne (Battle.net)"
4. (Répéter pour ouvrir plusieurs clients)

---

## 🔧 RÉSOLUTION DES BUGS MUGEN

### Problème : Le jeu crash au lancement d'un match

**Solution automatique :**
1. Lancer `LAUNCH_ULTIMATE.bat`
2. Cliquer sur "🔍 Détecter les Bugs"
3. Attendre la fin du scan (peut prendre 10-30 minutes)
4. Cliquer sur "📝 Optimiser Select.def"
5. Relancer le jeu

**Explication :**
Le détecteur teste chaque personnage et identifie :
- Personnages trop complexes (>20000 expressions)
- Fichiers manquants (.air, .sff, .snd)
- Temps de chargement excessifs (>5 secondes)

### Problème : Certains personnages causent des lags

**Solution manuelle :**
1. Ouvrir `bug_report.json`
2. Regarder la section `"problematic"`
3. Ouvrir `data/select.def`
4. Commenter les lignes des personnages problématiques avec `;`

**Exemple :**
```ini
; Personnages stables
Kyo
Iori
Terry

; Personnages problématiques (désactivés)
;Akiha Orochi
;Blood Rugal
```

---

## 📊 SYSTÈME ELO

Le système ELO fonctionne comme Battle.net :

- **ELO de départ :** 1000 points
- **Victoire contre adversaire plus fort :** +30-40 points
- **Victoire contre adversaire plus faible :** +10-15 points
- **Défaite contre adversaire plus fort :** -10-15 points
- **Défaite contre adversaire plus faible :** -30-40 points

### Classement par ELO

| ELO | Rang |
|-----|------|
| 0-999 | Bronze |
| 1000-1499 | Silver |
| 1500-1999 | Gold |
| 2000-2499 | Platinum |
| 2500+ | Diamond |

---

## 🛠️ CONFIGURATION AVANCÉE

### Modifier le port du serveur

Dans `BATTLENET_SERVER.py` ligne 289 :
```python
server = BattleNetServer(host="0.0.0.0", port=8765)
```

### Ajuster le matchmaking

Dans `BATTLENET_SERVER.py` ligne 238 :
```python
# Différence d'ELO maximale (actuellement 200)
if elo_diff <= 200:
```

Augmenter pour matcher plus rapidement, diminuer pour plus de précision.

### Personnaliser les couleurs du launcher

Dans `KOFUO_LAUNCHER_ULTIMATE.py` lignes 16-22 :
```python
class Colors:
    PRIMARY = "#00d4ff"
    SECONDARY = "#16213e"
    BACKGROUND = "#0a0e27"
    # etc.
```

---

## 📁 STRUCTURE DES FICHIERS

```
D:/KOF Ultimate Online/
│
├── KOF_Ultimate_Online.exe          # Jeu principal
├── LAUNCH_ULTIMATE.bat              # Launcher rapide
│
├── KOFUO_LAUNCHER_ULTIMATE.py       # Launcher principal
├── AUTO_BUG_DETECTOR.py             # Détecteur de bugs
├── BATTLENET_SERVER.py              # Serveur multijoueur
├── BATTLENET_CLIENT.py              # Client multijoueur
│
├── bug_report.json                  # Rapport des bugs (généré)
│
├── data/
│   ├── select.def                   # Liste des personnages
│   ├── select_optimal.def           # Liste optimisée (généré)
│   └── mugen.cfg                    # Configuration du jeu
│
├── chars/                           # Personnages
│   ├── kyo/
│   ├── iori/
│   └── ...
│
└── mugen.log                        # Log du jeu (généré)
```

---

## 🐛 PROBLÈMES CONNUS

### 1. "Module websockets not found"

**Solution :**
```bash
pip install websockets
```

### 2. "Permission denied" sur Windows

**Solution :**
- Exécuter en tant qu'administrateur
- Désactiver temporairement l'antivirus

### 3. Le serveur ne démarre pas (port déjà utilisé)

**Solution :**
```bash
# Trouver le processus utilisant le port 8765
netstat -ano | findstr 8765

# Tuer le processus (remplacer PID)
taskkill /PID <PID> /F
```

### 4. Le matchmaking ne trouve pas d'adversaires

**Causes possibles :**
- Pas assez de joueurs connectés (minimum 2)
- Différence d'ELO trop grande (>200 points)
- Serveur non démarré

**Solution :**
- Lancer plusieurs clients pour tester
- Vérifier que le serveur est en cours

---

## 📈 STATISTIQUES ET RAPPORTS

### bug_report.json

Contient :
```json
{
  "date": "2025-10-29T...",
  "tested": 150,
  "stable": ["Kyo", "Iori", ...],
  "problematic": ["Akiha Orochi", ...],
  "bugs": [
    {
      "char": "Asura",
      "type": "LOAD_FAILED",
      "message": "Fichier manquant"
    }
  ]
}
```

### mugen.log

Log détaillé du jeu :
- Chargement des personnages
- Temps de chargement
- Erreurs d'exécution

---

## 🎯 PROCHAINES AMÉLIORATIONS

- [ ] Support des parties classées vs parties normales
- [ ] Chat intégré pendant le matchmaking
- [ ] Replay des parties
- [ ] Statistiques détaillées par personnage
- [ ] Tournois automatiques
- [ ] Interface web pour le serveur
- [ ] Support du spectateur (observer les matchs)
- [ ] Anti-triche basique

---

## 💡 CONSEILS

### Pour les débutants
1. Commencez par tester le jeu en solo
2. Lancez le détecteur de bugs pour avoir un roster stable
3. Pratiquez avec les personnages recommandés
4. Jouez en ligne quand vous êtes prêt

### Pour les joueurs intermédiaires
1. Optimisez votre select.def avec le détecteur
2. Participez au classement ELO
3. Testez différents personnages en ligne

### Pour les joueurs avancés
1. Hébergez votre propre serveur
2. Personnalisez le système de matchmaking
3. Contribuez en rapportant les bugs

---

## 📞 SUPPORT

En cas de problème :

1. **Vérifier les logs** : `mugen.log`, journal du launcher
2. **Lire ce README** : La solution est souvent ici
3. **Réinstaller les dépendances** :
   ```bash
   pip install --upgrade websockets psutil
   ```
4. **Réinitialiser la configuration** :
   - Restaurer `select.def` depuis un backup
   - Supprimer `bug_report.json` et relancer le détecteur

---

## 📜 CRÉDITS

**Développement :**
- Système de détection de bugs automatique
- Serveur Battle.net et matchmaking ELO
- Interface graphique du launcher

**Technologies :**
- Python 3.8+
- Tkinter (GUI)
- WebSockets (Multijoueur temps réel)
- Asyncio (Serveur asynchrone)
- Mugen/Ikemen GO (Moteur de jeu)

---

## ⚖️ LICENSE

Ce projet est un outil pour améliorer l'expérience KOF Ultimate Online.
Le moteur de jeu (Mugen/Ikemen GO) et les personnages restent la propriété de leurs créateurs respectifs.

---

**Dernière mise à jour :** 2025-10-29
**Version du système :** 1.0 Ultimate Edition

🎮 **Amusez-vous bien et que le meilleur gagne !** ⚔️
