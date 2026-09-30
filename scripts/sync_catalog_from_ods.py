#!/usr/bin/env python3
"""Build cobblelore/legendary_items.json from Item Leg liste.ods (source of truth)."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from odf.opendocument import load
from odf.table import Table, TableCell, TableRow
from odf.text import P

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ODS = Path.home() / "Downloads" / "Item Leg liste.ods"
OUT = ROOT / "src/main/resources/cobblelore/legendary_items.json"
LANG_OUT = ROOT / "src/main/resources/assets/cobblelore/lang/en_us.json"

# French display name (first column) -> Cobblemon species id
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
    raise KeyError(f"No species mapping for French name: {french_name!r}")


def read_ods_rows(ods_path: Path) -> list[tuple[str, str, str]]:
    doc = load(str(ods_path))
    rows: list[tuple[str, str, str]] = []
    for table in doc.getElementsByType(Table):
        for row in table.getElementsByType(TableRow):
            cells = [cell_text(c) for c in row.getElementsByType(TableCell)]
            if len(cells) < 3:
                continue
            french, _fr_item, english = cells[0], cells[1], cells[2]
            if not french or french.lower() in {"pokemon", "pokémon"}:
                continue
            rows.append((french.strip(), english.strip(), _fr_item.strip()))
    return rows


def write_lang(items: list[str], labels: dict[str, str]) -> None:
    lines = {
        "itemGroup.cobblelore.legendary": "CobbleLore Legendary Items",
    }
    for item_id in items:
        label = labels.get(item_id, item_id.replace("_", " ").title())
        lines[f"item.cobblelore.{item_id}"] = label
    LANG_OUT.parent.mkdir(parents=True, exist_ok=True)
    LANG_OUT.write_text(json.dumps(lines, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    import sys

    ods_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ODS
    if not ods_path.is_file():
        raise SystemExit(f"ODS not found: {ods_path}")

    rows = read_ods_rows(ods_path)
    items: list[str] = []
    item_to_species: dict[str, str] = {}
    labels_en: dict[str, str] = {}
    seen_items: set[str] = set()

    for french, english, _ in rows:
        item_id = english_to_item_id(english)
        species = resolve_species(french)
        if item_id in seen_items:
            raise SystemExit(f"Duplicate item id {item_id!r} in ODS")
        seen_items.add(item_id)
        items.append(item_id)
        item_to_species[item_id] = species
        labels_en[item_id] = english

    payload = {
        "source_ods": ods_path.name,
        "items": items,
        "item_to_species": item_to_species,
        "item_labels_en": labels_en,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_lang(items, labels_en)
    print(f"Wrote {len(items)} items to {OUT}")


if __name__ == "__main__":
    main()
