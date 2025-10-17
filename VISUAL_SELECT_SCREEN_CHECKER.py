#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VISUAL SELECT SCREEN CHECKER - KOF ULTIMATE
Génère un rendu visuel HTML de l'écran de sélection pour vérifier la disposition
"""

import os
import re
from pathlib import Path
from datetime import datetime

class VisualSelectScreenChecker:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.system_def = self.base_path / "data" / "system.def"
        self.select_def = self.base_path / "data" / "select.def"

    def parse_system_def(self):
        """Parse system.def pour extraire la configuration"""
        content = self.system_def.read_text(encoding='utf-8', errors='ignore')

        config = {}

        # Grid config
        config['rows'] = int(re.search(r'rows\s*=\s*(\d+)', content).group(1))
        config['columns'] = int(re.search(r'columns\s*=\s*(\d+)', content).group(1))

        pos_match = re.search(r'pos\s*=\s*(\d+)\s*,\s*(\d+)', content)
        config['grid_x'] = int(pos_match.group(1))
        config['grid_y'] = int(pos_match.group(2))

        cell_size_match = re.search(r'cell\.size\s*=\s*(\d+)\s*,\s*(\d+)', content)
        config['cell_w'] = int(cell_size_match.group(1))
        config['cell_h'] = int(cell_size_match.group(2))

        cell_spacing_match = re.search(r'cell\.spacing\s*=\s*(\d+)', content)
        config['cell_spacing'] = int(cell_spacing_match.group(1))

        # Portrait config P1
        p1_face_offset = re.search(r'p1\.face\.offset\s*=\s*(\d+)\s*,\s*(\d+)', content)
        config['p1_face_x'] = int(p1_face_offset.group(1))
        config['p1_face_y'] = int(p1_face_offset.group(2))

        p1_face_scale = re.search(r'p1\.face\.scale\s*=\s*([\d.]+)\s*,\s*([\d.]+)', content)
        config['p1_face_scale_x'] = float(p1_face_scale.group(1))
        config['p1_face_scale_y'] = float(p1_face_scale.group(2))

        # Portrait config P2
        p2_face_offset = re.search(r'p2\.face\.offset\s*=\s*(\d+)\s*,\s*(\d+)', content)
        config['p2_face_x'] = int(p2_face_offset.group(1))
        config['p2_face_y'] = int(p2_face_offset.group(2))

        p2_face_scale = re.search(r'p2\.face\.scale\s*=\s*([\d.]+)\s*,\s*([\d.]+)', content)
        config['p2_face_scale_x'] = float(p2_face_scale.group(1))
        config['p2_face_scale_y'] = float(p2_face_scale.group(2))

        # Name config P1
        p1_name_offset = re.search(r'p1\.name\.offset\s*=\s*(\d+)\s*,\s*(\d+)', content)
        config['p1_name_x'] = int(p1_name_offset.group(1))
        config['p1_name_y'] = int(p1_name_offset.group(2))

        # Name config P2
        p2_name_offset = re.search(r'p2\.name\.offset\s*=\s*(\d+)\s*,\s*(\d+)', content)
        config['p2_name_x'] = int(p2_name_offset.group(1))
        config['p2_name_y'] = int(p2_name_offset.group(2))

        return config

    def count_characters(self):
        """Compte le nombre de personnages dans select.def"""
        content = self.select_def.read_text(encoding='utf-8', errors='ignore')

        count = 0
        in_characters = False

        for line in content.split('\n'):
            line = line.strip()
            if line == '[Characters]':
                in_characters = True
                continue
            elif line.startswith('[') and in_characters:
                break
            elif in_characters and line and not line.startswith(';'):
                char_name = line.split(',')[0].strip()
                if char_name:
                    count += 1

        return count

    def generate_visual_html(self, config, char_count):
        """Génère le HTML de visualisation"""

        # Calculs
        portrait_w = int(100 * config['p1_face_scale_x'])
        portrait_h = int(100 * config['p1_face_scale_y'])

        grid_w = config['columns'] * (config['cell_w'] + config['cell_spacing'])
        grid_h = config['rows'] * (config['cell_h'] + config['cell_spacing'])

        total_slots = config['rows'] * config['columns']
        empty_slots = total_slots - char_count

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visual Select Screen - KOF Ultimate</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #1a1a2e;
            color: #fff;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 20px;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 20px;
            color: #4a90e2;
        }}
        .screen {{
            position: relative;
            width: 640px;
            height: 480px;
            margin: 20px auto;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            border: 2px solid #4a90e2;
            overflow: hidden;
        }}
        .portrait {{
            position: absolute;
            background: radial-gradient(circle, #ff6b6b 0%, #c92a2a 100%);
            border: 3px solid #fff;
            border-radius: 5px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
            text-shadow: 1px 1px 2px #000;
            z-index: 2;
        }}
        .name-box {{
            position: absolute;
            background: rgba(255,255,255,0.9);
            color: #000;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 12px;
            text-align: center;
            z-index: 3;
        }}
        .grid {{
            position: absolute;
            background: rgba(100,100,100,0.3);
            border: 2px solid rgba(255,255,255,0.3);
            z-index: 1;
        }}
        .cell {{
            position: absolute;
            background: rgba(100,150,200,0.4);
            border: 1px solid rgba(255,255,255,0.3);
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .stat-box {{
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #4a90e2;
        }}
        .stat-label {{
            color: #aaa;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}
        .stat-value {{
            font-size: 1.5em;
            font-weight: bold;
        }}
        .issue {{
            background: rgba(255,100,100,0.2);
            border-left: 4px solid #ff6b6b;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }}
        .success {{
            background: rgba(100,255,100,0.2);
            border-left: 4px solid #51cf66;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }}
        .warning {{
            background: rgba(255,200,100,0.2);
            border-left: 4px solid #ffa500;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Visual Select Screen Checker</h1>
        <div class="subtitle" style="text-align: center; color: #aaa; margin-bottom: 20px;">
            KOF Ultimate Online - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </div>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-label">Grille</div>
                <div class="stat-value">{config['rows']}×{config['columns']}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Total Slots</div>
                <div class="stat-value">{total_slots}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Personnages</div>
                <div class="stat-value">{char_count}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Cases Vides</div>
                <div class="stat-value">{empty_slots}</div>
            </div>
        </div>

        <h2 style="margin: 20px 0;">Rendu Visuel (640×480)</h2>
        <div class="screen">
            <!-- P1 Portrait -->
            <div class="portrait" style="left: {config['p1_face_x']}px; top: {config['p1_face_y']}px; width: {portrait_w}px; height: {portrait_h}px;">
                P1
            </div>

            <!-- P2 Portrait -->
            <div class="portrait" style="left: {config['p2_face_x']}px; top: {config['p2_face_y']}px; width: {portrait_w}px; height: {portrait_h}px;">
                P2
            </div>

            <!-- P1 Name -->
            <div class="name-box" style="left: {config['p1_name_x']}px; top: {config['p1_name_y']}px;">
                Player 1 Name
            </div>

            <!-- P2 Name -->
            <div class="name-box" style="left: {config['p2_name_x']}px; top: {config['p2_name_y']}px;">
                Player 2 Name
            </div>

            <!-- Grid -->
            <div class="grid" style="left: {config['grid_x']}px; top: {config['grid_y']}px; width: {grid_w}px; height: {grid_h}px;">
"""

        # Ajouter les cellules de la grille
        for row in range(config['rows']):
            for col in range(config['columns']):
                cell_x = col * (config['cell_w'] + config['cell_spacing'])
                cell_y = row * (config['cell_h'] + config['cell_spacing'])

                html += f"""                <div class="cell" style="left: {cell_x}px; top: {cell_y}px; width: {config['cell_w']}px; height: {config['cell_h']}px;"></div>
"""

        html += """            </div>
        </div>

        <h2 style="margin: 20px 0;">Analyse</h2>
"""

        # Vérifications
        issues = []
        successes = []
        warnings = []

        # Check 1: Portraits vs Grid overlap
        p1_bottom = config['p1_face_y'] + portrait_h
        p2_bottom = config['p2_face_y'] + portrait_h
        grid_top = config['grid_y']

        if p1_bottom > grid_top:
            issues.append(f"Portrait P1 chevauche la grille: bottom={p1_bottom}px, grid_top={grid_top}px (overlap de {p1_bottom - grid_top}px)")
        else:
            successes.append(f"Portrait P1 bien positionné: {grid_top - p1_bottom}px d'espace avant la grille")

        if p2_bottom > grid_top:
            issues.append(f"Portrait P2 chevauche la grille: bottom={p2_bottom}px, grid_top={grid_top}px (overlap de {p2_bottom - grid_top}px)")
        else:
            successes.append(f"Portrait P2 bien positionné: {grid_top - p2_bottom}px d'espace avant la grille")

        # Check 2: Names vs Grid overlap
        p1_name_bottom = config['p1_name_y'] + 20  # Estimated name height
        p2_name_bottom = config['p2_name_y'] + 20

        if p1_name_bottom > grid_top:
            issues.append(f"Nom P1 chevauche la grille: bottom={p1_name_bottom}px, grid_top={grid_top}px")
        else:
            successes.append(f"Nom P1 bien positionné: {grid_top - p1_name_bottom}px d'espace avant la grille")

        if p2_name_bottom > grid_top:
            issues.append(f"Nom P2 chevauche la grille: bottom={p2_name_bottom}px, grid_top={grid_top}px")
        else:
            successes.append(f"Nom P2 bien positionné: {grid_top - p2_name_bottom}px d'espace avant la grille")

        # Check 3: Grid bottom vs screen
        grid_bottom = config['grid_y'] + grid_h
        screen_height = 480

        if grid_bottom > screen_height:
            issues.append(f"Grille dépasse l'écran: bottom={grid_bottom}px, screen={screen_height}px (dépasse de {grid_bottom - screen_height}px)")
        else:
            successes.append(f"Grille rentre dans l'écran: {screen_height - grid_bottom}px restants")

        # Check 4: Empty slots
        if empty_slots > 0:
            warnings.append(f"{empty_slots} cases vides dans la grille ({empty_slots}/{total_slots} = {100*empty_slots/total_slots:.1f}%)")
        else:
            successes.append(f"Grille parfaitement remplie: {char_count} personnages pour {total_slots} slots")

        # Display issues
        for issue in issues:
            html += f"""        <div class="issue">❌ {issue}</div>
"""

        for success in successes:
            html += f"""        <div class="success">✓ {success}</div>
"""

        for warning in warnings:
            html += f"""        <div class="warning">⚠️ {warning}</div>
"""

        html += """
        <h2 style="margin: 20px 0;">Coordonnées Détaillées</h2>
        <div class="stats">
            <div class="stat-box">
                <div class="stat-label">Portrait P1</div>
                <div class="stat-value" style="font-size: 1em;">
                    X={config['p1_face_x']}, Y={config['p1_face_y']}<br>
                    Size={portrait_w}×{portrait_h}px<br>
                    Bottom={p1_bottom}px
                </div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Portrait P2</div>
                <div class="stat-value" style="font-size: 1em;">
                    X={config['p2_face_x']}, Y={config['p2_face_y']}<br>
                    Size={portrait_w}×{portrait_h}px<br>
                    Bottom={p2_bottom}px
                </div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Grille</div>
                <div class="stat-value" style="font-size: 1em;">
                    X={config['grid_x']}, Y={config['grid_y']}<br>
                    Size={grid_w}×{grid_h}px<br>
                    Bottom={grid_bottom}px
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

        return html

    def run(self):
        """Exécute le checker visuel"""
        print("\n" + "="*70)
        print("  🎨 VISUAL SELECT SCREEN CHECKER")
        print("="*70 + "\n")

        # Parse config
        print("Lecture de system.def...")
        config = self.parse_system_def()

        print("Comptage des personnages...")
        char_count = self.count_characters()

        print("Génération du rendu visuel...")
        html = self.generate_visual_html(config, char_count)

        # Save HTML
        output_file = self.base_path / "VISUAL_SELECT_SCREEN.html"
        output_file.write_text(html, encoding='utf-8')

        print(f"\n✓ Rendu visuel généré: {output_file}")
        print("\n" + "="*70)
        print("  Ouvrez VISUAL_SELECT_SCREEN.html pour voir le rendu!")
        print("="*70 + "\n")

        return output_file

if __name__ == "__main__":
    checker = VisualSelectScreenChecker()
    checker.run()
