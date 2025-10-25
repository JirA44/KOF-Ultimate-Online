# 🤖 TESTS AUTOMATIQUES EN COURS

**Date de lancement:** 2025-10-25
**Status:** ✅ EN COURS

---

## 🎮 CE QUI TOURNE ACTUELLEMENT

### Test IA vs IA (ACTIF)

**Script:** `AUTO_TEST_IA_VS_IA.py`
**Status:** 🟢 EN COURS

**Ce qu'il fait:**
- ✅ Sélectionne 2 personnages aléatoires
- ✅ Lance un combat IA vs IA
- ✅ Détecte automatiquement les crashes
- ✅ Identifie les personnages problématiques
- ✅ Génère un rapport en temps réel

**Durée par combat:** 60 secondes max
**Pause entre combats:** 3 secondes

**Fichiers générés:**
- `test_ia_results.json` - Résultats détaillés (mis à jour en temps réel)
- `auto_test_ia_vs_ia.log` - Log complet de tous les tests

---

## 📊 SUIVRE LES RÉSULTATS

### Option 1: Consulter le fichier JSON

```bash
notepad test_ia_results.json
```

**Contient:**
```json
{
  "total_combats": 145,
  "total_crashes": 23,
  "characters_tested": {
    "Athena": {
      "total_combats": 15,
      "crashes": 0,
      "successes": 15
    },
    "Drakyola": {
      "total_combats": 8,
      "crashes": 8,
      "successes": 0
    }
  },
  "crashes": [...],
  "problematic_chars": [...]
}
```

### Option 2: Lire le log en temps réel

```bash
notepad auto_test_ia_vs_ia.log
```

**Format:**
```
[12:34:56] 🤖 Combat: Athena vs Kyo
[12:35:01]   ✅ Combat terminé sans crash
[12:35:05] 🤖 Combat: Drakyola vs Mai
[12:35:10]   ❌ Crash au démarrage
[12:35:15] 📊 Combat #145 | Crashes: 23 (15.8%)
```

### Option 3: Python script de monitoring

```python
import json

with open('test_ia_results.json') as f:
    data = json.load(f)

print(f"Total: {data['total_combats']} combats")
print(f"Crashes: {data['total_crashes']} ({data['total_crashes']/data['total_combats']*100:.1f}%)")

# Top personnages problématiques
for char, stats in sorted(data['characters_tested'].items(),
                          key=lambda x: x[1]['crashes'],
                          reverse=True)[:10]:
    if stats['crashes'] > 0:
        print(f"{char}: {stats['crashes']} crashes")
```

---

## 🛑 ARRÊTER LES TESTS

### Méthode 1: Ctrl+C dans la fenêtre du script

Si vous voyez la fenêtre "Test IA vs IA", appuyez sur `Ctrl+C`.
→ Génère automatiquement un rapport final.

### Méthode 2: Tuer le processus Python

```bash
taskkill /F /IM python.exe
```

⚠️ **Note:** Cette méthode force l'arrêt, le rapport final ne sera pas généré.

### Méthode 3: Script d'arrêt

```batch
@echo off
tasklist | findstr python.exe
taskkill /F /IM python.exe
echo Tests arrêtés.
pause
```

---

## 📈 RAPPORT EN TEMPS RÉEL

Le script génère automatiquement:

### Toutes les 10 combats

```
🔍 Top 5 personnages problématiques:
   ⚠️  Drakyola: 8 crashes (100%)
   ⚠️  Kasim_LV2-CKOFM: 6 crashes (75%)
   ⚠️  Aika_MK: 4 crashes (50%)
```

### À la fin (Ctrl+C)

```
📊 RAPPORT FINAL
═══════════════════════════════════════════════════════════
Total combats: 150
Crashes: 25
Taux de crash: 16.7%

❌ TOP 10 PERSONNAGES PROBLÉMATIQUES:
1. Drakyola: 10/10 crashes (100%)
2. Kasim_LV2-CKOFM: 8/12 crashes (67%)
3. Aika_MK: 5/8 crashes (63%)
4. Aileen: 3/6 crashes (50%)
...
```

---

## 🎯 OBJECTIF

**Identifier TOUS les personnages qui crashent en combat réel.**

Contrairement à `TEST_ALL_CHARACTERS.py` qui teste juste le chargement des fichiers,
ce test lance de **vrais combats** pour détecter:

- ❌ Crashes au démarrage du combat
- ❌ Crashes pendant le combat
- ❌ Erreurs CLSN dans les animations
- ❌ Problèmes de sprites/sounds
- ❌ Incompatibilités entre personnages

---

## 📁 FICHIERS CRÉÉS

```
D:\KOF Ultimate Online\
│
├── AUTO_TEST_IA_VS_IA.py              ← Script principal
├── LANCER_TEST_IA_CONTINU.bat         ← Launcher
│
├── test_ia_results.json               ← Résultats (mis à jour en temps réel)
├── auto_test_ia_vs_ia.log             ← Log complet
└── test_ia_output.log                 ← Output console
```

---

## ⚙️ CONFIGURATION

Vous pouvez modifier ces paramètres dans `AUTO_TEST_IA_VS_IA.py`:

```python
COMBAT_DURATION = 60        # Durée max par combat (secondes)
PAUSE_BETWEEN_COMBATS = 3   # Pause entre combats (secondes)
```

**Recommandations:**
- `COMBAT_DURATION = 60` → Détection fiable des crashes pendant combat
- `COMBAT_DURATION = 30` → Tests plus rapides mais peut rater certains crashes tardifs
- `PAUSE_BETWEEN_COMBATS = 3` → Laisse le temps au système de se stabiliser

---

## 🔍 ANALYSE DES RÉSULTATS

### Personnages à désactiver

Critère: **Crash rate > 50% après 5+ combats**

```python
import json

with open('test_ia_results.json') as f:
    data = json.load(f)

to_disable = []
for char, stats in data['characters_tested'].items():
    if stats['total_combats'] >= 5:
        crash_rate = stats['crashes'] / stats['total_combats']
        if crash_rate > 0.5:
            to_disable.append((char, crash_rate, stats['crashes']))

print("Personnages à désactiver:")
for char, rate, crashes in sorted(to_disable, key=lambda x: x[1], reverse=True):
    print(f"  {char}: {crashes} crashes ({rate*100:.0f}%)")
```

### Paires problématiques

Certains personnages peuvent crasher seulement contre certains adversaires:

```python
# Analyser test_ia_results.json > crashes
# Chercher si certaines paires reviennent souvent
```

---

## 🎓 APPRENTISSAGE

Au fur et à mesure des tests, le système apprend:

✅ **Personnages stables** → Peuvent être utilisés en production
⚠️ **Personnages instables** → À réparer ou désactiver
❌ **Personnages cassés** → À désactiver immédiatement

---

## 💡 PROCHAINES ÉTAPES

Après les tests automatiques:

1. **Analyser `test_ia_results.json`**
2. **Identifier les personnages > 50% crash rate**
3. **Désactiver ces personnages dans `select.def`**
4. **Relancer les tests** pour vérifier stabilité
5. **Répéter** jusqu'à taux de crash < 5%

---

## 📞 COMMANDES UTILES

### Voir combien de combats ont été faits

```batch
findstr "Combat #" auto_test_ia_vs_ia.log | find /C "#"
```

### Voir tous les crashes

```batch
findstr "❌ Crash" auto_test_ia_vs_ia.log
```

### Compter les crashes

```batch
findstr "❌ Crash" auto_test_ia_vs_ia.log | find /C "❌"
```

### Tail -f équivalent (Windows)

```powershell
Get-Content auto_test_ia_vs_ia.log -Wait -Tail 20
```

---

## ✅ AVANTAGES DE CE SYSTÈME

vs `TEST_ALL_CHARACTERS.py`:

| Feature | TEST_ALL_CHARACTERS | AUTO_TEST_IA_VS_IA |
|---------|--------------------|--------------------|
| Teste chargement fichiers | ✅ | ✅ |
| Teste combat réel | ❌ | ✅ |
| Détecte crashes CLSN | ❌ | ✅ |
| Détecte incompatibilités | ❌ | ✅ |
| Mode automatique | ✅ | ✅ |
| Rapport en temps réel | ✅ | ✅ |
| Identifie paires problématiques | ❌ | ✅ |

---

**Le système tourne en arrière-plan, vous pouvez continuer à travailler normalement!**

**Consultez `test_ia_results.json` quand vous voulez pour voir les résultats.**
