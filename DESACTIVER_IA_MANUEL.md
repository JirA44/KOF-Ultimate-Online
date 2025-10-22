# 🎮 Comment Désactiver l'IA Automatique

## Le Problème
L'IA du jeu joue automatiquement à votre place au lieu de vous laisser contrôler.

## Solutions

### 1. Dans le Jeu (Solution Rapide)
Pendant la sélection des personnages:
1. Appuyez sur **START** sur le personnage
2. Maintenez **START** pour le sélectionner en mode MANUEL
3. L'IA ne devrait plus contrôler ce personnage

### 2. Configuration Permanente (mugen.cfg)
Ouvrir `data/mugen.cfg` et modifier:

```ini
[Config]
; Désactiver toute IA pour le joueur
P1.CPU = 0
AIRandomColor = 0

; Le joueur 1 est TOUJOURS humain
Team.1VS2Life = 100
Team.LoseOnKO = 1
```

### 3. Mode de Jeu
Dans les options du jeu:
- Mode : **VS MODE** (pas Training, pas Watch)
- Difficulté : Normale
- P1 Control : **HUMAN** (pas AI, pas AUTO)

### 4. Fichiers Personnages
Certains personnages ont une IA forcée dans leur .def:
- Ouvrir `chars/[nom]/[nom].def`
- Chercher les lignes avec `AILevel` ou `ai.level`
- Les commenter avec un `;` devant

Exemple:
```ini
;AILevel = 8    <- Commenté, IA désactivée
```

### 5. Vérifier les Contrôles
Dans les options:
- Config → Input Config
- Vérifier que vos touches sont bien assignées
- Player 1 doit être en mode **Keyboard** ou **Joystick**

## Si Rien Ne Marche

1. Supprimer `data/mugen.cfg`
2. Relancer le jeu (créera un nouveau fichier par défaut)
3. Reconfigurer vos touches dans les options

## Script de Correction Automatique
Exécutez: `python FIX_AI_AUTOPLAY.py`

Ce script désactive automatiquement tous les paramètres d'IA automatique.
