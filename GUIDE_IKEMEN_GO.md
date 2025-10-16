# 🎮 Guide d'installation Ikemen GO pour KOF Ultimate

## Qu'est-ce qu'Ikemen GO?

**Ikemen GO** est un moteur de jeu de combat open-source compatible avec MUGEN qui ajoute:
- ✅ **Multijoueur en ligne** (netplay)
- ✅ **Meilleure performance** que MUGEN classique
- ✅ **Support résolution HD**
- ✅ **Modes de jeu avancés**
- ✅ **Compatibilité avec vos personnages MUGEN existants**

## 🚀 Installation rapide

### Option 1: Installation automatique (Recommandé)

1. **Double-cliquez** sur `install_ikemen_go.bat`
2. Choisissez l'option 1 pour le téléchargement automatique
3. Attendez la fin de l'installation
4. C'est fait!

### Option 2: Installation manuelle

1. **Téléchargez** Ikemen GO:
   - Allez sur: https://github.com/ikemen-engine/Ikemen-GO/releases/latest
   - Téléchargez: `Ikemen_GO_Win.zip`

2. **Extrayez** le fichier dans:
   ```
   D:\KOF Ultimate Online\
   ```

3. **Structure des fichiers**:
   ```
   D:\KOF Ultimate Online\
   ├── Ikemen_GO.exe          ← Le jeu
   ├── data\
   │   ├── mugen.cfg          ← Configuration
   │   └── screenpack\        ← Interface
   ├── chars\                 ← Personnages
   ├── stages\                ← Stages/Maps
   ├── sound\                 ← Musiques
   └── external\              ← Dépendances
   ```

## 📦 Configuration initiale

### 1. Copier vos personnages

```batch
REM Copiez vos personnages KOF depuis:
D:\KOF Ultimate\chars\*

REM Vers:
D:\KOF Ultimate Online\chars\
```

### 2. Copier vos stages

```batch
REM Copiez vos stages depuis:
D:\KOF Ultimate\stages\*

REM Vers:
D:\KOF Ultimate Online\stages\
```

### 3. Configuration résolution

Éditez `D:\KOF Ultimate Online\data\config.json`:

```json
{
  "GameWidth": 1280,
  "GameHeight": 720,
  "Fullscreen": false,
  "MSAA": true,
  "AIRamping": true
}
```

## 🌐 Configuration du multijoueur

### Mode 1: Partie locale (même réseau)

1. **Joueur 1 (Hôte)**:
   - Lancez Ikemen GO
   - Menu → Network → Host Game
   - Notez votre IP locale (ex: 192.168.1.10)

2. **Joueur 2**:
   - Menu → Network → Join Game
   - Entrez l'IP du joueur 1
   - Connectez-vous!

### Mode 2: Partie en ligne (Internet)

**Nécessite la redirection de port ou utilisation de services comme:**
- Hamachi
- Radmin VPN
- ZeroTier

**Configuration:**
1. Installez un service VPN gaming (ex: Radmin VPN - gratuit)
2. Créez un réseau ou rejoignez-en un
3. Utilisez l'IP VPN pour vous connecter

### Configuration du port

Dans `save\config.json`:
```json
{
  "ListenPort": "7500"
}
```

Redirigez le port **7500** (TCP et UDP) dans votre routeur.

## ⚙️ Configurations recommandées

### Pour performance maximale

`data\config.json`:
```json
{
  "GameWidth": 1280,
  "GameHeight": 720,
  "Fullscreen": true,
  "VRetrace": 1,
  "MSAA": false,
  "MaxBPS": 60,
  "AudioSampleRate": 48000
}
```

### Pour qualité maximale

```json
{
  "GameWidth": 1920,
  "GameHeight": 1080,
  "Fullscreen": true,
  "VRetrace": 1,
  "MSAA": true,
  "MaxBPS": 60,
  "AudioSampleRate": 48000,
  "PostProcessingShader": 1
}
```

## 🎨 Personnalisation de l'interface

### Ajouter un screenpack personnalisé

1. Téléchargez un screenpack pour Ikemen GO
2. Extrayez dans `data\`
3. Éditez `save\config.json`:
   ```json
   {
     "Motif": "data/votre_screenpack.def"
   }
   ```

### Ajouter de la musique

Placez vos fichiers MP3/OGG dans:
```
sound\
├── menu.mp3
├── select.mp3
└── versus.mp3
```

Référencez-les dans votre screenpack `.def`

## 🔧 Résolution de problèmes

### Le jeu ne démarre pas
- Vérifiez que tous les fichiers sont extraits
- Installez Visual C++ Redistributable 2019
- Vérifiez les droits d'administration

### Lag en multijoueur
1. Vérifiez votre ping
2. Activez le "Input Delay" dans les options réseau
3. Fermez les applications gourmandes en bande passante

### Personnages MUGEN incompatibles
- Certains personnages complexes peuvent ne pas fonctionner
- Mettez à jour vers les versions compatibles Ikemen GO

### Audio crackling
Changez le `AudioSampleRate` dans config.json:
```json
"AudioSampleRate": 44100
```

## 📊 Comparaison MUGEN vs Ikemen GO

| Fonctionnalité | MUGEN | Ikemen GO |
|----------------|-------|-----------|
| Multijoueur en ligne | ❌ | ✅ |
| Résolution HD | Limité | ✅ |
| Performance | Moyenne | Excellente |
| Modes de jeu | Basique | Avancés |
| Compatibilité personnages | 100% | 95% |
| Open source | ❌ | ✅ |
| Développement actif | ❌ | ✅ |

## 🎯 Intégration avec KOF Ultimate Launcher

Le launcher détecte automatiquement Ikemen GO si installé dans:
```
D:\KOF Ultimate Online\Ikemen_GO.exe
```

Le bouton **🌐 MULTIJOUEUR** lancera automatiquement Ikemen GO.

## 📚 Ressources utiles

- **Site officiel**: https://mugenguild.com/forum/topics/ikemen-go-184152.0.html
- **GitHub**: https://github.com/ikemen-engine/Ikemen-GO
- **Discord**: https://discord.gg/ikemen
- **Tutoriels**: https://ikemen-engine.github.io/Ikemen-GO/

## 🆘 Support

En cas de problème:
1. Consultez les logs dans `Ikemen_GO.log`
2. Visitez le Discord officiel
3. Ouvrez une issue sur GitHub

## 🔄 Mise à jour

Pour mettre à jour Ikemen GO:
1. Téléchargez la dernière version
2. Sauvegardez vos fichiers `save\`, `chars\`, `stages\`
3. Extrayez la nouvelle version
4. Restaurez vos fichiers sauvegardés

---

**Bon jeu! 🎮**
