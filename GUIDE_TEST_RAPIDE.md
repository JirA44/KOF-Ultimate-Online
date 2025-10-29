# 🚀 GUIDE DE TEST RAPIDE - KOF ULTIMATE ONLINE

## 📋 Checklist avant de commencer

- [ ] Python 3.8+ installé
- [ ] Dépendances installées (exécuter `INSTALL_DEPENDENCIES.bat`)
- [ ] Le jeu est dans `D:/KOF Ultimate Online/`
- [ ] `KOF_Ultimate_Online.exe` existe

---

## ⚡ TEST 1 : Lancer le Launcher (2 minutes)

### Objectif
Vérifier que le launcher démarre correctement.

### Étapes
1. Double-cliquer sur **`LAUNCH_ULTIMATE.bat`**
2. Le launcher doit s'ouvrir avec une interface graphique

### ✅ Résultat attendu
- Fenêtre "KOF Ultimate Online - Launcher Ultimate"
- 4 indicateurs de statut (tous "Arrêté")
- Journal d'activité avec "Launcher Ultimate démarré"

### ❌ Si ça ne marche pas
```bash
# Vérifier Python
python --version

# Installer les dépendances
INSTALL_DEPENDENCIES.bat

# Lancer manuellement
python KOFUO_LAUNCHER_ULTIMATE.py
```

---

## ⚡ TEST 2 : Détecter les Bugs (15-30 minutes)

### Objectif
Identifier les personnages problématiques et créer un roster optimal.

### Étapes
1. Dans le launcher, cliquer sur **"🔍 Détecter les Bugs"**
2. Une nouvelle console s'ouvre
3. Attendre que tous les personnages soient testés
4. À la fin, vérifier :
   - `bug_report.json` créé
   - `data/select_optimal.def` créé

### ✅ Résultat attendu
```
PERSONNAGES STABLES (Recommandés):
  ✓ Kyo
  ✓ Iori
  ✓ Terry
  ...

PERSONNAGES PROBLÉMATIQUES (À éviter):
  ✗ Akiha Orochi
  ✗ Blood Rugal
  ...
```

### 📊 Vérifier les résultats
```bash
# Ouvrir le rapport
notepad bug_report.json

# Compter les personnages stables
type bug_report.json | findstr "stable"
```

### ⚠️ Notes
- Le test prend du temps (1-2 minutes par personnage)
- Le jeu se lance et se ferme automatiquement pour chaque test
- Ne touchez à rien pendant le scan

---

## ⚡ TEST 3 : Optimiser le Roster (1 minute)

### Objectif
Utiliser uniquement les personnages stables détectés.

### Étapes
1. Dans le launcher, cliquer sur **"📝 Optimiser Select.def"**
2. Confirmer le message "select.def optimisé"

### ✅ Résultat attendu
- `data/select.def` maintenant contient uniquement les personnages stables
- Le jeu ne devrait plus crasher

### Vérification manuelle
```bash
# Voir le nouveau select.def
notepad "data/select.def"

# Compter les personnages
type "data/select.def" | findstr /V "^;" | findstr "chars"
```

---

## ⚡ TEST 4 : Lancer le Jeu en Solo (5 minutes)

### Objectif
Vérifier que le jeu démarre sans crash.

### Étapes
1. Dans le launcher, cliquer sur **"🎮 Lancer le Jeu (Solo)"**
2. Le jeu s'ouvre
3. Aller dans "Versus Mode"
4. Sélectionner 2 personnages
5. Lancer le match
6. Jouer pendant 1-2 minutes
7. Quitter

### ✅ Résultat attendu
- Le jeu démarre en moins de 10 secondes
- Pas de crash pendant la sélection
- Le match se lance correctement
- Pas de lag majeur

### ❌ Si ça crash
1. Vérifier `mugen.log`
2. Chercher le personnage problématique
3. Le retirer manuellement de `data/select.def`

---

## ⚡ TEST 5 : Serveur Battle.net (2 minutes)

### Objectif
Démarrer le serveur multijoueur.

### Étapes
1. Dans le launcher, cliquer sur **"🖥️ Lancer Serveur Battle.net"**
2. Une nouvelle console s'ouvre
3. Vérifier le message "Serveur Battle.net démarré sur 0.0.0.0:8765"

### ✅ Résultat attendu
```
🚀 Serveur Battle.net démarré sur 0.0.0.0:8765
```

Dans le launcher :
- Indicateur "Serveur Battle.net" passe à "● En cours" (vert)

### Vérifier le port
```bash
# Windows
netstat -ano | findstr 8765

# Doit afficher une ligne avec LISTENING
```

---

## ⚡ TEST 6 : Client Battle.net (2 minutes)

### Objectif
Se connecter au serveur.

### Étapes
1. S'assurer que le serveur est lancé (TEST 5)
2. Dans le launcher, cliquer sur **"⚔️ Jouer en Ligne (Battle.net)"**
3. Une interface graphique s'ouvre
4. Entrer un pseudo (ex: "TestPlayer")
5. Cliquer sur "Se Connecter"

### ✅ Résultat attendu
- Connexion réussie
- Statut passe à "En ligne - Prêt à jouer" (vert)
- Les stats du joueur s'affichent (ELO: 1000)
- Le bouton "Rechercher un Adversaire" est activé

### ❌ Si la connexion échoue
1. Vérifier que le serveur est bien lancé
2. Vérifier le pare-feu Windows
3. Essayer de relancer le serveur

---

## ⚡ TEST 7 : Matchmaking (5 minutes)

### Objectif
Tester le système de matchmaking avec 2 clients.

### Étapes
1. Lancer le serveur (TEST 5)
2. Lancer le client 1 (TEST 6)
3. Se connecter avec le pseudo "Player1"
4. Lancer un DEUXIÈME client :
   ```bash
   python BATTLENET_CLIENT.py
   ```
5. Se connecter avec le pseudo "Player2"
6. Sur les DEUX clients, cliquer sur "Rechercher un Adversaire"
7. Attendre le match (max 5 secondes)

### ✅ Résultat attendu
- Un message "Match Trouvé !" apparaît sur les 2 clients
- Les infos de l'adversaire s'affichent :
  - Pseudo
  - ELO
  - Victoires/Défaites
- Statut passe à "Match en Cours"

### 📊 Dans la console du serveur
```
⚔️ Match créé: Player1 vs Player2 (ID: match_0)
```

---

## ⚡ TEST 8 : Rapporter un Résultat (2 minutes)

### Objectif
Tester la mise à jour du classement ELO.

### Étapes
1. Après un match trouvé (TEST 7)
2. Jouer la partie dans le jeu (ou simuler)
3. Dans un des clients, simuler une victoire :
   ```python
   # Dans la console Python du client
   await client.report_match_result(winner_id="player1")
   ```

### ✅ Résultat attendu
- Message "Match Terminé"
- Nouveau ELO affiché
- Player1 : ELO augmente (~1016)
- Player2 : ELO diminue (~984)
- Statut repasse à "En ligne - Prêt à jouer"

---

## ⚡ TEST 9 : Classement (1 minute)

### Objectif
Voir le leaderboard.

### Étapes
1. Se connecter avec un client
2. Observer le panel "CLASSEMENT" à droite

### ✅ Résultat attendu
```
#1  Player1  1016 ELO  1W 0L
#2  Player2   984 ELO  0W 1L
```

---

## ⚡ TEST 10 : Arrêt Propre (1 minute)

### Objectif
Vérifier que tout s'arrête correctement.

### Étapes
1. Dans le launcher, cliquer sur **"❌ Quitter et Tout Arrêter"**
2. Confirmer

### ✅ Résultat attendu
- Tous les processus s'arrêtent
- Toutes les consoles se ferment
- Le launcher se ferme

### Vérification
```bash
# Vérifier qu'aucun processus Python ne tourne
tasklist | findstr python
```

---

## 📊 RÉSUMÉ DES TESTS

| Test | Durée | Priorité | Statut |
|------|-------|----------|--------|
| 1. Launcher | 2 min | 🔴 Critique | ⬜ |
| 2. Détection bugs | 15-30 min | 🔴 Critique | ⬜ |
| 3. Optimisation | 1 min | 🔴 Critique | ⬜ |
| 4. Jeu solo | 5 min | 🔴 Critique | ⬜ |
| 5. Serveur | 2 min | 🟡 Important | ⬜ |
| 6. Client | 2 min | 🟡 Important | ⬜ |
| 7. Matchmaking | 5 min | 🟡 Important | ⬜ |
| 8. Résultat | 2 min | 🟢 Optionnel | ⬜ |
| 9. Classement | 1 min | 🟢 Optionnel | ⬜ |
| 10. Arrêt | 1 min | 🟡 Important | ⬜ |

**Temps total :** 35-50 minutes

---

## 🐛 PROBLÈMES FRÉQUENTS

### "Python not found"
```bash
# Vérifier l'installation
python --version

# Ajouter au PATH si nécessaire
setx PATH "%PATH%;C:\Python39"
```

### "Module websockets not found"
```bash
pip install websockets
```

### Le serveur ne démarre pas
```bash
# Tuer les processus Python
taskkill /F /IM python.exe

# Relancer
python BATTLENET_SERVER.py
```

### Le jeu crash au lancement du match
1. Relancer le détecteur de bugs
2. Vérifier `mugen.log` pour voir quel personnage pose problème
3. Le retirer de `data/select.def`

---

## ✅ VALIDATION FINALE

Après tous les tests, vous devez avoir :

- [x] Le launcher fonctionne
- [x] Les bugs sont détectés
- [x] Le roster est optimisé
- [x] Le jeu démarre en solo sans crash
- [x] Le serveur Battle.net démarre
- [x] Les clients se connectent
- [x] Le matchmaking trouve des adversaires
- [x] Le classement ELO fonctionne
- [x] Tout s'arrête proprement

**Si tous les tests passent :** 🎉 Le système est opérationnel !

---

## 📝 NOTES

- Gardez ce guide pour référence future
- Exécutez le détecteur de bugs après chaque ajout de personnage
- Sauvegardez `select_optimal.def` et `bug_report.json`

**Bonne chance et amusez-vous bien !** 🎮⚔️
