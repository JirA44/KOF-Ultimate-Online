#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - CORRECTEUR D'ERREURS CRITIQUES AIR
Corrige les erreurs spécifiques trouvées dans mugen.log
"""

import re
from pathlib import Path
from datetime import datetime
import shutil

game_dir = Path(r"D:\KOF Ultimate Online Online Online")
chars_dir = game_dir / "chars"

class CriticalAirFixer:
    """Correcteur pour les erreurs critiques AIR"""

    def __init__(self):
        self.fixed_count = 0
        self.backup_dir = game_dir / "air_backups_critical" / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.errors_fixed = []

    def log(self, message, level='INFO'):
        """Log message"""
        symbols = {
            'INFO': 'ℹ️',
            'SUCCESS': '✅',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'FIX': '🔧'
        }
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {symbols.get(level, '•')} {message}")

    def backup_file(self, file_path):
        """Crée un backup"""
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = self.backup_dir / file_path.name
            shutil.copy2(file_path, backup_path)
            return True
        except Exception as e:
            self.log(f"Erreur backup: {e}", 'ERROR')
            return False

    def fix_literal_newlines(self, content):
        """Corrige les \\n littéraux"""
        # Remplacer les \n littéraux par de vrais retours à la ligne
        fixed = content.replace(r'\n', '\n')
        return fixed

    def fix_originalzero_air(self):
        """Corrige OriginalZero.air"""
        air_path = chars_dir / "Final-OriginalZero" / "OriginalZero.air"

        if not air_path.exists():
            self.log(f"Fichier introuvable: {air_path}", 'WARNING')
            return False

        self.log(f"Correction de {air_path.name}...", 'INFO')

        try:
            with open(air_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            original_content = content

            # FIX 1: Remplacer les \n littéraux
            if r'\n' in content:
                content = self.fix_literal_newlines(content)
                self.log("Correction des \\n littéraux", 'FIX')

            # FIX 2: Ligne 740 - Double Clsn2: 0
            # Chercher et corriger les doubles déclarations Clsn2: 0 consécutives
            content = re.sub(
                r'(Clsn2:\s*0\s*\n)(Clsn2:\s*0\s*\n)',
                r'\1',  # Garder seulement la première
                content
            )

            # FIX 3: Vérifier que chaque [Begin Action] est sur sa propre ligne
            # (déjà corrigé par fix_literal_newlines)

            if content != original_content:
                # Backup
                self.backup_file(air_path)

                # Sauvegarder
                with open(air_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                self.fixed_count += 1
                self.errors_fixed.append(f"OriginalZero.air: \\n littéraux et double Clsn2")
                self.log(f"✅ Corrigé: {air_path.name}", 'SUCCESS')
                return True
            else:
                self.log("Aucune modification nécessaire", 'INFO')
                return False

        except Exception as e:
            self.log(f"Erreur lors de la correction: {e}", 'ERROR')
            return False

    def fix_kain_air(self):
        """Corrige kain.air"""
        air_path = chars_dir / "_ArchiMurderer" / "kain.air"

        if not air_path.exists():
            self.log(f"Fichier introuvable: {air_path}", 'WARNING')
            return False

        self.log(f"Correction de {air_path.name}...", 'INFO')

        try:
            with open(air_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            original_lines = lines[:]

            # Ligne 142: Clsn2[1] sans déclaration Clsn2:
            # Trouver l'action 101
            action_101_idx = None
            for i, line in enumerate(lines):
                if re.match(r'^\s*\[Begin Action 101\]', line):
                    action_101_idx = i
                    break

            if action_101_idx is not None:
                # Vérifier si ligne 142 (index 141) a Clsn2[1]
                if action_101_idx + 1 < len(lines):
                    if re.match(r'^\s*Clsn2\[', lines[action_101_idx + 1]):
                        # Insérer une déclaration Clsn2: 1 AVANT Clsn2[1]
                        lines.insert(action_101_idx + 1, "Clsn2: 1\n")
                        self.log("Ajout de 'Clsn2: 1' avant Clsn2[1] dans Action 101", 'FIX')

            if lines != original_lines:
                # Backup
                self.backup_file(air_path)

                # Sauvegarder
                with open(air_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                self.fixed_count += 1
                self.errors_fixed.append(f"kain.air: Ajout déclaration Clsn2: 1")
                self.log(f"✅ Corrigé: {air_path.name}", 'SUCCESS')
                return True
            else:
                self.log("Aucune modification nécessaire", 'INFO')
                return False

        except Exception as e:
            self.log(f"Erreur lors de la correction: {e}", 'ERROR')
            return False

    def fix_all_critical_errors(self):
        """Corrige toutes les erreurs critiques"""
        print()
        print("=" * 70)
        print("  🔧 CORRECTEUR D'ERREURS CRITIQUES AIR")
        print("=" * 70)
        print()

        # Corriger OriginalZero.air
        self.log("🔍 Correction OriginalZero.air...")
        print()
        self.fix_originalzero_air()
        print()

        # Corriger kain.air
        self.log("🔍 Correction kain.air...")
        print()
        self.fix_kain_air()
        print()

        # Rapport final
        print()
        print("=" * 70)
        print("📊 RAPPORT FINAL")
        print("=" * 70)
        print(f"Fichiers corrigés:  {self.fixed_count}")
        print(f"Erreurs corrigées:  {len(self.errors_fixed)}")
        print()

        if self.errors_fixed:
            print("🔧 DÉTAILS DES CORRECTIONS:")
            for error in self.errors_fixed:
                print(f"  ✅ {error}")
            print()

        if self.fixed_count > 0:
            print(f"💾 Backups sauvegardés dans:")
            print(f"   {self.backup_dir}")
        else:
            print("⚠️  Aucune correction effectuée")

        print("=" * 70)
        print()

def main():
    """Main function"""
    print()
    print("=" * 70)
    print("  🔧 KOF ULTIMATE - CORRECTEUR D'ERREURS CRITIQUES")
    print("=" * 70)
    print()

    fixer = CriticalAirFixer()
    fixer.fix_all_critical_errors()

    print()
    try:
        input("Appuyez sur ENTRÉE pour fermer...")
    except EOFError:
        pass

if __name__ == '__main__':
    main()
