# 🎮 GUIDE MINI-FENÊTRE - KOF ULTIMATE ONLINE

## 📋 OPTIONS DISPONIBLES

Vous avez **3 façons** de lancer le jeu en mini-fenêtre:

---

## ⭐ OPTION 1: LANCEMENT SIMPLE (RECOMMANDÉ)

**Fichier:** `LANCER_MINI_FENETRE_CONTINUE.bat`

### Ce qu'il fait:
- ✅ Lance le jeu **UNE FOIS** en mini-fenêtre (800x600)
- ✅ La fenêtre reste **VISIBLE** et **ACCESSIBLE**
- ✅ Vous pouvez **JOUER NORMALEMENT**
- ✅ Vous pouvez **DÉPLACER** et **REDIMENSIONNER** la fenêtre
- ✅ Le jeu tourne **EN CONTINU** jusqu'à ce que vous le fermiez

### Comment utiliser:
```batch
Double-cliquer sur: LANCER_MINI_FENETRE_CONTINUE.bat
```

### Quand l'utiliser:
- Pour jouer normalement en mode fenêtré
- Pour garder le jeu visible pendant que vous faites autre chose
- Pour basculer facilement entre le jeu et d'autres programmes (ALT+TAB)

---

## 🔄 OPTION 2: TEST AUTOMATIQUE EN BOUCLE

**Fichier:** `TEST_CONTINU_MINI_VISIBLE.bat`

### Ce qu'il fait:
- ✅ Lance le jeu en **BOUCLE INFINIE**
- ✅ Chaque cycle dure **60 secondes**
- ✅ Ferme et relance automatiquement le jeu
- ✅ Compte les cycles effectués
- ✅ Fenêtre **TOUJOURS VISIBLE** (800x600)

### Comment utiliser:
```batch
Double-cliquer sur: TEST_CONTINU_MINI_VISIBLE.bat
```

### Quand l'utiliser:
- Pour tester la stabilité du jeu
- Pour détecter des bugs qui apparaissent après plusieurs lancements
- Pour stress-tester le système
- Pour surveiller visuellement le comportement du jeu

**⚠️ ATTENTION:** Pour arrêter, fermez la console Windows!

---

## ⚙️ OPTION 3: CONFIGURATION PERSONNALISÉE

**Fichier:** `PLAY_MINI_WINDOW.bat`

### Ce qu'il fait:
- ✅ Lance le jeu en mini-fenêtre **960x720**
- ✅ Affiche des **informations détaillées** sur les contrôles
- ✅ Crée automatiquement un fichier de **RESTAURATION**
- ✅ Sauvegarde la config plein écran

### Comment utiliser:
```batch
Double-cliquer sur: PLAY_MINI_WINDOW.bat
```

### Quand l'utiliser:
- Si vous voulez une fenêtre légèrement plus grande (960x720)
- Si vous avez besoin des infos de contrôles à l'écran
- Si vous voulez un backup automatique de votre config

---

## 📊 COMPARAISON DES OPTIONS

| Caractéristique | Option 1 (Simple) | Option 2 (Boucle) | Option 3 (Perso) |
|----------------|-------------------|-------------------|------------------|
| **Taille fenêtre** | 800x600 | 800x600 | 960x720 |
| **Lancement** | Une fois | En boucle | Une fois |
| **Visibilité** | ✅ Visible | ✅ Visible | ✅ Visible |
| **Durée** | Continue | 60s par cycle | Continue |
| **Backup auto** | ✅ | ✅ | ✅ |
| **Infos contrôles** | ❌ | ❌ | ✅ |
| **Facilité** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

---

## 🎯 QUEL LAUNCHER CHOISIR?

### 🏠 Pour jouer normalement en fenêtré:
→ **LANCER_MINI_FENETRE_CONTINUE.bat** (Option 1)

### 🔬 Pour tester en boucle automatique:
→ **TEST_CONTINU_MINI_VISIBLE.bat** (Option 2)

### ⚙️ Pour une config personnalisée:
→ **PLAY_MINI_WINDOW.bat** (Option 3)

---

## 📐 TAILLES DE FENÊTRE DISPONIBLES

### 800x600 (Options 1 & 2)
- **Avantages:** Compact, facile à positionner, peu gourmand
- **Idéal pour:** Multitâche, tests, surveillance

### 960x720 (Option 3)
- **Avantages:** Plus grand, meilleure visibilité, ratio 4:3
- **Idéal pour:** Jouer sérieusement, voir les détails

### Personnalisé
Pour changer la taille, éditez la ligne dans le .bat:
```python
'width = 800'    # Changer 800 par votre valeur
'height = 600'   # Changer 600 par votre valeur
```

---

## 🔧 FONCTIONNALITÉS COMMUNES

Tous les launchers incluent:

### ✅ Backup Automatique
- Sauvegarde votre config avant modification
- Fichier: `data/mugen.cfg.original_backup`

### ✅ Restauration Facile
- Fichier créé automatiquement: `RESTORE_FULLSCREEN.bat`
- Double-cliquer pour revenir en plein écran

### ✅ Optimisations
- VSync désactivé (réactivité maximale)
- Framerate 60 FPS garanti
- Scripts IA automatiquement arrêtés

### ✅ Compatibilité
- Fonctionne avec M.U.G.E.N
- Fonctionne avec Ikemen GO
- Compatible Windows 7/8/10/11

---

## 🎮 CONTRÔLES (Identiques pour toutes les options)

### Joueur 1 - Clavier
```
Déplacement:  ↑ ↓ ← →
Attaques:     A, S, D, F, G, H
Start:        Entrée
```

### Joueur 1 - Manette
```
Stick/D-Pad:  Déplacement
Boutons:      Selon config DirectInput
Start:        Bouton 8
```

---

## 🔄 RESTAURER LE PLEIN ÉCRAN

### Méthode 1: Automatique
```batch
Double-cliquer sur: RESTORE_FULLSCREEN.bat
```

### Méthode 2: Manuelle
```batch
copy /Y "data\mugen.cfg.original_backup" "data\mugen.cfg"
```

---

## 💡 ASTUCES

### Pour déplacer la fenêtre:
- Cliquer-glisser la barre de titre

### Pour redimensionner:
- Certaines versions M.U.G.E.N permettent le redimensionnement
- Sinon, modifier la config dans le .bat

### Pour garder la fenêtre au premier plan:
- Utiliser un outil comme "Always On Top"
- Ou garder le focus sur la fenêtre

### Pour basculer vers autre chose:
- ALT+TAB fonctionne en mode fenêtré!
- La fenêtre reste en arrière-plan

---

## 🐛 DÉPANNAGE

### La fenêtre est trop petite:
→ Utiliser **PLAY_MINI_WINDOW.bat** (960x720)

### La fenêtre est trop grande:
→ Utiliser **LANCER_MINI_FENETRE_CONTINUE.bat** (800x600)

### Le jeu est en plein écran malgré tout:
1. Fermer le jeu
2. Vérifier `data/mugen.cfg` → `fullscreen = 0`
3. Relancer

### Les tests en boucle ne s'arrêtent pas:
→ Fermer la fenêtre de console (X)

### Je veux revenir en plein écran:
→ Double-cliquer sur **RESTORE_FULLSCREEN.bat**

---

## 📊 STATISTIQUES DE TEST (Option 2 uniquement)

Le fichier `test_cycle_counter.txt` compte les cycles:
```
Nombre de cycles: 42
Temps total: 42 minutes (42 cycles × 60 secondes)
```

Pour réinitialiser le compteur:
```batch
del test_cycle_counter.txt
```

---

## ✅ RÉSUMÉ ULTRA-RAPIDE

### Pour jouer normalement:
```batch
LANCER_MINI_FENETRE_CONTINUE.bat
```

### Pour tester en boucle:
```batch
TEST_CONTINU_MINI_VISIBLE.bat
```

### Pour restaurer plein écran:
```batch
RESTORE_FULLSCREEN.bat
```

**C'est tout!** 🎮

---

*Guide généré le 2025-10-23*
*Tous les launchers testés et fonctionnels*
