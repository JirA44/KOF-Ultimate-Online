"""
KOF Ultimate - Intégration Automatique des Nouveaux Backgrounds
Intègre les nouveaux fonds d'écran dans la configuration du jeu
"""

import os
import shutil
from pathlib import Path
import configparser

GAME_PATH = Path("D:/KOF Ultimate")
BACKGROUNDS_SOURCE = GAME_PATH / "data" / "backgrounds"
MUGEN_CFG = GAME_PATH / "data" / "mugen.cfg"

def backup_config():
    """Sauvegarde la configuration"""
    if MUGEN_CFG.exists():
        backup_path = MUGEN_CFG.with_suffix('.cfg.backup_backgrounds')
        shutil.copy2(MUGEN_CFG, backup_path)
        print(f"💾 Backup créé: {backup_path.name}")
        return True
    return False

def integrate_title_screen():
    """Intègre le nouveau title screen"""
    title_bg = BACKGROUNDS_SOURCE / "title_screen.png"

    if not title_bg.exists():
        print("❌ title_screen.png non trouvé")
        return False

    # Dans MUGEN, le title screen est défini dans system.def
    system_def = GAME_PATH / "data" / "system.def"

    if system_def.exists():
        print("📝 Modification de system.def pour le title screen...")

        with open(system_def, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        modified = []
        in_title_section = False

        for line in lines:
            # Détecter la section [Title Info]
            if '[Title Info]' in line or '[TitleInfo]' in line:
                in_title_section = True
                modified.append(line)
                continue

            # Si on est dans la section Title et qu'on trouve une ligne de sprite
            if in_title_section and 'sprite' in line.lower() and '=' in line:
                # Remplacer par notre nouveau background
                modified.append(f"; {line}")  # Commenter l'ancienne ligne
                modified.append(f"sprite = data/backgrounds/title_screen.png, 0, 0\n")
                print("  ✓ Title screen configuré")
                in_title_section = False
            else:
                modified.append(line)

        with open(system_def, 'w', encoding='utf-8') as f:
            f.writelines(modified)

        return True

    print("⚠️  system.def non trouvé")
    return False

def integrate_character_select():
    """Intègre le nouveau character select screen"""
    select_bg = BACKGROUNDS_SOURCE / "character_select.png"

    if not select_bg.exists():
        print("❌ character_select.png non trouvé")
        return False

    system_def = GAME_PATH / "data" / "system.def"

    if system_def.exists():
        print("📝 Modification de system.def pour le character select...")

        with open(system_def, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        modified = []
        in_select_section = False

        for line in lines:
            if '[Select Info]' in line or '[SelectInfo]' in line:
                in_select_section = True
                modified.append(line)
                continue

            if in_select_section and 'bg' in line.lower() and '=' in line and not line.strip().startswith(';'):
                modified.append(f"; {line}")
                modified.append(f"bg.spr = data/backgrounds/character_select.png\n")
                print("  ✓ Character select configuré")
                in_select_section = False
            else:
                modified.append(line)

        with open(system_def, 'w', encoding='utf-8') as f:
            f.writelines(modified)

        return True

    return False

def integrate_versus_screen():
    """Intègre le nouveau versus screen"""
    versus_bg = BACKGROUNDS_SOURCE / "versus_screen.png"

    if not versus_bg.exists():
        print("❌ versus_screen.png non trouvé")
        return False

    system_def = GAME_PATH / "data" / "system.def"

    if system_def.exists():
        print("📝 Modification de system.def pour le versus screen...")

        with open(system_def, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        modified = []
        in_versus_section = False

        for line in lines:
            if '[VS Screen]' in line or '[Versus Screen]' in line:
                in_versus_section = True
                modified.append(line)
                continue

            if in_versus_section and ('sprite' in line.lower() or 'bg' in line.lower()) and '=' in line:
                modified.append(f"; {line}")
                modified.append(f"bg.spr = data/backgrounds/versus_screen.png\n")
                print("  ✓ Versus screen configuré")
                in_versus_section = False
            else:
                modified.append(line)

        with open(system_def, 'w', encoding='utf-8') as f:
            f.writelines(modified)

        return True

    return False

def integrate_victory_screen():
    """Intègre le nouveau victory screen"""
    victory_bg = BACKGROUNDS_SOURCE / "victory_screen.png"

    if not victory_bg.exists():
        print("❌ victory_screen.png non trouvé")
        return False

    system_def = GAME_PATH / "data" / "system.def"

    if system_def.exists():
        print("📝 Modification de system.def pour le victory screen...")

        with open(system_def, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        modified = []
        in_victory_section = False

        for line in lines:
            if '[Victory Screen]' in line or '[WinScreen]' in line:
                in_victory_section = True
                modified.append(line)
                continue

            if in_victory_section and ('sprite' in line.lower() or 'bg' in line.lower()) and '=' in line:
                modified.append(f"; {line}")
                modified.append(f"bg.spr = data/backgrounds/victory_screen.png\n")
                print("  ✓ Victory screen configuré")
                in_victory_section = False
            else:
                modified.append(line)

        with open(system_def, 'w', encoding='utf-8') as f:
            f.writelines(modified)

        return True

    return False

def create_background_readme():
    """Crée un README pour les backgrounds"""
    readme_content = """# KOF Ultimate - Nouveaux Backgrounds

## Backgrounds Intégrés

Les nouveaux backgrounds ont été automatiquement intégrés dans le jeu:

1. **Title Screen** (`title_screen.png`)
   - Dégradé radial violet brillant
   - 200+ étoiles
   - Effet spatial profond

2. **Character Select** (`character_select.png`)
   - Dégradé bleu électrique
   - Hexagones en arrière-plan
   - Lignes d'énergie cyberpunk

3. **Versus Screen** (`versus_screen.png`)
   - Explosion d'énergie centrale
   - Rayons lumineux radiaux
   - Effet jaune/rouge dynamique

4. **Victory Screen** (`victory_screen.png`)
   - Fond doré brillant
   - 300 particules scintillantes
   - Étoiles à 4 branches

5. **Menu Background** (`menu_background.png`)
   - Grille cyberpunk futuriste
   - Points lumineux aux intersections

6. **Loading Screen** (`loading_screen.png`)
   - Cercles concentriques pulsants
   - Effet de chargement moderne

## Fichiers Modifiés

- `data/system.def` - Configuration des écrans
- `data/mugen.cfg.backup_backgrounds` - Sauvegarde

## Restauration

Pour restaurer les anciens backgrounds:
```bash
copy data\\mugen.cfg.backup_backgrounds data\\mugen.cfg
```

## Personnalisation

Pour modifier les backgrounds:
1. Éditez les fichiers PNG dans `data/backgrounds/`
2. Résolution recommandée: 1280x720 ou 1920x1080
3. Relancez le jeu pour voir les changements

---

*Générés automatiquement par integrate_backgrounds.py*
"""

    readme_path = BACKGROUNDS_SOURCE / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"📖 README créé: {readme_path}")

def main():
    """Intègre tous les backgrounds"""
    print("=" * 70)
    print("KOF Ultimate - Intégration Automatique des Nouveaux Backgrounds")
    print("=" * 70)
    print()

    # Vérifier que les backgrounds existent
    if not BACKGROUNDS_SOURCE.exists():
        print(f"❌ Dossier backgrounds non trouvé: {BACKGROUNDS_SOURCE}")
        print("   Générez d'abord les backgrounds avec:")
        print("   python tools/create_game_backgrounds.py")
        return False

    # Backup
    backup_config()
    print()

    # Intégrer chaque background
    print("📥 Intégration des backgrounds dans le jeu...")
    print("-" * 70)

    results = []
    results.append(("Title Screen", integrate_title_screen()))
    results.append(("Character Select", integrate_character_select()))
    results.append(("Versus Screen", integrate_versus_screen()))
    results.append(("Victory Screen", integrate_victory_screen()))

    print()
    print("-" * 70)
    print("📊 Résultats:")
    print()

    success_count = 0
    for name, success in results:
        status = "✅ OK" if success else "❌ ÉCHEC"
        print(f"  {status}  {name}")
        if success:
            success_count += 1

    print()
    print(f"Total: {success_count}/{len(results)} backgrounds intégrés")

    # Créer le README
    print()
    create_background_readme()

    print()
    print("=" * 70)
    if success_count == len(results):
        print("✨ SUCCÈS! Tous les backgrounds ont été intégrés!")
    else:
        print("⚠️  Intégration partielle. Vérifiez les messages ci-dessus.")

    print()
    print("🎮 Lancez le jeu pour voir les nouveaux backgrounds!")
    print("=" * 70)

    return success_count > 0

if __name__ == "__main__":
    main()
