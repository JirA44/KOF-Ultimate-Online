#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - STANDARDISATION DES PORTRAITS
Redimensionne automatiquement tous les portraits à 32x32 pixels
"""

import os
import sys
from pathlib import Path
from PIL import Image
import shutil
from datetime import datetime

game_dir = Path(r"D:\KOF Ultimate Online")
chars_dir = game_dir / "chars"

class PortraitStandardizer:
    """Standardise les portraits de tous les personnages"""

    def __init__(self, target_size=(32, 32)):
        self.target_size = target_size
        self.processed = 0
        self.errors = []
        self.backup_dir = game_dir / "portraits_backup" / datetime.now().strftime("%Y%m%d_%H%M%S")

    def log(self, message, level='INFO'):
        """Log message"""
        symbols = {
            'INFO': 'ℹ️',
            'SUCCESS': '✅',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'PROCESS': '🔄'
        }
        print(f"{symbols.get(level, '•')} {message}")

    def find_portrait_files(self):
        """Trouve tous les fichiers portrait dans les dossiers chars"""
        portrait_files = []

        # Chercher fichiers PNG/BMP dans dossiers chars
        for char_dir in chars_dir.iterdir():
            if char_dir.is_dir():
                # Chercher portraits communs
                for pattern in ["portrait.png", "portrait.bmp", "9000_0.png", "9000_0.bmp"]:
                    matches = list(char_dir.glob(pattern))
                    portrait_files.extend(matches)

        return portrait_files

    def backup_portrait(self, portrait_path):
        """Crée un backup du portrait"""
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = self.backup_dir / f"{portrait_path.parent.name}_{portrait_path.name}"
            shutil.copy2(portrait_path, backup_path)
            return True
        except Exception as e:
            self.log(f"Erreur backup {portrait_path.name}: {e}", 'ERROR')
            return False

    def standardize_portrait(self, portrait_path):
        """Redimensionne un portrait à la taille cible"""
        try:
            # Ouvrir image
            img = Image.open(portrait_path)
            original_size = img.size

            # Si déjà à la bonne taille, ignorer
            if img.size == self.target_size:
                return False, "Already correct size"

            # Backup
            self.backup_portrait(portrait_path)

            # Redimensionner avec antialiasing
            img_resized = img.resize(self.target_size, Image.Resampling.LANCZOS)

            # Sauvegarder
            img_resized.save(portrait_path)

            self.processed += 1
            return True, f"{original_size} -> {self.target_size}"

        except Exception as e:
            error_msg = f"Erreur processing {portrait_path}: {e}"
            self.errors.append(error_msg)
            return False, str(e)

    def process_all_portraits(self):
        """Traite tous les portraits"""
        print()
        print("=" * 70)
        print("  🖼️  STANDARDISATION DES PORTRAITS")
        print("=" * 70)
        print(f"Taille cible: {self.target_size[0]}×{self.target_size[1]} pixels")
        print()

        # Trouver fichiers
        self.log("Recherche des portraits...")
        portrait_files = self.find_portrait_files()
        self.log(f"Trouvé {len(portrait_files)} portraits")
        print()

        # Traiter chaque portrait
        for portrait in portrait_files:
            char_name = portrait.parent.name
            changed, info = self.standardize_portrait(portrait)

            if changed:
                self.log(f"✓ {char_name}: {info}", 'PROCESS')

        print()
        print("=" * 70)
        print("📊 RAPPORT FINAL")
        print("=" * 70)
        print(f"Fichiers scannés:  {len(portrait_files)}")
        print(f"Fichiers modifiés: {self.processed}")
        print(f"Erreurs:           {len(self.errors)}")
        print()

        if self.errors:
            print("❌ ERREURS:")
            for error in self.errors[:10]:
                print(f"   • {error}")
            if len(self.errors) > 10:
                print(f"   ... et {len(self.errors) - 10} autres erreurs")
            print()

        if self.processed > 0:
            print(f"💾 Backups sauvegardés dans:")
            print(f"   {self.backup_dir}")

        print("=" * 70)
        print()

def main():
    """Main function"""
    print()
    print("=" * 70)
    print("  🖼️  KOF ULTIMATE - STANDARDISATION DES PORTRAITS")
    print("=" * 70)
    print()

    # Check PIL disponible
    try:
        from PIL import Image
    except ImportError:
        print("❌ ERREUR: Pillow (PIL) n'est pas installé")
        print("   Installer avec: pip install Pillow")
        print()
        try:
            input("Appuyez sur ENTRÉE pour fermer...")
        except EOFError:
            pass
        return

    standardizer = PortraitStandardizer(target_size=(32, 32))
    standardizer.process_all_portraits()

    print()
    try:
        input("Appuyez sur ENTRÉE pour fermer...")
    except EOFError:
        pass

if __name__ == '__main__':
    main()
