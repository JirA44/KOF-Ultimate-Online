# 🎮 KOF ULTIMATE - Guide de Lancement

## ❌ PROBLÈME RÉSOLU !

**Le problème:** Les IAs demandaient une clé API Anthropic et bloquaient au lancement.

**La solution:** Nouveau système d'auto-clicker sans API !

---

## ✅ NOUVEAU SYSTÈME - Auto-Clicker

### 🚀 Lancement Ultra-Simple

**Méthode 1 - Fichier BAT (RECOMMANDÉ)**
```
Double-cliquez sur: LAUNCH_KOF_AUTO.bat
```

**Méthode 2 - Python Direct**
```bash
python auto_clicker_kof.py
```

### 🎯 Ce que fait l'Auto-Clicker

1. **Lance le jeu automatiquement**
2. **Passe l'écran de titre** (Entrée)
3. **Navigue vers Arcade Mode** (Flèche bas + Entrée)
4. **Sélectionne un personnage** (Entrée)
5. **Confirme l'équipe** (Entrée)

**Résultat:** Le jeu se lance et arrive directement en mode combat !

---

## 📁 Fichiers Disponibles

### Auto-Clicker (NOUVEAU ✨)
- `LAUNCH_KOF_AUTO.bat` - **À UTILISER EN PRIORITÉ**
- `auto_clicker_kof.py` - Script auto-clicker

### Launchers Modernes
- `LAUNCHER_ULTIMATE_V2.py` - Launcher avec auto-installation progressive
- `launcher.py` - Launcher principal amélioré
- `character_dashboard.py` - Voir tous les personnages et leurs coups
- `visual_inspector.py` - Inspecteur visuel pour les animations

### Launchers Classiques
- `LAUNCH_KOF_ULTIMATE.bat` - Choix moteur M.U.G.E.N ou Ikemen
- `LAUNCH_ULTIMATE.bat` - Lancement avec dépendances

---

## 🔧 Dépendances

L'auto-clicker installe automatiquement :
- `pyautogui` - Pour les clics automatiques
- `pywin32` - Pour la gestion des fenêtres

**Pas besoin de clé API !**

---

## 🎯 Utilisation Recommandée

### Pour jouer normalement:
```
1. LAUNCH_KOF_AUTO.bat
2. Laissez l'auto-clicker faire son travail
3. Jouez !
```

### Pour gérer les personnages:
```
python launcher.py
→ Cliquez sur "👤 Personnages"
```

### Pour vérifier les animations:
```
python launcher.py
→ Cliquez sur "🔍 Inspecteur Visuel"
```

---

## ⚙️ Options Avancées

### Modifier la séquence de clics
Éditez `auto_clicker_kof.py`, section `auto_click_sequence()`:

```python
actions = [
    ("Description", "touche", durée_attente),
    ("Passer titre", "enter", 2),
    # Ajoutez vos actions ici
]
```

### Activer la surveillance continue
Dans `auto_clicker_kof.py`, décommentez:
```python
# self.monitor_and_click(duration_minutes=30)
```

---

## 🐛 Résolution de Problèmes

### Le jeu ne se lance pas
- Vérifiez que `KOF BLACK R.exe` existe
- Vérifiez le chemin dans `auto_clicker_kof.py` ligne 15

### L'auto-clicker ne clique pas
- Le jeu doit être en fenêtre visible
- Vérifiez que pyautogui est installé: `pip install pyautogui`

### Erreur "Fenêtre non trouvée"
- Le jeu met peut-être plus de temps à démarrer
- Augmentez le délai dans `auto_click_sequence()` ligne 84

---

## 📊 Statistiques

- **189 personnages** disponibles
- **Auto-clicker** opérationnel
- **Installation progressive** disponible
- **Pas de clé API requise**

---

## 💡 Conseils

1. **Première utilisation:** Utilisez `LAUNCH_KOF_AUTO.bat`
2. **Gestion avancée:** Utilisez `LAUNCHER_ULTIMATE_V2.py`
3. **Personnages:** Utilisez le Character Dashboard
4. **Debug:** Utilisez le Visual Inspector

---

## ✅ Checklist Rapide

- [x] Auto-clicker créé et fonctionnel
- [x] Pas besoin de clé API
- [x] Lance le jeu automatiquement
- [x] Navigue dans les menus
- [x] Sélectionne un personnage
- [x] Arrive en mode combat

**Tout est prêt ! Lancez `LAUNCH_KOF_AUTO.bat` et jouez !** 🎮
