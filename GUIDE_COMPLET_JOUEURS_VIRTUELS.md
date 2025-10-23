# 🎮 Guide Complet - Joueurs Virtuels Autonomes KOF

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Installation et Configuration](#installation-et-configuration)
3. [Démarrage Rapide](#démarrage-rapide)
4. [Fonctionnement Détaillé](#fonctionnement-détaillé)
5. [Dashboard de Monitoring](#dashboard-de-monitoring)
6. [Personnalisation](#personnalisation)
7. [Cas d'Usage](#cas-dusage)
8. [Dépannage](#dépannage)

---

## 🌟 Vue d'ensemble

### Qu'est-ce que c'est ?

Le **Système de Joueurs Virtuels** est une solution complète qui permet de créer des joueurs IA autonomes qui :

- 🎯 Naviguent automatiquement dans tous les menus du jeu
- 🎲 Sélectionnent des personnages et des stages aléatoirement
- 🕹️ Jouent à tous les modes de jeu (Arcade, Versus, Team, Survival, etc.)
- 🔄 Fonctionnent en continu pendant des heures
- 📊 Enregistrent leurs statistiques et leur progression
- 🤖 Ont des personnalités uniques (Aggressive, Defensive, Balanced)

### Architecture du Système

```
┌─────────────────────────────────────────────────┐
│         SYSTÈME JOUEURS VIRTUELS                │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐    ┌──────────────┐          │
│  │  Joueur 1    │    │  Joueur 2    │          │
│  │  Aggressive  │    │  Defensive   │ ...      │
│  └──────┬───────┘    └──────┬───────┘          │
│         │                   │                   │
│         └───────┬───────────┘                   │
│                 │                               │
│         ┌───────▼────────┐                      │
│         │ Orchestrateur  │                      │
│         └───────┬────────┘                      │
│                 │                               │
│         ┌───────▼────────┐                      │
│         │  KOF Ultimate  │                      │
│         │     Online     │                      │
│         └────────────────┘                      │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │     Dashboard de Monitoring (Web)        │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## 🔧 Installation et Configuration

### Prérequis

- ✅ Windows 10/11
- ✅ Python 3.8+ installé
- ✅ KOF Ultimate Online installé
- ✅ Bibliothèques Python nécessaires

### Installation des Dépendances

```bash
pip install pyautogui
pip install pillow
```

### Fichiers Requis

Tous ces fichiers sont déjà dans `D:\KOF Ultimate Online` :

```
KOF Ultimate Online/
├── VIRTUAL_PLAYERS_CONTINUOUS.py      # Script principal
├── VIRTUAL_PLAYERS_DASHBOARD.html     # Dashboard web
├── LAUNCH_VIRTUAL_PLAYERS.bat         # Launcher Windows
├── TEST_VIRTUAL_PLAYER_QUICK.py       # Script de test
├── README_VIRTUAL_PLAYERS.md          # Documentation
└── GUIDE_COMPLET_JOUEURS_VIRTUELS.md  # Ce guide
```

---

## 🚀 Démarrage Rapide

### Méthode 1 : Launcher Windows (Recommandé)

1. **Lancer le jeu** `KOF_Ultimate_Online.exe`
2. **Attendre le menu principal**
3. **Double-cliquer** sur `LAUNCH_VIRTUAL_PLAYERS.bat`
4. **Choisir l'option** dans le menu :
   - Option [1] : 3 joueurs, 2h de session
   - Option [2] : 5 joueurs, 2h de session
   - Option [3] : 10 joueurs, session infinie
   - Option [4] : Dashboard seulement

5. **Le système démarre automatiquement !**

### Méthode 2 : Ligne de Commande

```bash
# Terminal 1 : Lancer le système
cd "D:\KOF Ultimate Online"
python VIRTUAL_PLAYERS_CONTINUOUS.py

# Terminal 2 : Ouvrir le dashboard
start VIRTUAL_PLAYERS_DASHBOARD.html
```

### Test Rapide (2 minutes)

Pour tester que tout fonctionne :

```bash
python TEST_VIRTUAL_PLAYER_QUICK.py
```

---

## 🎯 Fonctionnement Détaillé

### Cycle de Vie d'un Joueur Virtuel

```
1. INITIALISATION
   └─> Création du profil
       ├─> Nom aléatoire généré
       ├─> Personnalité assignée
       └─> Statistiques à zéro

2. NAVIGATION MENU
   └─> Choix du mode de jeu
       ├─> Arcade
       ├─> Versus
       ├─> Team Battle
       ├─> Survival
       ├─> Time Attack
       └─> Training

3. SÉLECTION PERSONNAGES
   └─> Mouvements aléatoires dans la grille
       ├─> Directions : Up, Down, Left, Right
       ├─> Nombre de mouvements : 3-12
       └─> Confirmation : Touche A/J/Return

4. SÉLECTION STAGE
   └─> Mouvements gauche/droite aléatoires
       └─> Confirmation

5. COMBAT
   └─> Boucle d'actions pendant 90-180 secondes
       ├─> Actions selon personnalité
       ├─> Pauses aléatoires pour réalisme
       └─> Screenshots périodiques

6. POST-MATCH
   └─> Passer les écrans de résultats
       ├─> 70% : Continuer dans le mode
       └─> 30% : Retour au menu principal

7. BOUCLE
   └─> Retour à l'étape 2
```

### Personnalités et Comportements

#### 🔥 **Aggressive (Agressif)**

```python
Actions prioritaires:
- Avancer (Right)
- Punches rapides (A, S, D)
- Kicks rapides (J, K)
- Spéciaux (Down+Right+A)
- Peu de blocage
```

**Style de jeu** : Pression constante, rushdown

#### 🛡️ **Defensive (Défensif)**

```python
Actions prioritaires:
- Reculer (Left)
- Bloquer (Down)
- Backdash (Left, Left)
- Contre-attaques (S)
- Attente d'ouverture
```

**Style de jeu** : Patient, punitif

#### ⚖️ **Balanced (Équilibré)**

```python
Actions variées:
- Mouvements (Left, Right)
- Toutes les attaques (A, S, D, J, K, L)
- Jump (Up)
- Spéciaux occasionnels
- Mix de tout
```

**Style de jeu** : Polyvalent, adaptatif

---

## 📊 Dashboard de Monitoring

### Accès au Dashboard

Le dashboard s'ouvre automatiquement ou manuellement :

```bash
start VIRTUAL_PLAYERS_DASHBOARD.html
```

### Sections du Dashboard

#### 1. **Statistiques Globales** (En haut)

```
┌────────────────┬────────────────┬────────────────┬────────────────┐
│ Joueurs Actifs │ Matches Totaux │ Actions/Minute │  Temps Total   │
│       3        │       42       │      850       │      2h        │
└────────────────┴────────────────┴────────────────┴────────────────┘
```

#### 2. **Cartes de Joueurs** (Centre)

Chaque joueur a une carte avec :

- **Nom** : Ex. "DarkWarrior1"
- **Statut** : 🎮 En jeu / ⏸️ Pause
- **Personnalité** : Aggressive/Defensive/Balanced
- **Mode actuel** : Arcade, Versus, etc.
- **Statistiques** :
  - Matches joués
  - Actions effectuées
  - Win Rate (%)
- **Activité récente** : Log des 10 dernières actions

#### 3. **Contrôles** (Bas)

- **▶️ Démarrer Tous** : Active tous les joueurs
- **⏹️ Arrêter Tous** : Met en pause
- **🔄 Actualiser** : Rafraîchit les données

### Mise à Jour en Temps Réel

Le dashboard se met à jour automatiquement :
- **Toutes les 1 seconde** : Affichage
- **Toutes les 2 secondes** : Simulation d'activité

---

## ⚙️ Personnalisation

### Changer le Nombre de Joueurs

Éditer `VIRTUAL_PLAYERS_CONTINUOUS.py` :

```python
# Ligne 640 environ dans main()
num_players = 5  # Changez ce nombre
```

### Modifier la Durée de Session

```python
# Ligne 641 environ
session_duration = 240  # en minutes (4 heures)
```

### Forcer une Personnalité Spécifique

Dans `VirtualPlayersOrchestrator.create_players()` :

```python
# Au lieu de :
personality = personalities[i % len(personalities)]

# Forcer une personnalité :
personality = "aggressive"  # Tous les joueurs agressifs
```

### Ajouter des Modes de Jeu

Dans `GameModes` :

```python
class GameModes:
    ARCADE = "Arcade"
    VERSUS = "Versus"
    # ... autres modes
    BOSS_RUSH = "Boss Rush"  # Nouveau mode

    ALL = [ARCADE, VERSUS, ..., BOSS_RUSH]
```

### Modifier la Durée des Matches

```python
# Dans play_continuous_session(), ligne ~353
match_duration = random.randint(60, 120)  # 1-2 min au lieu de 90-180s
```

### Changer la Fréquence des Screenshots

```python
# Dans play_match(), ligne ~275
screenshot_interval = 60  # Toutes les 60 secondes au lieu de 30
```

---

## 📈 Statistiques et Logs

### Structure des Dossiers

```
KOF Ultimate Online/
├── virtual_player_1_logs/
│   ├── player_1.log          # Logs détaillés
│   └── stats_1.json          # Statistiques JSON
├── virtual_player_1_screenshots/
│   ├── 20250123_143052_Arcade_match_start.png
│   ├── 20250123_143125_Arcade_combat_50.png
│   └── ...
├── virtual_player_2_logs/
│   └── ...
└── virtual_players_continuous.log  # Log global
```

### Format des Logs

**player_X.log** :
```
2025-01-23 14:30:52 - INFO - Navigation vers Versus...
2025-01-23 14:30:54 - INFO - Mode Versus sélectionné
2025-01-23 14:30:56 - INFO - Sélection de 1 personnage(s)...
2025-01-23 14:30:58 - INFO -   ✓ Personnage 1/1 sélectionné
2025-01-23 14:31:00 - INFO - Stage sélectionné: Stage_5
2025-01-23 14:31:02 - INFO - 🎮 Début du match (120s)
2025-01-23 14:33:05 - INFO - ✓ Match terminé - 456 actions en 123.4s
```

### Format des Statistiques

**stats_X.json** :
```json
{
  "player_id": 1,
  "name": "DarkWarrior1",
  "matches_played": 42,
  "modes_played": {
    "Arcade": 15,
    "Versus": 12,
    "Team Battle": 8,
    "Survival": 5,
    "Time Attack": 2
  },
  "characters_used": {
    "Character_1": 5,
    "Character_7": 8,
    "Character_12": 4,
    ...
  },
  "stages_played": {
    "Stage_1": 3,
    "Stage_5": 7,
    ...
  },
  "total_playtime": 5040,
  "actions_performed": 15420,
  "session_start": "2025-01-23T14:30:00"
}
```

### Analyser les Statistiques

**Python** :
```python
import json

with open('virtual_player_1_logs/stats_1.json', 'r') as f:
    stats = json.load(f)

print(f"Joueur: {stats['name']}")
print(f"Matches: {stats['matches_played']}")
print(f"Temps de jeu: {stats['total_playtime']/3600:.1f}h")
```

**PowerShell** :
```powershell
$stats = Get-Content "virtual_player_1_logs/stats_1.json" | ConvertFrom-Json
Write-Host "Matches: $($stats.matches_played)"
```

---

## 🎮 Cas d'Usage

### 1. **Test de Stabilité**

**Objectif** : Tester si le jeu crash après plusieurs heures

**Configuration** :
```python
num_players = 1
session_duration = 1440  # 24 heures
```

**Résultat** : Logs automatiques des crashs

### 2. **Génération de Données**

**Objectif** : Collecter des stats de gameplay

**Configuration** :
```python
num_players = 5
session_duration = 480  # 8 heures
```

**Résultat** : Milliers de screenshots et stats JSON

### 3. **Stress Test Multijoueur**

**Objectif** : Tester performances avec beaucoup de joueurs

**Configuration** :
```python
num_players = 10
session_duration = 120  # 2 heures
```

**Résultat** : Métriques de performance CPU/RAM

### 4. **Démonstration Auto**

**Objectif** : Montrer le jeu lors d'un événement

**Configuration** :
```python
num_players = 2
personalities = ["aggressive", "aggressive"]  # Combat spectaculaire
```

**Résultat** : Gameplay dynamique continu

### 5. **Test de Tous les Modes**

**Objectif** : S'assurer que tous les modes fonctionnent

**Configuration** :
```python
# Activer mode_rotation dans l'orchestrateur
mode_rotation = True
```

**Résultat** : Tous les modes testés équitablement

---

## 🔧 Dépannage

### Problème : Les joueurs ne bougent pas

**Causes possibles** :
- Jeu pas lancé
- Jeu en fullscreen (empêche PyAutoGUI)
- Mauvais mapping clavier

**Solutions** :
1. Lancer le jeu en mode fenêtré
2. Vérifier que le jeu utilise les touches par défaut (WASD, JKL, etc.)
3. Tester avec `TEST_VIRTUAL_PLAYER_QUICK.py`

### Problème : Script plante avec une erreur

**Erreur** : `ModuleNotFoundError: No module named 'pyautogui'`

**Solution** :
```bash
pip install pyautogui pillow
```

**Erreur** : `PermissionError: [Errno 13] Permission denied`

**Solution** : Lancer en administrateur ou vérifier les droits sur le dossier

### Problème : Ralentissements / Lag

**Causes** :
- Trop de joueurs simultanés
- PC pas assez puissant
- Trop de screenshots

**Solutions** :
1. Réduire le nombre de joueurs
2. Augmenter `screenshot_interval`
3. Désactiver les screenshots :
   ```python
   def take_screenshot(self, name=""):
       return None  # Désactivé
   ```

### Problème : Dashboard ne se met pas à jour

**Causes** :
- Dashboard fermé
- Navigateur bloque JavaScript

**Solutions** :
1. Recharger la page (F5)
2. Autoriser JavaScript
3. Utiliser Chrome/Firefox

### Problème : Fichiers de stats manquants

**Cause** : Erreur d'écriture

**Solution** :
1. Vérifier les permissions du dossier
2. Vérifier l'espace disque
3. Consulter `virtual_players_continuous.log`

---

## 📞 Support et Aide

### Logs à Consulter

En cas de problème, consulter dans cet ordre :

1. **virtual_players_continuous.log** : Log global du système
2. **virtual_player_X_logs/player_X.log** : Logs du joueur spécifique
3. **stats_X.json** : Statistiques si le problème est récent

### Commandes de Debug

**Afficher les logs en temps réel** :
```bash
tail -f virtual_players_continuous.log
```

**Windows** :
```powershell
Get-Content virtual_players_continuous.log -Wait
```

**Vérifier la syntaxe Python** :
```bash
python -m py_compile VIRTUAL_PLAYERS_CONTINUOUS.py
```

---

## 🚀 Optimisations Avancées

### Réduire l'Usage CPU

```python
# Augmenter les pauses
pyautogui.PAUSE = 0.1  # Au lieu de 0.05

# Dans perform_combat_action()
time.sleep(random.uniform(0.2, 0.5))  # Plus de pauses
```

### Réduire l'Usage Mémoire

```python
# Limiter les logs gardés
if len(self.profile['match_history']) > 20:  # Au lieu de 50
    self.profile['match_history'] = self.profile['match_history'][-20:]
```

### Accélérer le Système

```python
# Réduire les pauses
time.sleep(0.05)  # Au lieu de 0.1

# Supprimer les screenshots
def take_screenshot(self, name=""):
    return None
```

---

## 🎓 Exemples de Scripts Personnalisés

### Script : Joueur Entraînement Seul

```python
from VIRTUAL_PLAYERS_CONTINUOUS import VirtualPlayer

player = VirtualPlayer(1, "TrainingBot", "D:/KOF Ultimate Online", "balanced")

# Forcer le mode Training
player.navigate_to_mode_from_menu("Training")
player.select_characters(1)

# Jouer pendant 1 heure
player.play_match(3600)
```

### Script : Match Agressif vs Défensif

```python
from VIRTUAL_PLAYERS_CONTINUOUS import VirtualPlayersOrchestrator

orchestrator = VirtualPlayersOrchestrator("D:/KOF Ultimate Online", 2)

# Joueur 1 : Agressif
p1 = VirtualPlayer(1, "Attacker", "D:/KOF Ultimate Online", "aggressive")

# Joueur 2 : Défensif
p2 = VirtualPlayer(2, "Defender", "D:/KOF Ultimate Online", "defensive")

orchestrator.players = [p1, p2]
orchestrator.start_all_players(60)  # 1 heure
```

---

## 📚 Ressources Supplémentaires

### Fichiers de Référence

- `README_VIRTUAL_PLAYERS.md` : Vue d'ensemble courte
- `GUIDE_COMPLET_JOUEURS_VIRTUELS.md` : Ce guide détaillé
- Code source commenté dans `VIRTUAL_PLAYERS_CONTINUOUS.py`

### Documentation Python

- [PyAutoGUI](https://pyautogui.readthedocs.io/) : Contrôle GUI
- [Threading](https://docs.python.org/3/library/threading.html) : Multi-threading
- [JSON](https://docs.python.org/3/library/json.html) : Sérialisation

---

## 🎉 Conclusion

Vous avez maintenant un **système complet de joueurs virtuels autonomes** !

### Checklist de Démarrage

- [ ] Python installé
- [ ] Dépendances installées (`pip install pyautogui pillow`)
- [ ] Jeu lancé et au menu principal
- [ ] Test rapide réussi (`TEST_VIRTUAL_PLAYER_QUICK.py`)
- [ ] Launcher configuré (`LAUNCH_VIRTUAL_PLAYERS.bat`)
- [ ] Dashboard accessible

### Prochaines Étapes

1. **Tester** avec 1 joueur pendant 10 minutes
2. **Ajuster** les paramètres selon vos besoins
3. **Lancer** une session complète
4. **Analyser** les statistiques générées
5. **Optimiser** selon les résultats

---

**Créé avec Claude Code** 🤖
**Dernière mise à jour** : 2025-01-23

*Amusez-vous bien avec vos joueurs virtuels !* 🎮✨
