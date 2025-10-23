# 🔇 GUIDE - MODE SILENCIEUX

**Date:** 2025-10-23
**Status:** ✅ OPÉRATIONNEL

---

## 🎯 Qu'est-ce que le Mode Silencieux ?

Le **Mode Silencieux** permet de faire tourner tout le système de matchmaking et d'IA **en arrière-plan** sans aucune fenêtre visible.

**Avantages:**
- ✅ Aucune fenêtre console qui s'affiche
- ✅ Pas de jeu en plein écran qui dérange
- ✅ Surveillance via dashboard web élégant
- ✅ Processus légers en arrière-plan
- ✅ Logs propres et organisés

---

## 🚀 Lancement

### Option 1: Matchmaking SANS le jeu (RECOMMANDÉ)
```batch
LAUNCH_MATCHMAKING_ONLY.bat
```

**Ce qui est lancé:**
- ✅ Serveur de matchmaking (port 9999)
- ✅ 20 joueurs virtuels IA
- ✅ Système ML d'amélioration continue
- ✅ Dashboard de monitoring

**Ce qui n'est PAS lancé:**
- ❌ Le jeu KOF (pas de plein écran!)
- ❌ Auto-combat

---

### Option 2: Tout inclus (avec jeu)
```batch
LAUNCH_SILENT.bat
```

**Ce qui est lancé:**
- ✅ Tout (matchmaking + jeu + auto-combat)

⚠️ **Attention:** Le jeu peut se lancer en plein écran

---

## 🛑 Arrêt

### Arrêter TOUT d'un coup
```batch
STOP_ALL.bat
```

**Ou manuellement:**
```batch
taskkill /IM pythonw.exe /F
taskkill /IM KOF_Ultimate_Online.exe /F
```

---

## 📊 Monitoring

### Dashboard Web
- **Fichier:** `monitoring_dashboard.html`
- **Actualisation:** Automatique toutes les 3 secondes
- **Contenu:**
  - 📈 Stats en temps réel
  - 🏆 Leaderboard Top 10
  - 🖥️ État des processus
  - 📜 Log d'activité récente
  - 📊 Graphique d'activité

**Pour ouvrir:**
```batch
start "" "monitoring_dashboard.html"
```

---

### Consulter les Logs

Tous les logs sont dans le dossier `logs/` :

```batch
# Serveur de matchmaking
type logs\matchmaking.log | more

# Joueurs virtuels
type logs\players.log | more

# Système ML
type logs\ml_system.log | more

# Jeu KOF (si lancé)
type logs\kof_combat.log | more
```

---

### Données JSON en temps réel

**État du matchmaking:**
```batch
type matchmaking_state.json
```

**Métadonnées ML:**
```batch
type ml_system_meta.json
```

**Profils des joueurs:**
```batch
dir player_profiles\*.json
type player_profiles\player_0.json
```

---

## 🎮 Différences avec le Mode Normal

| Aspect | Mode Normal | Mode Silencieux |
|--------|-------------|-----------------|
| Fenêtres console | ✅ Visibles | ❌ Cachées |
| Jeu auto-lancé | ✅ Oui | ❌ Non (option) |
| Monitoring | Logs console | Dashboard web |
| Processus | `python.exe` | `pythonw.exe` |
| Logs | Console | Fichiers `.log` |
| Performance | Standard | Optimale |

---

## 🔧 Configuration

### Changer le nombre de joueurs virtuels

Éditer `virtual_players_ai.py` ligne ~280:
```python
manager = VirtualPlayersManager(num_players=20)  # Changez 20 → 50
```

### Changer l'intervalle ML

Éditer `ml_continuous_improver.py` ligne ~75:
```python
time.sleep(30 * 60)  # 30 minutes → changez
```

### Changer le port du serveur

Éditer `matchmaking_server.py` ligne ~388:
```python
server = MatchmakingServer(host='0.0.0.0', port=9999)  # Changez port
```

---

## 📈 Performance

### Utilisation des ressources

**Mode Silencieux:**
- CPU: ~5-10% (selon nb de joueurs)
- RAM: ~200-300 MB
- Réseau: Localhost uniquement
- Disque: Écritures périodiques (logs + JSON)

**Processus actifs:**
- `pythonw.exe` (3-4 instances)
- Navigateur (pour dashboard)

---

## ⚠️ Dépannage

### Le dashboard ne montre rien
**Solution:**
1. Attendre 10 secondes que les données se génèrent
2. Actualiser la page (F5)
3. Vérifier que les processus tournent:
   ```batch
   tasklist | findstr pythonw
   ```

### Aucun processus ne tourne
**Solution:**
1. Lancer `LAUNCH_MATCHMAKING_ONLY.bat`
2. Vérifier que Python est installé:
   ```batch
   python --version
   ```

### Les logs sont vides
**Solution:**
1. Attendre quelques secondes
2. Vérifier que les processus ont démarré
3. Consulter `monitoring_dashboard.html`

### Le jeu se lance quand même
**Solution:**
1. Utiliser `STOP_ALL.bat`
2. Utiliser `LAUNCH_MATCHMAKING_ONLY.bat` (pas LAUNCH_SILENT.bat)

---

## 🎯 Fichiers Importants

### Launchers
- ✅ `LAUNCH_MATCHMAKING_ONLY.bat` - **RECOMMANDÉ** (sans jeu)
- ✅ `LAUNCH_SILENT.bat` - Tout en silencieux (avec jeu)
- ✅ `STOP_ALL.bat` - Arrêter tout

### Monitoring
- ✅ `monitoring_dashboard.html` - Dashboard principal
- ✅ `logs/` - Dossier des logs
- ✅ `matchmaking_state.json` - État du serveur
- ✅ `ml_system_meta.json` - Stats ML

### Scripts
- ✅ `matchmaking_server.py` - Serveur central
- ✅ `virtual_players_ai.py` - Joueurs IA
- ✅ `ml_continuous_improver.py` - Système ML
- ✅ `auto_combat_new_maps.py` - Auto-combat (optionnel)

---

## 🏆 Checklist de Vérification

Après lancement, vérifier:

- [ ] Dashboard ouvert dans le navigateur
- [ ] Stats s'affichent après 10s
- [ ] Leaderboard se remplit
- [ ] Log d'activité s'actualise
- [ ] État des processus = ✅ Actif
- [ ] Fichiers JSON créés (`matchmaking_state.json`)
- [ ] Dossier `player_profiles/` créé
- [ ] Dossier `logs/` créé et rempli

---

## 💡 Astuces

### Laisser tourner en permanence
Le système peut tourner 24/7 en arrière-plan:
- Logs limités (pas d'explosion de taille)
- Sauvegardes automatiques
- Amélioration continue des IA
- Pas de consommation excessive

### Surveiller à distance
Le dashboard est un simple fichier HTML:
- Partageable via réseau local
- Consultable depuis n'importe quel appareil
- Pas besoin de serveur web

### Multi-fenêtres
Vous pouvez ouvrir plusieurs instances du dashboard:
- Une pour les stats
- Une pour le leaderboard
- Une pour les logs

---

## 🎮 Utilisation Recommandée

**Scenario 1: Développement/Test**
```batch
LAUNCH_MATCHMAKING_ONLY.bat
```
→ Surveiller l'évolution des IA sans le jeu

**Scenario 2: Démo**
```batch
LAUNCH_SILENT.bat
```
→ Montrer le système complet (avec jeu)

**Scenario 3: Production**
```batch
LAUNCH_MATCHMAKING_ONLY.bat
```
→ Laisser tourner en permanence

---

## 📞 Support Rapide

**Problème:** Trop de fenêtres
**Solution:** Utiliser `LAUNCH_MATCHMAKING_ONLY.bat`

**Problème:** Jeu en plein écran
**Solution:** `STOP_ALL.bat` puis `LAUNCH_MATCHMAKING_ONLY.bat`

**Problème:** Tout est lent
**Solution:** Réduire le nombre de joueurs virtuels (ligne 280 dans `virtual_players_ai.py`)

**Problème:** Dashboard vide
**Solution:** Attendre 10-15 secondes, actualiser

---

## ✅ Avantages du Mode Silencieux

1. **🔇 Discrétion totale**
   - Pas de pollution visuelle
   - Travaillez normalement à côté

2. **📊 Monitoring élégant**
   - Dashboard moderne et responsive
   - Actualisation automatique
   - Données en temps réel

3. **⚡ Performance**
   - `pythonw.exe` plus léger que `python.exe`
   - Pas de rendu console inutile
   - Logs optimisés

4. **🎯 Contrôle précis**
   - Choisir ce qui tourne
   - Arrêt facile et rapide
   - Pas de surprises

---

**Créé le:** 2025-10-23
**Version:** 1.0
**Status:** ✅ Opérationnel

---

# 🔇 Profitez du silence ! 🎧
