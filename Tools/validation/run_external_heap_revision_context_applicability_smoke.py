#!/usr/bin/env python3
"""Smoke test for external heap revision-context candidate applicability.

This smoke is intentionally synthetic and offline. It validates the adapter
logic that turns rejected proposal blocks into next-run rewrite tasks.

Regression covered:
- placeholder/stub markers can live in candidate preview, diagnostic preview or
  rejection metadata;
- non-concrete candidates must force requires_concrete_rewrite=true;
- symbol propagation must be skipped for non-concrete candidates;
- PowerShell files must not be validated with python -m py_compile.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from Tools.ai.build_external_heap_revision_context import build_report
except ImportError:  # pragma: no cover
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.build_external_heap_revision_context import build_report  # type: ignore


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_fixture() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    proposal_preview = """```markdown
# HEAP_DELTA_PROPOSAL

CURRENT_POINTER:
- previous_block_id=<id-or-empty>
- refines_block_id=<id-or-empty>
- resume_from_block_id=<id-or-empty>

TARGET_FILES:
- Tools/workflow/run_unified_local_ai_refactor.ps1

IMPLEMENTATION_CHANGES:
```powershell
function Invoke-HeapEntry {
    # comment only function stub
    pass
}

& $RepoPy -m py_compile .\\Tools\\workflow\\run_unified_local_ai_refactor.ps1
```
```"""

    diagnostic_preview = """# Heap Proposal Iteration

- Quality passed: `False`

## Implementation quality

- Errors: `["placeholder/stub code detected: ['bare_pass', 'comment_only_function_stub', 'unresolved_angle_bracket_token']"]`
"""

    pointer = {
        "protocol": "external_heap_block_pointer_v1",
        "pointer_product_contract": {
            "product_contract": True,
            "decision_recovery": True,
            "supports_forward_navigation": True,
            "supports_backrefinement": True,
            "supports_resume": True,
            "provider_execution_is_separate_guardrail": True,
        },
        "pointer_contract_role": "product_graph_decision_recovery_and_long_response_composition",
        "provider_execution_semantics": "separate_guardrail_true_only_with_explicit_provider_or_workload_evidence",
        "provider_execution_performed": True,
        "block_count": 3,
        "source_block_count": 3,
        "roles_present": ["gpu1_planner", "gpu0_reviewer_refiner", "npu_auditor"],
        "all_roles_present": ["gpu1_planner", "gpu0_reviewer_refiner", "npu_auditor"],
        "blocks": [
            {
                "block_type": "proposal_chunk",
                "block_id": "proposal_smoke",
                "step_index": 0,
                "role": "gpu1_planner",
                "source_path": "output/validation/smoke/team_context/proposal_iterations/heap_proposal_revision_000.json",
                "markdown_path": "output/validation/smoke/team_context/proposal_iterations/heap_proposal_revision_000.md",
                "previous_block_id": "",
                "next_block_id": "",
                "refines_block_id": "",
                "resume_from_block_id": "",
                "quality_passed": False,
                "accepted": False,
                "preview_source": "candidate_response",
                "preview": proposal_preview,
                "candidate_response_preview": proposal_preview,
                "diagnostic_preview": diagnostic_preview,
            },
            {
                "block_type": "peer_review",
                "block_id": "gpu0_review_smoke",
                "step_index": 1,
                "role": "gpu0_reviewer_refiner",
            },
            {
                "block_type": "peer_audit",
                "block_id": "npu_audit_smoke",
                "step_index": 2,
                "role": "npu_auditor",
            },
        ],
    }

    composer = {
        "product_status": "blocked_with_reason",
        "rejected_proposals": [
            {
                "name": "heap_proposal_revision_000.json",
                "reason": "placeholder/stub code detected: ['bare_pass', 'comment_only_function_stub', 'unresolved_angle_bracket_token']",
            }
        ],
    }

    causality = {
        "causal_chain_status": "passed",
        "causal_chain_passed": True,
        "product_acceptance_status": "blocked",
        "product_acceptance_passed": False,
    }
    return pointer, composer, causality


def run_smoke() -> dict[str, Any]:
    pointer, composer, causality = build_fixture()
    report = build_report(pointer, composer, causality)
    summary = report.get("candidate_applicability_summary") or {}
    rewrite_tasks = [
        task
        for task in report.get("tasks", [])
        if isinstance(task, dict) and task.get("task_type") == "rewrite_rejected_block"
    ]
    first_task = rewrite_tasks[0] if rewrite_tasks else {}
    flags = set(first_task.get("candidate_applicability_flags") or [])

    required_flags = {
        "bare_pass",
        "comment_only_function_stub",
        "unresolved_angle_bracket_token",
        "invalid_ps1_py_compile_validation",
    }
    checks = [
        {
            "name": "operational_revision_context",
            "passed": report.get("operational_revision_context") is True,
        },
        {
            "name": "requires_concrete_rewrite",
            "passed": report.get("requires_concrete_rewrite") is True,
        },
        {
            "name": "priority_next_action_rewrite",
            "passed": report.get("priority_next_action") == "rewrite_non_concrete_candidates",
        },
        {
            "name": "non_concrete_count",
            "passed": summary.get("non_concrete_candidate_task_count") == 1,
        },
        {
            "name": "symbol_propagation_skipped",
            "passed": first_task.get("symbol_propagation_skipped") is True,
        },
        {
            "name": "candidate_concrete_false",
            "passed": first_task.get("candidate_concrete_enough") is False,
        },
        {
            "name": "required_flags_present",
            "passed": required_flags.issubset(flags),
        },
        {
            "name": "no_source_writes",
            "passed": report.get("source_writes_performed") is False,
        },
        {
            "name": "no_patch_application",
            "passed": report.get("patch_application_performed") is False,
        },
    ]
    passed = all(item["passed"] for item in checks)
    return {
        "schema_version": 1,
        "kind": "external_heap_revision_context_applicability_smoke",
        "passed": passed,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "checks": checks,
        "candidate_applicability_summary": summary,
        "rewrite_task": first_task,
        "errors": [] if passed else [item["name"] for item in checks if not item["passed"]],
        "warnings": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="output/validation/external_heap_revision_context_applicability_smoke.json",
    )
    args = parser.parse_args()

    report = run_smoke()
    write_json(Path(args.output), report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
