#!/usr/bin/env python3
"""Regenerate docs/TABLEAU-ITEMS-LEGENDAIRES.md from cobblelore/legendary_items.json."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "src/main/resources"
DOCS = ROOT / "docs"

MONUMENT_ONLY = {
    "dialga": "adamant_orb",
    "mew": "odd_sea_egg",
    "latias": "psychic_orb",
    "latios": "combat_orb",
    "zacian": "rusted_sword",
}

LM_PED = {
    "mew", "dialga", "palkia", "giratina", "glastrier", "spectrier", "latias", "latios",
    "entei", "raikou", "suicune", "heatran", "hooh", "lugia", "hoopa", "zekrom", "reshiram",
    "kyurem", "zacian", "zamazenta",
}


def load_catalog() -> tuple[list[str], dict[str, str]]:
    data = json.loads((RES / "cobblelore/legendary_items.json").read_text(encoding="utf-8"))
    return data["items"], data["item_to_species"]


def load_spawn_keys() -> dict[str, set[str]]:
    species_keys: dict[str, set[str]] = defaultdict(set)
    pool_dir = RES / "data/cobblemon/spawn_pool_world"
    for f in pool_dir.glob("cobblelore-*.json"):
        sp = f.stem.replace("cobblelore-", "")
        j = json.loads(f.read_text(encoding="utf-8"))
        for s in j.get("spawns", []):
            ki = s.get("condition", {}).get("key_item", "")
            if ki.startswith("cobblelore:"):
                species_keys[sp].add(ki.split(":", 1)[1])
    return species_keys


def describe_use(item: str, sp: str, species_keys: dict[str, set[str]]) -> str:
    if MONUMENT_ONLY.get(sp) == item:
        return "Monument (pedestal) uniquement"
    in_pool = item in species_keys.get(sp, set())
    parts: list[str] = []
    if in_pool:
        parts.append("Spawn monde")
    if sp in LM_PED and sp not in MONUMENT_ONLY:
        parts.append("Monument (pedestal)")
    return " · ".join(parts) if parts else "—"


def main() -> None:
    items_order, item_to_species = load_catalog()
    species_keys = load_spawn_keys()
    by_species: dict[str, list[str]] = defaultdict(list)
    for it, sp in item_to_species.items():
        by_species[sp].append(it)

    lines = [
        "# Tableau des items légendaires CobbleLore",
        "",
        f"**{len(items_order)} items** — **1 item par espèce** (doublons retirés du mod).",
        "",
        "| Item | Pokémon | À quoi ça sert |",
        "|------|---------|----------------|",
    ]
    for item in items_order:
        sp = item_to_species[item]
        lines.append(f"| `{item}` | {sp} | {describe_use(item, sp, species_keys)} |")

    spawn_items = sum(1 for it in items_order if it in species_keys.get(item_to_species[it], set()))
    lines.extend(
        [
            "",
            "## Espèces monument-only (pas de spawn monde)",
            "",
        ]
    )
    for sp, it in sorted(MONUMENT_ONLY.items()):
        lines.append(f"- **{sp}** → `{it}`")

    lines.extend(
        [
            "",
            "## Compteur",
            "",
            f"- Items : **{len(items_order)}**",
            f"- Espèces : **{len(by_species)}**",
            f"- Items avec spawn monde : **{spawn_items}**",
            f"- Espèces monument-only : **{len(MONUMENT_ONLY)}**",
            "",
        ]
    )
    (DOCS / "TABLEAU-ITEMS-LEGENDAIRES.md").write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", DOCS / "TABLEAU-ITEMS-LEGENDAIRES.md")


if __name__ == "__main__":
    main()
