#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - COMPREHENSIVE CLSN FIXER
Fixes Clsn counts AND reindexes collision boxes in all AIR files
"""

import re
from pathlib import Path
import shutil
from datetime import datetime

game_dir = Path(r"D:\KOF Ultimate Online")
chars_dir = game_dir / "chars"
backup_dir = game_dir / "backups_clsn_comprehensive_final"
backup_dir.mkdir(exist_ok=True)

def fix_clsn_complete(air_file):
    """Fix Clsn: reindex boxes AND update counts"""
    try:
        with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        # First pass: identify actions and count boxes
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
                    'clsn1_count_line': None,
                    'clsn2_count_line': None,
                    'clsn1_boxes': [],
                    'clsn2_boxes': []
                }
                continue

            if not current_action:
                continue

            # Detect Clsn1 counter
            if re.match(r'^\s*Clsn1:\s*\d+\s*$', line):
                current_action['clsn1_count_line'] = i
                continue

            # Detect Clsn2 counter
            if re.match(r'^\s*Clsn2:\s*\d+\s*$', line):
                current_action['clsn2_count_line'] = i
                continue

            # Detect Clsn1 box
            if re.match(r'^\s*Clsn1\[(\d+)\]', line):
                current_action['clsn1_boxes'].append(i)
                continue

            # Detect Clsn2 box
            if re.match(r'^\s*Clsn2\[(\d+)\]', line):
                current_action['clsn2_boxes'].append(i)
                continue

        if current_action:
            actions.append(current_action)

        # Second pass: rebuild file with fixes
        fixed_lines = []
        modified = False

        clsn1_index = 0
        clsn2_index = 0
        in_action_num = None

        for i, line in enumerate(lines):
            # Check if this is an action start
            match = re.match(r'^\[Begin Action (\d+)\]', line, re.IGNORECASE)
            if match:
                in_action_num = int(match.group(1))
                clsn1_index = 0
                clsn2_index = 0
                fixed_lines.append(line)
                continue

            # Find current action data
            action_data = None
            for act in actions:
                if act['num'] == in_action_num:
                    action_data = act
                    break

            # Check if this is a Clsn1 counter line
            if action_data and i == action_data.get('clsn1_count_line'):
                correct_count = len(action_data['clsn1_boxes'])
                old_match = re.match(r'^\s*Clsn1:\s*(\d+)', line)
                if old_match:
                    old_count = int(old_match.group(1))
                    if old_count != correct_count:
                        modified = True
                fixed_lines.append(f'Clsn1: {correct_count}\n')
                continue

            # Check if this is a Clsn2 counter line
            if action_data and i == action_data.get('clsn2_count_line'):
                correct_count = len(action_data['clsn2_boxes'])
                old_match = re.match(r'^\s*Clsn2:\s*(\d+)', line)
                if old_match:
                    old_count = int(old_match.group(1))
                    if old_count != correct_count:
                        modified = True
                fixed_lines.append(f'Clsn2: {correct_count}\n')
                continue

            # Check if this is a Clsn1 box - reindex
            match = re.match(r'^\s*Clsn1\[(\d+)\]\s*=(.+)$', line)
            if match:
                old_index = int(match.group(1))
                box_data = match.group(2)
                if old_index != clsn1_index:
                    modified = True
                fixed_lines.append(f'Clsn1[{clsn1_index}] ={box_data}\n')
                clsn1_index += 1
                continue

            # Check if this is a Clsn2 box - reindex
            match = re.match(r'^\s*Clsn2\[(\d+)\]\s*=(.+)$', line)
            if match:
                old_index = int(match.group(1))
                box_data = match.group(2)
                if old_index != clsn2_index:
                    modified = True
                fixed_lines.append(f'Clsn2[{clsn2_index}] ={box_data}\n')
                clsn2_index += 1
                continue

            fixed_lines.append(line)

        if modified:
            # Backup
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f'{air_file.name}.comprehensive_{timestamp}'
            backup_path = backup_dir / backup_name
            shutil.copy2(air_file, backup_path)

            # Save
            with open(air_file, 'w', encoding='utf-8') as f:
                f.writelines(fixed_lines)

            return True

        return False

    except Exception as e:
        print(f'ERROR {air_file.name}: {e}')
        return False

def main():
    """Main function"""
    # Get all AIR files
    air_files = list(chars_dir.rglob('*.air'))

    print('=' * 70)
    print('🔧 CORRECTION COMPREHENSIVE - TOUS LES AIR FILES')
    print('=' * 70)
    print(f'Total: {len(air_files)} fichiers à traiter')
    print()

    fixed_count = 0
    error_count = 0

    for air_file in air_files:
        try:
            if fix_clsn_complete(air_file):
                fixed_count += 1
                print(f'✅ {air_file.parent.name}/{air_file.name}')
        except Exception as e:
            error_count += 1
            print(f'❌ {air_file.parent.name}/{air_file.name}: {e}')

    print()
    print('=' * 70)
    print('📊 RAPPORT FINAL')
    print('=' * 70)
    print(f'Total traités: {len(air_files)}')
    print(f'✅ Corrigés: {fixed_count}')
    print(f'⚠️  Déjà OK: {len(air_files) - fixed_count - error_count}')
    print(f'❌ Erreurs: {error_count}')
    print(f'\n💾 Backups: {backup_dir}')
    print('=' * 70)

if __name__ == '__main__':
    main()
