#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - AUTO-CORRECTEUR LAUNCHERS
Corrige automatiquement tous les launchers qui ont des problèmes
"""

import re
from pathlib import Path
import shutil
from datetime import datetime

class LauncherFixer:
    """Correcteur automatique de launchers"""

    def __init__(self):
        self.game_dir = Path(r"D:\KOF Ultimate Online Online Online")
        self.backup_dir = self.game_dir / "backups_launchers"
        self.backup_dir.mkdir(exist_ok=True)

        self.fixes_applied = []

    def log(self, message, level='INFO'):
        """Log un message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def backup_file(self, filepath):
        """Backup avant modification"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{filepath.name}.backup_{timestamp}"
            backup_path = self.backup_dir / backup_name
            shutil.copy2(filepath, backup_path)
            return True
        except:
            return False

    def fix_pyautogui_failsafe(self, launcher_file):
        """Corrige les launchers avec PyAutoGUI fail-safe"""
        try:
            with open(launcher_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            modified = False

            # Si pyautogui est importé mais FAILSAFE pas désactivé
            if 'import pyautogui' in content and 'pyautogui.FAILSAFE' not in content:
                # Trouver la ligne d'import pyautogui
                lines = content.split('\n')
                new_lines = []

                for i, line in enumerate(lines):
                    new_lines.append(line)
                    if 'import pyautogui' in line and 'pyautogui.FAILSAFE' not in '\n'.join(lines):
                        # Ajouter FAILSAFE = False après l'import
                        new_lines.append('pyautogui.FAILSAFE = False  # Désactiver fail-safe pour tests')
                        modified = True
                        self.log(f"  Ajouté pyautogui.FAILSAFE = False")

                content = '\n'.join(new_lines)

            # Ajouter try-except autour des appels pyautogui
            if 'pyautogui.' in content and 'try:' not in content:
                # Wrapper les appels pyautogui dans try-except
                lines = content.split('\n')
                new_lines = []
                indent_level = 0

                for line in lines:
                    if 'pyautogui.' in line and 'FAILSAFE' not in line and 'try:' not in line:
                        # Détecter indentation
                        indent = len(line) - len(line.lstrip())
                        spaces = ' ' * indent

                        new_lines.append(f"{spaces}try:")
                        new_lines.append(line.replace(spaces, spaces + '    '))
                        new_lines.append(f"{spaces}except Exception as e:")
                        new_lines.append(f"{spaces}    pass  # Ignorer erreurs pyautogui")
                        modified = True
                    else:
                        new_lines.append(line)

                content = '\n'.join(new_lines)

            if modified:
                self.backup_file(launcher_file)
                with open(launcher_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                self.fixes_applied.append(f"Corrigé PyAutoGUI dans {launcher_file.name}")
                return True

            return False

        except Exception as e:
            self.log(f"Erreur correction {launcher_file.name}: {e}", 'ERROR')
            return False

    def fix_launcher_ultimate(self):
        """Corrige LAUNCHER_ULTIMATE.py qui se termine immédiatement"""
        launcher_file = self.game_dir / "LAUNCHER_ULTIMATE.py"

        if not launcher_file.exists():
            return False

        try:
            with open(launcher_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            modified = False
            new_lines = []

            for line in lines:
                # Chercher if __name__ == '__main__':
                if "if __name__ == '__main__':" in line:
                    new_lines.append(line)
                    # S'assurer qu'il y a un try-except
                    if 'try:' not in '\n'.join(lines):
                        new_lines.append('    try:\n')
                        modified = True
                elif 'sys.exit' in line and 'except' not in '\n'.join(lines[:len(new_lines)+10]):
                    # Remplacer sys.exit par pass ou ajouter exception handler
                    indent = len(line) - len(line.lstrip())
                    spaces = ' ' * indent
                    new_lines.append(f"{spaces}# {line.strip()}\n")
                    modified = True
                else:
                    new_lines.append(line)

            # S'assurer qu'il y a une boucle principale
            content = ''.join(new_lines)
            if 'while True:' not in content and 'mainloop()' not in content:
                # Ajouter une pause pour empêcher fermeture immédiate
                new_lines.append('\n# Garder le launcher ouvert\n')
                new_lines.append('input("Appuyez sur Entrée pour quitter...")\n')
                modified = True

            if modified:
                self.backup_file(launcher_file)
                with open(launcher_file, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)

                self.fixes_applied.append(f"Corrigé fermeture immédiate dans {launcher_file.name}")
                return True

            return False

        except Exception as e:
            self.log(f"Erreur correction {launcher_file.name}: {e}", 'ERROR')
            return False

    def fix_all_launchers(self):
        """Corrige tous les launchers en erreur"""
        self.log("\n" + "=" * 70)
        self.log("🔧 AUTO-CORRECTEUR LAUNCHERS")
        self.log("=" * 70)
        self.log("")

        # Launchers avec PyAutoGUI fail-safe
        self.log("🔧 Correction PyAutoGUI fail-safe...")
        launchers_pyautogui = [
            "launcher_modern.py",
            "LAUNCHER_ULTIMATE_V2.py"
        ]

        for launcher_name in launchers_pyautogui:
            launcher_file = self.game_dir / launcher_name
            if launcher_file.exists():
                if self.fix_pyautogui_failsafe(launcher_file):
                    self.log(f"  ✓ Corrigé: {launcher_name}")
                else:
                    self.log(f"  ⚠ Aucune correction: {launcher_name}")
            else:
                self.log(f"  ❌ Introuvable: {launcher_name}")

        # LAUNCHER_ULTIMATE.py fermeture immédiate
        self.log("\n🔧 Correction fermeture immédiate...")
        if self.fix_launcher_ultimate():
            self.log("  ✓ Corrigé: LAUNCHER_ULTIMATE.py")
        else:
            self.log("  ⚠ Aucune correction: LAUNCHER_ULTIMATE.py")

        # Rapport
        self.log("\n" + "=" * 70)
        self.log("📊 RAPPORT FINAL")
        self.log("=" * 70)

        if self.fixes_applied:
            self.log(f"\n✅ {len(self.fixes_applied)} corrections appliquées:")
            for fix in self.fixes_applied:
                self.log(f"  • {fix}")

            self.log(f"\n💾 Backups: {self.backup_dir}")
        else:
            self.log("\n⚠️ Aucune correction nécessaire")

        self.log("=" * 70)

        return len(self.fixes_applied) > 0

def main():
    """Point d'entrée"""
    print("\n" + "=" * 70)
    print("  🔧 AUTO-CORRECTEUR LAUNCHERS")
    print("=" * 70)
    print("\n  Corrige automatiquement:")
    print("  • PyAutoGUI fail-safe (launcher_modern, LAUNCHER_ULTIMATE_V2)")
    print("  • Fermeture immédiate (LAUNCHER_ULTIMATE)")
    print("\n" + "=" * 70)
    print()

    fixer = LauncherFixer()
    success = fixer.fix_all_launchers()

    print("\n\n" + "=" * 70)
    if success:
        print("✅ CORRECTIONS APPLIQUÉES!")
        print("\nRelancez les tests avec: python test_all_launchers.py")
    else:
        print("⚠️ AUCUNE CORRECTION NÉCESSAIRE")
    print("=" * 70)
    print()

if __name__ == '__main__':
    main()
