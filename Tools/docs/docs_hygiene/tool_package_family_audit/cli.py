"""Group ``Tools/*`` packages by semantic family and duplication signals."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from Tools.docs.docs_hygiene.repo_tool_surface_audit import git_visible_files, repo_root_from

COMMAND_PREFIXES = (
    "build",
    "run",
    "check",
    "validate",
    "apply",
    "analyze",
    "assemble",
    "prepare",
    "create",
    "generate",
    "promote",
    "rewrite",
    "split",
    "refactor",
)
FAMILY_ALIASES = {
    "agent_review": ("agent_review",),
    "agent_context": ("agent_context", "agent_state", "agent_memory_inventory", "agnostic_tool_inventory"),
    "agent_memory": ("agent_memory", "sqlite_memory", "memory_routing"),
    "code_product": ("code_product", "code_patch", "code_edit", "code_interpreter"),
    "generated_patch_specs": ("generated_patch_specs", "patch_spec", "patch_specs"),
    "heap_exchange": ("heap_exchange", "heap_runtime_context", "heap_peer", "task_ingress"),
    "heap_runtime": ("heap_runtime", "heap_code_execution", "virtual_dev", "completeness_gate"),
    "provider_runtime": ("provider_runtime", "runtime_heap", "peer_reports", "live_signals"),
    "runtime_tool": ("runtime_tool", "tool_broker", "tool_usage", "capability_manifest"),
    "runtime_universe": ("runtime_universe", "unified_", "raw_debug", "observer_snapshot"),
    "pipeline": ("pipeline", "artifact_pipeline", "dry_run_matrix"),
    "patch_product": ("patch_notes", "patch_plan", "patch_suggestion", "patch_unified"),
    "repository_product": ("repository_", "github_", "review_pr", "megalithic_review"),
    "provider_mesh": ("gpu", "gpu0", "openvino", "npu", "ollama", "provider_probe"),
    "workflow_run": ("workflow", "run_unified", "operator_product", "launcher"),
    "docs_hygiene": ("markdown", "md_", "repo_tool", "hygiene", "coherence"),
}
IGNORE_DIR_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


@dataclass(frozen=True)
class PackageInfo:
    area: str
    name: str
    path: str
    depth: int
    family: str
    normalized_name: str
    python_file_count: int
    code_line_count: int
    has_cli: bool
    has_init: bool
    root_package: bool
    command_prefixed: bool


@dataclass(frozen=True)
class Finding:
    kind: str
    severity: str
    family: str
    paths: list[str]
    detail: str
    recommendation: str


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def split_tokens(name: str) -> list[str]:
    return [part for part in name.replace("-", "_").split("_") if part]


def normalized_package_name(name: str) -> str:
    tokens = split_tokens(name)
    if tokens and tokens[0] in COMMAND_PREFIXES:
        tokens = tokens[1:]
    return "_".join(tokens) or name


def classify_family(name: str, path: str) -> str:
    text = f"{name} {path}".lower()
    for family, markers in FAMILY_ALIASES.items():
        if any(marker in text for marker in markers):
            return family
    normalized = normalized_package_name(name)
    tokens = split_tokens(normalized)
    if not tokens:
        return "misc"
    return "_".join(tokens[:2]) if len(tokens) > 1 else tokens[0]


def is_package_dir(path: Path) -> bool:
    if any(part in IGNORE_DIR_PARTS for part in path.parts):
        return False
    return (path / "__init__.py").exists() or (path / "cli.py").exists()


def code_line_count(paths: Iterable[Path]) -> int:
    total = 0
    for path in paths:
        try:
            total += len(path.read_text(encoding="utf-8", errors="ignore").splitlines())
        except OSError:
            continue
    return total


def package_info(root: Path, package_dir: Path) -> PackageInfo:
    area = package_dir.relative_to(root).parts[1]
    name = package_dir.name
    rel_path = rel(root, package_dir)
    py_files = sorted(package_dir.glob("*.py"))
    return PackageInfo(
        area=area,
        name=name,
        path=rel_path,
        depth=len(package_dir.relative_to(root / "Tools" / area).parts),
        family=classify_family(name, rel_path),
        normalized_name=normalized_package_name(name),
        python_file_count=len(py_files),
        code_line_count=code_line_count(py_files),
        has_cli=(package_dir / "cli.py").exists(),
        has_init=(package_dir / "__init__.py").exists(),
        root_package=len(package_dir.relative_to(root / "Tools" / area).parts) == 1,
        command_prefixed=bool(split_tokens(name) and split_tokens(name)[0] in COMMAND_PREFIXES),
    )


def iter_package_dirs(root: Path, selected_areas: set[str]) -> list[Path]:
    tools_root = root / "Tools"
    if not tools_root.exists():
        return []
    packages: list[Path] = []
    for area_dir in sorted(path for path in tools_root.iterdir() if path.is_dir()):
        if selected_areas and area_dir.name not in selected_areas:
            continue
        for path in sorted(area_dir.rglob("*")):
            if path.is_dir() and is_package_dir(path):
                packages.append(path)
    return packages


def build_findings(packages: list[PackageInfo]) -> list[Finding]:
    findings: list[Finding] = []
    by_area_normalized: dict[tuple[str, str], list[PackageInfo]] = defaultdict(list)
    by_area_family: dict[tuple[str, str], list[PackageInfo]] = defaultdict(list)
    for package in packages:
        by_area_normalized[(package.area, package.normalized_name)].append(package)
        by_area_family[(package.area, package.family)].append(package)

    for (area, normalized), items in sorted(by_area_normalized.items()):
        root_items = [item for item in items if item.root_package]
        if len(root_items) < 2:
            continue
        canonical = min(root_items, key=lambda item: (item.command_prefixed, len(item.name), item.name))
        findings.append(
            Finding(
                kind="normalized_name_collision",
                severity="high",
                family=classify_family(normalized, canonical.path),
                paths=[item.path for item in root_items],
                detail=f"`Tools/{area}` has multiple root packages that normalize to `{normalized}`.",
                recommendation=f"Consolidate under `{canonical.path}` or a nested family package.",
            )
        )

    for (area, family), items in sorted(by_area_family.items()):
        root_items = [item for item in items if item.root_package]
        if len(root_items) < 3:
            continue
        command_count = sum(1 for item in root_items if item.command_prefixed)
        recommendation = f"Create or use `Tools/{area}/{family}/...` as the macro package for this family."
        severity = "high" if command_count >= 2 else "medium"
        findings.append(
            Finding(
                kind="crowded_family_root_packages",
                severity=severity,
                family=family,
                paths=[item.path for item in root_items],
                detail=f"{len(root_items)} root packages share family `{family}`; {command_count} are command-prefixed.",
                recommendation=recommendation,
            )
        )
    return sorted(findings, key=lambda item: (item.severity, item.family, item.kind, item.paths))


def group_packages(packages: list[PackageInfo]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[PackageInfo]] = defaultdict(list)
    for package in packages:
        groups[(package.area, package.family)].append(package)
    rendered: list[dict[str, Any]] = []
    for (area, family), items in sorted(groups.items()):
        root_count = sum(1 for item in items if item.root_package)
        rendered.append(
            {
                "area": area,
                "family": family,
                "package_count": len(items),
                "root_package_count": root_count,
                "command_prefixed_root_count": sum(1 for item in items if item.root_package and item.command_prefixed),
                "code_line_count": sum(item.code_line_count for item in items),
                "packages": [asdict(item) for item in sorted(items, key=lambda item: item.path)],
            }
        )
    return rendered


def render_markdown(report: dict[str, Any], max_rows: int) -> str:
    lines = [
        "# Tool Package Family Audit",
        "",
        f"- Generated at: `{report['generated_at']}`",
        f"- Packages: `{report['summary']['package_count']}`",
        f"- Findings: `{report['summary']['finding_count']}`",
        f"- Source writes: `{report['source_writes_performed']}`",
        "",
        "## Findings",
        "",
        "| Severity | Kind | Family | Paths | Recommendation |",
        "|---|---|---|---|---|",
    ]
    for item in report["findings"][:max_rows]:
        paths = "<br>".join(f"`{path}`" for path in item["paths"])
        recommendation = str(item["recommendation"]).replace("|", "\\|")
        lines.append(f"| {item['severity']} | {item['kind']} | `{item['family']}` | {paths} | {recommendation} |")
    if len(report["findings"]) > max_rows:
        lines.append(f"\n_Truncated {len(report['findings']) - max_rows} findings; see JSON._")
    lines.extend(["", "## Largest Families", "", "| Area | Family | Root packages | Packages | Lines |", "|---|---|---:|---:|---:|"])
    largest = sorted(report["families"], key=lambda item: (item["root_package_count"], item["code_line_count"]), reverse=True)
    for item in largest[:max_rows]:
        lines.append(
            f"| `{item['area']}` | `{item['family']}` | {item['root_package_count']} | "
            f"{item['package_count']} | {item['code_line_count']} |"
        )
    return "\n".join(lines) + "\n"


def parse_areas(values: list[str]) -> set[str]:
    areas: set[str] = set()
    for value in values:
        areas.update(part.strip() for part in value.split(",") if part.strip())
    return areas


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--area", action="append", default=[])
    parser.add_argument("--output", default="output/validation/tool_package_family_audit.json")
    parser.add_argument("--markdown-output", default="output/validation/tool_package_family_audit.md")
    parser.add_argument("--max-markdown-rows", type=int, default=160)
    parser.add_argument("--fail-on-findings", action="store_true")
    args = parser.parse_args()

    root = repo_root_from(Path(args.repo_root))
    selected_areas = parse_areas(args.area)
    _ = git_visible_files(root)
    packages = [package_info(root, path) for path in iter_package_dirs(root, selected_areas)]
    findings = build_findings(packages)
    summary = {
        "package_count": len(packages),
        "family_count": len({(item.area, item.family) for item in packages}),
        "finding_count": len(findings),
        "by_kind": dict(Counter(item.kind for item in findings).most_common()),
        "by_severity": dict(Counter(item.severity for item in findings).most_common()),
    }
    report: dict[str, Any] = {
        "schema_version": 1,
        "kind": "tool_package_family_audit",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": root.as_posix(),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "summary": summary,
        "findings": [asdict(item) for item in findings],
        "families": group_packages(packages),
    }
    output = root / args.output
    markdown_output = root / args.markdown_output
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_output.write_text(render_markdown(report, args.max_markdown_rows), encoding="utf-8")
    print(json.dumps({"passed": not (args.fail_on_findings and findings), "summary": summary}, indent=2))
    return 1 if args.fail_on_findings and findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
