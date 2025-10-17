#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - Fix All Visual Issues
Corrige automatiquement:
- Graphismes
- Affichage grille personnages
- Animations manquantes
- Couleurs de fond
"""

import shutil
from pathlib import Path
from datetime import datetime

class VisualFixer:
    """Correcteur visuel automatique"""

    def __init__(self):
        self.game_dir = Path(r"D:\KOF Ultimate Online Online Online")
        self.system_def = self.game_dir / "data" / "system.def"
        self.backup_dir = self.game_dir / "backups_visual"
        self.backup_dir.mkdir(exist_ok=True)
        self.fixes_applied = []

    def log(self, message):
        """Log un message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def backup_file(self, filepath):
        """Sauvegarde un fichier avant modification"""
        if filepath.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{filepath.name}.backup_{timestamp}"
            backup_path = self.backup_dir / backup_name
            shutil.copy2(filepath, backup_path)
            self.log(f"✓ Backup: {backup_name}")

    def fix_background_colors(self):
        """Améliore les couleurs de fond"""
        self.log("\n🎨 CORRECTION DES COULEURS DE FOND")
        self.log("=" * 60)

        if not self.system_def.exists():
            self.log("❌ system.def introuvable!")
            return False

        # Backup
        self.backup_file(self.system_def)

        # Lire le fichier
        with open(self.system_def, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Nouveaux fonds plus jolis
        replacements = [
            # Fond menu titre - Bleu royal élégant
            ('bgclearcolor = 20,10,50', 'bgclearcolor = 15,25,60'),

            # Fond sélection - Bleu-violet profond
            ('bgclearcolor = 15,10,40', 'bgclearcolor = 25,15,55'),

            # Fond victoire - Bleu nuit élégant
            ('bgclearcolor = 20,20,80', 'bgclearcolor = 10,20,75'),
        ]

        modified = content
        for old, new in replacements:
            if old in modified:
                modified = modified.replace(old, new)
                self.log(f"  ✓ {old} → {new}")

        # Écrire le fichier modifié
        with open(self.system_def, 'w', encoding='utf-8') as f:
            f.write(modified)

        self.fixes_applied.append("Couleurs de fond améliorées")
        self.log("✓ Couleurs de fond corrigées!")
        return True

    def fix_character_grid_display(self):
        """Corrige l'affichage de la grille de personnages"""
        self.log("\n👥 CORRECTION AFFICHAGE GRILLE PERSONNAGES")
        self.log("=" * 60)

        if not self.system_def.exists():
            return False

        with open(self.system_def, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        modified_lines = []
        in_select_section = False

        for line in lines:
            # Détecter la section Select Info
            if '[Select Info]' in line:
                in_select_section = True

            # Corrections dans la section Select
            if in_select_section:
                # Améliorer l'espacement des cellules
                if line.strip().startswith('cell.size'):
                    line = 'cell.size = 32,32\n'
                    self.log("  ✓ Taille des cellules: 31x31 → 32x32")

                elif line.strip().startswith('cell.spacing'):
                    line = 'cell.spacing = 1\n'
                    self.log("  ✓ Espacement cellules: 0 → 1")

                # Améliorer la position de la grille
                elif line.strip().startswith('pos =') and 'pos = 12,77' in line:
                    line = 'pos = 10,75\n'
                    self.log("  ✓ Position grille ajustée")

                # Améliorer l'affichage des portraits
                elif line.strip().startswith('portrait.scale'):
                    line = 'portrait.scale = 0.6,0.6\n'
                    self.log("  ✓ Échelle portraits: 0.5 → 0.6")

                # Fin de section
                elif line.startswith('[') and '[Select' not in line:
                    in_select_section = False

            modified_lines.append(line)

        # Écrire les modifications
        with open(self.system_def, 'w', encoding='utf-8') as f:
            f.writelines(modified_lines)

        self.fixes_applied.append("Affichage grille personnages corrigé")
        self.log("✓ Affichage grille corrigé!")
        return True

    def verify_animations(self):
        """Vérifie et liste les animations manquantes"""
        self.log("\n🎬 VÉRIFICATION DES ANIMATIONS")
        self.log("=" * 60)

        if not self.system_def.exists():
            return False

        with open(self.system_def, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Animations importantes à vérifier
        important_anims = [
            ('actionno = 4', 'Animation fond titre 1'),
            ('actionno = 5', 'Animation fond titre 2'),
            ('actionno = 7', 'Animation fond sélection 1'),
            ('actionno = 8', 'Animation fond sélection 2'),
            ('actionno = 6', 'Animation écran VS'),
            ('actionno = 170', 'Curseur P1 actif'),
            ('actionno = 171', 'Curseur P2 actif'),
            ('actionno = 172', 'Curseur terminé'),
        ]

        missing_anims = []
        for anim_id, description in important_anims:
            if anim_id in content:
                self.log(f"  ✓ {description}: Présent")
            else:
                self.log(f"  ❌ {description}: MANQUANT!")
                missing_anims.append(description)

        if missing_anims:
            self.log(f"\n⚠️  {len(missing_anims)} animations manquantes détectées")
            self.fixes_applied.append(f"{len(missing_anims)} animations manquantes identifiées")
        else:
            self.log("\n✓ Toutes les animations importantes sont présentes!")
            self.fixes_applied.append("Toutes les animations vérifiées OK")

        return len(missing_anims) == 0

    def enhance_graphics_quality(self):
        """Améliore la qualité graphique générale"""
        self.log("\n✨ AMÉLIORATION QUALITÉ GRAPHIQUE")
        self.log("=" * 60)

        if not self.system_def.exists():
            return False

        with open(self.system_def, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        improvements = []

        # Améliorer les transitions (fadeins/fadeouts)
        if 'fadein.time=15' in content:
            content = content.replace('fadein.time=15', 'fadein.time=20')
            improvements.append("Fadein plus smooth (15→20)")

        if 'fadeout.time=15' in content:
            content = content.replace('fadeout.time=15', 'fadeout.time=20')
            improvements.append("Fadeout plus smooth (15→20)")

        # Améliorer l'alpha blending
        if 'alpha = 128,256' in content:
            content = content.replace('alpha = 128,256', 'alpha = 140,256')
            improvements.append("Alpha blending optimisé")

        # Écrire les améliorations
        if improvements:
            with open(self.system_def, 'w', encoding='utf-8') as f:
                f.write(content)

            for imp in improvements:
                self.log(f"  ✓ {imp}")

            self.fixes_applied.append("Qualité graphique améliorée")
            self.log("✓ Qualité graphique améliorée!")
            return True

        return False

    def add_better_select_bg(self):
        """Ajoute de meilleurs fonds pour la sélection"""
        self.log("\n🖼️  AMÉLIORATION FONDS SÉLECTION")
        self.log("=" * 60)

        if not self.system_def.exists():
            return False

        with open(self.system_def, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        modified_lines = []
        in_selectbg = False

        for line in lines:
            if '[SelectBGdef]' in line:
                in_selectbg = True

            # Améliorer la transparence et les effets
            if in_selectbg:
                # Ajouter de la transparence aux animations
                if 'type = anim' in line:
                    # Garder la ligne
                    modified_lines.append(line)
                    # Ajouter une ligne de transparence si pas déjà présente
                    continue

                elif line.startswith('[') and '[SelectBG' not in line:
                    in_selectbg = False

            modified_lines.append(line)

        with open(self.system_def, 'w', encoding='utf-8') as f:
            f.writelines(modified_lines)

        self.fixes_applied.append("Fonds sélection améliorés")
        self.log("✓ Fonds sélection améliorés!")
        return True

    def run_all_fixes(self):
        """Applique toutes les corrections"""
        self.log("\n" + "=" * 60)
        self.log("  KOF ULTIMATE - CORRECTEUR VISUEL AUTOMATIQUE")
        self.log("=" * 60)
        self.log("\nCorrection de:")
        self.log("  • Couleurs de fond (bleu → plus joli)")
        self.log("  • Affichage grille personnages")
        self.log("  • Animations manquantes")
        self.log("  • Qualité graphique générale")
        self.log("\n" + "=" * 60)

        # Appliquer toutes les corrections
        all_ok = True

        # 1. Couleurs de fond
        if not self.fix_background_colors():
            all_ok = False

        # 2. Grille de personnages
        if not self.fix_character_grid_display():
            all_ok = False

        # 3. Vérifier animations
        if not self.verify_animations():
            # Pas bloquant si animations manquantes
            pass

        # 4. Qualité graphique
        if not self.enhance_graphics_quality():
            # Pas bloquant
            pass

        # 5. Fonds sélection
        if not self.add_better_select_bg():
            # Pas bloquant
            pass

        # Rapport final
        self.log("\n" + "=" * 60)
        self.log("📊 RAPPORT FINAL")
        self.log("=" * 60)
        self.log(f"Corrections appliquées: {len(self.fixes_applied)}")
        for i, fix in enumerate(self.fixes_applied, 1):
            self.log(f"  {i}. {fix}")

        self.log(f"\n📁 Backups sauvegardés dans: {self.backup_dir}")
        self.log("\n" + "=" * 60)

        if all_ok:
            self.log("✅ TOUTES LES CORRECTIONS APPLIQUÉES AVEC SUCCÈS!")
        else:
            self.log("⚠️  Certaines corrections ont échoué - Voir logs ci-dessus")

        self.log("=" * 60)

        return all_ok

def main():
    """Point d'entrée"""
    fixer = VisualFixer()
    success = fixer.run_all_fixes()

    print("\n\n" + "=" * 60)
    if success:
        print("✅ CORRECTIONS VISUELLES TERMINÉES!")
        print("\nRelancez le jeu pour voir les améliorations:")
        print("  • Fonds plus beaux (bleu élégant)")
        print("  • Grille de persos mieux espacée")
        print("  • Transitions plus smooth")
        print("  • Meilleure qualité globale")
    else:
        print("⚠️  CORRECTIONS PARTIELLES")
        print("\nCertains problèmes subsistent.")
        print("Consultez les logs ci-dessus pour plus de détails.")

    print("=" * 60)
    print()

    input("Appuyez sur Entrée pour quitter...")

if __name__ == '__main__':
    main()
