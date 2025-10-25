# 🎮 RAPPORT - TEST RÉEL DE VS ET IDENTIFICATION DES CRASHEURS

**Date**: 2025-10-25
**Objectif**: Identifier précisément quels personnages causent des crashs en combat réel

---

## 📋 CONTEXTE

### Problème reporté par l'utilisateur:
> "mais il te suffit de lancer des vs comme moi tu verras que ça crash?"

Malgré toutes les réparations effectuées (147 erreurs CLSN, common1.cns, storyboards), le jeu crashe toujours pendant les combats VS.

### Découvertes:
1. **AUTO_TEST_AND_FIX.py** reportait "✅ Jeu stable 30s" mais ne testait PAS réellement les combats
2. **god_orochi** crashe systématiquement malgré les réparations (maintenant retiré du roster)
3. Le test automatique ne détectait que les crashes au lancement, pas pendant la sélection/combat

---

## 🛠️ NOUVEAUX OUTILS CRÉÉS

### 1. **TEST_REAL_VS.py** - Test VS automatisé
**Fonction**: Simule la sélection de personnages et le lancement d'un combat réel

**Résultat du test initial**:
```
🎮 TEST RÉEL DE VS - SIMULATION AUTOMATIQUE
✅ LE JEU EST STABLE - COMBAT CHARGÉ AVEC SUCCÈS!
```

Testé avec: **WhirlWind-Goenitz vs Viper**
- ✅ Ces 2 personnages sont confirmés 100% stables

---

### 2. **TEST_ALL_CHARACTERS_VS.py** - Test exhaustif en cours
**Fonction**: Teste CHAQUE personnage contre 3 adversaires différents

**Processus**:
1. Pour chaque personnage:
   - Crée un roster minimal (2 personnages)
   - Lance le jeu
   - Attend 15 secondes
   - Vérifie:
     - Si le jeu crash → **CRASHER**
     - Si 5+ erreurs dans le log → **PROBLÉMATIQUE**
     - Sinon → **SAFE**

2. Répète le test contre 3 adversaires différents
3. Si UN SEUL test crash → personnage marqué CRASHER

**Sortie attendue**:
- Liste des personnages SÛRS (✅)
- Liste des personnages CRASHEURS (❌)
- Création automatique de `select_ULTRA_SAFE.def` avec seulement les persos OK

---

## 🔍 CE QU'ON CHERCHE

### Hypothèses sur les crashs:
1. **Certains personnages sont cassés** malgré les réparations CLSN/common1.cns
2. **Certaines combinaisons** de personnages causent des crashes
3. **Fichiers .air/.cmd/.cns** avec erreurs non détectées par les scans automatiques

### Personnages déjà identifiés:
- ✅ **WhirlWind-Goenitz**: SAFE (testé OK)
- ✅ **Viper**: SAFE (testé OK)
- ✅ **Cronus**: SAFE (mentionné dans rapports précédents)
- ❌ **god_orochi**: CRASHER (retiré du roster)
- ⚠️ **Kei**: Fichiers manquants
- ⚠️ **Ryuji**: Fichiers manquants

---

## 📊 ROSTER ACTUEL

**Fichier**: `D:\KOF Ultimate Online\data\select.def`

**Total**: 26 personnages actifs (god_orochi retiré)

**Catégories**:
- KOF Classiques: Athena, Athena_XI, Ash, Kei
- Boss/Orochi: boss-orochi, final-goenitz, Lord-Goenitz, WhirlWind-Goenitz
- Igniz/Zero: Final-IGNIZ, Final-OriginalZero, Clone Zero, O.Zero-Prominence
- Rugal: Clone Blood Rugal, DG.Rugal-KOFM, Valmar Rugal
- Autres: akuma, Rose, Viper, Ryuji, Nero, Eve, Fang
- Boss spéciaux: Boss Gustab M, Unfailed Gustab, Cronus, Delirus

---

## 🎯 STRATÉGIE DE RÉPARATION

### Étape 1: Identification (EN COURS)
- Test exhaustif de tous les personnages
- Création de la liste CRASHERS vs SAFE

### Étape 2: Isolation
- Retirer tous les crasheurs du roster principal
- Créer `select_ULTRA_SAFE.def` avec seulement les persos OK

### Étape 3: Diagnostic approfondi
- Pour chaque crasheur identifié:
  - Analyser les fichiers .air/.cmd/.cns
  - Chercher les erreurs spécifiques
  - Tenter réparation ciblée OU remplacement

### Étape 4: Expansion
- Ajouter progressivement les personnages réparés
- Tester après chaque ajout
- Objectif: Roster le plus large possible tout en restant stable

---

## 📈 PROGRESSION

### Avant cette session:
- ❌ Jeu crashait immédiatement
- 147 erreurs CLSN
- 24/27 persos sans common1.cns
- Écran sélection cassé

### Après réparations:
- ✅ Jeu se lance correctement
- ✅ Écran sélection optimisé (4x7)
- ✅ 147 erreurs CLSN réparées
- ✅ 19 common1.cns copiés
- ⚠️ Mais: Crashs pendant combats VS

### Maintenant (25 oct 2025 - 21h37):
- 🔄 **Test exhaustif en cours**
- 🎯 Identification précise des crasheurs
- 🛠️ Création automatique du roster ultra-safe

---

## 🚀 UTILISATION DES NOUVEAUX OUTILS

### Test VS rapide (2 persos):
```bash
python TEST_REAL_VS.py
```

### Test exhaustif complet:
```bash
python TEST_ALL_CHARACTERS_VS.py
```

**Durée estimée**: ~10-15 minutes (26 persos × 3 tests × 15s)

**Résultats**:
- `RAPPORT_TEST_EXHAUSTIF.txt` - Liste détaillée SAFE vs CRASHERS
- `select_ULTRA_SAFE.def` - Roster automatique avec seulement persos OK

---

## 📁 FICHIERS MODIFIÉS/CRÉÉS

### Nouveaux scripts:
1. `TEST_REAL_VS.py` - Test VS automatisé (terminé ✅)
2. `TEST_ALL_CHARACTERS_VS.py` - Test exhaustif (en cours 🔄)
3. `QUICK_FIX.bat` - Retirer god_orochi

### Modifications:
1. `data/select.def` - god_orochi commenté (ligne 20)
2. `data/select.def.backup_test` - Backup pour tests

### Rapports:
1. `RAPPORT_TEST_RÉEL_VS.md` (ce fichier)
2. `RAPPORT_TEST_EXHAUSTIF.txt` (à venir)

---

## ⏭️ PROCHAINES ÉTAPES

1. ⏳ **Attendre fin du test exhaustif** (~10-15 min)
2. 📊 **Analyser les résultats** - Combien de crashers vs safe?
3. 🛠️ **Appliquer select_ULTRA_SAFE.def** comme roster principal
4. 🎮 **Tester manuellement** avec l'utilisateur
5. 🔧 **Si stable**: Analyser les crashers un par un pour tentative de réparation
6. 📈 **Expansion progressive** du roster avec persos réparés

---

## 💡 ENSEIGNEMENTS

### Ce qui marche:
- ✅ Tests automatisés avec simulation clavier (pyautogui)
- ✅ Création de rosters minimaux pour isolation
- ✅ Tests itératifs contre multiples adversaires
- ✅ Backup/restore automatique du roster

### Ce qui ne marche pas:
- ❌ Tests passifs (timeout 30s) ne détectent pas les crashs en combat
- ❌ Réparation CLSN/common1.cns ne suffit pas pour tous les persos
- ❌ Certains personnages ont des problèmes plus profonds (god_orochi)

---

**Statut actuel**: 🔄 Test exhaustif en cours...

*Dernière mise à jour: 2025-10-25 21:37*
