#!/usr/bin/env python3
"""
Script de nettoyage des launchers KOF Ultimate Online
Organise et archive les launchers redondants
"""

import os
import shutil
from pathlib import Path

class LauncherCleanup:
    def __init__(self):
        self.base_path = Path("D:/KOF Ultimate Online")
        self.archive_path = self.base_path / "launchers_archive"
        self.ai_tools_path = self.base_path / "ai_tools"
        self.dev_tools_path = self.base_path / "dev_tools"

        # Launchers à GARDER à la racine
        self.keep_at_root = {
            "GAME_LAUNCHER_ULTIMATE_V2.html",
            "LAUNCHER_DASHBOARD.py",
            "launcher_auto_diagnostic.py",
            "LAUNCH_WITH_MODE_SELECT.bat",
        }

        # Launchers pour AI tools
        self.move_to_ai_tools = {
            "launcher_ai_navigator.py",
            "launch_with_ai.bat",
            "launch_virtual_players_auto.py",
        }

        # Launchers pour dev tools
        self.move_to_dev_tools = {
            "test_all_launchers.py",
            "TEST_ALL_LAUNCHERS_AUTODIAG.py",
            "INTERACTIVE_LAUNCHER_TESTER.py",
            "LAUNCHER_ERROR_TESTER.py",
            "FIX_ALL_LAUNCHERS.py",
        }

        self.stats = {
            "kept": 0,
            "archived": 0,
            "moved_ai": 0,
            "moved_dev": 0,
            "created": 0,
        }

    def log(self, message, level="INFO"):
        """Affiche un message avec style"""
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "MOVE": "📦",
            "KEEP": "📌",
            "CREATE": "✨",
        }
        icon = icons.get(level, "")
        print(f"{icon} {message}")

    def create_directories(self):
        """Crée les dossiers nécessaires"""
        self.log("Création des dossiers...", "INFO")

        dirs_to_create = [
            self.archive_path,
            self.ai_tools_path,
            self.dev_tools_path,
        ]

        for directory in dirs_to_create:
            if not directory.exists():
                directory.mkdir(parents=True)
                self.log(f"Dossier créé: {directory.name}", "CREATE")
                self.stats["created"] += 1
            else:
                self.log(f"Dossier existe: {directory.name}", "INFO")

    def find_all_launchers(self):
        """Trouve tous les launchers"""
        self.log("\nRecherche des launchers...", "INFO")

        patterns = [
            "*launch*.bat",
            "*launch*.py",
            "*LAUNCH*.bat",
            "*LAUNCHER*.py",
            "*LAUNCHER*.html",
            "*launcher*.py",
        ]

        launchers = set()
        for pattern in patterns:
            for file in self.base_path.glob(pattern):
                if file.is_file() and file.parent == self.base_path:
                    launchers.add(file.name)

        self.log(f"Trouvé {len(launchers)} launchers", "SUCCESS")
        return sorted(launchers)

    def move_file(self, filename, destination, category):
        """Déplace un fichier vers une destination"""
        src = self.base_path / filename
        dst = destination / filename

        if src.exists():
            try:
                if dst.exists():
                    self.log(f"  {filename} existe déjà dans {destination.name}, skip", "WARNING")
                    return False

                shutil.move(str(src), str(dst))
                self.log(f"  {filename} → {destination.name}", "MOVE")
                self.stats[category] += 1
                return True
            except Exception as e:
                self.log(f"  Erreur lors du déplacement de {filename}: {e}", "ERROR")
                return False
        return False

    def organize_launchers(self):
        """Organise tous les launchers"""
        self.log("\nOrganisation des launchers...", "INFO")

        all_launchers = self.find_all_launchers()

        # Traiter chaque launcher
        for launcher in all_launchers:
            # À garder à la racine
            if launcher in self.keep_at_root:
                self.log(f"  {launcher} - CONSERVÉ", "KEEP")
                self.stats["kept"] += 1

            # Déplacer vers ai_tools
            elif launcher in self.move_to_ai_tools:
                self.move_file(launcher, self.ai_tools_path, "moved_ai")

            # Déplacer vers dev_tools
            elif launcher in self.move_to_dev_tools:
                self.move_file(launcher, self.dev_tools_path, "moved_dev")

            # Archiver le reste
            else:
                self.move_file(launcher, self.archive_path, "archived")

    def create_simple_launcher(self):
        """Crée le launcher batch simple"""
        self.log("\nCréation de LAUNCH_GAME.bat...", "INFO")

        launch_game_bat = self.base_path / "LAUNCH_GAME.bat"

        content = """@echo off
title KOF Ultimate Online - Quick Launch
cd /d "%~dp0"

echo.
echo ========================================
echo   KOF Ultimate Online
echo   Quick Launch
echo ========================================
echo.

REM Arrêter les scripts IA externes
taskkill /F /IM python.exe /T >nul 2>&1

echo Lancement du jeu...
start "" "KOF_Ultimate_Online.exe"

echo.
echo Jeu lance!
timeout /t 2 >nul
exit
"""

        try:
            with open(launch_game_bat, 'w', encoding='utf-8') as f:
                f.write(content)
            self.log("LAUNCH_GAME.bat créé", "CREATE")
            self.stats["created"] += 1
            self.stats["kept"] += 1
        except Exception as e:
            self.log(f"Erreur lors de la création de LAUNCH_GAME.bat: {e}", "ERROR")

    def rename_main_launcher(self):
        """Renomme le launcher HTML principal"""
        self.log("\nRenommage du launcher principal...", "INFO")

        old_name = self.base_path / "GAME_LAUNCHER_ULTIMATE_V2.html"
        new_name = self.base_path / "LAUNCHER_ULTIMATE.html"

        if old_name.exists() and not new_name.exists():
            try:
                shutil.move(str(old_name), str(new_name))
                self.log("GAME_LAUNCHER_ULTIMATE_V2.html → LAUNCHER_ULTIMATE.html", "SUCCESS")
                # Retirer de keep_at_root et ajouter le nouveau nom
                if "GAME_LAUNCHER_ULTIMATE_V2.html" in self.keep_at_root:
                    self.keep_at_root.remove("GAME_LAUNCHER_ULTIMATE_V2.html")
                    self.keep_at_root.add("LAUNCHER_ULTIMATE.html")
            except Exception as e:
                self.log(f"Erreur lors du renommage: {e}", "ERROR")
        elif new_name.exists():
            self.log("LAUNCHER_ULTIMATE.html existe déjà", "INFO")
        else:
            self.log("GAME_LAUNCHER_ULTIMATE_V2.html non trouvé", "WARNING")

    def create_readme(self):
        """Crée le README des launchers"""
        self.log("\nCréation de README_LAUNCHERS.md...", "INFO")

        readme_path = self.base_path / "README_LAUNCHERS.md"

        content = """# 🎮 Guide des Launchers - KOF Ultimate Online

## 🚀 Launchers Principaux

### Pour les nouveaux joueurs
**`LAUNCHER_ULTIMATE.html`** - Interface web magnifique
- Double-cliquez pour ouvrir dans le navigateur
- Design moderne et intuitif
- Stats, personnages, modes de jeu

### Pour l'usage quotidien
**`LAUNCHER_DASHBOARD.py`** - Interface graphique complète
- Lance avec: `python LAUNCHER_DASHBOARD.py`
- Accès à toutes les fonctionnalités
- Dashboard, tests, diagnostics

### En cas de problème
**`launcher_auto_diagnostic.py`** - Diagnostic automatique
- Lance avec: `python launcher_auto_diagnostic.py`
- Détecte et répare automatiquement
- Vérifie tous les fichiers

### Lancement rapide
**`LAUNCH_GAME.bat`** - Lance directement le jeu
- Double-cliquez pour lancer immédiatement
- Pas de menu, direct vers le jeu

### Sélection de mode
**`LAUNCH_WITH_MODE_SELECT.bat`** - Menu de sélection
- Choisir entre Solo / Versus / Netplay
- Menu texte simple

---

## 📁 Organisation

- `/launchers_archive/` - Anciens launchers archivés
- `/ai_tools/` - Outils pour l'IA
- `/dev_tools/` - Outils de développement

---

## 🆘 Support

Problème technique ? Lance `launcher_auto_diagnostic.py` !
"""

        try:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.log("README_LAUNCHERS.md créé", "CREATE")
            self.stats["created"] += 1
        except Exception as e:
            self.log(f"Erreur lors de la création du README: {e}", "ERROR")

    def show_summary(self):
        """Affiche le résumé"""
        self.log("\n" + "="*60, "INFO")
        self.log("📊 RÉSUMÉ DU NETTOYAGE", "SUCCESS")
        self.log("="*60, "INFO")

        print(f"""
  📌 Launchers conservés à la racine:  {self.stats['kept']}
  📦 Launchers archivés:                {self.stats['archived']}
  🤖 Déplacés vers ai_tools:            {self.stats['moved_ai']}
  🔧 Déplacés vers dev_tools:           {self.stats['moved_dev']}
  ✨ Fichiers créés:                    {self.stats['created']}
        """)

        self.log("="*60, "INFO")
        self.log("✅ Nettoyage terminé avec succès!", "SUCCESS")
        self.log("\nLaunchers finaux à la racine:", "INFO")
        for launcher in sorted(self.keep_at_root):
            if (self.base_path / launcher).exists() or launcher == "LAUNCHER_ULTIMATE.html":
                self.log(f"  • {launcher}", "KEEP")

    def run(self, auto_confirm=False):
        """Exécute le nettoyage complet"""
        print("\n" + "="*60)
        print("  🧹 NETTOYAGE DES LAUNCHERS KOF ULTIMATE ONLINE")
        print("="*60 + "\n")

        # Demander confirmation
        print("Ce script va:")
        print("  1. Créer les dossiers d'organisation")
        print("  2. Déplacer 45+ launchers redondants dans /launchers_archive/")
        print("  3. Organiser les scripts IA et dev")
        print("  4. Garder seulement 5 launchers principaux")
        print("  5. Créer les fichiers manquants")
        print()

        if not auto_confirm:
            response = input("Continuer ? (oui/non): ").strip().lower()
            if response not in ['oui', 'o', 'yes', 'y']:
                self.log("\nAnnulé par l'utilisateur", "WARNING")
                return
        else:
            print("✅ Mode automatique activé\n")

        print()

        # Exécuter les étapes
        self.create_directories()
        self.rename_main_launcher()
        self.organize_launchers()
        self.create_simple_launcher()
        self.create_readme()
        self.show_summary()

        print("\n✨ Vous pouvez maintenant utiliser les 5 launchers principaux!")
        print("📖 Consultez README_LAUNCHERS.md pour plus d'infos")
        print()

if __name__ == "__main__":
    import sys
    os.system("chcp 65001 > nul 2>&1")

    cleanup = LauncherCleanup()

    # Mode automatique si --yes ou -y est passé
    auto_confirm = '--yes' in sys.argv or '-y' in sys.argv
    cleanup.run(auto_confirm=auto_confirm)

    if not auto_confirm:
        input("\nAppuyez sur Entrée pour quitter...")
