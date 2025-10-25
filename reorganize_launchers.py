#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Réorganisation automatique des launchers v2.0
"""

import os
import shutil
from datetime import datetime

# Répertoire de base
BASE_DIR = r"D:\KOF Ultimate Online"
os.chdir(BASE_DIR)

# Timestamp pour backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = f"launchers_backup_{timestamp}"
archive_dir = "launchers_archive"

print("╔════════════════════════════════════════════════════════════════════╗")
print("║     🔄  RÉORGANISATION DES LAUNCHERS v2.0                          ║")
print("╚════════════════════════════════════════════════════════════════════╝")
print()

# Créer les dossiers
print("[1/4] Création des dossiers...")
os.makedirs(backup_dir, exist_ok=True)
os.makedirs(archive_dir, exist_ok=True)
print("  ✓ Dossiers créés")

# Définir les renommages
renames = {
    # CATÉGORIE 1: LAUNCHERS DE JEU
    "LANCER_JEU_SIMPLE.bat": "KOF-LAUNCHER-v2.0-SIMPLE.bat",
    "TEST_MINIMAL_10_PERSOS.bat": "KOF-LAUNCHER-v2.0-STABLE-10.bat",
    "PLAY.bat": "KOF-LAUNCHER-v2.0-QUICK.bat",
    "LAUNCHER_COMPLET.bat": "KOF-LAUNCHER-v2.0-FULL.bat",

    # CATÉGORIE 2: ONLINE MULTIPLAYER
    "START_MATCHMAKING_SYSTEM.bat": "KOF-ONLINE-v2.0-MATCHMAKING.bat",
    "START_SERVER.bat": "KOF-ONLINE-v2.0-SERVER.bat",
    "JOUER_CONTRE_IA_ONLINE.bat": "KOF-ONLINE-v2.0-VS-AI.bat",
    "LAUNCH_VIRTUAL_PLAYERS.bat": "KOF-ONLINE-v2.0-VIRTUAL-PLAYERS.bat",

    # CATÉGORIE 3: TESTS & DIAGNOSTIC
    "LANCER_TEST_EXHAUSTIF.bat": "KOF-TEST-v2.0-EXHAUSTIF.bat",
    "LANCER_AUTO_DIAGNOSTIC.bat": "KOF-TEST-v2.0-DIAGNOSTIC.bat",
    "CHECK_TEST_PROGRESS.bat": "KOF-TEST-v2.0-PROGRESS.bat",
    "RUN_AUTOCHECK.bat": "KOF-TEST-v2.0-AUTOCHECK.bat",

    # CATÉGORIE 4: RÉPARATION & MAINTENANCE
    "CORRIGER_CRASH.bat": "KOF-FIX-v2.0-CRASH.bat",
    "REPARER_JEU.bat": "KOF-FIX-v2.0-GENERAL.bat",
    "FIX_IKEMEN_GO.bat": "KOF-FIX-v2.0-IKEMEN.bat",
    "NETTOYER_PORTRAITS_CASSES.bat": "KOF-FIX-v2.0-PORTRAITS.bat",

    # CATÉGORIE 5: IA & AUTOMATION
    "LAUNCH_AI_MULTI_MODES.bat": "KOF-AI-v2.0-MULTI-MODES.bat",
    "LAUNCH_MULTIPLE_AI_PLAYERS.bat": "KOF-AI-v2.0-MULTI-PLAYERS.bat",
    "JOUER_LOCAL_VS_IA.bat": "KOF-AI-v2.0-LOCAL-VS.bat",

    # CATÉGORIE 6: MONITORING & RAPPORTS
    "OUVRIR_DASHBOARD.bat": "KOF-MONITOR-v2.0-DASHBOARD.bat",
    "VOIR_RAPPORTS_CONTINUS.bat": "KOF-MONITOR-v2.0-REPORTS.bat",

    # CATÉGORIE 7: CONTRÔLE & ARRÊT
    "STOP_ALL.bat": "KOF-CONTROL-v2.0-STOP-ALL.bat",
    "EMERGENCY_STOP.bat": "KOF-CONTROL-v2.0-EMERGENCY.bat",
}

# Fichiers à archiver
to_archive = [
    # Tests obsolètes
    "LANCER_TEST_MANUEL.bat", "LANCER_TEST_RAPIDE.bat", "LANCER_TEST_AUTO_FOCUS.bat",
    "LANCER_TEST_INJECTION.bat", "LANCER_TEST_JOUEURS.bat", "TEST_AUTO_SIMPLE.bat",
    "TEST_RAPIDE.bat", "TEST_ANIMATIONS.bat", "CONTINUOUS_MINI_TEST.bat",
    "TEST_CONTINU_MINI_VISIBLE.bat", "TEST_MINI_FENETRE_BOUCLE.bat",
    "LAUNCH_TESTS_SAFE.bat", "TEST_MANETTE.bat",

    # Réparation obsolète
    "AUTO_FIX.bat", "AUTOFIX_IKEMEN_NOW.bat", "FIX_GAME_NOW.bat",
    "REPARER_STAGES_IKEMEN.bat", "restore_original_config.bat",

    # IA obsolète
    "LAUNCH_ALL_AI_TESTS_SILENT.bat", "STOP_ALL_AI_TESTS.bat", "MONITOR_AI_LOGS.bat",

    # Monitoring obsolète
    "MONITOR_TESTS.bat", "START_MONITORING_ONLY.bat", "START_WITH_REPORTER.bat",
    "VOIR_DASHBOARD.bat", "VOIR_RAPPORT_PORTRAITS.bat", "VOIR_TESTS_EN_DIRECT.bat",
    "GENERATE_TEST_REPORT.bat",

    # Contrôle obsolète
    "ARRETER_TESTS_CONTINUS.bat", "DEMARRER_TESTS_CONTINUS.bat",

    # Installation obsolète
    "install_ikemen_go.bat", "INSTALL_MANETTE_VIRTUELLE.bat", "SETUP_AUTO_STARTUP.bat",
    "create_shortcuts.bat", "CREER_RACCOURCI_BUREAU.bat",

    # Autres obsolètes
    "START_KOF_ULTIMATE.bat", "LAUNCH_GAME.bat", "LAUNCH_WITH_MODE_SELECT.bat",
    "LANCER_JEU_AVEC_GUIDE.bat", "LANCER_MINI_FENETRE_CONTINUE.bat",
    "LANCER_MINI_FENETRE_SIMPLE.bat", "PLAY_MINI_WINDOW.bat",
    "VERIFIER_TOUT.bat", "PREUVE_SYSTEME.bat",
]

# Renommages
print()
print("[2/4] Renommage des fichiers essentiels...")
renamed_count = 0

for old_name, new_name in renames.items():
    if os.path.exists(old_name):
        # Backup
        try:
            shutil.copy2(old_name, os.path.join(backup_dir, old_name))
        except Exception as e:
            print(f"  ⚠ Backup failed for {old_name}: {e}")

        # Rename
        try:
            os.rename(old_name, new_name)
            print(f"  ✓ {old_name} → {new_name}")
            renamed_count += 1
        except Exception as e:
            print(f"  ❌ Failed to rename {old_name}: {e}")

print(f"  → {renamed_count} fichiers renommés")

# Archivage
print()
print("[3/4] Archivage des fichiers obsolètes...")
archived_count = 0

for filename in to_archive:
    if os.path.exists(filename):
        try:
            shutil.move(filename, os.path.join(archive_dir, filename))
            archived_count += 1
        except Exception as e:
            print(f"  ⚠ Failed to archive {filename}: {e}")

print(f"  ✓ {archived_count} fichiers archivés")

# Résumé
print()
print("[4/4] Génération du résumé...")

summary = f"""╔════════════════════════════════════════════════════════════════════╗
║                  ✅  RÉORGANISATION TERMINÉE                       ║
╚════════════════════════════════════════════════════════════════════╝

📊 Résumé:
• {renamed_count} fichiers renommés avec versioning v2.0
• {archived_count} fichiers archivés dans {archive_dir}/
• Backup créé dans {backup_dir}/

🎮 Nouveaux launchers:
• KOF-LAUNCHER-v2.0-MAIN.bat (launcher principal)
• KOF-ONLINE-v2.0-LOBBY.bat (lobby online)

📁 Structure:
  LAUNCHERS DE JEU:      4 fichiers
  ONLINE MULTIPLAYER:    5 fichiers (dont lobby)
  TESTS & DIAGNOSTIC:    4 fichiers
  RÉPARATION:           4 fichiers
  IA & AUTOMATION:      3 fichiers
  MONITORING:           2 fichiers
  CONTRÔLE:             2 fichiers

Pour lancer le jeu:
→ KOF-LAUNCHER-v2.0-MAIN.bat (recommandé)
→ KOF-LAUNCHER-v2.0-SIMPLE.bat (lancement direct)
→ KOF-LAUNCHER-v2.0-STABLE-10.bat (10 persos testés)

📖 Documentation complète:
→ GUIDE_LAUNCHERS_v2.0.md

Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

print(summary)

# Sauvegarder le résumé
with open("REORGANISATION_v2.0_RESUME.txt", "w", encoding="utf-8") as f:
    f.write(summary)

print("✓ Résumé sauvegardé dans REORGANISATION_v2.0_RESUME.txt")
print()
print("🎉 Réorganisation terminée avec succès!")
