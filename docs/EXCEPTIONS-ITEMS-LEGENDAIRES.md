# Exceptions et cas particuliers

## Règle gameplay (CobbleLore)

**Une seule voie par légendaire**, pas au choix :

1. Si Legendary Monuments propose un **pedestal** pour l’espèce → **monument + item** seulement (aucun pool spawn monde dans le mod).
2. Sinon → **spawn monde** (item CobbleLore + biomes via Myths and Legends).

**20 espèces** monument-only · **66 espèces** spawn monde. Détail : [`TABLEAU-ITEMS-LEGENDAIRES.md`](TABLEAU-ITEMS-LEGENDAIRES.md).

## Items retirés du mod (historique doublons)

**Monument-only (spawn supprimé)** : `time_core`, `rare_sea_egg`, `red_eon_ticket`, `blue_eon_ticket`, `z_soul`.

**Doublons spawn supprimés** : `cloning_cable`, `soul_heart`, `dark_orb`, `rks_communicator`, `wellspring_mask`, `hearthflame_mask`, `cornerstone_mask`.

Catalogue actuel : **86 items**, **86 espèces**, **1:1**. Tableau : [`TABLEAU-ITEMS-LEGENDAIRES.md`](TABLEAU-ITEMS-LEGENDAIRES.md).

## Legendary Monuments — à tester en jeu

1. **Mew** — LM peut attendre `old_sea_map` / carte ; loot `odd_sea_egg` pour île Final.
2. **Dialga / Palkia** — parfois `red_chain` en dur ; items CobbleLore : `adamant_orb`, `lustrous_orb`.
3. **Giratina** — pedestal peut exiger `mega_showdown:griseous_orb` vs `cobblelore:griseous_orb`.
4. **Zacian / Zamazenta** — totem + `rusted_sword` / `rusted_shield`.
5. **Hoopa** — `cobblelore:ring` + `mega_showdown:prison_bottle`.
6. **Reshiram / Zekrom** — pierre CobbleLore + gem Cobblemon.
7. **Kyurem** — 2× `gray_stone`.

## Gameplay mixte (volontaire)

Plusieurs espèces ont **spawn monde + monument** sur le **même** item (ex. Entei, Lugia, Palkia, Zamazenta). Pas de doublon d’item.

Regénérer le tableau après changement catalogue :

```bash
python3 scripts/regenerate_items_table.py
```
