# Shortlist — espèces à ajouter (Cobblemon 1.8.1)

**Périmètre CobbleLore :** légendaires + mythiques uniquement. **Ultra Beasts exclus** (pas d’items, pas de pools).

Référence Cobblemon **1.8.1** (`gBW3vLC7`) : **94** espèces tag `legendary` ou `mythical` (hors `ultra_beast`).

**Cobblelore aujourd’hui :** **86** espèces.  
**Manque pour couvrir les 94 :** **8** espèces.

> **Chi-Yu :** espèce **`chiyu`** (`cobblelore-chiyu.json`, item `ruinous_beads`) — corrigé.

---

## À ajouter (8)

| Espèce | Catégorie | Voie recommandée | Item CobbleLore suggéré | Notes |
|--------|-----------|------------------|-------------------------|--------|
| **meloetta** | Mythical | Spawn monde | `melody_disc` / `relic_harp` | Texture à créer |
| **marshadow** | Mythical | Spawn monde | `shadow_cloak` | Idem |
| **manaphy** | Mythical | Spawn monde | `sea_heart` | Phione optionnel (souvent exclu) |
| **phione** | Mythical | *(hors scope recommandé)* | `phione_egg` | Dérivé Manaphy — skip sauf quête |
| **melmetal** | Mythical | Quête / spawn | `melmetal_core` | Lien **`meltan_nut`** (Meltan déjà là) |
| **urshifu** | Legendary | Spawn monde | `urshifu_scroll` | Lien **`scroll_of_challenge`** (Kubfu) |
| **calyrex** | Legendary | **Monument** (LM steeds) | `crown_of_calyrex` | Glastrier / Spectrier déjà LM |
| **type:null** | Legendary | Spawn monde | `type_null_mask` | Avant Silvally (`broken_memory`) |

Sans **Phione** : **7** nouveaux items (+ Calyrex monument-only).

---

## Récap

| | Espèces |
|---|--------|
| Cobblelore actuel | 86 |
| Cible (leg + myth, sans UB) | 94 |
| Reste à implémenter | **8** (ou **7** sans Phione) |

---

## Ordre suggéré

1. ~~Fix `chiyu`~~ (fait).  
2. Meloetta, Marshadow, Calyrex, Urshifu.  
3. Melmetal (rituel Meltan).  
4. Type:Null (optionnel).  
5. Manaphy (+ Phione seulement si tu veux).

Après ajout : `./gradlew build`, `python3 scripts/regenerate_items_table.py`, règle **monument OU spawn** (comme le reste).

---

## Ultra Beasts (hors scope)

Non prévus sur CobbleLore : Nihilego, Buzzwole, Pheromosa, Xurkitree, Celesteela, Kartana, Guzzlord, Poipole, Naganadel, Stakataka, Blacephalon.
