# cobblelore-legendary

Mod Fabric **1.21.1** : items légendaires `cobblelore:*` (catalogue Delta/Academy), intégration **Myths and Legends** (key items + spawn pools) et doc/config pour **Legendary Monuments** (pedestals).

**Périmètre :** légendaires + mythiques Cobblemon — **pas d’Ultra Beasts**.

## Stack serveur / client

- Cobblemon
- Myths and Legends (+ datapack officiel recommandé)
- **Complete Cobblemon Collection — M&L compat** (`complete-cobblemon-collection-myths-and-legends-compat` **2.21** on Modrinth) — models/textures (e.g. Galar birds); **no** natural legendary spawns
- Legendary Monuments
- **cobblelore-legendary** (client + serveur) — key items, spawn pools, LM pedestal mapping

## Build

```bash
./gradlew build
```

JAR : `build/libs/cobblelore-legendary-0.1.0.jar`

Pour compiler Legendary Monuments en compile-only, placez le JAR dans `libs/` (voir `libs/.gitignore`).

## Gameplay visé

**Une seule voie par légendaire** (voir [`docs/TABLEAU-ITEMS-LEGENDAIRES.md`](docs/TABLEAU-ITEMS-LEGENDAIRES.md)) :

1. **Pedestal Legendary Monuments** (~20 espèces) → monument + item CobbleLore, **pas** de spawn monde.
2. **Tous les autres** (~66) → item en inventaire + biomes (Myths and Legends), **pas** de pedestal LM.

Exemple config LM : [`docs/legendary-monuments-pedestals-cobblelore.json`](docs/legendary-monuments-pedestals-cobblelore.json).

## Config Legendary Monuments

Exemple de section `pedestals` pointant vers nos items : [`docs/legendary-monuments-pedestals-cobblelore.json`](docs/legendary-monuments-pedestals-cobblelore.json) à fusionner dans `config/LegendaryMonuments/config.json`.

## Couverture monuments / pedestals

Tableau des gaps : [`docs/GAPS-LEGENDARY-MONUMENTS.md`](docs/GAPS-LEGENDARY-MONUMENTS.md) (généré par `scripts/generate_legendary_assets.py`).

## Assets

Legendary **item** textures come from Delta Client where applicable (verify rights before public distribution). **Pokémon models** for missing vanilla forms (Galar birds, etc.) come from **CCC M&L compat** in the CobbleLore pack — not from this mod.

Regenerate item textures and spawn pools:

```bash
python3 scripts/generate_legendary_assets.py
```

## Documentation

- [Analyse complète des mods source](docs/ANALYSE-MODS.md)
- [Alignement pack CobbleLore](docs/COMPAT-PACK-COBBLELORE.md)
- [Tableau des 86 items](docs/TABLEAU-ITEMS-LEGENDAIRES.md) · [Exceptions](docs/EXCEPTIONS-ITEMS-LEGENDAIRES.md)
