# 🎮 GUIDE DES TESTS AUTOMATIQUES
**KOF Ultimate Online - Système de Test UX**

---

## 🚀 TESTS DISPONIBLES

### 1. Test Rapide (2 minutes)
**Fichier:** `LANCER_TEST_RAPIDE.bat`
**Utilité:** Diagnostic UX rapide avec un seul joueur simulé

**Ce qui est testé:**
- ✅ Lancement du jeu
- ✅ Écran titre et entrée
- ✅ Navigation dans les menus
- ✅ Mode Versus
- ✅ Sélection de personnage
- ✅ Gameplay (30s)
- ✅ Pause et sortie

**Résultat:** Rapport dans `logs/test_rapide_XXXXXX.txt`

---

### 2. Test Multi-Joueurs (Plus long)
**Fichier:** `LANCER_TEST_JOUEURS.bat`
**Utilité:** Simule plusieurs joueurs simultanés

**Scénarios testés:**
- 🎯 Joueur novice (hésite, explore)
- 🎯 Joueur intermédiaire (efficace)
- 🎯 Joueur expérimenté (rapide)
- 🎯 Joueur qui abandonne (test frustration)

---

## ⚠️ PRÉCAUTIONS

**AVANT de lancer un test:**
1. Ne touchez PAS la souris/clavier
2. Assurez-vous que le jeu n'est pas déjà lancé
3. Fermez les autres applications qui pourraient capter les touches

**PENDANT le test:**
- ❌ Ne bougez pas la souris
- ❌ N'appuyez sur aucune touche
- ✅ Pour arrêter : déplacez la souris dans le coin haut-gauche

**APRÈS le test:**
- Consultez le rapport dans `logs/`
- Regardez les captures d'écran si disponibles
- Vérifiez les problèmes détectés

---

## 📊 INTERPRÉTATION DES RÉSULTATS

### ✅ Résultat Idéal
```
⏱️  Durée totale: 120s (2 min)
⚠️  Problèmes trouvés: 0
✅ AUCUN PROBLÈME DÉTECTÉ!
```

### ⚠️ Problèmes Courants

**"Exe introuvable"**
→ Vérifiez que `KOF_Ultimate_Online.exe` existe

**"Fenêtre du jeu jamais apparue"**
→ Le jeu ne se lance pas ou met trop de temps
→ Vérifiez les dépendances (DirectX, VC++ Runtime)

**"Timeout lors de X"**
→ L'écran de jeu ne répond pas aux touches
→ Possible bug interface ou IA qui prend le contrôle

---

## 🔧 PERSONNALISATION

### Modifier la durée du combat
Éditez `TEST_RAPIDE_UN_JOUEUR.py` ligne 262:
```python
self.test_gameplay(duration=30)  # Changez 30 pour autre valeur
```

### Ajouter des tests
Créez une nouvelle méthode `test_XXXXX()` dans la classe `QuickTester`

### Changer les touches
Modifiez les listes de touches dans chaque méthode de test

---

## 📝 LOGS & RAPPORTS

**Emplacement:** `D:\KOF Ultimate Online\logs\`

**Format du rapport:**
```
TEST RAPIDE - KOF ULTIMATE ONLINE
==================================================

Date: 2025-10-23 XX:XX:XX
Durée: XXXs
Problèmes: X

PROBLÈMES DÉTECTÉS:
1. [Description du problème]
2. [...]
```

**Fichiers générés:**
- `test_rapide_YYYYMMDD_HHMMSS.txt` - Rapport texte
- `test_multi_YYYYMMDD_HHMMSS.txt` - Rapport multi-joueurs
- `screenshots/` - Captures d'écran (si activé)

---

## 🎯 UTILISATION RECOMMANDÉE

### Développement Quotidien
```bash
LANCER_TEST_RAPIDE.bat
```
→ Vérification rapide avant chaque commit

### Avant Release
```bash
LANCER_TEST_JOUEURS.bat
```
→ Test complet de l'expérience utilisateur

### Après Modification UI
```bash
LANCER_TEST_RAPIDE.bat
```
→ Vérifier que rien n'est cassé

---

## 🐛 DÉPANNAGE

**Le test se bloque:**
- Déplacez la souris dans le coin haut-gauche
- Fermez manuellement le jeu
- Relancez

**PyAutoGUI n'est pas installé:**
```bash
pip install pyautogui
```

**Le jeu ne réagit pas aux touches:**
- Vérifiez la configuration des contrôles
- Assurez-vous que le jeu est en fenêtre active
- Désactivez l'IA auto-play

---

## 💡 CONSEILS

1. **Lancez les tests régulièrement** - Détectez les problèmes tôt
2. **Lisez TOUS les rapports** - Même "0 problèmes" peut cacher des choses
3. **Comparez les durées** - Un test qui devient plus lent = problème potentiel
4. **Testez sur différents PC** - Ce qui marche chez vous peut échouer ailleurs

---

## 🔗 VOIR AUSSI

- `LISEZMOI.md` - Guide général du jeu
- `GUIDE_DEVELOPPEUR.md` - Documentation technique
- `CHANGELOG.md` - Historique des modifications

---

**Dernière mise à jour:** 2025-10-23
**Version:** 1.0
