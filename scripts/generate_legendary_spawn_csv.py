#!/usr/bin/env python3
"""Player-facing CSV: legendary spawn methods, items, biomes (ODS + pools + LM pedestals)."""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path

from odf.opendocument import load
from odf.table import Table, TableCell, TableRow
from odf.text import P

MOD_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = MOD_ROOT.parents[1]
ODS_DEFAULT = Path.home() / "Downloads" / "Item Leg liste.ods"
CATALOG = MOD_ROOT / "src/main/resources/cobblelore/legendary_items.json"
COBBLELORE_POOLS = MOD_ROOT / "src/main/resources/data/cobblemon/spawn_pool_world"
MYTHS_POOLS = (
    REPO_ROOT / "pack/server/datapacks/myths-and-legends/data/cobblemon/spawn_pool_world"
)
OUT_CSV = REPO_ROOT / "docs/legendary-spawn-guide.csv"

LM_PEDESTAL_SPECIES = {
    "mew",
    "dialga",
    "palkia",
    "giratina",
    "glastrier",
    "spectrier",
    "latias",
    "latios",
    "entei",
    "raikou",
    "suicune",
    "heatran",
    "hooh",
    "lugia",
    "hoopa",
    "zekrom",
    "reshiram",
    "kyurem",
    "zacian",
    "zamazenta",
}

PEDESTAL_COBLELORE_ITEM: dict[str, str] = {
    "mew": "rare_dna",
    "dialga": "adamant_orb",
    "palkia": "lustrous_orb",
    "giratina": "griseous_orb",
    "glastrier": "iceroot_carrot",
    "spectrier": "shaderoot_carrot",
    "latias": "red_eon_ticket",
    "latios": "blue_eon_ticket",
    "entei": "sacred_flame",
    "raikou": "sacred_lightning",
    "suicune": "sacred_droplet",
    "heatran": "magma_chunk",
    "hooh": "rainbow_wing",
    "lugia": "silver_wing",
    "hoopa": "ring",
    "reshiram": "light_stone",
    "zekrom": "dark_stone",
    "kyurem": "gray_stone",
    "zacian": "rusted_sword",
    "zamazenta": "rusted_shield",
}

PEDESTAL_OTHER_ITEMS: dict[str, list[str]] = {}

MYTHS_FILE_ALIASES: dict[str, str] = {
    "enamorus": "namorus",
    "zygarde": "zygarde100",
}

# French display name (ODS col 1) -> Cobblemon species id
FRENCH_TO_SPECIES: dict[str, str] = {
    "Mew": "mew",
    "Celebi": "celebi",
    "Jirachi": "jirachi",
    "Deoxys": "deoxys",
    "Manaphy": "manaphy",
    "Darkrai": "darkrai",
    "Shaymn": "shaymin",
    "Shaymin": "shaymin",
    "Arceus": "arceus",
    "Victini": "victini",
    "Keldeo": "keldeo",
    "Meloetta": "meloetta",
    "Genesect": "genesect",
    "Diancie": "diancie",
    "Hoopa": "hoopa",
    "Volcanion": "volcanion",
    "Magearna": "magearna",
    "Marshadow": "marshadow",
    "Meltan": "meltan",
    "Zarude": "zarude",
    "Péchaminus": "pecharunt",
    "Pechaminus": "pecharunt",
    "Artikodin": "articuno",
    "Électhor": "zapdos",
    "Electhor": "zapdos",
    "Sulfura": "moltres",
    "Mewtwo": "mewtwo",
    "Raikou": "raikou",
    "Entei": "entei",
    "Suicune": "suicune",
    "Lugia": "lugia",
    "Ho-Oh": "hooh",
    "Registeel": "registeel",
    "Regice": "regice",
    "Regirock": "regirock",
    "Regieleki": "regieleki",
    "Regidraco": "regidrago",
    "Regigigas": "regigigas",
    "Latios": "latios",
    "Latias": "latias",
    "Kyogre": "kyogre",
    "Groudon": "groudon",
    "Rayquazza": "rayquaza",
    "Rayquaza": "rayquaza",
    "Créfadet": "azelf",
    "Créfollet": "mesprit",
    "Créhelf": "uxie",
    "Dialga": "dialga",
    "Palkia": "palkia",
    "Giratina": "giratina",
    "Heatran": "heatran",
    "Cresselia": "cresselia",
    "Viridium": "virizion",
    "Terrakium": "terrakion",
    "Cobaltium": "cobalion",
    "Fulguris": "thundurus",
    "Boréas": "tornadus",
    "Boreas": "tornadus",
    "Démétéros": "landorus",
    "Demeteros": "landorus",
    "Amovénus": "enamorus",
    "Amovenus": "enamorus",
    "Reshiram": "reshiram",
    "Zekrom": "zekrom",
    "Kyurem": "kyurem",
    "Xerneas": "xerneas",
    "Yveltal": "yveltal",
    "Zygarde": "zygarde",
    "Silvallié": "silvally",
    "Silvallie": "silvally",
    "Tokorico": "tapukoko",
    "Tokopiyon": "tapulele",
    "Tokotoro": "tapubulu",
    "Tokopisco": "tapufini",
    "Solgaleo": "solgaleo",
    "Lunala": "lunala",
    "Necrozma": "necrozma",
    "Zacian": "zacian",
    "Zamazenta": "zamazenta",
    "Éthernathos": "eternatus",
    "Ethernathos": "eternatus",
    "Calyrex": "calyrex",
    "Blizzeval": "glastrier",
    "Spectreval": "spectrier",
    "Miraidon": "miraidon",
    "Koraidon": "koraidon",
    "Félicanis": "okidogi",
    "Felicanis": "okidogi",
    "Fortusimia": "munkidori",
    "Favianos": "fezandipiti",
    "Ogerpon": "ogerpon",
    "Terapagos": "terapagos",
    "Artikodin de Galar": "articuno",
    "Électhor de Galar": "zapdos",
    "Electhor de Galar": "zapdos",
    "Sulfura de Galar": "moltres",
    "Baojian": "chienpao",
    "Yuyu": "chiyu",
    "Chongjian": "wochien",
    "Dinglu": "tinglu",
    "Zeraora": "zeraora",
    "Cosmog": "cosmog",
    "Cosmovum": "cosmoem",
    "Phione": "phione",
    "Type:0": "typenull",
    "Type:Null": "typenull",
    "Wushours": "kubfu",
}

ENGLISH_TO_ITEM_ID: dict[str, str] = {
    "Azelf's Fang": "azelf_s_fang",
    "Mesprit's Plume": "mesprit_s_plume",
    "Uxie's Claw": "uxie_s_claw",
    "Toxic Riboon": "toxic_riboon",
    "Star flute": "star_flute",
    "Star Flute": "star_flute",
}


def normalize_key(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.strip()


def cell_text(cell: TableCell) -> str:
    parts: list[str] = []
    for paragraph in cell.getElementsByType(P):
        for node in paragraph.childNodes:
            if hasattr(node, "data"):
                parts.append(node.data)
    return " ".join(parts).strip()


def english_to_item_id(english: str) -> str:
    english = english.strip()
    if english in ENGLISH_TO_ITEM_ID:
        return ENGLISH_TO_ITEM_ID[english]
    slug = re.sub(r"[^A-Za-z0-9]+", "_", english).strip("_").lower()
    return slug


def resolve_species(french_name: str) -> str:
    key = normalize_key(french_name)
    for candidate, species in FRENCH_TO_SPECIES.items():
        if normalize_key(candidate) == key:
            return species
    raise KeyError(f"No species mapping for {french_name!r}")


def read_ods_rows(ods_path: Path) -> list[tuple[str, str, str]]:
    doc = load(str(ods_path))
    rows: list[tuple[str, str, str]] = []
    for table in doc.getElementsByType(Table):
        for row in table.getElementsByType(TableRow):
            cells = [cell_text(c) for c in row.getElementsByType(TableCell)]
            if len(cells) < 3:
                continue
            french, fr_item, english = cells[0], cells[1], cells[2]
            if not french or french.lower() in {"pokemon", "pokémon"}:
                continue
            rows.append((french.strip(), fr_item.strip(), english.strip()))
    return rows


def load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def myths_pool_path(species: str) -> Path | None:
    name = MYTHS_FILE_ALIASES.get(species, species)
    path = MYTHS_POOLS / f"mythsandlegends-{name}.json"
    return path if path.is_file() else None


def collect_spawn_info(pool: dict, key_item_filter: str | None) -> dict:
    biomes: set[str] = set()
    levels: set[str] = set()
    buckets: set[str] = set()
    extras: list[str] = []
    contexts: set[str] = set()
    has_biome = False

    for spawn in pool.get("spawns", []):
        cond = spawn.get("condition") or {}
        if key_item_filter:
            ki = cond.get("key_item", "")
            if ki and ki != f"cobblelore:{key_item_filter}" and not ki.endswith(f":{key_item_filter}"):
                continue
        if spawn.get("level"):
            levels.add(str(spawn["level"]))
        if spawn.get("bucket"):
            buckets.add(str(spawn["bucket"]))
        if spawn.get("context"):
            contexts.add(str(spawn["context"]))
        if cond.get("biomes"):
            has_biome = True
            for b in cond["biomes"]:
                biomes.add(str(b))
        for key in ("time_range", "moon_phase", "structure", "min_sky_light", "max_sky_light"):
            if key in cond:
                extras.append(f"{key}={cond[key]}")
        if cond.get("item_requirement"):
            for req in cond["item_requirement"]:
                rid = req.get("id", "?")
                count = req.get("count", 1)
                consume = req.get("consume", False)
                extras.append(f"inventaire {rid} x{count}" + (" (consommé)" if consume else ""))

    return {
        "biomes": sorted(biomes),
        "has_biome": has_biome,
        "levels": sorted(levels),
        "buckets": sorted(buckets),
        "contexts": sorted(contexts),
        "extras": extras,
    }


def spawn_info_for(species: str, item_id: str) -> tuple[dict, str, str]:
    """Returns (info, biome_source, biomes_display)."""
    cobble_path = COBBLELORE_POOLS / f"cobblelore-{species}.json"
    cobble = load_json(cobble_path)
    cobble_info: dict | None = None
    if cobble and cobble.get("enabled", True):
        cobble_info = collect_spawn_info(cobble, item_id)

    myths_path = myths_pool_path(species)
    myths_info: dict | None = None
    if myths_path:
        myths = load_json(myths_path)
        if myths:
            myths_info = collect_spawn_info(myths, None)

    # Prefer cobblelore levels/bucket; biomes from cobblelore if present else M&L reference
    if cobble_info:
        info = cobble_info
        if info["has_biome"]:
            return info, "pool cobblelore (mod)", " | ".join(info["biomes"])
        if myths_info and myths_info["biomes"]:
            merged = {**info}
            merged["biomes"] = myths_info["biomes"]
            merged["has_biome"] = True
            if not merged["levels"] and myths_info["levels"]:
                merged["levels"] = myths_info["levels"]
            display = " | ".join(myths_info["biomes"])
            return merged, "réf. Myths & Legends (biomes cibles)", display
        return info, "pool cobblelore minimal (sans biome)", "Tous biomes (pool minimal actuel)"

    if myths_info:
        display = " | ".join(myths_info["biomes"]) if myths_info["biomes"] else "Voir mod M&L"
        return myths_info, "réf. Myths & Legends", display

    return {
        "biomes": [],
        "has_biome": False,
        "levels": [],
        "buckets": ["ultra-rare"],
        "contexts": ["grounded"],
        "extras": [],
    }, "aucun pool détaillé", "Tous biomes (spawn minimal)"


def player_steps_pedestal(species: str, cobble_items: list[str], other_items: list[str]) -> str:
    items_txt = ", ".join(f"cobblelore:{i}" for i in cobble_items)
    if other_items:
        items_txt += " + " + ", ".join(other_items)
    return (
        f"Trouver un monument Legendary Monuments ({species}). "
        f"Placer sur le pedestal : {items_txt}. "
        "Interagir pour invoquer (l'item pedestal est consommé)."
    )


def player_steps_wild(item_id: str, biomes: list[str], has_biome: bool) -> str:
    base = (
        f"Obtenir cobblelore:{item_id}, le garder dans l'inventaire, "
        "explorer en surface jusqu'à un spawn Cobblemon ultra-rare."
    )
    if has_biome and biomes:
        return base + " Privilégier les biomes listés."
    if not has_biome:
        return base + " (Pool actuel sans biome = possible sur la plupart des biomes.)"
    return base


def main() -> None:
    import sys

    ods_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ODS_DEFAULT
    if not ods_path.is_file():
        raise SystemExit(f"ODS not found: {ods_path}")
    if not CATALOG.is_file():
        raise SystemExit(f"Missing catalog: {CATALOG}")

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    item_to_species: dict[str, str] = catalog["item_to_species"]
    labels_en: dict[str, str] = catalog.get("item_labels_en", {})

    rows_out: list[dict[str, str]] = []

    for pokemon_fr, item_fr, item_en in read_ods_rows(ods_path):
        item_id = english_to_item_id(item_en)
        species = resolve_species(pokemon_fr)
        expected = item_to_species.get(item_id)
        note_mismatch = ""
        if expected and expected != species:
            note_mismatch = f"Catalogue espèce={expected} vs ODS ligne={species}. "

        if species in LM_PEDESTAL_SPECIES and PEDESTAL_COBLELORE_ITEM.get(species) == item_id:
            spawn_method = "Legendary Monuments — pedestal"
            other = PEDESTAL_OTHER_ITEMS.get(species, [])
            cobble_items = [item_id]
            items_cobblelore = "; ".join(f"cobblelore:{x}" for x in cobble_items)
            items_other = "; ".join(other)
            biomes_str = "Structure LM (pas de spawn sauvage cobblelore pour cette espèce)"
            info = {"levels": [], "buckets": [], "contexts": [], "extras": [], "has_biome": False}
            biome_source = "pedestal LM"
            player = player_steps_pedestal(species, cobble_items, other)
            notes = (
                note_mismatch
                + "Pas de pool spawn sauvage cobblelore. "
                + "Piste Arc Phone / exploration LM. "
                + "Distribution des items cobblelore : à définir côté serveur."
            )
        else:
            spawn_method = "Spawn sauvage Cobblemon (key_item)"
            items_cobblelore = f"cobblelore:{item_id}"
            items_other = ""
            info, biome_source, biomes_str = spawn_info_for(species, item_id)
            player = player_steps_wild(item_id, info["biomes"], info["has_biome"])
            notes = note_mismatch + (
                "Pools M&L vanilla désactivés (datapack cobblelore-myths-spawn-override). "
            )
            if "Galar" in pokemon_fr or "de Galar" in pokemon_fr:
                notes += "Même espèce Cobblemon que la forme Kanto ; forme Galar non séparée dans le spawn. "
            if info["extras"]:
                notes += "Conditions spawn cobblelore : " + "; ".join(dict.fromkeys(info["extras"])) + ". "
            notes += "Obtenir l'item : pas de loot/craft cobblelore documenté (event/admin/quêtes à venir)."

        rows_out.append(
            {
                "pokemon_fr": pokemon_fr,
                "pokemon_id": species,
                "item_id": item_id,
                "item_label_en": labels_en.get(item_id, item_en),
                "item_label_fr": item_fr,
                "spawn_method": spawn_method,
                "player_how_to_fr": player,
                "items_cobblelore": items_cobblelore,
                "items_other_mods": items_other,
                "biomes": biomes_str,
                "biome_source": biome_source,
                "level_range": " | ".join(info.get("levels", [])),
                "spawn_bucket": " | ".join(info.get("buckets", [])),
                "spawn_context": " | ".join(info.get("contexts", [])),
                "extra_spawn_conditions": " | ".join(dict.fromkeys(info.get("extras", []))),
                "notes": notes.strip(),
            }
        )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows_out[0].keys()) if rows_out else []
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"Wrote {len(rows_out)} rows -> {OUT_CSV}")


if __name__ == "__main__":
    main()
