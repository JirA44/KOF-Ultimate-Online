#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST MANUEL GUIDÉ
Vous guide étape par étape, VOUS appuyez sur les touches
"""

import time
from datetime import datetime

class GuidedTest:
    def __init__(self):
        self.start_time = datetime.now()
        self.step = 0

    def next_step(self, instruction, expected_result):
        """Affiche une étape et attend validation"""
        self.step += 1
        print(f"\n{'='*70}")
        print(f"ÉTAPE {self.step}")
        print('='*70)
        print(f"\n📝 À FAIRE: {instruction}")
        print(f"✓ RÉSULTAT ATTENDU: {expected_result}\n")

        input("➡️  Appuyez sur ENTRÉE quand c'est fait... ")

        result = input("✅ Ça a fonctionné ? (o/n) : ").lower().strip()
        return result == 'o' or result == 'oui' or result == 'y' or result == 'yes'

    def run(self):
        print("\n" + "="*70)
        print("  🎮 TEST MANUEL GUIDÉ")
        print("  KOF Ultimate Online")
        print("="*70 + "\n")

        print("Ce test vous guide pas à pas.")
        print("VOUS appuyez sur les touches, pas le script.\n")

        input("Appuyez sur ENTRÉE pour commencer...")

        results = []

        # Test 1
        ok = self.next_step(
            "Lancez le jeu (double-clic sur KOF_Ultimate_Online.exe)",
            "Le jeu démarre et affiche l'écran titre"
        )
        results.append(("Lancement", ok))

        if not ok:
            print("\n❌ Impossible de continuer sans le jeu lancé")
            return

        # Test 2
        ok = self.next_step(
            "Appuyez sur ESPACE",
            "Le menu principal apparaît"
        )
        results.append(("Écran titre", ok))

        # Test 3
        ok = self.next_step(
            "Naviguez dans le menu avec HAUT/BAS (7 options)",
            "Le curseur se déplace entre: Arcade, Versus, Team Arcade, etc."
        )
        results.append(("Navigation menu", ok))

        # Test 4
        ok = self.next_step(
            "Allez sur 'Versus' et appuyez sur ENTRÉE",
            "L'écran de sélection de personnages s'affiche"
        )
        results.append(("Mode Versus", ok))

        # Test 5
        ok = self.next_step(
            "Naviguez dans la grille avec les flèches et sélectionnez un personnage (ENTRÉE)",
            "Votre personnage est sélectionné (portrait affiché)"
        )
        results.append(("Sélection personnage", ok))

        # Test 6
        ok = self.next_step(
            "Jouez pendant 30 secondes (déplacez-vous, attaquez)",
            "Le combat se déroule normalement"
        )
        results.append(("Gameplay", ok))

        # Test 7
        ok = self.next_step(
            "Appuyez sur ESCAPE, naviguez dans le menu pause, puis sortez",
            "Retour au menu principal"
        )
        results.append(("Pause & sortie", ok))

        # Rapport
        print("\n" + "="*70)
        print("  RAPPORT FINAL")
        print("="*70 + "\n")

        passed = sum(1 for _, ok in results if ok)
        total = len(results)

        print(f"Tests réussis: {passed}/{total}\n")

        for test_name, ok in results:
            icon = "✅" if ok else "❌"
            print(f"{icon} {test_name}")

        duration = (datetime.now() - self.start_time).total_seconds()
        print(f"\n⏱️  Durée: {duration:.0f}s ({duration/60:.1f} min)")

        # Sauvegarder
        with open("logs/test_manuel_guide.txt", 'w', encoding='utf-8') as f:
            f.write("TEST MANUEL GUIDÉ\n")
            f.write("="*70 + "\n\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Durée: {duration:.0f}s\n")
            f.write(f"Réussis: {passed}/{total}\n\n")
            for test_name, ok in results:
                status = "OK" if ok else "ÉCHEC"
                f.write(f"[{status}] {test_name}\n")

        print("\n📄 Rapport sauvegardé: logs/test_manuel_guide.txt")

if __name__ == "__main__":
    tester = GuidedTest()
    tester.run()

    print("\n" + "="*70)
    input("Appuyez sur ENTRÉE pour fermer...")
