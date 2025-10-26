#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST RAPIDE - Échantillon de personnages
Teste rapidement 10 personnages contre WhirlWind-Goenitz
"""
import subprocess
import time
import psutil
import shutil
from pathlib import Path

base_path = Path(r"D:\KOF Ultimate Online")
game_exe = base_path / "KOF_Ultimate_Online.exe"
select_def = base_path / "data" / "select.def"

# Backup original
backup = select_def.parent / "select.def.backup_quick"
if not backup.exists():
    shutil.copy(select_def, backup)

def kill_game():
    for proc in psutil.process_iter(['name']):
        try:
            name = proc.info['name'].lower()
            if 'kof' in name or 'mugen' in name or 'ikemen' in name:
                proc.kill()
        except:
            pass
    time.sleep(0.5)

def test_char(char_name):
    """Test un personnage contre WhirlWind-Goenitz"""
    print(f"\n🥊 {char_name} vs WhirlWind-Goenitz...", end=" ", flush=True)

    # Créer roster minimal
    content = f"""; Test roster
[Characters]
{char_name}, stages/Abyss-Rugal-Palace.def
WhirlWind-Goenitz, stages/Abyss-Rugal-Palace.def
"""
    with open(select_def, 'w', encoding='utf-8') as f:
        f.write(content)

    # Lancer le jeu
    kill_game()

    proc = subprocess.Popen(
        [str(game_exe)],
        cwd=str(base_path),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Attendre 12 secondes
    time.sleep(12)

    # Vérifier si toujours en cours
    if proc.poll() is None:
        proc.kill()
        print("✅ OK")
        return "OK"
    else:
        print("❌ CRASH")
        return "CRASH"

# Liste de personnages à tester
chars_to_test = [
    "Athena",
    "boss-orochi",
    "final-goenitz",
    "Viper",
    "Cronus",
    "Rose",
    "akuma",
    "Final-IGNIZ",
    "Clone Blood Rugal",
    "Valmar Rugal"
]

print("="*60)
print("🚀 TEST RAPIDE - ÉCHANTILLON DE 10 PERSONNAGES")
print("="*60)

safe = []
crashers = []

for char in chars_to_test:
    result = test_char(char)

    if result == "OK":
        safe.append(char)
    else:
        crashers.append(char)

# Restaurer roster
if backup.exists():
    shutil.copy(backup, select_def)

print("\n" + "="*60)
print("📊 RÉSULTATS")
print("="*60)

print(f"\n✅ SÛRS ({len(safe)}):")
for c in safe:
    print(f"   ✓ {c}")

print(f"\n❌ CRASHEURS ({len(crashers)}):")
for c in crashers:
    print(f"   ✗ {c}")

kill_game()
print("\n✅ Test terminé!")
