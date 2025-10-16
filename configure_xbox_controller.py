"""
Configuration Xbox Controller pour MUGEN
Configure directement en modifiant les lignes du fichier
"""

from pathlib import Path

CONFIG_FILE = Path("D:/KOF Ultimate/data/mugen.cfg")

def configure_xbox():
    """Configure la manette Xbox"""
    print("⚙️  Configuration Xbox Controller...")

    with open(CONFIG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    # Chercher et remplacer les sections joystick
    modified = []
    in_p1_joystick = False
    in_p2_joystick = False

    for line in lines:
        # Détecter les sections
        if '[P1 Joystick]' in line:
            in_p1_joystick = True
            in_p2_joystick = False
            modified.append(line)
            continue
        elif '[P2 Joystick]' in line:
            in_p1_joystick = False
            in_p2_joystick = True
            modified.append(line)
            continue
        elif line.strip().startswith('[') and line.strip().endswith(']'):
            in_p1_joystick = False
            in_p2_joystick = False
            modified.append(line)
            continue

        # Remplacer les configurations joystick
        if in_p1_joystick:
            if line.strip() and not line.strip().startswith(';'):
                # Configuration Xbox pour P1
                if 'Jump' in line:
                    modified.append('Jump   = ~0     ; D-Pad Up\n')
                elif 'Crouch' in line:
                    modified.append('Crouch = 0      ; D-Pad Down\n')
                elif 'Left' in line:
                    modified.append('Left   = ~1     ; D-Pad Left\n')
                elif 'Right' in line:
                    modified.append('Right  = 1      ; D-Pad Right\n')
                elif line.startswith('A '):
                    modified.append('A      = 0      ; Bouton A\n')
                elif line.startswith('B '):
                    modified.append('B      = 1      ; Bouton B\n')
                elif line.startswith('C '):
                    modified.append('C      = 3      ; Bouton Y\n')
                elif line.startswith('X '):
                    modified.append('X      = 0      ; Bouton A\n')
                elif line.startswith('Y '):
                    modified.append('Y      = 2      ; Bouton X\n')
                elif line.startswith('Z '):
                    modified.append('Z      = 4      ; LB\n')
                elif 'Start' in line:
                    modified.append('Start  = 7      ; Bouton Start\n')
                else:
                    modified.append(line)
            else:
                modified.append(line)
        elif in_p2_joystick:
            # Garder P2 tel quel pour l'instant
            modified.append(line)
        else:
            modified.append(line)

    # Sauvegarder
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        f.writelines(modified)

    print("✅ Configuration Xbox appliquée!")
    print()
    print("Mapping:")
    print("  Navigation: D-Pad ou Stick gauche")
    print("  Valider: Bouton A")
    print("  Annuler: Bouton B")
    print("  Start: Bouton Start")

if __name__ == "__main__":
    configure_xbox()
