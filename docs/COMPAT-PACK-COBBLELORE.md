# Alignement avec le monorepo [CobbleLore/cobblelore](https://github.com/CobbleLore/cobblelore)

Source de vérité : `pack/pack.json` (pack **0.1.155**, SHA `07901b40…` au 2026-09-29).

## Versions déjà pinées dans le pack CobbleLore

| Composant | Version pack | Version dev `cobblelore-legendary` |
|-----------|--------------|--------------------------------------|
| Minecraft | 1.21.1 | 1.21.1 |
| Fabric Loader | **0.19.5** | **0.19.5** |
| Fabric API | **0.116.17+1.21.1** | **0.116.17+1.21.1** |
| Cobblemon | **1.8.1** (`gBW3vLC7`) | **1.8.1** |
| Legendary Monuments | **8.1-Love-for-All** (`F6Ub0Gga`) | compile-only réf. |
| Cobblemon Mega Showdown | 1.2.0+1.8.1… (`TKdAixuR`) | dépendance LM (client + serveur) |
| Lithostitched / Chipped / Accessories | oui (serveur) | deps LM déjà présentes |

Depuis **0.1.155**, **Legendary Monuments** est listé côté **client et serveur** (plus seulement client). Les structures LM et les pedestals peuvent donc tourner en multijoueur sans ajout LM supplémentaire dans le manifest.

## Ce qui **manque encore** dans `pack.json` (pour le projet légendaires)

| Mod / contenu | Client | Serveur (0.1.155) | Action recommandée |
|---------------|--------|-------------------|-------------------|
| **Myths and Legends** sidemod | absent | absent | Ajouter Modrinth `cobblemon-myths-and-legends-sidemod` **1.9.0** (`eg83qtSQ`) client **et** serveur |
| **Myths and Legends datapack** | N/A | absent (`serverDatapacks` = CobbleTowns seulement) | Ajouter slug `mythsandlegends-datapack` (1.21.1, version ≥ 1.3) |
| **Legendary Monuments** | présent | **présent** | Rien à ajouter au manifest ; config pedestals `cobblelore:*` côté serveur |
| **cobblelore-legendary** | absent | absent | JAR custom via `pack/client/mods` + `pack/server/mods` (script build dans le monorepo, comme les autres `cobblelore-*`) |

Sans **M&L** côté serveur + datapack, les spawn pools `key_item: cobblelore:…` et la consommation d’item au spawn ne s’activent pas. LM seul ne remplace pas M&L pour les spawns ultra-rares au monde.

## Changements notables pack 0.1.149 → 0.1.155 (hors légendaires)

- Serveur : Moog’s structure mods (`mtr-`, `mss-`, `mes-`, `mns-`), `item-obliterator`, `athena-ctm`, `openblocks-elevator`, `clumps`, datapacks farmers-cutting, etc.
- Client : `controlify`, `cubes-without-borders`, optimisations / UI diverses.
- **Inchangé pour nous** : pas de M&L, pas de `cobblelore-legendary`, Cobblemon reste **1.8.1**.

## Myths and Legends — dernière version

Modrinth Fabric 1.21.1 : **1.9.0** (`eg83qtSQ`, nov. 2025). Compatible Cobblemon **≥ 1.7** dans le `fabric.mod.json` du sidemod ; à valider en jeu avec **Cobblemon 1.8.1**.

Le pack est déjà en **1.8.1** ; **`cobblelore-legendary`** est aligné dans `gradle.properties`.

## Intégration pack (quand le mod est publié)

1. `./gradlew build` → copier le JAR vers `pack/client/mods/` et `pack/server/mods/` (script npm miroir des autres mods CobbleLore).
2. Entrées Modrinth M&L sidemod + datapack dans `pack.json`, bump version pack.
3. Merger `docs/legendary-monuments-pedestals-cobblelore.json` dans la config LM du serveur après premier boot.
4. `npm run build:pack` → nouvelle version immuable du manifest.

## Mods CobbleLore custom (org)

Les autres mods (`cobblelore-menu`, etc.) utilisent parfois Loader **0.17.2** dans leur propre `gradle.properties` alors que le **pack** impose **0.19.5** : au runtime c’est le loader du pack qui gagne. Harmoniser progressivement les `loader_version` des repos mods sur **0.19.5** évite les surprises en dev local.
