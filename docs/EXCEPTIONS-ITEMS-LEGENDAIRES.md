# Exceptions et cas particuliers

## Changement appliqué (doublons spawn + monument)

Pour **dialga, mew, latias, latios, zacian** : l’item « spawn monde » a été **retiré du mod** ; il ne reste que l’item **monument** (pools supprimés pour ces espèces).

| Pokémon | Item gardé | Item supprimé |
|---------|------------|---------------|
| dialga | `adamant_orb` | `time_core` |
| mew | `odd_sea_egg` | `rare_sea_egg` |
| latias | `psychic_orb` | `red_eon_ticket` |
| latios | `combat_orb` | `blue_eon_ticket` |
| zacian | `rusted_sword` | `z_soul` |

## Exceptions LM (Legendary Monuments) à tester en jeu

1. **Mew** — le mod LM peut encore attendre `old_sea_map` / carte, pas `odd_sea_egg`. Vérifier île Final + loot.
2. **Dialga / Palkia** — LM utilise parfois `red_chain` en dur ; `adamant_orb` / `lustrous_orb` selon config.
3. **Giratina** — pedestal peut exiger `mega_showdown:griseous_orb` au lieu de `cobblelore:griseous_orb`.
4. **Zacian / Zamazenta** — pedestal = **totem of undying** + `rusted_sword` / `rusted_shield` (2 slots).
5. **Hoopa** — `cobblelore:ring` + `mega_showdown:prison_bottle`.
6. **Reshiram / Zekrom** — pierre CobbleLore + **gem Cobblemon** (`fire_gem` / `electric_gem`).
7. **Kyurem** — 2× `gray_stone` sur le pedestal.

## Non touché (volontairement)

- **~15 espèces** avec **un seul item** qui fait encore **spawn monde + monument** (ex. Entei, Lugia, Hoopa spawn pool + pedestal).
- **Autres doublons** (Mewtwo `cloning_cable`, Ogerpon masques, Magearna `soul_heart`, etc.) — toujours **un seul** item spawn ; le second reste sans spawn.
- **Zamazenta** — garde `rusted_shield` + **spawn monde** + monument (pas de doublon supprimé).
- **Palkia / Giratina** — pas de paire doublon ; spawn monde **conservé** sur `lustrous_orb` / `griseous_orb`.
