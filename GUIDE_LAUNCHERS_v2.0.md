# 🎮 GUIDE COMPLET - LAUNCHERS v2.0

**Date:** 2025-10-25
**Version:** 2.0
**Status:** RÉORGANISÉ - Système Battle.net-style

---

## 🚀 DÉMARRAGE RAPIDE

### Launcher Principal (RECOMMANDÉ)
```
KOF-LAUNCHER-v2.0-MAIN.bat
```
Interface style Battle.net avec menu complet:
- Solo/Local
- **Online Multiplayer** (nouveau!)
- Tests & Diagnostic
- Configuration
- Outils de réparation

---

## 🎮 LAUNCHERS DE JEU

### Lancement Simple
| Fichier | Description | Usage |
|---------|-------------|-------|
| **`KOF-LAUNCHER-v2.0-MAIN.bat`** | 🌟 **Launcher principal** - Menu complet Battle.net-style | **Débutants & Tous** |
| `KOF-LAUNCHER-v2.0-SIMPLE.bat` | Lancement simple avec tous les personnages (121) | Joueurs réguliers |
| `KOF-LAUNCHER-v2.0-STABLE-10.bat` | Mode stable avec 10 personnages testés | Tests de stabilité |
| `KOF-LAUNCHER-v2.0-QUICK.bat` | Lancement rapide sans menu | Utilisateurs avancés |
| `KOF-LAUNCHER-v2.0-FULL.bat` | Launcher avec options complètes | Configuration avancée |

---

## 🌐 ONLINE MULTIPLAYER

### Système Multijoueur (Nouveau!)
| Fichier | Description | Status |
|---------|-------------|--------|
| **`KOF-ONLINE-v2.0-LOBBY.bat`** | 🌟 **Lobby multijoueur** - Interface Battle.net | En développement |
| `KOF-ONLINE-v2.0-MATCHMAKING.bat` | Système de matchmaking automatique | Fonctionnel |
| `KOF-ONLINE-v2.0-SERVER.bat` | Démarrer serveur multijoueur | Fonctionnel |
| `KOF-ONLINE-v2.0-VS-AI.bat` | Jouer vs IA en ligne | Fonctionnel |
| `KOF-ONLINE-v2.0-VIRTUAL-PLAYERS.bat` | Joueurs virtuels pour remplir lobbies | Optionnel |

### Fonctionnalités du Lobby (En développement)
- ✅ Interface Battle.net-style
- 🔄 Matchmaking rapide
- 🔄 Matchmaking classé (ELO)
- 🔄 Salles personnalisées
- 🔄 Liste joueurs en ligne
- 🔄 Système de profils
- 🔄 Statistiques et classement

---

## 🧪 TESTS & DIAGNOSTIC

| Fichier | Description | Usage |
|---------|-------------|-------|
| `KOF-TEST-v2.0-EXHAUSTIF.bat` | Test tous les personnages | Tests complets |
| `KOF-TEST-v2.0-DIAGNOSTIC.bat` | Auto-diagnostic du système | Résolution problèmes |
| `KOF-TEST-v2.0-PROGRESS.bat` | Vérifier progression des tests | Monitoring |
| `KOF-TEST-v2.0-AUTOCHECK.bat` | Vérification automatique | Maintenance |

---

## 🔧 RÉPARATION & MAINTENANCE

| Fichier | Description | Quand l'utiliser |
|---------|-------------|------------------|
| `KOF-FIX-v2.0-CRASH.bat` | Corriger les crashes | Après crash du jeu |
| `KOF-FIX-v2.0-GENERAL.bat` | Réparation générale | Problèmes divers |
| `KOF-FIX-v2.0-IKEMEN.bat` | Réparer Ikemen GO | Erreurs moteur |
| `KOF-FIX-v2.0-PORTRAITS.bat` | Nettoyer portraits cassés | Problèmes visuels |

---

## 🤖 IA & AUTOMATION

| Fichier | Description | Usage |
|---------|-------------|-------|
| `KOF-AI-v2.0-MULTI-MODES.bat` | IA multi-modes | Tests avancés |
| `KOF-AI-v2.0-MULTI-PLAYERS.bat` | Plusieurs IA simultanées | Tests masse |
| `KOF-AI-v2.0-LOCAL-VS.bat` | Jouer vs IA locale | Entraînement |

---

## 📊 MONITORING & RAPPORTS

| Fichier | Description | Usage |
|---------|-------------|-------|
| `KOF-MONITOR-v2.0-DASHBOARD.bat` | Dashboard principal | Vue d'ensemble |
| `KOF-MONITOR-v2.0-REPORTS.bat` | Rapports détaillés | Analyse |

---

## 🛑 CONTRÔLE

| Fichier | Description | Quand l'utiliser |
|---------|-------------|------------------|
| `KOF-CONTROL-v2.0-STOP-ALL.bat` | Arrêter tous les processus | Nettoyage |
| `KOF-CONTROL-v2.0-EMERGENCY.bat` | Arrêt d'urgence | Problèmes critiques |

---

## 📋 ARCHITECTURE DU SYSTÈME v2.0

```
KOF Ultimate Online/
│
├── 🌟 KOF-LAUNCHER-v2.0-MAIN.bat        ← Point d'entrée principal
├── 🌐 KOF-ONLINE-v2.0-LOBBY.bat         ← Lobby multijoueur
│
├── 🎮 LAUNCHERS DE JEU/
│   ├── KOF-LAUNCHER-v2.0-SIMPLE.bat
│   ├── KOF-LAUNCHER-v2.0-STABLE-10.bat
│   ├── KOF-LAUNCHER-v2.0-QUICK.bat
│   └── KOF-LAUNCHER-v2.0-FULL.bat
│
├── 🌐 ONLINE MULTIPLAYER/
│   ├── KOF-ONLINE-v2.0-MATCHMAKING.bat
│   ├── KOF-ONLINE-v2.0-SERVER.bat
│   ├── KOF-ONLINE-v2.0-VS-AI.bat
│   └── KOF-ONLINE-v2.0-VIRTUAL-PLAYERS.bat
│
├── 🧪 TESTS/
│   ├── KOF-TEST-v2.0-EXHAUSTIF.bat
│   ├── KOF-TEST-v2.0-DIAGNOSTIC.bat
│   ├── KOF-TEST-v2.0-PROGRESS.bat
│   └── KOF-TEST-v2.0-AUTOCHECK.bat
│
├── 🔧 RÉPARATION/
│   ├── KOF-FIX-v2.0-CRASH.bat
│   ├── KOF-FIX-v2.0-GENERAL.bat
│   ├── KOF-FIX-v2.0-IKEMEN.bat
│   └── KOF-FIX-v2.0-PORTRAITS.bat
│
├── 🤖 IA/
│   ├── KOF-AI-v2.0-MULTI-MODES.bat
│   ├── KOF-AI-v2.0-MULTI-PLAYERS.bat
│   └── KOF-AI-v2.0-LOCAL-VS.bat
│
├── 📊 MONITORING/
│   ├── KOF-MONITOR-v2.0-DASHBOARD.bat
│   └── KOF-MONITOR-v2.0-REPORTS.bat
│
├── 🛑 CONTRÔLE/
│   ├── KOF-CONTROL-v2.0-STOP-ALL.bat
│   └── KOF-CONTROL-v2.0-EMERGENCY.bat
│
└── 📦 ARCHIVES/
    └── launchers_archive/              ← Anciens launchers
```

---

## 🆚 COMPARAISON v1.0 → v2.0

### Avant (v1.0)
- ❌ 69 fichiers .bat désorganisés
- ❌ Noms incohérents
- ❌ Pas de versioning
- ❌ Doublons nombreux
- ❌ Aucun système online unifié

### Après (v2.0)
- ✅ ~25 fichiers essentiels organisés
- ✅ Noms cohérents avec préfixes
- ✅ Versioning v2.0
- ✅ 44 fichiers obsolètes archivés
- ✅ **Système online Battle.net-style**
- ✅ Launcher principal unifié

---

## 🎯 SCÉNARIOS D'UTILISATION

### Je veux jouer localement
```
→ KOF-LAUNCHER-v2.0-MAIN.bat
   → [1] Lancer le jeu (Simple)
```

### Je veux jouer en ligne
```
→ KOF-LAUNCHER-v2.0-MAIN.bat
   → [4] Système Matchmaking
   OU
   → [7] Lobby Multi-Joueurs (quand disponible)
```

### Le jeu crash
```
→ KOF-LAUNCHER-v2.0-MAIN.bat
   → [R] Outils de Réparation
   → [1] Correction des crashes
```

### Je veux tester la stabilité
```
→ KOF-LAUNCHER-v2.0-STABLE-10.bat
(Lance avec seulement 10 personnages testés)
```

### Je veux tout vérifier
```
→ KOF-LAUNCHER-v2.0-MAIN.bat
   → [9] Auto-diagnostic complet
```

---

## 🔄 MIGRATION DEPUIS v1.0

Si vous avez des scripts personnalisés utilisant les anciens noms:

| Ancien nom | Nouveau nom v2.0 |
|------------|------------------|
| `LANCER_JEU_SIMPLE.bat` | `KOF-LAUNCHER-v2.0-SIMPLE.bat` |
| `START_MATCHMAKING_SYSTEM.bat` | `KOF-ONLINE-v2.0-MATCHMAKING.bat` |
| `CORRIGER_CRASH.bat` | `KOF-FIX-v2.0-CRASH.bat` |
| `LANCER_TEST_EXHAUSTIF.bat` | `KOF-TEST-v2.0-EXHAUSTIF.bat` |

**Note:** Les anciens fichiers sont sauvegardés dans `launchers_archive/`

---

## 🌐 ROADMAP SYSTÈME ONLINE

### Phase 1 (Actuel) ✅
- ✅ Structure lobby Battle.net-style
- ✅ Interface utilisateur
- ✅ Menu intégré au launcher principal

### Phase 2 (En cours) 🔄
- 🔄 Serveur backend fonctionnel
- 🔄 Système de comptes joueurs
- 🔄 Matchmaking rapide

### Phase 3 (Prévu) 📋
- 📋 Matchmaking classé (ELO)
- 📋 Salles personnalisées
- 📋 Chat en temps réel
- 📋 Liste joueurs en ligne

### Phase 4 (Futur) 🔮
- 🔮 Système de classement par saisons
- 🔮 Tournois automatisés
- 🔮 Replay system
- 🔮 Statistiques avancées

---

## 📞 SUPPORT

### Problèmes courants

**Q: Le launcher principal ne s'affiche pas correctement**
```
R: Vérifiez que votre terminal supporte UTF-8 (chcp 65001)
```

**Q: Les anciens launchers ne marchent plus**
```
R: Utilisez les nouveaux noms v2.0 ou restaurez depuis launchers_archive/
```

**Q: Le lobby online ne fonctionne pas**
```
R: C'est normal, il est en développement. Utilisez KOF-ONLINE-v2.0-MATCHMAKING.bat
```

**Q: Comment restaurer l'ancien système?**
```
R: Copiez les fichiers depuis launchers_backup_AAAAMMJJ/
```

---

## 🎖️ BONNES PRATIQUES

1. **Toujours utiliser le launcher principal** pour une expérience complète
2. **Testez en mode stable** (10 persos) avant d'utiliser le mode complet
3. **Consultez le dashboard** régulièrement pour vérifier la santé du système
4. **Sauvegardez vos configurations** avant de faire des réparations
5. **Utilisez les outils de diagnostic** dès les premiers signes de problème

---

**Créé le:** 2025-10-25
**Dernière mise à jour:** 2025-10-25
**Version:** 2.0.0
