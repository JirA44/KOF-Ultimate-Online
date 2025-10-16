# Guide: Configuration des Images de Personnages

## Problème actuel
Les fonds des menus étaient noirs et les images des personnages ne s'affichaient pas correctement.

## Solution: Les 3 types d'images à gérer

Dans MUGEN, chaque personnage doit avoir **3 types d'images** stockées dans `data/system.sff`:

### 1. **Miniature (Cell Icon)** - Petite icône dans la grille
- **Taille recommandée**: 31x31 pixels (taille de la cellule)
- **Sprite**: Groupe 9000, Index 0
- **Utilisation**: Icône dans la grille de sélection
- **Configuration dans system.def**:
```ini
cell.size = 31,31
portrait.spr = 9000,2  ; Utilise l'index 2 pour les miniatures
portrait.scale = 0.5,0.5
```

### 2. **Portrait de Face (Face Portrait)** - Portrait moyen
- **Taille recommandée**: 80x100 pixels
- **Sprite**: Groupe 9000, Index 2
- **Utilisation**: Portrait affiché pendant la sélection (en haut de l'écran)
- **Configuration dans system.def**:
```ini
p1.face.offset = 25,20
p1.face.scale = 0.5,0.5
p1.face.facing = 1

p2.face.offset = 550,20
p2.face.scale = 0.5,0.5
p2.face.facing = -1
```

### 3. **Portrait Complet (Full Portrait)** - Grand portrait ou sprite entier
- **Taille recommandée**: 200x300 pixels
- **Sprite**: Groupe 9000, Index 1
- **Utilisation**: Écran VS, écran de victoire
- **Configuration dans system.def**:
```ini
; Écran VS
p1.spr = 9000,1
p1.offset = 19,100
p1.scale = 1,1

p2.spr = 9000,1
p2.offset = 520,100
p2.scale = 1,1
```

## Comment ajouter les images dans system.sff

### Méthode 1: Utiliser Fighter Factory (Recommandé)

1. **Télécharger Fighter Factory**:
   - Outil gratuit pour éditer les fichiers MUGEN
   - https://www.virtualltek.com/

2. **Ouvrir system.sff**:
   ```
   D:\KOF Ultimate Online\data\system.sff
   ```

3. **Ajouter les sprites**:
   - Clic droit → "Add Sprite"
   - Groupe: 9000
   - Index: 0 (miniature), 1 (grand portrait), 2 (portrait moyen)
   - Sélectionner l'image PNG ou BMP

4. **Répéter pour chaque personnage**:
   - Groupe 9000, Index 0: Miniature 31x31
   - Groupe 9000, Index 1: Grand portrait 200x300
   - Groupe 9000, Index 2: Portrait moyen 80x100

### Méthode 2: Sprites par défaut

Si tu n'as pas d'images spécifiques, MUGEN peut utiliser:
- Les sprites du dossier `chars/` de chaque personnage
- Chaque personnage a son propre fichier SFF avec ses sprites

**Pour utiliser les sprites des personnages**:
```ini
; Dans le .def de chaque personnage
[Files]
sprite = kyo.sff  ; Fichier de sprites du personnage
```

## Configuration actuelle corrigée

### Fonds des menus
✅ **Corrigé**: Les fonds noirs ont été remplacés par des couleurs:
- Menu principal: Bleu foncé (RGB: 20,10,50)
- Menu select: Bleu-violet (RGB: 15,10,40)

### Positions des portraits
✅ **Corrigé**: Tous les portraits sont maintenant à l'écran:
- Sélection P1: (25, 20)
- Sélection P2: (550, 20)
- VS P1: (19, 100)
- VS P2: (520, 100)
- Victoire: (450, 100)

## Structure des sprites recommandée

```
system.sff
├── Groupe 9000 (Portraits des personnages)
│   ├── Index 0: Kyo miniature (31x31)
│   ├── Index 1: Kyo grand portrait (200x300)
│   ├── Index 2: Kyo portrait moyen (80x100)
│   ├── Index 3: Iori miniature (31x31)
│   ├── Index 4: Iori grand portrait (200x300)
│   ├── Index 5: Iori portrait moyen (80x100)
│   └── ... (continuer pour chaque personnage)
```

## Système alternatif: Portraits individuels par personnage

Si tu préfères que chaque personnage ait ses propres portraits dans son dossier:

1. **Créer un fichier `portrait.def` pour chaque personnage**:
```
chars/kyo/portrait.def
```

2. **Contenu du portrait.def**:
```ini
[Portraits]
; Miniature
cell = sprite/kyo_cell.png
; Portrait moyen
face = sprite/kyo_face.png
; Grand portrait
full = sprite/kyo_full.png
```

3. **MUGEN chargera automatiquement** ces images si elles existent

## Test des images

Pour vérifier que tes images s'affichent:

1. Lance le jeu
2. Va dans le menu de sélection
3. Vérifie:
   - ✅ Les miniatures dans la grille
   - ✅ Les portraits en haut quand tu sélectionnes
   - ✅ Les grands portraits dans l'écran VS

## Prochaines étapes

1. **Collecter les images** de tous les personnages (189 persos)
2. **Redimensionner** aux tailles recommandées
3. **Ajouter dans system.sff** avec Fighter Factory
4. **Tester** chaque personnage

## Notes importantes

- **Format des images**: PNG ou BMP (PNG recommandé)
- **Transparence**: Utiliser un fond transparent ou couleur magenta (255,0,255)
- **Taille du fichier**: system.sff peut devenir très gros avec 189 personnages × 3 images
- **Alternative**: Utiliser des portraits par défaut de MUGEN si les images n'existent pas

## Ressources

- **Fighter Factory**: https://www.virtualltek.com/
- **MUGEN Documentation**: http://www.elecbyte.com/mugendocs/
- **Sprites KOF**: Rechercher "KOF sprites" sur spriters-resource.com
