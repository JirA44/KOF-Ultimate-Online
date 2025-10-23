#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-correction de la grille de sélection des personnages
Corrige les problèmes:
  1. 191 personnages > 189 slots
  2. Grille trop large (712px > 630px)
"""

import re
from pathlib import Path

class CharacterGridFixer:
    def __init__(self):
        self.base_path = Path("D:/KOF Ultimate Online")
        self.select_def = self.base_path / "data/select.def"
        self.system_def = self.base_path / "data/system.def"
        self.fixes_applied = []

    def log(self, message, level="INFO"):
        """Log avec icônes"""
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "FIX": "🔧"
        }
        print(f"{icons.get(level, '')} {message}")

    def analyze_current_grid(self):
        """Analyse la configuration actuelle"""
        self.log("Analyse de la configuration actuelle...", "INFO")

        if not self.select_def.exists():
            self.log("select.def non trouvé!", "ERROR")
            return None

        # Compter les personnages
        with open(self.select_def, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Compter les lignes de personnages (format: chars/nom/nom.def)
        char_lines = [line for line in content.split('\n')
                      if line.strip() and not line.strip().startswith(';')
                      and 'chars/' in line.lower() and '.def' in line.lower()]

        num_chars = len(char_lines)
        self.log(f"Personnages détectés: {num_chars}", "INFO")

        return num_chars

    def calculate_optimal_grid(self, num_chars):
        """Calcule la meilleure grille pour le nombre de personnages"""
        self.log("\nCalcul de la grille optimale...", "INFO")

        # Contraintes:
        # - Largeur max: ~630px / 32px = 19 colonnes max
        # - Hauteur: on peut aller jusqu'à 12-15 lignes

        max_cols = 19  # Pour tenir dans 630px avec cellules de 32px

        # Trouver la meilleure combinaison
        best_rows = None
        best_cols = None
        best_waste = float('inf')

        for cols in range(10, max_cols + 1):
            rows = (num_chars + cols - 1) // cols  # Arrondi vers le haut
            total_slots = rows * cols
            waste = total_slots - num_chars

            if waste < best_waste and waste >= 0:
                best_waste = waste
                best_rows = rows
                best_cols = cols

        self.log(f"Grille optimale: {best_rows} × {best_cols} = {best_rows * best_cols} slots", "SUCCESS")
        self.log(f"Personnages: {num_chars}, Slots vides: {best_waste}", "INFO")
        self.log(f"Largeur: {best_cols * 32}px (< 630px ✓)", "SUCCESS")

        return best_rows, best_cols

    def fix_system_def_grid(self, rows, cols):
        """Corrige les paramètres de grille dans system.def"""
        self.log("\n🔧 Correction de la grille dans system.def...", "FIX")

        if not self.system_def.exists():
            self.log("system.def non trouvé!", "ERROR")
            return False

        # Backup
        backup_path = self.system_def.with_suffix('.def.backup_grid')
        with open(self.system_def, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)

        self.log(f"Backup créé: {backup_path.name}", "SUCCESS")

        # Modifier la grille dans [Select Info]
        pattern = r'rows\s*=\s*\d+'
        replacement = f'rows = {rows}'
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

        pattern = r'columns\s*=\s*\d+'
        replacement = f'columns = {cols}'
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

        # Écrire le fichier corrigé
        with open(self.system_def, 'w', encoding='utf-8') as f:
            f.write(content)

        self.log(f"system.def grille mis à jour: {rows}×{cols}", "SUCCESS")
        self.fixes_applied.append(f"Grid updated to {rows}×{cols} in system.def")
        return True


    def run(self):
        """Exécute toutes les corrections"""
        print("\n" + "="*60)
        print("  🔧 AUTO-FIX: Character Grid")
        print("="*60 + "\n")

        # 1. Analyser
        num_chars = self.analyze_current_grid()
        if num_chars is None:
            self.log("Impossible d'analyser la grille", "ERROR")
            return False

        # 2. Calculer la grille optimale
        rows, cols = self.calculate_optimal_grid(num_chars)

        # 3. Appliquer les corrections
        self.fix_system_def_grid(rows, cols)

        # 4. Résumé
        print("\n" + "="*60)
        print("  ✅ CORRECTIONS APPLIQUÉES")
        print("="*60)
        for fix in self.fixes_applied:
            self.log(fix, "SUCCESS")

        print("\n" + "="*60)
        print("  💡 RECOMMANDATIONS")
        print("="*60)
        self.log("Relancez le jeu pour voir les changements", "INFO")
        self.log("Les backups sont disponibles (.def.backup)", "INFO")

        return True

if __name__ == "__main__":
    import sys
    fixer = CharacterGridFixer()
    success = fixer.run()

    if success:
        print("\n✅ Auto-correction terminée avec succès!")
    else:
        print("\n❌ Échec de l'auto-correction")

    sys.exit(0 if success else 1)
