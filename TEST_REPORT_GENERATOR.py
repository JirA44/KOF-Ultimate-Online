#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GÉNÉRATEUR DE RAPPORTS DE TESTS IA
Analyse tous les logs et génère un rapport HTML complet
"""
import os
import json
from datetime import datetime
from pathlib import Path

def generate_test_report():
    """Génère un rapport HTML complet des tests IA"""

    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport Tests IA - KOF Ultimate Online</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #fff;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }}
        h1 {{
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        .subtitle {{
            text-align: center;
            opacity: 0.8;
            margin-bottom: 30px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.15);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            transition: transform 0.3s;
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        .stat-value {{
            font-size: 3em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-label {{
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .section {{
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
        }}
        .section h2 {{
            border-bottom: 2px solid rgba(255,255,255,0.3);
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .log-entry {{
            background: rgba(0,0,0,0.3);
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        .success {{ color: #4ade80; }}
        .warning {{ color: #fbbf24; }}
        .error {{ color: #f87171; }}
        .info {{ color: #60a5fa; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        th {{
            background: rgba(255,255,255,0.2);
            font-weight: bold;
        }}
        .progress-bar {{
            width: 100%;
            height: 30px;
            background: rgba(0,0,0,0.3);
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #4ade80, #22c55e);
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 RAPPORT TESTS IA</h1>
        <div class="subtitle">KOF Ultimate Online - {report_time}</div>
"""

    # Statistiques globales
    total_matches = 0
    total_actions = 0
    total_time = 0
    modes_played = {}

    # Analyser les stats JSON
    ai_logs_dir = Path("ai_logs")
    if ai_logs_dir.exists():
        for stats_file in ai_logs_dir.glob("stats_player_*.json"):
            try:
                with open(stats_file, 'r') as f:
                    stats = json.load(f)
                    total_matches += stats.get('matches_played', 0)
                    for mode, count in stats.get('modes_played', {}).items():
                        modes_played[mode] = modes_played.get(mode, 0) + count
            except:
                pass

    # Compter les processus actifs
    import subprocess
    try:
        result = subprocess.run(['tasklist'], capture_output=True, text=True)
        active_processes = result.stdout.count('python.exe')
    except:
        active_processes = 0

    html += f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value success">{total_matches}</div>
                <div class="stat-label">Matches Joués</div>
            </div>
            <div class="stat-card">
                <div class="stat-value info">{len(modes_played)}</div>
                <div class="stat-label">Modes Testés</div>
            </div>
            <div class="stat-card">
                <div class="stat-value warning">{active_processes}</div>
                <div class="stat-label">IA Actives</div>
            </div>
        </div>
"""

    # Répartition par mode
    if modes_played:
        html += """
        <div class="section">
            <h2>📊 Répartition par Mode de Jeu</h2>
            <table>
                <tr>
                    <th>Mode</th>
                    <th>Matches</th>
                    <th>Progression</th>
                </tr>
"""
        max_matches = max(modes_played.values()) if modes_played else 1
        for mode, count in sorted(modes_played.items(), key=lambda x: x[1], reverse=True):
            percent = (count / max_matches) * 100
            html += f"""
                <tr>
                    <td>{mode.upper()}</td>
                    <td>{count}</td>
                    <td>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {percent}%">{percent:.1f}%</div>
                        </div>
                    </td>
                </tr>
"""
        html += """
            </table>
        </div>
"""

    # Logs récents
    html += """
        <div class="section">
            <h2>📝 Logs Récents</h2>
"""

    logs_dir = Path("logs")
    if logs_dir.exists():
        log_files = list(logs_dir.glob("*.log"))
        if log_files:
            # Prendre les 20 dernières lignes de chaque log
            for log_file in log_files[:3]:  # Max 3 fichiers
                html += f"<h3>{log_file.name}</h3>"
                try:
                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()[-20:]
                        for line in lines:
                            line = line.strip()
                            if not line:
                                continue

                            css_class = 'info'
                            if 'ERROR' in line or 'Erreur' in line:
                                css_class = 'error'
                            elif 'WARNING' in line or 'Attention' in line:
                                css_class = 'warning'
                            elif 'SUCCESS' in line or '✓' in line or '✅' in line:
                                css_class = 'success'

                            html += f'<div class="log-entry {css_class}">{line}</div>'
                except:
                    html += '<div class="log-entry error">Erreur de lecture du log</div>'
        else:
            html += '<div class="log-entry warning">Aucun log disponible</div>'
    else:
        html += '<div class="log-entry warning">Dossier logs introuvable</div>'

    html += """
        </div>

        <div class="section">
            <h2>✅ État du Système</h2>
            <table>
                <tr>
                    <th>Composant</th>
                    <th>État</th>
                </tr>
"""

    # Vérifier les composants
    components = {
        "AI_MULTI_MODE_SYSTEM.py": Path("AI_MULTI_MODE_SYSTEM.py").exists(),
        "AI_PLAYS_SILENT.py": Path("AI_PLAYS_SILENT.py").exists(),
        "ai_vs_ai_match.py": Path("ai_vs_ai_match.py").exists(),
        "virtual_players_ai.py": Path("virtual_players_ai.py").exists(),
        "Dossier logs/": logs_dir.exists(),
        "Dossier ai_logs/": ai_logs_dir.exists(),
    }

    for comp, exists in components.items():
        status = '<span class="success">✅ OK</span>' if exists else '<span class="error">❌ Manquant</span>'
        html += f"""
                <tr>
                    <td>{comp}</td>
                    <td>{status}</td>
                </tr>
"""

    html += """
            </table>
        </div>

        <div style="text-align: center; margin-top: 30px; opacity: 0.7;">
            <p>Généré automatiquement par TEST_REPORT_GENERATOR.py</p>
            <p>KOF Ultimate Online © 2025</p>
        </div>
    </div>
</body>
</html>
"""

    # Sauvegarder le rapport
    report_file = Path("test_results") / f"rapport_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    report_file.parent.mkdir(exist_ok=True)

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Rapport généré: {report_file}")
    return report_file

if __name__ == "__main__":
    os.chdir(r"D:\KOF Ultimate Online")
    report = generate_test_report()

    # Ouvrir le rapport
    import subprocess
    subprocess.Popen(['start', '', str(report)], shell=True)
