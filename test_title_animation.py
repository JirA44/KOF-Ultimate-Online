#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide pour vérifier que l'animation du titre fonctionne
"""

import subprocess
import time
import os
from pathlib import Path

def test_title_animation():
    base_dir = Path(r"D:\KOF Ultimate Online")
    exe_path = base_dir / "KOF_Ultimate_Online.exe"
    log_path = base_dir / "mugen.log"

    # Supprimer l'ancien log
    if log_path.exists():
        os.remove(log_path)
        print("✓ Ancien log supprimé")

    print("\n🎮 Lancement du jeu pour tester l'animation du titre...")
    print("   Le jeu va se lancer pendant 8 secondes")
    print("   Vérifiez visuellement si l'animation est visible sur l'écran titre\n")

    # Lancer le jeu
    try:
        process = subprocess.Popen(
            [str(exe_path)],
            cwd=str(base_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        print(f"✓ Jeu lancé (PID: {process.pid})")
        print("⏳ Attente de 8 secondes...")

        # Attendre 8 secondes
        time.sleep(8)

        # Terminer le processus
        print("🛑 Fermeture du jeu...")
        process.terminate()

        # Attendre que le processus se termine
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

        print("✓ Jeu fermé\n")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return

    # Analyser le log
    print("📋 Analyse du log mugen.log...\n")

    if not log_path.exists():
        print("❌ Le fichier mugen.log n'a pas été créé")
        return

    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        log_content = f.read()

    # Vérifier les erreurs liées au TitleBG
    if "Error loading TitleBG" in log_content:
        print("❌ ERREUR: TitleBG n'a pas pu être chargé!")
        # Trouver et afficher l'erreur
        for line in log_content.split('\n'):
            if "TitleBG" in line or "Error" in line:
                print(f"   {line}")
    elif "Load TitleBG" in log_content:
        print("✅ TitleBG chargé sans erreur!")
    else:
        print("⚠️  Aucune mention explicite du TitleBG dans le log")

    # Vérifier que le jeu a atteint l'écran titre
    if "Gameflow 2" in log_content:
        print("✅ Le jeu a atteint l'écran titre (Gameflow 2)")
    else:
        print("⚠️  Le jeu n'a peut-être pas atteint l'écran titre")

    print("\n" + "="*60)
    print("RÉSULTAT DU TEST")
    print("="*60)

    # Afficher les lignes pertinentes du log
    print("\nLignes importantes du log:")
    for line in log_content.split('\n'):
        if any(keyword in line for keyword in ["TitleBG", "SelectBG", "VictoryBG", "VersusBG", "Error loading", "Gameflow"]):
            print(f"  {line.strip()}")

    print("\n💡 VÉRIFICATION VISUELLE:")
    print("   Avez-vous vu une animation sur l'écran titre?")
    print("   L'animation devrait montrer des effets de fade/transparence")
    print("   avec les sprites 878,62 et 878,63")

if __name__ == '__main__':
    test_title_animation()
