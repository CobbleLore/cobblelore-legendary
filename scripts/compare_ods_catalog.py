#!/usr/bin/env python3
"""Compare Item Leg.ods against cobblelore/legendary_items.json."""
from __future__ import annotations

import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ODS = Path(r"c:\Users\sweiz\Downloads\Item Leg liste.ods")
CATALOG = ROOT / "src/main/resources/cobblelore/legendary_items.json"
BUILD_CATALOG = ROOT / "build/resources/main/cobblelore/legendary_items.json"


def parse_ods(path: Path) -> list[tuple[str, str, str]]:
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("content.xml"))
    ns = {
        "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
        "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    }
    rows: list[tuple[str, str, str]] = []
    for table in root.findall(".//table:table", ns):
        for row in table.findall("table:table-row", ns):
            cells: list[str] = []
            for cell in row.findall("table:table-cell", ns):
                rep = int(
                    cell.get("{urn:oasis:names:tc:opendocument:xmlns:table:1.0}number-columns-repeated")
                    or 1
                )
                texts: list[str] = []
                for p in cell.findall(".//text:p", ns):
                    texts.extend(p.itertext())
                val = "".join(texts).strip()
                for _ in range(rep):
                    cells.append(val)
            if len(cells) >= 3 and cells[2].strip():
                rows.append((cells[0].strip(), cells[1].strip(), cells[2].strip()))
    return rows


def to_snake(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"['`]", "", s)
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return re.sub(r"_+", "_", s).strip("_")


def norm_poke(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load_catalog() -> dict:
    path = CATALOG if CATALOG.exists() else BUILD_CATALOG
    if not path.exists():
        raise SystemExit(f"Missing catalog at {CATALOG} or {BUILD_CATALOG}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    if not ODS.exists():
        raise SystemExit(f"Missing ODS: {ODS}")
    data = load_catalog()
    mod_items = set(data["items"])
    item_to_spec: dict[str, str] = data.get("item_to_species", {})
    spec_to_item = {norm_poke(sp): item for item, sp in item_to_spec.items()}

    ods_rows = parse_ods(ODS)
    print(f"ODS entries: {len(ods_rows)}")
    print(f"Mod items: {len(mod_items)}")

    # ODS english label -> mod id when spelling differs
    english_to_id: dict[str, str] = {}
    for item_id in mod_items:
        english_to_id[to_snake(item_id.replace("_", " "))] = item_id
        english_to_id[item_id] = item_id

    # ODS english label -> mod id when spelling differs
    english_fix: dict[str, str] = {
        "rubis_of_knowledge": "ruby_of_knowledge",
    }

    by_name_ok: list[tuple[str, str, str]] = []
    by_name_miss: list[tuple[str, str, str]] = []

    for poke, _fr, en in ods_rows:
        guess = to_snake(en)
        guess = english_fix.get(guess, guess)
        if guess in mod_items:
            by_name_ok.append((poke, en, guess))
        else:
            by_name_miss.append((poke, en, guess))

    matched_ids = {g for _, _, g in by_name_ok}
    mod_only_ids = sorted(mod_items - matched_ids)

    print(f"Match nom anglais ODS (snake) -> id mod: {len(by_name_ok)}/{len(ods_rows)}")

    if by_name_miss:
        print("\n--- Noms ODS sans item `cobblelore:` dans le mod ---")
        for poke, en, guess in by_name_miss:
            print(f"  {poke:22} | {en:28} | `{guess}`")

    if mod_only_ids:
        print(f"\n--- Items mod non listés dans ODS ({len(mod_only_ids)}) ---")
        for item in mod_only_ids:
            print(f"  cobblelore:{item} -> {item_to_spec.get(item, '?')}")

    print(
        f"\nConclusion (par nom d'item anglais): "
        f"{len(by_name_ok)}/{len(ods_rows)} lignes ODS ont un id mod; "
        f"le mod a {len(mod_items)} items dont {len(mod_only_ids)} absents du tableur."
    )


if __name__ == "__main__":
    main()
