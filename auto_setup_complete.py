"""
KOF Ultimate - Auto-Setup Complet
Installe TOUT automatiquement sans rien demander
"""

import os
import sys
import subprocess
from pathlib import Path

def silent_install(package):
    """Installe un package silencieusement"""
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", "-q", package],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except:
        return False

def check_and_install_all():
    """Vérifie et installe toutes les dépendances"""
    print("🔧 Auto-Setup KOF Ultimate...")
    print()

    packages = {
        'pillow': 'PIL',
        'pygame': 'pygame',
        'anthropic': 'anthropic',
        'pyautogui': 'pyautogui',
        'opencv-python': 'cv2',
        'numpy': 'numpy',
        'keyboard': 'keyboard',
        'mouse': 'mouse',
        'python-dotenv': 'dotenv',
        'requests': 'requests'
    }

    missing = []
    installed_now = []

    # Détecter les packages manquants
    for package, import_name in packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package)

    if not missing:
        print("✅ Toutes les dépendances sont déjà installées!")
        return True

    print(f"📦 Installation de {len(missing)} packages...")

    # Installer silencieusement
    for package in missing:
        print(f"   • {package}...", end=" ", flush=True)
        if silent_install(package):
            print("✓")
            installed_now.append(package)
        else:
            print("✗")

    print()
    if len(installed_now) == len(missing):
        print(f"✅ {len(installed_now)} packages installés avec succès!")
        return True
    else:
        print(f"⚠️  {len(installed_now)}/{len(missing)} packages installés")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("KOF ULTIMATE - AUTO-SETUP")
    print("=" * 60)
    print()

    if check_and_install_all():
        print()
        print("=" * 60)
        print("✨ Système prêt !")
        print()
        print("Pour lancer:")
        print("  Double-clic: launch_complete_system.bat")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("⚠️  Setup incomplet")
        print("Relancez ce script ou installez manuellement:")
        print("  pip install -r requirements_ai.txt")
        print("=" * 60)
