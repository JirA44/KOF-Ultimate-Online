#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - Testeur Simple
Lance le jeu et te laisse le voir en action
"""

import subprocess
import time
import os
from pathlib import Path
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def main():
    game_dir = Path(r"D:\KOF Ultimate Online Online Online")
    exe_path = game_dir / "KOF_Ultimate_Online.exe"
    log_file = game_dir / "mugen.log"

    print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'KOF ULTIMATE - TEST MANUEL SIMPLE':^80}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

    print(f"{Colors.CYAN}Ce test va:{Colors.RESET}")
    print(f"  1. Lancer le jeu")
    print(f"  2. Attendre 30 secondes")
    print(f"  3. Fermer le jeu automatiquement")
    print(f"  4. Analyser le log\n")

    print(f"{Colors.YELLOW}PENDANT LE TEST, REGARDE BIEN:{Colors.RESET}")
    print(f"  ❓ Le fond du menu est-il NOIR ou ANIMÉ?")
    print(f"  ❓ L'option 'MULTIJOUEUR EN LIGNE' apparaît-elle?")
    print(f"  ❓ Y a-t-il des animations qui bougent?\n")

    input(f"{Colors.CYAN}Appuie sur ENTRÉE pour démarrer le test...{Colors.RESET}")

    # Supprimer l'ancien log
    if log_file.exists():
        log_file.unlink()

    # Lancer le jeu
    print(f"\n{Colors.GREEN}🎮 Lancement du jeu...{Colors.RESET}")
    process = subprocess.Popen(
        [str(exe_path)],
        cwd=str(game_dir)
    )

    print(f"{Colors.GREEN}✓ Jeu lancé (PID: {process.pid}){Colors.RESET}\n")

    # Compter à rebours
    print(f"{Colors.CYAN}⏱ Compte à rebours (observe bien le jeu!):{Colors.RESET}\n")
    for remaining in range(30, 0, -1):
        print(f"\r  {remaining:2d} secondes restantes... ", end='', flush=True)
        time.sleep(1)
    print(f"\r  {Colors.GREEN}✓ Test terminé!          {Colors.RESET}\n")

    # Fermer le jeu
    print(f"{Colors.YELLOW}⏹ Fermeture du jeu...{Colors.RESET}")
    try:
        process.terminate()
        process.wait(timeout=5)
    except:
        try:
            process.kill()
        except:
            pass

    print(f"{Colors.GREEN}✓ Jeu fermé{Colors.RESET}\n")

    # Attendre un peu pour que le log soit écrit
    time.sleep(2)

    # Analyser le log
    print(f"{Colors.CYAN}{Colors.BOLD}📋 ANALYSE DU LOG{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")

    if not log_file.exists():
        print(f"{Colors.RED}✗ Fichier log introuvable!{Colors.RESET}")
        return

    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Vérifier TitleBG
    if "Load TitleBG" in content:
        if "TitleBG...OK" in content or "TitleBG...VersusBG...VictoryBG...SelectBG...OptionBG...OK" in content:
            print(f"{Colors.GREEN}✓ TitleBG chargé avec succès{Colors.RESET}")
        else:
            print(f"{Colors.RED}✗ TitleBG a des erreurs{Colors.RESET}")

    # Vérifier Title Info
    if "Load [Title Info]...OK" in content:
        print(f"{Colors.GREEN}✓ Title Info (menu) chargé avec succès{Colors.RESET}")
    else:
        print(f"{Colors.RED}✗ Title Info n'a pas chargé correctement{Colors.RESET}")

    # Compter les erreurs
    errors = []
    for line in content.split('\n'):
        if 'error' in line.lower() or ('failed' in line.lower() and 'pads' not in line.lower()):
            errors.append(line.strip())

    # Retirer les erreurs x/x.def (connues)
    real_errors = [e for e in errors if 'chars/x/x.def' not in e]

    print(f"\n{Colors.CYAN}Erreurs détectées:{Colors.RESET}")
    print(f"  - Erreurs chars/x/x.def: {len(errors) - len(real_errors)} (connues, à nettoyer)")
    print(f"  - Autres erreurs: {len(real_errors)}")

    if real_errors:
        print(f"\n{Colors.RED}Erreurs critiques:{Colors.RESET}")
        for error in real_errors[:5]:
            print(f"  - {error}")

    # Questions à l'utilisateur
    print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'FEEDBACK UTILISATEUR':^80}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

    print(f"{Colors.YELLOW}Maintenant DIS-MOI ce que TU as vu:{Colors.RESET}\n")

    feedback = {}

    feedback['fond_noir'] = input(f"  1. Le fond du menu était-il NOIR? (oui/non): ").lower().strip()
    feedback['animation'] = input(f"  2. Y avait-il des ANIMATIONS qui bougeaient? (oui/non): ").lower().strip()
    feedback['option_multi'] = input(f"  3. L'option 'MULTIJOUEUR EN LIGNE' était visible? (oui/non): ").lower().strip()
    feedback['bugs'] = input(f"  4. As-tu vu des bugs ou crashs? (oui/non): ").lower().strip()

    # Rapport final
    print(f"\n{Colors.CYAN}{Colors.BOLD}📊 RAPPORT FINAL{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")

    issues = []

    if feedback['fond_noir'] == 'oui':
        issues.append("❌ PROBLÈME: Le fond est noir (devrait être animé)")
    elif feedback['animation'] == 'non':
        issues.append("❌ PROBLÈME: Pas d'animations visibles")

    if feedback['option_multi'] == 'non':
        issues.append("❌ PROBLÈME: Option 'MULTIJOUEUR EN LIGNE' manquante")

    if feedback['bugs'] == 'oui':
        issues.append("❌ PROBLÈME: Bugs détectés pendant le jeu")

    if issues:
        print(f"{Colors.RED}Issues trouvées:{Colors.RESET}")
        for issue in issues:
            print(f"  {issue}")
    else:
        print(f"{Colors.GREEN}✓ Aucun problème signalé par l'utilisateur!{Colors.RESET}")

    # Sauvegarder le rapport
    report_dir = game_dir / "test_reports"
    report_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = report_dir / f"manual_test_{timestamp}.txt"

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("KOF ULTIMATE - RAPPORT DE TEST MANUEL\n")
        f.write("="*80 + "\n\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("FEEDBACK UTILISATEUR:\n")
        f.write(f"  - Fond noir: {feedback['fond_noir']}\n")
        f.write(f"  - Animations visibles: {feedback['animation']}\n")
        f.write(f"  - Option multijoueur visible: {feedback['option_multi']}\n")
        f.write(f"  - Bugs rencontrés: {feedback['bugs']}\n\n")
        f.write("ISSUES DÉTECTÉES:\n")
        if issues:
            for issue in issues:
                f.write(f"  {issue}\n")
        else:
            f.write("  Aucune\n")

    print(f"\n{Colors.GREEN}✓ Rapport sauvegardé: {report_file}{Colors.RESET}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interruption par l'utilisateur{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Erreur: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
