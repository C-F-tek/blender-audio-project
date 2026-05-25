"""Smoke test heap final decision trace classification."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from ia_carmine.runtime.heap_context_closure.decision_trace import (
    build_final_decision_trace,
    render_final_decision_trace_markdown,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    with tempfile.TemporaryDirectory(prefix="heap_final_decision_trace_smoke_") as tmp:
        proposal_dir = Path(tmp) / "team_context" / "proposal_iterations"
        proposal_dir.mkdir(parents=True, exist_ok=True)
        (proposal_dir / "heap_proposal_revision_001.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "gpu1_mpc_governor_report": {
                        "kind": "gpu1_tool_mpc_governor",
                        "decision": "force_consume_tool_result",
                        "first_blocker": "gpu1_requested_tool_result_not_consumed",
                        "total_cost": 90,
                    },
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        cases = {
            "approved_text_only": _trace(
                product_state={"product_status": "approved_product", "product_kind": "text_product"},
                code_contract={
                    "text_product_ready": True,
                    "real_code_product_ready": False,
                    "final_product_surface_ready": True,
                    "final_product_delta_applied_count": 1,
                },
            ),
            "blocked_tool_result": _trace(
                summary={
                    "gpu1_one_turn_runtime_gate_passed": False,
                    "gpu1_one_turn_blocker": "gpu1_one_turn_tool_result_not_consumed",
                },
                product_state={
                    "product_status": "blocked_with_reason",
                    "product_kind": "diagnostic_decision_product",
                },
                code_contract={"final_product_surface_ready": False, "final_product_delta_applied_count": 1},
            ),
            "blocked_no_surface": _trace(
                product_state={
                    "product_status": "blocked_with_reason",
                    "product_kind": "diagnostic_decision_product",
                },
                code_contract={"final_product_surface_ready": False, "final_product_delta_applied_count": 1},
            ),
            "latest_proposal_mpc": _trace(
                run_dir=Path(tmp),
                product_state={
                    "product_status": "blocked_with_reason",
                    "product_kind": "diagnostic_decision_product",
                },
                code_contract={"final_product_surface_ready": False, "final_product_delta_applied_count": 1},
            ),
        }
        expected = {
            "approved_text_only": "approved_product",
            "blocked_tool_result": "gpu1_one_turn_tool_result_not_consumed",
            "blocked_no_surface": "FINAL_PRODUCT has no accepted text or code surface",
            "latest_proposal_mpc": "gpu1_requested_tool_result_not_consumed",
        }
        errors = []
        if cases["approved_text_only"].get("final_decision") != expected["approved_text_only"]:
            errors.append("approved text-only trace did not approve product")
        for key in ("blocked_tool_result", "blocked_no_surface", "latest_proposal_mpc"):
            if cases[key].get("first_blocker") != expected[key]:
                errors.append(
                    f"{key}: expected first blocker {expected[key]}, got {cases[key].get('first_blocker')}"
                )
        report = {
            "schema_version": 1,
            "kind": "heap_final_decision_trace_smoke",
            "repo_root": str(repo_root),
            "passed": not errors,
            "first_blockers": {key: value.get("first_blocker") for key, value in cases.items()},
            "decisions": {key: value.get("final_decision") for key, value in cases.items()},
            "markdown_preview": render_final_decision_trace_markdown(cases["blocked_tool_result"])[:1200],
            "errors": errors,
        }
    _write(args.output, repo_root, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


def _trace(
    *,
    summary: dict[str, Any] | None = None,
    product_state: dict[str, Any],
    code_contract: dict[str, Any],
    run_dir: Path | None = None,
) -> dict[str, Any]:
    summary = summary if isinstance(summary, dict) else {"gpu1_one_turn_runtime_gate_passed": True}
    return build_final_decision_trace(
        args=SimpleNamespace(allow_provider_generation=True, strict_startup_reload=False),
        state={
            "preflight_result": {"passed": True},
            "startup_result": {"passed": True},
            "startup_payload": {},
            "can_continue": True,
            "heap_result": {"passed": True},
            "final_readable_payload": {},
            "run_dir": run_dir or "",
        },
        launcher_summary=summary,
        code_product_contract=code_contract,
        external_contract={
            "provider_execution_performed": True,
            "product_acceptance_passed": True,
            "pointer_manifest_passed": True,
            "passed": True,
        },
        product_state=product_state,
        launcher_contract_errors=[],
    )


def _write(output: str, repo_root: Path, report: dict[str, Any]) -> None:
    if not output:
        return
    path = Path(output)
    if not path.is_absolute():
        path = repo_root / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
