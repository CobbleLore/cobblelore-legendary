#!/usr/bin/env python3
"""Generate cobblelore item assets, spawn pools, and gap report from analysis JARs."""
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DELTA = ROOT / "analysis/mods/delta-client.jar"
MYTHS = ROOT / "analysis/mods/myths-and-legends.jar"
LM = ROOT / "analysis/mods/legendary-monuments.jar"
RES = ROOT / "src/main/resources"
ASSETS = RES / "assets/cobblelore"
DATA = RES / "data/cobblemon/spawn_pool_world"
DOCS = ROOT / "docs"

LEGENDARY_IDS: list[str] = []
ITEM_TO_SPECIES: dict[str, str] = {}

# When an ODS id has no Delta texture, copy from a legacy gimmick id if present.
TEXTURE_ALIAS: dict[str, str] = {
    "heart_diamond": "pink_diamond",
    "liberty_pass": "victory_star",
    "sun_flute": "solar_core",
    "moon_flute": "lunar_core",
    "scarlet_book": "koraidon_key",
    "violet_book": "miraidon_key",
    "iceroot_carrot": "frozen_hoof",
    "shaderoot_carrot": "ghostly_hoof",
    "cosmic_flute": "cosmic_core",
    "star_flute": "cosmic_core",
    "azelf_s_fang": "ruby_of_willpower",
    "mesprit_s_plume": "ruby_of_emotion",
    "uxie_s_claw": "ruby_of_knowledge",
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

# ODS Galar bird key items → Cobblemon spawn string (species + regional aspect).
ITEM_SPAWN_POKEMON: dict[str, str] = {
    "psychic_orb": "articuno galarian",
    "combat_orb": "zapdos galarian",
    "dark_orb": "moltres galarian",
}


def sanitize_spawn_condition(cond: dict | None) -> None:
    """CobbleLore: only the legendary key item gates spawns (no extra inventory items)."""
    if not cond:
        return
    cond.pop("item_requirement", None)


def spawn_pokemon_string(species: str, item_id: str) -> str:
    return ITEM_SPAWN_POKEMON.get(item_id, species)


def placeholder_color(item_id: str) -> tuple[int, int, int]:
    digest = hashlib.sha256(item_id.encode()).digest()
    return digest[0], digest[1], digest[2]


def write_placeholder_png(path: Path, item_id: str) -> None:
    color = placeholder_color(item_id)
    img = Image.new("RGBA", (16, 16), color + (255,))
    img.save(path)


def read_delta_texture(z: zipfile.ZipFile | None, item_id: str) -> bytes | None:
    if z is None:
        return None
    for candidate in (item_id, TEXTURE_ALIAS.get(item_id, "")):
        if not candidate:
            continue
        src = f"assets/cobblemon/textures/item/gimmick/{candidate}.png"
        try:
            return z.read(src)
        except KeyError:
            continue
    return None


def extract_textures() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    tex_dir = ASSETS / "textures/item"
    models_dir = ASSETS / "models/item"
    tex_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)

    keep = set(LEGENDARY_IDS)
    for path in tex_dir.glob("*.png"):
        if path.stem not in keep:
            path.unlink()
    for path in models_dir.glob("*.json"):
        if path.stem not in keep:
            path.unlink()

    delta_zip: zipfile.ZipFile | None = None
    if DELTA.is_file():
        delta_zip = zipfile.ZipFile(DELTA)
    else:
        print("WARN missing", DELTA, "— using placeholders and existing PNGs only")

    try:
        for item_id in LEGENDARY_IDS:
            tex_path = tex_dir / f"{item_id}.png"
            data = read_delta_texture(delta_zip, item_id) if delta_zip else None
            if data:
                tex_path.write_bytes(data)
            elif not tex_path.is_file():
                alias = TEXTURE_ALIAS.get(item_id)
                alias_path = tex_dir / f"{alias}.png" if alias else None
                if alias_path and alias_path.is_file():
                    shutil.copy(alias_path, tex_path)
                else:
                    write_placeholder_png(tex_path, item_id)
                    print("PLACEHOLDER texture", item_id)

            model = {
                "parent": "minecraft:item/generated",
                "textures": {"layer0": f"cobblelore:item/{item_id}"},
            }
            (models_dir / f"{item_id}.json").write_text(json.dumps(model, indent=2) + "\n")
    finally:
        if delta_zip:
            delta_zip.close()


def load_myths_pools() -> dict[str, dict]:
    if not MYTHS.is_file():
        print("WARN missing", MYTHS, "— spawn pools will be minimal cobblelore-only")
        return {}
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

    species_to_items: dict[str, list[str]] = {}
    for item_id, species in ITEM_TO_SPECIES.items():
        species_to_items.setdefault(species, []).append(item_id)

    for species, pool in myths_pools.items():
        if species in LM_PEDESTAL_SPECIES:
            continue
        item_ids = species_to_items.get(species)
        if not item_ids:
            continue
        new_pool = json.loads(json.dumps(pool))
        spawn_idx = 0
        for spawn in new_pool.get("spawns", []):
            cond = spawn.get("condition")
            if cond and "key_item" in cond:
                item_id = item_ids[min(spawn_idx, len(item_ids) - 1)]
                cond["key_item"] = f"cobblelore:{item_id}"
                sanitize_spawn_condition(cond)
                spawn["pokemon"] = spawn_pokemon_string(species, item_id)
                spawn_idx += 1
        for extra_item in item_ids[spawn_idx:]:
            template = new_pool["spawns"][0] if new_pool.get("spawns") else None
            if not template:
                break
            extra = json.loads(json.dumps(template))
            extra["id"] = f"cobblelore-{species}-{extra_item}"
            extra["pokemon"] = spawn_pokemon_string(species, extra_item)
            cond = extra.get("condition")
            if cond:
                cond["key_item"] = f"cobblelore:{extra_item}"
                sanitize_spawn_condition(cond)
            new_pool.setdefault("spawns", []).append(extra)
        for spawn in new_pool.get("spawns", []):
            sanitize_spawn_condition(spawn.get("condition"))
        out = DATA / f"cobblelore-{species}.json"
        out.write_text(json.dumps(new_pool, indent=2) + "\n")

    for species, item_ids in species_to_items.items():
        if species in myths_pools or species in LM_PEDESTAL_SPECIES:
            continue
        spawns = []
        for item_id in item_ids:
            spawns.append(
                {
                    "id": f"cobblelore-{species}-{item_id}",
                    "pokemon": spawn_pokemon_string(species, item_id),
                    "presets": ["natural"],
                    "type": "pokemon",
                    "context": "grounded",
                    "bucket": "ultra-rare",
                    "level": "50-70",
                    "weight": 0.1,
                    "condition": {"key_item": f"cobblelore:{item_id}"},
                }
            )
        minimal = {
            "enabled": True,
            "neededInstalledMods": [],
            "neededUninstalledMods": [],
            "spawns": spawns,
        }
        (DATA / f"cobblelore-{species}.json").write_text(json.dumps(minimal, indent=2) + "\n")

    for path in DATA.glob("cobblelore-*.json"):
        pool = json.loads(path.read_text(encoding="utf-8"))
        for spawn in pool.get("spawns", []):
            sanitize_spawn_condition(spawn.get("condition"))
        path.write_text(json.dumps(pool, indent=2) + "\n", encoding="utf-8")


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
    """Preserve optional metadata from disk; refresh items + mappings only."""
    meta = RES / "cobblelore"
    meta.mkdir(parents=True, exist_ok=True)
    path = meta / "legendary_items.json"
    extra: dict = {}
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        for key in ("source_ods", "item_labels_en"):
            if key in existing:
                extra[key] = existing[key]
    payload = {"items": LEGENDARY_IDS, "item_to_species": ITEM_TO_SPECIES, **extra}
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


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
