# 🎮 SYSTÈME DE TESTS CONTINUS - EN COURS

## ✅ STATUT : ACTIF

**Date de démarrage :** 2025-10-23 10:59:54

Le système de tests automatiques tourne **en arrière-plan** et **ne vous dérange PAS** !

---

## 📊 CONFIGURATION

| Paramètre | Valeur |
|-----------|--------|
| **Intervalle entre tests** | 5 minutes (300s) |
| **Durée d'un test** | ~90 secondes |
| **Tests max par session** | 100 |
| **Mode** | Silencieux (arrière-plan) |
| **Méthode** | Injection d'inputs (Windows Messages) |

---

## 🎯 CE QUI EST TESTÉ

Chaque test automatique effectue :

1. **Lancement du jeu** → Trouve la fenêtre
2. **Écran titre** → ESPACE pour entrer
3. **Navigation menus** → Parcourt les 7 options
4. **Mode Versus** → Entre dans la sélection
5. **Sélection personnage** → Choisit un combattant
6. **Gameplay** → Joue pendant 15 secondes
7. **Sortie** → ESCAPE et retour menu

**Total par test :** ~90 secondes

---

## 📁 OÙ TROUVER LES RAPPORTS

Tous les rapports sont sauvegardés dans :

```
D:\KOF Ultimate Online\logs\tests_continus\
```

### Fichiers générés :

```
logs/tests_continus/
├── continuous.log              ← Log en temps réel
├── stats.json                  ← Statistiques globales
├── console.log                 ← Console du système
├── test_0001_YYYYMMDD_HHMMSS.txt  ← Rapport test #1
├── test_0002_YYYYMMDD_HHMMSS.txt  ← Rapport test #2
└── ...
```

---

## 🎯 COMMANDES UTILES

### Voir le dashboard en temps réel

```bash
VOIR_DASHBOARD.bat
```

Affiche :
- ✅ Nombre total de tests
- ✅ Taux de réussite
- ✅ Derniers problèmes détectés
- ✅ Log en direct
- ✅ Actualisation automatique toutes les 5s

### Voir les rapports

```bash
VOIR_RAPPORTS_CONTINUS.bat
```

Affiche :
- 📊 Statistiques JSON
- 📝 Dernier rapport de test
- 📋 Log continu (50 dernières lignes)

### Arrêter les tests

```bash
ARRETER_TESTS_CONTINUS.bat
```

Arrête proprement :
- Le système de tests
- Le jeu s'il est ouvert
- Sauvegarde les stats

---

## 📊 EXEMPLE DE RAPPORT

Voici à quoi ressemble un rapport de test :

```
TEST AUTOMATIQUE #1
============================================================

Date: 2025-10-23 10:59:54
Durée: 87.3s
Problèmes: 0

✅ Aucun problème détecté
```

---

## 🔄 CYCLE DE TESTS

```
┌─────────────────────────────────────────────────────────┐
│ [10:59] Test #1 démarre                                │
│ [11:01] Test #1 terminé (87s) → ✅                      │
│ [11:01-11:06] Pause de 5 minutes                       │
│ [11:06] Test #2 démarre                                │
│ [11:08] Test #2 terminé (89s) → ✅                      │
│ [11:08-11:13] Pause de 5 minutes                       │
│ [11:13] Test #3 démarre                                │
│ ...                                                     │
└─────────────────────────────────────────────────────────┘
```

**Tests par jour :** ~288 tests (24h ÷ 5min)

---

## ✅ AVANTAGES

### Vous pouvez travailler normalement

- ✅ **Aucune interference** avec vos consoles/éditeurs
- ✅ **Inputs injectés** directement dans le jeu
- ✅ **Mode silencieux** (fenêtres minimisées)
- ✅ **Rapports automatiques** sans intervention

### Détection précoce des bugs

- 🐛 Crashs aléatoires
- 🐛 Freeze du jeu
- 🐛 Problèmes de menus
- 🐛 Bugs de sélection
- 🐛 Problèmes de gameplay

### Statistiques fiables

- 📊 Taux de réussite sur longue période
- 📊 Tendances (le jeu devient plus stable/bugué ?)
- 📊 Identification de patterns

---

## 🎯 ÉTAT ACTUEL (Premier test)

D'après les logs :

```
[10:59:54] Système démarré
[10:59:54] Test #1 commence
[10:59:54] Jeu lancé (PID: 4864)
[En cours...]
```

**Le premier test est EN COURS !** 🎮

Résultats disponibles dans ~2 minutes.

---

## 💡 CONSEILS

### Pour monitoring actif

Laissez ouvert un terminal avec :

```bash
VOIR_DASHBOARD.bat
```

Il se rafraîchit toutes les 5 secondes avec les dernières infos.

### Pour vérification ponctuelle

De temps en temps, lancez :

```bash
VOIR_RAPPORTS_CONTINUS.bat
```

Pour voir les stats globales et le dernier test.

### Pour debug

Si quelque chose ne va pas :

```bash
# Voir tous les logs
type logs\tests_continus\continuous.log

# Voir le dernier rapport
dir /od logs\tests_continus\test_*.txt
type logs\tests_continus\test_XXXX_XXXXXXXXX_XXXXXX.txt
```

---

## 🐛 EN CAS DE PROBLÈME

### Le jeu crash

Le système va :
1. Détecter l'échec
2. Logger le problème
3. Fermer proprement
4. Attendre 5 minutes
5. Relancer un nouveau test

### Le système ne démarre pas

Vérifiez :
- `pywin32` est installé : `pip show pywin32`
- Le jeu existe : `KOF_Ultimate_Online.exe`
- Python est accessible : `python --version`

### Pas de rapports générés

Vérifiez :
- Le dossier existe : `logs\tests_continus\`
- Le système tourne : Regardez les processus Python
- Les permissions : Droits en écriture sur le dossier

---

## 🎉 RÉSUMÉ

**Vous avez maintenant un système de tests AUTONOME qui :**

✅ Teste le jeu toutes les 5 minutes
✅ Génère des rapports automatiques
✅ Ne vous dérange PAS pendant votre travail
✅ Détecte les bugs automatiquement
✅ S'arrête proprement si demandé

**Vous pouvez continuer à coder tranquillement !** 🚀

---

**Créé le :** 2025-10-23 11:00
**Statut :** ✅ ACTIF
**Premier test :** En cours...
