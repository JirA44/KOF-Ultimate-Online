# Guide Complet - Animations et Fonds d'Écrans KOF Ultimate Online

## Vue d'ensemble

Ce guide explique comment personnaliser les animations et fonds d'écrans pour :
- **Menu principal** (Title Screen)
- **Écran de sélection des personnages** (Character Select)
- **Menu de combat** (Versus Screen)

## Table des matières

1. [Préparation des Assets](#préparation-des-assets)
2. [Menu Principal Animé](#menu-principal-animé)
3. [Écran de Sélection Animé](#écran-de-sélection-animé)
4. [Configuration Avancée](#configuration-avancée)
5. [Exemples Pratiques](#exemples-pratiques)

---

## Préparation des Assets

### Formats Supportés

**Images:**
- Format: PCX (recommandé) ou PNG
- Palette: 256 couleurs max pour PCX
- Résolution: 640x480 (standard) ou votre résolution configurée

**Sprites Animés:**
- Format: SFF (Sprite File Format - MUGEN)
- Créez avec Fighter Factory ou SFFMaker

### Organisation des Fichiers

```
D:/KOF Ultimate Online/
├── data/
│   ├── system.def          # Configuration principale
│   ├── system.sff          # Sprites système
│   ├── select.def          # Configuration sélection persos
│   └── mugen.cfg           # Configuration générale
├── backgrounds/            # Vos fonds d'écrans custom
│   ├── title/
│   │   ├── bg1.pcx
│   │   ├── bg2.pcx
│   │   └── animation.sff
│   └── select/
│       ├── bg_select.pcx
│       └── fx_select.sff
└── sound/
    └── menu_theme.mp3     # Musiques custom
```

---

## Menu Principal Animé

### Étape 1: Créer le Fond d'Écran

**Option A - Image Statique:**

1. Créez une image 640x480px
2. Convertissez en PCX (avec GIMP ou Photoshop)
3. Placez dans `backgrounds/title/`

**Option B - Fond Animé (Recommandé):**

Créez plusieurs frames d'animation et compilez en SFF:

```python
# Script pour créer une animation de fond
# auto_create_title_animation.py

from PIL import Image
import os

def create_animated_background():
    """Crée une animation de fond pour le menu titre"""

    frames = []
    width, height = 640, 480

    # Exemple: Animation de gradient qui bouge
    for frame in range(30):  # 30 frames
        img = Image.new('RGB', (width, height))
        pixels = img.load()

        for y in range(height):
            for x in range(width):
                # Calculer couleur avec effet de mouvement
                r = int((x + frame * 10) % 255)
                g = int((y + frame * 5) % 255)
                b = 100
                pixels[x, y] = (r, g, b)

        # Sauvegarder la frame
        img.save(f"backgrounds/title/frame_{frame:03d}.pcx")
        frames.append(f"frame_{frame:03d}.pcx")

    print(f"✓ {len(frames)} frames créées!")
    return frames

if __name__ == "__main__":
    os.makedirs("backgrounds/title", exist_ok=True)
    create_animated_background()
```

### Étape 2: Configuration dans system.def

Éditez `data/system.def`:

```ini
[TitleBGdef]
; Fond d'écran du menu titre

; Option 1: Image statique
;bgclearcolor = 0,0,0
;[TitleBG 0]
;type = normal
;spriteno = 100, 0
;layerno = 0
;start = 0, 0

; Option 2: Animation (RECOMMANDÉ)
[TitleBG 0]
type = anim
actionno = 100
layerno = 0   ; Arrière-plan
start = 0, 0
mask = 0

; Animation supplémentaire (effets au premier plan)
[TitleBG 1]
type = anim
actionno = 101
layerno = 1   ; Premier plan
start = 320, 240
trans = add   ; Effet de transparence additif
alpha = 200, 255

; Particules flottantes
[TitleBG 2]
type = anim
actionno = 102
layerno = 1
start = 100, 100
velocity = 1, -0.5  ; Mouvement vers le haut
```

### Étape 3: Définir les Animations

Dans `data/system.def`, ajoutez les animations:

```ini
; Animation du fond principal
[Begin Action 100]
100,0, 0,0, 3    ; Frame 100,0 pendant 3 ticks
100,1, 0,0, 3
100,2, 0,0, 3
; ... (continuez pour toutes les frames)
100,29, 0,0, 3
Loopstart          ; Point de début de boucle
100,0, 0,0, 3
; ... répétez
Loopend:           ; Fin de boucle (recommence)

; Animation d'effets lumineux
[Begin Action 101]
101,0, 0,0, 5, , A
101,1, 0,0, 5, , A
101,2, 0,0, 5, , A
101,3, 0,0, 5, , A

; Animation de particules
[Begin Action 102]
102,0, 0,0, 2
102,1, 0,0, 2
102,2, 0,0, 2
```

### Étape 4: Ajouter les Sprites

Vous devez ajouter vos sprites dans `data/system.sff`:

**Méthode 1 - Fighter Factory:**
1. Ouvrez `system.sff` avec Fighter Factory
2. Allez dans l'onglet "Sprites"
3. Importez vos images:
   - Groupe 100, Index 0-29 pour l'animation principale
   - Groupe 101, Index 0-3 pour les effets
   - Groupe 102, Index 0-2 pour les particules

**Méthode 2 - Script Python:**

```python
# add_sprites_to_sff.py
import struct

def add_sprite_to_sff(sff_path, group, index, pcx_path):
    """Ajoute un sprite à un fichier SFF"""
    # Cette fonction nécessite une bibliothèque SFF
    # Ou utilisez Fighter Factory (plus simple)
    pass
```

---

## Écran de Sélection Animé

### Étape 1: Configuration dans select.def

Éditez `data/select.def`:

```ini
[Select Info]
fadein.time = 30
fadeout.time = 30
rows = 5
columns = 10
wrapping = 0
pos = 70, 110
showemptyboxes = 1
moveoveremptyboxes = 1

; Curseur personnalisé
cursor.move.snd = 100, 0
cursor.done.snd = 100, 1
cursor.active = 1
cursor.anim = 160
cursor.scale = 1.0

; Portrait des personnages
p1.face.offset = 10, 10
p1.face.scale = 1, 1
p1.face.facing = 1
p2.face.offset = 630, 10
p2.face.scale = 1, 1
p2.face.facing = -1

; Position du nom du joueur
p1.name.offset = 10, 460
p1.name.font = 3, 0, 1
p2.name.offset = 630, 460
p2.name.font = 3, 0, -1

[SelectBGdef]
; Configuration du fond de l'écran de sélection

; Fond de base
[SelectBG 0]
type = normal
spriteno = 150, 0
layerno = 0
start = 0, 0

; Animation de fond
[SelectBG 1]
type = anim
actionno = 150
layerno = 0
start = 0, 0
mask = 0

; Effet de lumière dynamique
[SelectBG 2]
type = anim
actionno = 151
layerno = 1
start = 320, 240
trans = add
alpha = 180, 255

; Particules flottantes
[SelectBG 3]
type = anim
actionno = 152
layerno = 1
start = 0, 0
velocity = 0.5, 0
tile = 1, 1
window = 0, 0, 640, 480

; Définir les animations
[Begin Action 150]
; Animation de fond principal
150,0, 0,0, 5
150,1, 0,0, 5
150,2, 0,0, 5
150,3, 0,0, 5
; ... continuez

[Begin Action 151]
; Effets lumineux pulsants
151,0, 0,0, 10, , A1
151,1, 0,0, 10, , A1
151,2, 0,0, 10, , A1
151,3, 0,0, 10, , A1

[Begin Action 152]
; Particules
152,0, 0,0, 3
152,1, 0,0, 3

; Animation du curseur personnalisée
[Begin Action 160]
160,0, 0,0, 5
160,1, 0,0, 5
160,2, 0,0, 5
160,3, 0,0, 5
```

### Étape 2: Animations Avancées

**Effet Parallax:**

```ini
; Couche arrière (bouge lentement)
[SelectBG 0]
type = normal
spriteno = 150, 0
layerno = 0
start = 0, 0
velocity = -0.2, 0
tile = 1, 1

; Couche milieu (bouge normalement)
[SelectBG 1]
type = normal
spriteno = 151, 0
layerno = 1
start = 0, 0
velocity = -0.5, 0
tile = 1, 1
trans = add
alpha = 200, 256

; Couche avant (bouge vite)
[SelectBG 2]
type = normal
spriteno = 152, 0
layerno = 2
start = 0, 0
velocity = -1.0, 0
tile = 1, 1
trans = add
alpha = 150, 256
```

---

## Configuration Avancée

### Effets de Transparence

```ini
; Transparence normale
trans = none          ; Aucune transparence
trans = add           ; Additif (éclairage)
trans = sub           ; Soustractif (ombres)
trans = alpha         ; Alpha blending

; Valeurs alpha
alpha = source, dest
alpha = 256, 256      ; Opaque
alpha = 128, 256      ; Semi-transparent
alpha = 64, 256       ; Très transparent
```

### Effets Spéciaux

```ini
; Effet de zoom/scale
[TitleBG X]
type = anim
actionno = XXX
start = 320, 240
scale = 2.0, 2.0      ; 200% de taille
scaledelta = -0.01, -0.01  ; Réduction progressive

; Rotation
angle = 45            ; Rotation de 45 degrés
angledelta = 1        ; Tourne de 1 degré par tick

; Effet de couleur
color = 255, 200, 200  ; Teinte rougeâtre
coloradd = -5, -5, -5  ; Assombrir progressivement
```

### Musiques Personnalisées

Dans `data/system.def`:

```ini
[Music]
; Musique du menu titre
title.bgm = sound/menu_theme.mp3
title.bgm.loop = 1
title.bgm.volume = 100

; Musique de sélection
select.bgm = sound/select_theme.mp3
select.bgm.loop = 1
select.bgm.volume = 80

; Musique du versus screen
vs.bgm = sound/vs_theme.mp3
vs.bgm.loop = 0
```

---

## Exemples Pratiques

### Exemple 1: Menu avec Video en Fond

```ini
; Nécessite une séquence d'images
[TitleBG 0]
type = anim
actionno = 200
layerno = 0
start = 0, 0
mask = 0

[Begin Action 200]
; 300 frames (10 secondes à 30 FPS)
200,0, 0,0, 1
200,1, 0,0, 1
200,2, 0,0, 1
; ... (jusqu'à 200,299)
Loopstart
200,0, 0,0, 1
; ... répétez
```

### Exemple 2: Écran de Sélection Style Anime

```ini
[SelectBG 0]
; Fond style manga/anime
type = normal
spriteno = 150, 0
start = 0, 0

[SelectBG 1]
; Lignes de vitesse animées
type = anim
actionno = 151
layerno = 1
velocity = -5, 0
tile = 1, 0
trans = add
alpha = 180, 256

[SelectBG 2]
; Personnages en silhouette
type = anim
actionno = 152
layerno = 2
start = 500, 100
trans = sub
```

### Exemple 3: Particules Dynamiques

```ini
; Particules qui tombent (neige, pétales, etc.)
[TitleBG 10]
type = anim
actionno = 110
start = rand % 640, -50
velocity = 0, 1.5 + (rand % 100) / 100
layerno = 2
trans = add
alpha = 150, 256

; Répéter pour plusieurs particules
[TitleBG 11]
type = anim
actionno = 110
start = rand % 640, -100
velocity = 0.2, 1.8
layerno = 2
trans = add
alpha = 150, 256
```

---

## Outils Recommandés

### Création de Sprites
- **Fighter Factory Ultimate** - Éditeur SFF/AIR complet
- **SFFMaker** - Création rapide de SFF
- **GIMP** - Édition d'images, export PCX

### Création d'Animations
- **After Effects** - Animations professionnelles
- **Aseprite** - Pixel art animé
- **Blender** - Rendu 3D en séquence d'images

### Test et Debug
- **MUGEN 1.1** - Testez vos modifications
- **WinMUGEN** - Version Windows classique
- **Ikemen GO** - Alternative moderne (supporte HD)

---

## Fichiers de Configuration Importants

### system.def
Contrôle TOUT l'interface:
- Menu titre
- Options
- Training mode
- Survival mode

### select.def
Contrôle l'écran de sélection des personnages

### fight.def
Contrôle l'interface en combat (barres de vie, timer, etc.)

---

## Troubleshooting

### Problème: Animation ne s'affiche pas

**Solutions:**
1. Vérifiez que les sprites existent dans system.sff
2. Vérifiez les numéros de groupe/index
3. Assurez-vous que `layerno` est correct (0 = arrière)

### Problème: Ralentissements

**Solutions:**
1. Réduisez la résolution des sprites
2. Utilisez moins de layers
3. Optimisez la palette de couleurs (256 max)
4. Réduisez le nombre de frames d'animation

### Problème: Couleurs incorrectes

**Solutions:**
1. Utilisez une palette shared (index 0)
2. Convertissez en PCX avec la bonne palette
3. Vérifiez les paramètres `alpha` et `trans`

---

## Scripts d'Automatisation

Pour automatiser la création d'animations, utilisez:

```bash
# Lancer le générateur d'animations
python create_menu_animation.py

# Tester les modifications
python verify_game.py
```

---

## Conclusion

Avec ce guide, vous pouvez créer des menus entièrement personnalisés pour KOF Ultimate Online!

**Prochaines étapes:**
1. Créez vos assets graphiques
2. Modifiez system.def et select.def
3. Testez dans le jeu
4. Ajustez selon vos besoins

**Ressources supplémentaires:**
- [MUGEN Documentation](http://mugenguild.com/forum/)
- [Elecbyte Forums](http://www.elecbyte.com/)
- Community Discord pour aide
