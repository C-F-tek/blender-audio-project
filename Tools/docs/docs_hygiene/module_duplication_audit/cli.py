"""Audit duplicate and highly similar Python modules under ``Tools/*``."""

from __future__ import annotations

import argparse
import ast
import io
import json
import re
import tokenize
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from difflib import SequenceMatcher
from hashlib import sha256
from pathlib import Path
from typing import Iterable

from Tools.validation._shared.report_utils import resolve_output_path, write_json_report

IGNORED_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
TRIVIAL_MODULE_NAMES = {"__init__.py", "__main__.py"}
ROLE_STEMS = {
    "cli",
    "common",
    "config",
    "constants",
    "dispatch",
    "markdown",
    "paths",
    "render",
    "report",
    "reporting",
    "runner",
}
STEM_NOISE = {
    "agent",
    "apply",
    "build",
    "check",
    "cli",
    "core",
    "create",
    "report",
    "run",
    "runtime",
    "smoke",
    "tool",
    "tools",
    "validate",
}


@dataclass(frozen=True)
class ModuleInfo:
    path: str
    area: str
    stem: str
    code_line_count: int
    token_count: int
    role_module: bool


@dataclass(frozen=True)
class SimilarityFinding:
    kind: str
    severity: str
    score: float
    path_a: str
    path_b: str
    detail: str
    recommendation: str


def repo_rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def code_lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]


def normalized_ast_hash(text: str) -> str:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        payload = text
    else:
        for node in ast.walk(tree):
            for attr in ("lineno", "col_offset", "end_lineno", "end_col_offset"):
                if hasattr(node, attr):
                    setattr(node, attr, None)
        payload = ast.dump(tree, annotate_fields=True, include_attributes=False)
    return sha256(payload.encode("utf-8", errors="ignore")).hexdigest()


def code_tokens(text: str) -> list[str]:
    tokens: list[str] = []
    try:
        stream = tokenize.generate_tokens(io.StringIO(text).readline)
        for token in stream:
            if token.type in (tokenize.NAME, tokenize.STRING, tokenize.NUMBER, tokenize.OP):
                value = token.string.lower()
                if value not in {"encoding", "utf"}:
                    tokens.append(value)
    except tokenize.TokenError:
        return []
    return tokens


def stem_tokens(stem: str) -> set[str]:
    return {
        token
        for token in re.split(r"[_\W]+", stem.lower())
        if token and token not in STEM_NOISE
    }


def token_jaccard(left: Counter[str], right: Counter[str]) -> float:
    keys = set(left) | set(right)
    if not keys:
        return 0.0
    intersection = sum(min(left[key], right[key]) for key in keys)
    union = sum(max(left[key], right[key]) for key in keys)
    return intersection / union if union else 0.0


def iter_python_files(root: Path, areas: set[str]) -> Iterable[Path]:
    tools_root = root / "Tools"
    if not tools_root.exists():
        return []
    paths: list[Path] = []
    for path in sorted(tools_root.rglob("*.py")):
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.name in TRIVIAL_MODULE_NAMES:
            continue
        try:
            relative_parts = path.relative_to(tools_root).parts
        except ValueError:
            continue
        if not relative_parts:
            continue
        if areas and relative_parts[0] not in areas:
            continue
        paths.append(path)
    return paths


def inspect_modules(root: Path, areas: set[str], min_lines: int) -> tuple[list[ModuleInfo], dict[str, list[str]], list[tuple[Path, list[str], Counter[str]]]]:
    modules: list[ModuleInfo] = []
    exact_hashes: dict[str, list[str]] = defaultdict(list)
    tokenized: list[tuple[Path, list[str], Counter[str]]] = []
    tools_root = root / "Tools"
    for path in iter_python_files(root, areas):
        text = path.read_text(encoding="utf-8", errors="ignore")
        lines = code_lines(text)
        if len(lines) < min_lines:
            continue
        tokens = code_tokens(text)
        area = path.relative_to(tools_root).parts[0]
        rel_path = repo_rel(root, path)
        role_module = path.stem in ROLE_STEMS
        modules.append(
            ModuleInfo(
                path=rel_path,
                area=area,
                stem=path.stem,
                code_line_count=len(lines),
                token_count=len(tokens),
                role_module=role_module,
            )
        )
        if not role_module and len(tokens) >= 80:
            exact_hashes[normalized_ast_hash(text)].append(rel_path)
            tokenized.append((path, tokens, Counter(tokens)))
    return modules, exact_hashes, tokenized


def exact_duplicate_findings(exact_hashes: dict[str, list[str]]) -> list[SimilarityFinding]:
    findings: list[SimilarityFinding] = []
    for digest, paths in sorted(exact_hashes.items()):
        if len(paths) < 2:
            continue
        findings.append(
            SimilarityFinding(
                kind="exact_ast_duplicate",
                severity="high",
                score=1.0,
                path_a=paths[0],
                path_b=paths[1],
                detail=f"{len(paths)} modules share AST hash `{digest[:12]}`.",
                recommendation="Merge the duplicate module bodies into one owner package.",
            )
        )
    return findings


def similarity_findings(
    root: Path,
    tokenized: list[tuple[Path, list[str], Counter[str]]],
    threshold: float,
) -> list[SimilarityFinding]:
    findings: list[SimilarityFinding] = []
    tools_root = root / "Tools"
    stem_cache = {path: stem_tokens(path.stem) for path, _tokens, _counter in tokenized}
    for index, (left_path, left_tokens, left_counter) in enumerate(tokenized):
        left_area = left_path.relative_to(tools_root).parts[0]
        for right_path, right_tokens, right_counter in tokenized[index + 1 :]:
            right_area = right_path.relative_to(tools_root).parts[0]
            same_area = left_area == right_area
            shared_stem = bool(stem_cache[left_path] & stem_cache[right_path])
            if not same_area and not shared_stem:
                continue
            jaccard = token_jaccard(left_counter, right_counter)
            if jaccard < threshold - 0.08:
                continue
            sequence = SequenceMatcher(None, left_tokens[:3000], right_tokens[:3000]).ratio()
            score = (jaccard + sequence) / 2
            if score >= threshold:
                findings.append(
                    SimilarityFinding(
                        kind="high_similarity_modules",
                        severity="medium" if score < 0.85 else "high",
                        score=round(score, 3),
                        path_a=repo_rel(root, left_path),
                        path_b=repo_rel(root, right_path),
                        detail=f"token_jaccard={jaccard:.3f}; sequence={sequence:.3f}",
                        recommendation="Extract shared logic or consolidate under the relevant macro package.",
                    )
                )
    return sorted(findings, key=lambda item: (-item.score, item.path_a, item.path_b))


def render_markdown(report: dict, max_findings: int) -> str:
    lines = [
        "# Module Duplication Audit",
        "",
        f"- Generated at: `{report['generated_at']}`",
        f"- Modules scanned: `{report['summary']['module_count']}`",
        f"- Findings: `{report['summary']['finding_count']}`",
        f"- Similarity threshold: `{report['parameters']['similarity_threshold']}`",
        "",
        "## Findings",
        "",
        "| Severity | Kind | Score | Module A | Module B | Detail |",
        "|---|---|---:|---|---|---|",
    ]
    for item in report["findings"][:max_findings]:
        detail = str(item["detail"]).replace("|", "\\|")
        lines.append(
            f"| {item['severity']} | {item['kind']} | {item['score']} | "
            f"`{item['path_a']}` | `{item['path_b']}` | {detail} |"
        )
    if len(report["findings"]) > max_findings:
        lines.append(f"\n_Truncated {len(report['findings']) - max_findings} findings; see JSON._")
    lines.extend(["", "## Same-Stem Inventory", ""])
    for stem, paths in report["same_stem_inventory"][:max_findings]:
        lines.append(f"- `{stem}`: " + ", ".join(f"`{path}`" for path in paths[:8]))
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
    parser.add_argument("--min-lines", type=int, default=20)
    parser.add_argument("--similarity-threshold", type=float, default=0.70)
    parser.add_argument("--max-findings", type=int, default=80)
    parser.add_argument("--output")
    parser.add_argument("--markdown-output")
    parser.add_argument("--fail-on-findings", action="store_true")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    areas = parse_areas(list(args.area or []))
    modules, exact_hashes, tokenized = inspect_modules(root, areas, max(1, args.min_lines))
    findings = exact_duplicate_findings(exact_hashes)
    findings.extend(similarity_findings(root, tokenized, args.similarity_threshold))

    by_stem: dict[str, list[str]] = defaultdict(list)
    for module in modules:
        if not module.role_module:
            by_stem[module.stem].append(module.path)
    same_stem = sorted(
        ((stem, sorted(paths)) for stem, paths in by_stem.items() if len(paths) > 1),
        key=lambda item: (-len(item[1]), item[0]),
    )
    report = {
        "schema_version": 1,
        "kind": "module_duplication_audit",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(root),
        "passed": not findings,
        "parameters": {
            "areas": sorted(areas),
            "min_lines": args.min_lines,
            "similarity_threshold": args.similarity_threshold,
        },
        "summary": {
            "module_count": len(modules),
            "finding_count": len(findings),
            "same_stem_group_count": len(same_stem),
        },
        "source_writes_performed": False,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "findings": [asdict(item) for item in findings],
        "same_stem_inventory": same_stem,
        "modules": [asdict(item) for item in modules],
    }
    output = resolve_output_path(root, args.output) if args.output else None
    print(write_json_report(report, output), end="")
    if args.markdown_output:
        markdown = resolve_output_path(root, args.markdown_output)
        markdown.parent.mkdir(parents=True, exist_ok=True)
        markdown.write_text(render_markdown(report, args.max_findings), encoding="utf-8")
    return 2 if args.fail_on_findings and findings else 0
