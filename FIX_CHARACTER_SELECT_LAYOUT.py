#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIX CHARACTER SELECT LAYOUT - KOF ULTIMATE
Optimise l'affichage de l'écran de sélection avec des spacers
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

class CharSelectLayoutFixer:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.select_def = self.base_path / "data" / "select.def"
        self.system_def = self.base_path / "data" / "system.def"

    def log(self, message, level="INFO"):
        """Affiche un message avec niveau"""
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✓",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "FIX": "🔧"
        }
        icon = icons.get(level, "•")
        print(f"{icon} {message}")

    def get_current_grid_config(self):
        """Récupère la configuration de la grille"""
        content = self.system_def.read_text(encoding='utf-8', errors='ignore')

        import re
        rows = int(re.search(r'rows\s*=\s*(\d+)', content).group(1))
        columns = int(re.search(r'columns\s*=\s*(\d+)', content).group(1))

        return rows, columns

    def load_characters(self):
        """Charge la liste des personnages"""
        content = self.select_def.read_text(encoding='utf-8', errors='ignore')

        characters = []
        in_characters = False

        for line in content.split('\n'):
            line = line.strip()

            if line == '[Characters]':
                in_characters = True
                continue
            elif line.startswith('['):
                break
            elif in_characters and line and not line.startswith(';'):
                characters.append(line)

        return characters

    def create_optimized_layout(self, characters, rows, columns):
        """Crée un layout optimisé avec spacers"""
        total_slots = rows * columns
        num_chars = len(characters)

        self.log(f"\n📊 Configuration actuelle:", "INFO")
        self.log(f"  Grille: {rows}×{columns} = {total_slots} slots", "INFO")
        self.log(f"  Personnages: {num_chars}", "INFO")
        self.log(f"  Slots vides disponibles: {total_slots - num_chars}", "INFO")

        # Stratégie: répartir les personnages avec des espaces
        # Pour éviter le chevauchement des grands portraits, on met des spacers tous les X personnages

        optimized = []
        spacer_interval = 15  # Ajouter un spacer tous les 15 personnages

        for i, char in enumerate(characters):
            optimized.append(char)

            # Ajouter un spacer après chaque intervalle (sauf le dernier)
            if (i + 1) % spacer_interval == 0 and i < len(characters) - 1:
                # Ajouter une case vide
                optimized.append("")  # Case vide

        self.log(f"\n🔧 Nouveau layout:", "FIX")
        self.log(f"  Personnages: {len([c for c in optimized if c])}", "INFO")
        self.log(f"  Spacers ajoutés: {len([c for c in optimized if not c])}", "INFO")

        return optimized

    def apply_layout(self, optimized_chars):
        """Applique le nouveau layout à select.def"""
        # Backup
        backup_file = self.select_def.with_suffix(f'.def.layout_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        shutil.copy2(self.select_def, backup_file)
        self.log(f"\n✓ Backup créé: {backup_file.name}", "SUCCESS")

        # Lire le fichier actuel
        content = self.select_def.read_text(encoding='utf-8', errors='ignore')

        # Trouver la section [Characters]
        lines = content.split('\n')
        new_lines = []
        in_characters = False
        characters_written = False

        for line in lines:
            if line.strip() == '[Characters]':
                in_characters = True
                new_lines.append(line)
                new_lines.append("")
                # Écrire les personnages optimisés
                for char in optimized_chars:
                    new_lines.append(char if char else "")  # Case vide = ligne vide
                characters_written = True
                continue
            elif line.strip().startswith('[') and in_characters:
                # Fin de la section Characters
                in_characters = False
                new_lines.append("")
                new_lines.append(line)
                continue
            elif not in_characters:
                new_lines.append(line)

        # Sauvegarder
        self.select_def.write_text('\n'.join(new_lines), encoding='utf-8')
        self.log(f"✓ Fichier sauvegardé: {self.select_def}", "SUCCESS")

    def run(self):
        """Exécute le fix complet"""
        print("\n" + "="*60)
        print("  🎨 FIX CHARACTER SELECT LAYOUT")
        print("="*60 + "\n")

        # 1. Récupérer la config
        rows, columns = self.get_current_grid_config()

        # 2. Charger les personnages
        characters = self.load_characters()

        # 3. Créer layout optimisé
        optimized = self.create_optimized_layout(characters, rows, columns)

        # 4. Demander confirmation
        self.log("\n⚠️  Cette modification va réorganiser l'écran de sélection", "WARNING")
        self.log("  Des cases vides seront ajoutées pour espacer les personnages", "INFO")
        user_input = input("\nContinuer? (o/N): ")

        if user_input.lower() not in ['o', 'oui', 'y', 'yes']:
            self.log("Opération annulée par l'utilisateur", "INFO")
            return False

        # 5. Appliquer
        self.apply_layout(optimized)

        print("\n" + "="*60)
        print("  ✓ LAYOUT OPTIMISÉ!")
        print("="*60)
        print("\nRelance le jeu pour voir les changements.")
        print("="*60 + "\n")

        return True

if __name__ == "__main__":
    fixer = CharSelectLayoutFixer()
    success = fixer.run()

    if not success:
        sys.exit(1)
