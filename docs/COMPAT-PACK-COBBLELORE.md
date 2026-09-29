# Alignement avec le monorepo [CobbleLore/cobblelore](https://github.com/CobbleLore/cobblelore)

Source de vérité : `pack/pack.json` (pack **0.1.149** au moment de l’audit).

## Versions déjà pinées dans le pack CobbleLore

| Composant | Version pack | Version dev `cobblelore-legendary` |
|-----------|--------------|--------------------------------------|
| Minecraft | 1.21.1 | 1.21.1 |
| Fabric Loader | **0.19.5** | **0.19.5** (mis à jour) |
| Fabric API | **0.116.17+1.21.1** | **0.116.17+1.21.1** |
| Cobblemon | **1.8.1** (`gBW3vLC7`) | **1.8.1** (mis à jour, était 1.6.1) |
| Legendary Monuments | **8.1-Love-for-All** (`F6Ub0Gga`) | compile-only réf. |
| Cobblemon Mega Showdown | 1.2.0+1.8.1… (`TKdAixuR`) | dépendance LM (déjà sur serveur) |
| Lithostitched / Chipped / Accessories | oui (serveur) | deps LM déjà présentes |

## Ce qui **manque encore** dans `pack.json` (à ajouter pour le projet légendaires)

| Mod / contenu | Client | Serveur aujourd’hui | Action recommandée |
|---------------|--------|---------------------|-------------------|
| **Myths and Legends** sidemod | absent | absent | Ajouter Modrinth `cobblemon-myths-and-legends-sidemod` **1.9.0** (`eg83qtSQ`) client **et** serveur |
| **Myths and Legends datapack** | N/A | absent | Ajouter dans `serverDatapacks` (slug `mythsandlegends-datapack`, dernière version 1.21.1) |
| **Legendary Monuments** | présent | **absent** | **Obligatoire sur le serveur** pour structures + pedestals (aujourd’hui client seulement) |
| **cobblelore-legendary** | absent | absent | JAR custom via `pack/client/mods` + `pack/server/mods` (script build à créer, comme `build:menu-mod`) |

Sans LM + M&L côté **serveur**, le gameplay item → structure → pedestal ne peut pas fonctionner en multijoueur.

## Myths and Legends — dernière version

Modrinth Fabric 1.21.1 : **1.9.0** (`eg83qtSQ`, nov. 2025). Compatible avec Cobblemon **≥ 1.7** dans le `fabric.mod.json` du mod ; à valider en jeu avec **Cobblemon 1.8.1**.

Pas besoin de rétrograder Cobblemon : le pack est **déjà** en 1.8.1 ; c’est **`cobblelore-legendary`** qui devait rattraper le pack (fait dans `gradle.properties`).

## Intégration pack (quand le mod est prêt)

1. `./gradlew build` → copier le JAR vers `pack/client/mods/` et `pack/server/mods/` (ajouter un script npm miroir des autres mods CobbleLore).
2. Merger `docs/legendary-monuments-pedestals-cobblelore.json` dans la config LM du serveur après premier boot.
3. `npm run build:pack` → nouvelle version immuable du manifest.

## Mods CobbleLore custom (org)

Les autres mods (`cobblelore-menu`, etc.) utilisent souvent Loader **0.17.2** dans leur propre `gradle.properties` alors que le **pack** impose **0.19.5** : au runtime c’est le loader du pack qui gagne. Harmoniser progressivement les `loader_version` des repos mods sur **0.19.5** évite les surprises en dev local.
