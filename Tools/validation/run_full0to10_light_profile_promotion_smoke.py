#!/usr/bin/env python3
"""Static smoke for legacy LightFull0To10 compatibility promotion.

This smoke validates compatibility semantics only. LightFull0To10 is not a
standalone pipeline and not an operational profile; it is a legacy alias routed
toward the single unified heap/exchange run.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/full0to10_light_profile_promotion_smoke.json")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    wrapper = repo / "Tools/workflow/run_unified_light_full0to10_profile.ps1"
    builder = repo / "Tools/ai/build_full0to10_light_profile_promotion.py"
    summary = repo / "Tools/ai/summarize_full0to10_light_evidence.py"
    constants = repo / "Tools/ai/full0to10_light_profile/constants.py"

    wrapper_text = read(wrapper)
    builder_text = read(builder)
    summary_text = read(summary)
    constants_text = read(constants)

    checks = {
        "wrapper_exists": wrapper.exists(),
        "builder_exists": builder.exists(),
        "summary_exists": summary.exists(),
        "constants_exists": constants.exists(),
        "wrapper_declares_legacy_alias": "legacy alias" in wrapper_text.lower() or "LegacyAlias:LightFull0To10" in wrapper_text,
        "wrapper_keeps_external_probe_guard": "-NoExternalProbes" in wrapper_text,
        "builder_is_compatibility_artifact": "compatibility artifacts" in builder_text.lower() or "compatibility" in builder_text.lower(),
        "summary_declares_unified_compat_kind": "unified_run_light_evidence_compatibility" in summary_text,
        "summary_declares_legacy_kind": "legacy_kind" in summary_text,
        "summary_declares_not_standalone": "standalone_pipeline" in summary_text,
        "summary_declares_unified_entrypoint": "recommended_unified_entrypoint" in summary_text,
        "summary_checks_provider_false": "provider_execution_performed" in summary_text,
        "summary_checks_patch_false": "patch_application_performed" in summary_text,
        "constants_keep_legacy_alias": "compatibility alias" in constants_text,
        "constants_route_to_unified_run": "unified run product model" in constants_text,
    }

    report = {
        "kind": "unified_run_light_compatibility_promotion_smoke",
        "legacy_smoke_name": "full0to10_light_profile_promotion_smoke",
        "full0to10_standalone_pipeline": False,
        "operational_model": "single_dynamic_heap_exchange_run",
        "passed": all(checks.values()),
        "checks": checks,
    }

    output = resolve_output_path(repo, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
