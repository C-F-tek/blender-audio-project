"""Move a root helper module into a package and rewrite active imports."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

from Tools.docs.repo_tool_surface_audit import git_visible_files, repo_root_from

TEXT_SUFFIXES = {".py", ".ps1", ".json", ".yml", ".yaml", ".toml", ".md"}
SKIP_PREFIXES = (
    "output/",
    "indexAI/",
    "renders/",
    "docs/LOCAL_VALIDATION_EVIDENCE/",
)


@dataclass(frozen=True)
class Rewrite:
    path: str
    old: str
    new: str
    count: int


def relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def skip_path(rel: str) -> bool:
    normalized = rel.replace("\\", "/")
    return any(normalized.startswith(prefix) for prefix in SKIP_PREFIXES)


def git_mv(root: Path, source: Path, target: Path) -> None:
    source_rel = str(source.relative_to(root))
    target_rel = str(target.relative_to(root))
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", source_rel],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
        text=True,
    )
    if tracked.returncode == 0:
        completed = subprocess.run(["git", "mv", source_rel, target_rel], cwd=root, check=False)
        if completed.returncode == 0:
            return
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    source.unlink()


def replacement_pairs(area: str, module: str, package: str, target_stem: str) -> list[tuple[str, str]]:
    old_path = f"Tools/{area}/{module}.py"
    new_path = f"Tools/{area}/{package}/{target_stem}.py"
    old_backslash = old_path.replace("/", "\\")
    new_backslash = new_path.replace("/", "\\")
    old_mod = f"Tools.{area}.{module}"
    new_mod = f"Tools.{area}.{package}.{target_stem}"
    pairs = [
        (old_path, new_path),
        (old_backslash, new_backslash),
        (old_mod, new_mod),
    ]
    return pairs


def rewrite_python_imports(text: str, *, area: str, module: str, package: str, target_stem: str) -> tuple[str, int]:
    direct_from = f"from {module} import"
    package_from = f"from Tools.{area}.{module} import"
    new_from = f"from Tools.{area}.{package}.{target_stem} import"
    direct_import = f"import {module}"
    package_import = f"import Tools.{area}.{module}"
    new_import = f"from Tools.{area}.{package} import {target_stem}"
    count = 0
    lines: list[str] = []
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]
        if stripped.startswith(direct_from):
            line = f"{indent}{new_from}{stripped[len(direct_from):]}"
            count += 1
        elif stripped.startswith(package_from):
            line = f"{indent}{new_from}{stripped[len(package_from):]}"
            count += 1
        elif stripped.startswith(direct_import) and (
            len(stripped) == len(direct_import) or stripped[len(direct_import)].isspace()
        ):
            suffix = stripped[len(direct_import):]
            line = f"{indent}{new_import}{suffix}"
            count += 1
        elif stripped.startswith(package_import) and (
            len(stripped) == len(package_import) or stripped[len(package_import)].isspace()
        ):
            suffix = stripped[len(package_import):]
            if suffix.strip().startswith("as "):
                line = f"{indent}{new_import}{suffix}"
            else:
                line = f"{indent}{new_import}\n"
            count += 1
        lines.append(line)
    return "".join(lines), count


def rewrite_active_refs(
    root: Path,
    *,
    area: str,
    module: str,
    package: str,
    target_stem: str,
    apply: bool,
) -> list[Rewrite]:
    rewrites: list[Rewrite] = []
    pairs = replacement_pairs(area, module, package, target_stem)
    for path in git_visible_files(root):
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = relative(root, path)
        if skip_path(rel):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        updated = text
        for old, new in pairs:
            count = updated.count(old)
            if count:
                updated = updated.replace(old, new)
                rewrites.append(Rewrite(path=rel, old=old, new=new, count=count))
        if path.suffix.lower() == ".py":
            updated_python, count = rewrite_python_imports(
                updated,
                area=area,
                module=module,
                package=package,
                target_stem=target_stem,
            )
            if count:
                rewrites.append(
                    Rewrite(
                        path=rel,
                        old=f"python import {module}",
                        new=f"python import Tools.{area}.{package}.{target_stem}",
                        count=count,
                    )
                )
                updated = updated_python
        if apply and updated != text:
            path.write_text(updated, encoding="utf-8")
    return rewrites


def render_markdown(report: dict[str, object]) -> str:
    lines = [
        "# Internalize Root Module",
        "",
        f"- Generated at: `{report['generated_at']}`",
        f"- Apply: `{report['apply']}`",
        f"- Source writes: `{report['source_writes_performed']}`",
        f"- Source: `{report['source']}`",
        f"- Target: `{report['target']}`",
        f"- Rewrite count: `{report['summary']['rewrite_count']}`",
        "",
        "## Rewrites",
        "",
        "| Path | Count | Old | New |",
        "|---|---:|---|---|",
    ]
    rewrites = report["rewrites"]
    assert isinstance(rewrites, list)
    for item in rewrites[:200]:
        assert isinstance(item, dict)
        old = str(item["old"]).replace("|", "\\|")
        new = str(item["new"]).replace("|", "\\|")
        lines.append(f"| `{item['path']}` | {item['count']} | `{old}` | `{new}` |")
    if len(rewrites) > 200:
        lines.append(f"\n_Truncated {len(rewrites) - 200} more rewrites; see JSON._")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--area", required=True)
    parser.add_argument("--module", required=True)
    parser.add_argument("--package", default="_shared")
    parser.add_argument("--target-name", default="")
    parser.add_argument("--output", default="output/validation/internalize_root_module.json")
    parser.add_argument("--markdown-output", default="output/validation/internalize_root_module.md")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    root = repo_root_from(Path(args.repo_root))
    source = root / "Tools" / args.area / f"{args.module}.py"
    target_name = args.target_name or f"{args.module}.py"
    if not target_name.endswith(".py"):
        target_name = f"{target_name}.py"
    target = root / "Tools" / args.area / args.package / target_name
    init = target.parent / "__init__.py"
    if not source.exists():
        raise SystemExit(f"source module not found: {source}")
    if target.exists():
        raise SystemExit(f"target already exists: {target}")

    target_stem = Path(target_name).stem
    rewrites = rewrite_active_refs(
        root,
        area=args.area,
        module=args.module,
        package=args.package,
        target_stem=target_stem,
        apply=args.apply,
    )
    if args.apply:
        target.parent.mkdir(parents=True, exist_ok=True)
        if not init.exists():
            init.write_text('"""Internal shared modules."""\n', encoding="utf-8")
        git_mv(root, source, target)

    report: dict[str, object] = {
        "schema_version": 1,
        "kind": "internalize_root_module",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": root.as_posix(),
        "apply": args.apply,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": args.apply,
        "source": relative(root, source),
        "target": relative(root, target),
        "summary": {"rewrite_count": sum(item.count for item in rewrites)},
        "rewrites": [asdict(item) for item in rewrites],
    }
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
