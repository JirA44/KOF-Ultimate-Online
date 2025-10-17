# 🤖 KOF ULTIMATE - Système d'IAs de Test

## 🎯 Objectif

Faire naviguer et cliquer les IAs **PARTOUT** dans le jeu pour détecter **TOUTES LES ERREURS**.

---

## 🚀 Lancement Rapide

### Méthode Simple (RECOMMANDÉE)
```
Double-cliquez sur: LAUNCH_IAs_COMPLETE.bat
```

Le système lance automatiquement:
1. ✅ Le jeu KOF Ultimate
2. 🤖 3 IAs en parallèle
3. 📊 Le monitoring en temps réel

---

## 🤖 Les 3 IAs

### 1. IA Navigator (`ia_navigator_simple.py`)
**Rôle:** Explorer TOUS les menus

**Actions:**
- ✅ Teste le menu principal (10 options)
- ✅ Navigate dans Options et sous-menus
- ✅ Explore la grille de personnages
- ✅ Fait un stress test (navigation aléatoire)
- ✅ Prend des screenshots de tout

**Durée:** ~10 minutes

### 2. IA Character Tester (`ia_test_all_chars.py`)
**Rôle:** Tester les 189 personnages un par un

**Actions:**
- ✅ Parcourt la grille 20x10
- ✅ Sélectionne chaque personnage
- ✅ Tente de lancer un combat
- ✅ Détecte les crashes
- ✅ Log les erreurs dans `char_test_log.txt`

**Durée:** ~30-40 minutes (189 personnages)

### 3. IA Auto Clicker (`auto_clicker_kof.py`)
**Rôle:** Cliquer en continu pour éviter les freezes

**Actions:**
- ✅ Maintient le jeu actif
- ✅ Clique périodiquement
- ✅ Évite les timeouts

**Durée:** Continu

---

## 📊 Fichiers Générés

### Logs
- `ia_navigator.log` - Log de navigation dans les menus
- `ia_chars.log` - Log des tests de personnages
- `char_test_log.txt` - **Détails complets des tests persos**

### Screenshots
- `ia_screenshots/` - Tous les screenshots (menu, persos, erreurs)
  - `menu_*.png` - Screenshots des menus
  - `char_*.png` - Screenshots de la grille
  - `error_*.png` - Screenshots des erreurs détectées

---

## 📈 Monitoring en Temps Réel

Le batch affiche:
- ⏱️ Heure actuelle
- 📸 Nombre de screenshots pris
- 📄 Derniers logs des tests
- ⚠️ Erreurs détectées (en rouge)

**Rafraîchissement:** Toutes les 10 secondes

---

## ⚠️ Pendant les Tests

### À FAIRE
- ✅ Laisser tourner sans toucher
- ✅ Surveiller le monitoring
- ✅ Consulter les logs

### À NE PAS FAIRE
- ❌ Ne touchez PAS au jeu
- ❌ Ne fermez PAS les fenêtres d'IA
- ❌ Ne bougez PAS la souris pendant les tests

---

## 🐛 Détection d'Erreurs

### Types d'erreurs détectées

1. **Personnages qui crashent**
   - L'IA tente de sélectionner chaque perso
   - Si crash → Screenshot + log

2. **Menus qui freezent**
   - Navigation dans tous les menus
   - Si freeze → Détecté et log

3. **Options manquantes**
   - Exploration exhaustive
   - Si option inaccessible → Log

4. **Sélection de personnages bugguée**
   - Test de la grille complète
   - Si grille cassée → Screenshot

---

## 📋 Rapport Final

Après les tests, consultez:

### 1. `char_test_log.txt`
```
[12:34:56] 🧪 Test personnage #1 (ligne 0, col 0)
[12:34:58] ✅ Personnage #1 OK
[12:35:01] 🧪 Test personnage #2 (ligne 0, col 1)
[12:35:03] ❌ ERREUR personnage #2: Crash détecté
```

### 2. Dossier `ia_screenshots/`
- Regardez les screenshots pour voir exactement ce qui s'est passé
- Les erreurs ont des screenshots `error_*.png`

### 3. Compter les erreurs
```bash
# Dans le dossier du jeu:
type char_test_log.txt | find /c "ERREUR"
```

---

## 🔧 Configuration

### Modifier la durée du stress test
Dans `ia_navigator_simple.py` ligne 244:
```python
self.stress_test_navigation(duration_minutes=2)  # Changez 2 en X minutes
```

### Tester moins de personnages
Dans `ia_test_all_chars.py` ligne 111:
```python
rows = 19  # Changez pour tester moins de lignes
```

### Désactiver une IA
Commentez la ligne dans `LAUNCH_IAs_COMPLETE.bat`:
```batch
REM start "IA Navigator" cmd /c "python ia_navigator_simple.py > ia_navigator.log 2>&1"
```

---

## ✅ Checklist de Vérification

Avant de lancer:
- [ ] Le jeu `KOF BLACK R.exe` existe
- [ ] Python est installé
- [ ] `pyautogui` et `win32gui` sont installés

Après les tests:
- [ ] Consulter `char_test_log.txt`
- [ ] Vérifier `ia_screenshots/`
- [ ] Compter les erreurs
- [ ] Corriger les personnages bugués

---

## 🎮 Lancement Manuel des IAs

Si vous voulez lancer les IAs séparément:

```bash
# Lancer uniquement le navigator
python ia_navigator_simple.py

# Lancer uniquement le testeur de persos
python ia_test_all_chars.py

# Lancer uniquement l'auto-clicker
python auto_clicker_kof.py
```

---

## 📊 Statistiques Attendues

Après un test complet:
- **Actions effectuées:** ~2000-3000
- **Screenshots pris:** ~100-200
- **Personnages testés:** 189
- **Temps total:** 30-45 minutes
- **Erreurs trouvées:** Variable (à corriger!)

---

## 🚨 En Cas de Problème

### Le jeu ne se lance pas
→ Vérifiez le chemin dans les scripts Python

### Les IAs ne cliquent pas
→ Le jeu doit être en fenêtre visible
→ Vérifiez que `pyautogui` est installé

### Trop d'erreurs détectées
→ C'est normal ! C'est le but de trouver TOUTES les erreurs
→ Consultez les logs pour voir lesquelles

---

## 🎯 Prochaines Étapes

Après avoir détecté les erreurs:

1. Consulter `char_test_log.txt`
2. Identifier les personnages cassés
3. Fixer les personnages (fichiers .def, .air, etc.)
4. Re-tester avec les IAs
5. Répéter jusqu'à 0 erreur

**Objectif:** 189/189 personnages ✅

---

## 💡 Conseils

- Lancez les tests le soir et laissez tourner
- Surveillez les logs en temps réel
- Prenez des notes sur les erreurs fréquentes
- Utilisez les screenshots pour debug
- Testez par lots (ex: 50 persos à la fois)

---

**Les IAs vont tout tester pour vous !** 🤖✨
