# KOF Ultimate - Guide Multijoueur

## 🎮 Vue d'ensemble

Ce guide vous explique comment jouer en ligne avec KOF Ultimate en utilisant **Ikemen GO**, un moteur compatible MUGEN avec support réseau intégré.

---

## 📋 Table des matières

1. [Installation Rapide](#installation-rapide)
2. [Configuration Réseau](#configuration-réseau)
3. [Héberger une Partie](#héberger-une-partie)
4. [Rejoindre une Partie](#rejoindre-une-partie)
5. [Alternative: Parsec](#alternative-parsec)
6. [Dépannage](#dépannage)

---

## ⚡ Installation Rapide

### Option A: Installation Automatique (Recommandé)

```bash
python install_ikemen.py
```

Ce script va:
1. Télécharger Ikemen GO automatiquement
2. Créer le dossier `D:\KOF Ultimate Online\`
3. Copier tous vos personnages et stages
4. Configurer automatiquement le jeu

### Option B: Installation Manuelle

1. **Télécharger Ikemen GO**
   - Site officiel: https://github.com/ikemen-engine/Ikemen-GO/releases
   - Téléchargez la dernière version Windows (fichier .zip)

2. **Extraire**
   - Créez le dossier: `D:\KOF Ultimate Online\`
   - Extrayez le contenu du .zip dans ce dossier

3. **Copier les Assets**
   ```
   Copiez depuis D:\KOF Ultimate\:
   - chars/     → D:\KOF Ultimate Online\chars\
   - stages/    → D:\KOF Ultimate Online\stages\
   - data/      → D:\KOF Ultimate Online\data\
   - sound/     → D:\KOF Ultimate Online\sound\
   - font/      → D:\KOF Ultimate Online\font\
   ```

4. **Configuration**
   - Lancez `Ikemen_GO.exe` une fois
   - Il créera automatiquement `save/config.json`
   - Éditez `data/select.def` si nécessaire

---

## 🌐 Configuration Réseau

### Pour l'Hébergeur (Host)

1. **Ouvrir le Port 7500**
   - Accédez à votre routeur (généralement http://192.168.1.1)
   - Trouvez la section "Port Forwarding" ou "NAT"
   - Créez une règle:
     - Port externe: 7500
     - Port interne: 7500
     - Protocole: TCP/UDP
     - IP: Votre IP locale (ex: 192.168.1.100)

2. **Trouver votre IP Publique**
   - Visitez: https://www.whatismyip.com/
   - Notez votre adresse IP publique
   - Partagez-la avec vos adversaires

3. **Configurer le Pare-feu Windows**
   ```powershell
   # Exécuter en tant qu'Administrateur
   New-NetFirewallRule -DisplayName "Ikemen GO" -Direction Inbound -Program "D:\KOF Ultimate Online\Ikemen_GO.exe" -Action Allow
   ```

### Pour le Joueur qui Rejoint

- Demandez l'IP publique de l'hébergeur
- Assurez-vous d'avoir exactement la même version du jeu
- Vérifiez que tous les personnages et stages sont identiques

---

## 🎯 Héberger une Partie

1. **Lancer Ikemen GO**
   ```
   D:\KOF Ultimate Online\Ikemen_GO.exe
   ```

2. **Dans le Menu Principal**
   - Sélectionnez **"NETWORK"** ou **"ONLINE"**
   - Choisissez **"HOST GAME"**
   - Le jeu affichera: `Waiting for Player 2...`
   - Votre port 7500 est maintenant ouvert

3. **Partager Votre IP**
   - Donnez votre IP publique à vos amis
   - Format: `123.456.789.012`

4. **Attendre la Connexion**
   - Le jeu détectera automatiquement quand un joueur se connecte
   - Vous passerez alors à l'écran de sélection

5. **Modes Disponibles**
   - Versus (1v1)
   - Arcade Coop
   - Survival Coop
   - Team Battles

---

## 🔗 Rejoindre une Partie

1. **Lancer Ikemen GO**

2. **Dans le Menu Principal**
   - Sélectionnez **"NETWORK"** ou **"ONLINE"**
   - Choisissez **"JOIN GAME"**

3. **Entrer l'IP**
   - Tapez l'IP publique de l'hébergeur
   - Exemple: `123.456.789.012`
   - Appuyez sur Entrée

4. **Connexion**
   - Le jeu tentera de se connecter
   - Si succès: vous verrez l'écran de sélection
   - Si échec: vérifiez l'IP et le port 7500

---

## 🚀 Alternative: Parsec (Plus Facile)

Si Ikemen GO est trop complexe, utilisez **Parsec** pour une solution immédiate:

### Installation Parsec

1. **Télécharger**
   - Site: https://parsec.app/downloads
   - Installez sur tous les PC (host + guests)

2. **Créer un Compte**
   - Gratuit
   - Nécessaire pour tous les joueurs

3. **Configuration Hôte**
   ```
   1. Lancez Parsec
   2. Connectez-vous
   3. Lancez KOF Ultimate
   4. Dans Parsec, cliquez "Share"
   5. Envoyez le lien à vos amis
   ```

4. **Rejoindre (Guest)**
   ```
   1. Lancez Parsec
   2. Connectez-vous
   3. Cliquez sur le lien de votre ami
   4. Vous verrez son écran
   5. Vos contrôles sont automatiquement mappés
   ```

### Avantages Parsec
- ✅ Pas de port forwarding
- ✅ Configuration 5 minutes
- ✅ Fonctionne avec MUGEN vanilla
- ✅ Guests n'ont pas besoin du jeu installé

### Inconvénients Parsec
- ❌ 60 FPS max (version gratuite)
- ❌ Latence dépend de la connexion
- ❌ Pas de vrai netcode

---

## 🛠 Dépannage

### Problème: Ne peut pas se connecter

**Solution 1: Vérifier le Port**
```bash
# Sur l'hôte, vérifier que le port est ouvert
netstat -an | findstr 7500
```

**Solution 2: Utiliser un VPN**
- Installez Hamachi ou ZeroTier
- Créez un réseau virtuel
- Connectez tous les joueurs au même réseau
- Utilisez l'IP VPN au lieu de l'IP publique

**Solution 3: Pare-feu**
```powershell
# Désactiver temporairement le pare-feu Windows (tests seulement)
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# Réactiver après
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

### Problème: Désynchronisation

**Causes:**
- Versions différentes du jeu
- Personnages/stages différents
- Fichiers modifiés différemment

**Solution:**
- Les deux joueurs doivent avoir EXACTEMENT les mêmes fichiers
- Utilisez le script de synchronisation:
  ```bash
  python sync_game_files.py --create-package
  ```
- Envoyez le package .zip à votre adversaire

### Problème: Lag/Latence

**Solutions:**
- Fermez les applications qui utilisent Internet
- Utilisez une connexion filaire (pas Wi-Fi)
- Vérifiez votre ping: `ping [IP_ADVERSAIRE]`
- Si > 100ms: le jeu sera difficile à jouer
- Ikemen GO rollback (version alpha) réduit le lag perçu

---

## 📊 Menu Multijoueur Personnalisé

Le menu multijoueur style Warcraft 3 est disponible dans Ikemen GO:

### Structure du Menu

```
MAIN MENU
├─ ARCADE
├─ VS MODE
├─ MULTIPLAYER ← Nouveau!
│  ├─ HOST GAME
│  │  ├─ Versus
│  │  ├─ Team Battle
│  │  └─ Survival Coop
│  ├─ JOIN GAME
│  │  └─ [Entrer IP]
│  ├─ LAN GAMES
│  │  └─ [Scan réseau local]
│  └─ OPTIONS
│     ├─ Port: 7500
│     └─ Latence: Auto/Fixed
├─ TRAINING
├─ OPTIONS
└─ EXIT
```

### Personnalisation

Éditez: `D:\KOF Ultimate Online\data\system.def`

```ini
[Title Info]
menu.itemname.network = "MULTIPLAYER"

[Network Info]
menu.itemname.host = "HOST GAME"
menu.itemname.join = "JOIN GAME"
menu.itemname.lan = "LAN GAMES"
```

---

## 🎯 Commandes Réseau

### Pendant un Match en Ligne

- **ESC**: Pause (les deux joueurs doivent confirmer)
- **F1**: Afficher les stats réseau (ping, paquets perdus)
- **F2**: Changer la qualité (Auto/Low/High)
- **F3**: Activer le mode rollback (si disponible)

### Chat (Si activé)

- **T**: Ouvrir le chat
- **Entrée**: Envoyer le message
- **Échap**: Fermer le chat

---

## 🔧 Scripts Utilitaires

### 1. Test de Connexion

```bash
python test_connection.py --ip [IP_ADVERSAIRE] --port 7500
```

### 2. Synchronisation des Fichiers

```bash
# Créer un package
python sync_game_files.py --create-package

# Installer un package reçu
python sync_game_files.py --install package.zip
```

### 3. Serveur Dédié

```bash
# Lancer un serveur persistant
python dedicated_server.py --port 7500 --max-players 8
```

---

## 🌟 Fonctionnalités Avancées

### Rollback Netcode (Expérimental)

Ikemen GO propose une version alpha avec rollback:

```bash
# Télécharger la version rollback
# https://github.com/assemblaj/Ikemen-GO/releases

# Activer dans config.json
{
  "Network": {
    "RollbackEnabled": true,
    "RollbackFrames": 7
  }
}
```

### Lobby Public (Communauté)

Rejoignez le Discord MUGEN pour trouver des adversaires:
- Aiki's Mugen Server: 4,468 membres
- M.U.G.E.N Battle Hub

---

## 📞 Support

- **Discord**: Rejoignez notre serveur (lien dans README)
- **GitHub**: Signalez les bugs
- **Documentation**: Voir `/docs` pour plus d'infos

---

## ✅ Checklist Rapide

### Avant de Jouer

- [ ] Ikemen GO installé
- [ ] Port 7500 ouvert (hôte seulement)
- [ ] IP publique connue (hôte)
- [ ] Pare-feu configuré
- [ ] Même version du jeu (tous)
- [ ] Connexion stable (ping < 100ms)

### Première Partie

- [ ] Hôte lance "HOST GAME"
- [ ] Hôte partage son IP
- [ ] Guest lance "JOIN GAME"
- [ ] Guest entre l'IP
- [ ] Connexion établie ✓
- [ ] Sélection des personnages
- [ ] Combat!

---

**Bon jeu! 🎮**

*Dernière mise à jour: 2025*
