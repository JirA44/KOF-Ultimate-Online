# Guide des Backgrounds et Stages - KOF Ultimate

## Table des Matières
1. [Introduction](#introduction)
2. [Structure des Stages](#structure-des-stages)
3. [Créer un Nouveau Stage](#créer-un-nouveau-stage)
4. [Format et Spécifications](#format-et-spécifications)
5. [Suggestions de Thèmes](#suggestions-de-thèmes)
6. [Intégration au Jeu](#intégration-au-jeu)
7. [Optimisation](#optimisation)
8. [Troubleshooting](#troubleshooting)

---

## Introduction

Les stages (arènes/backgrounds) dans KOF Ultimate sont définis par deux fichiers principaux:
- **`.def`**: Fichier de définition contenant la configuration
- **`.sff`**: Fichier sprite contenant les images/animations

**Emplacement**: `D:\KOF Ultimate\stages\`

---

## Structure des Stages

### Fichiers Actuels

Le jeu contient actuellement **25 stages uniques**:

```
stages/
├── Abyss-Rugal-Palace.def/.sff      (9.7 MB)
├── Anime Blu.def/.sff               (625 KB)
├── Anubis.def/.sff                  (2.5 MB)
├── Basque Palace.def/.sff           (2.7 MB)
├── BLACK SON DROTIME.def/.sff       (716 KB)
├── Black wall.def/.sff              (1.9 MB)
├── clones lab destroyed.def/.sff    (1.1 MB)
├── DARK SAID RUGAL S.def/.sff       (652 KB)
├── Darkness.def/.sff                (3.7 MB)
├── DROBLOOD R 2.0.def/.sff          (2.2 MB)
├── Exagon Force.def/.sff            (30 KB)
├── Far from here.def/.sff           (5.5 MB)
├── forest infernal fire.def/.sff    (939 KB)
├── Galaxy BG.def/.sff               (410 KB)
├── light kyouki.def/.sff            (12 MB)
├── Moon of dark wall.def/.sff       (1 MB)
├── Moon recidence.def/.sff          (912 KB)
├── O.DB DRORANGE BLACK.def/.sff     (1.4 MB)
├── Palece Mistery R.def/.sff        (204 KB)
├── RED.def/.sff                     (4.3 MB)
├── Red_Cliff.def/.sff               (10 MB)
├── The Will Of Hades S.def/.sff     (2.5 MB)
├── TIME INGCODNITA.def/.sff         (2.4 MB)
├── Wall of paintings.def/.sff       (1.2 MB)
└── xX-Hell-Dark-Xx.def/.sff         (1.9 MB)
```

### Tailles Recommandées

| Type | Petite | Moyenne | Grande |
|------|--------|---------|---------|
| Statique | < 500 KB | 500 KB - 2 MB | > 2 MB |
| Animée | < 1 MB | 1 MB - 5 MB | > 5 MB |

**Note**: Les stages de plus de 5 MB peuvent causer des ralentissements sur les PC moins puissants.

---

## Créer un Nouveau Stage

### Méthode 1: À partir d'un Template

#### Étape 1: Copier un Stage Existant

```bash
# Choisissez un stage simple comme template
cp "stages/Anime Blu.def" "stages/MyNewStage.def"
cp "stages/Anime Blu.sff" "stages/MyNewStage.sff"
```

#### Étape 2: Éditer le Fichier .def

Ouvrez `MyNewStage.def` avec un éditeur de texte et modifiez:

```ini
[Info]
name = "MyNewStage"
displayname = "My Awesome Stage"
mugenversion = 1.0
author = "Votre Nom"

[Camera]
startx = 0
starty = 0
boundleft = -139
boundright = 139
boundhigh = -20
boundlow = 0
tension = 100
verticalfollow = .75
floortension = 100

[PlayerInfo]
p1startx = -70      ; Position X du joueur 1
p1starty = 0        ; Position Y du joueur 1
p1startz = 0
p1facing = 1        ; Facing droite
p2startx = 70       ; Position X du joueur 2
p2starty = 0
p2startz = 0
p2facing = -1       ; Facing gauche
leftbound = -1000
rightbound = 1000
topbound = 0
botbound = 0

[Bound]
screenleft = 20
screenright = 20

[StageInfo]
zoffset = 227       ; Profondeur du stage
autoturn = 1        ; Les joueurs se tournent auto
resetBG = 0
Hires = 1           ; 1 = Haute résolution

[Scaling]
topz = 0
botz = 50
topscale = 1
botscale = 1.2

[Shadow]
color = 0,0,0
yscale = .2

[Reflection]
intensity = 90      ; Intensité du reflet (si eau)

[Music]
bgmusic = sound/your_music.ogg
bgvolume = 255

[BGdef]
spr = stages/MyNewStage.sff
debugbg = 0

[BG image]
type = normal
spriteno = 0, 0     ; Sprite ID dans le .sff
start = 0, -257     ; Position de départ
delta = 2, 2        ; Vitesse de parallaxe
```

#### Étape 3: Créer le Fichier .sff

**Option A: Utiliser Fighter Factory**
1. Téléchargez Fighter Factory (outil MUGEN gratuit)
2. Créez un nouveau fichier SFF
3. Importez vos images de background
4. Sauvegardez comme `MyNewStage.sff`

**Option B: Utiliser un Stage Builder**
1. Téléchargez MUGEN Stage Builder
2. Importez votre image de fond
3. Configurez les couches de parallaxe
4. Exportez en .sff

### Méthode 2: Convertir une Image Existante

#### Prérequis
- Image de fond (1920x1080 recommandé)
- Fighter Factory Classic
- Éditeur de texte

#### Étapes

1. **Préparer l'image**:
   - Format: PNG ou JPG
   - Résolution: 1920x1080 ou 1280x720
   - Optimiser la taille du fichier

2. **Créer le .sff avec Fighter Factory**:
   ```
   File > New > SFF File
   Insert > Add Sprite
   Sélectionnez votre image
   Group: 0, Index: 0
   Save As: MyStage.sff
   ```

3. **Créer le .def** (voir template ci-dessus)

4. **Tester dans MUGEN**:
   ```
   Ajoutez à data/select.def:

   [ExtraStages]
   stages/MyStage.def
   ```

---

## Format et Spécifications

### Images de Background

#### Résolutions Recommandées

| Type | Résolution | Ratio | Usage |
|------|-----------|-------|-------|
| SD | 640x480 | 4:3 | Compatibilité maximale |
| HD | 1280x720 | 16:9 | Recommandé |
| Full HD | 1920x1080 | 16:9 | Haute qualité |
| 4K | 3840x2160 | 16:9 | Ultra (lent) |

#### Formats Supportés

- **PNG**: Transparence, meilleure qualité, fichiers plus gros
- **JPG**: Pas de transparence, bonne qualité, fichiers plus petits
- **PCX**: Format MUGEN natif (obsolète)

#### Couleurs

- **Profondeur**: 24-bit ou 32-bit
- **Palette**: RGB complet recommandé
- **Transparence**: Utiliser PNG avec canal alpha

### Animations

Pour créer des backgrounds animés:

```ini
[BG AnimatedLayer]
type = anim
actionno = 1        ; Numéro de l'animation
start = 0, -257
delta = 2, 2

[Begin Action 1]
0,0, 0,0, 5, , A    ; Sprite 0,0 pour 5 ticks
0,1, 0,0, 5, , A    ; Sprite 0,1 pour 5 ticks
0,2, 0,0, 5, , A    ; Sprite 0,2 pour 5 ticks
```

### Parallaxe

Pour créer de la profondeur avec des couches multiples:

```ini
; Couche arrière (lente)
[BG Layer1]
type = normal
spriteno = 0, 0
delta = 0.5, 0.5    ; Défilement lent

; Couche milieu (normale)
[BG Layer2]
type = normal
spriteno = 0, 1
delta = 1, 1        ; Défilement normal

; Couche avant (rapide)
[BG Layer3]
type = normal
spriteno = 0, 2
delta = 2, 2        ; Défilement rapide
```

---

## Suggestions de Thèmes

### Thèmes Manquants / À Créer

#### 1. Temple Mystique
**Description**: Temple asiatique avec colonnes et lanternes
**Ambiance**: Spirituel, mystique, paisible
**Éléments**:
- Colonnes rouges traditionnelles
- Lanternes suspendues (animées)
- Cerisiers en fleurs
- Brume légère au sol
**Couleurs dominantes**: Rouge, or, rose pastel
**Taille recommandée**: 2-3 MB

#### 2. Ville Cyberpunk
**Description**: Métropole futuriste nocturne
**Ambiance**: Néon, high-tech, pluie
**Éléments**:
- Gratte-ciels avec publicités néon
- Pluie animée
- Véhicules volants en arrière-plan
- Reflets au sol mouillé
**Couleurs dominantes**: Bleu néon, violet, cyan
**Taille recommandée**: 4-5 MB

#### 3. Forêt Enchantée
**Description**: Forêt magique avec créatures fantastiques
**Ambiance**: Féerique, lumineux, nature
**Éléments**:
- Arbres géants bioluminescents
- Papillons/lucioles animés
- Cascade en arrière-plan
- Champignons géants
**Couleurs dominantes**: Vert émeraude, bleu clair, blanc
**Taille recommandée**: 3-4 MB

#### 4. Station Spatiale
**Description**: Intérieur de station orbitale
**Ambiance**: Sci-fi, zéro gravité, espace
**Éléments**:
- Hublots montrant l'espace
- Panneaux lumineux
- Planète visible au loin
- Débris flottants (animés)
**Couleurs dominantes**: Gris métallique, bleu froid, étoiles blanches
**Taille recommandée**: 2-3 MB

#### 5. Arène de Gladiateurs
**Description**: Colisée romain antique
**Ambiance**: Épique, historique, brutal
**Éléments**:
- Gradins avec foule animée
- Sable au sol
- Colonnes détruites
- Bannières flottantes
**Couleurs dominantes**: Beige, brun, rouge sang
**Taille recommandée**: 3-4 MB

#### 6. Laboratoire Secret
**Description**: Lab sci-fi avec expériences
**Ambiance**: Scientifique, dangereux, mystérieux
**Éléments**:
- Tubes avec liquides colorés (animés)
- Écrans holographiques
- Machines complexes
- Éclairage néon vert
**Couleurs dominantes**: Vert, blanc, gris métal
**Taille recommandée**: 2-3 MB

#### 7. Volcan Actif
**Description**: Intérieur d'un volcan avec lave
**Ambiance**: Chaleur intense, danger, feu
**Éléments**:
- Lave coulante (animée)
- Roches incandescentes
- Fumée et cendres
- Lueur rouge ambiante
**Couleurs dominantes**: Rouge, orange, noir
**Taille recommandée**: 3-4 MB

#### 8. Château Hanté
**Description**: Château gothique abandonné
**Ambiance**: Horreur, sombre, mystérieux
**Éléments**:
- Lune pleine en arrière-plan
- Chauve-souris animées
- Candélabres
- Toiles d'araignées
**Couleurs dominantes**: Violet sombre, noir, blanc lunaire
**Taille recommandée**: 2-3 MB

#### 9. Plage Tropicale
**Description**: Plage paradisiaque au coucher du soleil
**Ambiance**: Relaxant, coloré, exotique
**Éléments**:
- Palmiers
- Vagues animées
- Coucher de soleil
- Oiseaux tropicaux
**Couleurs dominantes**: Orange, bleu turquoise, jaune doré
**Taille recommandée**: 2-3 MB

#### 10. Désert Aride
**Description**: Désert avec pyramides au loin
**Ambiance**: Chaud, vaste, mystérieux
**Éléments**:
- Dunes de sable
- Pyramides en silhouette
- Tempête de sable (animée)
- Soleil intense
**Couleurs dominantes**: Jaune sable, orange, bleu ciel
**Taille recommandée**: 1-2 MB

---

## Intégration au Jeu

### Ajouter un Stage au Jeu

#### Étape 1: Placer les Fichiers

```bash
# Copiez vos fichiers dans le dossier stages/
cp MyStage.def "D:\KOF Ultimate\stages\"
cp MyStage.sff "D:\KOF Ultimate\stages\"
```

#### Étape 2: Éditer select.def

Ouvrez `D:\KOF Ultimate\data\select.def` et ajoutez votre stage:

```ini
[ExtraStages]
stages/Wall of paintings.def
stages/TIME INGCODNITA.def
; ... autres stages ...
stages/MyStage.def          ; <-- Ajoutez cette ligne
```

#### Étape 3: Tester

1. Lancez KOF Ultimate
2. Allez en mode Versus ou Training
3. Votre stage devrait apparaître dans la sélection aléatoire

### Configuration Avancée

#### Stage Spécifique pour un Personnage

Éditez le fichier `.def` du personnage (`chars/PersonnageName/PersonnageName.def`):

```ini
[StageInfo]
stage = stages/MyStage.def  ; Stage par défaut pour ce personnage
```

#### Musique Personnalisée

```ini
[Music]
bgmusic = sound/MyMusic.ogg  ; Ou .mp3
bgvolume = 200               ; Volume (0-255)
```

Formats supportés:
- OGG Vorbis (recommandé)
- MP3
- MIDI (qualité inférieure)

---

## Optimisation

### Réduire la Taille des Fichiers

#### Images

```bash
# Avec ImageMagick
magick convert input.png -quality 85 -strip output.jpg

# Réduire la résolution
magick convert input.png -resize 1280x720 output.png

# Optimiser PNG
pngquant input.png --output output.png --quality 65-80
```

#### Animations

- Limitez le nombre de frames (12-24 max)
- Utilisez des loops plutôt que de longues séquences
- Compressez les sprites répétés

### Performance

#### Conseils pour PC Lents

```ini
[StageInfo]
Hires = 0           ; Désactiver haute résolution
debugbg = 0

[Scaling]
; Réduire les calculs de scaling
topscale = 1
botscale = 1

; Limiter les animations
[BG Layer]
type = normal       ; Utiliser 'normal' au lieu de 'anim'
```

#### Profiler un Stage

1. Lancez le jeu en mode fenêtré
2. Ouvrez le Task Manager
3. Surveillez l'usage CPU/GPU
4. Objectif: < 30% CPU, < 50% GPU

### Batch Optimization Script

Créez `optimize_stages.py`:

```python
import os
from PIL import Image
from pathlib import Path

stages_dir = Path("D:/KOF Ultimate/stages")

for img_file in stages_dir.glob("*.png"):
    img = Image.open(img_file)

    # Redimensionner si trop grand
    if img.width > 1920:
        new_height = int((1920 / img.width) * img.height)
        img = img.resize((1920, new_height), Image.LANCZOS)

    # Convertir en JPG (plus léger)
    output_file = img_file.with_suffix('.jpg')
    img.convert('RGB').save(output_file, 'JPEG', quality=85, optimize=True)
    print(f"Optimized: {img_file.name} -> {output_file.name}")
```

---

## Troubleshooting

### Problèmes Courants

#### Le stage n'apparaît pas

**Solutions**:
1. Vérifiez que le .def est bien référencé dans `select.def`
2. Vérifiez l'orthographe du nom de fichier
3. Assurez-vous que le fichier .sff existe et a le bon nom

#### Écran noir

**Causes possibles**:
- Le sprite référencé n'existe pas dans le .sff
- Mauvais format d'image
- Fichier .sff corrompu

**Solutions**:
```ini
; Dans le .def, vérifiez:
[BGdef]
spr = stages/VotreFichier.sff  ; Nom correct?

[BG image]
spriteno = 0, 0  ; Ce sprite existe dans le .sff?
```

#### Ralentissements

**Solutions**:
1. Réduire la résolution des images
2. Limiter les animations
3. Désactiver Hires
4. Réduire le nombre de couches

#### Images déformées

**Problème**: Mauvais ratio aspect

**Solution**:
```ini
[StageInfo]
; Ajustez zoffset pour corriger la perspective
zoffset = 227  ; Valeur standard, testez 200-250
```

#### Musique ne joue pas

**Solutions**:
1. Vérifiez que le fichier audio existe
2. Vérifiez le format (OGG recommandé)
3. Vérifiez le volume:
```ini
[Music]
bgvolume = 255  ; Maximum
```

### Logs de Debug

Activez le mode debug dans `data/mugen.cfg`:

```ini
[Debug]
Debug = 1
AllowDebugMode = 1
```

Appuyez sur `Ctrl+D` pendant le jeu pour voir les informations de debug.

---

## Ressources Utiles

### Outils

| Outil | Usage | Lien |
|-------|-------|------|
| Fighter Factory | Éditeur SFF/AIR | [MUGEN Free For All](https://mugenfreeforall.com) |
| MUGEN Stage Builder | Création de stages | Recherche Google |
| Air Editor | Éditer animations | Inclus avec MUGEN |
| ImageMagick | Optimisation images | [imagemagick.org](https://imagemagick.org) |
| Audacity | Édition audio | [audacityteam.org](https://www.audacityteam.org) |

### Communautés

- **MUGEN Free For All**: Forums, tutoriels, downloads
- **Mugen Archive**: Grande collection de stages
- **Reddit r/mugen**: Questions et partage

### Tutoriels Vidéo

- "How to Make a MUGEN Stage" (YouTube)
- "MUGEN Stage Tutorial - Parallax Effect" (YouTube)
- "Creating Animated Backgrounds in MUGEN" (YouTube)

---

## Exemples Pratiques

### Exemple 1: Stage Simple Statique

**MySimpleStage.def**:
```ini
[Info]
name = "Simple Stage"
displayname = "My Simple Stage"
mugenversion = 1.0

[Camera]
startx = 0
starty = 0
boundleft = -100
boundright = 100

[PlayerInfo]
p1startx = -70
p1starty = 0
p1facing = 1
p2startx = 70
p2starty = 0
p2facing = -1

[StageInfo]
zoffset = 200
autoturn = 1

[BGdef]
spr = stages/MySimpleStage.sff

[BG Background]
type = normal
spriteno = 0, 0
start = 0, 0
delta = 1, 1
```

### Exemple 2: Stage avec Parallaxe

```ini
; Ciel (très lent)
[BG Sky]
type = normal
spriteno = 0, 0
start = 0, -300
delta = 0.3, 0.3

; Montagnes (lent)
[BG Mountains]
type = normal
spriteno = 0, 1
start = 0, -150
delta = 0.6, 0.6

; Sol (normal)
[BG Ground]
type = normal
spriteno = 0, 2
start = 0, 0
delta = 1, 1
```

### Exemple 3: Stage Animé

```ini
[BG AnimatedWater]
type = anim
actionno = 100
start = 0, 0
delta = 1, 1

[Begin Action 100]
0,0, 0,0, 8, , A
0,1, 0,0, 8, , A
0,2, 0,0, 8, , A
0,3, 0,0, 8, , A
```

---

## Checklist Finale

Avant de publier votre stage:

- [ ] Testé sur différentes résolutions
- [ ] Pas de ralentissements visibles
- [ ] Musique fonctionne correctement
- [ ] Fichiers optimisés (taille raisonnable)
- [ ] Positions des joueurs correctes
- [ ] Pas de bugs visuels
- [ ] Nom et auteur renseignés
- [ ] Compatible MUGEN 1.0+

---

## Contact et Contribution

Pour partager vos créations ou obtenir de l'aide:

1. Placez vos stages dans `stages/custom/`
2. Documentez-les dans `CUSTOM_STAGES.md`
3. Partagez avec la communauté!

**Bon développement! 🎮**
