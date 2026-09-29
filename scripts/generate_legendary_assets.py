#!/usr/bin/env python3
"""Generate cobblelore item assets, spawn pools, and gap report from analysis JARs."""
from __future__ import annotations

import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DELTA = ROOT / "analysis/mods/delta-client.jar"
MYTHS = ROOT / "analysis/mods/myths-and-legends.jar"
LM = ROOT / "analysis/mods/legendary-monuments.jar"
RES = ROOT / "src/main/resources"
ASSETS = RES / "assets/cobblelore"
DATA = RES / "data/cobblemon/spawn_pool_world"
DOCS = ROOT / "docs"

LEGENDARY_IDS = """
rare_dna time_core wishing_star meteorite rare_sea_egg nightmare_core gracidea jewel_of_life
victory_star resolute_sword relic_disc disc_drive pink_diamond ring steam_engine soul_heart z_soul
meltan_nut dada_scarf mythical_pecha_berry glacial_orb static_orb flare_orb cloning_cable
sacred_lightning sacred_flame sacred_droplet silver_wing rainbow_wing steel_alloy never_melt_icicle
ancient_ingot infinite_source dragon_skull titan_totem blue_eon_ticket red_eon_ticket blue_orb red_orb
jade_orb ruby_of_willpower ruby_of_emotion ruby_of_knowledge adamant_orb lustrous_orb griseous_orb
magma_chunk lunar_feather cobalion_sword virizion_sword terrakion_sword thundurus_bottle tornadus_bottle
landorus_bottle enamorus_bottle light_stone dark_stone gray_stone tree_of_life cocoon_of_destruction
zygarde_cube broken_memory electric_totem psychic_totem grass_totem water_totem solar_core lunar_core
eclipse_core rusted_sword rusted_shield dynamax_core mystical_branch frozen_hoof ghostly_hoof
koraidon_key miraidon_key toxic_scarf toxic_headband toxic_ribbon stellar_tera_core psychic_orb
combat_orb dark_orb ruinous_sword ruinous_beads ruinous_tablet ruinous_vessel zeraora_tuft cosmic_core
cosmic_flute odd_sea_egg rks_communicator scroll_of_challenge teal_mask wellspring_mask hearthflame_mask
cornerstone_mask
""".split()

# cobblelore item -> primary Cobblemon species (1:1 design target)
ITEM_TO_SPECIES: dict[str, str] = {
    "rare_dna": "mewtwo",
    "cloning_cable": "mewtwo",
    "time_core": "dialga",
    "wishing_star": "jirachi",
    "meteorite": "deoxys",
    "rare_sea_egg": "mew",
    "odd_sea_egg": "mew",
    "nightmare_core": "darkrai",
    "gracidea": "shaymin",
    "jewel_of_life": "arceus",
    "victory_star": "victini",
    "resolute_sword": "keldeo",
    "relic_disc": "magearna",
    "disc_drive": "genesect",
    "pink_diamond": "diancie",
    "ring": "hoopa",
    "steam_engine": "volcanion",
    "soul_heart": "magearna",
    "z_soul": "zacian",
    "meltan_nut": "meltan",
    "dada_scarf": "zarude",
    "mythical_pecha_berry": "pecharunt",
    "glacial_orb": "articuno",
    "static_orb": "zapdos",
    "flare_orb": "moltres",
    "sacred_lightning": "raikou",
    "sacred_flame": "entei",
    "sacred_droplet": "suicune",
    "silver_wing": "lugia",
    "rainbow_wing": "hooh",
    "steel_alloy": "registeel",
    "never_melt_icicle": "regice",
    "ancient_ingot": "regirock",
    "infinite_source": "regieleki",
    "dragon_skull": "regidrago",
    "titan_totem": "regigigas",
    "blue_eon_ticket": "latios",
    "red_eon_ticket": "latias",
    "blue_orb": "kyogre",
    "red_orb": "groudon",
    "jade_orb": "rayquaza",
    "ruby_of_willpower": "azelf",
    "ruby_of_emotion": "mesprit",
    "ruby_of_knowledge": "uxie",
    "adamant_orb": "dialga",
    "lustrous_orb": "palkia",
    "griseous_orb": "giratina",
    "magma_chunk": "heatran",
    "lunar_feather": "cresselia",
    "cobalion_sword": "cobalion",
    "virizion_sword": "virizion",
    "terrakion_sword": "terrakion",
    "thundurus_bottle": "thundurus",
    "tornadus_bottle": "tornadus",
    "landorus_bottle": "landorus",
    "enamorus_bottle": "enamorus",
    "light_stone": "reshiram",
    "dark_stone": "zekrom",
    "gray_stone": "kyurem",
    "tree_of_life": "xerneas",
    "cocoon_of_destruction": "yveltal",
    "zygarde_cube": "zygarde",
    "broken_memory": "silvally",
    "electric_totem": "tapukoko",
    "psychic_totem": "tapulele",
    "grass_totem": "tapubulu",
    "water_totem": "tapufini",
    "solar_core": "solgaleo",
    "lunar_core": "lunala",
    "eclipse_core": "necrozma",
    "rusted_sword": "zacian",
    "rusted_shield": "zamazenta",
    "dynamax_core": "eternatus",
    "mystical_branch": "celebi",
    "frozen_hoof": "glastrier",
    "ghostly_hoof": "spectrier",
    "koraidon_key": "koraidon",
    "miraidon_key": "miraidon",
    "toxic_scarf": "okidogi",
    "toxic_headband": "munkidori",
    "toxic_ribbon": "fezandipiti",
    "stellar_tera_core": "terapagos",
    "psychic_orb": "latias",
    "combat_orb": "latios",
    "dark_orb": "darkrai",
    "ruinous_sword": "chienpao",
    "ruinous_beads": "chiyu",
    "ruinous_tablet": "wochien",
    "ruinous_vessel": "tinglu",
    "zeraora_tuft": "zeraora",
    "cosmic_core": "cosmog",
    "cosmic_flute": "cosmoem",
    "rks_communicator": "silvally",
    "scroll_of_challenge": "kubfu",
    "teal_mask": "ogerpon",
    "wellspring_mask": "ogerpon",
    "hearthflame_mask": "ogerpon",
    "cornerstone_mask": "ogerpon",
}

LM_TRACKER_STRUCTURES = {
    "dragonspiral_tower", "kyurem_cave", "turnback_cave", "giratina_island", "spear_pillar",
    "snowpoint_temple", "lake_valor", "lake_acuity", "lake_verity", "lugia_temple", "southern_island",
    "ecruteak", "heatran_cave", "cobalion_shrine", "virizion_shrine", "terrakion_shrine", "keldeo_shrine",
    "hoopa_pyramid", "eternatus_cocoon", "crown_shrine", "frost_carrot", "knightly_heroes",
    "dyna_tree", "tree_of_life", "yveltal_cocoon", "amphitheater", "final_island", "liberty_island",
}

LM_PEDESTAL_SPECIES = {
    "mew", "dialga", "palkia", "giratina", "glastrier", "spectrier", "latias", "latios",
    "entei", "raikou", "suicune", "heatran", "hooh", "lugia", "hoopa", "zekrom", "reshiram",
    "kyurem", "zacian", "zamazenta",
}


def extract_textures() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    tex_dir = ASSETS / "textures/item"
    tex_dir.mkdir(parents=True, exist_ok=True)
    models_dir = ASSETS / "models/item"
    models_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DELTA) as z:
        for item_id in LEGENDARY_IDS:
            src = f"assets/cobblemon/textures/item/gimmick/{item_id}.png"
            try:
                data = z.read(src)
            except KeyError:
                print("WARN missing texture", item_id)
                continue
            (tex_dir / f"{item_id}.png").write_bytes(data)
            model = {
                "parent": "minecraft:item/generated",
                "textures": {"layer0": f"cobblelore:item/{item_id}"},
            }
            (models_dir / f"{item_id}.json").write_text(json.dumps(model, indent=2) + "\n")


def load_myths_pools() -> dict[str, dict]:
    pools = {}
    with zipfile.ZipFile(MYTHS) as z:
        for name in z.namelist():
            if not name.startswith("data/cobblemon/spawn_pool_world/mythsandlegends-"):
                continue
            if not name.endswith(".json"):
                continue
            species = name.split("mythsandlegends-")[1].replace(".json", "")
            pools[species] = json.loads(z.read(name))
    return pools


def generate_spawn_pools(myths_pools: dict[str, dict]) -> None:
    if DATA.exists():
        shutil.rmtree(DATA)
    DATA.mkdir(parents=True)
    species_to_item: dict[str, str] = {}
    for item_id, species in ITEM_TO_SPECIES.items():
        species_to_item.setdefault(species, item_id)

    for species, pool in myths_pools.items():
        if species in LM_PEDESTAL_SPECIES:
            continue
        item_id = species_to_item.get(species)
        if not item_id:
            continue
        new_pool = json.loads(json.dumps(pool))
        for spawn in new_pool.get("spawns", []):
            cond = spawn.get("condition")
            if cond and "key_item" in cond:
                cond["key_item"] = f"cobblelore:{item_id}"
        out = DATA / f"cobblelore-{species}.json"
        out.write_text(json.dumps(new_pool, indent=2) + "\n")

    # Extra pools for species not in M&L but mapped from items
    for species, item_id in species_to_item.items():
        if species in myths_pools or species in LM_PEDESTAL_SPECIES:
            continue
        minimal = {
            "enabled": True,
            "neededInstalledMods": [],
            "neededUninstalledMods": [],
            "spawns": [
                {
                    "id": f"cobblelore-{species}-0",
                    "pokemon": species,
                    "presets": ["natural"],
                    "type": "pokemon",
                    "context": "grounded",
                    "bucket": "ultra-rare",
                    "level": "50-70",
                    "weight": 0.1,
                    "condition": {"key_item": f"cobblelore:{item_id}"},
                }
            ],
        }
        (DATA / f"cobblelore-{species}.json").write_text(json.dumps(minimal, indent=2) + "\n")


def generate_gaps() -> None:
    myths_pools = load_myths_pools()
    lines = [
        "# Couverture structures / pedestals (Legendary Monuments 8.1)",
        "",
        "Légende : **M&L** = pool spawn Myths and Legends de base pour l'espèce ; **LM struct** = monument piste Arc Phone (approx.) ; **LM pedestal** = bloc pedestal dédié.",
        "",
        "| Item `cobblelore:` | Espèce | M&L vanilla pool | LM pedestal | Notes |",
        "|---|---|---|---|---|",
    ]
    for item_id in LEGENDARY_IDS:
        species = ITEM_TO_SPECIES.get(item_id, "?")
        ml = "oui" if species in myths_pools else "non"
        ped = "oui" if species in LM_PEDESTAL_SPECIES else "non"
        note = ""
        if species == "ogerpon" and item_id != "teal_mask":
            note = "masque Ogerpon — même espèce, pas de pedestal séparé LM"
        if ml == "non":
            note = (note + "; " if note else "") + "spawn via pool cobblelore minimal"
        if ped == "non" and ml == "oui":
            note = (note + "; " if note else "") + "M&L biome spawn — pas de pedestal LM"
        lines.append(f"| `{item_id}` | {species} | {ml} | {ped} | {note} |")

    missing_ped = sorted(
        {ITEM_TO_SPECIES[i] for i in LEGENDARY_IDS if ITEM_TO_SPECIES.get(i) not in LM_PEDESTAL_SPECIES}
    )
    lines.extend(
        [
            "",
            "## Espèces sans pedestal Legendary Monuments",
            "",
            f"Total espèces distinctes : {len(set(ITEM_TO_SPECIES.values()))}.",
            f"Avec pedestal LM (~20) : {len(LM_PEDESTAL_SPECIES)}.",
            "",
            "Pour le gameplay **structure + pedestal**, seules les espèces avec pedestal LM (ou config custom) fonctionnent sans autre mécanique LM (urnes, clés golem, etc.).",
            "",
        ]
    )
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "GAPS-LEGENDARY-MONUMENTS.md").write_text("\n".join(lines) + "\n")


def write_catalog_json() -> None:
    meta = RES / "cobblelore"
    meta.mkdir(parents=True, exist_ok=True)
    (meta / "legendary_items.json").write_text(
        json.dumps({"items": LEGENDARY_IDS, "item_to_species": ITEM_TO_SPECIES}, indent=2) + "\n"
    )


def sync_catalog_from_disk() -> None:
    """Use legendary_items.json as source of truth (do not resurrect removed items)."""
    global LEGENDARY_IDS, ITEM_TO_SPECIES
    path = RES / "cobblelore/legendary_items.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    LEGENDARY_IDS = data["items"]
    ITEM_TO_SPECIES = data["item_to_species"]


def main() -> None:
    sync_catalog_from_disk()
    extract_textures()
    myths = load_myths_pools()
    generate_spawn_pools(myths)
    generate_gaps()
    write_catalog_json()
    print("Generated", len(LEGENDARY_IDS), "items")


if __name__ == "__main__":
    main()
