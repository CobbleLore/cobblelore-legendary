#!/usr/bin/env python3
"""Regenerate docs/TABLEAU-ITEMS-LEGENDAIRES.md from cobblelore/legendary_items.json."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "src/main/resources"
DOCS = ROOT / "docs"

# Legendary Monuments 8.1 — espèces avec pedestal dédié (priorité sur spawn monde).
LM_PEDESTAL_SPECIES = frozenset(
    {
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
)


def load_catalog() -> tuple[list[str], dict[str, str]]:
    data = json.loads((RES / "cobblelore/legendary_items.json").read_text(encoding="utf-8"))
    return data["items"], data["item_to_species"]


def load_spawn_keys() -> dict[str, set[str]]:
    species_keys: dict[str, set[str]] = defaultdict(set)
    pool_dir = RES / "data/cobblemon/spawn_pool_world"
    if not pool_dir.exists():
        return species_keys
    for f in pool_dir.glob("cobblelore-*.json"):
        sp = f.stem.replace("cobblelore-", "")
        j = json.loads(f.read_text(encoding="utf-8"))
        for s in j.get("spawns", []):
            ki = s.get("condition", {}).get("key_item", "")
            if ki.startswith("cobblelore:"):
                species_keys[sp].add(ki.split(":", 1)[1])
    return species_keys


def describe_use(item: str, sp: str, species_keys: dict[str, set[str]]) -> str:
    if sp in LM_PEDESTAL_SPECIES:
        return "Monument (pedestal) uniquement"
    if item in species_keys.get(sp, set()):
        return "Spawn monde (item + biomes)"
    return "—"


def main() -> None:
    items_order, item_to_species = load_catalog()
    species_keys = load_spawn_keys()

    lines = [
        "# Tableau des items légendaires CobbleLore",
        "",
        f"**{len(items_order)} items** — **1 item par espèce**.",
        "",
        "**Règle serveur** : pedestal LM possible → **monument seulement** (pas de spawn monde). "
        "Sinon → **spawn monde** (item + biomes, Myths and Legends). **Une seule voie par légendaire.**",
        "",
        "| Item | Pokémon | Voie |",
        "|------|---------|------|",
    ]
    for item in items_order:
        sp = item_to_species[item]
        lines.append(f"| `{item}` | {sp} | {describe_use(item, sp, species_keys)} |")

    monument = sorted(s for s in LM_PEDESTAL_SPECIES if s in set(item_to_species.values()))
    spawn_count = sum(
        1 for it in items_order if item_to_species[it] not in LM_PEDESTAL_SPECIES
    )

    lines.extend(["", "## Monument (pedestal) uniquement", ""])
    for sp in monument:
        it = next(k for k, v in item_to_species.items() if v == sp)
        lines.append(f"- **{sp}** → `{it}`")

    lines.extend(
        [
            "",
            "## Compteur",
            "",
            f"- Items : **{len(items_order)}**",
            f"- Spawn monde : **{spawn_count}** espèces",
            f"- Monument only : **{len(monument)}** espèces",
            "",
        ]
    )
    (DOCS / "TABLEAU-ITEMS-LEGENDAIRES.md").write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", DOCS / "TABLEAU-ITEMS-LEGENDAIRES.md")


if __name__ == "__main__":
    main()
