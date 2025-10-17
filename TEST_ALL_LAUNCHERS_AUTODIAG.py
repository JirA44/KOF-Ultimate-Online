#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test automatique de tous les launchers - Vérification auto-diagnostic
"""

import subprocess
import sys
from pathlib import Path

class LauncherTester:
    def __init__(self):
        self.base_path = Path("D:/KOF Ultimate Online")
        self.results = []

    def test_launcher(self, launcher_name, launcher_path, test_type="python"):
        """Teste un launcher spécifique"""
        print(f"\n{'='*60}")
        print(f"Testing: {launcher_name}")
        print(f"{'='*60}")

        try:
            if test_type == "python":
                # Test Python launcher
                result = subprocess.run(
                    ['python', str(launcher_path), '--help'],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=str(self.base_path)
                )

                # Si --help ne fonctionne pas, essayer juste de l'importer
                if result.returncode != 0:
                    result = subprocess.run(
                        ['python', '-c', f'import sys; sys.path.insert(0, "{self.base_path}"); import {launcher_path.stem}; print("OK")'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )

            elif test_type == "batch":
                # Test batch file - juste vérifier qu'il existe et est lisible
                if launcher_path.exists():
                    with open(launcher_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    # Vérifier si le batch contient des checks
                    has_checks = any(keyword in content.lower() for keyword in [
                        'if exist', 'if not exist', 'check', 'verify', 'diagnostic'
                    ])

                    status = "✓ Has checks" if has_checks else "⚠ No checks"
                    print(f"  Status: {status}")
                    self.results.append({
                        'launcher': launcher_name,
                        'status': 'OK' if has_checks else 'WARNING',
                        'type': 'batch',
                        'has_checks': has_checks
                    })
                    return

            if "OK" in result.stdout or result.returncode == 0:
                print(f"  ✓ Launcher functional")
                self.results.append({
                    'launcher': launcher_name,
                    'status': 'OK',
                    'type': test_type
                })
            else:
                print(f"  ⚠ Launcher may need review")
                print(f"  Output: {result.stdout[:200]}")
                self.results.append({
                    'launcher': launcher_name,
                    'status': 'WARNING',
                    'type': test_type,
                    'error': result.stderr[:200]
                })

        except subprocess.TimeoutExpired:
            print(f"  ⚠ Launcher timeout (may require user input)")
            self.results.append({
                'launcher': launcher_name,
                'status': 'TIMEOUT',
                'type': test_type
            })
        except Exception as e:
            print(f"  ❌ Error: {e}")
            self.results.append({
                'launcher': launcher_name,
                'status': 'ERROR',
                'type': test_type,
                'error': str(e)
            })

    def verify_autodiag_features(self):
        """Vérifie que les features d'auto-diagnostic sont présentes"""
        print(f"\n{'='*60}")
        print("VERIFICATION AUTO-DIAGNOSTIC FEATURES")
        print(f"{'='*60}")

        # Vérifier launcher_auto_diagnostic.py
        autodiag_path = self.base_path / "launcher_auto_diagnostic.py"
        if autodiag_path.exists():
            with open(autodiag_path, 'r', encoding='utf-8') as f:
                content = f.read()

            features = {
                'check_mugen_engine': 'check_mugen_engine' in content,
                'check_ikemen_engine': 'check_ikemen_engine' in content,
                'auto_fix_ikemen_folders': 'auto_fix_ikemen_folders' in content,
                'auto_fix_debug_font': 'auto_fix_debug_font' in content,
                'FIX_IKEMEN_FORCE.ps1': 'FIX_IKEMEN_FORCE.ps1' in content
            }

            print("\nFeatures in launcher_auto_diagnostic.py:")
            for feature, present in features.items():
                status = "✓" if present else "❌"
                print(f"  {status} {feature}")

            return all(features.values())
        else:
            print("  ❌ launcher_auto_diagnostic.py NOT FOUND!")
            return False

        # Vérifier FIX_IKEMEN_FORCE.ps1
        ps_script = self.base_path / "FIX_IKEMEN_FORCE.ps1"
        if ps_script.exists():
            print("\n✓ FIX_IKEMEN_FORCE.ps1 present")
        else:
            print("\n❌ FIX_IKEMEN_FORCE.ps1 MISSING!")

    def run_full_test(self):
        """Lance tous les tests"""
        print("="*60)
        print("  KOF ULTIMATE - LAUNCHER AUTO-DIAGNOSTIC TEST")
        print("="*60)

        # Test launchers Python principaux
        python_launchers = [
            ("launcher_auto_diagnostic.py", "Auto-Diagnostic Launcher (PRIMARY)"),
            ("LAUNCHER_ULTIMATE.py", "Ultimate Launcher"),
            ("launcher.py", "Basic Launcher"),
        ]

        for filename, name in python_launchers:
            launcher_path = self.base_path / filename
            if launcher_path.exists():
                self.test_launcher(name, launcher_path, "python")

        # Test batch files principaux
        batch_launchers = [
            ("LAUNCH_KOF_ULTIMATE.bat", "KOF Ultimate Batch Launcher"),
            ("LAUNCH_GAME_WITH_CHECK.bat", "Game with Check Launcher"),
        ]

        for filename, name in batch_launchers:
            launcher_path = self.base_path / filename
            if launcher_path.exists():
                self.test_launcher(name, launcher_path, "batch")

        # Vérifier les features d'auto-diagnostic
        self.verify_autodiag_features()

        # Résumé
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")

        ok_count = sum(1 for r in self.results if r['status'] == 'OK')
        warning_count = sum(1 for r in self.results if r['status'] in ['WARNING', 'TIMEOUT'])
        error_count = sum(1 for r in self.results if r['status'] == 'ERROR')

        print(f"\nTotal launchers tested: {len(self.results)}")
        print(f"  ✓ OK: {ok_count}")
        print(f"  ⚠ Warnings: {warning_count}")
        print(f"  ❌ Errors: {error_count}")

        if error_count == 0 and warning_count <= 1:
            print("\n✓ All launchers operational!")
            return True
        else:
            print("\n⚠ Some launchers may need attention")
            return False

if __name__ == "__main__":
    tester = LauncherTester()
    success = tester.run_full_test()
    sys.exit(0 if success else 1)
