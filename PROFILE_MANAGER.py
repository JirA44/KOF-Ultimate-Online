#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - GESTIONNAIRE DE PROFILS
Système de profils utilisateur avec personnalisation du fond animé
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

class ProfileManager:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.profiles_file = self.base_path / "profiles.json"
        self.system_def = self.base_path / "data" / "system.def"
        self.backgrounds = self.scan_available_backgrounds()

    def log(self, message, level="INFO"):
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "MENU": "🎨"}
        print(f"{icons.get(level, '')} {message}")

    def scan_available_backgrounds(self):
        """Scanne les fonds disponibles"""
        backgrounds = {
            "default": {
                "name": "KOF DM BLACK (Default)",
                "actions": [2, 6, 5, 7, 8, 9],  # Actions d'animation par défaut
                "description": "Fond par défaut du jeu"
            },
            "blue_fire": {
                "name": "Flammes Bleues",
                "actions": [2, 6, 5],
                "description": "Fond avec flammes bleues animées"
            },
            "red_energy": {
                "name": "Énergie Rouge",
                "actions": [7, 8, 9],
                "description": "Fond avec énergie rouge"
            },
            "minimal": {
                "name": "Minimaliste",
                "actions": [2],
                "description": "Fond simple et épuré"
            },
            "full_animated": {
                "name": "Ultra Animé",
                "actions": [2, 6, 5, 7, 8, 9, 10, 11],
                "description": "Maximum d'animations"
            }
        }
        return backgrounds

    def load_profiles(self):
        """Charge les profils depuis le fichier JSON"""
        if not self.profiles_file.exists():
            return {
                "active_profile": "default",
                "profiles": {
                    "default": {
                        "name": "Joueur 1",
                        "background": "default",
                        "music_volume": 100,
                        "created": datetime.now().isoformat()
                    }
                }
            }

        try:
            return json.loads(self.profiles_file.read_text(encoding='utf-8'))
        except:
            self.log("Erreur lecture profils, création nouveaux", "ERROR")
            return self.load_profiles()  # Retourne les valeurs par défaut

    def save_profiles(self, profiles_data):
        """Sauvegarde les profils"""
        self.profiles_file.write_text(
            json.dumps(profiles_data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

    def apply_background(self, bg_key):
        """Applique un fond animé en modifiant system.def"""
        if bg_key not in self.backgrounds:
            self.log(f"Fond '{bg_key}' inconnu", "ERROR")
            return False

        bg = self.backgrounds[bg_key]

        # Backup system.def
        backup = self.system_def.with_suffix('.def.backup_profile')
        if not backup.exists():
            shutil.copy2(self.system_def, backup)

        try:
            # Lire system.def
            content = self.system_def.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            new_lines = []

            in_titlebg = False
            bg_index = 0

            for line in lines:
                # Détecter la section TitleBGdef
                if '[TitleBGdef]' in line:
                    in_titlebg = True
                    new_lines.append(line)
                    new_lines.append('bgclearcolor = 0,0,0')
                    new_lines.append('')

                    # Ajouter tous les layers du fond choisi
                    for i, action in enumerate(bg['actions']):
                        new_lines.append(f'[TitleBG {i}]')
                        new_lines.append('type = anim')
                        new_lines.append(f'actionno = {action}')
                        new_lines.append(f'layerno = {i}')

                        if i == 0:
                            new_lines.append('start = 320,240')
                        else:
                            new_lines.append(f'start = 0,{-80 + i * 20}')

                        new_lines.append('mask = 1')
                        new_lines.append('trans = add')
                        new_lines.append('')

                    bg_index = len(bg['actions'])
                    continue

                # Ignorer les anciennes définitions de TitleBG
                if in_titlebg and line.strip().startswith('[TitleBG'):
                    # Passer toutes les lignes jusqu'à la prochaine section
                    continue

                # Sortir du mode TitleBG si on rencontre une nouvelle section
                if in_titlebg and line.strip().startswith('[') and 'TitleBG' not in line:
                    in_titlebg = False

                if not in_titlebg or not line.strip().startswith('type'):
                    if not (in_titlebg and any(x in line for x in ['actionno', 'layerno', 'start', 'mask', 'trans'])):
                        new_lines.append(line)

            # Écrire le nouveau system.def
            self.system_def.write_text('\n'.join(new_lines), encoding='utf-8')
            self.log(f"✅ Fond '{bg['name']}' appliqué", "SUCCESS")
            return True

        except Exception as e:
            self.log(f"Erreur application fond: {e}", "ERROR")
            return False

    def create_profile(self, name, background="default"):
        """Crée un nouveau profil"""
        profiles_data = self.load_profiles()

        profile_id = f"profile_{len(profiles_data['profiles']) + 1}"

        profiles_data['profiles'][profile_id] = {
            "name": name,
            "background": background,
            "music_volume": 100,
            "created": datetime.now().isoformat()
        }

        self.save_profiles(profiles_data)
        self.log(f"✅ Profil '{name}' créé", "SUCCESS")
        return profile_id

    def switch_profile(self, profile_id):
        """Change le profil actif"""
        profiles_data = self.load_profiles()

        if profile_id not in profiles_data['profiles']:
            self.log(f"Profil '{profile_id}' introuvable", "ERROR")
            return False

        profile = profiles_data['profiles'][profile_id]
        profiles_data['active_profile'] = profile_id
        self.save_profiles(profiles_data)

        # Appliquer le fond du profil
        self.apply_background(profile['background'])

        self.log(f"✅ Profil '{profile['name']}' activé", "SUCCESS")
        return True

    def interactive_menu(self):
        """Menu interactif pour gérer les profils"""
        print("\n" + "="*70)
        print("  🎨 KOF ULTIMATE - GESTIONNAIRE DE PROFILS")
        print("="*70 + "\n")

        while True:
            profiles_data = self.load_profiles()
            active_profile_id = profiles_data['active_profile']
            active_profile = profiles_data['profiles'].get(active_profile_id, {})

            print(f"\n📋 Profil actif: {active_profile.get('name', 'Aucun')}")
            print(f"🎨 Fond: {self.backgrounds.get(active_profile.get('background', 'default'), {}).get('name', 'Default')}")
            print()
            print("1. Changer de profil")
            print("2. Créer un nouveau profil")
            print("3. Changer le fond animé du profil actuel")
            print("4. Lister tous les fonds disponibles")
            print("5. Quitter et lancer le jeu")
            print("0. Quitter")
            print()

            choice = input("Votre choix: ").strip()

            if choice == "0":
                break

            elif choice == "1":
                print("\n📋 PROFILS DISPONIBLES:")
                for i, (pid, prof) in enumerate(profiles_data['profiles'].items(), 1):
                    marker = "👉" if pid == active_profile_id else "  "
                    print(f"{marker} {i}. {prof['name']} (Fond: {prof['background']})")

                try:
                    idx = int(input("\nNuméro du profil: ").strip()) - 1
                    profile_id = list(profiles_data['profiles'].keys())[idx]
                    self.switch_profile(profile_id)
                except:
                    print("❌ Choix invalide")

            elif choice == "2":
                name = input("\nNom du nouveau profil: ").strip()
                if name:
                    self.create_profile(name)

            elif choice == "3":
                print("\n🎨 FONDS DISPONIBLES:")
                for i, (key, bg) in enumerate(self.backgrounds.items(), 1):
                    marker = "👉" if key == active_profile.get('background') else "  "
                    print(f"{marker} {i}. {bg['name']}")
                    print(f"     {bg['description']}")

                try:
                    idx = int(input("\nNuméro du fond: ").strip()) - 1
                    bg_key = list(self.backgrounds.keys())[idx]

                    # Mettre à jour le profil
                    profiles_data['profiles'][active_profile_id]['background'] = bg_key
                    self.save_profiles(profiles_data)

                    # Appliquer le fond
                    self.apply_background(bg_key)
                except:
                    print("❌ Choix invalide")

            elif choice == "4":
                print("\n🎨 TOUS LES FONDS DISPONIBLES:")
                for i, (key, bg) in enumerate(self.backgrounds.items(), 1):
                    print(f"\n{i}. {bg['name']}")
                    print(f"   {bg['description']}")
                    print(f"   Actions: {bg['actions']}")

                input("\nAppuyez sur Entrée pour continuer...")

            elif choice == "5":
                print("\n🎮 Lancement du jeu...")
                import subprocess
                subprocess.Popen([str(self.base_path / "KOF_Ultimate_Online.exe")], cwd=str(self.base_path))
                break

        print("\n✅ Au revoir !")

if __name__ == "__main__":
    manager = ProfileManager()
    manager.interactive_menu()
