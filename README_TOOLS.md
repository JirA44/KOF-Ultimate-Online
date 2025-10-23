# 🛠️ KOF Ultimate Online - Outils de Maintenance

## 📋 Vue d'ensemble

Ce pack contient des outils intelligents pour vérifier, réparer et lancer KOF Ultimate Online sans problèmes.

---

## 🎯 Fichiers disponibles

### 🚀 Lanceurs (recommandés)

| Fichier | Description | Usage |
|---------|-------------|-------|
| **LAUNCH_MENU.bat** | Menu interactif complet | ⭐ **RECOMMANDÉ** - Toutes les options dans un seul menu |
| **LAUNCH_SAFE.bat** | Lancement direct sécurisé | Vérifie et répare automatiquement, puis lance le jeu |

### 🔧 Outils Python

| Fichier | Description | Commande |
|---------|-------------|----------|
| **IKEMEN_CHECKER.py** | Vérificateur intelligent | `python IKEMEN_CHECKER.py` |
| **REBUILD_SELECT.py** | Reconstructeur de select.def | `python REBUILD_SELECT.py --yes` |

---

## 🎮 Utilisation

### Méthode 1 : Menu interactif (RECOMMANDÉ)

```batch
Double-cliquez sur : LAUNCH_MENU.bat
```

Le menu vous permet de :
- 🚀 Lancer le jeu avec vérification automatique
- 🔍 Vérifier l'installation
- 🔨 Reconstruire select.def si nécessaire
- 📊 Voir les statistiques

### Méthode 2 : Lancement direct

```batch
Double-cliquez sur : LAUNCH_SAFE.bat
```

Lance automatiquement après vérification et réparation si nécessaire.

---

## 🔍 Détails des outils

### IKEMEN_CHECKER.py

**Fonction** : Vérifie l'intégrité de votre installation

**Ce qu'il vérifie** :
- ✅ Présence des dossiers essentiels (chars, stages, data, sound)
- ✅ Présence de l'exécutable
- ✅ Validité du fichier select.def
- ✅ Existence de tous les personnages listés
- ✅ Existence de tous les stages listés

**Ligne de commande** :
```bash
# Vérification simple
python IKEMEN_CHECKER.py

# Vérification + réparation automatique
python IKEMEN_CHECKER.py --auto-repair
```

**Sortie** :
- ✅ Vert = OK
- ⚠️ Jaune = Avertissement
- ❌ Rouge = Erreur critique

---

### REBUILD_SELECT.py

**Fonction** : Reconstruit complètement le fichier select.def

**Ce qu'il fait** :
1. 🔍 Scanne le dossier `chars/` pour trouver tous les personnages disponibles
2. 🔍 Scanne le dossier `stages/` pour trouver tous les stages
3. 💾 Crée un backup horodaté du select.def actuel
4. ✍️ Génère un nouveau select.def avec tous les personnages et stages trouvés

**Ligne de commande** :
```bash
# Avec confirmation
python REBUILD_SELECT.py

# Sans confirmation (automatique)
python REBUILD_SELECT.py --yes
```

**Backups** :
Les backups sont créés automatiquement avec un timestamp :
- `select.def.backup_20251023_113846`
- `select.def.backup_20251023_120000`
- etc.

---

## 🐛 Problèmes courants

### Le jeu ne se lance pas

1. Exécutez `LAUNCH_MENU.bat`
2. Choisissez l'option "2. Vérifier l'installation"
3. Si des erreurs apparaissent, choisissez "3. Reconstruire select.def"
4. Relancez avec l'option 1

### "Personnages invalides" détectés

**Cause** : Le fichier select.def contient des références à des personnages qui n'existent pas

**Solution automatique** :
```batch
python REBUILD_SELECT.py --yes
```

**Solution manuelle** :
1. Ouvrir `data\select.def` avec un éditeur de texte
2. Supprimer les lignes des personnages manquants
3. Sauvegarder

### "Stages invalides" détectés

Même solution que pour les personnages invalides.

---

## 📊 Format du fichier select.def

Le fichier `data/select.def` doit suivre ce format :

```ini
[Characters]
;------------------------------

arcade.maxmatches = 6,1,1,0,0,0,0,0,0,0
team.maxmatches = 4,1,1,0,0,0,0,0,0,0

chars/Rugal-boss/Rugal-boss.def
chars/Kyo/Kyo.def
chars/Iori/Iori.def
...

[ExtraStages]
;------------------------------

stages/stage1.def
stages/stage2.def

[Stages]
;------------------------------

stages/stage1.def
stages/stage2.def
stages/stage3.def

[Options]
;------------------------------

arcade.rematches = 0
team.loseondraw = 1
```

**Important** :
- Les chemins doivent être relatifs depuis la racine du jeu
- Format : `chars/nom-dossier/nom-fichier.def`
- Les lignes commençant par `;` sont des commentaires
- Les lignes avec `=` sont des paramètres de configuration

---

## 🔧 Maintenance régulière

### Après avoir ajouté de nouveaux personnages

1. Copiez les dossiers de personnages dans `chars/`
2. Lancez `REBUILD_SELECT.py --yes`
3. Les nouveaux personnages seront automatiquement ajoutés

### Après avoir ajouté de nouveaux stages

1. Copiez les fichiers .def de stages dans `stages/`
2. Lancez `REBUILD_SELECT.py --yes`
3. Les nouveaux stages seront automatiquement ajoutés

---

## 💡 Astuces

### Lancement rapide

Créez un raccourci sur le bureau vers `LAUNCH_SAFE.bat` pour un lancement en un clic.

### Vérification périodique

Lancez `IKEMEN_CHECKER.py` de temps en temps pour vous assurer que tout est OK.

### Backups automatiques

Tous les outils créent des backups automatiques avant toute modification. Vous pouvez les trouver dans le dossier `data/` avec l'extension `.backup_*`.

---

## 📝 Logs et diagnostics

### En cas de problème

1. Lancez : `python IKEMEN_CHECKER.py > diagnostic.txt`
2. Envoyez le fichier `diagnostic.txt` pour obtenir de l'aide

---

## 🆘 Support

Si vous rencontrez des problèmes :

1. ✅ Vérifiez que Python 3.x est installé
2. ✅ Vérifiez que tous les fichiers .py et .bat sont dans le même dossier que le jeu
3. ✅ Lancez `IKEMEN_CHECKER.py` pour voir les erreurs détaillées
4. ✅ Essayez `REBUILD_SELECT.py --yes` pour une reconstruction complète

---

## 📜 Historique des versions

### v1.0 (2025-10-23)
- ✨ Première version
- ✅ Vérificateur intelligent (IKEMEN_CHECKER.py)
- ✅ Reconstructeur automatique (REBUILD_SELECT.py)
- ✅ Lanceurs sécurisés (.bat)
- ✅ Menu interactif complet

---

## 👥 Crédits

Développé avec ❤️ par l'équipe KOF Ultimate Online
Propulsé par Claude Code 🤖

---

**🎮 Bon jeu !**
