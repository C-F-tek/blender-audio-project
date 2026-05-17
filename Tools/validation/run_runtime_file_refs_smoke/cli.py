#!/usr/bin/env python3
"""Smoke test runtime file reference resolution."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CORE_RUNTIME_GUARD = True

try:
    from tools.ai.runtime_file_refs import (
        RuntimeConsumer,
        RuntimeFileRefResolver,
        RuntimeRefProvenance,
    )
    from tools.ai.runtime_file_refs.classifier import extract_target_refs, extract_validation_refs
    from tools.validation.report_utils import write_json_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from tools.ai.runtime_file_refs import (  # type: ignore
        RuntimeConsumer,
        RuntimeFileRefResolver,
        RuntimeRefProvenance,
    )
    from tools.ai.runtime_file_refs.classifier import (  # type: ignore
        extract_target_refs,
        extract_validation_refs,
    )
    from tools.validation.report_utils import write_json_report  # type: ignore


def build_report(repo_root: Path) -> dict[str, object]:
    source_target = first_git_file(repo_root, ("*.py", "*.ps1", "*.json", "*.md"), exclude_prefix="Tools/validation/")
    validation_target = first_git_file(repo_root, ("Tools/validation/*.py",), exclude_prefix="")
    text = """
TARGET_FILES:
 - {source_target}
 - output/validation/generated.json

VALIDATION_COMMANDS:
- python {validation_target} --repo-root .
""".format(source_target=source_target, validation_target=validation_target)
    resolver = RuntimeFileRefResolver(repo_root)
    target_refs = resolver.resolve_many(
        extract_target_refs(text),
        provenance=RuntimeRefProvenance.PROVIDER,
        consumers=(RuntimeConsumer.MATRIX,),
    )
    validation_refs = resolver.resolve_many(
        extract_validation_refs(text),
        provenance=RuntimeRefProvenance.PROVIDER,
        consumers=(RuntimeConsumer.BROKER_TOOL,),
        validation_ref=True,
    )
    errors: list[str] = []
    if not any(item.patchable for item in target_refs):
        errors.append("source target was not patchable")
    if not any(item.output_only for item in target_refs):
        errors.append("output artifact was not marked output-only")
    if not validation_refs or not all(item.validation_only for item in validation_refs):
        errors.append("validation command refs were not isolated as validation-only")
    return {
        "schema_version": 1,
        "kind": "runtime_file_refs_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "passed": not errors,
        "errors": errors,
        "target_refs": [item.as_dict() for item in target_refs],
        "validation_refs": [item.as_dict() for item in validation_refs],
        "source_writes_performed": False,
        "patch_application_performed": False,
    }


def first_git_file(repo_root: Path, patterns: tuple[str, ...], *, exclude_prefix: str) -> str:
    for pattern in patterns:
        completed = subprocess.run(
            ["git", "ls-files", "--", pattern],
            cwd=repo_root,
            text=True,
            capture_output=True,
            check=False,
        )
        for line in completed.stdout.splitlines():
            item = line.strip().replace("\\", "/")
            if item and (not exclude_prefix or not item.startswith(exclude_prefix)):
                return item
    raise RuntimeError(f"no git-tracked file matched {patterns}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/runtime_file_refs_smoke.json")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    output = Path(args.output)
    if not output.is_absolute():
        output = repo_root / output
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
