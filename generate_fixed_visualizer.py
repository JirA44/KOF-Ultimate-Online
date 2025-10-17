# -*- coding: utf-8 -*-
"""
Génère un visualiseur HTML avec données embarquées (pas de fetch/CORS)
"""

import os
import json
from pathlib import Path

def load_all_characters():
    """Charge tous les personnages depuis INDEX.md"""
    base_dir = Path(r'D:\KOF Ultimate Online Online Online')
    index_file = base_dir / 'FICHES_PERSONNAGES' / 'INDEX.md'

    characters = []

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse l'index
    for line in content.split('\n'):
        if line.startswith('- [') and '.md)' in line:
            try:
                # Extrait nom, fichier, et nombre de techniques
                # Format: - [Name](file.md) - XX techniques
                parts = line.split('](')
                if len(parts) < 2:
                    continue

                name = parts[0].replace('- [', '').strip()
                rest = parts[1]

                filename = rest.split(')')[0].strip()

                # Extrait le nombre de techniques
                tech_count = '0'
                if '- ' in rest and 'techniques' in rest:
                    try:
                        tech_part = rest.split('- ')[1].split(' techniques')[0].strip()
                        tech_count = tech_part
                    except:
                        tech_count = '0'
            except Exception as e:
                print(f"Erreur parsing ligne: {line[:50]}")
                continue

            # Charge la fiche complète
            fiche_path = base_dir / 'FICHES_PERSONNAGES' / filename

            character_data = {
                'name': name,
                'file': filename,
                'techniqueCount': int(tech_count),
                'moves': {
                    'supers': [],
                    'specials': [],
                    'throws': [],
                    'other': []
                }
            }

            if fiche_path.exists():
                with open(fiche_path, 'r', encoding='utf-8') as cf:
                    fiche_content = cf.read()

                # Parse la fiche
                current_section = None
                current_move = None

                for fiche_line in fiche_content.split('\n'):
                    # Détecte les sections
                    if '## 🔥 SUPER MOVES' in fiche_line:
                        current_section = 'supers'
                    elif '## ⚡ COUPS SPÉCIAUX' in fiche_line:
                        current_section = 'specials'
                    elif '## 🤜 PROJECTIONS' in fiche_line:
                        current_section = 'throws'
                    elif '## 🎯 AUTRES' in fiche_line:
                        current_section = 'other'

                    # Détecte les noms de moves
                    if fiche_line.startswith('### '):
                        if current_move and current_section:
                            character_data['moves'][current_section].append(current_move)

                        current_move = {
                            'name': fiche_line.replace('### ', '').strip(),
                            'command': ''
                        }

                    # Détecte les commandes
                    if fiche_line.startswith('**Commande**: ') and current_move:
                        current_move['command'] = fiche_line.replace('**Commande**: ', '').replace('`', '').strip()

                # Ajoute le dernier move
                if current_move and current_section:
                    character_data['moves'][current_section].append(current_move)

            characters.append(character_data)

    return characters

def generate_html(characters):
    """Génère le HTML avec données embarquées"""

    # Convertit en JSON
    characters_json = json.dumps(characters, ensure_ascii=False, indent=2)

    html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOF Ultimate Online - Guide des Personnages</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            min-height: 100vh;
        }}

        .header {{
            background: linear-gradient(135deg, #e94560 0%, #c72c41 100%);
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }}

        .header h1 {{
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            margin-bottom: 10px;
        }}

        .status-bar {{
            background: rgba(78, 204, 163, 0.2);
            padding: 10px;
            text-align: center;
            font-weight: bold;
            color: #4ecca3;
        }}

        .search-bar {{
            margin: 20px auto;
            max-width: 600px;
            padding: 0 20px;
        }}

        .search-bar input {{
            width: 100%;
            padding: 15px;
            font-size: 1.1em;
            border: none;
            border-radius: 10px;
            background: rgba(255,255,255,0.1);
            color: #fff;
            backdrop-filter: blur(10px);
        }}

        .search-bar input::placeholder {{
            color: rgba(255,255,255,0.6);
        }}

        .container {{
            display: flex;
            min-height: calc(100vh - 250px);
        }}

        .character-list {{
            width: 300px;
            background: rgba(0,0,0,0.3);
            padding: 20px;
            overflow-y: auto;
            border-right: 2px solid rgba(233, 69, 96, 0.5);
        }}

        .character-item {{
            padding: 15px;
            margin: 10px 0;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            border-left: 4px solid transparent;
        }}

        .character-item:hover {{
            background: rgba(233, 69, 96, 0.3);
            border-left-color: #e94560;
            transform: translateX(5px);
        }}

        .character-item.active {{
            background: rgba(233, 69, 96, 0.5);
            border-left-color: #e94560;
        }}

        .character-name {{
            font-weight: bold;
            font-size: 1.1em;
        }}

        .technique-count {{
            font-size: 0.9em;
            color: rgba(255,255,255,0.7);
            margin-top: 5px;
        }}

        .character-details {{
            flex: 1;
            padding: 30px;
            overflow-y: auto;
        }}

        .detail-header {{
            background: linear-gradient(135deg, rgba(233, 69, 96, 0.3) 0%, rgba(199, 44, 65, 0.3) 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            border: 2px solid rgba(233, 69, 96, 0.5);
        }}

        .detail-header h2 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .section {{
            background: rgba(0,0,0,0.3);
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
            border-left: 4px solid #e94560;
        }}

        .section-title {{
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #e94560;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .move {{
            background: rgba(255,255,255,0.05);
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }}

        .move:hover {{
            background: rgba(233, 69, 96, 0.2);
            transform: scale(1.02);
        }}

        .move-name {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #fff;
        }}

        .move-command {{
            font-size: 1.2em;
            font-family: 'Courier New', monospace;
            background: rgba(0,0,0,0.5);
            padding: 12px;
            border-radius: 6px;
            display: inline-block;
            color: #4ecca3;
        }}

        .button {{
            display: inline-block;
            padding: 5px 12px;
            margin: 2px;
            background: #e94560;
            border-radius: 5px;
            font-weight: bold;
            font-size: 0.9em;
        }}

        .direction {{
            display: inline-block;
            padding: 5px 12px;
            margin: 2px;
            background: #4ecca3;
            border-radius: 5px;
            font-weight: bold;
            color: #000;
            font-size: 1.1em;
        }}

        .legend {{
            background: rgba(0,0,0,0.5);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}

        .legend-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .empty-state {{
            text-align: center;
            padding: 50px;
            color: rgba(255,255,255,0.5);
        }}

        .combo-box {{
            background: linear-gradient(135deg, rgba(78, 204, 163, 0.1) 0%, rgba(78, 204, 163, 0.05) 100%);
            border: 2px solid #4ecca3;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }}

        .combo-title {{
            color: #4ecca3;
            font-weight: bold;
            margin-bottom: 10px;
        }}

        ::-webkit-scrollbar {{
            width: 10px;
        }}

        ::-webkit-scrollbar-track {{
            background: rgba(0,0,0,0.3);
        }}

        ::-webkit-scrollbar-thumb {{
            background: #e94560;
            border-radius: 5px;
        }}

        @media (max-width: 768px) {{
            .container {{
                flex-direction: column;
            }}

            .character-list {{
                width: 100%;
                max-height: 200px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🥋 KOF ULTIMATE ONLINE</h1>
        <p>Guide Interactif des Personnages</p>
    </div>

    <div class="status-bar">
        ✅ Version Corrigée - Données Embarquées - {len(characters)} Personnages Chargés
    </div>

    <div class="search-bar">
        <input type="text" id="searchInput" placeholder="🔍 Rechercher un personnage...">
    </div>

    <div class="container">
        <div class="character-list" id="characterList">
            <!-- Liste générée dynamiquement -->
        </div>

        <div class="character-details" id="characterDetails">
            <div class="empty-state">
                <h2>👈 Sélectionnez un personnage</h2>
                <p>Choisissez un personnage dans la liste pour voir ses coups et combos</p>
            </div>
        </div>
    </div>

    <script>
        // Données embarquées (pas de fetch/CORS)
        const characters = {characters_json};

        function renderCharacterList() {{
            const listContainer = document.getElementById('characterList');
            listContainer.innerHTML = '';

            characters.forEach((char, index) => {{
                const div = document.createElement('div');
                div.className = 'character-item';
                div.innerHTML = `
                    <div class="character-name">${{char.name}}</div>
                    <div class="technique-count">⚡ ${{char.techniqueCount}} techniques</div>
                `;
                div.onclick = () => loadCharacter(char, div);
                listContainer.appendChild(div);
            }});
        }}

        function loadCharacter(char, element) {{
            // Marque comme actif
            document.querySelectorAll('.character-item').forEach(el => el.classList.remove('active'));
            element.classList.add('active');

            displayCharacterDetails(char);
        }}

        function displayCharacterDetails(char) {{
            const detailsContainer = document.getElementById('characterDetails');

            let html = `
                <div class="detail-header">
                    <h2>${{char.name}}</h2>
                    <p>⚡ ${{char.techniqueCount}} techniques disponibles</p>
                </div>

                <div class="legend">
                    <h3>🎮 Légende des Commandes</h3>
                    <div class="legend-grid">
                        <div class="legend-item">
                            <span class="direction">→</span> Avant (F)
                        </div>
                        <div class="legend-item">
                            <span class="direction">←</span> Arrière (B)
                        </div>
                        <div class="legend-item">
                            <span class="direction">↓</span> Bas (D)
                        </div>
                        <div class="legend-item">
                            <span class="direction">↑</span> Haut (U)
                        </div>
                        <div class="legend-item">
                            <span class="button">A</span> Light Punch
                        </div>
                        <div class="legend-item">
                            <span class="button">B</span> Medium Punch
                        </div>
                        <div class="legend-item">
                            <span class="button">C</span> Heavy Punch
                        </div>
                        <div class="legend-item">
                            <span class="button">X</span> Light Kick
                        </div>
                        <div class="legend-item">
                            <span class="button">Y</span> Medium Kick
                        </div>
                        <div class="legend-item">
                            <span class="button">Z</span> Heavy Kick
                        </div>
                    </div>
                </div>
            `;

            // Supers
            if (char.moves.supers && char.moves.supers.length > 0) {{
                html += `
                    <div class="section">
                        <div class="section-title">🔥 SUPER MOVES / DESPERATION MOVES</div>
                        ${{char.moves.supers.map(move => `
                            <div class="move">
                                <div class="move-name">${{move.name}}</div>
                                <div class="move-command">${{formatCommand(move.command)}}</div>
                            </div>
                        `).join('')}}
                    </div>
                `;
            }}

            // Specials
            if (char.moves.specials && char.moves.specials.length > 0) {{
                html += `
                    <div class="section">
                        <div class="section-title">⚡ COUPS SPÉCIAUX</div>
                        ${{char.moves.specials.map(move => `
                            <div class="move">
                                <div class="move-name">${{move.name}}</div>
                                <div class="move-command">${{formatCommand(move.command)}}</div>
                            </div>
                        `).join('')}}
                    </div>
                `;
            }}

            // Throws
            if (char.moves.throws && char.moves.throws.length > 0) {{
                html += `
                    <div class="section">
                        <div class="section-title">🤜 PROJECTIONS</div>
                        ${{char.moves.throws.map(move => `
                            <div class="move">
                                <div class="move-name">${{move.name}}</div>
                                <div class="move-command">${{formatCommand(move.command)}}</div>
                            </div>
                        `).join('')}}
                    </div>
                `;
            }}

            // Combos
            html += `
                <div class="section">
                    <div class="section-title">💥 COMBOS SUGGÉRÉS</div>
                    <div class="combo-box">
                        <div class="combo-title">Combo 1 - Basic</div>
                        <div class="move-command">LP → MP → HP → Special Move</div>
                    </div>
                    <div class="combo-box">
                        <div class="combo-title">Combo 2 - Jumping</div>
                        <div class="move-command">Jump HK → LP → MP → Special Move</div>
                    </div>
                    <div class="combo-box">
                        <div class="combo-title">Combo 3 - Super Finish</div>
                        <div class="move-command">LP → MP → HP → Super Move</div>
                    </div>
                </div>
            `;

            detailsContainer.innerHTML = html;
            detailsContainer.scrollTop = 0;
        }}

        function formatCommand(command) {{
            if (!command) return '';

            let formatted = command;

            // Directions
            formatted = formatted.replace(/→/g, '<span class="direction">→</span>');
            formatted = formatted.replace(/←/g, '<span class="direction">←</span>');
            formatted = formatted.replace(/↓/g, '<span class="direction">↓</span>');
            formatted = formatted.replace(/↑/g, '<span class="direction">↑</span>');
            formatted = formatted.replace(/↘/g, '<span class="direction">↘</span>');
            formatted = formatted.replace(/↙/g, '<span class="direction">↙</span>');
            formatted = formatted.replace(/↗/g, '<span class="direction">↗</span>');
            formatted = formatted.replace(/↖/g, '<span class="direction">↖</span>');

            // Boutons
            formatted = formatted.replace(/\\bA\\b/g, '<span class="button">A</span>');
            formatted = formatted.replace(/\\bB\\b/g, '<span class="button">B</span>');
            formatted = formatted.replace(/\\bC\\b/g, '<span class="button">C</span>');
            formatted = formatted.replace(/\\bX\\b/g, '<span class="button">X</span>');
            formatted = formatted.replace(/\\bY\\b/g, '<span class="button">Y</span>');
            formatted = formatted.replace(/\\bZ\\b/g, '<span class="button">Z</span>');

            return formatted;
        }}

        // Recherche
        document.getElementById('searchInput').addEventListener('input', function(e) {{
            const query = e.target.value.toLowerCase();
            const items = document.querySelectorAll('.character-item');

            items.forEach(item => {{
                const name = item.querySelector('.character-name').textContent.toLowerCase();
                if (name.includes(query)) {{
                    item.style.display = 'block';
                }} else {{
                    item.style.display = 'none';
                }}
            }});
        }});

        // Charge les données au démarrage
        renderCharacterList();
    </script>
</body>
</html>'''

    return html

def main():
    print("="*80)
    print("  GÉNÉRATION DU VISUALISEUR CORRIGÉ")
    print("="*80)
    print()

    print("📖 Chargement des personnages...")
    characters = load_all_characters()
    print(f"✓ {len(characters)} personnages chargés")

    print("\n🔨 Génération du HTML...")
    html = generate_html(characters)

    output_file = Path(r'D:\KOF Ultimate Online Online Online\VISUALISEUR_PERSONNAGES_FIXED.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Visualiseur généré: {output_file}")
    print(f"📦 Taille des données: {len(html) // 1024} KB")
    print()
    print("✓ Ce fichier fonctionne en local (pas de CORS/fetch)")
    print("✓ Toutes les données sont embarquées directement")
    print()
    print("Pour utiliser: Double-cliquez sur VISUALISEUR_PERSONNAGES_FIXED.html")

if __name__ == '__main__':
    main()
