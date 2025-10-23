# 🎮 Système de Joueurs Virtuels en Continu

## Description

Ce système permet de lancer des **joueurs virtuels autonomes** qui jouent automatiquement au jeu en continu. Les joueurs virtuels :

- ✅ Naviguent dans les menus du jeu
- ✅ Sélectionnent des personnages aléatoirement
- ✅ Jouent tous les types de parties (Arcade, Versus, Team, Survival, etc.)
- ✅ S'améliorent avec différentes personnalités
- ✅ Fonctionnent en parallèle (plusieurs joueurs simultanés)
- ✅ Enregistrent leurs statistiques

## 📁 Fichiers du Système

### Scripts Principaux

1. **VIRTUAL_PLAYERS_CONTINUOUS.py**
   - Script Python principal
   - Crée et gère les joueurs virtuels
   - Orchestre les sessions de jeu

2. **VIRTUAL_PLAYERS_DASHBOARD.html**
   - Dashboard de monitoring en temps réel
   - Affiche l'activité de tous les joueurs
   - Statistiques globales

3. **LAUNCH_VIRTUAL_PLAYERS.bat**
   - Launcher Windows facile à utiliser
   - Menu interactif pour démarrer le système

## 🚀 Comment Utiliser

### Méthode Simple (Recommandée)

1. **Double-cliquer sur `LAUNCH_VIRTUAL_PLAYERS.bat`**
2. Choisir une option dans le menu
3. Le système se lance automatiquement !

### Méthode Manuelle

```bash
# Lancer 3 joueurs virtuels
python VIRTUAL_PLAYERS_CONTINUOUS.py
```

Le dashboard s'ouvre automatiquement dans votre navigateur.

## 🎯 Personnalités des Joueurs

Chaque joueur virtuel a une personnalité unique :

### 🔥 **Aggressive**
- Fonce sur l'adversaire
- Utilise beaucoup d'attaques
- Prend des risques

### 🛡️ **Defensive**
- Joue prudemment
- Privilégie le blocage
- Contre-attaque

### ⚖️ **Balanced**
- Équilibre attaque/défense
- Adaptatif
- Polyvalent

## 📊 Dashboard de Monitoring

Le dashboard affiche en temps réel :

- **Joueurs actifs** : Nombre de joueurs en train de jouer
- **Matches totaux** : Cumul de tous les matches
- **Actions/minute** : Intensité d'activité
- **Temps total de jeu** : Durée cumulée

### Cartes de Joueurs

Chaque joueur a sa carte avec :
- Nom et personnalité
- Statut (En jeu / Pause)
- Mode de jeu actuel
- Statistiques (matches, actions, win rate)
- Log d'activité récente

## 📈 Statistiques

Les stats sont sauvegardées dans :
```
virtual_player_X_logs/
├── player_X.log           # Logs détaillés
└── stats_X.json          # Statistiques JSON
```

### Format des Statistiques JSON

```json
{
  "player_id": 1,
  "name": "DarkWarrior1",
  "matches_played": 42,
  "modes_played": {
    "Arcade": 15,
    "Versus": 12,
    "Team Battle": 8,
    "Survival": 7
  },
  "characters_used": {
    "Character_1": 5,
    "Character_2": 8,
    ...
  },
  "total_playtime": 3600,
  "actions_performed": 15420
}
```

## ⚙️ Configuration

### Modifier le nombre de joueurs

Éditer `VIRTUAL_PLAYERS_CONTINUOUS.py` :

```python
# Ligne 640 environ
num_players = 3  # Changer ce nombre
```

### Modifier la durée de session

```python
# Ligne 641 environ
session_duration = 120  # en minutes
```

### Modifier les personnalités

Les personnalités sont assignées en rotation automatiquement, mais vous pouvez forcer :

```python
player = VirtualPlayer(
    player_id=i+1,
    name=name,
    game_dir=self.game_dir,
    personality="aggressive"  # ou "defensive", "balanced"
)
```

## 🎮 Modes de Jeu Supportés

- ✅ **Arcade** : Progression contre l'IA
- ✅ **Versus** : 1v1 classique
- ✅ **Team Battle** : Équipes de 3
- ✅ **Survival** : Combat continu
- ✅ **Time Attack** : Course contre la montre
- ✅ **Training** : Entraînement libre

## 🔧 Dépannage

### Les joueurs ne bougent pas ?

1. Vérifier que le jeu est bien lancé
2. Vérifier que le jeu est en fenêtre (pas fullscreen)
3. Vérifier les contrôles clavier dans le jeu

### Le script plante ?

1. Vérifier les logs : `virtual_player_X_logs/player_X.log`
2. Relancer le système
3. Réduire le nombre de joueurs

### Ralentissements ?

Le système peut être intensif. Recommandations :
- Pas plus de 3 joueurs simultanés sur PC moyen
- Jusqu'à 5-10 joueurs sur PC puissant
- Fermer les autres applications

## 📝 Notes Importantes

1. **Le jeu doit être lancé avant** de démarrer les joueurs virtuels
2. **Ne pas minimiser** le jeu pendant la session
3. **Les joueurs utilisent le clavier** - ne pas interférer manuellement
4. **Sauvegardes automatiques** des stats toutes les 5 minutes

## 🎯 Cas d'Usage

### Test de Longue Durée
Lancer 3 joueurs pour 24h pour tester la stabilité du jeu.

### Génération de Données
Collecter des statistiques de gameplay pour analyse.

### Stress Test
Lancer 10 joueurs pour tester les performances.

### Démonstration
Montrer le jeu en action automatiquement lors d'événements.

## 🆘 Support

Si vous rencontrez des problèmes :

1. Consulter les logs dans `virtual_player_X_logs/`
2. Vérifier `virtual_players_continuous.log`
3. Redémarrer le système

## 🔮 Améliorations Futures

- [ ] Support du mode Online/Netplay
- [ ] Machine Learning pour améliorer les stratégies
- [ ] API REST pour contrôle à distance
- [ ] Intégration avec le système de matchmaking
- [ ] Replay automatique des meilleurs matches

## 📄 Licence

Ce système fait partie de **KOF Ultimate Online**.

---

**Créé avec Claude Code** 🤖

*Amusez-vous bien avec vos joueurs virtuels !* 🎮
