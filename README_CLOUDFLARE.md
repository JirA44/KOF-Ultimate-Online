# 🌐 DÉPLOIEMENT SUR CLOUDFLARE PAGES

## 📋 Vue d'ensemble

Ce guide vous explique comment déployer le site web de KOF Ultimate Online sur **Cloudflare Pages** pour qu'il soit accessible en ligne gratuitement.

---

## 🚀 DÉPLOIEMENT RAPIDE (5 MINUTES)

### Étape 1 : Préparer le Repository Git

1. **Initialiser Git** (si pas déjà fait)
   ```bash
   cd "D:\KOF Ultimate Online"
   git init
   git add web/ .gitignore README_CLOUDFLARE.md
   git commit -m "Initial commit - Site web KOF Ultimate Online"
   ```

2. **Créer un repository sur GitHub**
   - Aller sur [github.com](https://github.com)
   - Cliquer sur "New repository"
   - Nom : `kof-ultimate-online-web`
   - Public ou Private (au choix)
   - NE PAS initialiser avec README
   - Créer le repository

3. **Pousser le code sur GitHub**
   ```bash
   git remote add origin https://github.com/VOTRE_USERNAME/kof-ultimate-online-web.git
   git branch -M main
   git push -u origin main
   ```

### Étape 2 : Déployer sur Cloudflare Pages

1. **Se connecter à Cloudflare**
   - Aller sur [dash.cloudflare.com](https://dash.cloudflare.com)
   - Se connecter ou créer un compte (gratuit)

2. **Créer un nouveau projet**
   - Aller dans "Workers & Pages"
   - Cliquer sur "Create application"
   - Choisir "Pages"
   - Cliquer sur "Connect to Git"

3. **Connecter GitHub**
   - Autoriser Cloudflare à accéder à GitHub
   - Sélectionner le repository `kof-ultimate-online-web`

4. **Configurer le build**
   ```
   Project name: kof-ultimate-online
   Production branch: main
   Build command: (laisser vide)
   Build output directory: web
   ```

5. **Déployer**
   - Cliquer sur "Save and Deploy"
   - Attendre 1-2 minutes

6. **Accéder au site**
   - Votre site sera disponible sur : `https://kof-ultimate-online.pages.dev`

---

## 🎯 CONFIGURATION DÉTAILLÉE

### Structure du Repository

Seuls ces fichiers seront sur Git :

```
kof-ultimate-online-web/
├── web/
│   ├── index.html
│   ├── dashboard.html
│   ├── leaderboard.html
│   ├── docs.html
│   ├── style.css
│   ├── app-static.js
│   └── api-mock.js
├── .gitignore
└── README_CLOUDFLARE.md
```

### Paramètres Cloudflare Pages

| Paramètre | Valeur |
|-----------|--------|
| Framework preset | None |
| Build command | (vide) |
| Build output directory | `web` |
| Root directory | `/` |
| Environment variables | (aucune nécessaire) |

---

## 🔧 VERSION STATIQUE

### Différences avec la version locale

| Fonctionnalité | Local (Node.js) | Cloudflare (Statique) |
|----------------|-----------------|----------------------|
| Serveur | Node.js + WebSocket | HTML/CSS/JS statique |
| API | REST + WebSocket temps réel | Données mockées |
| Données | Serveur Battle.net réel | Données de démo |
| Mise à jour | Temps réel | Simulée |
| Hébergement | Localhost:3000 | pages.dev (en ligne) |

### Fichiers créés pour la version statique

1. **`api-mock.js`** : Données de démonstration
   - Simule les stats du serveur
   - Faux classement de 20 joueurs
   - Données réalistes

2. **`app-static.js`** : Application sans serveur
   - Remplace `app.js`
   - Utilise les données mockées
   - Simule les mises à jour temps réel

### Avantages de la version statique

✅ **Gratuit** : Hébergement illimité sur Cloudflare
✅ **Rapide** : CDN mondial de Cloudflare
✅ **Fiable** : 99.99% uptime
✅ **Simple** : Pas de serveur à gérer
✅ **Accessible** : URL publique .pages.dev

### Limitations

❌ Pas de données en temps réel (données mockées)
❌ Pas de connexion au serveur Battle.net
❌ Pas d'API REST fonctionnelle
❌ Classement non mis à jour automatiquement

---

## 📝 COMMANDES GIT UTILES

### Ajouter des modifications

```bash
# Ajouter tous les fichiers modifiés
git add .

# Ou ajouter seulement le dossier web
git add web/

# Commit
git commit -m "Description des modifications"

# Push vers GitHub
git push
```

### Voir l'état

```bash
# Voir les fichiers modifiés
git status

# Voir l'historique
git log --oneline

# Voir les différences
git diff
```

### Annuler des modifications

```bash
# Annuler les modifications d'un fichier
git checkout -- fichier.html

# Annuler le dernier commit (garder les modifications)
git reset --soft HEAD~1

# Annuler le dernier commit (tout supprimer)
git reset --hard HEAD~1
```

---

## 🌐 DOMAINE PERSONNALISÉ (Optionnel)

### Utiliser votre propre domaine

1. **Acheter un domaine** (ex: kofultimate.com)
   - Namecheap, Google Domains, etc.

2. **Dans Cloudflare Pages**
   - Aller dans votre projet
   - Onglet "Custom domains"
   - Cliquer sur "Set up a custom domain"

3. **Configurer les DNS**
   - Suivre les instructions de Cloudflare
   - Ajouter un CNAME vers votre site .pages.dev

4. **Activer HTTPS**
   - Automatique avec Cloudflare

---

## 🔄 MISES À JOUR AUTOMATIQUES

Cloudflare Pages redéploie automatiquement le site à chaque push sur GitHub !

**Workflow :**
```bash
1. Modifier les fichiers localement
2. git add . && git commit -m "Mise à jour"
3. git push
4. ⏳ Cloudflare redéploie automatiquement (1-2 min)
5. ✅ Site mis à jour !
```

---

## 📊 STATISTIQUES & ANALYTICS

### Voir les stats de votre site

1. Dans Cloudflare Pages, onglet "Analytics"
2. Vous verrez :
   - Nombre de visiteurs
   - Pages vues
   - Bande passante utilisée
   - Pays des visiteurs

### Ajouter Google Analytics (optionnel)

Dans `web/index.html`, avant `</head>` :

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## 🐛 DÉPANNAGE

### Le site ne se déploie pas

**Vérifier :**
1. Le repository GitHub est bien public ou Cloudflare a accès
2. Le dossier `web/` existe dans le repository
3. Les fichiers HTML sont bien dans `web/`
4. Pas d'erreurs dans le log de build Cloudflare

**Solution :**
```bash
# Vérifier que les fichiers sont bien commités
git status

# Si des fichiers sont manquants
git add web/
git commit -m "Ajout fichiers manquants"
git push
```

### Le site affiche une page blanche

**Causes possibles :**
1. Chemin incorrect dans `Build output directory`
2. Fichiers JavaScript avec des erreurs
3. Ressources externes bloquées

**Solution :**
- Vérifier la console du navigateur (F12)
- Dans Cloudflare Pages, vérifier que `Build output directory = web`

### Les styles ne s'appliquent pas

**Vérifier :**
- Le fichier `style.css` est bien dans `web/`
- Le lien dans HTML pointe vers `style.css` (pas `/style.css`)

### Les données ne s'affichent pas

**Normal pour la version statique !**
- La version statique utilise des données mockées
- Si les données ne s'affichent pas du tout, vérifier que `api-mock.js` et `app-static.js` sont bien chargés

---

## 🎨 PERSONNALISATION

### Modifier les données mockées

Dans `web/api-mock.js`, modifier :

```javascript
const API_MOCK = {
    stats: {
        onlinePlayers: 10,  // ← Modifier ici
        activeMatches: 5,
        totalMatches: 200,
        totalPlayers: 50
    },
    // ...
};
```

### Ajouter plus de joueurs au classement

Dans `web/api-mock.js`, ajouter dans le tableau `leaderboard` :

```javascript
{
    id: 21,
    username: "NouveauJoueur",
    elo: 700,
    wins: 5,
    losses: 65,
    win_rate: 7.1,
    status: "offline"
}
```

---

## 📈 ÉVOLUTIONS POSSIBLES

### Version 2.0 avec backend

Pour avoir des données réelles en ligne :

1. **Déployer le serveur Battle.net sur un VPS**
   - Heroku, DigitalOcean, AWS, etc.
   - Modifier `BATTLENET_SERVER.py` pour accepter les connexions externes

2. **Créer une API Cloudflare Workers**
   - Créer des Workers pour gérer les données
   - Connecter au serveur Battle.net

3. **Utiliser une base de données**
   - Cloudflare D1 (SQL)
   - Ou Firebase, Supabase, etc.

---

## ✅ CHECKLIST AVANT DÉPLOIEMENT

- [ ] Git initialisé
- [ ] Repository GitHub créé
- [ ] Fichiers `web/` commités
- [ ] `.gitignore` en place
- [ ] Compte Cloudflare créé
- [ ] Repository connecté à Cloudflare
- [ ] `Build output directory = web`
- [ ] Déploiement lancé
- [ ] Site accessible sur .pages.dev
- [ ] Test du site en ligne

---

## 🎉 FÉLICITATIONS !

Votre site est maintenant en ligne et accessible à tous sur Internet !

**URL par défaut :** `https://votre-projet.pages.dev`

**Partagez le lien avec vos amis et la communauté KOF !**

---

## 📞 SUPPORT

**Documentation Cloudflare Pages :**
https://developers.cloudflare.com/pages

**Problèmes ?**
1. Vérifier les logs de build dans Cloudflare
2. Vérifier la console navigateur (F12)
3. Consulter ce README

---

**Créé le :** 2025-10-29
**Version :** 1.0
**Hébergement :** Cloudflare Pages (gratuit)

🌐 **Votre site KOF Ultimate Online est maintenant mondial !**
