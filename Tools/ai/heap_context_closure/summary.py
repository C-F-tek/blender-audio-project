"""Launcher summary assembly."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .requesting import startup_artifact_refs


def build_launcher_summary(args: Any, state: dict[str, Any]) -> dict[str, Any]:
    revision_payload = state["revision_context_payload"]
    startup_payload = state["startup_payload"]
    composer_report = state["composer_report"]
    external_payload = state["external_postrun_payload"]
    final_payload = state["final_readable_payload"]
    preflight_result = state["preflight_result"]
    startup_result = state["startup_result"]
    heap_result = state["heap_result"]
    composer_result = state["composer_result"]
    external_result = state["external_postrun_result"]
    final_result = state["final_readable_result"]
    startup_reconcile_result = state["startup_heap_reconcile_result"]
    code_product_contract = _code_product_contract(state, final_payload)
    external_contract = _external_heap_contract(external_payload)
    launcher_contract_errors = _launcher_contract_errors(
        args=args,
        code_product_contract=code_product_contract,
        external_contract=external_contract,
        external_result=external_result,
        final_result=final_result,
        final_payload=final_payload,
    )
    composer_product_ready = bool(
        composer_result["passed"]
        or (
            state["composer_packaging_performed"]
            and code_product_contract.get("real_code_product_ready")
        )
    )
    launcher_passed = bool(
        state["can_continue"]
        and heap_result["passed"]
        and composer_product_ready
        and not launcher_contract_errors
    )

    return {
        "schema_version": 1,
        "kind": "heap_runtime_context_closure_launcher",
        "stamp": state["stamp"],
        "repo_root": state["repo_root"].as_posix(),
        "project_python": state["project_python"],
        "run_dir": str(state["run_dir"]),
        "revision_context_selection_policy": state["revision_context_selection_policy"],
        "revision_context_path": (
            str(state["revision_context_path"]) if state["revision_context_path"] else ""
        ),
        "revision_context_loaded": bool(revision_payload),
        "operator_request_file": state["operator_request_file"],
        "request_transport": state.get("request_transport", ""),
        "request_file": (
            str(state.get("heap_request_file") or "")
            if state.get("heap_request_file")
            and Path(state["heap_request_file"]).exists()
            else ""
        ),
        "revision_context_task_count": _list_len(revision_payload.get("tasks")),
        "revision_context_requires_concrete_rewrite": revision_payload.get(
            "requires_concrete_rewrite"
        ),
        "revision_context_priority_next_action": revision_payload.get("priority_next_action"),
        "revision_context_candidate_applicability_summary": _dict_or_empty(
            revision_payload.get("candidate_applicability_summary")
        ),
        "max_iterations_requested": args.max_iterations,
        "min_runtime_rounds_requested": args.min_runtime_rounds,
        "min_proposal_iterations_requested": args.min_proposal_iterations,
        "max_rounds_forwarded": args.max_rounds,
        "preflight_performed": not args.skip_preflight,
        "preflight_passed": bool(preflight_result["passed"]),
        "preflight_blocked_startup": state["preflight_blocks_startup"],
        "preflight_nonblocking_for_provider_generation": state[
            "preflight_nonblocking_for_provider_generation"
        ],
        "preflight_report": str(state["preflight_report"]) if state["preflight_report"].exists() else "",
        "preflight_markdown": (
            str(state["preflight_markdown"]) if state["preflight_markdown"].exists() else ""
        ),
        "preflight_returncode": preflight_result["returncode"],
        "startup_reload_performed": state["startup_reload_performed"],
        "startup_reload_passed": bool(startup_result["passed"]),
        "startup_reload_degraded": state["startup_reload_degraded"],
        "startup_can_continue": state["can_continue"],
        "strict_startup_reload": bool(args.strict_startup_reload),
        "startup_manifest": str(state["startup_manifest"]) if state["startup_manifest"].exists() else "",
        "startup_heap_reconcile_returncode": startup_reconcile_result["returncode"],
        "startup_heap_reconcile_passed": bool(startup_reconcile_result["passed"]),
        "startup_heap_reconcile_report": _existing_path(state["startup_heap_reconcile_report"]),
        "startup_heap_reconcile_markdown": _existing_path(
            state["startup_heap_reconcile_markdown"]
        ),
        "startup_reconcile_degraded_policy_used": bool(
            state["startup_reload_degraded"]
            and state["can_continue"]
            and not args.strict_startup_reload
        ),
        "startup_task_file": str(state["startup_task_file"]) if state["startup_task_file"].exists() else "",
        "startup_artifacts": _dict_or_empty(startup_payload.get("artifacts")),
        "startup_artifact_ref_count": len(startup_artifact_refs(startup_payload)),
        "startup_blocking_requirements": _list_or_empty(
            startup_payload.get("blocking_requirements")
        ),
        "startup_degraded_requirements": _list_or_empty(
            startup_payload.get("degraded_requirements")
        ),
        "heap_report": str(state["report_file"]),
        "heap_markdown": str(state["markdown_file"]),
        "heap_context_closure_live_flow_status": _existing_path(
            state["run_dir"] / "heap_context_closure_live_flow.json"
        ),
        "heap_context_closure_live_flow_markdown": _existing_path(
            state["run_dir"] / "heap_context_closure_live_flow.md"
        ),
        "provider_orphan_cleanup": state.get("provider_orphan_cleanup", {}),
        "heap_returncode": heap_result["returncode"],
        "composer_returncode": composer_result["returncode"],
        "heap_passed": heap_result["passed"],
        "composer_passed": composer_result["passed"],
        "fallback_heap_report_written": state["fallback_heap_report_written"],
        "composer_packaging_performed": state["composer_packaging_performed"],
        "composer_blocking_issue_count": composer_report.get("blocking_issue_count"),
        "composer_documents_dir": state["composer_documents_dir"],
        "composer_documents_outputs": state["composer_documents_outputs"],
        "final_proposal_txt": state["final_proposal_txt"],
        "final_proposal_markdown": state["final_proposal_markdown"],
        "final_proposal_json": state["final_proposal_json"],
        "final_download_manifest_txt": state["final_download_manifest_txt"],
        "proposal_txt_outputs": state["proposal_txt_outputs"],
        "external_postrun_package_performed": bool(external_result.get("performed")),
        "external_postrun_package_passed": bool(external_result.get("passed")),
        "external_postrun_package_returncode": external_result.get("returncode"),
        "external_postrun_package_report": external_result.get("report", ""),
        "external_long_response_markdown": external_payload.get("long_response_markdown", "") or "",
        "external_revision_context_json": external_payload.get("revision_context_json", "") or "",
        "external_pointer_manifest_json": external_payload.get("pointer_manifest_json", "") or "",
        "final_readable_product_performed": bool(final_result.get("performed")),
        "final_readable_product_passed": bool(final_result.get("passed")),
        "final_readable_product_report": final_result.get("report", ""),
        "final_readable_product_markdown": final_result.get("markdown", ""),
        "final_readable_product_text": final_result.get("text", ""),
        "final_readable_product_documents_outputs": final_payload.get("documents_outputs", {}),
        "final_readable_product_zip": final_result.get("documents_zip", ""),
        "final_code_product_contract": code_product_contract,
        "external_heap_contract": external_contract,
        "launcher_contract_errors": launcher_contract_errors,
        "download_hint": composer_report.get("download_hint", ""),
        "launcher_passed": launcher_passed,
        "launcher_packaging_succeeded": bool(
            state["composer_packaging_performed"]
            and final_result.get("passed")
            and (state["can_continue"] or state["fallback_heap_report_written"])
        ),
        "preflight_stdout_tail": preflight_result["stdout_tail"],
        "preflight_stderr_tail": preflight_result["stderr_tail"],
        "heap_stdout_tail": heap_result["stdout_tail"],
        "heap_stderr_tail": heap_result["stderr_tail"],
        "preflight_command": preflight_result.get("command", []),
        "startup_command": startup_result.get("command", []),
        "heap_command": heap_result.get("command", []),
        "composer_command": composer_result.get("command", []),
        "external_postrun_command": external_result.get("command", []),
        "final_readable_product_command": final_result.get("command", []),
        "startup_stdout_tail": startup_result["stdout_tail"],
        "startup_stderr_tail": startup_result["stderr_tail"],
        "composer_stdout_tail": composer_result["stdout_tail"],
        "composer_stderr_tail": composer_result["stderr_tail"],
        "external_postrun_stdout_tail": external_result.get("stdout_tail", ""),
        "external_postrun_stderr_tail": external_result.get("stderr_tail", ""),
        "final_readable_product_stdout_tail": final_result.get("stdout_tail", ""),
        "final_readable_product_stderr_tail": final_result.get("stderr_tail", ""),
    }


def _list_len(value: Any) -> int:
    return len(value) if isinstance(value, list) else 0


def _dict_or_empty(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list_or_empty(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _existing_path(path: Any) -> str:
    return str(path) if path.exists() else ""


def _read_json_object(path_value: Any) -> dict[str, Any]:
    if not path_value:
        return {}
    path = Path(str(path_value))
    if not path.exists() or not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _read_text(path_value: Any) -> str:
    if not path_value:
        return ""
    path = Path(str(path_value))
    if not path.exists() or not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""


def _code_product_contract(state: dict[str, Any], final_payload: dict[str, Any]) -> dict[str, Any]:
    metrics = _dict_or_empty(final_payload.get("code_product_metrics"))
    documents_outputs = _dict_or_empty(final_payload.get("documents_outputs"))
    code_product_path = (
        documents_outputs.get("documents_code_product")
        or final_payload.get("full_code_product_output")
        or str(state["run_dir"] / "CODE_PRODUCT_FULL_PATCH.md")
    )
    if not metrics:
        text = _read_text(code_product_path)
        metrics = {
            "bytes": len(text.encode("utf-8")),
            "line_count": len(text.splitlines()),
            "diff_git_blocks": text.count("diff --git"),
            "empty_code_product_marker": "EMPTY CODE PRODUCT" in text,
            "no_applicable_marker": "NO_APPLICABLE_CODE_PRODUCT" in text,
            "truncation_marker": "[truncated]" in text.lower(),
        }
    real_code_product_ready = bool(
        final_payload.get("real_code_product_ready")
        or (
            int(metrics.get("diff_git_blocks") or 0) > 0
            and not metrics.get("empty_code_product_marker")
            and not metrics.get("no_applicable_marker")
            and not metrics.get("truncation_marker")
        )
    )
    return {
        "path": str(code_product_path or ""),
        "real_code_product_ready": real_code_product_ready,
        "metrics": metrics,
        "final_document_status": final_payload.get("final_document_status"),
        "blocking_reasons": _list_or_empty(final_payload.get("blocking_reasons")),
    }


def _external_heap_contract(external_payload: dict[str, Any]) -> dict[str, Any]:
    long_md = str(external_payload.get("long_response_markdown") or "")
    long_json = Path(long_md).with_suffix(".json") if long_md else None
    long_response = _read_json_object(long_json)
    revision = _read_json_object(external_payload.get("revision_context_json"))
    pointer = _read_json_object(external_payload.get("pointer_manifest_json"))
    stats = _dict_or_empty(long_response.get("stats"))
    roles = set(
        _list_or_empty(stats.get("all_roles_present"))
        or _list_or_empty(revision.get("all_roles_present"))
        or _list_or_empty(pointer.get("all_roles_present"))
        or _list_or_empty(pointer.get("roles_present"))
    )
    pointer_contract = _dict_or_empty(
        long_response.get("pointer_product_contract")
        or revision.get("pointer_product_contract")
        or pointer.get("pointer_product_contract")
    )
    return {
        "postrun_passed": bool(external_payload.get("passed")),
        "provider_execution_performed": bool(
            external_payload.get("provider_execution_performed")
            or long_response.get("provider_execution_performed")
            or revision.get("provider_execution_performed")
            or pointer.get("provider_execution_performed")
        ),
        "long_response_path": str(long_json) if long_json else "",
        "long_response_passed": bool(long_response.get("passed")),
        "revision_context_path": str(external_payload.get("revision_context_json") or ""),
        "revision_context_operational": bool(revision.get("operational_revision_context")),
        "revision_context_passed": bool(revision.get("passed")),
        "pointer_manifest_path": str(external_payload.get("pointer_manifest_json") or ""),
        "pointer_manifest_passed": bool(pointer.get("passed")),
        "roles_present": sorted(roles),
        "missing_roles": sorted(
            {"gpu1_planner", "gpu0_reviewer_refiner", "npu_auditor"} - roles
        ),
        "proposal_block_count": _safe_int(stats.get("proposal_block_count") or revision.get("proposal_block_count")),
        "pointer_block_count": _safe_int(stats.get("pointer_block_count") or revision.get("pointer_block_count")),
        "gpu1_block_count": _safe_int(stats.get("gpu1_block_count")),
        "gpu0_block_count": _safe_int(stats.get("gpu0_block_count") or revision.get("gpu0_block_count")),
        "npu_block_count": _safe_int(stats.get("npu_block_count") or revision.get("npu_block_count")),
        "supports_forward_navigation": bool(pointer_contract.get("supports_forward_navigation")),
        "supports_backrefinement": bool(pointer_contract.get("supports_backrefinement")),
        "supports_resume": bool(pointer_contract.get("supports_resume")),
    }


def _launcher_contract_errors(
    *,
    args: Any,
    code_product_contract: dict[str, Any],
    external_contract: dict[str, Any],
    external_result: dict[str, Any],
    final_result: dict[str, Any],
    final_payload: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    if not final_result.get("passed"):
        errors.append("final readable product did not pass the real code product contract")
    if not code_product_contract.get("real_code_product_ready"):
        errors.append("CODE_PRODUCT_FULL_PATCH.md is missing a real non-truncated diff product")
    if final_payload.get("final_document_status") in {
        "DIAGNOSTIC_REVIEW_READY",
        "NO_APPLICABLE_CODE_PRODUCT",
    }:
        errors.append(
            "final product is diagnostic/no-applicable instead of a concrete code product"
        )
    if not external_result.get("passed"):
        errors.append("external heap postrun package did not complete")
    if getattr(args, "allow_provider_generation", False):
        if not external_contract.get("provider_execution_performed"):
            errors.append("provider execution evidence is missing")
        if external_contract.get("missing_roles"):
            errors.append(
                "external heap is missing provider roles: "
                + ",".join(external_contract.get("missing_roles") or [])
            )
        for key in ("proposal_block_count", "pointer_block_count", "gpu0_block_count", "npu_block_count"):
            if _safe_int(external_contract.get(key)) <= 0:
                errors.append(f"external heap contract requires {key} > 0")
        for key in (
            "supports_forward_navigation",
            "supports_backrefinement",
            "supports_resume",
        ):
            if not external_contract.get(key):
                errors.append(f"external heap pointer contract missing {key}")
        if not external_contract.get("revision_context_operational"):
            errors.append("external heap revision context is not operational")
    return errors


def _safe_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0
