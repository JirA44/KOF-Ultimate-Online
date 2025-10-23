# 🤖 SYSTÈME IA MULTI-MODES AUTONOME

## Vue d'ensemble

Le système IA Multi-Modes permet à des joueurs IA virtuels de jouer **automatiquement** dans **tous les modes de jeu** de KOF Ultimate Online, **sans vous déranger** !

---

## 🎮 Modes de jeu pris en charge

Le système supporte **7 modes de jeu différents** :

| Mode | Description | Durée moyenne |
|------|-------------|---------------|
| **Arcade** | Combat contre l'IA en progression | 5 minutes |
| **Versus** | Combat 1v1 rapide | 3 minutes |
| **Team** | Combat d'équipe 3v3 | 7 minutes |
| **Survival** | Survie contre vagues d'ennemis | 10 minutes |
| **Time Attack** | Vitesse de complétion | 4 minutes |
| **Training** | Mode entraînement libre | 5 minutes |
| **Team Versus** | Combat d'équipe versus | 6 minutes |

---

## 🚀 Lancement rapide

### Option 1 : Une seule IA
```batch
LAUNCH_AI_MULTI_MODES.bat
```
Lance **1 IA** qui joue automatiquement dans tous les modes en rotation.

### Option 2 : Plusieurs IA simultanées
```batch
LAUNCH_MULTIPLE_AI_PLAYERS.bat
```
Vous pouvez lancer **jusqu'à 5 IA** qui jouent **en même temps** dans différents modes !

---

## 🎯 Fonctionnalités

### Rotation automatique des modes
- ✅ L'IA change de mode automatiquement après chaque match
- ✅ Équilibre entre tous les modes de jeu
- ✅ Diversité maximale

### Personnalités d'IA
Chaque IA peut avoir une personnalité différente :

**🔴 Aggressive**
- Attaque constante
- Mouvements vers l'avant
- Combos agressifs

**🔵 Defensive**
- Garde fréquente
- Recul et esquive
- Contre-attaques

**🟢 Balanced**
- Mélange attaque/défense
- Stratégie équilibrée
- Adaptabilité

### Sélection intelligente
- ✅ Personnages aléatoires
- ✅ Stages aléatoires
- ✅ Teams pour modes équipe (3 personnages)

### Actions de combat réalistes
- ✅ Plus de 10 types d'actions différentes
- ✅ Combos spéciaux
- ✅ Mouvements spéciaux
- ✅ Pauses réalistes
- ✅ 120-240 actions par match

---

## 📊 Statistiques et logs

### Logs automatiques
Tous les événements sont enregistrés dans :
```
D:\KOF Ultimate Online\logs\ai_multi_mode.log
```

Format :
```
[HH:MM:SS] [P1] Mode sélectionné: ARCADE
[HH:MM:SS] [P1] Navigation vers arcade...
[HH:MM:SS] [P1] Sélection de 1 personnage(s)...
[HH:MM:SS] [P1] Début du match en mode arcade
[HH:MM:SS] [P1] Match terminé - 187 actions effectuées
```

### Screenshots automatiques
Des screenshots sont pris automatiquement à des moments clés :
```
D:\KOF Ultimate Online\ai_screenshots_p1\
D:\KOF Ultimate Online\ai_screenshots_p2\
...
```

Types de screenshots :
- `game_start` : Démarrage du jeu
- `main_menu` : Menu principal
- `[mode]_selected` : Mode sélectionné
- `characters_selected` : Personnages choisis
- `stage_selected` : Stage choisi
- `match_start` : Début du match
- `combat_XXX` : Pendant le match (toutes les 30s)
- `match_end` : Fin du match

### Statistiques JSON
Les stats sont sauvegardées par joueur :
```json
{
  "matches_played": 47,
  "modes_played": {
    "arcade": 8,
    "versus": 7,
    "team": 6,
    "survival": 9,
    "time_attack": 8,
    "training": 5,
    "team_versus": 4
  },
  "session_start": "2025-10-23T15:30:00",
  "player_id": 1
}
```

Emplacement :
```
D:\KOF Ultimate Online\ai_logs\stats_player_1.json
D:\KOF Ultimate Online\ai_logs\stats_player_2.json
...
```

---

## ⚙️ Configuration avancée

### Modifier le nombre de matches
Éditez `AI_MULTI_MODE_SYSTEM.py` ligne 402 :
```python
num_matches = 10  # Changez cette valeur
```

### Modifier la durée des matches
Ligne 354 :
```python
match_duration = random.randint(120, 240)  # Min-Max en secondes
```

### Forcer une personnalité
Ligne 401 :
```python
personality = "aggressive"  # ou "defensive" ou "balanced"
```

### Désactiver la rotation des modes
Ligne 416 :
```python
mode_rotation=False
```

---

## 🎬 Workflow complet

1. **Lancement**
   - L'IA lance le jeu automatiquement
   - Screenshot du démarrage

2. **Sélection du mode**
   - Choix aléatoire ou en rotation
   - Navigation dans les menus
   - Screenshot du menu

3. **Sélection des personnages**
   - 1 personnage pour modes solo
   - 3 personnages pour modes équipe
   - Mouvements aléatoires dans la grille
   - Screenshot de la sélection

4. **Sélection du stage**
   - Choix aléatoire
   - Screenshot du stage

5. **Combat**
   - Actions de combat pendant 2-4 minutes
   - Screenshots périodiques (toutes les 30s)
   - Statistiques en temps réel

6. **Post-match**
   - Passage des écrans de résultats
   - 30% de chance de retour au menu
   - 70% de chance de continuer dans le mode

7. **Répétition**
   - Rotation vers un autre mode
   - Pause de 3-8 secondes
   - Recommence au point 2

---

## 🛠️ Dépannage

### L'IA ne trouve pas le jeu
- Vérifiez que `KOF_Ultimate_Online.exe` existe dans `D:\KOF Ultimate Online\`
- Modifiez le chemin ligne 397 si nécessaire

### L'IA semble bloquée
- Ctrl+C pour arrêter
- Vérifiez les logs dans `logs\ai_multi_mode.log`
- Regardez les screenshots pour voir où ça bloque

### Plusieurs IA se marchent dessus
- C'est normal ! Elles jouent indépendamment
- Chaque IA a son propre dossier de screenshots
- Les logs sont partagés mais identifiés par `[P1]`, `[P2]`, etc.

### Arrêter toutes les IA
```batch
taskkill /F /IM python.exe /FI "WINDOWTITLE eq IA Multi-Modes*"
```

---

## 📈 Utilisation recommandée

### Test d'endurance
```batch
LAUNCH_AI_MULTI_MODES.bat
```
Laissez tourner pendant des heures pour tester la stabilité !

### Farming / Déblocages
Certains jeux ont des récompenses basées sur le nombre de matches.
Les IA peuvent farmer automatiquement !

### Génération de replays
Les screenshots permettent de créer des timelapses ou des rapports visuels.

### Stress test
```batch
LAUNCH_MULTIPLE_AI_PLAYERS.bat
```
Lancez 5 IA en même temps pour tester les performances système !

---

## 🎯 Exemples d'utilisation

### Session courte (30 minutes)
```python
num_matches = 3  # Environ 10 minutes par match
```

### Session longue (toute la nuit)
```python
num_matches = 50  # ~8 heures de jeu continu
```

### Mode farming spécifique (ex: Arcade uniquement)
Éditez ligne 147-160 pour forcer un mode :
```python
def choose_mode(self):
    self.current_mode = GameMode.ARCADE  # Force Arcade
    return GameMode.ARCADE
```

---

## 🏆 Avantages

- ✅ **Zéro intervention** : Lance et oublie !
- ✅ **Multi-modes** : Explore tout le contenu
- ✅ **Logs complets** : Trace complète de l'activité
- ✅ **Screenshots** : Documentation visuelle
- ✅ **Statistiques** : Données JSON structurées
- ✅ **Personnalités** : IA variées et réalistes
- ✅ **Multi-instance** : Plusieurs IA en parallèle
- ✅ **Configurable** : Tous les paramètres modifiables

---

## 📝 Notes techniques

### Touches utilisées
- **Navigation** : `up`, `down`, `left`, `right`, `return`, `esc`
- **Combat** : `a`, `s`, `d`, `w`, `space`, `q`, `e`, `r`, `f`

### Compatibilité
- ✅ Windows (testé)
- ⚠️ Linux/Mac : Adapter les touches et chemins

### Dépendances Python
```bash
pip install pyautogui
```

### Performance
- CPU : ~5% par IA
- RAM : ~50MB par IA
- Disque : ~1MB de logs par heure

---

## 🎮 C'est parti !

Lancez simplement :
```batch
LAUNCH_AI_MULTI_MODES.bat
```

Et laissez les IA jouer pour vous ! 🚀

**Bon jeu (automatique) !** 🎮🤖
