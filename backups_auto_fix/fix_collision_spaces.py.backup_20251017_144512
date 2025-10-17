# -*- coding: utf-8 -*-
"""
Corrige les espaces dans les déclarations de collision boxes
"""

import re

file_path = r'D:\KOF Ultimate Online\chars\orochi-iori\Iori-Orochi.air'

# Lit le fichier
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Remplace les espaces problématiques
content = re.sub(r'Clsn2 \[', 'Clsn2[', content)
content = re.sub(r'Clsn1 \[', 'Clsn1[', content)

# Sauvegarde
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Fichier corrigé: {file_path}")
