# Project Code Chunk 188/212

- File: `Tools/workflow/asset_inventory.py`
- Part: `1`
- Lines: `1-110`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `json`
- Functions: `classify_asset(path)` line 10; `build_asset_inventory(root, project_dir, output_json, output_md)` line 23
- Assignments: `SUPPORTED_ASSET_EXTENSIONS`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from pathlib import Path
00004: import json
00005: 
00006: 
00007: SUPPORTED_ASSET_EXTENSIONS = {".fbx", ".glb", ".gltf", ".obj", ".blend", ".stl", ".abc", ".usd", ".usdz", ".dae"}
00008: 
00009: 
00010: def classify_asset(path: Path) -> str:
00011:     text = str(path).lower()
00012:     if "\\assets\\ball\\" in text or "/assets/ball/" in text or "ball" in path.stem.lower():
00013:         return "primary_ball_asset"
00014:     if "\\assets\\hdri\\" in text or "/assets/hdri/" in text or path.suffix.lower() == ".exr":
00015:         return "environment_asset"
00016:     if "animated" in text or "effect" in text:
00017:         return "animated_effect_asset"
00018:     if path.suffix.lower() == ".blend":
00019:         return "blend_scene_reference"
00020:     return "scene_asset"
00021: 
00022: 
00023: def build_asset_inventory(root: Path, project_dir: Path, output_json: Path, output_md: Path | None = None) -> dict:
00024:     search_roots = [
00025:         root / "assets",
00026:         root,
00027:         project_dir / "assets",
00028:     ]
00029:     excluded_parts = {
00030:         "venvs",
00031:         "manual",
00032:         "renders",
00033:         "output",
00034:         "indexAI",
00035:         ".git",
00036:         ".aider.tags.cache.v4",
00037:         "__pycache__",
00038:     }
00039: 
00040:     assets: list[dict] = []
00041:     seen: set[Path] = set()
00042:     for search_root in search_roots:
00043:         if not search_root.exists():
00044:             continue
00045:         for path in search_root.rglob("*"):
00046:             if not path.is_file():
00047:                 continue
00048:             if any(part in excluded_parts for part in path.parts):
00049:                 continue
00050:             if path.suffix.lower() not in SUPPORTED_ASSET_EXTENSIONS:
00051:                 continue
00052:             resolved = path.resolve(strict=False)
00053:             if resolved in seen:
00054:                 continue
00055:             seen.add(resolved)
00056:             try:
00057:                 size = path.stat().st_size
00058:             except OSError:
00059:                 size = 0
00060:             rel = str(path)
00061:             try:
00062:                 rel = str(path.relative_to(root))
00063:             except ValueError:
00064:                 pass
00065:             assets.append(
00066:                 {
00067:                     "name": path.stem,
00068:                     "role": classify_asset(path),
00069:                     "path": str(path),
00070:                     "relative_path": rel,
00071:                     "extension": path.suffix.lower(),
00072:                     "bytes": size,
00073:                 }
00074:             )
00075: 
00076:     priority = {
00077:         "primary_ball_asset": 0,
00078:         "animated_effect_asset": 1,
00079:         "blend_scene_reference": 2,
00080:         "environment_asset": 3,
00081:         "scene_asset": 4,
00082:     }
00083:     assets.sort(key=lambda item: (priority.get(item["role"], 99), item["relative_path"].lower()))
00084: 
00085:     inventory = {
00086:         "kind": "spaziotempo_asset_inventory",
00087:         "root": str(root),
00088:         "project_dir": str(project_dir),
00089:         "asset_count": len(assets),
00090:         "assets": assets,
00091:         "notes": [
00092:             "Use primary_ball_asset as known existing ball/hero asset when the scene director asks for ball or dual focus.",
00093:             "Do not assume imported .blend files are available inside the current Blender scene; import/link explicitly in generated scripts.",
00094:         ],
00095:     }
00096:     output_json.parent.mkdir(parents=True, exist_ok=True)
00097:     output_json.write_text(json.dumps(inventory, indent=2, ensure_ascii=False), encoding="utf-8")
00098: 
00099:     if output_md:
00100:         lines = [
00101:             "# Spaziotempo Asset Inventory\n\n",
00102:             f"Root: `{root}`\n\n",
00103:             f"Assets: `{len(assets)}`\n\n",
00104:         ]
00105:         for asset in assets:
00106:             lines.append(f"- `{asset['role']}` `{asset['name']}` -> `{asset['path']}`\n")
00107:         output_md.parent.mkdir(parents=True, exist_ok=True)
00108:         output_md.write_text("".join(lines), encoding="utf-8")
00109: 
00110:     return inventory
```
