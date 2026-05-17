"""Launcher summary assembly."""

from __future__ import annotations

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
        "request_file": str(state["heap_request_file"]),
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
        "download_hint": composer_report.get("download_hint", ""),
        "launcher_passed": bool(
            state["can_continue"] and heap_result["passed"] and composer_result["passed"]
        ),
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
