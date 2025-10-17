#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - FIX CLSN FINAL (REGROUPEMENT)
Regroupe TOUTES les Clsn boxes AU DÉBUT de chaque action
"""

import re
from pathlib import Path
import shutil
from datetime import datetime

game_dir = Path(r"D:\KOF Ultimate Online")
chars_dir = game_dir / "chars"
backup_dir = game_dir / "backups_clsn_regrouped"
backup_dir.mkdir(exist_ok=True)

def fix_air_regroup_clsn(air_file):
    """Regroupe les Clsn boxes au début de chaque action"""
    try:
        with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        # Parse actions
        actions = []
        current_action = None

        for i, line in enumerate(lines):
            # Detect action start
            match = re.match(r'^\[Begin Action (\d+)\]', line, re.IGNORECASE)
            if match:
                if current_action:
                    actions.append(current_action)

                current_action = {
                    'num': int(match.group(1)),
                    'start_line': i,
                    'header': line,
                    'clsn1default': None,
                    'clsn2default': None,
                    'clsn1_boxes': [],
                    'clsn2_boxes': [],
                    'other_lines': []
                }
                continue

            if not current_action:
                # Before first action
                continue

            # Detect Clsn1Default
            match = re.match(r'^(\s*Clsn1Default:.+)$', line)
            if match:
                current_action['clsn1default'] = line
                continue

            # Detect Clsn2Default
            match = re.match(r'^(\s*Clsn2Default:.+)$', line)
            if match:
                current_action['clsn2default'] = line
                continue

            # Detect Clsn1 counter - SKIP
            if re.match(r'^\s*Clsn1:\s*\d+\s*$', line):
                continue

            # Detect Clsn2 counter - SKIP
            if re.match(r'^\s*Clsn2:\s*\d+\s*$', line):
                continue

            # Detect Clsn1 box - COLLECT
            match = re.match(r'^\s*Clsn1\[\d+\]\s*=(.+)$', line)
            if match:
                current_action['clsn1_boxes'].append(match.group(1).strip())
                continue

            # Detect Clsn2 box - COLLECT
            match = re.match(r'^\s*Clsn2\[\d+\]\s*=(.+)$', line)
            if match:
                current_action['clsn2_boxes'].append(match.group(1).strip())
                continue

            # Everything else
            current_action['other_lines'].append(line)

        if current_action:
            actions.append(current_action)

        # Rebuild file
        result_lines = []

        # Add lines before first action
        if actions:
            first_action_line = actions[0]['start_line']
            result_lines.extend(lines[:first_action_line])

        modified = False

        for action in actions:
            # Add action header
            result_lines.append(action['header'])

            # Add Clsn defaults if present
            if action['clsn1default']:
                result_lines.append(action['clsn1default'])
            if action['clsn2default']:
                result_lines.append(action['clsn2default'])

            # Add ALL Clsn1 boxes (regrouped, reindexed)
            if action['clsn1_boxes']:
                result_lines.append(f"Clsn1: {len(action['clsn1_boxes'])}\n")
                for idx, box_data in enumerate(action['clsn1_boxes']):
                    result_lines.append(f"Clsn1[{idx}] = {box_data}\n")
                    modified = True

            # Add ALL Clsn2 boxes (regrouped, reindexed)
            if action['clsn2_boxes']:
                result_lines.append(f"Clsn2: {len(action['clsn2_boxes'])}\n")
                for idx, box_data in enumerate(action['clsn2_boxes']):
                    result_lines.append(f"Clsn2[{idx}] = {box_data}\n")
                    modified = True

            # Add all other lines (sprites, etc.)
            result_lines.extend(action['other_lines'])

        if modified:
            # Backup
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f'{air_file.name}.regrouped_{timestamp}'
            backup_path = backup_dir / backup_name
            shutil.copy2(air_file, backup_path)

            # Save
            with open(air_file, 'w', encoding='utf-8') as f:
                f.writelines(result_lines)

            return True

        return False

    except Exception as e:
        print(f'ERROR {air_file.name}: {e}')
        return False

def main():
    """Main function"""
    air_files = list(chars_dir.rglob('*.air'))

    print('=' * 70)
    print('🔧 FIX FINAL - REGROUPEMENT CLSN BOXES')
    print('=' * 70)
    print(f'Total: {len(air_files)} fichiers')
    print()
    print('Ce script va:')
    print('  1. Extraire TOUTES les Clsn boxes de chaque action')
    print('  2. Les regrouper AU DÉBUT de l\'action')
    print('  3. Mettre les sprites APRÈS')
    print()
    print('=' * 70)
    print()

    fixed_count = 0

    for air_file in air_files:
        try:
            if fix_air_regroup_clsn(air_file):
                fixed_count += 1
                print(f'✅ {air_file.parent.name}/{air_file.name}')
        except Exception as e:
            print(f'❌ {air_file.parent.name}/{air_file.name}: {e}')

    print()
    print('=' * 70)
    print('📊 RAPPORT FINAL')
    print('=' * 70)
    print(f'✅ Corrigés: {fixed_count}/{len(air_files)}')
    print(f'💾 Backups: {backup_dir}')
    print('=' * 70)

if __name__ == '__main__':
    main()
