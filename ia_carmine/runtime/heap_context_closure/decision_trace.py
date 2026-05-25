"""Final decision trace for heap context closure summaries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STAGE_ORDER = (
    "preflight",
    "startup_reload",
    "heap_gate",
    "provider_execution",
    "runtime_tool_cycle",
    "external_heap_contract",
    "gpu1_one_turn_gate",
    "gpu1_mpc_governor",
    "tool_result_consumption",
    "runtime_file_window_contract",
    "pointer_manifest",
    "sidecar_roles",
    "final_product_delta",
    "final_product_surface",
)


def build_final_decision_trace(
    *,
    args: Any,
    state: dict[str, Any],
    launcher_summary: dict[str, Any],
    code_product_contract: dict[str, Any],
    external_contract: dict[str, Any],
    product_state: dict[str, Any],
    launcher_contract_errors: list[str],
) -> dict[str, Any]:
    """Build an ordered, compact explanation of the launcher decision."""
    final_payload = state.get("final_readable_payload", {})
    final_payload = final_payload if isinstance(final_payload, dict) else {}
    latest_proposal = _latest_proposal_report(state)
    mpc = (
        _find_kind(final_payload, "gpu1_tool_mpc_governor")
        or _find_prefixed(final_payload, "gpu1_mpc_governor_")
        or _find_kind(latest_proposal, "gpu1_tool_mpc_governor")
        or _find_prefixed(latest_proposal, "gpu1_mpc_governor_")
        or _find_prefixed(external_contract, "gpu1_mpc_governor_")
    )
    tool_cycle = _tool_cycle_stage(final_payload, external_contract, mpc, latest_proposal)
    tool_consumption_blockers = _tool_consumption_blockers(
        final_payload, external_contract, mpc
    )
    stages = [
        _stage("preflight", bool(state.get("preflight_result", {}).get("passed")), []),
        _stage(
            "startup_reload",
            bool(state.get("startup_result", {}).get("passed") or state.get("can_continue")),
            _list(state.get("startup_payload", {}).get("blocking_requirements")),
        ),
        _stage(
            "heap_gate",
            bool(state.get("heap_result", {}).get("passed")),
            _result_errors(state.get("heap_result")),
        ),
        _stage(
            "provider_execution",
            bool(external_contract.get("provider_execution_performed")),
            _provider_blockers(external_contract),
            {"provider_execution_performed": bool(external_contract.get("provider_execution_performed"))},
        ),
        tool_cycle,
        _stage(
            "external_heap_contract",
            bool(external_contract.get("product_acceptance_passed", external_contract.get("passed", False))),
            _external_blockers(external_contract),
            external_contract,
        ),
        _stage(
            "gpu1_one_turn_gate",
            bool(
                launcher_summary.get("gpu1_one_turn_runtime_gate_passed")
                or external_contract.get("gpu1_one_turn_runtime_gate_passed")
            ),
            _one_turn_blockers(launcher_summary, external_contract),
            {
                "path": launcher_summary.get("gpu1_one_turn_runtime_gate_path", ""),
                "blocker": launcher_summary.get("gpu1_one_turn_blocker", ""),
            },
        ),
        _mpc_stage(mpc),
        _stage(
            "tool_result_consumption",
            not tool_consumption_blockers,
            tool_consumption_blockers,
        ),
        _stage(
            "runtime_file_window_contract",
            not _truthy(code_product_contract.get("final_product_requires_file_read"))
            or _truthy(code_product_contract.get("final_product_file_read_verified")),
            _file_window_blockers(code_product_contract),
            {
                "required": code_product_contract.get("final_product_requires_file_read"),
                "verified": code_product_contract.get("final_product_file_read_verified"),
            },
        ),
        _stage(
            "pointer_manifest",
            bool(external_contract.get("pointer_manifest_passed", external_contract.get("passed", False))),
            _pointer_blockers(external_contract),
        ),
        _stage(
            "sidecar_roles",
            not bool(external_contract.get("missing_roles")),
            _list(external_contract.get("missing_roles")),
        ),
        _stage(
            "final_product_delta",
            _safe_int(code_product_contract.get("final_product_delta_applied_count")) > 0,
            _delta_blockers(code_product_contract),
            {
                "final_product_delta_applied_count": _safe_int(
                    code_product_contract.get("final_product_delta_applied_count")
                )
            },
        ),
        _stage(
            "final_product_surface",
            bool(code_product_contract.get("final_product_surface_ready")),
            _surface_blockers(code_product_contract),
            {
                "text_product_ready": code_product_contract.get("text_product_ready"),
                "real_code_product_ready": code_product_contract.get("real_code_product_ready"),
                "final_product_delta_applied_count": _safe_int(
                    code_product_contract.get("final_product_delta_applied_count")
                ),
            },
        ),
    ]
    blockers = [
        blocker
        for stage in stages
        for blocker in stage.get("blockers", [])
        if str(blocker).strip()
    ]
    if launcher_contract_errors:
        blockers.extend(str(item) for item in launcher_contract_errors if str(item).strip())
    first_blocker = blockers[0] if blockers else ""
    final_decision = str(product_state.get("product_status") or "blocked_with_reason")
    return {
        "schema_version": 1,
        "kind": "heap_final_decision_trace",
        "passed": final_decision == "approved_product",
        "final_decision": final_decision,
        "product_kind": product_state.get("product_kind", ""),
        "first_blocker": first_blocker,
        "stages": stages,
        "next_action_hint": _next_action_hint(final_decision, first_blocker, mpc),
        "operator_config": {
            "allow_provider_generation": bool(getattr(args, "allow_provider_generation", False)),
            "strict_startup_reload": bool(getattr(args, "strict_startup_reload", False)),
        },
    }


def render_final_decision_trace_markdown(trace: dict[str, Any]) -> str:
    lines = [
        "# Heap Final Decision Trace",
        "",
        f"- Final decision: `{trace.get('final_decision', '')}`",
        f"- Product kind: `{trace.get('product_kind', '')}`",
        f"- First blocker: `{trace.get('first_blocker', '')}`",
        "",
        "## Stage order",
        "",
        "| Stage | Passed | Blockers |",
        "|---|---:|---|",
    ]
    for stage in trace.get("stages") or []:
        blockers = ", ".join(str(item) for item in stage.get("blockers") or [])
        lines.append(f"| {stage.get('stage')} | {str(stage.get('passed')).lower()} | {blockers} |")
    lines.extend(["", "## Next action hint", "", str(trace.get("next_action_hint") or "")])
    return "\n".join(lines) + "\n"


def _tool_cycle_stage(
    final_payload: dict[str, Any],
    external_contract: dict[str, Any],
    mpc: dict[str, Any],
    latest_proposal: dict[str, Any],
) -> dict[str, Any]:
    statuses = _first_list(
        final_payload.get("tool_cycle_statuses"),
        external_contract.get("tool_cycle_statuses"),
        mpc.get("tool_cycle_statuses"),
        latest_proposal.get("tool_cycle_statuses"),
    )
    evidence = statuses[0] if statuses else {}
    blockers = [
        str(item.get("tool_failure_reason") or item.get("tool_status"))
        for item in statuses
        if str(item.get("tool_status") or "") not in {"result_consumed", "not_requested"}
        and str(item.get("tool_status") or "").strip()
    ]
    return _stage(
        "runtime_tool_cycle",
        not blockers,
        blockers[:5],
        evidence,
    )


def _mpc_stage(mpc: dict[str, Any]) -> dict[str, Any]:
    if not mpc:
        return _stage("gpu1_mpc_governor", True, [], {})
    decision = str(mpc.get("decision") or "")
    blocker = str(mpc.get("first_blocker") or "").strip()
    blocking = decision in {
        "force_consume_tool_result",
        "block_repeat_tool_call",
        "force_gpu1_refine",
        "block_with_reason",
    }
    return _stage(
        "gpu1_mpc_governor",
        not blocking,
        [blocker] if blocker else [],
        {"decision": decision, "total_cost": mpc.get("total_cost")},
    )


def _stage(
    name: str,
    passed: bool,
    blockers: list[Any],
    evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "stage": name,
        "passed": bool(passed),
        "blockers": [str(item) for item in blockers if str(item).strip()],
        "evidence": evidence if isinstance(evidence, dict) else {},
    }


def _next_action_hint(final_decision: str, first_blocker: str, mpc: dict[str, Any]) -> str:
    decision = str(mpc.get("decision") or "")
    if decision == "force_consume_tool_result" or "not_consumed" in first_blocker:
        return "Resume GPU1 from the latest block and consume the pending tool_result in CONSUMED_EVIDENCE."
    if decision == "force_gpu1_refine":
        return "Resume GPU1 and refine against unconsumed GPU0/NPU sidecar evidence."
    if final_decision == "approved_product":
        return "Product approved; no continuation required."
    return "Inspect the first blocker and resume from the latest pointer-safe block."


def _find_kind(value: Any, kind: str) -> dict[str, Any]:
    if isinstance(value, dict):
        if value.get("kind") == kind:
            return value
        for child in value.values():
            found = _find_kind(child, kind)
            if found:
                return found
    if isinstance(value, list):
        for child in value:
            found = _find_kind(child, kind)
            if found:
                return found
    return {}


def _find_prefixed(value: dict[str, Any], prefix: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    out = {key: value for key, value in value.items() if str(key).startswith(prefix)}
    if out:
        return {
            "kind": "gpu1_tool_mpc_governor",
            "decision": out.get("gpu1_mpc_governor_decision", ""),
            "first_blocker": out.get("gpu1_mpc_governor_first_blocker", ""),
            "total_cost": out.get("gpu1_mpc_governor_total_cost", 0),
        }
    return {}


def _latest_proposal_report(state: dict[str, Any]) -> dict[str, Any]:
    run_dir_value = state.get("run_dir")
    if not run_dir_value:
        return {}
    proposal_dir = Path(str(run_dir_value)) / "team_context" / "proposal_iterations"
    if not proposal_dir.exists() or not proposal_dir.is_dir():
        return {}
    candidates = sorted(proposal_dir.glob("heap_proposal_revision_*.json"))
    for path in reversed(candidates):
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        if isinstance(data, dict):
            return data
    return {}


def _provider_blockers(external_contract: dict[str, Any]) -> list[str]:
    return [
        *[str(item) for item in external_contract.get("provider_rejection_reasons") or []],
        *[f"missing_role:{item}" for item in external_contract.get("missing_roles") or []],
    ]


def _external_blockers(external_contract: dict[str, Any]) -> list[str]:
    return _list(external_contract.get("errors")) or _provider_blockers(external_contract)


def _one_turn_blockers(summary: dict[str, Any], external_contract: dict[str, Any]) -> list[str]:
    if summary.get("gpu1_one_turn_runtime_gate_passed") or external_contract.get(
        "gpu1_one_turn_runtime_gate_passed"
    ):
        return []
    blocker = summary.get("gpu1_one_turn_blocker") or external_contract.get("gpu1_one_turn_blocker")
    return [blocker or "gpu1_one_turn_runtime_gate_missing_or_failed"]


def _tool_consumed(
    final_payload: dict[str, Any],
    external_contract: dict[str, Any],
    mpc: dict[str, Any],
) -> bool:
    return any(
        _truthy(value)
        for value in (
            final_payload.get("tool_result_consumed_by_gpu1"),
            final_payload.get("gpu1_one_turn_tool_result_consumed"),
            external_contract.get("gpu1_one_turn_tool_result_consumed"),
            mpc.get("decision") == "emit_final_delta",
        )
    )


def _tool_consumption_blockers(
    final_payload: dict[str, Any],
    external_contract: dict[str, Any],
    mpc: dict[str, Any],
) -> list[str]:
    if _tool_consumed(final_payload, external_contract, mpc):
        return []
    decision = str(mpc.get("decision") or "")
    if not decision and not any(
        key in final_payload or key in external_contract
        for key in (
            "gpu1_tool_result_blocker",
            "tool_result_consumed_by_gpu1",
            "gpu1_one_turn_tool_result_consumed",
        )
    ):
        return []
    blocker = (
        final_payload.get("gpu1_tool_result_blocker")
        or external_contract.get("gpu1_tool_result_blocker")
        or mpc.get("first_blocker")
    )
    return [blocker or "tool_result_not_consumed"]


def _file_window_blockers(contract: dict[str, Any]) -> list[str]:
    if _truthy(contract.get("final_product_requires_file_read")) and not _truthy(
        contract.get("final_product_file_read_verified")
    ):
        return ["runtime_file_window_result_required_not_verified"]
    return []


def _pointer_blockers(contract: dict[str, Any]) -> list[str]:
    if contract.get("pointer_manifest_passed", contract.get("passed")) is False:
        return ["external_heap_pointer_manifest_failed"]
    return []


def _delta_blockers(contract: dict[str, Any]) -> list[str]:
    if _safe_int(contract.get("final_product_delta_applied_count")) <= 0:
        return ["final_product_delta_applied_count_zero"]
    return []


def _surface_blockers(contract: dict[str, Any]) -> list[str]:
    if not contract.get("final_product_surface_ready"):
        return ["FINAL_PRODUCT has no accepted text or code surface"]
    return []


def _result_errors(result: Any) -> list[str]:
    result = result if isinstance(result, dict) else {}
    return _list(result.get("errors"))


def _first_list(*values: Any) -> list[dict[str, Any]]:
    for value in values:
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _truthy(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def _safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
