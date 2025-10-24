# 🧪 PLAN DE TEST MANUEL COMPLET

**Objectif:** Tester TOUS les personnages en combat réel et créer une liste ultra-stable

---

## 📋 MÉTHODE PROPOSÉE

### Option A: Test Rapide par Vous (Recommandé)
Vous testez chaque personnage pendant 10 secondes en combat:

1. Mode Versus
2. Sélectionnez le personnage à tester (P1)
3. Sélectionnez un personnage "safe" connu (P2) - ex: Hunter_U6746
4. Lancez le combat
5. Laissez tourner 10 secondes
6. Si crash → Notez le personnage
7. Passez au suivant

**Durée:** 122 personnages × 20 secondes = ~40 minutes

### Option B: Script de Test Combat Réel (Automatique)
Je crée un script qui:
- Lance le jeu
- Sélectionne automatiquement 2 personnages
- Lance le combat
- Attend 30 secondes
- Détecte si crash
- Passe au suivant

**Durée:** 122 personnages × 45 secondes = ~90 minutes

### Option C: Test par Groupe (Hybride)
On divise les 122 personnages en 10 groupes de 12:
- Vous testez rapidement chaque groupe
- Vous notez ceux qui crashent
- Je les désactive en masse

**Durée:** ~20-30 minutes

---

## 🎯 QUELLE OPTION CHOISISSEZ-VOUS?

**A** - Je teste manuellement (40 min mais fiable)
**B** - Script automatique de combat (90 min, automatique)
**C** - Test par groupes (20-30 min, rapide)

---

## 📊 RÉALITÉ ACTUELLE

Sur ~190 personnages dans le dossier:
- ✅ ~122 actifs actuellement
- ❌ ~18 désactivés
- ❓ **Combien crashent vraiment en jeu?** Probablement 30-50+

**Pour un jeu "release-ready"**, on devrait avoir:
- **70-90 personnages ultra-stables**
- Tous testés en combat réel
- Aucun crash

---

## 🚀 MA RECOMMANDATION

**Option C - Test par groupes:**

Je vous donne une liste de 12 personnages à tester:
1. Vous testez rapidement (1-2 min par groupe)
2. Vous me dites lesquels crashent
3. Je les désactive
4. On passe au groupe suivant
5. En 10 groupes, on a un jeu ultra-stable

**Voulez-vous qu'on fasse ça maintenant?**

Ou préférez-vous que je crée le script automatique (Option B)?
