"""Move a ``Tools/<area>/<package>`` tool package under a macro package."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from Tools.docs.docs_hygiene.repo_tool_surface_audit import (
    git_visible_files,
    repo_root_from,
)

TEXT_SUFFIXES = {".py", ".ps1", ".md", ".txt", ".json", ".yml", ".yaml", ".toml"}
SKIP_PREFIXES = (
    "output/",
    "indexAI/",
    "renders/",
    "docs/LOCAL_VALIDATION_EVIDENCE/",
)


@dataclass(frozen=True)
class Rewrite:
    path: str
    count: int


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def normalize_package_path(value: str) -> str:
    path = value.strip().replace("\\", "/").strip("/")
    if not path or path.startswith(".") or "/../" in f"/{path}/":
        raise SystemExit(f"invalid package path: {value!r}")
    parts = path.split("/")
    if any(not part or part in {".", ".."} for part in parts):
        raise SystemExit(f"invalid package path: {value!r}")
    return path


def target_package_from_args(args: argparse.Namespace) -> str:
    if args.target_package:
        return normalize_package_path(args.target_package)
    if not args.macro_package:
        raise SystemExit("provide --target-package or --macro-package")
    macro = normalize_package_path(args.macro_package)
    target_name = normalize_package_path(args.target_name or args.package)
    return f"{macro}/{target_name}"


def should_scan(rel_path: str, path: Path) -> bool:
    if any(rel_path.startswith(prefix) for prefix in SKIP_PREFIXES):
        return False
    return path.suffix.lower() in TEXT_SUFFIXES


def replace_module_refs(text: str, old_module: str, new_module: str) -> tuple[str, int]:
    pattern = re.compile(rf"(?<![\w.]){re.escape(old_module)}(?=\.|[^\w.]|$)")
    return pattern.subn(new_module, text)


def reference_pairs(area: str, source: str, target: str) -> list[tuple[str, str]]:
    return [
        (f"Tools/{area}/{source}/", f"Tools/{area}/{target}/"),
        (f"Tools\\{area}\\{source}\\", f"Tools\\{area}\\{target_windows}\\"),
    ]


def rewrite_references(
    root: Path,
    *,
    area: str,
    source: str,
    target: str,
    apply: bool,
) -> list[Rewrite]:
    old_module = f"Tools.{area}.{source}"
    new_module = f"Tools.{area}.{target.replace('/', '.')}"
    pairs = reference_pairs(area, source, target)
    rewrites: list[Rewrite] = []
    for path in git_visible_files(root):
        rel_path = rel(root, path)
        if not should_scan(rel_path, path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        updated = text
        count = 0
        for old, new in pairs:
            old_count = updated.count(old)
            if old_count:
                updated = updated.replace(old, new)
                count += old_count
        updated, module_count = replace_module_refs(updated, old_module, new_module)
        count += module_count
        if count:
            if apply:
                path.write_text(updated, encoding="utf-8")
            rewrites.append(Rewrite(path=rel_path, count=count))
    return rewrites


def dispatch_target(area: str, target: str) -> str:
    return f"Tools.{area}.{target.replace('/', '.')}.cli:main"


def update_dispatch(
    root: Path,
    *,
    area: str,
    tool_name: str,
    target: str,
    apply: bool,
) -> Rewrite | None:
    path = root / "Tools" / area / "dispatch.py"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    target_text = dispatch_target(area, target)
    key_pattern = re.compile(rf'("{re.escape(tool_name)}"\s*:\s*)"[^"]+"')
    match = key_pattern.search(text)
    if match:
        old_line = match.group(0)
        new_line = f'{match.group(1)}"{target_text}"'
        if old_line == new_line:
            return None
        updated = text[: match.start()] + new_line + text[match.end() :]
    else:
        entry = f'    "{tool_name}": "{target_text}",\n'
        lines = text.splitlines(keepends=True)
        start = next(
            (index for index, line in enumerate(lines) if line.startswith("TOOL_MAIN_TARGETS")),
            -1,
        )
        end = next(
            (index for index in range(start + 1, len(lines)) if lines[index].strip() == "}"),
            -1,
        )
        if start < 0 or end < 0:
            raise SystemExit(f"cannot find dispatch registry end in {path}")
        lines.insert(end, entry)
        updated = "".join(lines)
    if apply:
        path.write_text(updated, encoding="utf-8")
    return Rewrite(path=rel(root, path), count=1)


def tracked_paths(root: Path, package: Path) -> list[str]:
    package_rel = rel(root, package)
    completed = subprocess.run(
        ["git", "ls-files", "--", package_rel],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    return [line for line in completed.stdout.splitlines() if line]


def code_line_counts(root: Path, paths: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in paths:
        path = root / item
        if path.suffix.lower() not in {".py", ".ps1"}:
            continue
        try:
            counts[item] = len(path.read_text(encoding="utf-8", errors="ignore").splitlines())
        except OSError:
            continue
    return counts


def move_package(root: Path, source_dir: Path, target_dir: Path, apply: bool) -> str:
    if not apply:
        return "planned"
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    source_rel = rel(root, source_dir)
    target_rel = rel(root, target_dir)
    completed = subprocess.run(
        ["git", "mv", source_rel, target_rel],
        cwd=root,
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode == 0:
        return "git_mv"
    shutil.move(str(source_dir), str(target_dir))
    return "shutil_move"


def adjust_parent_indexes(
    root: Path,
    *,
    moved_paths: list[str],
    source_package: str,
    target_package: str,
    apply: bool,
) -> list[Rewrite]:
    delta = len(target_package.split("/")) - len(source_package.split("/"))
    if delta == 0:
        return []
    rewrites: list[Rewrite] = []
    for old_rel in moved_paths:
        if not old_rel.endswith(".py"):
            continue
        new_rel = old_rel.replace(f"/{source_package}/", f"/{target_package}/", 1)
        path = root / new_rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")

        def replace(match: re.Match[str]) -> str:
            return f"parents[{int(match.group(1)) + delta}]"

        updated, count = re.subn(r"parents\[(\d+)\]", replace, text)
        if count:
            if apply:
                path.write_text(updated, encoding="utf-8")
            rewrites.append(Rewrite(path=new_rel, count=count))
    return rewrites


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Tool Package Move",
        "",
        f"- Generated at: `{report['generated_at']}`",
        f"- Apply: `{report['apply']}`",
        f"- Source: `{report['source_package']}`",
        f"- Target: `{report['target_package']}`",
        f"- Move method: `{report['move_method']}`",
        f"- Reference rewrites: `{report['summary']['reference_rewrite_count']}`",
        "",
        "## Rewrites",
        "",
    ]
    for item in report["reference_rewrites"][:100]:
        lines.append(f"- `{item['path']}` count=`{item['count']}`")
    if len(report["reference_rewrites"]) > 100:
        lines.append(f"- truncated={len(report['reference_rewrites']) - 100}")
    return "\n".join(lines) + "\n"


def build_report(
    *,
    root: Path,
    area: str,
    source_package: str,
    target_package: str,
    apply: bool,
    move_method: str,
    rewrites: list[Rewrite],
    dispatch_update: Rewrite | None,
    moved_paths: list[str],
    line_counts: dict[str, int],
    parent_index_rewrites: list[Rewrite],
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "kind": "tool_package_move",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": root.as_posix(),
        "area": area,
        "source_package": f"Tools/{area}/{source_package}",
        "target_package": f"Tools/{area}/{target_package}",
        "apply": apply,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": apply,
        "move_method": move_method,
        "summary": {
            "moved_path_count": len(moved_paths),
            "reference_rewrite_count": len(rewrites),
            "reference_rewrite_occurrences": sum(item.count for item in rewrites),
            "dispatch_update_count": 1 if dispatch_update else 0,
            "parent_index_rewrite_count": len(parent_index_rewrites),
        },
        "moved_paths": moved_paths,
        "line_counts": line_counts,
        "reference_rewrites": [asdict(item) for item in rewrites],
        "dispatch_update": asdict(dispatch_update) if dispatch_update else None,
        "parent_index_rewrites": [asdict(item) for item in parent_index_rewrites],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--area", required=True)
    parser.add_argument("--package", required=True)
    parser.add_argument("--target-package", default="")
    parser.add_argument("--macro-package", default="")
    parser.add_argument("--target-name", default="")
    parser.add_argument("--output", default="output/validation/tool_package_move.json")
    parser.add_argument("--markdown-output", default="output/validation/tool_package_move.md")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--no-rewrite-references", action="store_true")
    parser.add_argument("--no-update-dispatch", action="store_true")
    args = parser.parse_args()

    root = repo_root_from(Path(args.repo_root))
    source_package = normalize_package_path(args.package)
    target_package = target_package_from_args(args)
    source_dir = root / "Tools" / args.area / source_package
    target_dir = root / "Tools" / args.area / target_package
    if not source_dir.is_dir():
        raise SystemExit(f"source package not found: {source_dir}")
    if target_dir.exists():
        raise SystemExit(f"target package already exists: {target_dir}")
    moved_paths = tracked_paths(root, source_dir)
    line_counts = code_line_counts(root, moved_paths)
    rewrites = []
    if not args.no_rewrite_references:
        rewrites = rewrite_references(
            root,
            area=args.area,
            source=source_package,
            target=target_package,
            apply=args.apply,
        )
    dispatch_update = None
    if not args.no_update_dispatch:
        dispatch_update = update_dispatch(
            root,
            area=args.area,
            tool_name=Path(source_package).name,
            target=target_package,
            apply=args.apply,
        )
    move_method = move_package(root, source_dir, target_dir, args.apply)
    parent_index_rewrites = adjust_parent_indexes(
        root,
        moved_paths=moved_paths,
        source_package=f"{args.area}/{source_package}",
        target_package=f"{args.area}/{target_package}",
        apply=args.apply,
    )
    report = build_report(
        root=root,
        area=args.area,
        source_package=source_package,
        target_package=target_package,
        apply=args.apply,
        move_method=move_method,
        rewrites=rewrites,
        dispatch_update=dispatch_update,
        moved_paths=moved_paths,
        line_counts=line_counts,
        parent_index_rewrites=parent_index_rewrites,
    )
    output = root / args.output
    markdown_output = root / args.markdown_output
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": True, "summary": report["summary"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
