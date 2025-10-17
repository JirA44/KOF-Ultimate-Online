# -*- coding: utf-8 -*-
"""
Vérifie et corrige automatiquement les erreurs dans tous les fichiers .air
"""

import os
import re
import glob

def fix_air_file(file_path):
    """Corrige les erreurs courantes dans un fichier .air"""
    try:
        # Lit le fichier avec plusieurs encodages possibles
        content = None
        for encoding in ['utf-8', 'shift-jis', 'latin-1', 'cp1252']:
            try:
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    content = f.read()
                break
            except:
                continue

        if not content:
            return False, "Impossible de lire le fichier"

        original_content = content
        errors_fixed = []

        # Correction 1: Espaces dans les déclarations Clsn
        if re.search(r'Clsn[12] \[', content):
            content = re.sub(r'Clsn2 \[', 'Clsn2[', content)
            content = re.sub(r'Clsn1 \[', 'Clsn1[', content)
            errors_fixed.append("Espaces dans Clsn[] corrigés")

        # Correction 2: Clsn[X] sans déclaration préalable
        lines = content.split('\n')
        fixed_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]

            # Détecte une ligne Clsn1[X] ou Clsn2[X] sans déclaration
            if re.match(r'\s*Clsn[12]\[\d+\]\s*=', line):
                # Vérifie si la ligne précédente est une déclaration Clsn
                if i > 0:
                    prev_line = fixed_lines[-1] if fixed_lines else ""
                    if not re.match(r'\s*Clsn[12]:\s*\d+', prev_line):
                        # Manque une déclaration, on l'ajoute
                        clsn_type = line.strip()[:5]  # "Clsn1" ou "Clsn2"
                        fixed_lines.append(f"{clsn_type}: 1")
                        errors_fixed.append(f"Déclaration {clsn_type} ajoutée avant ligne {i+1}")

            fixed_lines.append(line)
            i += 1

        content = '\n'.join(fixed_lines)

        # Correction 3: Collision boxes invalides (même point)
        # Exemple: Clsn2[1] = -130, 13,-130, 13
        def fix_invalid_box(match):
            full = match.group(0)
            coords = match.group(1)
            parts = [x.strip() for x in coords.split(',')]
            if len(parts) == 4:
                x1, y1, x2, y2 = parts
                # Si c'est le même point, crée une box par défaut
                if x1 == x2 and y1 == y2:
                    errors_fixed.append(f"Collision box invalide corrigée: {coords}")
                    return f"Clsn{match.group(2)}[{match.group(3)}] = -30, -90, 30, 0"
            return full

        content = re.sub(r'Clsn([12])\[(\d+)\]\s*=\s*([^\n]+)',
                        lambda m: fix_invalid_box(m), content)

        # Sauvegarde si des corrections ont été faites
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, errors_fixed

        return False, []

    except Exception as e:
        return False, f"Erreur: {e}"

def main():
    """Fonction principale"""
    chars_dir = r'D:\KOF Ultimate Online\chars'

    print("🔍 Scan de tous les fichiers .air...")

    air_files = glob.glob(os.path.join(chars_dir, '**', '*.air'), recursive=True)

    print(f"📁 {len(air_files)} fichiers trouvés\n")

    fixed_count = 0
    error_count = 0

    for air_file in air_files:
        char_name = os.path.basename(os.path.dirname(air_file))
        fixed, result = fix_air_file(air_file)

        if fixed:
            fixed_count += 1
            print(f"✅ {char_name}")
            if isinstance(result, list):
                for err in result:
                    print(f"   - {err}")
        elif result and isinstance(result, str) and "Erreur" in result:
            error_count += 1
            print(f"❌ {char_name}: {result}")

    print(f"\n{'='*60}")
    print(f"✅ Fichiers corrigés: {fixed_count}")
    print(f"❌ Erreurs non corrigées: {error_count}")
    print(f"✔️  Fichiers OK: {len(air_files) - fixed_count - error_count}")

if __name__ == '__main__':
    main()
