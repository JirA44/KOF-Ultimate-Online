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
        self.base_path = Path("D:/KOF Ultimate")
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

        exe_path = self.base_path / "KOF BLACK R.exe"
        data_path = self.base_path / "data"
        cfg_path = self.base_path / "data/mugen.cfg"

        all_ok = True

        if not exe_path.exists():
            self.log("  KOF BLACK R.exe: MANQUANT", "ERROR")
            self.errors.append("MUGEN executable missing")
            all_ok = False
        else:
            self.log("  KOF BLACK R.exe: OK", "SUCCESS")

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

        # Vérifier le dossier font
        if not font_path.exists():
            self.log("  font/ folder: MANQUANT", "ERROR")
            self.errors.append("Ikemen GO font folder missing")
            all_ok = False
        else:
            self.log("  font/ folder: OK", "SUCCESS")

            # Vérifier debug.def
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

    def launch_mugen(self):
        """Lance M.U.G.E.N"""
        self.log("\n🚀 Lancement M.U.G.E.N...", "INFO")

        exe_path = self.base_path / "KOF BLACK R.exe"

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
