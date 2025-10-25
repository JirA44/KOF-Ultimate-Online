# ☁️ GUIDE CLOUDFLARE - KOF Ultimate Online

Guide rapide pour déployer le backend sur Cloudflare et exposer votre API.

---

## 🎯 OPTIONS DE DÉPLOIEMENT

Vous avez **3 options** pour exposer votre backend:

### Option 1: Cloudflare Tunnel (Recommandé pour dev/test)
**Avantages:**
- ✅ Gratuit
- ✅ Setup rapide (5 min)
- ✅ HTTPS automatique
- ✅ Pas besoin de domaine

**Inconvénients:**
- ❌ Tunnel doit rester actif

### Option 2: Cloudflare Worker (Production)
**Avantages:**
- ✅ Edge computing global
- ✅ Ultra rapide
- ✅ Scalable automatiquement

**Inconvénients:**
- ❌ Backend doit être accessible publiquement

### Option 3: Cloudflare Pages + Worker (Full stack)
**Avantages:**
- ✅ Frontend + Backend ensemble
- ✅ Deploy automatique depuis Git

---

## 🚀 OPTION 1: CLOUDFLARE TUNNEL (Rapide)

Exposez votre backend local sur Internet via Cloudflare.

### Étape 1: Installer cloudflared

**Windows:**
```bash
winget install Cloudflare.cloudflared
```

**Vérifier installation:**
```bash
cloudflared --version
```

### Étape 2: Login Cloudflare

```bash
cloudflared tunnel login
```

Un navigateur s'ouvrira. Connectez-vous et autorisez.

### Étape 3: Créer un tunnel

```bash
cloudflared tunnel create kof-ultimate
```

**Note:** Gardez l'UUID généré (tunnel ID)

### Étape 4: Configurer le tunnel

Créez `tunnel-config.yml` dans `C:\Users\VotreNom\.cloudflared\`:

```yaml
tunnel: VOTRE_TUNNEL_ID
credentials-file: C:\Users\VotreNom\.cloudflared\VOTRE_TUNNEL_ID.json

ingress:
  # API Server
  - hostname: kof-api.votre-domaine.com
    service: http://localhost:3100

  # Matchmaking (WebSocket)
  - hostname: kof-ws.votre-domaine.com
    service: http://localhost:3101

  # Catch-all
  - service: http_status:404
```

### Étape 5: Router le DNS

```bash
# API
cloudflared tunnel route dns kof-ultimate kof-api.votre-domaine.com

# WebSocket
cloudflared tunnel route dns kof-ultimate kof-ws.votre-domaine.com
```

### Étape 6: Démarrer le tunnel

```bash
cloudflared tunnel run kof-ultimate
```

**OU en arrière-plan:**
```bash
cloudflared tunnel run kof-ultimate --config tunnel-config.yml
```

### Étape 7: Tester

```bash
curl https://kof-api.votre-domaine.com/api/health
```

**Success! 🎉** Votre API est maintenant accessible via HTTPS.

---

## 🌐 OPTION 2: CLOUDFLARE WORKER

Déployez votre API directement sur le réseau Cloudflare.

### Prérequis

- Backend accessible publiquement (via tunnel ou serveur)
- Node.js 16+

### Étape 1: Installer Wrangler

```bash
npm install -g wrangler
```

### Étape 2: Login Cloudflare

```bash
wrangler login
```

### Étape 3: Obtenir Account ID

1. Allez sur https://dash.cloudflare.com/
2. Workers & Pages → Overview
3. Copiez votre **Account ID**

### Étape 4: Configurer wrangler.toml

```toml
name = "kof-ultimate-online-api"
main = "cloudflare_worker.js"
compatibility_date = "2024-01-01"
account_id = "VOTRE_ACCOUNT_ID"

[vars]
BACKEND_API_URL = "https://kof-api.votre-domaine.com"
```

### Étape 5: Modifier cloudflare_worker.js

Changez la ligne:
```javascript
const BACKEND_API_URL = 'YOUR_BACKEND_URL';
```

En:
```javascript
const BACKEND_API_URL = 'https://kof-api.votre-domaine.com';
```

### Étape 6: Deploy

```bash
wrangler publish
```

**Output:**
```
✅ Uploaded kof-ultimate-online-api
✅ Published kof-ultimate-online-api
   https://kof-ultimate-online-api.your-subdomain.workers.dev
```

### Étape 7: Tester

```bash
curl https://kof-ultimate-online-api.your-subdomain.workers.dev/api/health
```

---

## 🔧 CONFIGURATION AVANCÉE

### Custom Domain

1. Dashboard Cloudflare → Workers → kof-ultimate-online-api
2. Triggers → Custom Domains
3. Add Custom Domain: `api.votre-domaine.com`

### Secrets (Variables sécurisées)

```bash
# JWT Secret
wrangler secret put JWT_SECRET
# Tapez votre secret et Enter

# API Key
wrangler secret put API_KEY
```

### KV Storage (Cache)

```bash
# Créer namespace
wrangler kv:namespace create "KOF_CACHE"

# Ajouter à wrangler.toml
kv_namespaces = [
  { binding = "KOF_CACHE", id = "VOTRE_KV_ID" }
]
```

---

## 🎮 LANCER LE SYSTÈME COMPLET

### 1. Démarrer le backend local

```bash
cd "D:\KOF Ultimate Online\online_backend"
START_BACKEND_COMPLETE.bat
```

**Vérifie que:**
- ✅ API Server → http://localhost:3100
- ✅ Matchmaking → ws://localhost:3101

### 2. Démarrer le tunnel Cloudflare

**Nouvelle fenêtre CMD:**
```bash
cloudflared tunnel run kof-ultimate
```

**Vérifie que:**
- ✅ API accessible via https://kof-api.votre-domaine.com
- ✅ WS accessible via https://kof-ws.votre-domaine.com

### 3. (Optionnel) Deploy Worker

```bash
wrangler publish
```

---

## 🧪 TESTS

### Test API locale

```bash
curl http://localhost:3100/api/health
```

### Test API via Tunnel

```bash
curl https://kof-api.votre-domaine.com/api/health
```

### Test API via Worker

```bash
curl https://kof-ultimate-online-api.your-subdomain.workers.dev/api/health
```

### Test WebSocket

```javascript
const ws = new WebSocket('wss://kof-ws.votre-domaine.com');

ws.on('open', () => {
  console.log('✅ WebSocket connecté!');
  ws.send(JSON.stringify({
    type: 'ping'
  }));
});

ws.on('message', (data) => {
  console.log('📩 Message:', data.toString());
});
```

---

## 📊 MONITORING

### Cloudflare Dashboard

- Workers & Pages → kof-ultimate-online-api
- Metrics → Requêtes, Erreurs, Latence
- Logs → Real-time logs

### Tunnel Status

```bash
cloudflared tunnel info kof-ultimate
```

### Logs en temps réel

```bash
wrangler tail
```

---

## 🔒 SÉCURITÉ

### 1. Rate Limiting

Dashboard → Security → WAF → Rate Limiting Rules

```
Si requêtes > 100/minute depuis même IP
Alors bloquer pendant 10 minutes
```

### 2. Firewall Rules

Bloquer pays/IPs spécifiques:

```
(ip.geoip.country ne "FR" et ip.geoip.country ne "BE")
et (http.request.uri.path contains "/api/")
```

### 3. SSL/TLS

Dashboard → SSL/TLS → Overview
Mode: **Full (strict)**

### 4. Bot Protection

Dashboard → Security → Bots
Mode: **Fight** ou **Challenge**

---

## 💰 COÛTS

### Cloudflare Tunnel
- **Gratuit** ✅

### Cloudflare Workers
- **Plan gratuit:** 100,000 requêtes/jour
- **Workers Paid ($5/mois):** 10M requêtes/mois
- Au-delà: $0.50 par million

### Cloudflare KV
- **Gratuit:** 100,000 reads/day
- **KV Paid:** Illimité

---

## 🆘 TROUBLESHOOTING

### Tunnel ne démarre pas

```bash
# Vérifier statut
cloudflared tunnel list

# Supprimer et recréer
cloudflared tunnel delete kof-ultimate
cloudflared tunnel create kof-ultimate
```

### Worker erreur 502

Vérifiez que `BACKEND_API_URL` est correct dans `cloudflare_worker.js`

### WebSocket ne connecte pas

Assurez-vous d'utiliser `wss://` (pas `ws://`) via tunnel.

### CORS errors

Ajoutez votre domaine dans `.env`:
```env
ALLOWED_ORIGINS=https://votre-frontend.com,https://autre-domaine.com
```

---

## 📚 RESSOURCES

- [Cloudflare Tunnel Docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [Wrangler CLI Docs](https://developers.cloudflare.com/workers/wrangler/)

---

## ✅ CHECKLIST DÉPLOIEMENT

Avant de lancer en production:

- [ ] JWT_SECRET changé et sécurisé
- [ ] Tunnel configuré et testé
- [ ] Worker déployé et fonctionnel
- [ ] Custom domain configuré
- [ ] SSL/TLS en mode Full (strict)
- [ ] Rate limiting activé
- [ ] Firewall rules configurées
- [ ] Monitoring et logs actifs
- [ ] Backups base de données programmés
- [ ] Documentation à jour

---

**Créé pour KOF Ultimate Online v2.0**
