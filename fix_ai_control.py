"""
Script pour désactiver le contrôle IA et permettre au joueur de jouer normalement
"""

import os
from pathlib import Path

def fix_ai_control():
    """Désactive l'IA qui joue à la place du joueur"""

    config_file = Path("D:/KOF Ultimate Online/data/mugen.cfg")

    if not config_file.exists():
        print(f"❌ Fichier de configuration introuvable: {config_file}")
        return False

    print("🔧 Correction du contrôle IA...")

    try:
        # Lire le fichier
        with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        modified = False
        new_lines = []

        for line in lines:
            # Désactiver l'IA qui "triche" (joue à la place du joueur)
            if line.strip().startswith('AI.Cheat'):
                new_lines.append('AI.Cheat = 0\n')
                modified = True
                print("  ✓ AI.Cheat désactivé (0)")

            # S'assurer que les joueurs utilisent le clavier
            elif line.strip().startswith('P1.UseKeyboard'):
                new_lines.append('P1.UseKeyboard = 1\n')
                print("  ✓ P1.UseKeyboard activé (1)")

            elif line.strip().startswith('P2.UseKeyboard'):
                new_lines.append('P2.UseKeyboard = 1\n')
                print("  ✓ P2.UseKeyboard activé (1)")

            else:
                new_lines.append(line)

        if modified:
            # Sauvegarder les modifications
            with open(config_file, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

            print("\n✅ Configuration corrigée!")
            print("   Maintenant vous pouvez jouer normalement avec vos contrôles:")
            print("\n   🎮 Contrôles Joueur 1:")
            print("      Flèches directionnelles: ↑ ↓ ← →")
            print("      Attaques: A, S, D, F, G, H")
            print("      Start: Entrée")
            print("\n   🎮 Contrôles Joueur 2:")
            print("      Déplacement: Q, W, E, R")
            print("      Attaques: T, U, O, P, L")

            return True
        else:
            print("ℹ️  Aucune modification nécessaire")
            return True

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════╗
║   FIX AI CONTROL - KOF Ultimate                    ║
║                                                    ║
║   Ce script désactive l'IA qui joue à votre place ║
╚════════════════════════════════════════════════════╝
    """)

    success = fix_ai_control()

    if success:
        print("\n🎮 Vous pouvez maintenant lancer le jeu et jouer normalement!")
    else:
        print("\n❌ La correction a échoué. Vérifiez le chemin du fichier.")

    input("\nAppuyez sur Entrée pour quitter...")
