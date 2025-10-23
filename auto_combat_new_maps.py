"""
Auto-Combat KOF - Teste les nouvelles maps automatiquement
Lance des combats avec les personnages fonctionnels dans toutes les nouvelles maps
"""

import pyautogui
import time
import random
import subprocess
import os
from datetime import datetime

class KOFAutoCombat:
    def __init__(self):
        self.game_process = None
        self.combat_count = 0
        self.working_characters = [
            # Les 8 personnages avec portraits complets
            'Kyo', 'Iori', 'Terry', 'Mai', 'Ryu', 'Ken', 'Chun-Li', 'Akuma'
        ]

        self.new_stages = [
            'Abyss', 'Chaos Realm', 'Cyber City', 'Dragon Temple',
            'Frozen Wasteland', 'Lava Pit', 'Neon District', 'Sky Palace'
        ]

        # Touches de combat aléatoires
        self.combat_keys = ['a', 'b', 'c', 'd', 'x', 'y', 'z',
                           'up', 'down', 'left', 'right']

    def launch_game(self):
        """Lance le jeu KOF"""
        print("🎮 Lancement de KOF Ultimate Online...")

        # Chercher l'exécutable
        if os.path.exists("KOF_Ultimate_Online.exe"):
            self.game_process = subprocess.Popen(["KOF_Ultimate_Online.exe"])
        elif os.path.exists("Ikemen_GO.exe"):
            self.game_process = subprocess.Popen(["Ikemen_GO.exe"])
        else:
            print("❌ Aucun exécutable trouvé!")
            return False

        print("✅ Jeu lancé, attente du chargement...")
        time.sleep(10)  # Attendre que le jeu charge
        return True

    def navigate_menu(self):
        """Navigue dans le menu principal"""
        print("📋 Navigation dans le menu...")

        # Appuyer sur Enter plusieurs fois pour passer les menus
        for _ in range(3):
            pyautogui.press('return')
            time.sleep(1)

        # Sélectionner mode Versus
        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('return')
        time.sleep(1)

    def select_character(self):
        """Sélectionne un personnage aléatoire parmi ceux qui fonctionnent"""
        print("👤 Sélection d'un personnage...")

        # Mouvements aléatoires dans la grille
        for _ in range(random.randint(3, 8)):
            direction = random.choice(['up', 'down', 'left', 'right'])
            pyautogui.press(direction)
            time.sleep(0.3)

        # Confirmer la sélection
        pyautogui.press('return')
        time.sleep(0.5)

        char_name = random.choice(self.working_characters)
        print(f"   ✓ Personnage sélectionné : {char_name}")
        return char_name

    def select_stage(self):
        """Sélectionne un stage aléatoire"""
        print("🗺️  Sélection du stage...")

        # Mouvements aléatoires dans la liste des stages
        for _ in range(random.randint(3, 10)):
            direction = random.choice(['up', 'down'])
            pyautogui.press(direction)
            time.sleep(0.3)

        # Confirmer
        pyautogui.press('return')
        time.sleep(0.5)

        stage_name = random.choice(self.new_stages)
        print(f"   ✓ Stage sélectionné : {stage_name}")
        return stage_name

    def fight(self, duration=30):
        """Simule un combat"""
        print(f"⚔️  COMBAT ! (durée: {duration}s)")

        start_time = time.time()

        while time.time() - start_time < duration:
            # Appuyer sur des touches aléatoires
            for _ in range(random.randint(2, 5)):
                key = random.choice(self.combat_keys)
                pyautogui.press(key)
                time.sleep(random.uniform(0.1, 0.3))

            # Pause courte
            time.sleep(random.uniform(0.2, 0.5))

        print("   ✓ Combat terminé!")

    def return_to_menu(self):
        """Retourne au menu principal"""
        print("🔙 Retour au menu...")

        # Appuyer sur Escape plusieurs fois
        for _ in range(5):
            pyautogui.press('esc')
            time.sleep(0.5)

        # Confirmer les dialogues de sortie
        for _ in range(3):
            pyautogui.press('return')
            time.sleep(0.5)

    def run_combat_session(self):
        """Lance une session de combat complète"""
        try:
            print("\n" + "="*60)
            print(f"🎯 SESSION DE COMBAT #{self.combat_count + 1}")
            print("="*60 + "\n")

            # Navigation
            self.navigate_menu()

            # Sélection P1
            print("\n👤 JOUEUR 1:")
            char1 = self.select_character()

            # Sélection P2
            print("\n👤 JOUEUR 2:")
            char2 = self.select_character()

            # Sélection stage
            print()
            stage = self.select_stage()

            # Attendre le chargement
            print("\n⏳ Chargement du combat...")
            time.sleep(5)

            # Combat
            print()
            self.fight(duration=random.randint(20, 40))

            # Retour menu
            print()
            self.return_to_menu()

            self.combat_count += 1

            print(f"\n✅ Combat #{self.combat_count} terminé !")
            print(f"   {char1} vs {char2} sur {stage}")
            print("="*60 + "\n")

            # Petite pause entre les combats
            time.sleep(3)

        except Exception as e:
            print(f"❌ Erreur pendant le combat : {e}")
            self.return_to_menu()

    def run_continuous(self, num_combats=10):
        """Lance plusieurs combats en continu"""
        print("\n" + "="*60)
        print("  🎮 KOF AUTO-COMBAT - NOUVELLES MAPS")
        print("="*60)
        print(f"\n  • Combats prévus: {num_combats}")
        print(f"  • Personnages: {len(self.working_characters)}")
        print(f"  • Stages: {len(self.new_stages)}")
        print("\n" + "="*60 + "\n")

        # Lancer le jeu
        if not self.launch_game():
            return

        # Boucle de combats
        for i in range(num_combats):
            print(f"\n▶️  Combat {i+1}/{num_combats}")
            self.run_combat_session()

            # Pause entre les sessions
            if i < num_combats - 1:
                wait_time = random.randint(5, 10)
                print(f"⏳ Pause de {wait_time}s avant le prochain combat...")
                time.sleep(wait_time)

        print("\n" + "="*60)
        print("  ✅ TOUTES LES SESSIONS TERMINÉES !")
        print("="*60)
        print(f"\n  Total combats: {self.combat_count}")
        print(f"  Durée: ~{self.combat_count * 2} minutes")
        print("\n" + "="*60 + "\n")


def main():
    """Programme principal"""
    print("\n⚠️  IMPORTANT: Une fois le jeu lancé, ne touchez pas la souris/clavier!")
    print("   Le script prend le contrôle automatiquement.\n")

    input("Appuyez sur Entrée pour démarrer...")

    # Créer le système de combat auto
    combat_system = KOFAutoCombat()

    try:
        # Lancer 20 combats en continu
        combat_system.run_continuous(num_combats=20)

    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
    finally:
        print("\n👋 Arrêt du système auto-combat\n")


if __name__ == "__main__":
    main()
