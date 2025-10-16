"""
KOF Ultimate - Lanceur en Mode Fenêtré
Lance le jeu dans une fenêtre réduite pour le développement
"""
import subprocess
import sys
from pathlib import Path

def modify_config_for_windowed():
    """Modifie temporairement la config pour mode fenêtré"""
    config_file = Path(r"D:\KOF Ultimate\data\mugen.cfg")

    if not config_file.exists():
        print("❌ Fichier mugen.cfg non trouvé!")
        return False

    # Lire le fichier
    with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    # Modifier les paramètres
    modified_lines = []
    for line in lines:
        # Passer en mode fenêtré
        if line.strip().startswith('FullScreen'):
            modified_lines.append('FullScreen = 0\n')
        # Réduire la résolution
        elif line.strip().startswith('Width') and 'Video' in ''.join(modified_lines[-10:]):
            modified_lines.append('Width  = 800\n')
        elif line.strip().startswith('Height') and 'Video' in ''.join(modified_lines[-10:]):
            modified_lines.append('Height = 600\n')
        else:
            modified_lines.append(line)

    # Sauvegarder
    with open(config_file, 'w', encoding='utf-8') as f:
        f.writelines(modified_lines)

    print("✓ Configuration modifiée pour mode fenêtré (800x600)")
    return True

def launch_game():
    """Lance le jeu"""
    exe_path = Path(r"D:\KOF Ultimate\KOF BLACK R.exe")

    if not exe_path.exists():
        print("❌ Executable non trouvé!")
        return False

    print("▶ Lancement du jeu en mode fenêtré...")
    try:
        subprocess.Popen([str(exe_path)], cwd=str(exe_path.parent))
        print("✓ Jeu lancé avec succès!")
        print("ℹ Le jeu s'affiche maintenant dans une fenêtre réduite")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("🎮 KOF Ultimate - Lanceur Mode Fenêtré")
    print("=" * 50)

    if modify_config_for_windowed():
        launch_game()
    else:
        print("❌ Échec de la modification de la configuration")
        sys.exit(1)
