# KOF Ultimate - AI Player System

## 🤖 Qu'est-ce que c'est?

Le **AI Player System** est un système d'intelligence artificielle autonome qui peut:

- ✅ **Jouer au jeu automatiquement** - L'IA contrôle les personnages et joue des matchs
- ✅ **Explorer tous les menus** - Navigation intelligente dans l'interface du jeu
- ✅ **Tester le mode multijoueur** - Simule des matchs IA vs IA
- ✅ **Apprendre et s'améliorer** - Système d'apprentissage basé sur les statistiques
- ✅ **Détecter les bugs** - Analyse visuelle pour trouver les problèmes
- ✅ **Générer des rapports** - Logs détaillés de toutes les activités

## 📋 Fonctionnalités principales

### 1. Vision par IA (Claude Vision)
- Capture et analyse l'écran du jeu en temps réel
- Identifie les éléments du menu, barres de vie, positions des personnages
- Détecte les anomalies graphiques et les bugs

### 2. Contrôleur de jeu intelligent
- Simule des pressions de touches réalistes
- Exécute des combos appris
- S'adapte à la situation de combat

### 3. Système d'apprentissage
- Sauvegarde les statistiques de jeu (victoires/défaites)
- Apprend de nouveaux combos
- Demande des suggestions d'amélioration à Claude AI

### 4. Détection de bugs
- Analyse chaque écran pour détecter les problèmes
- Sauvegarde des captures d'écran des bugs
- Génère des rapports JSON automatiques

## 🚀 Installation

### Étape 1: Installer les dépendances

```bash
cd "D:\KOF Ultimate"
pip install -r requirements_ai.txt
```

### Étape 2: Configurer l'API Anthropic

Créez un fichier `.env` dans le dossier du jeu:

```env
ANTHROPIC_API_KEY=votre_clé_api_ici
```

Ou définissez la variable d'environnement:

```bash
set ANTHROPIC_API_KEY=votre_clé_api
```

### Étape 3: Lancer le système

**Option A: Via le launcher**
1. Lancez `launcher.py`
2. Cliquez sur **🤖 AI PLAYER (Auto-Play & Test)**

**Option B: Direct**
```bash
python ai_player_system.py
```

## 🎮 Modes d'utilisation

### Mode 1: Auto-Exploration (30 min)
L'IA explore le jeu pendant 30 minutes:
- Joue plusieurs matchs
- Teste différents personnages
- Détecte les bugs
- S'améliore automatiquement

### Mode 2: Auto-Exploration (60 min)
Version longue pour tests approfondis

### Mode 3: Match unique
Joue un seul match pour test rapide

### Mode 4: Voir les statistiques
Affiche le profil et les stats d'apprentissage

### Mode 5: Détection de bugs uniquement
Analyse l'écran actuel sans jouer

## 📊 Fichiers générés

### `profiles/Claude_AI_Player.json`
Profil du joueur IA avec statistiques:
```json
{
  "games_played": 45,
  "wins": 28,
  "losses": 15,
  "draws": 2,
  "favorite_characters": ["Kyo", "Iori", "K'"],
  "learned_combos": ["punch_light-punch_light-punch_heavy", ...],
  "bugs_found": [...]
}
```

### `ai_player.log`
Log détaillé de toutes les actions:
```
2025-10-15 10:30:15 - INFO - Starting exploration session...
2025-10-15 10:30:20 - INFO - Navigating to: Versus
2025-10-15 10:30:25 - INFO - Starting AI vs AI match...
2025-10-15 10:31:00 - INFO - Match finished! Result: WIN
```

### `bug_reports.json`
Rapports de bugs détectés avec captures d'écran

### `ai_improvements.log`
Suggestions d'amélioration générées par Claude

## 🎯 Commandes clavier pendant l'exécution

- **Ctrl+C** - Arrêter l'exploration
- Le jeu continue à utiliser ses contrôles normaux

## 🔧 Contrôles du jeu (mappés par l'IA)

```python
"up": "w"
"down": "s"
"left": "a"
"right": "d"
"punch_light": "j"
"punch_medium": "k"
"punch_heavy": "l"
"kick_light": "u"
"kick_medium": "i"
"kick_heavy": "o"
"start": "return"
"select": "backspace"
```

## 💡 Comment l'IA s'améliore

1. **Collecte de données** - Chaque match génère des statistiques
2. **Analyse** - Tous les 5 matchs, l'IA demande des suggestions à Claude
3. **Apprentissage** - Les nouveaux combos et stratégies sont sauvegardés
4. **Application** - Les prochains matchs utilisent les nouvelles stratégies

## 🐛 Détection de bugs

L'IA recherche:
- Glitches graphiques
- Problèmes d'interface
- Texte incorrect
- Éléments manquants
- Problèmes de performance

Chaque bug détecté est sauvegardé avec:
- Timestamp
- Description détaillée
- Capture d'écran
- Contexte (menu/combat/etc)

## 📈 Statistiques d'exemple

Après une session de 1 heure:
```
╔══════════════════════════════════════════════════════╗
║              SESSION SUMMARY                         ║
╠══════════════════════════════════════════════════════╣
║  Total Games:     24                                 ║
║  Wins:            15                                 ║
║  Losses:          8                                  ║
║  Draws:           1                                  ║
║  Win Rate:        62.50%                             ║
║  Combos Learned:  12                                 ║
║  Bugs Found:      3                                  ║
╚══════════════════════════════════════════════════════╝
```

## ⚠️ Limitations

- Nécessite une clé API Anthropic (coût par analyse)
- Performance dépend de la puissance du PC
- Reconnaissance visuelle peut nécessiter ajustements selon la résolution
- Les mouvements sont simulés, pas aussi précis qu'un humain expert

## 🔮 Améliorations futures possibles

- [ ] Support multi-résolutions
- [ ] Apprentissage par renforcement (RL)
- [ ] Reconnaissance de frames spécifiques
- [ ] Optimisation des timings de combos
- [ ] Mode spectateur avec commentaire en direct
- [ ] API pour contrôle externe
- [ ] Dashboard web pour visualiser les stats

## 🤝 Contribution

Le système est conçu pour être extensible. Vous pouvez:

1. Ajouter de nouveaux combos dans `learned_combos`
2. Modifier les stratégies de combat
3. Améliorer la détection de bugs
4. Ajouter de nouveaux modes d'exploration

## 📞 Support

Si vous rencontrez des problèmes:
1. Vérifiez que toutes les dépendances sont installées
2. Consultez `ai_player.log` pour les erreurs
3. Assurez-vous que la clé API est valide
4. Vérifiez que le jeu est correctement installé

## 🎓 Apprentissage technique

Ce système utilise:
- **Claude Vision API** - Analyse visuelle
- **PyAutoGUI** - Simulation d'entrées
- **Keyboard** - Capture et simulation de touches
- **PIL** - Capture et traitement d'images
- **Threading** - Exécution asynchrone

C'est un excellent exemple de:
- Vision par ordinateur
- Automatisation de jeux
- Apprentissage par l'expérience
- Détection automatique de bugs
- Intelligence artificielle appliquée aux jeux

## 🏆 Objectif final

Créer un système qui peut:
1. **Tester exhaustivement** le jeu sans intervention humaine
2. **Découvrir des bugs** que les tests manuels pourraient manquer
3. **Équilibrer le gameplay** en identifiant les personnages/combos trop forts
4. **Générer du contenu** (replays, statistiques, guides)
5. **Servir de sparring partner** pour les joueurs humains

---

**Développé avec ❤️ pour KOF Ultimate**
