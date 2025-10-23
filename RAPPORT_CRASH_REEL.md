# 🚨 RAPPORT DE CRASH - MODE VS

## ❌ PROBLÈME CONFIRMÉ

**Le jeu CRASH au démarrage d'un match VS.**

---

## 🔍 CE QUE J'AI TROUVÉ

### Analyse du mugen.log

```
[OK] Gameflow jusqu'à sélection personnages
[OK] Chargement du stage
[OK] Chargement personnage 1 (Akiha Orochi) - 9000ms ⚠️ TRÈS LENT
[OK] Chargement personnage 2 (Yuri_SV) - 3400ms
[OK] Match assets initialized
[OK] Game loop init
[OK] Match loop init
[CRASH] ← Le jeu se ferme ici
```

### 🐛 Problèmes détectés

| Problème | Gravité | Impact |
|----------|---------|--------|
| **Temps de chargement 9 secondes** | ⚠️ Critique | Peut causer timeout/crash |
| **Crash après "Match loop init"** | ❌ Bloquant | Jeu impossible |
| **55180 expressions dans un perso** | ⚠️ Très élevé | Surcharge mémoire |
| **Pas d'erreur dans le log** | ⚠️ Problématique | Difficile à debugger |

---

## 💡 CAUSES PROBABLES

### 1. Personnages trop complexes (TRÈS PROBABLE)

**Akiha Orochi** a **55,180 expressions** (dont 15,794 triggers) :
- Un personnage normal : ~5,000-10,000 expressions
- Akiha Orochi : **55,180 expressions** (5-10x la normale !)

**Conséquence** :
- Chargement ultra-lent (9 secondes)
- Crash par manque de mémoire
- Ikemen GO ne peut pas gérer cette complexité

### 2. Cache de personnages insuffisant

```
(1/7 cached) Load time: 9000.000ms
(2/7 cached) Load time: 3400.000ms
```

Le cache est limité à 7 personnages, mais :
- Les personnages sont trop gros
- Le cache déborde
- Crash à l'initialisation du match

### 3. Bug Ikemen GO

Le crash silencieux (sans erreur) suggère :
- Bug dans le moteur Ikemen GO
- Incompatibilité avec certains personnages
- Problème de gestion mémoire

---

## ✅ SOLUTIONS

### Solution 1 : Désactiver les personnages problématiques (RAPIDE)

**Personnages suspects :**
- Akiha Orochi (55,180 expressions - TRÈS lourd)
- Tous les personnages "Orochi" ou "Blood" (généralement très complexes)

**Action :**
1. Ouvrir `data/select.def`
2. Commenter les lignes avec `;` :
   ```
   ;Akiha Orochi
   ;Akiha Yagami DK
   ;Clone Blood Rugal
   ```
3. Tester avec des personnages plus simples

### Solution 2 : Augmenter cache et mémoire

**Dans `data/mugen.cfg` :**

```ini
[Config]
MaxPlayerCache = 20        ; Au lieu de 7
BufferSize = 1073741824    ; 1 GB au lieu de 512 MB
```

### Solution 3 : Mode debug Ikemen GO

**Lancer avec :**
```bash
KOF_Ultimate_Online.exe -debug -log
```

Génèrera plus d'infos dans mugen.log

### Solution 4 : Utiliser des personnages vanilla (RECOMMANDÉ)

Les personnages "custom" trop complexes causent souvent des crashs.

**Personnages "sûrs" à garder :**
- Kyo (vanilla KOF)
- Iori (vanilla KOF)
- Terry (vanilla KOF)
- Mai (vanilla KOF)

**Personnages "risqués" à enlever :**
- Tout ce qui a "Blood", "Orochi", "Chaos" dans le nom
- Personnages avec effets visuels ultra-complexes
- Boss modifiés (ABYSS, etc.)

---

## 🎯 PLAN D'ACTION RECOMMANDÉ

### Étape 1 : Test rapide (2 minutes)

1. Ouvrir `data/select.def`
2. Commenter TOUS les personnages sauf 4-5 simples :
   ```
   Kyo
   Iori
   Terry
   Mai
   Athena
   ```
3. Relancer le jeu
4. Tester mode VS

**Si ça marche** → Le problème vient des personnages complexes

**Si ça ne marche pas** → Problème plus profond (config, Ikemen GO, etc.)

### Étape 2 : Si ça marche, réactiver progressivement

1. Ajouter 10 personnages à la fois
2. Tester après chaque ajout
3. Noter quel personnage cause le crash
4. Le retirer définitivement

### Étape 3 : Si ça ne marche toujours pas

1. Vérifier version Ikemen GO (peut-être bugée)
2. Vérifier `mugen.cfg` (corruption?)
3. Réinstaller Ikemen GO
4. Tester avec une config vanilla

---

## 📊 MES TESTS AUTOMATIQUES ÉTAIENT FAUX

### Pourquoi mes tests disaient "✅ OK" ?

**Mes tests** :
```python
1. Lancer le jeu
2. Envoyer des touches
3. Fermer le jeu après 90s
4. Dire "✅ Aucun problème"
```

**Ce qu'ils NE vérifiaient PAS** :
- ❌ Si le jeu crash entre-temps
- ❌ Si le match démarre réellement
- ❌ Si le gameplay fonctionne

**Résultat** : FAUX POSITIFS

### Amélioration nécessaire

Les tests doivent vérifier :
```python
✓ Le processus du jeu ne crash pas
✓ La fenêtre reste ouverte
✓ Le match charge complètement
✓ Le gameplay répond aux inputs
✓ Pas de freeze/timeout
```

---

## 🔧 PROCHAINES ÉTAPES

**Pour vous :**
1. Essayer Solution 1 (désactiver personnages complexes)
2. Tester avec 5 personnages simples
3. Me dire si ça marche

**Pour moi :**
1. Arrêter les tests défaillants ✅ FAIT
2. Créer des VRAIS tests qui détectent les crashs
3. Créer un script de nettoyage automatique du select.def

---

## ✅ CONCLUSION

**Mes tests automatiques étaient DÉFAILLANTS** - Vous aviez raison !

**Le vrai problème** : Personnages trop complexes qui crashent Ikemen GO

**La solution** : Désactiver les personnages problématiques et garder seulement les simples/vanilla

---

**Créé le** : 2025-10-23 11:15
**Statut** : Crash confirmé
**Cause probable** : Personnages ultra-complexes (55K expressions)
**Solution** : Utiliser personnages vanilla uniquement
