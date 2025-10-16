# 🤖 KOF Ultimate - AI Navigator System

## Vue d'ensemble

Le système AI Navigator est un agent intelligent qui surveille automatiquement le launcher KOF Ultimate en parallèle et détecte tous les problèmes potentiels.

## ✨ Fonctionnalités

### 🎯 Détection Automatique
- ✅ Auto-installation des dépendances Python manquantes
- ✅ Surveillance en temps réel du launcher
- ✅ Capture d'écran automatique
- ✅ Analyse avec Claude AI (si clé API disponible)
- ✅ Vérifications basiques sans IA
- ✅ Détection des erreurs et warnings
- ✅ Log complet de toutes les actions
- ✅ Interface de monitoring moderne

### 📊 Interface de Monitoring

L'agent AI Navigator affiche :
- **Statut en temps réel** du monitoring
- **Statistiques** (actions, problèmes détectés, temps)
- **Log de navigation** complet avec horodatage
- **Problèmes détectés** classés par sévérité
- **Contrôles** (Start, Stop, Save Log)

## 🚀 Lancement

### Méthode 1 : Lancement Automatique (Recommandé)

Double-cliquez sur :
```
D:\KOF Ultimate\launch_with_ai.bat
```

Cela lance automatiquement :
1. Le launcher principal (fenêtre 1)
2. L'agent AI Navigator (fenêtre 2)

### Méthode 2 : Lancement Manuel

**Fenêtre 1 - Launcher Principal :**
```bash
cd "D:\KOF Ultimate"
python launcher.py
```

**Fenêtre 2 - AI Navigator :**
```bash
cd "D:\KOF Ultimate"
python launcher_ai_navigator.py
```

## 🔧 Configuration

### Dépendances Auto-Installées

Au premier lancement, le launcher installe automatiquement :
- `pillow` - Traitement d'images
- `anthropic` - API Claude AI
- `pyautogui` - Automatisation GUI
- `opencv-python` - Vision par ordinateur
- `numpy` - Calculs numériques
- `keyboard` - Contrôle clavier
- `mouse` - Contrôle souris
- `python-dotenv` - Variables d'environnement
- `requests` - Requêtes HTTP

### Configuration de l'API Claude (Optionnel)

Pour activer l'analyse IA avancée avec Claude :

**Windows :**
```bash
set ANTHROPIC_API_KEY=votre_clé_api_ici
```

**PowerShell :**
```powershell
$env:ANTHROPIC_API_KEY="votre_clé_api_ici"
```

**Permanent (dans le système) :**
1. Panneau de configuration > Système > Paramètres système avancés
2. Variables d'environnement
3. Nouvelle variable : `ANTHROPIC_API_KEY`
4. Valeur : votre clé API

> **Note :** L'agent fonctionne aussi sans clé API (mode basique)

## 📋 Utilisation

### 1. Démarrer le Monitoring

1. Lancez les deux fenêtres (méthode 1 ou 2)
2. Dans la fenêtre AI Navigator, cliquez sur **"▶ START MONITORING"**
3. L'agent commence à surveiller automatiquement

### 2. Navigation Parallèle

L'agent surveille pendant que vous naviguez sur le launcher :
- Cliquez sur différents boutons
- Testez les fonctionnalités
- Changez les options
- L'agent détecte tout problème automatiquement

### 3. Consulter les Résultats

**Navigation Log :**
- Affiche toutes les actions effectuées
- Horodatage précis
- Niveaux : INFO, WARNING, ERROR, SUCCESS

**Problems Detected :**
- 🔴 HIGH - Problème critique (fichier manquant, etc.)
- 🟠 MEDIUM - Problème modéré (warning, etc.)
- 🟡 LOW - Problème mineur (launcher non ouvert, etc.)

### 4. Sauvegarder le Log

Cliquez sur **"💾 SAVE LOG"** pour sauvegarder :
```
D:\KOF Ultimate\launcher_ai_log.json
```

Format JSON complet avec :
- Timestamp
- Runtime total
- Log de navigation complet
- Liste des problèmes détectés

## 🎨 Design Amélioré du Launcher

Le launcher a été entièrement redesigné avec :

### Nouveau Design Moderne
- 🌟 Titre doré avec effets visuels
- 🎨 Palette de couleurs améliorée (bleu foncé, violet, doré)
- ✨ Effets de survol sur tous les boutons
- 📐 Bordures et reliefs 3D
- 💎 Typographie Consolas moderne

### Boutons Principaux
- **▶▶▶ JOUER ◀◀◀** - Vert lumineux avec effet hover
- **🌐 MULTIJOUEUR ONLINE 🌐** - Bleu éclatant
- **🤖 AI PLAYER** - Rouge/jaune pour l'attention

### Boutons Secondaires
- Effet hover sur tous
- Couleurs cohérentes
- Icônes emoji pour clarté

## 🌌 Nouveaux Backgrounds Spatiaux

6 superbes fonds d'écran spatiaux ont été générés :

### 1. Deep Space
**Fichier :** `space_deep.png`
- Espace profond avec nébuleuse violette/bleue
- 800+ étoiles
- Effet nébuleuse atmosphérique

### 2. Purple Nebula
**Fichier :** `space_nebula_purple.png`
- Nébuleuse rose/violette éclatante
- Nuages cosmiques
- Étoiles scintillantes

### 3. Planet View
**Fichier :** `space_planet.png`
- Grande planète bleue avec anneaux (type Saturne)
- Petite lune en arrière-plan
- Nébuleuse bleue

### 4. Spiral Galaxy
**Fichier :** `space_galaxy.png`
- Galaxie spirale complète
- Bras spiraux lumineux
- Centre galactique brillant

### 5. Binary Stars
**Fichier :** `space_binary.png`
- Deux soleils (rouge et bleu)
- Effet de luminosité intense
- Espace profond en arrière-plan

### 6. Cosmic Void
**Fichier :** `space_void.png`
- Vide cosmique mystérieux
- Peu d'étoiles, très espacées
- Nébuleuse très sombre

**Emplacement :**
```
D:\KOF Ultimate\stages\space_backgrounds\
```

**Fichiers .def créés :**
- `space_deep.def`
- `space_nebula_purple.def`
- `space_planet.def`
- `space_galaxy.def`
- `space_binary.def`
- `space_void.def`

### 📦 Prochaines Étapes pour les Stages Spatiaux

Pour utiliser ces backgrounds dans le jeu :

1. **Convertir en format SFF** (requis par MUGEN)
   ```
   Utilisez Fighter Factory pour convertir les PNG en SFF
   ```

2. **Placer les fichiers SFF**
   ```
   D:\KOF Ultimate\stages\space_backgrounds\*.sff
   ```

3. **Ajouter aux stages disponibles**
   ```
   Éditer: D:\KOF Ultimate\data\select.def
   Ajouter: stages/space_deep.def (etc.)
   ```

## 🔍 Détection des Problèmes

### Vérifications Automatiques

L'agent vérifie :
- ✅ Fenêtre du launcher ouverte
- ✅ Fichiers essentiels présents
- ✅ État de l'interface (via Claude AI)
- ✅ Messages d'erreur visibles
- ✅ Boutons accessibles

### Analyse avec Claude AI

Quand l'API est configurée, Claude analyse :
1. **État de l'interface**
   - Tous les boutons visibles
   - Leurs états (activé/désactivé)

2. **Problèmes potentiels**
   - Messages d'erreur
   - Éléments manquants
   - Warnings

3. **Actions recommandées**
   - Corrections suggérées
   - Étapes de résolution

## 📊 Statistiques de Monitoring

L'interface affiche en temps réel :
- **Actions effectuées** : Nombre total d'itérations
- **Problèmes détectés** : Compteur de problèmes
- **Temps d'exécution** : HH:MM:SS
- **Statut IA** : Connected / Not connected

## 🛠️ Dépannage

### Problème : "ANTHROPIC_API_KEY not found"
**Solution :** Normal si vous n'avez pas configuré l'API. L'agent fonctionne quand même en mode basique.

### Problème : "Launcher window not found"
**Solution :** Lancez d'abord le launcher principal avant de démarrer le monitoring.

### Problème : Dépendances manquantes
**Solution :** Le launcher les installe automatiquement au premier lancement.

### Problème : L'interface AI Navigator ne répond pas
**Solution :** Normal pendant le monitoring. Cliquez sur "⏹ STOP" pour arrêter.

## 📝 Format du Log JSON

Structure du fichier `launcher_ai_log.json` :

```json
{
  "timestamp": "2025-10-15T20:30:45.123456",
  "runtime": "00:05:23",
  "navigation_log": [
    {
      "timestamp": "20:30:45",
      "level": "INFO",
      "message": "Starting AI navigation monitoring"
    },
    ...
  ],
  "problems_detected": [
    {
      "timestamp": "2025-10-15T20:31:12.456789",
      "severity": "HIGH",
      "description": "Missing essential file: mugen.cfg"
    },
    ...
  ]
}
```

## 🎯 Améliorations Futures

- [ ] Support multi-langue
- [ ] Historique des sessions
- [ ] Graphiques de statistiques
- [ ] Auto-correction des problèmes
- [ ] Intégration Discord pour notifications
- [ ] Mode headless (sans interface)
- [ ] API REST pour contrôle externe

## 📞 Support

En cas de problème :
1. Consultez ce README
2. Vérifiez le log : `launcher_ai_log.json`
3. Consultez les autres guides dans le dossier

## 🏆 Résumé

**Système complet de monitoring intelligent pour KOF Ultimate !**

- ✅ Auto-installation des dépendances
- ✅ Design moderne du launcher
- ✅ Agent IA de surveillance
- ✅ Détection automatique des problèmes
- ✅ 6 nouveaux backgrounds spatiaux
- ✅ Interface de monitoring professionnelle
- ✅ Logs complets et détaillés

**Profitez de votre expérience KOF Ultimate améliorée ! 🎮⚡**
