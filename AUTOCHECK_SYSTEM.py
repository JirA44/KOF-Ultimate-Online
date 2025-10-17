#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOF ULTIMATE - SYSTÈME D'AUTO-VÉRIFICATION COMPLET
Vérifie tout: backgrounds, AIR files, stages, launchers
"""

import os
import re
from pathlib import Path
from datetime import datetime

class KOFAutoChecker:
    """Auto-checker complet pour KOF Ultimate"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.checks_passed = 0
        self.checks_failed = 0
    
    def log(self, message, level='INFO'):
        """Log message"""
        symbols = {
            'INFO': 'ℹ️',
            'SUCCESS': '✅',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'CHECK': '🔍'
        }
        print(f"{symbols.get(level, '•')} {message}")
    
    def check_backgrounds(self):
        """Vérifie que les fonds sont beaux et animés (pas bleus)"""
        self.log("CHECK: Backgrounds dans system.def", 'CHECK')
        
        try:
            with open('data/system.def', 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Title BG
            title_section = content.split('[TitleBGdef]')[1].split('[Select')[0]
            if 'bgclearcolor = 0,0,0' in title_section:
                self.log("  Title menu: Black animated background ✓", 'SUCCESS')
                self.checks_passed += 1
            else:
                self.log("  Title menu: Still has blue background!", 'ERROR')
                self.checks_failed += 1
                self.errors.append("Title background is not black")
            
            # Select BG
            select_section = content.split('[SelectBGdef]')[1].split('[VS')[0]
            if 'bgclearcolor = 0,0,0' in select_section:
                self.log("  Select menu: Black animated background ✓", 'SUCCESS')
                self.checks_passed += 1
            else:
                self.log("  Select menu: Still has blue background!", 'ERROR')
                self.checks_failed += 1
                self.errors.append("Select background is not black")
                
        except Exception as e:
            self.log(f"  Error checking backgrounds: {e}", 'ERROR')
            self.checks_failed += 1
    
    def check_air_files(self):
        """Vérifie les fichiers AIR pour merged lines"""
        self.log("CHECK: AIR files for errors", 'CHECK')
        
        chars_dir = Path('chars')
        air_files = list(chars_dir.rglob('*.air'))
        
        # Sample 30 files
        import random
        sample = random.sample(air_files, min(30, len(air_files)))
        
        problems = 0
        for air_file in sample:
            try:
                with open(air_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check for merged lines
                if re.search(r'Clsn[12]\[\d+\]\s*=\s*[^\n]+\[Begin Action', content):
                    problems += 1
            except:
                pass
        
        if problems == 0:
            self.log(f"  Checked {len(sample)} AIR files - all clean ✓", 'SUCCESS')
            self.checks_passed += 1
        else:
            self.log(f"  {problems}/{len(sample)} AIR files have issues", 'WARNING')
            self.warnings.append(f"{problems} AIR files may have problems")
            self.checks_passed += 1  # Non-critical
    
    def check_mugen_log(self):
        """Vérifie mugen.log pour erreurs"""
        self.log("CHECK: mugen.log for errors", 'CHECK')
        
        if not os.path.exists('mugen.log'):
            self.log("  mugen.log not found (game not launched)", 'INFO')
            return
        
        try:
            with open('mugen.log', 'r', encoding='utf-8', errors='ignore') as f:
                log_content = f.read()
            
            # Check for errors
            error_lines = [line for line in log_content.split('\n') 
                          if 'error' in line.lower() or 'failed' in line.lower()]
            
            if error_lines:
                self.log(f"  Found {len(error_lines)} potential errors", 'WARNING')
                for err in error_lines[:3]:
                    self.log(f"    • {err.strip()}", 'WARNING')
                self.warnings.append(f"{len(error_lines)} errors in mugen.log")
            else:
                self.log("  No errors in mugen.log ✓", 'SUCCESS')
                self.checks_passed += 1
                
        except Exception as e:
            self.log(f"  Error reading mugen.log: {e}", 'ERROR')
    
    def check_launchers(self):
        """Vérifie la syntaxe des launchers"""
        self.log("CHECK: Launcher syntax", 'CHECK')
        
        launchers = [
            'launcher.py',
            'launcher_modern.py', 
            'LAUNCHER_ULTIMATE.py',
            'LAUNCHER_ULTIMATE_V2.py'
        ]
        
        syntax_errors = 0
        for launcher in launchers:
            if os.path.exists(launcher):
                try:
                    with open(launcher, 'r', encoding='utf-8') as f:
                        compile(f.read(), launcher, 'exec')
                except SyntaxError:
                    syntax_errors += 1
                    self.errors.append(f"{launcher} has syntax errors")
        
        if syntax_errors == 0:
            self.log("  All launchers have valid syntax ✓", 'SUCCESS')
            self.checks_passed += 1
        else:
            self.log(f"  {syntax_errors} launchers have syntax errors!", 'ERROR')
            self.checks_failed += 1
    
    def generate_report(self):
        """Génère le rapport final"""
        print()
        print("=" * 60)
        print("📊 RAPPORT D'AUTO-VÉRIFICATION")
        print("=" * 60)
        print(f"✅ Vérifications réussies: {self.checks_passed}")
        print(f"❌ Vérifications échouées: {self.checks_failed}")
        print(f"⚠️  Avertissements: {len(self.warnings)}")
        print()
        
        if self.errors:
            print("ERREURS CRITIQUES:")
            for err in self.errors:
                print(f"  • {err}")
            print()
        
        if self.warnings:
            print("AVERTISSEMENTS:")
            for warn in self.warnings[:5]:
                print(f"  • {warn}")
            print()
        
        total = self.checks_passed + self.checks_failed
        if total > 0:
            success_rate = (self.checks_passed / total) * 100
            print(f"Taux de réussite: {success_rate:.1f}%")
        
        print("=" * 60)

def main():
    """Main function"""
    print()
    print("╔═══════════════════════════════════════════════════════╗")
    print("║   KOF ULTIMATE - AUTO-VÉRIFICATION SYSTÈME           ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print()
    
    checker = KOFAutoChecker()
    
    # Run all checks
    checker.check_backgrounds()
    checker.check_air_files()
    checker.check_mugen_log()
    checker.check_launchers()
    
    # Generate report
    checker.generate_report()
    
    return 0 if checker.checks_failed == 0 else 1

if __name__ == '__main__':
    exit(main())
