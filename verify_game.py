#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification complète de KOF Ultimate
Génère un rapport détaillé sur l'état du jeu
"""

import os
import sys
from pathlib import Path
from collections import defaultdict

# Couleurs pour le terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_header(text):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text:^80}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*80}{Colors.RESET}\n")

def print_section(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{text}{Colors.RESET}")
    print(f"{Colors.BLUE}{'-'*len(text)}{Colors.RESET}")

def print_ok(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.WHITE}  {text}{Colors.RESET}")

def check_file_exists(file_path, description=""):
    """Vérifie si un fichier existe"""
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        size_mb = size / (1024 * 1024)
        desc = f" ({description})" if description else ""
        print_ok(f"{os.path.basename(file_path)}{desc} - {size_mb:.2f} MB")
        return True
    else:
        desc = f" ({description})" if description else ""
        print_error(f"{os.path.basename(file_path)}{desc} - MANQUANT")
        return False

def check_directory_exists(dir_path, description=""):
    """Vérifie si un dossier existe"""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        count = len(os.listdir(dir_path))
        desc = f" ({description})" if description else ""
        print_ok(f"{os.path.basename(dir_path)}{desc} - {count} fichiers/dossiers")
        return True
    else:
        desc = f" ({description})" if description else ""
        print_error(f"{os.path.basename(dir_path)}{desc} - MANQUANT")
        return False

def analyze_select_def(file_path):
    """Analyse le fichier select.def pour compter les personnages"""
    characters = []
    stages = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            in_chars_section = False
            in_stages_section = False

            for line in f:
                line = line.strip()

                if line.startswith('[Characters]'):
                    in_chars_section = True
                    in_stages_section = False
                    continue
                elif line.startswith('[ExtraStages]'):
                    in_stages_section = True
                    in_chars_section = False
                    continue
                elif line.startswith('['):
                    in_chars_section = False
                    in_stages_section = False
                    continue

                if in_chars_section and line and not line.startswith(';') and line.lower() != 'x':
                    characters.append(line.split(',')[0].strip())

                if in_stages_section and line and not line.startswith(';'):
                    stages.append(line)

        return characters, stages
    except Exception as e:
        print_error(f"Erreur lors de la lecture de select.def: {e}")
        return [], []

def analyze_stages_directory(stages_dir):
    """Analyse le dossier des stages"""
    stages = []
    if os.path.exists(stages_dir):
        for file in os.listdir(stages_dir):
            if file.endswith('.def'):
                stages.append(file)
    return stages

def analyze_chars_directory(chars_dir):
    """Analyse le dossier des personnages"""
    characters = []
    if os.path.exists(chars_dir):
        for item in os.listdir(chars_dir):
            char_path = os.path.join(chars_dir, item)
            if os.path.isdir(char_path):
                # Vérifier si le dossier contient un fichier .def
                has_def = any(f.endswith('.def') for f in os.listdir(char_path))
                if has_def:
                    characters.append(item)
    return characters

def check_config_file(file_path):
    """Vérifie un fichier de configuration"""
    if not os.path.exists(file_path):
        print_error(f"{os.path.basename(file_path)} - MANQUANT")
        return False

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            print_ok(f"{os.path.basename(file_path)} - {len(lines)} lignes")
            return True
    except Exception as e:
        print_error(f"{os.path.basename(file_path)} - ERREUR: {e}")
        return False

def main():
    print_header("VÉRIFICATION COMPLÈTE DE KOF ULTIMATE")

    base_dir = Path(__file__).parent
    os.chdir(base_dir)

    print_info(f"Répertoire du jeu: {base_dir}")

    # Statistiques globales
    stats = {
        'files_ok': 0,
        'files_missing': 0,
        'dirs_ok': 0,
        'dirs_missing': 0,
        'characters': 0,
        'stages': 0
    }

    # 1. FICHIERS EXÉCUTABLES
    print_section("1. FICHIERS EXÉCUTABLES")
    executables = [
        ('KOF BLACK R.exe', 'Exécutable principal du jeu'),
        ('KOF Ultimate Launcher.exe', 'Launcher moderne'),
        ('launch_complete_system.bat', 'Script de lancement complet'),
        ('LAUNCH_ULTIMATE.bat', 'Script de lancement simple'),
    ]
    for exe, desc in executables:
        if check_file_exists(exe, desc):
            stats['files_ok'] += 1
        else:
            stats['files_missing'] += 1

    # 2. DOSSIERS PRINCIPAUX
    print_section("2. DOSSIERS PRINCIPAUX")
    directories = [
        ('data', 'Données du jeu'),
        ('chars', 'Personnages'),
        ('stages', 'Stages/Arènes'),
        ('sound', 'Sons et musiques'),
        ('font', 'Polices'),
        ('tools', 'Outils'),
    ]
    for dir_name, desc in directories:
        if check_directory_exists(dir_name, desc):
            stats['dirs_ok'] += 1
        else:
            stats['dirs_missing'] += 1

    # 3. FICHIERS DE CONFIGURATION
    print_section("3. FICHIERS DE CONFIGURATION")
    configs = [
        'data/system.def',
        'data/select.def',
        'data/fight.def',
        'data/mugen.cfg',
    ]
    for config in configs:
        if check_config_file(config):
            stats['files_ok'] += 1
        else:
            stats['files_missing'] += 1

    # 4. FICHIERS D'ASSETS
    print_section("4. ASSETS (SPRITES & SONS)")
    assets = [
        ('data/system.sff', 'Sprites du système'),
        ('data/system.snd', 'Sons du système'),
        ('data/fight.sff', 'Sprites de combat'),
        ('data/fight.snd', 'Sons de combat'),
        ('data/fightfx.sff', 'Effets de combat'),
    ]
    for asset, desc in assets:
        if check_file_exists(asset, desc):
            stats['files_ok'] += 1
        else:
            stats['files_missing'] += 1

    # 5. ANALYSE DES PERSONNAGES
    print_section("5. PERSONNAGES")
    chars_in_select, stages_in_select = analyze_select_def('data/select.def')
    chars_in_directory = analyze_chars_directory('chars')

    print_info(f"Personnages dans select.def: {len(chars_in_select)}")
    print_info(f"Dossiers de personnages: {len(chars_in_directory)}")

    stats['characters'] = len(chars_in_select)

    # Vérifier les personnages manquants
    missing_chars = []
    for char in chars_in_select[:10]:  # Vérifier les 10 premiers
        char_path = os.path.join('chars', char)
        if not os.path.exists(char_path):
            missing_chars.append(char)

    if missing_chars:
        print_warning(f"{len(missing_chars)} personnages dans select.def n'ont pas de dossier")
        for char in missing_chars[:5]:
            print_info(f"  - {char}")
    else:
        print_ok("Tous les personnages vérifiés ont leur dossier")

    # 6. ANALYSE DES STAGES
    print_section("6. STAGES")
    stages_in_directory = analyze_stages_directory('stages')

    print_info(f"Stages dans select.def: {len(stages_in_select)}")
    print_info(f"Fichiers .def dans stages/: {len(stages_in_directory)}")

    stats['stages'] = len(stages_in_directory)

    # 7. SCRIPTS PYTHON
    print_section("7. SCRIPTS PYTHON")
    python_scripts = [
        ('launcher_modern.py', 'Launcher moderne v2.0'),
        ('gamepad_hotplug_monitor.py', 'Monitor hot-plug'),
        ('launcher_ai_navigator.py', 'Agent IA'),
        ('gamepad_auto_config.py', 'Config auto des manettes'),
    ]
    for script, desc in python_scripts:
        if check_file_exists(script, desc):
            stats['files_ok'] += 1
        else:
            stats['files_missing'] += 1

    # 8. BACKGROUNDS
    print_section("8. BACKGROUNDS")
    bg_dir = 'data/backgrounds'
    if os.path.exists(bg_dir):
        bg_files = [f for f in os.listdir(bg_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        print_ok(f"{len(bg_files)} fichiers d'images de fond")
        stats['files_ok'] += len(bg_files)
    else:
        print_warning("Dossier backgrounds non trouvé")

    # RAPPORT FINAL
    print_section("RAPPORT FINAL")

    total_files = stats['files_ok'] + stats['files_missing']
    total_dirs = stats['dirs_ok'] + stats['dirs_missing']

    print(f"\n{Colors.BOLD}Fichiers:{Colors.RESET}")
    print_ok(f"{stats['files_ok']} fichiers OK")
    if stats['files_missing'] > 0:
        print_error(f"{stats['files_missing']} fichiers manquants")

    print(f"\n{Colors.BOLD}Dossiers:{Colors.RESET}")
    print_ok(f"{stats['dirs_ok']} dossiers OK")
    if stats['dirs_missing'] > 0:
        print_error(f"{stats['dirs_missing']} dossiers manquants")

    print(f"\n{Colors.BOLD}Contenu:{Colors.RESET}")
    print_ok(f"{stats['characters']} personnages configurés")
    print_ok(f"{stats['stages']} stages disponibles")

    # Score global
    total_checks = total_files + total_dirs
    total_ok = stats['files_ok'] + stats['dirs_ok']

    if total_checks > 0:
        success_rate = (total_ok / total_checks) * 100
        print(f"\n{Colors.BOLD}Score Global:{Colors.RESET}")

        if success_rate >= 90:
            print(f"{Colors.GREEN}{Colors.BOLD}{success_rate:.1f}% - EXCELLENT{Colors.RESET}")
        elif success_rate >= 70:
            print(f"{Colors.YELLOW}{Colors.BOLD}{success_rate:.1f}% - BON{Colors.RESET}")
        else:
            print(f"{Colors.RED}{Colors.BOLD}{success_rate:.1f}% - PROBLÈMES DÉTECTÉS{Colors.RESET}")

    # RECOMMANDATIONS
    print_section("RECOMMANDATIONS")

    if stats['files_missing'] == 0 and stats['dirs_missing'] == 0:
        print_ok("Le jeu semble complet et prêt à être lancé!")
        print_info("Pour démarrer: Double-cliquez sur launch_complete_system.bat")
    else:
        print_warning("Quelques fichiers ou dossiers sont manquants")
        print_info("Vérifiez les détails ci-dessus pour plus d'informations")

    print("\n")

if __name__ == '__main__':
    main()
