# ⚠️ PROBLÈME AVEC LES TESTS AUTOMATIQUES

## 🐛 Le Problème

Quand le test automatique envoie des touches (via `pyautogui`), ces touches sont reçues par **toutes les fenêtres actives**, pas seulement le jeu :

- ❌ Vos consoles PowerShell/CMD
- ❌ Votre éditeur de code
- ❌ Votre navigateur
- ❌ N'importe quelle application ouverte

**Résultat :** Des caractères bizarres apparaissent dans vos consoles : `aaaaasssszzzxxx↓↓↑↑→←`

---

## ✅ SOLUTIONS DISPONIBLES

### 1️⃣ TEST MANUEL GUIDÉ (RECOMMANDÉ)
**Fichier :** `LANCER_TEST_MANUEL.bat`

**Comment ça marche :**
- Le script vous **guide** pas à pas
- **VOUS** appuyez sur les touches
- Le script note si ça a fonctionné ou non

**Avantages :**
- ✅ Aucun risque pour vos autres fenêtres
- ✅ Vous gardez le contrôle total
- ✅ Bon pour apprendre le jeu
- ✅ Détecte les vrais problèmes UX

**Inconvénients :**
- ⚠️ Demande votre temps (~3 min)
- ⚠️ Pas complètement automatique

**Utilisation :**
```bash
# Double-cliquez sur :
LANCER_TEST_MANUEL.bat

# Suivez les instructions à l'écran
```

---

### 2️⃣ TEST AUTO AVEC FOCUS FORCÉ
**Fichier :** `LANCER_TEST_AUTO_FOCUS.bat`

**Comment ça marche :**
- Le script force le focus sur la fenêtre du jeu avant chaque touche
- Réduit (mais n'élimine pas) le risque d'interférence

**Avantages :**
- ✅ Plus automatique
- ✅ Moins de risque que le test basique

**Inconvénients :**
- ⚠️ Peut encore affecter d'autres fenêtres
- ⚠️ Nécessite installation de `pygetwindow`
- ⚠️ Moins fiable sur multi-écrans

**Préparation :**
```bash
pip install pygetwindow
```

**Utilisation :**
```bash
# 1. Minimisez vos fenêtres importantes
# 2. Fermez vos consoles de travail
# 3. Lancez :
LANCER_TEST_AUTO_FOCUS.bat
```

---

### 3️⃣ TEST AUTO BASIQUE (NON RECOMMANDÉ)
**Fichier :** `LANCER_TEST_RAPIDE.bat`

**⚠️ NE PAS UTILISER** si vous avez d'autres fenêtres ouvertes !

**Utilisation :**
```bash
# Seulement si :
# - Vous fermez TOUTES les autres fenêtres
# - Le jeu est en plein écran
# - Vous ne touchez à RIEN pendant 2 minutes

LANCER_TEST_RAPIDE.bat
```

---

## 🎯 QUELLE SOLUTION CHOISIR ?

| Situation | Solution |
|-----------|----------|
| **Vous travaillez** sur d'autres projets | ➡️ **TEST MANUEL GUIDÉ** |
| **Vous voulez tester rapidement** | ➡️ **TEST MANUEL GUIDÉ** |
| **Première fois** que vous testez | ➡️ **TEST MANUEL GUIDÉ** |
| **Test de régression** (rien d'ouvert) | ➡️ Test auto avec focus |
| **Test CI/CD** (machine dédiée) | ➡️ Test auto basique |

---

## 📊 RÉSULTATS DU DERNIER TEST AUTO

**Date :** 2025-10-23 10:43
**Durée :** 86.8s (1.4 min)
**Résultat :** ✅ 0 problème détecté

**Tests passés :**
1. ✅ Lancement du jeu (3.2s)
2. ✅ Écran titre (20.3s)
3. ✅ Navigation menus (31.6s)
4. ✅ Mode Versus (39.6s)
5. ✅ Sélection personnage (44.1s)
6. ✅ Gameplay 30s (80.3s)
7. ✅ Pause & sortie (86.8s)

**Conclusion :** Le jeu fonctionne parfaitement !

---

## 💡 CONSEIL

Pour les **tests réguliers pendant le développement**, utilisez :

```bash
LANCER_TEST_MANUEL.bat
```

C'est rapide, sûr, et vous permet de garder vos consoles ouvertes. 👍

---

## 🔧 ALTERNATIVES AVANCÉES

Si vous voulez vraiment des tests 100% automatiques sans interférence :

### Option A : Machine virtuelle
- Créer une VM Windows
- Y installer le jeu
- Lancer les tests automatiques dedans

### Option B : Conteneur Docker (Windows)
- Container Windows Server
- Jeu + tests à l'intérieur
- Isolé de votre système

### Option C : API de test Ikemen GO
- Modifier Ikemen GO pour exposer une API
- Contrôler le jeu via HTTP/WebSocket
- Pas de simulation clavier

**Note :** Ces options sont complexes et probablement **overkill** pour ce projet.

---

## 📝 RECOMMANDATION FINALE

**Utilisez `LANCER_TEST_MANUEL.bat` !**

C'est la solution la plus simple, la plus sûre, et franchement, ça prend juste 3 minutes de votre temps. Le jeu fonctionne déjà bien (0 problème détecté), donc pas besoin de tests automatiques complexes.

---

**Dernière mise à jour :** 2025-10-23
