from __future__ import annotations

from pathlib import Path
import json


SUPPORTED_ASSET_EXTENSIONS = {".fbx", ".glb", ".gltf", ".obj", ".blend", ".stl", ".abc", ".usd", ".usdz", ".dae"}


def classify_asset(path: Path) -> str:
    text = str(path).lower()
    if "\\assets\\ball\\" in text or "/assets/ball/" in text or "ball" in path.stem.lower():
        return "primary_ball_asset"
    if "\\assets\\hdri\\" in text or "/assets/hdri/" in text or path.suffix.lower() == ".exr":
        return "environment_asset"
    if "animated" in text or "effect" in text:
        return "animated_effect_asset"
    if path.suffix.lower() == ".blend":
        return "blend_scene_reference"
    return "scene_asset"


def build_asset_inventory(root: Path, project_dir: Path, output_json: Path, output_md: Path | None = None) -> dict:
    search_roots = [
        root / "assets",
        root,
        project_dir / "assets",
    ]
    excluded_parts = {
        "venvs",
        "manual",
        "renders",
        "output",
        "indexAI",
        ".git",
        ".aider.tags.cache.v4",
        "__pycache__",
    }

    assets: list[dict] = []
    seen: set[Path] = set()
    for search_root in search_roots:
        if not search_root.exists():
            continue
        for path in search_root.rglob("*"):
            if not path.is_file():
                continue
            if any(part in excluded_parts for part in path.parts):
                continue
            if path.suffix.lower() not in SUPPORTED_ASSET_EXTENSIONS:
                continue
            resolved = path.resolve(strict=False)
            if resolved in seen:
                continue
            seen.add(resolved)
            try:
                size = path.stat().st_size
            except OSError:
                size = 0
            rel = str(path)
            try:
                rel = str(path.relative_to(root))
            except ValueError:
                pass
            assets.append(
                {
                    "name": path.stem,
                    "role": classify_asset(path),
                    "path": str(path),
                    "relative_path": rel,
                    "extension": path.suffix.lower(),
                    "bytes": size,
                }
            )

    priority = {
        "primary_ball_asset": 0,
        "animated_effect_asset": 1,
        "blend_scene_reference": 2,
        "environment_asset": 3,
        "scene_asset": 4,
    }
    assets.sort(key=lambda item: (priority.get(item["role"], 99), item["relative_path"].lower()))

    inventory = {
        "kind": "spaziotempo_asset_inventory",
        "root": str(root),
        "project_dir": str(project_dir),
        "asset_count": len(assets),
        "assets": assets,
        "notes": [
            "Use primary_ball_asset as known existing ball/hero asset when the scene director asks for ball or dual focus.",
            "Do not assume imported .blend files are available inside the current Blender scene; import/link explicitly in generated scripts.",
        ],
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(inventory, indent=2, ensure_ascii=False), encoding="utf-8")

    if output_md:
        lines = [
            "# Spaziotempo Asset Inventory\n\n",
            f"Root: `{root}`\n\n",
            f"Assets: `{len(assets)}`\n\n",
        ]
        for asset in assets:
            lines.append(f"- `{asset['role']}` `{asset['name']}` -> `{asset['path']}`\n")
        output_md.parent.mkdir(parents=True, exist_ok=True)
        output_md.write_text("".join(lines), encoding="utf-8")

    return inventory
