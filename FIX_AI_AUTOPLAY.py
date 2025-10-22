#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIX AI AUTOPLAY - Désactive l'IA automatique pour permettre au joueur de jouer
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

class AIAutoplayFixer:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.mugen_cfg = self.base_path / "data" / "mugen.cfg"
        self.fixes_applied = 0

    def log(self, message, level="INFO"):
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✓",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "FIX": "🔧"
        }
        print(f"{icons.get(level, '')} {message}")

    def backup_config(self):
        """Crée un backup du fichier de config"""
        if not self.mugen_cfg.exists():
            self.log("mugen.cfg non trouvé!", "ERROR")
            return False

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = self.mugen_cfg.with_suffix(f'.cfg.ai_backup_{timestamp}')
        shutil.copy2(self.mugen_cfg, backup)
        self.log(f"Backup créé: {backup.name}", "SUCCESS")
        return True

    def fix_ai_settings(self):
        """Désactive tous les paramètres d'IA automatique"""
        self.log("Correction des paramètres IA...", "FIX")

        if not self.mugen_cfg.exists():
            return False

        content = self.mugen_cfg.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')

        # Paramètres à corriger
        ai_fixes = {
            'AIRandomColor': '0',           # Pas de couleur aléatoire IA
            'Team.1VS2Life': '100',         # Vie normale
            'Team.LoseOnKO': '1',           # Perdre si KO
            'Default.Attack.LifeToPowerMul': '0.7',
            'Default.GetHit.LifeToPowerMul': '0.6',
        }

        in_config = False
        section = None

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Détecter les sections
            if stripped.startswith('['):
                section = stripped
                in_config = True
                continue

            # Paramètres spécifiques dans [Config]
            if section == '[Config]' and '=' in line:
                for key, value in ai_fixes.items():
                    if line.strip().startswith(key):
                        old_value = line.split('=')[1].strip() if '=' in line else 'N/A'
                        lines[i] = f'{key} = {value}'
                        self.log(f"  Modifié: {key} = {value} (était: {old_value})", "FIX")
                        self.fixes_applied += 1

            # DÉSACTIVER L'AI AUTOMATIQUE - Le plus important !
            if 'AI' in line and 'level' in line.lower():
                # Chercher les lignes comme: AI.RandomColor, AILevel, etc.
                if not stripped.startswith(';') and '=' in line:
                    key = line.split('=')[0].strip()
                    if 'AI' in key or 'ai' in key:
                        # Commenter la ligne
                        lines[i] = f';DISABLED_AI: {line}'
                        self.log(f"  IA désactivée: {key}", "FIX")
                        self.fixes_applied += 1

        # Sauvegarder
        content = '\n'.join(lines)
        self.mugen_cfg.write_text(content, encoding='utf-8')
        return True

    def fix_character_ai_levels(self):
        """Vérifie et corrige les niveaux AI dans les fichiers personnages"""
        self.log("\nVérification des personnages...", "INFO")

        chars_path = self.base_path / "chars"
        if not chars_path.exists():
            return

        ai_chars_fixed = 0

        for char_folder in chars_path.iterdir():
            if not char_folder.is_dir():
                continue

            # Vérifier le .def
            def_files = list(char_folder.glob("*.def"))
            if not def_files:
                continue

            def_file = def_files[0]
            content = def_file.read_text(encoding='utf-8', errors='ignore')

            # Chercher et désactiver AILevel forcé
            if 'AILevel' in content or 'ai.level' in content.lower():
                lines = content.split('\n')
                modified = False

                for i, line in enumerate(lines):
                    if 'AILevel' in line or 'ai.level' in line.lower():
                        if not line.strip().startswith(';') and '=' in line:
                            lines[i] = f';DISABLED: {line}'
                            modified = True

                if modified:
                    content = '\n'.join(lines)
                    def_file.write_text(content, encoding='utf-8')
                    ai_chars_fixed += 1

        if ai_chars_fixed > 0:
            self.log(f"  {ai_chars_fixed} personnages corrigés", "SUCCESS")
            self.fixes_applied += ai_chars_fixed

    def check_controller_config(self):
        """Vérifie la configuration des contrôles"""
        self.log("\nVérification des contrôles...", "INFO")

        if not self.mugen_cfg.exists():
            return

        content = self.mugen_cfg.read_text(encoding='utf-8', errors='ignore')

        # Vérifier que les contrôles joueur sont activés
        if '[P1 Keys]' not in content and '[Input]' not in content:
            self.log("  ⚠️ Configuration contrôles manquante!", "WARNING")
            self.log("  Le jeu utilisera les contrôles par défaut", "INFO")
        else:
            self.log("  ✓ Configuration contrôles OK", "SUCCESS")

    def add_player_control_info(self):
        """Ajoute des infos pour forcer le contrôle joueur"""
        self.log("\nAjout de la configuration contrôle joueur...", "FIX")

        if not self.mugen_cfg.exists():
            return

        content = self.mugen_cfg.read_text(encoding='utf-8', errors='ignore')

        # Chercher la section [Config] et ajouter les paramètres
        if '[Config]' in content:
            # Ajouter juste après [Config]
            config_pos = content.find('[Config]')
            next_section = content.find('[', config_pos + 8)

            if next_section == -1:
                next_section = len(content)

            # Insérer les paramètres de contrôle joueur
            insert_text = """
;=== CONTRÔLE JOUEUR FORCÉ ===
;L'IA ne doit PAS jouer automatiquement pour le joueur humain!
Team.1VS2Life = 100
Team.LoseOnKO = 1
;IA désactivée pour le joueur 1
P1.CPU = 0
;Le joueur 1 est toujours humain
"""

            content = content[:next_section] + insert_text + content[next_section:]

            self.mugen_cfg.write_text(content, encoding='utf-8')
            self.log("  Configuration contrôle joueur ajoutée", "SUCCESS")
            self.fixes_applied += 1

    def create_manual_control_guide(self):
        """Crée un guide pour désactiver manuellement l'IA"""
        guide_file = self.base_path / "DESACTIVER_IA_MANUEL.md"

        guide_content = """# 🎮 Comment Désactiver l'IA Automatique

## Le Problème
L'IA du jeu joue automatiquement à votre place au lieu de vous laisser contrôler.

## Solutions

### 1. Dans le Jeu (Solution Rapide)
Pendant la sélection des personnages:
1. Appuyez sur **START** sur le personnage
2. Maintenez **START** pour le sélectionner en mode MANUEL
3. L'IA ne devrait plus contrôler ce personnage

### 2. Configuration Permanente (mugen.cfg)
Ouvrir `data/mugen.cfg` et modifier:

```ini
[Config]
; Désactiver toute IA pour le joueur
P1.CPU = 0
AIRandomColor = 0

; Le joueur 1 est TOUJOURS humain
Team.1VS2Life = 100
Team.LoseOnKO = 1
```

### 3. Mode de Jeu
Dans les options du jeu:
- Mode : **VS MODE** (pas Training, pas Watch)
- Difficulté : Normale
- P1 Control : **HUMAN** (pas AI, pas AUTO)

### 4. Fichiers Personnages
Certains personnages ont une IA forcée dans leur .def:
- Ouvrir `chars/[nom]/[nom].def`
- Chercher les lignes avec `AILevel` ou `ai.level`
- Les commenter avec un `;` devant

Exemple:
```ini
;AILevel = 8    <- Commenté, IA désactivée
```

### 5. Vérifier les Contrôles
Dans les options:
- Config → Input Config
- Vérifier que vos touches sont bien assignées
- Player 1 doit être en mode **Keyboard** ou **Joystick**

## Si Rien Ne Marche

1. Supprimer `data/mugen.cfg`
2. Relancer le jeu (créera un nouveau fichier par défaut)
3. Reconfigurer vos touches dans les options

## Script de Correction Automatique
Exécutez: `python FIX_AI_AUTOPLAY.py`

Ce script désactive automatiquement tous les paramètres d'IA automatique.
"""

        guide_file.write_text(guide_content, encoding='utf-8')
        self.log(f"Guide créé: {guide_file.name}", "SUCCESS")

    def run(self):
        """Applique toutes les corrections"""
        print("\n" + "="*70)
        print("  🎮 FIX AI AUTOPLAY - Désactivation IA Automatique")
        print("="*70 + "\n")

        # Backup
        if not self.backup_config():
            return False

        print()

        # Corrections
        self.fix_ai_settings()
        self.fix_character_ai_levels()
        self.check_controller_config()
        self.add_player_control_info()
        self.create_manual_control_guide()

        print("\n" + "="*70)
        print(f"  ✓ {self.fixes_applied} CORRECTIONS APPLIQUÉES!")
        print("="*70 + "\n")

        print("L'IA ne devrait plus jouer automatiquement à votre place.")
        print("\n📖 Consultez DESACTIVER_IA_MANUEL.md pour plus d'infos")
        print("\n💡 Astuce: Pendant la sélection, maintenez START sur votre perso")
        print("   pour forcer le mode manuel!\n")

        return True

if __name__ == "__main__":
    fixer = AIAutoplayFixer()
    fixer.run()
