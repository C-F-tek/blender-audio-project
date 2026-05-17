"""Rewrite legacy ``Tools/<area>/<script>`` calls to dispatcher commands."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

from Tools.docs.repo_tool_surface_audit import git_visible_files, repo_root_from

TEXT_SUFFIXES = {".md", ".ps1", ".py", ".txt", ".json", ".yml", ".yaml", ".toml"}
REFERENCE_SKIP_PREFIXES = (
    "output/",
    "indexAI/",
    "renders/",
    "docs/LOCAL_VALIDATION_EVIDENCE/",
)
PYTHON_SCRIPT_PATTERN = re.compile(
    r"(?P<runner>(?:&\s*)?(?:python(?:\.exe)?|py|"
    r"\$[A-Za-z_][A-Za-z0-9_]*(?:py|python)[A-Za-z0-9_]*|"
    r"\$env:[A-Za-z_][A-Za-z0-9_]*(?:py|python)[A-Za-z0-9_]*))"
    r"(?P<space>\s+)"
    r"(?P<quote>[\"']?)"
    r"(?P<path>(?:\.?[\\/])?Tools[\\/](?P<area>[A-Za-z0-9_.-]+)[\\/]"
    r"(?P<tail>[A-Za-z0-9_.\\/-]+)\.py)"
    r"(?P=quote)"
    ,
    re.IGNORECASE,
)
POWERSHELL_SCRIPT_PATTERN = re.compile(
    r"(?P<runner>powershell(?:\.exe)?[^\n\r`|&;]*?\s+-File)"
    r"(?P<space>\s+)"
    r"(?P<quote>[\"']?)"
    r"(?P<path>(?:\.?[\\/])?Tools[\\/](?P<area>[A-Za-z0-9_.-]+)[\\/]"
    r"(?P<tail>[A-Za-z0-9_.\\/-]+)\.ps1)"
    r"(?P=quote)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Rewrite:
    path: str
    line: int
    old: str
    new: str
    area: str
    tool: str


def parse_csv(values: list[str], default: set[str] | None = None) -> set[str]:
    parsed: set[str] = set(default or set())
    for value in values:
        parsed.update(part.strip() for part in value.split(",") if part.strip())
    return parsed


def tool_name_from_tail(tail: str) -> str:
    return Path(tail.replace("\\", "/")).stem


def replacement_for(match: re.Match[str]) -> str:
    area = match.group("area")
    tool = tool_name_from_tail(match.group("tail"))
    return f"{match.group('runner')} -m Tools.{area} {tool}"


def powershell_replacement_for(match: re.Match[str]) -> str:
    area = match.group("area")
    tool = tool_name_from_tail(match.group("tail"))
    return f"python -m Tools.{area} {tool}"


def should_scan(path: Path, suffixes: set[str]) -> bool:
    return path.is_file() and path.suffix.lower() in suffixes


def relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def is_generated_reference_path(rel: str) -> bool:
    normalized = rel.replace("\\", "/")
    return any(normalized.startswith(prefix) for prefix in REFERENCE_SKIP_PREFIXES)


def matches_root_prefix(rel: str, prefixes: set[str]) -> bool:
    if not prefixes:
        return True
    normalized = rel.replace("\\", "/")
    for prefix in prefixes:
        clean = prefix.strip().replace("\\", "/").strip("/")
        if normalized == clean or normalized.startswith(f"{clean}/"):
            return True
    return False


def rewrite_text(
    text: str,
    *,
    areas: set[str],
    path_label: str,
) -> tuple[str, list[Rewrite]]:
    rewrites: list[Rewrite] = []
    output_lines: list[str] = []
    for line_number, line in enumerate(text.splitlines(keepends=True), start=1):
        def replace(match: re.Match[str]) -> str:
            area = match.group("area")
            if areas and area not in areas:
                return match.group(0)
            new = replacement_for(match)
            rewrites.append(
                Rewrite(
                    path=path_label,
                    line=line_number,
                    old=match.group(0),
                    new=new,
                    area=area,
                    tool=tool_name_from_tail(match.group("tail")),
                )
            )
            return new

        def replace_powershell(match: re.Match[str]) -> str:
            area = match.group("area")
            if areas and area not in areas:
                return match.group(0)
            new = powershell_replacement_for(match)
            rewrites.append(
                Rewrite(
                    path=path_label,
                    line=line_number,
                    old=match.group(0),
                    new=new,
                    area=area,
                    tool=tool_name_from_tail(match.group("tail")),
                )
            )
            return new

        rewritten = PYTHON_SCRIPT_PATTERN.sub(replace, line)
        rewritten = POWERSHELL_SCRIPT_PATTERN.sub(replace_powershell, rewritten)
        output_lines.append(rewritten)
    return "".join(output_lines), rewrites


def selected_files(root: Path, args: argparse.Namespace) -> list[Path]:
    if args.path:
        return [root / item for item in args.path]
    suffixes = parse_csv(args.suffix) if args.suffix else set(TEXT_SUFFIXES)
    prefixes = parse_csv(args.root_prefix)
    selected: list[Path] = []
    for path in git_visible_files(root):
        if not should_scan(path, suffixes):
            continue
        rel = relative(root, path)
        if is_generated_reference_path(rel):
            continue
        if not matches_root_prefix(rel, prefixes):
            continue
        selected.append(path)
    return selected


def render_markdown(report: dict[str, object]) -> str:
    lines = [
        "# Legacy Tool Invocation Rewrite",
        "",
        f"- Generated at: `{report['generated_at']}`",
        f"- Apply: `{report['apply']}`",
        f"- Candidate rewrites: `{report['summary']['rewrite_count']}`",
        f"- Files touched: `{report['summary']['file_count']}`",
        "",
        "## Rewrites",
        "",
        "| Path | Line | Old | New |",
        "|---|---:|---|---|",
    ]
    rewrites = report["rewrites"]
    assert isinstance(rewrites, list)
    for item in rewrites[:250]:
        assert isinstance(item, dict)
        old = str(item["old"]).replace("|", "\\|")
        new = str(item["new"]).replace("|", "\\|")
        lines.append(f"| `{item['path']}` | {item['line']} | `{old}` | `{new}` |")
    if len(rewrites) > 250:
        lines.append(f"\n_Truncated {len(rewrites) - 250} more rewrites; see JSON._")
    lines.extend(
        [
            "",
            "## Policy",
            "",
            "Dry-run is the default. Source writes happen only with `--apply`.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--area", action="append", default=[], help="Limit to Tools area names.")
    parser.add_argument("--path", action="append", default=[], help="Limit to relative file path.")
    parser.add_argument("--root-prefix", action="append", default=[], help="Limit scanned files to root prefixes.")
    parser.add_argument("--suffix", action="append", default=[], help="Limit scanned suffixes.")
    parser.add_argument("--output", default="output/validation/legacy_tool_invocation_rewrite.json")
    parser.add_argument("--markdown-output", default="output/validation/legacy_tool_invocation_rewrite.md")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--max-apply-rewrites", type=int, default=500)
    args = parser.parse_args()

    root = repo_root_from(Path(args.repo_root))
    areas = parse_csv(args.area)
    all_rewrites: list[Rewrite] = []
    changed_files = 0
    pending_writes: list[tuple[Path, str]] = []
    for path in selected_files(root, args):
        if not path.exists() or not path.is_file():
            continue
        rel = relative(root, path)
        original = path.read_text(encoding="utf-8", errors="ignore")
        rewritten, rewrites = rewrite_text(original, areas=areas, path_label=rel)
        if not rewrites:
            continue
        all_rewrites.extend(rewrites)
        if rewritten != original:
            changed_files += 1
            pending_writes.append((path, rewritten))

    if args.apply and len(all_rewrites) > args.max_apply_rewrites:
        raise SystemExit(
            f"Refusing to apply {len(all_rewrites)} rewrites; raise --max-apply-rewrites explicitly."
        )
    if args.apply:
        for path, rewritten in pending_writes:
            path.write_text(rewritten, encoding="utf-8")

    report: dict[str, object] = {
        "schema_version": 1,
        "kind": "legacy_tool_invocation_rewrite",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": root.as_posix(),
        "apply": args.apply,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": args.apply and bool(pending_writes),
        "summary": {
            "rewrite_count": len(all_rewrites),
            "file_count": changed_files,
            "areas": sorted({item.area for item in all_rewrites}),
        },
        "rewrites": [asdict(item) for item in all_rewrites],
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
