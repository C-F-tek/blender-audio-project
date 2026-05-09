#!/usr/bin/env python3
"""Validate Full0To10/LightFull0To10 legacy alias registry."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


FORBIDDEN_TEXT = (
    "Full0To10 is a separate pipeline",
    "Full0To10 is an operational profile",
    "LightFull0To10 is a separate pipeline",
    "LightFull0To10 is an operational profile",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--registry", default="Tools/ai/unified_run_legacy_alias_registry.json")
    parser.add_argument("--output", default="output/validation/unified_run_legacy_alias_registry_smoke.json")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    registry_path = repo / args.registry
    errors: list[str] = []
    warnings: list[str] = []

    if not registry_path.exists():
        errors.append(f"registry missing: {registry_path}")
        registry = {}
    else:
        registry = json.loads(registry_path.read_text(encoding="utf-8-sig"))

    if registry.get("operational_model") != "single_dynamic_heap_exchange_run":
        errors.append("registry operational_model must be single_dynamic_heap_exchange_run")
    if registry.get("source_of_knowledge") != "heap_exchange":
        errors.append("registry source_of_knowledge must be heap_exchange")
    if registry.get("standalone_pipelines_forbidden") is not True:
        errors.append("standalone_pipelines_forbidden must be true")

    aliases = {item.get("alias"): item for item in registry.get("aliases") or [] if isinstance(item, dict)}
    for alias in ("Full0To10", "LightFull0To10"):
        item = aliases.get(alias)
        if not item:
            errors.append(f"missing alias registry entry: {alias}")
            continue
        if item.get("standalone_pipeline") is not False:
            errors.append(f"{alias} standalone_pipeline must be false")
        if item.get("status") != "legacy_compatibility_alias":
            errors.append(f"{alias} status must be legacy_compatibility_alias")

    for rel in registry.get("allowed_legacy_paths") or []:
        path = repo / rel
        if not path.exists():
            warnings.append(f"allowed legacy path missing: {rel}")
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for forbidden in FORBIDDEN_TEXT:
            if forbidden in text:
                errors.append(f"forbidden legacy semantics in {rel}: {forbidden}")

    report = {
        "schema_version": 1,
        "kind": "unified_run_legacy_alias_registry_smoke",
        "repo_root": repo.as_posix(),
        "registry": str(registry_path),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": errors,
        "warnings": warnings,
    }

    output = resolve_output_path(repo, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
