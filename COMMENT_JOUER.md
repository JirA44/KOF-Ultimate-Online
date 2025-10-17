# 🎮 KOF ULTIMATE - GUIDE RAPIDE

## 🚀 Lancement Rapide

### Double-clique sur: **`LAUNCH_WITH_MODE_SELECT.bat`**

Ce launcher te donne 3 options:

---

## 📋 Modes de Jeu

### 1️⃣ Solo vs IA (Mode Normal)
**Tu joues contre l'ordinateur**

- **Moteur**: M.U.G.E.N
- **P1**: TOI (clavier ou manette)
- **P2**: IA du jeu
- **Utilise**: `LAUNCH_WITH_MODE_SELECT.bat` → Choix 1

**Contrôles P1 (Clavier par défaut):**
- Flèches: Déplacement
- A: Coup faible
- S: Coup moyen
- D: Coup fort
- Z: Super 1
- X: Super 2
- C: Super 3

**Ou Manette 1 (auto-détectée)**

---

### 2️⃣ Versus Local (2 Joueurs même PC)
**Toi + un ami sur le même ordinateur**

- **Moteur**: M.U.G.E.N
- **P1**: Joueur 1 (clavier ou manette 1)
- **P2**: Joueur 2 (clavier 2 ou manette 2)
- **Utilise**: `LAUNCH_WITH_MODE_SELECT.bat` → Choix 2

**Contrôles P2 (Clavier):**
- E/R/T/Y: Déplacement
- T: Coup faible
- U: Coup moyen
- O: Coup fort
- Y: Super 1
- P: Super 2
- L: Super 3

**Ou Manette 2**

---

### 3️⃣ Netplay (En Ligne)
**Jouer contre quelqu'un sur internet**

- **Moteur**: Ikemen GO (avec support netplay)
- **P1**: TOI
- **P2**: Joueur distant (internet)
- **Utilise**: `LAUNCH_WITH_MODE_SELECT.bat` → Choix 3

**Dans le menu Ikemen GO:**
1. Choisis **"Network"**
2. **"Host Game"** (créer une partie) ou **"Join Game"** (rejoindre)
3. Si Host: Partage ton IP à ton ami
4. Si Join: Entre l'IP de ton ami
5. Attendez la connexion
6. Sélectionnez vos personnages
7. Combat!

**Note**: Il faut que l'un de vous deux ouvre le port (par défaut 7500) sur son routeur.

---

## ⚠️ IMPORTANT

### Si l'IA contrôle P1 automatiquement:

**Problème**: Des scripts Python d'IA tournent en arrière-plan.

**Solution**:
1. Ferme le jeu
2. Lance: `LAUNCH_WITH_MODE_SELECT.bat`
3. Le script tue automatiquement les IA externes
4. Relance en mode Solo (choix 1)

**Ou manuellement**:
```
taskkill /F /IM python.exe
```

---

## 🔧 Launchers Disponibles

| Fichier | Description |
|---------|-------------|
| **LAUNCH_WITH_MODE_SELECT.bat** | **RECOMMANDÉ** - Menu avec 3 modes |
| **LAUNCH_CLEAN_GAME.bat** | Lance direct sans IA externe |
| **launcher_auto_diagnostic.py** | Diagnostic + choix moteur |
| **Ikemen_GO.exe** | Direct Ikemen GO (netplay) |
| **KOF_Ultimate_Online.exe** | Direct M.U.G.E.N |

---

## 🎯 Quel Launcher Utiliser?

### Pour jouer normalement:
→ **`LAUNCH_WITH_MODE_SELECT.bat`**

### Pour tester/diagnostiquer:
→ **`launcher_auto_diagnostic.py`**

### Pour les tests IA:
→ **`LAUNCH_IAs_COMPLETE.bat`** (ATTENTION: IA joue P1!)

---

## 📦 Contenu du Pack

- **189 personnages** KOF
- **50+ stages**
- **2 moteurs**: M.U.G.E.N + Ikemen GO
- **Support netplay** (Ikemen GO)
- **Scripts IA** (optionnels)
- **Auto-diagnostic** intégré

---

## 🆘 Problèmes Courants

### "Je ne peux pas contrôler P1"
→ Scripts IA en cours. Utilise `LAUNCH_WITH_MODE_SELECT.bat`

### "Erreur Ikemen GO: data/system.def"
→ Lance: `python launcher_auto_diagnostic.py` → Auto-fix automatique

### "Personnages pas dans les bonnes cases"
→ Problème de portraits, à corriger dans system.def

### "Le jeu crash au lancement"
→ Lance: `python launcher_auto_diagnostic.py` → Diagnostic complet

---

## 🎮 Profite bien du jeu!

Pour plus d'infos sur les personnages, regarde les fiches dans le dossier `chars/`
