# 🎯 TESTS AUTOMATIQUES SANS INTERFÉRENCES

## ✅ SOLUTION PARFAITE : INJECTION D'INPUTS

### Comment ça marche ?

Au lieu d'utiliser `pyautogui` qui envoie des touches **globales** à tout Windows, le nouveau système utilise **Windows Messages** pour envoyer les inputs **directement au processus du jeu**.

**Technologie utilisée :**
- `win32api.SendMessage()` avec `WM_KEYDOWN`/`WM_KEYUP`
- Ciblage du handle de fenêtre (`HWND`) du jeu uniquement
- Aucune interaction avec les autres processus

---

## 🚀 UTILISATION

### Lancer le test automatique sans interférences

```bash
# Double-cliquez sur :
LANCER_TEST_INJECTION.bat
```

**Ou en ligne de commande :**
```bash
cd "D:\KOF Ultimate Online"
python test_input_injection.py
```

---

## ✅ AVANTAGES

| Critère | Injection d'inputs | PyAutoGUI | Test manuel |
|---------|-------------------|-----------|-------------|
| **Affecte autres fenêtres** | ❌ Non | ✅ Oui | ❌ Non |
| **Automatique** | ✅ Oui | ✅ Oui | ❌ Non |
| **Vous pouvez travailler** | ✅ Oui | ❌ Non | ❌ Non |
| **Fiabilité** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Setup** | pip install pywin32 | pip install pyautogui | Aucun |

---

## 🎯 CE QUI EST TESTÉ

Le test avec injection d'inputs effectue **7 tests** :

1. **Lancement du jeu** (3-5s)
   - Démarre le processus
   - Trouve la fenêtre du jeu
   - Récupère le handle (HWND)

2. **Écran titre** (10s)
   - Attend l'écran titre
   - Envoie ESPACE → Menu principal

3. **Navigation menus** (15s)
   - Parcourt les 7 options du menu
   - BAS ×7 puis HAUT ×7

4. **Mode Versus** (5s)
   - Sélectionne "Versus"
   - Entre dans la sélection de personnages

5. **Sélection personnage** (10s)
   - Navigue dans la grille
   - Sélectionne un personnage

6. **Gameplay** (30s)
   - Combat avec inputs aléatoires
   - ~60-80 actions effectuées

7. **Pause & sortie** (5s)
   - ESCAPE → Menu pause
   - Sortie du match

**Durée totale :** ~90 secondes (1.5 min)

---

## 📊 RÉSULTATS

Les résultats sont sauvegardés dans :
```
logs/test_injection_YYYYMMDD_HHMMSS.txt
```

**Exemple de rapport :**
```
TEST AVEC INJECTION D'INPUTS - KOF ULTIMATE ONLINE
============================================================

Date: 2025-10-23 10:50:00
Durée: 87.3s
Problèmes: 0

✅ Aucun problème détecté
```

---

## 🔧 COMMENT ÇA MARCHE TECHNIQUEMENT

### 1. Trouver la fenêtre du jeu

```python
def find_game_window(self):
    def callback(hwnd, windows):
        title = win32gui.GetWindowText(hwnd)
        if "KOF" in title or "Ikemen" in title:
            windows.append(hwnd)

    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows[0] if windows else None
```

### 2. Envoyer une touche

```python
def send_key(self, key):
    vk_code = VK_CODES[key]  # Virtual Key Code

    # WM_KEYDOWN
    lparam_down = win32api.MapVirtualKey(vk_code, 0) << 16 | 1
    win32api.SendMessage(self.game_hwnd, win32con.WM_KEYDOWN,
                        vk_code, lparam_down)

    time.sleep(0.1)

    # WM_KEYUP
    lparam_up = lparam_down | (0x3 << 30)
    win32api.SendMessage(self.game_hwnd, win32con.WM_KEYUP,
                        vk_code, lparam_up)
```

### 3. Mapping des touches

```python
VK_CODES = {
    'space': win32con.VK_SPACE,      # START
    'return': win32con.VK_RETURN,    # Sélection
    'escape': win32con.VK_ESCAPE,    # Pause
    'up': win32con.VK_UP,
    'down': win32con.VK_DOWN,
    'left': win32con.VK_LEFT,
    'right': win32con.VK_RIGHT,
    'a': ord('A'),  # Attaque faible
    's': ord('S'),  # Attaque moyenne
    'z': ord('Z'),  # Attaque forte
    'x': ord('X'),  # Spécial
}
```

---

## 🐛 DÉPANNAGE

### "pywin32 non installé"

```bash
pip install pywin32
```

### "Fenêtre du jeu non trouvée"

Le script cherche ces mots-clés dans le titre :
- "KOF"
- "Ikemen"
- "MUGEN"
- "AI Navigator"

Si votre jeu a un titre différent, modifiez la fonction `find_game_window()` :

```python
if any(keyword in title for keyword in ["Votre", "Titre", "Ici"]):
```

### "Touches ne fonctionnent pas"

Certains jeux utilisent DirectInput au lieu de Windows Messages. Dans ce cas :
1. Vérifiez que le jeu accepte les inputs clavier (pas seulement manette)
2. Essayez le test manuel guidé à la place
3. Contactez le support

---

## 💡 CONSEILS

### Pendant le développement

Utilisez ce test après chaque modification importante :
```bash
LANCER_TEST_INJECTION.bat
```

Vous pouvez continuer à coder pendant que le test tourne ! 👍

### Avant un commit

```bash
# Terminal 1 : Test auto
python test_input_injection.py

# Terminal 2 : Vous continuez à bosser
git add .
git commit -m "..."
```

### CI/CD

Ajoutez ce test à votre pipeline :
```yaml
- name: Test UX automatique
  run: python test_input_injection.py
  timeout-minutes: 3
```

---

## 📌 COMPARAISON DES MÉTHODES

### ⭐ Test Injection (RECOMMANDÉ pour auto)

```bash
LANCER_TEST_INJECTION.bat
```

- ✅ Automatique
- ✅ N'affecte pas vos fenêtres
- ✅ Fiable
- ✅ Rapide (90s)
- ⚠️ Nécessite pywin32

### Test Manuel Guidé (RECOMMANDÉ pour apprentissage)

```bash
LANCER_TEST_MANUEL.bat
```

- ✅ Aucune dépendance
- ✅ Bon pour apprendre
- ✅ Contrôle total
- ⚠️ Demande votre temps (3 min)

### ❌ Test PyAutoGUI (À ÉVITER)

```bash
LANCER_TEST_RAPIDE.bat
```

- ⚠️ Affecte toutes vos fenêtres
- ⚠️ Frappes clavier globales
- ❌ Ne pas utiliser pendant le travail

---

## 🎯 RECOMMANDATION FINALE

**Pour les tests automatiques réguliers :**
```bash
LANCER_TEST_INJECTION.bat
```

C'est la meilleure solution pour tester sans être dérangé ! 🚀

---

## 📝 NOTES TECHNIQUES

### Limitations connues

1. **Jeux en fullscreen exclusif**
   - Certains jeux bloquent `SendMessage`
   - Solution : Lancer en mode fenêtré

2. **Anti-cheat / Protection**
   - Certains anti-cheats détectent `SendMessage`
   - Pas un problème pour ce jeu

3. **Timing des inputs**
   - Peut être légèrement différent des vraies frappes
   - Ajustez les `time.sleep()` si nécessaire

### Améliorations possibles

- [ ] Support DirectInput si Windows Messages ne marche pas
- [ ] Enregistrement vidéo du test
- [ ] Captures d'écran à chaque étape
- [ ] Détection automatique de bugs visuels
- [ ] Tests de performance (FPS, input lag)

---

**Dernière mise à jour :** 2025-10-23
**Version :** 2.0 - Injection d'inputs
