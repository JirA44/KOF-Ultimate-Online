#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNOSE AND FIX PORTRAITS - KOF ULTIMATE
Analyse et corrige automatiquement l'affichage des portraits sur l'écran de sélection
"""

import os
import sys
import re
import shutil
from pathlib import Path
from datetime import datetime

class PortraitDiagnostic:
    def __init__(self):
        self.base_path = Path(r"D:\KOF Ultimate Online")
        self.system_def = self.base_path / "data" / "system.def"
        self.issues = []
        self.fixes = []

    def log(self, message, level="INFO"):
        """Affiche un message avec niveau"""
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✓",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "FIX": "🔧"
        }
        icon = icons.get(level, "•")
        print(f"{icon} {message}")

    def analyze_current_config(self):
        """Analyse la configuration actuelle"""
        self.log("Analyse de la configuration actuelle...", "INFO")

        if not self.system_def.exists():
            self.log(f"Fichier system.def non trouvé: {self.system_def}", "ERROR")
            return None

        content = self.system_def.read_text(encoding='utf-8', errors='ignore')

        # Extraire les paramètres de Select Info
        config = {}

        # Grid configuration
        if m := re.search(r'rows\s*=\s*(\d+)', content):
            config['rows'] = int(m.group(1))
        if m := re.search(r'columns\s*=\s*(\d+)', content):
            config['columns'] = int(m.group(1))
        if m := re.search(r'cell\.size\s*=\s*(\d+),(\d+)', content):
            config['cell_width'] = int(m.group(1))
            config['cell_height'] = int(m.group(2))
        if m := re.search(r'cell\.spacing\s*=\s*(\d+)', content):
            config['cell_spacing'] = int(m.group(1))
        if m := re.search(r'^pos\s*=\s*(\d+),(\d+)', content, re.MULTILINE):
            config['grid_x'] = int(m.group(1))
            config['grid_y'] = int(m.group(2))

        # Portrait configuration
        if m := re.search(r'portrait\.scale\s*=\s*([\d.]+),([\d.]+)', content):
            config['portrait_scale_x'] = float(m.group(1))
            config['portrait_scale_y'] = float(m.group(2))
        if m := re.search(r'portrait\.offset\s*=\s*([-\d]+),([-\d]+)', content):
            config['portrait_offset_x'] = int(m.group(1))
            config['portrait_offset_y'] = int(m.group(2))

        return config

    def diagnose_issues(self, config):
        """Diagnostique les problèmes de portrait"""
        self.log("\nDiagnostic des problèmes...", "INFO")

        if not config:
            return

        # Afficher config actuelle
        self.log(f"  Grille: {config.get('rows', '?')}×{config.get('columns', '?')}", "INFO")
        self.log(f"  Taille cellules: {config.get('cell_width', '?')}×{config.get('cell_height', '?')} px", "INFO")
        self.log(f"  Espacement: {config.get('cell_spacing', '?')} px", "INFO")
        self.log(f"  Échelle portraits: {config.get('portrait_scale_x', '?')}×{config.get('portrait_scale_y', '?')}", "INFO")
        self.log(f"  Position grille: ({config.get('grid_x', '?')}, {config.get('grid_y', '?')})", "INFO")

        # Détecter problèmes
        cell_w = config.get('cell_width', 34)
        cell_h = config.get('cell_height', 34)
        scale_x = config.get('portrait_scale_x', 1.0)
        scale_y = config.get('portrait_scale_y', 1.0)

        # Les portraits M.U.G.E.N standard font généralement ~100x100px
        # Avec échelle 1.0, ils font 100x100
        # Pour une cellule de 34x34, on a besoin d'une échelle de ~0.34

        ideal_scale_x = cell_w / 100.0
        ideal_scale_y = cell_h / 100.0

        if scale_x > ideal_scale_x * 1.2:
            issue = f"Portraits trop larges: échelle {scale_x} > idéal {ideal_scale_x:.2f}"
            self.issues.append(issue)
            self.log(f"  {issue}", "WARNING")

        if scale_y > ideal_scale_y * 1.2:
            issue = f"Portraits trop hauts: échelle {scale_y} > idéal {ideal_scale_y:.2f}"
            self.issues.append(issue)
            self.log(f"  {issue}", "WARNING")

        if cell_w < 30:
            issue = f"Cellules trop petites: {cell_w}px < 30px recommandé"
            self.issues.append(issue)
            self.log(f"  {issue}", "WARNING")

        grid_width = config.get('columns', 15) * (cell_w + config.get('cell_spacing', 2))
        if grid_width > 640:
            issue = f"Grille trop large: {grid_width}px > 640px écran"
            self.issues.append(issue)
            self.log(f"  {issue}", "WARNING")

        return len(self.issues) == 0

    def apply_optimal_portrait_config(self):
        """Applique une configuration optimale pour les portraits"""
        self.log("\nApplication de la configuration optimale...", "INFO")

        # Backup
        backup_file = self.system_def.with_suffix(f'.def.portrait_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        shutil.copy2(self.system_def, backup_file)
        self.log(f"  Backup créé: {backup_file.name}", "SUCCESS")

        content = self.system_def.read_text(encoding='utf-8', errors='ignore')

        # Configuration optimale pour portraits dans cellules 34×34
        # Portraits M.U.G.E.N standards = ~100×100px
        # Scale = cell_size / portrait_size = 34/100 = 0.34

        optimal_config = {
            'portrait.scale': '0.34,0.34',  # Scale pour que 100px → 34px
            'portrait.offset': '0,0',  # Centré
        }

        # Appliquer les modifications
        for key, value in optimal_config.items():
            pattern = re.compile(rf'^{re.escape(key)}\s*=.*$', re.MULTILINE)
            replacement = f'{key} = {value}'

            if pattern.search(content):
                content = pattern.sub(replacement, content)
                self.fixes.append(f"Modified {key} = {value}")
                self.log(f"  ✓ {key} = {value}", "FIX")
            else:
                # Ajouter après [Select Info] si absent
                select_info_pos = content.find('[Select Info]')
                if select_info_pos != -1:
                    # Trouver la fin de la ligne
                    next_line = content.find('\n', select_info_pos)
                    content = content[:next_line+1] + f'{key} = {value}\n' + content[next_line+1:]
                    self.fixes.append(f"Added {key} = {value}")
                    self.log(f"  ✓ Ajouté {key} = {value}", "FIX")

        # Sauvegarder
        self.system_def.write_text(content, encoding='utf-8')
        self.log(f"  ✓ Fichier sauvegardé: {self.system_def}", "SUCCESS")

    def generate_visual_report(self):
        """Génère un rapport visuel HTML"""
        self.log("\nGénération du rapport visuel...", "INFO")

        config = self.analyze_current_config()
        if not config:
            return

        html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diagnostic Portraits - KOF Ultimate</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #fff;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(0,0,0,0.4);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }}
        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        .subtitle {{
            text-align: center;
            color: #aaa;
            margin-bottom: 30px;
        }}
        .section {{
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .section h2 {{
            font-size: 1.8em;
            margin-bottom: 15px;
            border-bottom: 2px solid #4a90e2;
            padding-bottom: 10px;
        }}
        .grid-visual {{
            display: grid;
            grid-template-columns: repeat({config.get('columns', 15)}, {config.get('cell_width', 34)}px);
            grid-gap: {config.get('cell_spacing', 2)}px;
            margin: 20px auto;
            width: fit-content;
            padding: 10px;
            background: rgba(0,0,0,0.3);
            border-radius: 5px;
        }}
        .cell {{
            width: {config.get('cell_width', 34)}px;
            height: {config.get('cell_height', 34)}px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: 1px solid rgba(255,255,255,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            color: #fff;
            position: relative;
            overflow: hidden;
        }}
        .portrait-mock {{
            width: calc(100px * {config.get('portrait_scale_x', 1.0)});
            height: calc(100px * {config.get('portrait_scale_y', 1.0)});
            background: radial-gradient(circle, #ff6b6b 0%, #c92a2a 100%);
            border-radius: 50%;
            opacity: 0.7;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
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
        .fix {{
            background: rgba(100,255,100,0.2);
            border-left: 4px solid #51cf66;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }}
        .recommendation {{
            background: rgba(100,150,255,0.2);
            border-left: 4px solid #4a90e2;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Diagnostic Portraits</h1>
        <div class="subtitle">KOF Ultimate Online - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>

        <div class="section">
            <h2>📊 Configuration Actuelle</h2>
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-label">Grille</div>
                    <div class="stat-value">{config.get('rows', '?')}×{config.get('columns', '?')}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Taille Cellules</div>
                    <div class="stat-value">{config.get('cell_width', '?')}×{config.get('cell_height', '?')} px</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Espacement</div>
                    <div class="stat-value">{config.get('cell_spacing', '?')} px</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Échelle Portraits</div>
                    <div class="stat-value">{config.get('portrait_scale_x', '?')}×{config.get('portrait_scale_y', '?')}</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>🖼️ Aperçu Visuel (Première Ligne)</h2>
            <p style="margin-bottom: 10px; color: #aaa;">Les cercles rouges représentent les portraits à l'échelle actuelle</p>
            <div class="grid-visual">
                {''.join([f'<div class="cell"><div class="portrait-mock"></div></div>' for _ in range(config.get('columns', 15))])}
            </div>
        </div>

        <div class="section">
            <h2>⚠️ Problèmes Détectés</h2>
            {''.join([f'<div class="issue">❌ {issue}</div>' for issue in self.issues]) if self.issues else '<div class="fix">✓ Aucun problème détecté</div>'}
        </div>

        <div class="section">
            <h2>🔧 Corrections Appliquées</h2>
            {''.join([f'<div class="fix">✓ {fix}</div>' for fix in self.fixes]) if self.fixes else '<div>Aucune correction appliquée</div>'}
        </div>

        <div class="section">
            <h2>💡 Recommandations</h2>
            <div class="recommendation">
                <strong>Échelle Portraits Optimale:</strong><br>
                Pour des cellules de {config.get('cell_width', 34)}×{config.get('cell_height', 34)} px
                et des portraits de ~100×100 px (taille standard M.U.G.E.N),<br>
                l'échelle optimale est: <strong>0.34×0.34</strong>
            </div>
            <div class="recommendation">
                <strong>Taille Cellules Recommandée:</strong><br>
                Minimum: 30×30 px<br>
                Optimal: 34×34 px (configuration actuelle ✓)<br>
                Maximum: 40×40 px
            </div>
            <div class="recommendation">
                <strong>Espacement Recommandé:</strong><br>
                2-3 px pour éviter que les cellules se touchent (actuel: {config.get('cell_spacing', 2)} px ✓)
            </div>
        </div>
    </div>
</body>
</html>"""

        report_file = self.base_path / "PORTRAIT_DIAGNOSTIC_REPORT.html"
        report_file.write_text(html_content, encoding='utf-8')
        self.log(f"  ✓ Rapport créé: {report_file}", "SUCCESS")

        return report_file

    def run(self):
        """Exécute le diagnostic complet"""
        print("\n" + "="*60)
        print("  🎨 DIAGNOSE AND FIX PORTRAITS - KOF ULTIMATE")
        print("="*60 + "\n")

        # 1. Analyser
        config = self.analyze_current_config()
        if not config:
            self.log("Impossible d'analyser la configuration", "ERROR")
            return False

        # 2. Diagnostiquer
        is_ok = self.diagnose_issues(config)

        # 3. Corriger si problèmes
        if not is_ok:
            self.log("\n⚠️  Problèmes détectés!", "WARNING")
            user_input = input("\nAppliquer les corrections automatiquement? (o/N): ")
            if user_input.lower() in ['o', 'oui', 'y', 'yes']:
                self.apply_optimal_portrait_config()
            else:
                self.log("Corrections annulées par l'utilisateur", "INFO")
        else:
            self.log("\n✓ Configuration optimale!", "SUCCESS")

        # 4. Générer rapport
        report_file = self.generate_visual_report()

        # 5. Résumé
        print("\n" + "="*60)
        print("  📋 RÉSUMÉ")
        print("="*60)
        self.log(f"Problèmes détectés: {len(self.issues)}", "INFO")
        self.log(f"Corrections appliquées: {len(self.fixes)}", "INFO")
        self.log(f"Rapport visuel: {report_file}", "INFO")
        print("="*60 + "\n")

        return True

if __name__ == "__main__":
    diagnostic = PortraitDiagnostic()
    success = diagnostic.run()

    if success:
        print("\n✓ Diagnostic terminé avec succès!")
        print("\nOuvrez PORTRAIT_DIAGNOSTIC_REPORT.html pour voir le rapport visuel.")
    else:
        print("\n❌ Échec du diagnostic")
        sys.exit(1)
