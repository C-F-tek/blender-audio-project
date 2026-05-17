#!/usr/bin/env python3
"""Validate safe repository destinations for generated artifacts.

This validator is intentionally input-agnostic and output-application-agnostic.
It checks where generated files may be written, not what source data produced
them and not which runtime will consume them.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.generated_file_policy import (
        PathPolicy,
        evaluate_generated_artifact_paths,
    )
except ImportError:  # Allows direct execution from Tools/validation.
    import sys

    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from Tools.validation._shared.generated_file_policy import (  # type: ignore
        PathPolicy,
        evaluate_generated_artifact_paths,
    )


DEFAULT_ALLOWED_PREFIXES: tuple[str, ...] = (
    "output/",
    "indexAI/",
    "patch_specs/inbox/",
    "patch_specs/applied/",
    "Scripting/v61b/hotpatch/",
    "Tools/npu/npu_code_chunks/",
)

DEFAULT_ALLOWED_EXACT_PATHS: tuple[str, ...] = (
    "Tools/npu/context_artifacts/npu_code_context.md",
    "Tools/npu/context_artifacts/npu_code_index.md",
    "Tools/npu/context_artifacts/npu_code_manifest.json",
)

ARTIFACT_PATH_KEYS: tuple[str, ...] = (
    "markdown_output",
    "output",
    "output_dir",
    "packet",
    "path",
    "report",
    "report_path",
)


def load_json_report(path: Path) -> Any:
    """Load a JSON report with tolerant UTF-8 BOM handling."""
    return json.loads(path.read_text(encoding="utf-8-sig"))


def looks_like_artifact_path(value: str) -> bool:
    """Return True when a report string looks like a filesystem destination."""
    text = value.strip()
    if not text or "\n" in text or "\r" in text:
        return False
    if "/" in text or "\\" in text:
        return True
    return bool(Path(text).suffix)


def collect_artifact_paths_from_report(value: Any) -> list[str]:
    """Collect generated artifact destinations from known report path fields.

    The collector is deliberately structural rather than domain-specific. It
    walks JSON report objects and captures values of known artifact path keys,
    while ignoring command argv arrays and prose-only fields.
    """
    paths: list[str] = []

    def walk(node: Any, key: str | None = None) -> None:
        if isinstance(node, dict):
            for child_key, child_value in node.items():
                if (
                    child_key in ARTIFACT_PATH_KEYS
                    and isinstance(child_value, str)
                    and looks_like_artifact_path(child_value)
                ):
                    paths.append(child_value)
                else:
                    walk(child_value, child_key)
        elif isinstance(node, list):
            if key == "command":
                return
            for item in node:
                walk(item, key)

    walk(value)
    return list(dict.fromkeys(paths))


def collect_artifact_paths_from_reports(
    repo_root: Path, report_paths: list[str]
) -> tuple[list[str], list[dict[str, Any]], list[str]]:
    """Load JSON reports and return collected artifact paths plus metadata."""
    collected: list[str] = []
    reports: list[dict[str, Any]] = []
    errors: list[str] = []
    for item in report_paths:
        report_path = Path(item)
        if not report_path.is_absolute():
            report_path = repo_root / report_path
        report_path = report_path.resolve()
        if not report_path.exists():
            errors.append(f"artifact report not found: {report_path}")
            reports.append({"path": str(report_path), "exists": False, "path_count": 0})
            continue
        try:
            payload = load_json_report(report_path)
        except Exception as exc:
            errors.append(
                f"artifact report parse failed: {report_path}: {type(exc).__name__}: {exc}"
            )
            reports.append({"path": str(report_path), "exists": True, "path_count": 0})
            continue
        paths = collect_artifact_paths_from_report(payload)
        collected.extend(paths)
        reports.append({"path": str(report_path), "exists": True, "path_count": len(paths)})
    return list(dict.fromkeys(collected)), reports, errors


def sample_results(repo_root: Path, policy: PathPolicy) -> list[dict[str, Any]]:
    """Run deterministic path-policy samples."""
    samples = {
        "allowed_output_report": ("output/ai_pipeline/dry_run_matrix_report.json", True),
        "allowed_project_index": ("indexAI/project_code_index.md", True),
        "allowed_npu_context": ("Tools/npu/context_artifacts/npu_code_context.md", True),
        "allowed_hotpatch": ("Scripting/v61b/hotpatch/generated_scene_patch.py", True),
        "blocked_runtime_source": ("Scripting/v61b/main_v61b.py", False),
        "blocked_docs_source": ("docs/README.md", False),
        "blocked_workflow_source": (".github/workflows/apply_repo_mods.yml", False),
        "blocked_outside_repo": ("../generated_outside_repo.txt", False),
    }
    results = evaluate_generated_artifact_paths(
        repo_root, [Path(value) for value, _ in samples.values()], policy
    )
    rendered: list[dict[str, Any]] = []
    for result, (label, (_, expected)) in zip(results, samples.items(), strict=True):
        data = result.to_dict()
        data["label"] = label
        data["expected_passed"] = expected
        data["sample_passed"] = result.passed is expected
        rendered.append(data)
    return rendered


def build_policy(
    allowed_prefixes: list[str],
    allowed_exact_paths: list[str],
    max_repo_relative_path_chars: int | None,
    max_filename_chars: int | None,
) -> PathPolicy:
    """Build an active policy from defaults plus optional CLI additions."""
    return PathPolicy(
        allowed_prefixes=tuple(dict.fromkeys([*DEFAULT_ALLOWED_PREFIXES, *allowed_prefixes])),
        allowed_exact_paths=tuple(
            dict.fromkeys([*DEFAULT_ALLOWED_EXACT_PATHS, *allowed_exact_paths])
        ),
        max_repo_relative_path_chars=max_repo_relative_path_chars,
        max_filename_chars=max_filename_chars,
    )


def check_policy(
    repo_root: Path,
    paths: list[str],
    artifact_reports: list[str],
    allowed_prefixes: list[str],
    allowed_exact_paths: list[str],
    max_repo_relative_path_chars: int | None,
    max_filename_chars: int | None,
) -> dict[str, Any]:
    """Evaluate sample and explicit generated artifact destinations."""
    policy = build_policy(
        allowed_prefixes, allowed_exact_paths, max_repo_relative_path_chars, max_filename_chars
    )
    samples = sample_results(repo_root, policy)
    report_paths, report_inputs, report_errors = collect_artifact_paths_from_reports(
        repo_root, artifact_reports
    )
    explicit_paths = [Path(item) for item in [*paths, *report_paths]]
    path_results = (
        evaluate_generated_artifact_paths(repo_root, explicit_paths, policy)
        if explicit_paths
        else []
    )

    errors = list(report_errors)
    for item in samples:
        if not item["sample_passed"]:
            errors.append(
                f"sample {item['label']} expected passed={item['expected_passed']}, got {item['passed']}"
            )
    for item in path_results:
        if not item.passed:
            errors.append(f"path policy failed: {item.label}")

    return {
        "schema_version": 1,
        "kind": "generated_artifact_path_policy",
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "allowed_prefixes": list(policy.allowed_prefixes),
        "allowed_exact_paths": list(policy.allowed_exact_paths),
        "max_repo_relative_path_chars": policy.max_repo_relative_path_chars,
        "max_filename_chars": policy.max_filename_chars,
        "artifact_reports": report_inputs,
        "artifact_report_path_count": len(report_paths),
        "sample_results": samples,
        "path_count": len(path_results),
        "path_results": [item.to_dict() for item in path_results],
        "notes": [
            "This validator checks generated artifact destinations, not input domains or output applications.",
            "Use --path for proposed generated files before writing or committing them.",
            "Use --allowed-prefix or --allowed-exact-path for deliberate workflow-specific extensions.",
            "Use --max-repo-relative-path-chars and --max-filename-chars to catch bundle names that may fail Windows/Git push workflows.",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Generated Artifact Path Policy", ""]
    lines.append(f"- Passed: `{report.get('passed')}`")
    lines.append(f"- Path count: `{report.get('path_count')}`")
    lines.append(f"- Artifact report path count: `{report.get('artifact_report_path_count')}`")
    lines.append(f"- Max repo-relative path chars: `{report.get('max_repo_relative_path_chars')}`")
    lines.append(f"- Max filename chars: `{report.get('max_filename_chars')}`")
    failing = [item for item in report.get("path_results", []) if not item.get("passed")]
    lines.append(f"- Failing path count: `{len(failing)}`")
    if failing:
        lines.append("")
        lines.append("## Failing Paths")
        lines.append("")
        for item in failing[:80]:
            lines.append(f"- `{item.get('repo_relative_path') or item.get('path')}`")
            for finding in item.get("findings", []):
                lines.append(f"  - {finding.get('rule_id')}: {finding.get('message')}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        help="Generated artifact destination path to validate. Can be repeated.",
    )
    parser.add_argument(
        "--artifact-report",
        action="append",
        default=[],
        help="JSON report to scan for generated artifact destination fields. Can be repeated.",
    )
    parser.add_argument(
        "--allowed-prefix",
        action="append",
        default=[],
        help="Additional allowed repo-relative prefix.",
    )
    parser.add_argument(
        "--allowed-exact-path",
        action="append",
        default=[],
        help="Additional allowed repo-relative exact path.",
    )
    parser.add_argument("--max-repo-relative-path-chars", type=int, default=None)
    parser.add_argument("--max-filename-chars", type=int, default=None)
    parser.add_argument("--output", help="Optional JSON report path.")
    parser.add_argument("--markdown-output", help="Optional Markdown report path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = check_policy(
        repo_root,
        args.path,
        args.artifact_report,
        args.allowed_prefix,
        args.allowed_exact_path,
        args.max_repo_relative_path_chars,
        args.max_filename_chars,
    )
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = repo_root / output
        output = output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    if args.markdown_output:
        markdown_output = Path(args.markdown_output)
        if not markdown_output.is_absolute():
            markdown_output = repo_root / markdown_output
        markdown_output = markdown_output.resolve()
        markdown_output.parent.mkdir(parents=True, exist_ok=True)
        markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(text, end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
