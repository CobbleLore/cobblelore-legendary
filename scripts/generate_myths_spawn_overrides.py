#!/usr/bin/env python3
"""Emit datapack + mod overrides that disable vanilla Myths & Legends spawn pools."""
from __future__ import annotations

import json
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
MOD_ROOT = Path(__file__).resolve().parents[1]
MYTHS_SPAWN_DIR = (
    REPO / "pack/server/datapacks/myths-and-legends/data/cobblemon/spawn_pool_world"
)
MYTHS_JAR = REPO / "pack/server/mods/MythsAndLegends-fabric-1.9.0.jar"
OUT_ROOTS = [
    REPO / "pack/server/datapacks/cobblelore-myths-spawn-override",
    REPO
    / "infrastructure/minecraft/cobblemon/datapacks/cobblelore-myths-spawn-override",
]

DISABLED_POOL = {
    "_comment": "CobbleLore: mythsandlegends:* key_item spawns off; cobblelore-legendary mod pools apply.",
    "enabled": False,
    "neededInstalledMods": [],
    "neededUninstalledMods": [],
    "spawns": [],
}

PACK_MCMETA = {
    "pack": {
        "description": "CobbleLore — disable Myths & Legends vanilla spawn pools",
        "pack_format": 48,
        "supported_formats": {"min_inclusive": 48, "max_inclusive": 48},
    }
}


def list_myths_pool_filenames() -> list[str]:
    names: set[str] = set()
    if MYTHS_SPAWN_DIR.is_dir():
        for path in MYTHS_SPAWN_DIR.glob("mythsandlegends-*.json"):
            names.add(path.name)
    if MYTHS_JAR.is_file():
        with zipfile.ZipFile(MYTHS_JAR) as jar:
            for entry in jar.namelist():
                if not entry.startswith("data/cobblemon/spawn_pool_world/mythsandlegends-"):
                    continue
                if not entry.endswith(".json"):
                    continue
                names.add(Path(entry).name)
    return sorted(names)


def write_mod_embedded_overrides(filenames: list[str]) -> None:
    """Same disable JSON inside cobblelore-legendary so mod-jar M&L pools are overridden."""
    spawn_out = MOD_ROOT / "src/main/resources/data/cobblemon/spawn_pool_world"
    spawn_out.mkdir(parents=True, exist_ok=True)
    for stale in spawn_out.glob("mythsandlegends-*.json"):
        stale.unlink()
    for name in filenames:
        (spawn_out / name).write_text(
            json.dumps(DISABLED_POOL, indent=2) + "\n", encoding="utf-8"
        )
    print(f"Wrote {len(filenames)} embedded overrides -> {spawn_out}")


def main() -> None:
    sources = list_myths_pool_filenames()
    if not sources:
        raise SystemExit(
            f"No mythsandlegends-*.json pools found under {MYTHS_SPAWN_DIR} or {MYTHS_JAR}"
        )

    for root in OUT_ROOTS:
        spawn_out = root / "data/cobblemon/spawn_pool_world"
        spawn_out.mkdir(parents=True, exist_ok=True)
        for stale in spawn_out.glob("mythsandlegends-*.json"):
            stale.unlink()
        for name in sources:
            dest = spawn_out / name
            dest.write_text(json.dumps(DISABLED_POOL, indent=2) + "\n", encoding="utf-8")
        (root / "pack.mcmeta").write_text(
            json.dumps(PACK_MCMETA, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Wrote {len(sources)} overrides -> {root}")

    write_mod_embedded_overrides(sources)


if __name__ == "__main__":
    main()
