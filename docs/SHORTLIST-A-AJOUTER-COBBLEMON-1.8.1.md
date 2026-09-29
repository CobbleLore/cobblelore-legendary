# Shortlist — espèces à ajouter (Cobblemon 1.8.1)

Référence : tags **`legendary` / `mythical` / `ultra_beast`** dans le JAR Cobblemon **1.8.1** (`gBW3vLC7`) — **105** espèces implémentées.

**Cobblelore aujourd’hui :** **86** espèces (catalogue Delta/Academy).  
**Manque pour couvrir les 105 :** **19** espèces (voir ci‑dessous).

> **Note technique :** le pool `cobblelore-chiiyu.json` utilise l’id `chiiyu` ; Cobblemon attend **`chiyu`**. À corriger séparément (pas un “oubli” de contenu).

---

## Priorité haute — légendaires / mythiques “classiques” (8)

| Espèce Cobblemon | Catégorie | Voie recommandée | Item CobbleLore suggéré | Notes |
|------------------|-----------|------------------|-------------------------|--------|
| **meloetta** | Mythical | Spawn monde | `melody_disc` ou `relic_harp` | Pas de gimmick Delta ; créer texture |
| **marshadow** | Mythical | Spawn monde | `shadow_cloak` | Idem |
| **manaphy** | Mythical | Spawn monde | `sea_heart` | Pair avec Phione (décision loot) |
| **phione** | Mythical | Spawn monde (optionnel) | `phione_egg` | Souvent exclu des packs ; dérivé Manaphy |
| **melmetal** | Mythical | Spawn monde **ou** quête Meltan | `melmetal_nut` / fusion Meltan | Tu as déjà **`meltan_nut`** → Meltan ; Melmetal = évolution / rituel |
| **urshifu** | Legendary | Spawn monde | `scroll_of_urshifu` | Tu as **`scroll_of_challenge`** → Kubfu ; Urshifu = forme finale |
| **calyrex** | Legendary | **Monument** (pedestal steed LM) | `crown_of_calyrex` | Glastrier/Spectrier déjà en LM ; un item “roi” pour le rituel |
| **type:null** | Legendary | Spawn monde | `type_null_mask` | Silvally (`broken_memory`) est la **ligne** ; Type:Null = étape précédente si tu veux 100 % dex |

---

## Priorité moyenne — décision produit Ultra Beasts (11)

Toutes tag **`ultra_beast`** en 1.8.1. Aucune dans Delta gimmick / Cobblelore actuel.

| Espèce | Item suggéré (thème) |
|--------|----------------------|
| nihilego | `parasite_crystal` |
| buzzwole | `muscle_essence` |
| pheromosa | `speed_crystal` |
| xurkitree | `lightning_stake` |
| celesteela | `rocket_shell` |
| kartana | `paper_blade` |
| guzzlord | `hunger_core` |
| poipole | `poison_stinger` |
| naganadel | `naga_wing` (ou spawn via évolution Poipole) |
| stakataka | `stack_stone` |
| blacephalon | `firework_head` |

**Reco réseau :**

- **Pack “légendaires only”** → ne pas ajouter les UB (reste à **94** espèces special + 86 actuelles = gap 8 sans UB).
- **Pack “100 % tags Cobblemon”** → ajouter les **11** UB + pools spawn monde (pas de pedestal LM).

---

## Récap chiffré

| Scope | Espèces | Items à créer (ordre de grandeur) |
|-------|---------|-----------------------------------|
| **Actuel** | 86 | — |
| **+ mythiques / legs manquants (sans UB)** | +8 (ou +7 sans Phione) | ~7–8 items + 1 fix `chiyu` |
| **+ Ultra Beasts** | +11 | ~11 items |
| **Total “105 Cobblemon”** | 105 | **+19** items (+ fix id `chiyu`) |

---

## Ordre d’implémentation suggéré

1. Fix **`chiiyu` → `chiyu`** dans `legendary_items.json` + pool.  
2. **Meloetta, Marshadow, Calyrex, Urshifu** (impact joueur visible).  
3. **Melmetal** (lien **`meltan_nut`** / quête).  
4. **Type:Null** si tu veux la chaîne avant Silvally.  
5. **Manaphy / Phione** si tu veux les mythiques “mer”.  
6. **Ultra Beasts** en bloc si le réseau les accepte.

Après chaque ajout : `./gradlew build` + `python3 scripts/regenerate_items_table.py` + décider **monument vs spawn** avec la même règle que le reste (pedestal LM → pas de pool).
