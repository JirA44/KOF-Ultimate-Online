#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTO CALCULATE OPTIMAL GRID - KOF ULTIMATE
Calcule automatiquement la grille optimale pour 169 personnages
"""

import math

# Contraintes
SCREEN_W = 640
SCREEN_H = 480
CHAR_COUNT = 169
CELL_W = 28  # Reduced from 34 to fit more characters
CELL_H = 28  # Reduced from 34 to fit more characters
CELL_SPACING = 1  # Reduced spacing

# NOUVELLE APPROCHE: Portraits sur les CÔTÉS (gauche/droite)
# au lieu d'en haut, pour libérer l'espace vertical!
PORTRAIT_W = 80   # Portrait width on sides
MARGIN_LEFT = 10
MARGIN_RIGHT = 10
MARGIN_TOP = 10
MARGIN_BOTTOM = 10

# Espace disponible pour la grille
GRID_SPACE_W = SCREEN_W - (PORTRAIT_W * 2) - MARGIN_LEFT - MARGIN_RIGHT  # Space for 2 portraits on sides
GRID_SPACE_H = SCREEN_H - MARGIN_TOP - MARGIN_BOTTOM  # Full vertical space

print(f"\n{'='*70}")
print(f"  AUTO CALCULATE OPTIMAL GRID")
print(f"{'='*70}\n")

print(f"Contraintes:")
print(f"  Écran: {SCREEN_W}×{SCREEN_H}")
print(f"  Personnages: {CHAR_COUNT}")
print(f"  Cell size: {CELL_W}×{CELL_H}")
print(f"  Cell spacing: {CELL_SPACING}")
print(f"\nEspace:")
print(f"  Portraits sur les côtés (2 × {PORTRAIT_W}px)")
print(f"  Espace horizontal disponible: {GRID_SPACE_W}px")
print(f"  Espace vertical disponible: {GRID_SPACE_H}px")

# Calculer les dimensions avec spacing
CELL_TOTAL_W = CELL_W + CELL_SPACING
CELL_TOTAL_H = CELL_H + CELL_SPACING

# Nombre de lignes/colonnes max
MAX_COLS = int(GRID_SPACE_W / CELL_TOTAL_W)
MAX_ROWS = int(GRID_SPACE_H / CELL_TOTAL_H)
print(f"  Colonnes max: {MAX_COLS}")
print(f"  Lignes max: {MAX_ROWS}")

# Trouver la combinaison optimale rows × cols
best_combo = None
best_empty = 999999

for rows in range(1, MAX_ROWS + 1):
    # Calculer cols nécessaires
    cols = math.ceil(CHAR_COUNT / rows)
    total_slots = rows * cols
    empty_slots = total_slots - CHAR_COUNT

    # Calculer les dimensions
    grid_w = cols * CELL_TOTAL_W
    grid_h = rows * CELL_TOTAL_H

    # Vérifier si ça rentre dans l'espace disponible
    if grid_w > GRID_SPACE_W:
        continue
    if grid_h > GRID_SPACE_H:
        continue

    # Préférer le minimum de cases vides
    if empty_slots < best_empty:
        best_empty = empty_slots
        best_combo = (rows, cols, grid_w, grid_h, total_slots, empty_slots)

if not best_combo:
    print("\n❌ ERREUR: Impossible de trouver une configuration valide!")
    exit(1)

rows, cols, grid_w, grid_h, total_slots, empty_slots = best_combo

# Calculer position optimale (centrer dans l'espace disponible)
grid_x = PORTRAIT_W + MARGIN_LEFT + ((GRID_SPACE_W - grid_w) // 2)
grid_y = MARGIN_TOP + ((GRID_SPACE_H - grid_h) // 2)

# Vérifier que ça rentre
grid_bottom = grid_y + grid_h

print(f"\n{'='*70}")
print(f"  CONFIGURATION OPTIMALE")
print(f"{'='*70}")
print(f"\nGrille: {rows}×{cols}")
print(f"  Total slots: {total_slots}")
print(f"  Personnages: {CHAR_COUNT}")
print(f"  Cases vides: {empty_slots} ({100*empty_slots/total_slots:.1f}%)")
print(f"\nDimensions:")
print(f"  Largeur: {grid_w}px (espace: {GRID_SPACE_W}px)")
print(f"  Hauteur: {grid_h}px (espace: {GRID_SPACE_H}px)")
print(f"\nPosition:")
print(f"  X: {grid_x}px")
print(f"  Y: {grid_y}px")
print(f"  Bottom: {grid_bottom}px (écran: {SCREEN_H}px)")
print(f"\nMarge bottom: {SCREEN_H - grid_bottom}px")

if grid_bottom > SCREEN_H:
    print(f"\n❌ ERREUR: La grille dépasse l'écran de {grid_bottom - SCREEN_H}px!")
else:
    print(f"\n✓ La grille rentre parfaitement!")

print(f"\n{'='*70}")
print(f"  À METTRE DANS system.def:")
print(f"{'='*70}")
print(f"\nrows = {rows}")
print(f"columns = {cols}")
print(f"pos = {grid_x},{grid_y}")
print(f"{'='*70}\n")
