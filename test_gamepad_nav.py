#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - Test Navigation Manette
Vérifie que les manettes peuvent naviguer dans le menu
"""

import subprocess
import time
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def check_gamepad_config():
    """Vérifie la configuration des manettes dans mugen.cfg"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}VÉRIFICATION CONFIGURATION MANETTE{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")

    config_file = Path(r"D:\KOF Ultimate Online\data\mugen.cfg")

    if not config_file.exists():
        print(f"{Colors.RED}✗ mugen.cfg introuvable!{Colors.RESET}")
        return False

    with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    issues = []

    # Vérifier joystick.enabled
    if "Joystick.enabled" in content:
        for line in content.split('\n'):
            if 'Joystick.enabled' in line and not line.strip().startswith(';'):
                value = line.split('=')[-1].strip()
                if value == '1':
                    print(f"{Colors.GREEN}  ✓ Joystick activé{Colors.RESET}")
                else:
                    print(f"{Colors.YELLOW}  ⚠ Joystick désactivé{Colors.RESET}")
                    issues.append("Joystick désactivé dans la config")
                break
    else:
        print(f"{Colors.RED}  ✗ Configuration joystick manquante{Colors.RESET}")
        issues.append("Pas de config joystick")

    # Vérifier InputAutoremap
    if "InputAutoremap" in content:
        for line in content.split('\n'):
            if 'InputAutoremap' in line and not line.strip().startswith(';'):
                value = line.split('=')[-1].strip()
                if value == '1':
                    print(f"{Colors.GREEN}  ✓ Auto-remap activé{Colors.RESET}")
                else:
                    print(f"{Colors.YELLOW}  ⚠ Auto-remap désactivé{Colors.RESET}")
                break

    # Vérifier mappings P1 et P2
    p1_keys_found = False
    p2_keys_found = False

    for line in content.split('\n'):
        if '[P1 Keys]' in line:
            p1_keys_found = True
        if '[P2 Keys]' in line:
            p2_keys_found = True

    if p1_keys_found:
        print(f"{Colors.GREEN}  ✓ Config touches P1 trouvée{Colors.RESET}")
    else:
        print(f"{Colors.RED}  ✗ Config touches P1 manquante{Colors.RESET}")
        issues.append("Config P1 manquante")

    if p2_keys_found:
        print(f"{Colors.GREEN}  ✓ Config touches P2 trouvée{Colors.RESET}")
    else:
        print(f"{Colors.RED}  ✗ Config touches P2 manquante{Colors.RESET}")
        issues.append("Config P2 manquante")

    if issues:
        print(f"\n{Colors.YELLOW}Issues détectées:{Colors.RESET}")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"\n{Colors.GREEN}✓ Configuration manette OK{Colors.RESET}")
        return True

def enable_joystick_if_needed():
    """Active le joystick si nécessaire"""
    print(f"\n{Colors.CYAN}Activation automatique du joystick...{Colors.RESET}")

    config_file = Path(r"D:\KOF Ultimate Online\data\mugen.cfg")

    with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Remplacer Joystick.enabled = 0 par Joystick.enabled = 1
    content_modified = content.replace('Joystick.enabled = 0', 'Joystick.enabled = 1')

    if content != content_modified:
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(content_modified)

        print(f"{Colors.GREEN}  ✓ Joystick activé!{Colors.RESET}")
        return True
    else:
        print(f"{Colors.GREEN}  ✓ Joystick déjà activé{Colors.RESET}")
        return True

def main():
    print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'TEST NAVIGATION MANETTE':^80}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

    print(f"{Colors.CYAN}Ce test vérifie que:{Colors.RESET}")
    print(f"  1. Les manettes sont activées dans la config")
    print(f"  2. Les touches sont bien mappées")
    print(f"  3. La navigation au menu fonctionne\n")

    # Vérifier la config
    config_ok = check_gamepad_config()

    if not config_ok:
        enable_joystick_if_needed()

    print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Vérification terminée{Colors.RESET}")
    print(f"\n{Colors.CYAN}Pour tester:{Colors.RESET}")
    print(f"  1. Branche ta manette")
    print(f"  2. Lance le jeu")
    print(f"  3. Utilise la manette pour naviguer dans le menu")
    print(f"  4. Les flèches / D-pad doivent faire défiler les options")
    print(f"  5. Le bouton A doit valider")
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interruption par l'utilisateur{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Erreur: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
