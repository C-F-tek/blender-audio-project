"""Inventory files present in each root ``Tools/<area>`` folder."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from Tools.docs.docs_hygiene.repo_tool_surface_audit import repo_root_from

ROOT_ALLOWLIST = {"__init__.py", "__main__.py", "dispatch.py", "README.md"}
CODE_SUFFIXES = {".py", ".ps1"}


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def exposes_main(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    return "def main(" in text or "def main()" in text or "if __name__" in text


def classify_root_file(path: Path) -> str:
    if path.name in ROOT_ALLOWLIST:
        return "allowed_surface"
    if path.name.endswith(("_cli.py", "_core.py", "_view.py", "_model.py", "_controller.py")):
        return "internal_root_module"
    if path.suffix == ".ps1":
        return "root_powershell_entrypoint"
    if path.suffix in CODE_SUFFIXES and exposes_main(path):
        return "root_script_entrypoint"
    if path.suffix in CODE_SUFFIXES:
        return "root_code_helper"
    return "root_data_or_doc"


def package_info(root: Path, path: Path) -> dict[str, Any]:
    files = [item for item in path.iterdir() if item.is_file()]
    return {
        "path": rel(root, path),
        "has_init": (path / "__init__.py").exists(),
        "has_cli": (path / "cli.py").exists(),
        "file_count": len(files),
        "suffixes": dict(Counter(item.suffix or "<none>" for item in files).most_common()),
    }


def area_inventory(root: Path, area_dir: Path) -> dict[str, Any]:
    root_files: list[dict[str, Any]] = []
    packages: list[dict[str, Any]] = []
    for item in sorted(area_dir.iterdir()):
        if item.is_file():
            kind = classify_root_file(item)
            root_files.append(
                {
                    "path": rel(root, item),
                    "name": item.name,
                    "suffix": item.suffix or "<none>",
                    "kind": kind,
                    "line_count": len(item.read_text(encoding="utf-8", errors="ignore").splitlines())
                    if item.suffix in {".py", ".ps1", ".md"}
                    else None,
                }
            )
        elif item.is_dir() and not item.name.startswith("__"):
            packages.append(package_info(root, item))
    by_kind = Counter(item["kind"] for item in root_files)
    suffixes = Counter(item["suffix"] for item in root_files)
    return {
        "area": area_dir.name,
        "path": rel(root, area_dir),
        "root_file_count": len(root_files),
        "package_count": len(packages),
        "root_files_by_kind": dict(by_kind.most_common()),
        "root_files_by_suffix": dict(suffixes.most_common()),
        "root_files": root_files,
        "packages": packages,
    }


def render_markdown(report: dict[str, Any], max_rows: int) -> str:
    lines = [
        "# Tools Root Inventory",
        "",
        f"- Generated at: `{report['generated_at']}`",
        f"- Area count: `{report['summary']['area_count']}`",
        f"- Root files: `{report['summary']['root_file_count']}`",
        f"- Root script entrypoints: `{report['summary']['root_script_entrypoint_count']}`",
        "",
        "## Areas",
        "",
        "| Area | Root files | Packages | Root entrypoints | Root helpers |",
        "|---|---:|---:|---:|---:|",
    ]
    for area in report["areas"]:
        kinds = area["root_files_by_kind"]
        lines.append(
            f"| `{area['area']}` | {area['root_file_count']} | {area['package_count']} | "
            f"{kinds.get('root_script_entrypoint', 0)} | {kinds.get('root_code_helper', 0)} |"
        )
    lines.extend(["", "## Root Files", "", "| Kind | Path | Lines |", "|---|---|---:|"])
    rows: list[dict[str, Any]] = []
    for area in report["areas"]:
        rows.extend(area["root_files"])
    for item in rows[:max_rows]:
        lines.append(f"| {item['kind']} | `{item['path']}` | {item.get('line_count') or ''} |")
    if len(rows) > max_rows:
        lines.append(f"\n_Truncated {len(rows) - max_rows} root files; see JSON._")
    return "\n".join(lines) + "\n"


def build_summary(areas: list[dict[str, Any]]) -> dict[str, Any]:
    root_files = [item for area in areas for item in area["root_files"]]
    return {
        "area_count": len(areas),
        "root_file_count": len(root_files),
        "package_count": sum(area["package_count"] for area in areas),
        "root_files_by_kind": dict(Counter(item["kind"] for item in root_files).most_common()),
        "root_script_entrypoint_count": sum(
            1
            for item in root_files
            if item["kind"] in {"root_script_entrypoint", "root_powershell_entrypoint"}
        ),
    }


def parse_areas(values: list[str]) -> set[str]:
    areas: set[str] = set()
    for value in values:
        areas.update(part.strip() for part in value.split(",") if part.strip())
    return areas


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--area", action="append", default=[])
    parser.add_argument("--output", default="output/validation/tool_root_inventory.json")
    parser.add_argument("--markdown-output", default="output/validation/tool_root_inventory.md")
    parser.add_argument("--max-markdown-rows", type=int, default=240)
    args = parser.parse_args()

    root = repo_root_from(Path(args.repo_root))
    selected = parse_areas(args.area)
    tools_root = root / "Tools"
    areas = [
        area_inventory(root, path)
        for path in sorted(tools_root.iterdir())
        if path.is_dir() and not path.name.startswith("__") and (not selected or path.name in selected)
    ]
    report: dict[str, Any] = {
        "schema_version": 1,
        "kind": "tool_root_inventory",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": root.as_posix(),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "summary": build_summary(areas),
        "areas": areas,
    }
    output = root / args.output
    markdown_output = root / args.markdown_output
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_output.write_text(render_markdown(report, args.max_markdown_rows), encoding="utf-8")
    print(json.dumps({"passed": True, "summary": report["summary"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
