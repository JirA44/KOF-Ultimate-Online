# 📊 SYSTÈME DE RAPPORTS EN DIRECT

**Date:** 2025-10-23
**Fréquence:** Toutes les 5 minutes

---

## 🎯 Ce qui a été créé

### Live Reporter (`live_reporter.py`)
Script qui génère automatiquement des rapports détaillés toutes les 5 minutes.

**Contenu des rapports:**
- 📈 Statistiques globales (joueurs, matchs, ELO moyen)
- 🏆 Top 5 joueurs
- 📉 Bottom 5 joueurs (en progression)
- ⚔️ 5 derniers matchs
- 🧠 Stats Machine Learning
- 📊 Distribution par niveau de compétence
- ⏱️ Activité (matchs/minute)

---

## 🚀 Comment lancer

### Option 1: Tout en une fois (RECOMMANDÉ)
```batch
START_WITH_REPORTER.bat
```

**Ce qui se passe:**
1. Nettoie les processus existants
2. Lance le serveur de matchmaking
3. Lance 20 joueurs virtuels IA
4. Lance le système ML
5. Ouvre le dashboard web
6. Attend 15 secondes
7. **Lance le Live Reporter dans la même fenêtre**
8. Affiche un rapport toutes les 5 minutes

**Avantages:**
- ✅ Tout se lance automatiquement
- ✅ Rapports visibles directement dans la console
- ✅ Dashboard web en parallèle
- ✅ Pas besoin de manipulations supplémentaires

---

### Option 2: Lancer seulement le reporter
Si le système tourne déjà:
```batch
python live_reporter.py
```

---

## 📊 Format des rapports

```
======================================================================
📊 RAPPORT #1 - 2025-10-23 10:45:30
======================================================================

📈 STATISTIQUES GLOBALES
----------------------------------------------------------------------
👥 Joueurs enregistrés:    20
⚔️  Total des matchs:       143
🆕 Nouveaux matchs (5 min): 47
📊 ELO moyen:              1024

🏆 TOP 5 JOUEURS
----------------------------------------------------------------------
🥇 DarkWarrior999        | ELO: 1245 | W/L: 23/18 | WR:  56.1% | Advanced
🥈 FireKing420           | ELO: 1189 | W/L: 19/15 | WR:  55.9% | Intermediate
🥉 ThunderSlayer         | ELO: 1156 | W/L: 21/20 | WR:  51.2% | Intermediate
4️⃣ CyberNinja999         | ELO: 1134 | W/L: 18/19 | WR:  48.6% | Intermediate
5️⃣ ShadowAce123          | ELO: 1098 | W/L: 15/18 | WR:  45.5% | Beginner

📉 BOTTOM 5 (En progression)
----------------------------------------------------------------------
 1. PhoenixX420          | ELO:  867 | W/L:  8/25 | WR:  24.2%
 2. StormBreaker88       | ELO:  891 | W/L: 10/23 | WR:  30.3%
 3. IceDragon777         | ELO:  924 | W/L: 12/21 | WR:  36.4%
 4. BladeRunner99        | ELO:  945 | W/L: 14/20 | WR:  41.2%
 5. NeonKing2000         | ELO:  968 | W/L: 16/19 | WR:  45.7%

⚔️  MATCHS RÉCENTS (5 derniers)
----------------------------------------------------------------------
   🏆 DarkWarrior999  (1245) vs 💀 FireKing420     (1189)
   💀 ThunderSlayer   (1156) vs 🏆 CyberNinja999   (1134)
   🏆 ShadowAce123    (1098) vs 💀 PhoenixX420     ( 867)
   💀 StormBreaker88  ( 891) vs 🏆 IceDragon777    ( 924)
   🏆 BladeRunner99   ( 945) vs 💀 NeonKing2000    ( 968)

🧠 MACHINE LEARNING
----------------------------------------------------------------------
🔄 Cycles d'apprentissage: 3

🎯 Stratégies optimales:
   1. aggressive      -  58.3% WR (84 matchs)
   2. balanced        -  52.7% WR (91 matchs)
   3. defensive       -  47.9% WR (73 matchs)

📊 DISTRIBUTION PAR NIVEAU
----------------------------------------------------------------------
   Master          ( 1): █
   Expert          ( 3): ███
   Advanced        ( 5): █████
   Intermediate    ( 8): ████████
   Beginner        ( 3): ███

⏱️  ACTIVITÉ
----------------------------------------------------------------------
   Matchs/minute: 9.4
   Estimation matchs/heure: 564

======================================================================
⏰ Prochain rapport dans 5 minutes...
======================================================================
```

---

## 📋 Informations affichées

### Statistiques Globales
- **Joueurs enregistrés**: Nombre total de joueurs dans le système
- **Total des matchs**: Nombre cumulé de tous les matchs
- **Nouveaux matchs**: Matchs joués dans les dernières 5 minutes
- **ELO moyen**: Moyenne de tous les ELO

### Top 5 Joueurs
- Classement par ELO décroissant
- Médailles pour le podium (🥇🥈🥉)
- Victoires/Défaites
- Winrate (%)
- Niveau de compétence

### Bottom 5
- Les 5 joueurs avec le plus bas ELO
- Utile pour voir qui va être amélioré par le système ML

### Matchs Récents
- 5 derniers matchs joués
- 🏆 = Gagnant
- 💀 = Perdant
- ELO des deux joueurs au moment du match

### Machine Learning
- Nombre de cycles d'amélioration effectués
- Stratégies les plus efficaces
- Winrate par stratégie

### Distribution par Niveau
- Visualisation du nombre de joueurs par niveau
- Graphique en barres ASCII
- Niveaux: Beginner → Intermediate → Advanced → Expert → Master

### Activité
- Matchs par minute (moyenne sur 5 min)
- Estimation matchs par heure

---

## ⚙️ Configuration

### Changer l'intervalle des rapports

Éditer `live_reporter.py` ligne ~295:
```python
time.sleep(300)  # 300 secondes = 5 minutes
```

**Exemples:**
- 1 minute: `time.sleep(60)`
- 2 minutes: `time.sleep(120)`
- 10 minutes: `time.sleep(600)`

---

## 🛑 Arrêter

**Arrêter seulement le reporter:**
- Appuyer sur `Ctrl+C` dans la fenêtre du reporter

**Arrêter tout le système:**
```batch
EMERGENCY_STOP.bat
```

---

## 📂 Fichiers utilisés

Le reporter lit ces fichiers:
- `matchmaking_state.json` - État du serveur et joueurs
- `ml_system_meta.json` - Métadonnées ML (optionnel)

Ces fichiers sont générés automatiquement par le système.

---

## 🔧 Dépannage

### Rapport vide ou "Aucune donnée disponible"
**Cause**: Le système n'a pas encore généré les fichiers JSON

**Solution**:
1. Attendre 15-20 secondes
2. Vérifier que les processus tournent:
   ```batch
   tasklist | findstr python
   ```
3. Si rien, relancer: `START_WITH_REPORTER.bat`

### Le reporter ne s'affiche pas
**Cause**: Lancé en arrière-plan au lieu de la console

**Solution**:
- Fermer tous les processus: `EMERGENCY_STOP.bat`
- Relancer: `START_WITH_REPORTER.bat`

### Trop de rapports
**Cause**: Intervalle trop court

**Solution**:
- Augmenter l'intervalle dans `live_reporter.py`
- Ou lancer le dashboard web uniquement (pas de rapports console)

---

## 💡 Astuces

### Sauvegarder les rapports dans un fichier
```batch
python live_reporter.py > rapports.txt
```

### Voir les rapports + dashboard en même temps
1. Lancer `START_WITH_REPORTER.bat`
2. Consulter la console pour les rapports texte
3. Consulter le navigateur pour le dashboard graphique

### Reporter + Dashboard = Vue complète
- **Console**: Rapports détaillés toutes les 5 min
- **Dashboard Web**: Stats en temps réel (actualisation 3s)

---

## 🎯 Cas d'usage

### Usage 1: Monitoring passif
- Lancer `START_WITH_REPORTER.bat`
- Laisser la fenêtre ouverte
- Jeter un œil toutes les 5 minutes

### Usage 2: Analyse détaillée
- Lancer le reporter
- Sauvegarder dans un fichier
- Analyser l'évolution sur plusieurs heures

### Usage 3: Démo
- Lancer `START_WITH_REPORTER.bat`
- Montrer la console avec les rapports
- Montrer le dashboard web
- Impressionner avec le système autonome!

---

## 📊 Métriques importantes à surveiller

### Santé du système
- ✅ Nouveaux matchs > 0 (le système fonctionne)
- ✅ ELO moyen stable ou en progression
- ✅ Distribution équilibrée des niveaux

### Performance
- 🎯 Optimal: 8-12 matchs/minute avec 20 joueurs
- ⚠️ Faible: < 5 matchs/minute (problème?)
- 🔥 Élevé: > 15 matchs/minute (excellent!)

### Apprentissage
- 📈 Winrate des bottom 5 augmente = ML fonctionne
- 📈 Cycles ML s'incrémentent = Système actif
- 📈 Stratégies optimales émergent

---

## ✅ Checklist

Après lancement, vérifier:
- [ ] Console affiche "LIVE REPORTER" en header
- [ ] Premier rapport s'affiche après 15s
- [ ] Stats non nulles (joueurs, matchs)
- [ ] Top 5 se remplit
- [ ] Matchs récents s'affichent
- [ ] Dashboard web fonctionne en parallèle
- [ ] Nouveau rapport toutes les 5 minutes

---

**Créé le:** 2025-10-23
**Version:** 1.0
**Intervalle par défaut:** 5 minutes

---

# 📊 Bon monitoring ! 🎮
