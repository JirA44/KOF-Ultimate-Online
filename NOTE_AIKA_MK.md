# ⚠️ Aika_MK - Test en cours

**Date:** 2025-10-24 20:10

## Ce qui s'est passé

Le jeu a crashé après la sélection de **Aika_MK** en mode Versus.

### Log mugen.log:
```
Selected char 5 on teamslot 0.0
Char Aika_MK.def (5) request pal 0 FFF (FFF) -> reserved 0 (FFE)
End of charsel loop
[...]
Character Aika_MK.def loaded OK
New char Aika_MK loaded into cache: (1/7 cached) Load time: 950.000ms
```

Puis le jeu s'arrête brutalement.

## Analyse

- ✅ Aika_MK se charge correctement
- ✅ Pas d'erreur dans les fichiers
- ❌ **MAIS** crash après chargement, avant sélection P2

Cela suggère que Aika_MK pourrait causer un crash au démarrage du combat.

## Action prise

Aika_MK désactivé **TEMPORAIREMENT** pour test.

## À faire

1. Relancer le jeu
2. Tester avec un autre personnage
3. Si ça fonctionne → Aika_MK est le problème, on le garde désactivé
4. Si ça crash encore → Le problème est ailleurs
