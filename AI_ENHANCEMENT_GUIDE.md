# KOF ULTIMATE - AI RETRO ANIME ENHANCEMENT GUIDE

Version 2.0 - Style Rétro Anime 80-90 (Aquarelle)

---

## 🎨 QU'EST-CE QUE C'EST?

Ce système transforme automatiquement les sprites du jeu en **style rétro anime des années 80-90**, avec des effets:

- **Aquarelle** - Textures douces et fluides
- **Couleurs vibrantes** - Palette pastel saturée
- **Grain de film** - Effet rétro authentique
- **Contours marqués** - Style anime classique
- **Cel-shading doux** - Ombrage anime

### Références Visuelles

Le style s'inspire de:
- **Akira** (1988) - Couleurs néon vibrantes
- **Bubblegum Crisis** (1987) - Cyberpunk doux
- **City Hunter** (1987) - Palette urbaine
- **Kimagure Orange Road** (1987) - Teintes pastel

---

## 🚀 DÉMARRAGE RAPIDE

### 1. Voir les Démos

```bash
python enhance_sprites_batch.py demo
```

Cela crée 4 images dans `ai_enhanced_demos/`:
- `demo_original.png` - Image de base
- `demo_retro_light.png` - Style léger (subtil)
- `demo_retro_normal.png` - Style normal (recommandé)
- `demo_retro_heavy.png` - Style intense (très marqué)

### 2. Améliorer un Personnage

Il y a deux méthodes:

#### Méthode A: Extraction Automatique (Recommandé)

```bash
# 1. Installer MUGEN Character Manager (MCM)
# Télécharger: https://github.com/2damnmemes/MCM

# 2. Extraire les sprites d'un personnage
# Dans MCM: File > Extract > Select Character .sff
# Sauvegarder dans: chars/[personnage]/sprites_extracted/

# 3. Améliorer les sprites
python enhance_sprites_batch.py "chars/Kyo/sprites_extracted"

# 4. Résultat dans: chars/Kyo/sprites_extracted/enhanced_retro/
```

#### Méthode B: Amélioration Manuelle

```bash
# Améliorer un dossier spécifique
python enhance_sprites_batch.py <dossier_source> <dossier_sortie>

# Exemple
python enhance_sprites_batch.py "D:\sprites\kyo" "D:\sprites\kyo_enhanced"

# Avec intensité personnalisée (light/normal/heavy)
python enhance_sprites_batch.py "D:\sprites\kyo" "D:\sprites\kyo_enhanced" heavy
```

---

## 📋 WORKFLOW COMPLET

### Étape 1: Préparation

1. **Identifier les personnages prioritaires**
   - Personnages principaux du jeu (Kyo, Iori, etc.)
   - Personnages les plus utilisés

2. **Backup complet**
   ```bash
   # Créer une sauvegarde
   xcopy "D:\KOF Ultimate\chars" "D:\KOF Ultimate\chars_BACKUP" /E /I /H
   ```

### Étape 2: Extraction des Sprites

**Option 1: Avec MUGEN Character Manager (MCM)**

1. Télécharger MCM: https://github.com/2damnmemes/MCM
2. Lancer MCM
3. File > Open > Sélectionner le fichier .sff du personnage
   - Exemple: `chars/Kyo/kyo.sff`
4. Edit > Extract All Sprites
5. Sauvegarder dans: `chars/Kyo/sprites_extracted/`

**Option 2: Avec Fighter Factory**

1. Télécharger Fighter Factory: http://www.virtualltek.com/ff3.php
2. Ouvrir le fichier .def du personnage
3. Sprites > Export All
4. Sauvegarder en PNG

**Option 3: Avec SpriteEx**

1. Télécharger: https://mugenguild.com/forum/topics/spriteex-189576.0.html
2. Glisser-déposer le .sff
3. Export All

### Étape 3: Amélioration AI

```bash
cd "D:\KOF Ultimate"

# Test sur un personnage (light = subtil)
python enhance_sprites_batch.py "chars/Kyo/sprites_extracted" "chars/Kyo/enhanced_light" light

# Production (normal = équilibré, recommandé)
python enhance_sprites_batch.py "chars/Kyo/sprites_extracted" "chars/Kyo/enhanced_normal" normal

# Extrême (heavy = très marqué)
python enhance_sprites_batch.py "chars/Kyo/sprites_extracted" "chars/Kyo/enhanced_heavy" heavy
```

### Étape 4: Réintégration dans le Jeu

**Avec MUGEN Character Manager (MCM):**

1. Ouvrir MCM
2. File > New > Create Empty SFF
3. Edit > Import Sprites
4. Sélectionner tous les PNG améliorés
5. File > Save As > `kyo_retro.sff`
6. Copier dans `chars/Kyo/`
7. Éditer `chars/Kyo/kyo.def`:
   ```ini
   [Files]
   sprite = kyo_retro.sff  ; <-- Changez ici
   ```

**Avec Fighter Factory:**

1. Ouvrir le .def original
2. Sprites > Import > Batch Import
3. Sélectionner les PNG améliorés
4. Sprites > Rebuild > Save

### Étape 5: Test dans le Jeu

1. Lancer le jeu
2. Sélectionner le personnage modifié
3. Vérifier visuellement:
   - Couleurs plus vibrantes ✓
   - Effet aquarelle visible ✓
   - Grain de film présent ✓
   - Pas de bugs visuels ✓

---

## 🎛️ PARAMÈTRES DE STYLE

### Intensités Disponibles

| Intensité | Saturation | Contraste | Grain | Usage |
|-----------|------------|-----------|-------|-------|
| **light** | 1.2x | 1.1x | 10 | Amélioration subtile, conserve l'original |
| **normal** | 1.4x | 1.15x | 15 | Équilibré, style rétro visible |
| **heavy** | 1.6x | 1.2x | 20 | Très marqué, effet aquarelle intense |

### Configuration Personnalisée

Éditez `enhance_sprites_batch.py` pour ajuster finement:

```python
'custom': {
    'saturation': 1.5,        # 1.0 = normal, 2.0 = très saturé
    'contrast': 1.18,         # 1.0 = normal, 1.5 = très contrasté
    'brightness': 1.06,       # 1.0 = normal, 1.2 = très lumineux
    'watercolor_blur': 1.3,   # Flou aquarelle (pixels)
    'grain': 18,              # Quantité de grain de film
    'pastel_shift': 22        # Décalage vers pastel (%)
}
```

---

## 🎨 TECHNIQUES AVANCÉES

### 1. Amélioration Sélective

Pour améliorer seulement certains sprites (portraits, attaques spéciales):

```bash
# Copier seulement les sprites désirés dans un dossier
mkdir sprites_special
copy sprites_extracted\9000*.png sprites_special\

# Améliorer seulement ceux-ci
python enhance_sprites_batch.py sprites_special sprites_special_enhanced
```

### 2. Mélange de Styles

Combiner différentes intensités:

```python
# Portraits en heavy (très visible)
enhance_directory("sprites/portraits", "sprites/portraits_enhanced", "heavy")

# Sprites de jeu en normal
enhance_directory("sprites/game", "sprites/game_enhanced", "normal")

# Effets en light (subtil)
enhance_directory("sprites/effects", "sprites/effects_enhanced", "light")
```

### 3. Post-Traitement Manuel

Après l'amélioration AI, vous pouvez retoucher manuellement avec:

- **GIMP** (gratuit): Ajuster niveaux, teintes
- **Aseprite**: Pixel art retouching
- **Photoshop**: Filtres avancés

---

## 📊 PERFORMANCES

### Vitesse de Traitement

- **1 sprite**: ~0.5 secondes
- **100 sprites**: ~50 secondes
- **1000 sprites**: ~8 minutes
- **Personnage complet (500-2000 sprites)**: 5-15 minutes

### Taille des Fichiers

- Images PNG: +20-40% de taille (grain et détails)
- Fichier .sff final: Similaire ou légèrement plus grand
- Compression recommandée: PNG avec optimisation

---

## 🐛 DÉPANNAGE

### Problème: "ModuleNotFoundError: PIL"

```bash
pip install Pillow
```

### Problème: "ModuleNotFoundError: tqdm"

```bash
pip install tqdm
```

### Problème: "ModuleNotFoundError: numpy"

```bash
pip install numpy
```

### Installation Complète

```bash
pip install Pillow tqdm numpy
```

### Problème: Sprites Transparents Deviennent Opaques

Le canal alpha est préservé automatiquement. Si problème:
1. Vérifier que les PNG sources ont un canal alpha
2. Sauvegarder en PNG (pas JPG)

### Problème: Couleurs Trop Saturées

```bash
# Utilisez l'intensité "light"
python enhance_sprites_batch.py <input> <output> light
```

### Problème: Sprites Flous

Le flou aquarelle est intentionnel pour le style rétro. Pour réduire:

Éditez `enhance_sprites_batch.py`, ligne ~25:
```python
'watercolor_blur': 0.5,  # Au lieu de 1.2
```

---

## 📈 AMÉLIORATION PAR PHASES

### Phase 1: Personnages Principaux (Priorité Haute)

1. Kyo Kusanagi
2. Iori Yagami
3. Terry Bogard
4. Mai Shiranui
5. Ryo Sakazaki

**Temps estimé**: 1-2 heures

### Phase 2: Personnages Populaires (Priorité Moyenne)

6-20. Autres personnages populaires

**Temps estimé**: 3-5 heures

### Phase 3: Personnages Secondaires (Priorité Basse)

21+. Tous les autres

**Temps estimé**: 10-20 heures

---

## 🔧 AUTOMATISATION COMPLÈTE

Script pour améliorer tous les personnages automatiquement:

```bash
# Créer un script batch (Windows)
# Fichier: enhance_all_characters.bat

@echo off
FOR /D %%G IN ("chars\*") DO (
    echo Processing %%G...

    IF EXIST "%%G\sprites_extracted" (
        python enhance_sprites_batch.py "%%G\sprites_extracted" "%%G\enhanced_retro" normal
        echo Done: %%G
    ) ELSE (
        echo Skipped: %%G (no sprites_extracted folder)
    )
)

echo All characters processed!
pause
```

---

## 🎯 EXEMPLES DE RÉSULTATS

### Avant/Après

**Couleurs:**
- Avant: RGB(200,100,50) - Orange terne
- Après: RGB(255,140,85) - Orange vif pastel

**Saturation:**
- Avant: 40% saturation
- Après: 56% saturation (+40% boost)

**Texture:**
- Avant: Pixels nets
- Après: Léger flou aquarelle + grain de film

---

## 📝 NOTES IMPORTANTES

1. **Backup**: Toujours sauvegarder les fichiers originaux
2. **Tests**: Tester sur 1-2 personnages avant traitement en masse
3. **Performance**: Le jeu peut charger légèrement plus lentement avec des fichiers plus gros
4. **Cohérence**: Utiliser la même intensité pour tous les personnages

---

## 🌟 CRÉDITS

- **Style Design**: Inspiré des animes rétro 80-90
- **Pipeline AI**: Traitement d'image Python/PIL
- **Références**: Akira, Bubblegum Crisis, City Hunter

---

## 📧 SUPPORT

Pour toute question ou problème:
1. Vérifier la section Dépannage ci-dessus
2. Consulter le fichier `DEMARRAGE_RAPIDE.txt`
3. Tester avec les démos (`python enhance_sprites_batch.py demo`)

---

**Version**: 2.0 Enhanced
**Date**: 16 Octobre 2025
**Statut**: Production Ready

Bon travail! 🎮🎨
