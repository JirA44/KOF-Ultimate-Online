# 🌐 SITE WEB KOF ULTIMATE ONLINE

## 📋 Vue d'ensemble

Le site web de KOF Ultimate Online est une interface complète pour consulter les statistiques du serveur, le classement des joueurs et surveiller l'activité en temps réel.

---

## 🚀 DÉMARRAGE RAPIDE

### Prérequis

- ✅ **Node.js 14+** installé ([Télécharger](https://nodejs.org/))
- ✅ Le serveur Battle.net doit être lancé (`BATTLENET_SERVER.py`)

### Installation

1. **Installer les dépendances**
   ```bash
   npm install
   ```

2. **Lancer le serveur web**
   ```bash
   npm start
   ```

   **OU** double-cliquer sur :
   ```
   LAUNCH_WEB_SERVER.bat
   ```

3. **Accéder au site**
   - Ouvrir un navigateur
   - Aller sur : `http://localhost:3000`

---

## 📑 PAGES DISPONIBLES

### 🏠 Page d'Accueil (`index.html`)

**URL :** `http://localhost:3000/`

**Contenu :**
- Vue d'ensemble du système
- Statistiques en temps réel
- Top 10 joueurs
- Guide d'installation
- Fonctionnalités

### 📊 Dashboard (`dashboard.html`)

**URL :** `http://localhost:3000/dashboard.html`

**Contenu :**
- Statistiques en temps réel
- Statut des services
- Graphique d'activité des matchs
- Joueurs actifs
- Journal d'activité

**Mises à jour :**
- Stats : Toutes les 5 secondes
- Statut services : Toutes les 2 secondes
- WebSocket : Temps réel

### 🏆 Classement (`leaderboard.html`)

**URL :** `http://localhost:3000/leaderboard.html`

**Contenu :**
- Podium Top 3
- Classement complet
- Recherche de joueurs
- Filtres (Tous, En ligne, Top 50)
- Rangs ELO (Diamond, Platinum, Gold, Silver, Bronze)

**Mises à jour :**
- Classement : Toutes les 30 secondes
- Statut joueurs : Temps réel

---

## 🔌 API REST

Le serveur web expose plusieurs endpoints API :

### GET `/api/stats`

Retourne les statistiques du serveur.

**Réponse :**
```json
{
  "success": true,
  "data": {
    "totalPlayers": 10,
    "onlinePlayers": 3,
    "activeMatches": 1,
    "totalMatches": 25
  },
  "lastUpdate": "2025-10-29T12:34:56.789Z"
}
```

### GET `/api/leaderboard`

Retourne le classement complet (Top 100).

**Réponse :**
```json
{
  "success": true,
  "data": [
    {
      "id": "player1",
      "username": "ProGamer",
      "elo": 1500,
      "wins": 10,
      "losses": 5,
      "win_rate": 66.7,
      "status": "online"
    },
    ...
  ]
}
```

### GET `/api/players`

Retourne tous les joueurs en ligne.

**Réponse :**
```json
{
  "success": true,
  "data": [...]
}
```

### GET `/api/health`

Health check du serveur.

**Réponse :**
```json
{
  "success": true,
  "status": "running",
  "battlenet": true
}
```

---

## 🔄 WEBSOCKET

Le serveur expose également un endpoint WebSocket pour les mises à jour en temps réel.

**URL :** `ws://localhost:3000`

**Messages reçus :**

```json
// Stats update
{
  "type": "stats",
  "data": {
    "onlinePlayers": 3,
    "activeMatches": 1,
    ...
  }
}

// Leaderboard update
{
  "type": "leaderboard",
  "data": [...]
}
```

**Exemple de connexion :**
```javascript
const ws = new WebSocket('ws://localhost:3000');

ws.onopen = () => {
  console.log('Connecté au serveur');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Message reçu:', data);
};
```

---

## 🏗️ ARCHITECTURE

```
web_server.js          → Serveur Node.js principal
├── HTTP Server        → Serveur de fichiers statiques
├── WebSocket Server   → Mises à jour temps réel
└── API REST           → Endpoints /api/*

web/
├── index.html         → Page d'accueil
├── dashboard.html     → Dashboard temps réel
├── leaderboard.html   → Classement ELO
├── style.css          → Styles globaux
└── app.js             → Application JavaScript
```

---

## ⚙️ CONFIGURATION

### Modifier le port du serveur web

Dans `web_server.js` ligne 7 :
```javascript
const PORT = 3000; // Changer ici
```

### Modifier l'URL du serveur Battle.net

Dans `web_server.js` ligne 8 :
```javascript
const BATTLENET_WS_URL = 'ws://localhost:8765'; // Changer ici
```

### Modifier l'API dans les pages web

Dans `web/app.js` ligne 4 :
```javascript
const API_BASE = 'http://localhost:3000/api'; // Changer ici
```

---

## 🎨 DESIGN

Le site utilise un design moderne avec :

- **Couleurs :**
  - Primary : `#00d4ff` (Cyan)
  - Secondary : `#1e3a8a` (Bleu foncé)
  - Background : `#0a0e27` (Noir bleuté)
  - Success : `#00ff88` (Vert)
  - Error : `#ff0055` (Rouge)

- **Animations :**
  - Background animé avec gradient
  - Effets de hover sur les cartes
  - Compteurs animés
  - Indicateurs de statut clignotants

- **Responsive :**
  - Adapté aux écrans desktop, tablette et mobile
  - Grille flexible
  - Navigation mobile-friendly

---

## 🐛 DÉPANNAGE

### Le serveur ne démarre pas

**Problème :** `Error: Cannot find module 'ws'`

**Solution :**
```bash
npm install ws
```

---

### Le serveur web ne se connecte pas au serveur Battle.net

**Vérification :**
1. Le serveur Battle.net est-il lancé ?
   ```bash
   python BATTLENET_SERVER.py
   ```

2. Le port 8765 est-il accessible ?
   ```bash
   netstat -ano | findstr 8765
   ```

**Solution :**
- Lancer le serveur Battle.net d'abord
- Vérifier que l'URL est correcte dans `web_server.js`

---

### Les stats ne s'affichent pas

**Vérification :**
1. Ouvrir la console du navigateur (F12)
2. Vérifier les erreurs JavaScript
3. Vérifier la connexion WebSocket

**Solution :**
- Rafraîchir la page (Ctrl+R)
- Vérifier que le serveur web est lancé
- Vérifier que l'API REST fonctionne : `http://localhost:3000/api/stats`

---

### Erreur CORS (Cross-Origin)

**Problème :** Les requêtes API sont bloquées

**Solution :**
Le serveur inclut déjà les headers CORS :
```javascript
res.setHeader('Access-Control-Allow-Origin', '*');
```

Si le problème persiste, vérifier que vous accédez au site via `http://localhost:3000` et non `file://`.

---

## 📊 STATISTIQUES

### Métriques suivies

- **Joueurs en ligne** : Nombre de joueurs actuellement connectés
- **Matchs actifs** : Nombre de parties en cours
- **Total matchs** : Nombre total de parties jouées
- **Joueurs inscrits** : Nombre total de comptes créés

### Fréquence de mise à jour

- WebSocket : Temps réel
- API REST : Sur demande
- Dashboard : 5 secondes
- Classement : 30 secondes

---

## 🚀 AMÉLIORATIONS FUTURES

- [ ] Page de profil joueur détaillé
- [ ] Historique des matchs
- [ ] Graphiques interactifs (Chart.js)
- [ ] Système de notifications
- [ ] Chat intégré
- [ ] Thème clair/sombre
- [ ] Multi-langue (FR/EN)
- [ ] Mode admin
- [ ] Export des stats (CSV, JSON)
- [ ] Recherche avancée

---

## 💻 DÉVELOPPEMENT

### Structure des fichiers

```
web/
├── index.html          # Page d'accueil
├── dashboard.html      # Dashboard
├── leaderboard.html    # Classement
├── style.css           # Styles globaux
└── app.js              # Application JS

web_server.js           # Serveur Node.js
package.json            # Dépendances npm
```

### Ajouter une nouvelle page

1. Créer le fichier HTML dans `web/`
2. Inclure `style.css` et `app.js`
3. Ajouter le lien dans la navigation

**Exemple :**
```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="main-header">
        <nav class="main-nav">
            <a href="nouvelle-page.html" class="active">Nouvelle Page</a>
        </nav>
    </header>

    <main class="container">
        <!-- Contenu -->
    </main>

    <script src="app.js"></script>
</body>
</html>
```

### Ajouter un nouvel endpoint API

Dans `web_server.js`, fonction `handleApiRequest` :

```javascript
else if (url === '/api/mon-endpoint') {
    res.writeHead(200);
    res.end(JSON.stringify({
        success: true,
        data: { ... }
    }));
}
```

---

## 📝 NOTES

- Le serveur web est indépendant du jeu et du serveur Battle.net
- Il se connecte au serveur Battle.net pour récupérer les données
- Toutes les stats sont en temps réel via WebSocket
- Le site est accessible uniquement en local par défaut

**Pour rendre le site accessible sur Internet :**
1. Configurer le port forwarding (port 3000)
2. Utiliser un service comme ngrok
3. Déployer sur un serveur cloud (AWS, Heroku, etc.)

---

## 📞 SUPPORT

En cas de problème :

1. Vérifier les logs du serveur web
2. Vérifier la console du navigateur (F12)
3. Consulter `README_SYSTÈME_COMPLET.md`
4. Vérifier que tous les services sont lancés

---

**Créé le :** 2025-10-29
**Version :** 1.0
**Port par défaut :** 3000

🌐 **Profitez du site web KOF Ultimate Online !**
