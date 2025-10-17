"""
KOF Ultimate - Système de diagnostic automatique complet
Vérifie tous les aspects du jeu avant lancement
"""
import os
import re
from pathlib import Path

class KOFDiagnostic:
    def __init__(self, base_dir=r"D:\KOF Ultimate Online"):
        self.base_dir = Path(base_dir)
        self.errors = []
        self.warnings = []
        self.success = []

    def log_error(self, msg):
        self.errors.append(f"❌ ERREUR: {msg}")

    def log_warning(self, msg):
        self.warnings.append(f"⚠️  WARNING: {msg}")

    def log_success(self, msg):
        self.success.append(f"✅ OK: {msg}")

    def check_file_exists(self, filepath, description):
        """Vérifie qu'un fichier existe"""
        full_path = self.base_dir / filepath
        if full_path.exists():
            self.log_success(f"{description} existe: {filepath}")
            return True
        else:
            self.log_error(f"{description} MANQUANT: {filepath}")
            return False

    def check_config_value(self, file_path, section, key, description):
        """Vérifie une valeur dans un fichier de configuration"""
        full_path = self.base_dir / file_path
        if not full_path.exists():
            self.log_error(f"Fichier config manquant: {file_path}")
            return None

        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Trouver la section
            section_pattern = rf'\[{re.escape(section)}\]'
            section_match = re.search(section_pattern, content, re.IGNORECASE)

            if not section_match:
                self.log_error(f"Section [{section}] manquante dans {file_path}")
                return None

            # Chercher la clé après la section
            section_start = section_match.end()
            next_section = re.search(r'\n\[', content[section_start:])
            section_end = section_start + next_section.start() if next_section else len(content)
            section_content = content[section_start:section_end]

            # Chercher la clé
            key_pattern = rf'{re.escape(key)}\s*=\s*(.+?)(?:\n|$)'
            key_match = re.search(key_pattern, section_content, re.IGNORECASE)

            if key_match:
                value = key_match.group(1).strip()
                self.log_success(f"{description}: {key} = {value}")
                return value
            else:
                self.log_warning(f"{description}: {key} non trouvé dans [{section}]")
                return None

        except Exception as e:
            self.log_error(f"Erreur lecture {file_path}: {e}")
            return None

    def check_system_def(self):
        """Vérifie la configuration system.def"""
        print("\n" + "="*70)
        print("📋 VÉRIFICATION SYSTEM.DEF")
        print("="*70)

        system_def = "data/system.def"

        # Vérifier l'existence
        if not self.check_file_exists(system_def, "system.def"):
            return False

        # Vérifier les sprites du titre
        spr_file = self.check_config_value(system_def, "TitleBGdef", "spr", "Fichier sprites titre")
        if spr_file:
            self.check_file_exists(spr_file, "Fichier sprites titre")

        # Vérifier la musique du titre
        bgm_file = self.check_config_value(system_def, "Music", "title.bgm", "Musique du titre")
        if bgm_file:
            self.check_file_exists(bgm_file, "Musique du titre")

        # Vérifier les animations de fond
        self.check_config_value(system_def, "TitleBG 0", "type", "Type d'animation fond")
        self.check_config_value(system_def, "TitleBG 0", "spriteno", "Numéro de sprite fond")

        return True

    def check_menu_configuration(self):
        """Vérifie la configuration des menus"""
        print("\n" + "="*70)
        print("🎮 VÉRIFICATION CONFIGURATION MENUS")
        print("="*70)

        system_def = "data/system.def"

        # Vérifier les items de menu
        menu_items = []
        for i in range(1, 20):
            item = self.check_config_value(system_def, "Title Info", f"menu.itemname.{i}", f"Menu item {i}")
            if item:
                menu_items.append(item)

        if len(menu_items) > 0:
            self.log_success(f"Nombre d'items de menu trouvés: {len(menu_items)}")
            print("\n   Items de menu détectés:")
            for idx, item in enumerate(menu_items, 1):
                print(f"   {idx}. {item}")

            # Vérifier si "Versus" ou "VS Mode" existe
            vs_mode_found = any('versus' in item.lower() or 'vs' in item.lower() for item in menu_items)
            if vs_mode_found:
                self.log_success("Mode Versus/Multijoueur trouvé dans le menu")
            else:
                self.log_error("Mode Versus/Multijoueur ABSENT du menu!")
                self.log_warning("Le jeu pourrait ne pas avoir de mode 2 joueurs accessible")
        else:
            self.log_error("Aucun item de menu trouvé dans system.def!")

        return len(menu_items) > 0

    def check_select_def(self):
        """Vérifie le fichier select.def"""
        print("\n" + "="*70)
        print("👥 VÉRIFICATION SELECT.DEF")
        print("="*70)

        select_def = "data/select.def"

        if not self.check_file_exists(select_def, "select.def"):
            return False

        # Compter les personnages
        try:
            with open(self.base_dir / select_def, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Trouver la section [Characters]
            chars_match = re.search(r'\[Characters\](.*?)(?:\[|$)', content, re.DOTALL | re.IGNORECASE)
            if chars_match:
                chars_section = chars_match.group(1)
                # Compter les lignes non vides et non commentaires
                char_lines = [line.strip() for line in chars_section.split('\n')
                             if line.strip() and not line.strip().startswith(';')]

                char_count = len(char_lines)
                if char_count > 0:
                    self.log_success(f"Nombre de personnages dans select.def: {char_count}")
                    if char_count < 10:
                        self.log_warning(f"Seulement {char_count} personnages trouvés (peu)")
                else:
                    self.log_error("Aucun personnage trouvé dans select.def!")
            else:
                self.log_error("Section [Characters] non trouvée dans select.def")

        except Exception as e:
            self.log_error(f"Erreur lecture select.def: {e}")
            return False

        return True

    def check_joystick_config(self):
        """Vérifie la configuration des manettes"""
        print("\n" + "="*70)
        print("🎮 VÉRIFICATION CONFIGURATION MANETTES")
        print("="*70)

        mugen_cfg = "data/mugen.cfg"

        if not self.check_file_exists(mugen_cfg, "mugen.cfg"):
            return False

        # Vérifier P1
        p1_type = self.check_config_value(mugen_cfg, "Input", "P1.Joystick.type", "Type joystick P1")
        p1_joystick = self.check_config_value(mugen_cfg, "Input", "p1.joystick", "Activation joystick P1")

        # Vérifier P2
        p2_type = self.check_config_value(mugen_cfg, "Input", "P2.Joystick.type", "Type joystick P2")
        p2_joystick = self.check_config_value(mugen_cfg, "Input", "p2.joystick", "Activation joystick P2")

        # Vérifier les sections [P1 Joystick] et [P2 Joystick]
        try:
            with open(self.base_dir / mugen_cfg, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            if '[P1 Joystick]' in content:
                self.log_success("Section [P1 Joystick] trouvée")
            else:
                self.log_warning("Section [P1 Joystick] manquante")

            if '[P2 Joystick]' in content:
                self.log_success("Section [P2 Joystick] trouvée")
            else:
                self.log_warning("Section [P2 Joystick] manquante")

        except Exception as e:
            self.log_error(f"Erreur vérification sections joystick: {e}")

        return True

    def check_sprites_and_sounds(self):
        """Vérifie les fichiers sprites et sons essentiels"""
        print("\n" + "="*70)
        print("🎨 VÉRIFICATION SPRITES ET SONS")
        print("="*70)

        # Vérifier dossiers principaux
        dirs_to_check = [
            ("sprites", "Dossier sprites"),
            ("sound", "Dossier sons"),
            ("stages", "Dossier stages"),
            ("chars", "Dossier personnages")
        ]

        for dir_path, desc in dirs_to_check:
            full_path = self.base_dir / dir_path
            if full_path.exists() and full_path.is_dir():
                # Compter les fichiers
                try:
                    file_count = len(list(full_path.iterdir()))
                    self.log_success(f"{desc}: {file_count} fichiers/dossiers")
                except Exception as e:
                    self.log_warning(f"{desc} existe mais erreur de lecture: {e}")
            else:
                self.log_error(f"{desc} MANQUANT: {dir_path}")

        return True

    def check_chars_directory(self):
        """Vérifie le contenu du dossier chars"""
        print("\n" + "="*70)
        print("👤 VÉRIFICATION DOSSIER PERSONNAGES")
        print("="*70)

        chars_dir = self.base_dir / "chars"

        if not chars_dir.exists():
            self.log_error("Dossier chars/ manquant!")
            return False

        try:
            # Lister tous les sous-dossiers
            char_folders = [d for d in chars_dir.iterdir() if d.is_dir()]
            self.log_success(f"Nombre de dossiers personnages: {len(char_folders)}")

            # Vérifier quelques personnages au hasard
            valid_chars = 0
            for char_dir in char_folders[:10]:  # Vérifier les 10 premiers
                def_files = list(char_dir.glob("*.def"))
                if def_files:
                    valid_chars += 1

            if valid_chars > 0:
                self.log_success(f"Personnages valides vérifiés: {valid_chars}/10")
            else:
                self.log_warning("Aucun personnage valide trouvé dans les 10 premiers")

        except Exception as e:
            self.log_error(f"Erreur vérification dossier chars: {e}")
            return False

        return True

    def run_full_diagnostic(self):
        """Lance le diagnostic complet"""
        print("\n" + "="*70)
        print("🔍 KOF ULTIMATE - DIAGNOSTIC AUTOMATIQUE COMPLET")
        print("="*70)
        print(f"Dossier de base: {self.base_dir}")

        # Exécuter toutes les vérifications
        self.check_system_def()
        self.check_menu_configuration()
        self.check_select_def()
        self.check_joystick_config()
        self.check_sprites_and_sounds()
        self.check_chars_directory()

        # Afficher le résumé
        print("\n" + "="*70)
        print("📊 RÉSUMÉ DU DIAGNOSTIC")
        print("="*70)

        print(f"\n✅ SUCCÈS: {len(self.success)}")
        for msg in self.success[:5]:  # Afficher les 5 premiers
            print(f"  {msg}")
        if len(self.success) > 5:
            print(f"  ... et {len(self.success) - 5} autres")

        print(f"\n⚠️  WARNINGS: {len(self.warnings)}")
        for msg in self.warnings:
            print(f"  {msg}")

        print(f"\n❌ ERREURS: {len(self.errors)}")
        for msg in self.errors:
            print(f"  {msg}")

        # Score global
        total_checks = len(self.success) + len(self.warnings) + len(self.errors)
        score = (len(self.success) / total_checks * 100) if total_checks > 0 else 0

        print("\n" + "="*70)
        print(f"🎯 SCORE GLOBAL: {score:.1f}% ({len(self.success)}/{total_checks} vérifications réussies)")
        print("="*70)

        if len(self.errors) == 0 and len(self.warnings) == 0:
            print("\n🎉 PARFAIT! Le jeu est prêt à être lancé!")
            return True
        elif len(self.errors) == 0:
            print("\n✅ Le jeu devrait fonctionner, mais avec quelques avertissements.")
            return True
        else:
            print("\n⚠️  ATTENTION: Des erreurs critiques ont été détectées!")
            print("   Le jeu pourrait ne pas fonctionner correctement.")
            return False

if __name__ == "__main__":
    diagnostic = KOFDiagnostic()
    result = diagnostic.run_full_diagnostic()

    print("\n" + "="*70)
    input("\nAppuyez sur Entrée pour quitter...")
