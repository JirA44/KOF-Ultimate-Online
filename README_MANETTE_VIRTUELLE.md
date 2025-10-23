# 🎮 Joueurs Virtuels avec Manette Virtuelle

## 🎯 Problème Résolu

**AVANT** : Les joueurs virtuels utilisaient PyAutoGUI qui tapait sur votre CLAVIER réel
- ❌ Impossible d'utiliser votre PC pendant que l'IA joue
- ❌ Les touches s'écrivent dans votre console/éditeur

**MAINTENANT** : Les joueurs virtuels utilisent une MANETTE VIRTUELLE Xbox 360
- ✅ Votre clavier reste 100% libre
- ✅ Vous pouvez taper/travailler normalement
- ✅ Aucune interférence

---

## 📦 Installation

### Étape 1 : Installer vgamepad

**Double-cliquer** sur :
```
INSTALL_MANETTE_VIRTUELLE.bat
```

Ou manuellement dans un terminal :
```bash
pip install vgamepad
```

### Étape 2 : Lancer le système

**Double-cliquer** sur :
```
LAUNCHER_MANETTE.pyw
```

---

## 🎮 Configuration du Jeu

**TRÈS IMPORTANT** : Le jeu doit être configuré pour utiliser une manette !

1. Lancer KOF Ultimate Online
2. Aller dans **Options** > **Controls**
3. Configurer **Player 1** en mode **MANETTE** (pas clavier)
4. Sauvegarder et retourner au menu principal
5. Lancer les joueurs virtuels

### Mapping Manette

Les joueurs virtuels utilisent :

**Boutons** :
- A = Light Punch
- B = Light Kick
- X = Heavy Punch
- Y = Heavy Kick
- START = Menu/Pause

**Directions** :
- D-Pad = Navigation menus
- Stick Gauche = Mouvements combat

---

## 🚀 Utilisation

### Lancer les Joueurs

1. **Double-cliquer** `LAUNCHER_MANETTE.pyw`
2. Choisir le nombre de joueurs (1-5)
3. Choisir la durée (30-999 min)
4. Cliquer **▶️ LANCER**
5. Le dashboard s'ouvre automatiquement

### Vérifier que ça Fonctionne

**Test simple** :
1. Lancer 1 joueur
2. Ouvrir Notepad
3. **Taper du texte** pendant que le joueur joue
4. Aucune lettre bizarre ne devrait apparaître !

Si des lettres apparaissent = le jeu est configuré en clavier, pas en manette

---

## 🔧 Fonctionnement Technique

### Architecture

```
Joueur Virtuel (Python)
        ↓
   vgamepad library
        ↓
Driver Manette Virtuelle Windows
        ↓
   Xbox 360 Controller (virtuel)
        ↓
    KOF Ultimate Online
```

### Avantages vs PyAutoGUI

| PyAutoGUI (clavier) | vgamepad (manette) |
|---------------------|-------------------|
| ❌ Bloque votre clavier | ✅ Clavier libre |
| ❌ Tape dans toutes les apps | ✅ Isolé au jeu |
| ❌ Problèmes de focus | ✅ Pas de focus requis |
| ✅ Simple à utiliser | ⚠️ Nécessite config jeu |

---

## 📊 Fichiers Générés

Même structure que la version clavier :

```
vp_X_gamepad/
└── stats.json
```

---

## ❓ FAQ

### Q: Est-ce que je peux utiliser MA vraie manette en même temps ?

**R:** Non, la manette virtuelle est détectée comme "Player 1". Configurez le jeu pour que Player 2 utilise votre vraie manette si vous voulez jouer contre l'IA.

### Q: Le joueur virtuel ne bouge pas

**R:** Le jeu n'est probablement pas configuré en mode manette. Allez dans Options > Controls et configurez Player 1 en MANETTE.

### Q: Erreur "vgamepad not installed"

**R:** Lancez `INSTALL_MANETTE_VIRTUELLE.bat` ou faites `pip install vgamepad`.

### Q: Puis-je utiliser plusieurs joueurs virtuels ?

**R:** Oui, mais ils partageront tous la même manette virtuelle (Player 1). Pour éviter les conflits, lancez-les avec des délais.

### Q: C'est plus lent que la version clavier ?

**R:** Non, les performances sont identiques. La manette virtuelle est tout aussi rapide.

---

## 🎯 Quand Utiliser Quelle Version ?

### Version MANETTE (`LAUNCHER_MANETTE.pyw`)
✅ Utiliser SI :
- Vous voulez utiliser votre PC pendant que l'IA joue
- Vous tapez beaucoup dans une console/éditeur
- Le jeu supporte les manettes

### Version CLAVIER (`LAUNCHER_SIMPLE.pyw`)
✅ Utiliser SI :
- Le jeu ne supporte PAS les manettes
- Vous ne touchez pas au PC pendant la session
- Plus simple, pas besoin de config manette

---

## 🔄 Migration Clavier → Manette

Si vous utilisiez l'ancienne version clavier :

1. Installer vgamepad : `INSTALL_MANETTE_VIRTUELLE.bat`
2. Configurer le jeu en mode manette
3. Utiliser `LAUNCHER_MANETTE.pyw` au lieu de `LAUNCHER_SIMPLE.pyw`
4. Tout le reste est identique !

---

## 🎉 Profitez de Votre Clavier Libre !

Maintenant vous pouvez :
- ✅ Coder pendant que l'IA joue
- ✅ Écrire des documents
- ✅ Utiliser la console
- ✅ Naviguer sur le web
- ✅ Tout ce que vous voulez !

L'IA joue avec sa propre manette virtuelle en arrière-plan 🎮

---

**Créé avec Claude Code** 🤖
**Solution au problème de clavier partagé** ⌨️➡️🎮
