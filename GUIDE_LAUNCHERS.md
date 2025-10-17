# 🚀 GUIDE DES LAUNCHERS - KOF ULTIMATE ONLINE

## 📋 LAUNCHERS DISPONIBLES

Voici **tous les launchers** disponibles, classés du plus simple au plus avancé.

---

## ⭐ RECOMMANDÉS (UTILISE CES DEUX-LÀ)

### 1. **LAUNCH_WITH_MODE_SELECT.bat** ⭐⭐⭐
**LE PLUS SIMPLE - RECOMMANDÉ POUR JOUER**

```batch
LAUNCH_WITH_MODE_SELECT.bat
```

**Ce qu'il fait:**
- ✓ Menu avec 3 modes de jeu
- ✓ Tue automatiquement les scripts IA
- ✓ Lance directement le jeu

**Les 3 modes:**
1. **Solo vs IA** - Tu joues P1, l'ordinateur joue P2
2. **Versus Local** - 2 joueurs sur le même PC
3. **Netplay** - Jouer en ligne (Ikemen GO)

**Quand l'utiliser:** Pour jouer normalement, tous les jours

---

### 2. **launcher_auto_diagnostic.py** ⭐⭐⭐
**LE PLUS COMPLET - RECOMMANDÉ POUR DIAGNOSTIC**

```batch
python launcher_auto_diagnostic.py
```

**Ce qu'il fait:**
- ✓ **Auto-vérification complète** (M.U.G.E.N, Ikemen GO, AIR files, Character Select)
- ✓ **Auto-correction automatique** des erreurs détectées
- ✓ **Rapport détaillé** avec résumé (errors, warnings, fixes)
- ✓ Choix du moteur (M.U.G.E.N ou Ikemen GO)

**Vérifications automatiques:**
```
📦 Vérification M.U.G.E.N...
✓ KOF_Ultimate_Online.exe: OK
✓ data/ folder: OK
✓ mugen.cfg: OK

📦 Vérification Ikemen GO...
✓ Ikemen_GO.exe: OK
✓ 5 folders (data, font, chars, stages, sound): OK
✓ debug.def: OK

🔍 Vérification fichiers AIR...
✓ Aucune erreur détectée

🎮 Vérification Character Select...
✓ Configuration optimale (14×15, 189 chars)
```

**Quand l'utiliser:**
- Quand tu as des problèmes
- Pour vérifier que tout est OK
- Première utilisation du jeu

---

## 🔧 AUTRES LAUNCHERS (OPTIONNELS)

### 3. **LAUNCH_ULTIMATE_SMART.bat**
**LAUNCHER "INTELLIGENT" (CORRIGÉ)**

```batch
LAUNCH_ULTIMATE_SMART.bat
```

**Ce qu'il fait:**
- ✓ Tue les scripts IA
- ✓ Essaie l'auto-diagnostic (si disponible)
- ✓ Lance le jeu automatiquement
- ✓ Détecte quel exe existe (M.U.G.E.N ou Ikemen GO)

**Quand l'utiliser:** Alternative à LAUNCH_WITH_MODE_SELECT si tu veux un lancement direct

---

### 4. **LAUNCH_CLEAN_GAME.bat**
**LANCEMENT PROPRE SANS IA**

```batch
LAUNCH_CLEAN_GAME.bat
```

**Ce qu'il fait:**
- ✓ Tue tous les scripts Python/IA
- ✓ Lance M.U.G.E.N directement
- ✓ Simple et rapide

**Quand l'utiliser:** Lancement rapide sans menu

---

### 5. **KOF_Ultimate_Online.exe** (Direct)
**LANCEMENT DIRECT M.U.G.E.N**

Double-clic sur l'exe, ou:
```batch
start "" "KOF_Ultimate_Online.exe"
```

**Ce qu'il fait:**
- Lance M.U.G.E.N directement
- Pas de vérifications
- Pas d'auto-correction

**⚠️ Attention:** Si des scripts IA tournent, ils contrôleront P1!

**Quand l'utiliser:** Seulement si tu es sûr qu'aucune IA ne tourne

---

### 6. **Ikemen_GO.exe** (Direct)
**LANCEMENT DIRECT IKEMEN GO**

```batch
cd Ikemen_GO
start "" "Ikemen_GO.exe"
```

**Ce qu'il fait:**
- Lance Ikemen GO directement
- Support netplay
- Pas de vérifications

**Quand l'utiliser:** Pour jouer en ligne (netplay) rapidement

---

## ❌ LAUNCHERS OBSOLÈTES (NE PAS UTILISER)

### ❌ KOF BLACK R.exe
**SUPPRIMÉ - N'EXISTE PLUS**

Ce fichier a été remplacé par `KOF_Ultimate_Online.exe`

### ❌ Anciens scripts auto_repair_system.py / auto_test_system.py
**REMPLACÉS PAR launcher_auto_diagnostic.py**

Ces scripts sont obsolètes, utilise `launcher_auto_diagnostic.py` à la place.

---

## 🎯 QUEL LAUNCHER CHOISIR?

### Pour jouer normalement:
→ **LAUNCH_WITH_MODE_SELECT.bat**

### Si tu as des problèmes:
→ **python launcher_auto_diagnostic.py**

### Pour un lancement rapide sans menu:
→ **LAUNCH_ULTIMATE_SMART.bat** ou **LAUNCH_CLEAN_GAME.bat**

### Pour jouer en ligne (netplay):
→ **LAUNCH_WITH_MODE_SELECT.bat** → Choix 3

---

## 📊 COMPARAISON RAPIDE

| Launcher | Auto-diag | Auto-fix | Menu | Tue IA | Recommandé |
|----------|-----------|----------|------|--------|------------|
| **LAUNCH_WITH_MODE_SELECT.bat** | ❌ | ❌ | ✅ | ✅ | ⭐⭐⭐ |
| **launcher_auto_diagnostic.py** | ✅ | ✅ | ✅ | ❌ | ⭐⭐⭐ |
| LAUNCH_ULTIMATE_SMART.bat | ⚠️ | ❌ | ❌ | ✅ | ⭐⭐ |
| LAUNCH_CLEAN_GAME.bat | ❌ | ❌ | ❌ | ✅ | ⭐ |
| KOF_Ultimate_Online.exe | ❌ | ❌ | ❌ | ❌ | ⭐ |
| Ikemen_GO.exe | ❌ | ❌ | ❌ | ❌ | ⭐ |

**Légende:**
- ⭐⭐⭐ = Fortement recommandé
- ⭐⭐ = Recommandé
- ⭐ = Utilisable mais basique

---

## 🛠️ DÉPANNAGE

### Problème: "L'IA contrôle P1"
**Solution:** Utilise un launcher qui tue les IA:
- LAUNCH_WITH_MODE_SELECT.bat
- LAUNCH_ULTIMATE_SMART.bat
- LAUNCH_CLEAN_GAME.bat

### Problème: "Character select bugué"
**Solution:** Lance:
```batch
python APPLY_OPTIMAL_CHAR_SELECT.py
```
Puis relance le jeu.

### Problème: "Ikemen GO ne se lance pas"
**Solution:** Lance:
```batch
python launcher_auto_diagnostic.py
```
Il réparera automatiquement les folders Ikemen GO.

### Problème: "Erreurs dans les logs AIR"
**Solution:** Lance:
```batch
python launcher_auto_diagnostic.py
```
Il corrigera automatiquement les erreurs CLSN2.

---

## 📝 RÉSUMÉ ULTRA-RAPIDE

**Pour 99% des cas:**
```batch
LAUNCH_WITH_MODE_SELECT.bat
```

**Si ça ne marche pas:**
```batch
python launcher_auto_diagnostic.py
```

**C'est tout!** 🎮

---

## 📂 FICHIERS CRÉÉS RÉCEMMENT

### Scripts de diagnostic:
- `ANALYZE_CHAR_SELECT.py` - Analyse character select
- `APPLY_OPTIMAL_CHAR_SELECT.py` - Applique config optimale
- `FIX_IKEMEN_FORCE.ps1` - Répare Ikemen GO folders

### Documentation:
- `COMMENT_JOUER.md` - Guide complet du jeu
- `CORRECTIONS_APPLIQUEES.md` - Détails techniques des corrections
- `RAPPORT_FINAL_2025-10-17.md` - Rapport final complet
- `GUIDE_LAUNCHERS.md` - Ce fichier

---

## 🎉 TOUT EST PRÊT!

Tous les launchers sont configurés et fonctionnels.

**Lance simplement:**
```batch
LAUNCH_WITH_MODE_SELECT.bat
```

**Et joue! 🎮🔥**

---

*Dernière mise à jour: 2025-10-17*
*Tous les launchers ont été testés et fonctionnent correctement!*
