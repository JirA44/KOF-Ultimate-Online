"""
KOF Ultimate - Launcher avec Auto-Diagnostic
Détecte automatiquement les problèmes et corrige ce qui peut l'être
"""

import os
import sys
import subprocess
import time
from pathlib import Path

class SmartLauncher:
    """Launcher intelligent avec auto-diagnostic et correction"""

    def __init__(self):
        self.base_path = Path("D:/KOF Ultimate Online")
        self.errors = []
        self.warnings = []
        self.fixes = []

    def log(self, message, level="INFO"):
        """Log avec couleurs"""
        colors = {
            "INFO": "",
            "SUCCESS": "✓ ",
            "WARNING": "⚠️  ",
            "ERROR": "❌ ",
            "FIX": "🔧 "
        }
        prefix = colors.get(level, "")
        print(f"{prefix}{message}")

    def check_mugen_engine(self):
        """Vérifie que MUGEN est disponible"""
        self.log("\n📦 Vérification M.U.G.E.N...", "INFO")

        exe_path = self.base_path / "KOF_Ultimate_Online.exe"
        data_path = self.base_path / "data"
        cfg_path = self.base_path / "data/mugen.cfg"

        all_ok = True

        if not exe_path.exists():
            self.log("  KOF_Ultimate_Online.exe: MANQUANT", "ERROR")
            self.errors.append("MUGEN executable missing")
            all_ok = False
        else:
            self.log("  KOF_Ultimate_Online.exe: OK", "SUCCESS")

        if not data_path.exists():
            self.log("  data/ folder: MANQUANT", "ERROR")
            self.errors.append("MUGEN data folder missing")
            all_ok = False
        else:
            self.log("  data/ folder: OK", "SUCCESS")

        if not cfg_path.exists():
            self.log("  mugen.cfg: MANQUANT", "WARNING")
            self.warnings.append("MUGEN config missing")
        else:
            self.log("  mugen.cfg: OK", "SUCCESS")

        return all_ok

    def check_ikemen_engine(self):
        """Vérifie que Ikemen GO est disponible et répare si nécessaire"""
        self.log("\n📦 Vérification Ikemen GO...", "INFO")

        ikemen_path = self.base_path / "Ikemen_GO"
        exe_path = ikemen_path / "Ikemen_GO.exe"
        font_path = ikemen_path / "font"
        data_path = ikemen_path / "data"
        debug_font_path = ikemen_path / "font/debug.def"
        log_path = ikemen_path / "Ikemen.log"

        all_ok = True

        # Vérifier l'exécutable
        if not exe_path.exists():
            self.log("  Ikemen_GO.exe: MANQUANT", "ERROR")
            self.errors.append("Ikemen GO executable missing")
            all_ok = False
        else:
            self.log("  Ikemen_GO.exe: OK", "SUCCESS")

        # Vérifier les dossiers critiques (peuvent être des liens symboliques)
        critical_folders = {
            "data": data_path,
            "font": font_path,
            "chars": ikemen_path / "chars",
            "stages": ikemen_path / "stages",
            "sound": ikemen_path / "sound"
        }

        missing_folders = []
        for folder_name, folder_path in critical_folders.items():
            if not folder_path.exists():
                self.log(f"  {folder_name}/ folder: MANQUANT", "ERROR")
                missing_folders.append(folder_name)
                all_ok = False
            else:
                self.log(f"  {folder_name}/ folder: OK", "SUCCESS")

        # Si des dossiers manquent, essayer de les réparer automatiquement
        if missing_folders:
            self.log("\n🔧 AUTO-FIX: Réparation des dossiers Ikemen GO...", "FIX")
            if self.auto_fix_ikemen_folders(ikemen_path):
                # Revérifier après fix
                for folder_name, folder_path in critical_folders.items():
                    if folder_name in missing_folders and folder_path.exists():
                        self.log(f"  {folder_name}/ folder: RÉPARÉ ✓", "FIX")
                        self.fixes.append(f"Fixed {folder_name} folder link")
                        missing_folders.remove(folder_name)
                        all_ok = True

        # Vérifier debug.def seulement si font existe maintenant
        if font_path.exists():
            if not debug_font_path.exists():
                self.log("  font/debug.def: MANQUANT - AUTO-FIX", "WARNING")
                self.auto_fix_debug_font(ikemen_path)
            else:
                self.log("  font/debug.def: OK", "SUCCESS")

        # Vérifier le log d'erreurs précédent
        if log_path.exists():
            try:
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    log_content = f.read()

                if "error" in log_content.lower() or "can't load" in log_content.lower():
                    self.log("  Log d'erreur détecté", "WARNING")
                    self.warnings.append("Previous Ikemen GO errors detected")

                    # Afficher les dernières erreurs
                    lines = log_content.strip().split('\n')
                    if lines:
                        self.log("    Dernière erreur:", "INFO")
                        for line in lines[-5:]:
                            if line.strip():
                                self.log(f"      {line.strip()}", "WARNING")
            except:
                pass

        return all_ok

    def auto_fix_ikemen_folders(self, ikemen_path):
        """Répare automatiquement les dossiers Ikemen GO en exécutant le script PowerShell"""
        try:
            ps_script = self.base_path / "FIX_IKEMEN_FORCE.ps1"

            if not ps_script.exists():
                self.log("  ❌ Script FIX_IKEMEN_FORCE.ps1 introuvable", "ERROR")
                return False

            # Exécuter le script PowerShell avec variables d'environnement
            import os
            env = os.environ.copy()
            env['AUTOMATED_RUN'] = '1'

            result = subprocess.run(
                ['powershell', '-ExecutionPolicy', 'Bypass', '-NoProfile',
                 '-Command', f'& "{ps_script}"'],
                capture_output=True,
                text=True,
                timeout=30,
                env=env
            )

            if result.returncode == 0 or "data/system.def found" in result.stdout:
                self.log("  ✓ Dossiers Ikemen GO réparés", "FIX")
                self.fixes.append("Repaired Ikemen GO folder structure")
                return True
            else:
                self.log(f"  ⚠️  Réparation partielle", "WARNING")
                return False

        except Exception as e:
            self.log(f"  ❌ Impossible de réparer: {e}", "ERROR")
            return False

    def auto_fix_debug_font(self, ikemen_path):
        """Crée automatiquement le fichier debug.def manquant"""
        try:
            debug_font_path = ikemen_path / "font/debug.def"

            debug_content = """[FNT v2]
; FNT v2 version number.  Don't change this.
fntversion = 2,00
; Name of this font.
name = "Debug Font"
; This font is used for debug display

[Def]
; This is a bitmap font
Type = bitmap
; Size of font: width, height.  Width is used for spaces.
Size = 3,6
; Spacing between font glyphs: width, height.
Spacing = 1,0
; Drawing offset: x, y.
Offset = 0,1
; Filename of the sff containing the glyphs.  Use sff v2 only.
File = f-4x6.sff

; Note: All units are in pixels.
; Text rendered with bitmap fonts may be in ASCII only.
"""

            with open(debug_font_path, 'w', encoding='utf-8') as f:
                f.write(debug_content)

            self.log("  ✓ debug.def créé automatiquement", "FIX")
            self.fixes.append("Created missing debug.def font file")
            return True
        except Exception as e:
            self.log(f"  ❌ Impossible de créer debug.def: {e}", "ERROR")
            return False

    def check_and_fix_air_files(self):
        """Vérifie et corrige automatiquement les erreurs CLSN dans les fichiers AIR"""
        self.log("\n🔍 Vérification des fichiers AIR...", "INFO")

        fix_script = self.base_path / "FIX_ALL_CLSN_COMPLETE.py"

        if not fix_script.exists():
            self.log("  ⚠️  Script de correction AIR non trouvé", "WARNING")
            return False

        try:
            # Exécuter le script de correction
            result = subprocess.run(
                [sys.executable, str(fix_script)],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(self.base_path)
            )

            # Analyser le résultat
            if "0 fichiers corrigés" in result.stdout:
                self.log("  ✓ Aucune erreur AIR détectée", "SUCCESS")
                return True
            elif "fichiers corrigés" in result.stdout:
                # Extraire le nombre de fichiers corrigés
                import re
                match = re.search(r'(\d+) fichiers corrigés', result.stdout)
                if match:
                    num_fixed = match.group(1)
                    self.log(f"  🔧 {num_fixed} fichiers AIR corrigés automatiquement", "FIX")
                    self.fixes.append(f"Fixed {num_fixed} AIR files with CLSN errors")
                return True
            else:
                self.log("  ✓ Vérification AIR terminée", "SUCCESS")
                return True

        except subprocess.TimeoutExpired:
            self.log("  ⚠️  Timeout de la vérification AIR", "WARNING")
            return False
        except Exception as e:
            self.log(f"  ❌ Erreur lors de la vérification AIR: {e}", "ERROR")
            return False

    def check_char_select_config(self):
        """Vérifie la configuration de l'écran de sélection des personnages"""
        self.log("\n🎮 Vérification Character Select...", "INFO")

        system_def = self.base_path / "data/system.def"
        select_def = self.base_path / "data/select.def"

        if not system_def.exists():
            self.log("  ❌ system.def non trouvé", "ERROR")
            return False

        if not select_def.exists():
            self.log("  ❌ select.def non trouvé", "ERROR")
            return False

        try:
            # Compter les personnages dans select.def
            with open(select_def, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            in_characters = False
            char_count = 0
            for line in lines:
                stripped = line.strip()
                if stripped == "[Characters]":
                    in_characters = True
                    continue
                if in_characters:
                    if stripped.startswith('['):
                        break
                    if stripped and not stripped.startswith(';'):
                        char_count += 1

            # Lire la configuration de la grille
            with open(system_def, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            rows = 10
            columns = 20
            cell_size = "30,30"

            for line in content.split('\n'):
                if line.strip().startswith('rows ='):
                    rows = int(line.split('=')[1].strip())
                elif line.strip().startswith('columns ='):
                    columns = int(line.split('=')[1].strip())
                elif line.strip().startswith('cell.size ='):
                    cell_size = line.split('=')[1].strip()

            total_slots = rows * columns

            self.log(f"  Personnages: {char_count}", "INFO")
            self.log(f"  Grille: {rows}×{columns} = {total_slots} slots", "INFO")
            self.log(f"  Taille cellule: {cell_size}", "INFO")

            # Vérifier si la configuration est optimale
            cell_w, cell_h = map(int, cell_size.split(','))

            if char_count > total_slots:
                self.log(f"  ⚠️  PROBLÈME: {char_count} personnages > {total_slots} slots!", "WARNING")
                self.warnings.append("Not enough slots for all characters")
            elif total_slots - char_count > 50:
                self.log(f"  ⚠️  Trop de slots vides ({total_slots - char_count})", "WARNING")
                self.warnings.append("Too many empty slots in grid")

            if cell_w < 32 or cell_h < 32:
                self.log(f"  ⚠️  Cellules trop petites ({cell_size})", "WARNING")
                self.warnings.append("Character cells too small")

            # Vérifier largeur écran
            spacing = 2
            total_width = columns * cell_w + (columns - 1) * spacing
            if total_width > 630:
                self.log(f"  ⚠️  Grille trop large ({total_width}px > 630px)", "WARNING")
                self.warnings.append("Grid too wide for screen")

            if not self.warnings or all("character" not in w.lower() and "grid" not in w.lower() and "slot" not in w.lower() for w in self.warnings):
                self.log("  ✓ Configuration optimale", "SUCCESS")

            return True

        except Exception as e:
            self.log(f"  ❌ Erreur: {e}", "ERROR")
            return False

    def launch_mugen(self):
        """Lance M.U.G.E.N"""
        self.log("\n🚀 Lancement M.U.G.E.N...", "INFO")

        exe_path = self.base_path / "KOF_Ultimate_Online.exe"

        try:
            # Lancer le jeu
            subprocess.Popen([str(exe_path)], cwd=str(self.base_path))
            self.log("✓ M.U.G.E.N lancé avec succès!", "SUCCESS")
            return True
        except Exception as e:
            self.log(f"❌ Erreur au lancement: {e}", "ERROR")
            return False

    def launch_ikemen(self):
        """Lance Ikemen GO"""
        self.log("\n🚀 Lancement Ikemen GO...", "INFO")

        ikemen_path = self.base_path / "Ikemen_GO"
        exe_path = ikemen_path / "Ikemen_GO.exe"
        log_path = ikemen_path / "Ikemen.log"

        # Supprimer l'ancien log pour voir les nouvelles erreurs
        if log_path.exists():
            try:
                log_path.unlink()
                self.log("  Ancien log supprimé", "INFO")
            except:
                pass

        try:
            # Lancer le jeu
            process = subprocess.Popen([str(exe_path)], cwd=str(ikemen_path))

            # Attendre un peu pour voir si ça crash immédiatement
            time.sleep(2)

            # Vérifier si le processus est encore en cours
            if process.poll() is not None:
                self.log("⚠️  Ikemen GO s'est arrêté immédiatement", "WARNING")

                # Lire le log d'erreur
                if log_path.exists():
                    self.log("\n📋 Log d'erreur:", "ERROR")
                    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                        print(f.read())

                return False
            else:
                self.log("✓ Ikemen GO lancé avec succès!", "SUCCESS")
                return True
        except Exception as e:
            self.log(f"❌ Erreur au lancement: {e}", "ERROR")
            return False

    def show_menu(self):
        """Affiche le menu principal"""
        print("\n")
        print("=" * 60)
        print("  🎮 KOF ULTIMATE - LAUNCHER AUTO-DIAGNOSTIC")
        print("=" * 60)
        print()
        print("Ce launcher vérifie automatiquement tous les fichiers")
        print("et corrige ce qui peut l'être avant de lancer le jeu.")
        print()

        # Vérifications automatiques
        mugen_ok = self.check_mugen_engine()
        ikemen_ok = self.check_ikemen_engine()

        # Vérifications supplémentaires
        self.check_and_fix_air_files()
        self.check_char_select_config()

        # Résumé
        print()
        print("=" * 60)
        print("📊 RÉSUMÉ DU DIAGNOSTIC")
        print("=" * 60)

        if self.fixes:
            self.log(f"\n🔧 Corrections appliquées: {len(self.fixes)}", "FIX")
            for fix in self.fixes:
                self.log(f"  • {fix}", "FIX")

        if self.warnings:
            self.log(f"\n⚠️  Avertissements: {len(self.warnings)}", "WARNING")
            for warning in self.warnings:
                self.log(f"  • {warning}", "WARNING")

        if self.errors:
            self.log(f"\n❌ Erreurs critiques: {len(self.errors)}", "ERROR")
            for error in self.errors:
                self.log(f"  • {error}", "ERROR")

        if not self.errors and not self.warnings:
            self.log("\n✓ Tout est OK! Tous les moteurs sont prêts.", "SUCCESS")

        # Menu de choix
        print()
        print("=" * 60)
        print("MOTEURS DISPONIBLES:")
        print("=" * 60)
        print()

        if mugen_ok:
            print("  [1] 🥊 M.U.G.E.N (Classique) ✓")
        else:
            print("  [1] 🥊 M.U.G.E.N (Classique) ❌ NON DISPONIBLE")

        if ikemen_ok:
            print("  [2] 🌐 Ikemen GO (Moderne + Netplay) ✓")
        else:
            print("  [2] 🌐 Ikemen GO (Moderne + Netplay) ⚠️  VÉRIFIÉ")

        print()
        print("  [3] 🔄 Re-diagnostiquer")
        print("  [0] ❌ Quitter")
        print()

        return mugen_ok, ikemen_ok

    def run(self):
        """Boucle principale"""
        while True:
            # Reset des listes
            self.errors = []
            self.warnings = []
            self.fixes = []

            mugen_ok, ikemen_ok = self.show_menu()

            try:
                choice = input("Votre choix: ").strip()
            except KeyboardInterrupt:
                print("\n\nAu revoir!")
                sys.exit(0)

            if choice == "1":
                if mugen_ok:
                    self.launch_mugen()
                    print("\n")
                    input("Appuyez sur Entrée pour revenir au menu...")
                else:
                    self.log("\n❌ M.U.G.E.N n'est pas disponible", "ERROR")
                    print()
                    input("Appuyez sur Entrée pour continuer...")

            elif choice == "2":
                self.launch_ikemen()
                print("\n")
                input("Appuyez sur Entrée pour revenir au menu...")

            elif choice == "3":
                self.log("\n🔄 Re-diagnostic en cours...", "INFO")
                time.sleep(1)
                continue

            elif choice == "0":
                print("\n👋 Au revoir!")
                break

            else:
                self.log("\n❌ Choix invalide", "ERROR")
                time.sleep(1)

if __name__ == "__main__":
    os.system("chcp 65001 > nul")  # UTF-8 pour Windows
    os.system("cls" if os.name == "nt" else "clear")

    launcher = SmartLauncher()
    launcher.run()
