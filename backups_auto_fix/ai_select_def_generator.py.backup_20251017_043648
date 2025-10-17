"""
KOF Ultimate - Générateur Automatique de select.def
Génère un fichier select.def complet avec tous les personnages disponibles
"""

import os
from pathlib import Path

class SelectDefGenerator:
    """Génère automatiquement select.def avec tous les personnages"""

    def __init__(self, chars_path, output_path):
        self.chars_path = Path(chars_path)
        self.output_path = Path(output_path)
        self.characters = []

    def log(self, message, level="INFO"):
        """Log avec couleurs"""
        colors = {
            "INFO": "",
            "SUCCESS": "✓ ",
            "WARNING": "⚠️  ",
            "ERROR": "❌ "
        }
        prefix = colors.get(level, "")
        print(f"{prefix}{message}")

    def scan_characters(self):
        """Scanne tous les personnages disponibles"""
        self.log("\n🔍 Scan des personnages...", "INFO")

        if not self.chars_path.exists():
            self.log(f"Dossier chars introuvable: {self.chars_path}", "ERROR")
            return False

        # Lister tous les dossiers de personnages
        char_folders = [d for d in self.chars_path.iterdir() if d.is_dir()]

        # Filtrer les dossiers de backup et autres
        valid_chars = []
        for char_dir in char_folders:
            char_name = char_dir.name

            # Ignorer les dossiers de backup
            if "backup" in char_name.lower() or char_name.startswith("@"):
                continue

            # Vérifier qu'il y a au moins un fichier .def
            def_files = list(char_dir.glob("*.def"))
            if not def_files:
                self.log(f"  Ignoré (pas de .def): {char_name}", "WARNING")
                continue

            valid_chars.append(char_name)

        self.characters = sorted(valid_chars)
        self.log(f"✓ {len(self.characters)} personnages trouvés", "SUCCESS")

        return True

    def generate_select_def(self, mode="full"):
        """Génère le fichier select.def"""
        self.log("\n📝 Génération du select.def...", "INFO")

        if mode == "full":
            content = self._generate_full_roster()
        elif mode == "kof_teams":
            content = self._generate_kof_teams()
        else:
            content = self._generate_full_roster()

        # Sauvegarder
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(content)

            self.log(f"✓ select.def généré: {self.output_path}", "SUCCESS")
            self.log(f"  • {len(self.characters)} personnages ajoutés", "INFO")

            return True
        except Exception as e:
            self.log(f"Erreur lors de la sauvegarde: {e}", "ERROR")
            return False

    def _generate_full_roster(self):
        """Génère un roster complet (tous les personnages)"""
        lines = []

        # Header
        lines.append("; KOF ULTIMATE - select.def")
        lines.append("; Généré automatiquement avec TOUS les personnages")
        lines.append("; Total: {} personnages".format(len(self.characters)))
        lines.append("")

        lines.append("[Characters]")
        lines.append("")

        # Ajouter tous les personnages
        for char_name in self.characters:
            lines.append(char_name)

        lines.append("")

        # Extra stages
        lines.append("[ExtraStages]")
        lines.append("")

        # Options
        lines.append("[Options]")
        lines.append("arcade.maxmatches = 6,1,1,0,0,0,0,0,0,0")
        lines.append("team.maxmatches = 4,1,1,1,0,0,0,0,0,0")
        lines.append("")

        return "\n".join(lines)

    def _generate_kof_teams(self):
        """Génère un roster organisé par teams KOF"""
        lines = []

        # Header
        lines.append("; KOF ULTIMATE - select.def")
        lines.append("; Roster organisé par équipes")
        lines.append("; Total: {} personnages".format(len(self.characters)))
        lines.append("")

        lines.append("[Characters]")
        lines.append("")

        # Organiser par équipes (simple grouping par 3)
        lines.append("; === TEAMS ===")
        lines.append("")

        for i in range(0, len(self.characters), 3):
            team = self.characters[i:i+3]

            lines.append("; Team {}".format(i//3 + 1))
            for char_name in team:
                lines.append(char_name)
            lines.append("")

        # Extra stages
        lines.append("[ExtraStages]")
        lines.append("")

        # Options - Mode teams
        lines.append("[Options]")
        lines.append("arcade.maxmatches = 6,1,1,0,0,0,0,0,0,0")
        lines.append("team.maxmatches = 4,1,1,1,0,0,0,0,0,0")
        lines.append("team.single = 1")
        lines.append("")

        return "\n".join(lines)

    def backup_existing(self):
        """Sauvegarde l'ancien select.def"""
        if self.output_path.exists():
            backup_path = self.output_path.with_suffix('.def.backup')
            try:
                import shutil
                shutil.copy2(self.output_path, backup_path)
                self.log(f"✓ Backup créé: {backup_path}", "SUCCESS")
                return True
            except Exception as e:
                self.log(f"⚠️  Impossible de créer le backup: {e}", "WARNING")
                return False
        return True

    def run(self, mode="full"):
        """Lance la génération complète"""
        print("\n")
        print("=" * 60)
        print("🎮 GÉNÉRATEUR AUTOMATIQUE DE SELECT.DEF")
        print("=" * 60)
        print()

        # Étape 1: Scanner
        if not self.scan_characters():
            return False

        # Étape 2: Backup
        self.backup_existing()

        # Étape 3: Générer
        if not self.generate_select_def(mode):
            return False

        print()
        print("=" * 60)
        print("✓ SELECT.DEF GÉNÉRÉ AVEC SUCCÈS!")
        print("=" * 60)
        print()

        return True

if __name__ == "__main__":
    import sys

    print("\n")
    print("=" * 60)
    print("🎮 GÉNÉRATEUR DE SELECT.DEF - KOF ULTIMATE")
    print("=" * 60)
    print()
    print("Ce script va:")
    print("  1. Scanner tous les personnages disponibles")
    print("  2. Créer un backup de l'ancien select.def")
    print("  3. Générer un nouveau select.def complet")
    print()

    # Choix du mode
    print("Choisissez le mode:")
    print("  [1] Roster complet (tous les personnages)")
    print("  [2] Roster par équipes (organisé en teams)")
    print()

    try:
        choice = input("Votre choix (1 ou 2): ").strip()
    except KeyboardInterrupt:
        print("\n\nAnnulé.")
        sys.exit(0)

    mode = "full" if choice == "1" else "kof_teams"

    # Générer pour Ikemen GO
    print("\n>>> Génération pour IKEMEN GO")
    generator_ikemen = SelectDefGenerator(
        chars_path="D:/KOF Ultimate/Ikemen_GO/chars",
        output_path="D:/KOF Ultimate/Ikemen_GO/data/select.def"
    )
    generator_ikemen.run(mode)

    # Optionnel: Générer aussi pour MUGEN
    print("\n>>> Génération pour M.U.G.E.N")
    generator_mugen = SelectDefGenerator(
        chars_path="D:/KOF Ultimate/chars",
        output_path="D:/KOF Ultimate/data/select.def"
    )
    generator_mugen.run(mode)

    print()
    input("Appuyez sur Entrée pour quitter...")
