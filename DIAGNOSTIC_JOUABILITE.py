#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNOSTIC DE JOUABILITÉ - KOF ULTIMATE ONLINE
Analyse et corrige tous les problèmes de jouabilité
Standard éditeur professionnel (Blizzard, PlayStation, Xbox)
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

class PlayabilityDiagnostic:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.issues = []
        self.fixes_applied = []
        self.critical_issues = []

    def print_header(self):
        """Affiche le header du diagnostic"""
        print("\n" + "="*70)
        print(" " * 15 + "KOF ULTIMATE ONLINE")
        print(" " * 10 + "DIAGNOSTIC DE JOUABILITÉ PROFESSIONNEL")
        print("="*70 + "\n")

    def check_game_executable(self):
        """Vérifie que l'exécutable du jeu existe"""
        print("[1/10] Vérification de l'exécutable du jeu...")

        mugen_exe = self.base_path / "KOF_Ultimate_Online.exe"
        ikemen_exe = self.base_path / "Ikemen_GO" / "Ikemen_GO.exe"

        if mugen_exe.exists():
            print(f"   ✓ M.U.G.E.N trouvé: {mugen_exe.name}")
            return True
        elif ikemen_exe.exists():
            print(f"   ✓ Ikemen GO trouvé: {ikemen_exe.name}")
            return True
        else:
            self.critical_issues.append("Aucun exécutable de jeu trouvé!")
            print("   ✗ CRITIQUE: Aucun exécutable trouvé!")
            return False

    def check_mugen_config(self):
        """Vérifie la configuration M.U.G.E.N pour la jouabilité"""
        print("\n[2/10] Analyse de la configuration M.U.G.E.N...")

        config_file = self.base_path / "data" / "mugen.cfg"
        if not config_file.exists():
            self.critical_issues.append("mugen.cfg introuvable!")
            print("   ✗ mugen.cfg introuvable!")
            return False

        with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
            config = f.read()

        # Vérifications de jouabilité
        checks = {
            'Résolution vidéo': (r'width\s*=\s*(\d+)', r'height\s*=\s*(\d+)'),
            'Mode plein écran': (r'fullscreen\s*=\s*([01])',),
            'VSync': (r'vretrace\s*=\s*([01])',),
            'Framerate': (r'gamespeed\s*=\s*(\d+)',),
            'Mode de rendu': (r'rendermode\s*=\s*(\w+)',),
        }

        issues_found = []

        # Résolution
        width_match = re.search(r'width\s*=\s*(\d+)', config)
        height_match = re.search(r'height\s*=\s*(\d+)', config)
        if width_match and height_match:
            width, height = int(width_match.group(1)), int(height_match.group(1))
            print(f"   ✓ Résolution: {width}x{height}")

            if width < 640 or height < 480:
                issues_found.append("Résolution trop basse (< 640x480)")
            elif width > 1920 or height > 1080:
                issues_found.append("Résolution très élevée (risque de lag)")

        # Mode plein écran
        fullscreen_match = re.search(r'fullscreen\s*=\s*([01])', config)
        if fullscreen_match:
            fullscreen = int(fullscreen_match.group(1))
            mode = "Plein écran" if fullscreen == 1 else "Fenêtré"
            print(f"   ✓ Mode d'affichage: {mode}")

        # VSync
        vretrace_match = re.search(r'vretrace\s*=\s*([01])', config)
        if vretrace_match:
            vretrace = int(vretrace_match.group(1))
            if vretrace == 1:
                issues_found.append("VSync activé (peut causer du lag d'entrée)")
                print("   ⚠ VSync activé (risque de lag d'entrée)")
            else:
                print("   ✓ VSync désactivé (bonne réactivité)")

        # Framerate
        framerate_match = re.search(r'gamespeed\s*=\s*(\d+)', config)
        if framerate_match:
            framerate = int(framerate_match.group(1))
            if framerate != 60:
                issues_found.append(f"Framerate non standard ({framerate} au lieu de 60)")
                print(f"   ⚠ Framerate: {framerate} (recommandé: 60)")
            else:
                print(f"   ✓ Framerate: 60 FPS")

        # Mode de rendu
        rendermode_match = re.search(r'rendermode\s*=\s*(\w+)', config)
        if rendermode_match:
            rendermode = rendermode_match.group(1)
            print(f"   ✓ Mode de rendu: {rendermode}")

        self.issues.extend(issues_found)
        return len(issues_found) == 0

    def check_input_config(self):
        """Vérifie la configuration des contrôles"""
        print("\n[3/10] Vérification de la configuration des contrôles...")

        config_file = self.base_path / "data" / "mugen.cfg"
        with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
            config = f.read()

        # Vérifier que P1 peut utiliser le clavier
        p1_keyboard = re.search(r'p1\.usekeyboard\s*=\s*([01])', config)
        if p1_keyboard and int(p1_keyboard.group(1)) == 1:
            print("   ✓ Clavier activé pour Joueur 1")
        else:
            self.issues.append("Clavier désactivé pour Joueur 1")
            print("   ✗ Clavier désactivé pour Joueur 1")

        # Vérifier la config joystick
        p1_joystick = re.search(r'p1\.joystick\.type\s*=\s*(\d+)', config)
        if p1_joystick:
            joystick_type = int(p1_joystick.group(1))
            if joystick_type == 0:
                print("   ✓ Manette configurée (DirectInput)")
            elif joystick_type == -1:
                print("   ⚠ Manette désactivée")

        # Vérifier que P1.CPU est désactivé
        p1_cpu = re.search(r'P1\.CPU\s*=\s*([01])', config)
        if p1_cpu and int(p1_cpu.group(1)) == 0:
            print("   ✓ IA désactivée pour Joueur 1 (contrôle humain)")
        elif p1_cpu and int(p1_cpu.group(1)) == 1:
            self.critical_issues.append("P1.CPU activé - IA contrôle le joueur!")
            print("   ✗ CRITIQUE: IA activée pour Joueur 1!")

        return len(self.critical_issues) == 0

    def check_character_select(self):
        """Vérifie le character select"""
        print("\n[4/10] Vérification du character select...")

        select_file = self.base_path / "data" / "select.def"
        if not select_file.exists():
            self.critical_issues.append("select.def introuvable!")
            print("   ✗ select.def introuvable!")
            return False

        with open(select_file, 'r', encoding='utf-8', errors='ignore') as f:
            select_content = f.read()

        # Compter les personnages
        chars_pattern = r'^[^;]*,\s*(?:stages|random)'
        char_lines = [line for line in select_content.split('\n')
                     if re.match(r'^[a-zA-Z0-9_\-/]+\s*,', line) and not line.strip().startswith(';')]

        char_count = len(char_lines)
        print(f"   ✓ {char_count} personnages dans select.def")

        if char_count < 10:
            self.issues.append(f"Très peu de personnages ({char_count})")
            print(f"   ⚠ Seulement {char_count} personnages (peu de contenu)")

        # Vérifier la grille
        rows_match = re.search(r'rows\s*=\s*(\d+)', select_content)
        cols_match = re.search(r'columns\s*=\s*(\d+)', select_content)

        if rows_match and cols_match:
            rows = int(rows_match.group(1))
            cols = int(cols_match.group(1))
            grid_size = rows * cols
            print(f"   ✓ Grille: {rows}x{cols} ({grid_size} emplacements)")

            if grid_size < char_count:
                self.issues.append("Grille trop petite pour tous les personnages")
                print(f"   ⚠ Grille trop petite ({grid_size} < {char_count})")

        return True

    def check_stages(self):
        """Vérifie les stages"""
        print("\n[5/10] Vérification des stages...")

        stages_dir = self.base_path / "stages"
        if not stages_dir.exists():
            self.critical_issues.append("Dossier stages/ introuvable!")
            print("   ✗ Dossier stages/ introuvable!")
            return False

        # Compter les fichiers .def
        stage_files = list(stages_dir.glob("*.def"))
        print(f"   ✓ {len(stage_files)} stages trouvés")

        if len(stage_files) < 5:
            self.issues.append(f"Très peu de stages ({len(stage_files)})")
            print(f"   ⚠ Seulement {len(stage_files)} stages")

        return True

    def check_sound_config(self):
        """Vérifie la configuration audio"""
        print("\n[6/10] Vérification de la configuration audio...")

        config_file = self.base_path / "data" / "mugen.cfg"
        with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
            config = f.read()

        # Vérifier que le son est activé
        sound_match = re.search(r'sound\s*=\s*([01])', config)
        if sound_match and int(sound_match.group(1)) == 1:
            print("   ✓ Son activé")
        else:
            self.issues.append("Son désactivé")
            print("   ⚠ Son désactivé")

        # Vérifier le volume
        master_vol = re.search(r'mastervolume\s*=\s*(\d+)', config)
        if master_vol:
            vol = int(master_vol.group(1))
            print(f"   ✓ Volume principal: {vol}%")
            if vol < 10:
                self.issues.append(f"Volume très faible ({vol}%)")

        return True

    def check_fonts(self):
        """Vérifie les polices d'écriture"""
        print("\n[7/10] Vérification des polices...")

        font_dir = self.base_path / "font"
        if font_dir.exists():
            font_files = list(font_dir.glob("*.fnt")) + list(font_dir.glob("*.def"))
            print(f"   ✓ {len(font_files)} fichiers de police trouvés")
        else:
            self.issues.append("Dossier font/ introuvable")
            print("   ⚠ Dossier font/ introuvable")

        return True

    def check_running_processes(self):
        """Vérifie les processus en conflit"""
        print("\n[8/10] Vérification des processus en conflit...")

        import subprocess

        # Vérifier si des scripts IA tournent
        try:
            result = subprocess.run(['tasklist'], capture_output=True, text=True)

            python_count = result.stdout.count('python.exe')
            if python_count > 1:  # 1 = ce script
                self.issues.append(f"{python_count - 1} processus Python en arrière-plan (possibles scripts IA)")
                print(f"   ⚠ {python_count - 1} processus Python détectés (risque de scripts IA)")
            else:
                print("   ✓ Aucun processus en conflit")
        except:
            print("   ⚠ Impossible de vérifier les processus")

        return True

    def check_performance_config(self):
        """Vérifie les paramètres de performance"""
        print("\n[9/10] Vérification des paramètres de performance...")

        config_file = self.base_path / "data" / "mugen.cfg"
        with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
            config = f.read()

        # Paramètres de performance
        checks = [
            ('precache', r'precache\s*=\s*([01])'),
            ('playercache', r'playercache\s*=\s*(\d+)'),
            ('explodmax', r'explodmax\s*=\s*(\d+)'),
            ('helpermax', r'helpermax\s*=\s*(\d+)'),
        ]

        for name, pattern in checks:
            match = re.search(pattern, config)
            if match:
                value = match.group(1)
                print(f"   ✓ {name}: {value}")

        return True

    def apply_critical_fixes(self):
        """Applique les corrections critiques"""
        print("\n[10/10] Application des corrections critiques...")

        config_file = self.base_path / "data" / "mugen.cfg"

        if not config_file.exists():
            print("   ✗ Impossible de corriger: mugen.cfg introuvable")
            return False

        with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
            config = f.read()

        original_config = config
        fixes_count = 0

        # Fix 1: Désactiver VSync si activé
        if re.search(r'vretrace\s*=\s*1', config):
            config = re.sub(r'vretrace\s*=\s*1', 'vretrace = 0', config)
            self.fixes_applied.append("VSync désactivé pour réduire le lag d'entrée")
            fixes_count += 1

        # Fix 2: S'assurer que P1.CPU = 0
        if re.search(r'P1\.CPU\s*=\s*1', config):
            config = re.sub(r'P1\.CPU\s*=\s*1', 'P1.CPU = 0', config)
            self.fixes_applied.append("IA désactivée pour Joueur 1")
            fixes_count += 1

        # Fix 3: Activer le clavier pour P1
        if re.search(r'p1\.usekeyboard\s*=\s*0', config):
            config = re.sub(r'p1\.usekeyboard\s*=\s*0', 'p1.usekeyboard = 1', config)
            self.fixes_applied.append("Clavier activé pour Joueur 1")
            fixes_count += 1

        # Fix 4: Framerate à 60 si différent
        if re.search(r'gamespeed\s*=\s*(?!60)\d+', config):
            config = re.sub(r'gamespeed\s*=\s*\d+', 'gamespeed = 60', config)
            self.fixes_applied.append("Framerate ajusté à 60 FPS")
            fixes_count += 1

        # Fix 5: Son activé
        if re.search(r'sound\s*=\s*0', config):
            config = re.sub(r'sound\s*=\s*0', 'sound = 1', config)
            self.fixes_applied.append("Son activé")
            fixes_count += 1

        # Sauvegarder si des changements ont été faits
        if config != original_config:
            # Backup
            backup_file = config_file.parent / f"mugen.cfg.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(original_config)

            # Écrire la nouvelle config
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(config)

            print(f"   ✓ {fixes_count} corrections appliquées")
            print(f"   ✓ Backup sauvegardé: {backup_file.name}")
        else:
            print("   ✓ Aucune correction nécessaire")

        return True

    def generate_report(self):
        """Génère le rapport final"""
        print("\n" + "="*70)
        print(" " * 20 + "RAPPORT DE DIAGNOSTIC")
        print("="*70 + "\n")

        # Résumé
        total_issues = len(self.issues) + len(self.critical_issues)

        if len(self.critical_issues) > 0:
            print("🔴 STATUT: PROBLÈMES CRITIQUES DÉTECTÉS")
            print(f"\n   {len(self.critical_issues)} problème(s) critique(s):")
            for issue in self.critical_issues:
                print(f"   • {issue}")
        elif len(self.issues) > 0:
            print("🟡 STATUT: JOUABLE AVEC AVERTISSEMENTS")
            print(f"\n   {len(self.issues)} avertissement(s):")
            for issue in self.issues:
                print(f"   • {issue}")
        else:
            print("🟢 STATUT: PARFAITEMENT JOUABLE")
            print("\n   ✓ Aucun problème détecté!")

        # Corrections appliquées
        if len(self.fixes_applied) > 0:
            print(f"\n✅ CORRECTIONS APPLIQUÉES ({len(self.fixes_applied)}):")
            for fix in self.fixes_applied:
                print(f"   • {fix}")

        # Recommandations
        print("\n📋 RECOMMANDATIONS:")
        print("   1. Utiliser PLAY_MINI_WINDOW.bat pour mode fenêtré optimisé")
        print("   2. Fermer tous les scripts Python avant de jouer")
        print("   3. Pour une meilleure expérience:")
        print("      - Utiliser une manette (Xbox/PlayStation)")
        print("      - Désactiver programmes en arrière-plan")
        print("      - Vérifier que VSync est désactivé (fait)")

        print("\n" + "="*70)
        print(" " * 15 + "DIAGNOSTIC TERMINÉ")
        print("="*70 + "\n")

    def run(self):
        """Execute le diagnostic complet"""
        self.print_header()

        # Exécuter tous les checks
        self.check_game_executable()
        self.check_mugen_config()
        self.check_input_config()
        self.check_character_select()
        self.check_stages()
        self.check_sound_config()
        self.check_fonts()
        self.check_running_processes()
        self.check_performance_config()
        self.apply_critical_fixes()

        # Générer le rapport
        self.generate_report()

        return len(self.critical_issues) == 0

if __name__ == "__main__":
    diagnostic = PlayabilityDiagnostic()
    success = diagnostic.run()

    print("\nAppuyez sur Entrée pour fermer...")
    input()

    sys.exit(0 if success else 1)
