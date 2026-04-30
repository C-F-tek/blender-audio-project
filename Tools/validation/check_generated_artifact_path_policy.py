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
    from Tools.validation.generated_file_policy import (
        PathPolicy,
        evaluate_generated_artifact_paths,
    )
except ImportError:  # Allows direct execution from Tools/validation.
    import sys

    repo_root = Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from Tools.validation.generated_file_policy import PathPolicy, evaluate_generated_artifact_paths  # type: ignore


DEFAULT_ALLOWED_PREFIXES: tuple[str, ...] = (
    "output/",
    "indexAI/",
    "patch_specs/inbox/",
    "patch_specs/applied/",
    "Scripting/v61b/hotpatch/",
    "Tools/npu/npu_code_chunks/",
)

DEFAULT_ALLOWED_EXACT_PATHS: tuple[str, ...] = (
    "Tools/npu/npu_code_context.md",
    "Tools/npu/npu_code_index.md",
    "Tools/npu/npu_code_manifest.json",
)


def sample_results(repo_root: Path, policy: PathPolicy) -> list[dict[str, Any]]:
    """Run deterministic path-policy samples."""
    samples = {
        "allowed_output_report": ("output/ai_pipeline/dry_run_matrix_report.json", True),
        "allowed_project_index": ("indexAI/project_code_index.md", True),
        "allowed_npu_context": ("Tools/npu/npu_code_context.md", True),
        "allowed_hotpatch": ("Scripting/v61b/hotpatch/generated_scene_patch.py", True),
        "blocked_runtime_source": ("Scripting/v61b/main_v61b.py", False),
        "blocked_docs_source": ("docs/README.md", False),
        "blocked_workflow_source": (".github/workflows/apply_repo_mods.yml", False),
        "blocked_outside_repo": ("../generated_outside_repo.txt", False),
    }
    results = evaluate_generated_artifact_paths(repo_root, [Path(value) for value, _ in samples.values()], policy)
    rendered: list[dict[str, Any]] = []
    for result, (label, (_, expected)) in zip(results, samples.items(), strict=True):
        data = result.to_dict()
        data["label"] = label
        data["expected_passed"] = expected
        data["sample_passed"] = result.passed is expected
        rendered.append(data)
    return rendered


def build_policy(allowed_prefixes: list[str], allowed_exact_paths: list[str]) -> PathPolicy:
    """Build an active policy from defaults plus optional CLI additions."""
    return PathPolicy(
        allowed_prefixes=tuple(dict.fromkeys([*DEFAULT_ALLOWED_PREFIXES, *allowed_prefixes])),
        allowed_exact_paths=tuple(dict.fromkeys([*DEFAULT_ALLOWED_EXACT_PATHS, *allowed_exact_paths])),
    )


def check_policy(repo_root: Path, paths: list[str], allowed_prefixes: list[str], allowed_exact_paths: list[str]) -> dict[str, Any]:
    """Evaluate sample and explicit generated artifact destinations."""
    policy = build_policy(allowed_prefixes, allowed_exact_paths)
    samples = sample_results(repo_root, policy)
    explicit_paths = [Path(item) for item in paths]
    path_results = evaluate_generated_artifact_paths(repo_root, explicit_paths, policy) if explicit_paths else []

    errors = []
    for item in samples:
        if not item["sample_passed"]:
            errors.append(f"sample {item['label']} expected passed={item['expected_passed']}, got {item['passed']}")
    for item in path_results:
        if not item.passed:
            errors.append(f"path policy failed: {item.label}")

    return {
        "schema_version": 1,
        "kind": "generated_artifact_path_policy",
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "allowed_prefixes": list(policy.allowed_prefixes),
        "allowed_exact_paths": list(policy.allowed_exact_paths),
        "sample_results": samples,
        "path_count": len(path_results),
        "path_results": [item.to_dict() for item in path_results],
        "notes": [
            "This validator checks generated artifact destinations, not input domains or output applications.",
            "Use --path for proposed generated files before writing or committing them.",
            "Use --allowed-prefix or --allowed-exact-path for deliberate workflow-specific extensions.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--path", action="append", default=[], help="Generated artifact destination path to validate. Can be repeated.")
    parser.add_argument("--allowed-prefix", action="append", default=[], help="Additional allowed repo-relative prefix.")
    parser.add_argument("--allowed-exact-path", action="append", default=[], help="Additional allowed repo-relative exact path.")
    parser.add_argument("--output", help="Optional JSON report path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = check_policy(repo_root, args.path, args.allowed_prefix, args.allowed_exact_path)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = repo_root / output
        output = output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
