"""CLI for patch-notes quality product smoke."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report

from .cases import (
    area_diversity_smoke,
    deterministic_doc_python_patchable_smoke,
    patchable_availability_smoke,
    python_python_symbol_smoke,
)
from .common import now_stamp, render_markdown
from .fixtures import build_fixtures
from .runner import run_case

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    stamp = args.stamp or now_stamp()
    fixtures = build_fixtures(repo_root, stamp)
    positive = run_case(repo_root, stamp, fixtures, 72.0)
    negative = run_case(repo_root, stamp + "_forced_false", fixtures, 101.0)
    all_all_task_path = repo_root / fixtures["task"]
    all_all_task_path.write_text(
        "# ALL_ALL smoke task\n\n"
        "Objective: ALL_ALL repository progression. Required areas: "
        "doc_doc, doc_python, python_doc, python_python, policy_violation, "
        "refactor_candidate, evidence_gap.\n",
        encoding="utf-8",
    )
    all_all_insufficient = run_case(repo_root, stamp + "_all_all_insufficient", fixtures, 72.0)
    errors: list[str] = []
    if (
        not positive.get("passed")
        or not positive.get("quality_gate_passed")
        or not positive.get("patch_notes")
    ):
        errors.append("positive case did not produce passing patch notes")
    if not positive.get("success_cases"):
        errors.append("positive case did not produce structured success cases")
    if (
        not negative.get("passed")
        or negative.get("quality_gate_passed")
        or not negative.get("fallback_path_notes")
    ):
        errors.append("negative non-blocking fallback case did not behave as expected")
    if not negative.get("fallback_cases"):
        errors.append(
            "negative non-blocking fallback case did not produce structured fallback cases"
        )
    if all_all_insufficient.get("quality_gate_passed"):
        errors.append("ALL_ALL insufficient case incorrectly passed quality gate")
    if (
        all_all_insufficient.get("classification")
        != "completed_with_insufficient_all_all_patch_notes"
    ):
        errors.append("ALL_ALL insufficient case did not receive insufficient classification")
    area_diversity = area_diversity_smoke()
    if not area_diversity.get("passed"):
        errors.append(
            "area diversity smoke failed to include doc_doc/python_doc alongside doc_python"
        )
    python_python_symbol = python_python_symbol_smoke()
    if not python_python_symbol.get("passed"):
        errors.append("python_python symbol import smoke failed")
    patchable_availability = patchable_availability_smoke()
    if not patchable_availability.get("passed"):
        errors.append("patchable availability smoke failed")
    deterministic_doc_python_patchable = deterministic_doc_python_patchable_smoke()
    if not deterministic_doc_python_patchable.get("passed"):
        errors.append("deterministic doc_python patchable smoke failed")
    report = {
        "schema_version": 1,
        "kind": "patch_notes_quality_product_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "sqlite_write_performed": False,
        "persistent_memory_write_performed": False,
        "manual_review_required": True,
        "positive": {
            "passed": positive.get("passed"),
            "quality_gate_passed": positive.get("quality_gate_passed"),
            "classification": positive.get("classification"),
            "patch_note_count": len(positive.get("patch_notes", [])),
            "success_case_count": len(positive.get("success_cases", [])),
        },
        "negative": {
            "passed": negative.get("passed"),
            "quality_gate_passed": negative.get("quality_gate_passed"),
            "classification": negative.get("classification"),
            "fallback_path_note_count": len(negative.get("fallback_path_notes", [])),
            "fallback_case_count": len(negative.get("fallback_cases", [])),
        },
        "all_all_insufficient": {
            "passed": all_all_insufficient.get("passed"),
            "quality_gate_passed": all_all_insufficient.get("quality_gate_passed"),
            "classification": all_all_insufficient.get("classification"),
            "product_sufficiency": all_all_insufficient.get("product_sufficiency"),
        },
        "area_diversity": area_diversity,
        "python_python_symbol": python_python_symbol,
        "patchable_availability": patchable_availability,
        "deterministic_doc_python_patchable": deterministic_doc_python_patchable,
        "guardrails": {
            "report_only": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
        },
    }
    output = resolve_output_path(
        repo_root,
        args.output or f"output/validation/patch_notes_quality_product_smoke_{stamp}.json",
    )
    markdown = resolve_output_path(
        repo_root,
        args.markdown_output or f"output/validation/patch_notes_quality_product_smoke_{stamp}.md",
    )
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
