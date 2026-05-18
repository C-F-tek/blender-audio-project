"""Broker request execution and report aggregation."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any

from Tools.ai._shared.agent_runtime_tool_broker_execution import execute_command_timed
from Tools.validation._shared.report_utils import read_json_report

from .common import (
    compact_value,
    fixture_repo_write,
    now_iso,
    output_owned_artifact_write,
    repo_rel,
    resolve_path,
    safe_id,
    truthy,
    validate_request_args,
)
from .registry import TOOL_SPECS

def extract_tool_requests(data: dict[str, Any]) -> list[dict[str, Any]]:
    requests = data.get("tool_requests", [])
    if not isinstance(requests, list):
        return []
    return [item for item in requests if isinstance(item, dict)]


def first_tool_request_source(tool_requests: list[dict[str, Any]]) -> str:
    for item in tool_requests:
        source = str(item.get("source") or "").strip()
        if source:
            return source
    return ""


def infer_request_source(requests_data: dict[str, Any], request_path: Path) -> str:
    for key in ("source", "source_lane", "target_lane"):
        value = str(requests_data.get(key) or "").strip()
        if value:
            return value

    tool_request_source = first_tool_request_source(extract_tool_requests(requests_data))
    if tool_request_source:
        return tool_request_source

    kind = str(requests_data.get("kind") or "").strip()
    if kind == "gpu0_peer_tool_requests":
        return "gpu0_peer_companion"
    if kind == "npu_gpu_deep_review_audit":
        return "npu_micro_peer_assistant"
    if kind == "agent_runtime_tool_requests":
        return "gpu1_primary_advisory"

    path_text = request_path.as_posix().lower()
    if "gpu0" in path_text:
        return "gpu0_peer_companion"
    if "npu_micro" in path_text or "/npu_" in path_text:
        return "npu_micro_peer_assistant"
    if "gpu1" in path_text:
        return "gpu1_primary_advisory"
    return kind or "unknown"


def execute_tool_request(
    *,
    repo_root: Path,
    out_dir: Path,
    index: int,
    request: dict[str, Any],
    timeout_seconds: int,
    dry_run: bool,
) -> dict[str, Any]:
    request_id = safe_id(request.get("id"), f"tool_{index:03d}")
    tool_name = str(request.get("tool") or "")
    request_args = request.get("args") if isinstance(request.get("args"), dict) else {}
    base_result: dict[str, Any] = {
        "id": request_id,
        "tool": tool_name,
        "reason": str(request.get("reason") or ""),
        "requirement": str(request.get("requirement") or ""),
        "requested": True,
        "executed": False,
        "blocked": False,
        "dry_run": dry_run,
        "status": "dry_run_pending" if dry_run else "pending",
        "persistent_memory_write_authorized": False,
        "code_product_safe_apply_authorized": False,
        "returncode": None,
        "errors": [],
        "warnings": [],
        "outputs": {},
        "summary": {},
        "guardrails": {
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "persistent_memory_write_count": 0,
            "persistent_memory_write_requires_explicit_confirm": True,
            "operational_sqlite_write_performed": False,
            "operational_memory_write_performed": False,
            "operational_memory_clear_performed": False,
            "blender_runtime_touched": False,
            "git_write_performed": False,
        },
    }

    base_result["persistent_memory_write_authorized"] = (
        tool_name == "runtime_sqlite_memory"
        and str(request_args.get("action") or "") == "remember"
        and str(request_args.get("scope") or "") == "persistent"
        and truthy(request_args.get("allow_persistent_write"))
        and str(request_args.get("confirm") or "") == "persistent_write"
    )
    base_result["code_product_safe_apply_authorized"] = (
        tool_name == "analyze_code_product_artifact"
        and truthy(request_args.get("apply_safe"))
        and str(request_args.get("confirm") or "") == "safe_apply"
    )

    spec = TOOL_SPECS.get(tool_name)
    if spec is None:
        base_result["blocked"] = True
        base_result["status"] = "blocked_not_allowlisted"
        base_result["errors"] = [f"tool not allowlisted: {tool_name}"]
        return base_result

    arg_errors = validate_request_args(tool_name, request_args, spec.allowed_args)
    if arg_errors:
        base_result["blocked"] = True
        base_result["status"] = "blocked_invalid_args"
        base_result["errors"] = arg_errors
        return base_result

    command, outputs = spec.builder(repo_root, out_dir, request_id, request_args)
    base_result["command"] = command
    base_result["outputs"] = outputs

    if dry_run:
        base_result["status"] = "dry_run"
        return base_result

    timed = execute_command_timed(command, repo_root, timeout_seconds)
    base_result["executed"] = True
    base_result["returncode"] = timed.returncode
    base_result["started_at"] = timed.started_at
    base_result["finished_at"] = timed.finished_at
    base_result["elapsed_seconds"] = timed.elapsed_seconds
    base_result["status"] = "executed_ok" if timed.returncode == 0 else "executed_failed"
    base_result["stdout_tail"] = timed.stdout_tail
    base_result["stderr_tail"] = timed.stderr_tail
    if timed.error:
        base_result["errors"].append(timed.error)
    if timed.returncode != 0:
        base_result["errors"].append(f"tool returned {timed.returncode}")

    json_report = outputs.get("json_report")
    if json_report:
        report_data = read_json_report(resolve_path(repo_root, json_report))
        if report_data:
            base_result["summary"] = {
                "kind": report_data.get("kind"),
                "passed": report_data.get("passed"),
                "target_count": report_data.get("target_count"),
                "verified_target_count": report_data.get("verified_target_count"),
                "concrete_code_proposal_count": report_data.get(
                    "concrete_code_proposal_count"
                ),
                "patch_candidate_synthesis_requested": report_data.get(
                    "patch_candidate_synthesis_requested"
                ),
                "patch_candidate_synthesis_passed_count": report_data.get(
                    "patch_candidate_synthesis_passed_count"
                ),
                "candidate_count": report_data.get("candidate_count"),
                "tool_catalog_ref_count": report_data.get("tool_catalog_ref_count"),
                "startup_artifact_ref_count": report_data.get("startup_artifact_ref_count"),
                "errors": compact_value(report_data.get("errors", [])),
                "warnings": compact_value(report_data.get("warnings", [])),
                "decision": compact_value(report_data.get("decision", {})),
                "guardrails": compact_value(report_data.get("guardrails", {})),
            }
            guardrails = (
                report_data.get("guardrails")
                if isinstance(report_data.get("guardrails"), dict)
                else {}
            )
            source_writes = bool(
                report_data.get("source_writes_performed")
                or guardrails.get("source_writes_performed")
            )
            patch_application = bool(
                report_data.get("patch_application_performed")
                or guardrails.get("patch_application_performed")
            )
            git_write = bool(
                report_data.get("git_write_performed") or guardrails.get("git_write_performed")
            )
            fixture_write = fixture_repo_write(repo_root, report_data, outputs)
            output_artifact_write = output_owned_artifact_write(repo_root, report_data, outputs)
            if source_writes and fixture_write:
                source_writes = False
                base_result["warnings"].append(
                    "fixture/output write ignored for source-write guardrail"
                )
            elif (
                source_writes and output_artifact_write and not patch_application and not git_write
            ):
                source_writes = False
                base_result["warnings"].append(
                    "output-owned artifact write ignored for source-write guardrail"
                )
            if patch_application and fixture_write and not git_write:
                patch_application = False
                base_result["warnings"].append(
                    "fixture patch application ignored for patch guardrail"
                )
            base_result["guardrails"].update(
                {
                    "provider_execution_performed": bool(
                        report_data.get("provider_execution_performed")
                        or guardrails.get("provider_execution_performed")
                    ),
                    "patch_application_performed": patch_application,
                    "source_writes_performed": source_writes,
                    "sqlite_write_performed": bool(
                        guardrails.get("sqlite_write_performed")
                        or guardrails.get("sqlite_db_committed")
                        or guardrails.get("sqlite_db_touched") is True
                        and not guardrails.get("sqlite_read_only")
                    ),
                    "persistent_memory_write_performed": bool(
                        guardrails.get("persistent_memory_write_performed")
                        or guardrails.get("memory_promotion_performed")
                    ),
                    "operational_sqlite_write_performed": bool(
                        report_data.get("operational_sqlite_write_performed")
                        or guardrails.get("operational_sqlite_write_performed")
                    ),
                    "operational_memory_write_performed": bool(
                        report_data.get("operational_memory_write_performed")
                        or guardrails.get("operational_memory_write_performed")
                    ),
                    "operational_memory_clear_performed": bool(
                        report_data.get("operational_memory_clear_performed")
                        or guardrails.get("operational_memory_clear_performed")
                    ),
                    "blender_runtime_touched": bool(guardrails.get("blender_runtime_touched")),
                    "git_write_performed": git_write,
                }
            )
            report_only_review_required = (
                timed.returncode != 0
                and guardrails.get("report_only") is True
                and guardrails.get("manual_review_required") is True
                and not report_data.get("errors")
                and not base_result["guardrails"].get("provider_execution_performed")
                and not base_result["guardrails"].get("patch_application_performed")
                and not base_result["guardrails"].get("source_writes_performed")
                and not base_result["guardrails"].get("sqlite_write_performed")
                and not base_result["guardrails"].get("persistent_memory_write_performed")
                and not base_result["guardrails"].get("git_write_performed")
            )
            if report_only_review_required:
                base_result["status"] = "executed_review_required"
                base_result["errors"] = [
                    error
                    for error in base_result["errors"]
                    if not error.startswith("tool returned ")
                ]
                base_result["warnings"].append(
                    "report-only manual-review result did not fail broker guardrails"
                )
    return base_result


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    request_path = resolve_path(repo_root, args.request_file)
    requests_data = read_json_report(request_path)
    tool_requests = extract_tool_requests(requests_data)
    request_source = infer_request_source(requests_data, request_path)
    stamp = args.stamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = resolve_path(repo_root, args.tool_output_dir or f"output/ai_runtime_tools/{stamp}")
    out_dir.mkdir(parents=True, exist_ok=True)

    results = [
        execute_tool_request(
            repo_root=repo_root,
            out_dir=out_dir,
            index=index,
            request=request,
            timeout_seconds=args.timeout_seconds,
            dry_run=args.dry_run,
        )
        for index, request in enumerate(tool_requests, start=1)
    ]

    blocked = [item for item in results if item.get("blocked")]
    executed = [item for item in results if item.get("executed")]
    failed = [item for item in results if item.get("errors") and not item.get("blocked")]
    dangerous_guardrail = [
        item
        for item in results
        if item.get("guardrails", {}).get("provider_execution_performed")
        or (
            item.get("guardrails", {}).get("patch_application_performed")
            and not item.get("code_product_safe_apply_authorized")
        )
        or (
            item.get("guardrails", {}).get("source_writes_performed")
            and not item.get("code_product_safe_apply_authorized")
        )
        or (
            item.get("guardrails", {}).get("sqlite_write_performed")
            and not item.get("persistent_memory_write_authorized")
        )
        or (
            item.get("guardrails", {}).get("persistent_memory_write_performed")
            and not item.get("persistent_memory_write_authorized")
        )
        or item.get("guardrails", {}).get("blender_runtime_touched")
        or item.get("guardrails", {}).get("git_write_performed")
    ]
    operational_sqlite_write_count = sum(
        1
        for item in results
        if item.get("guardrails", {}).get("operational_sqlite_write_performed")
    )
    persistent_memory_write_count = sum(
        1 for item in results if item.get("guardrails", {}).get("persistent_memory_write_performed")
    )
    source_write_count = sum(
        1 for item in results if item.get("guardrails", {}).get("source_writes_performed")
    )
    patch_application_count = sum(
        1 for item in results if item.get("guardrails", {}).get("patch_application_performed")
    )
    operational_memory_clear_count = sum(
        1
        for item in results
        if item.get("guardrails", {}).get("operational_memory_clear_performed")
    )

    return {
        "schema_version": 1,
        "kind": "agent_runtime_tool_broker",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "request_file": repo_rel(request_path, repo_root),
        "request_kind": requests_data.get("kind"),
        "source": request_source,
        "source_classification": request_source,
        "tool_output_dir": repo_rel(out_dir, repo_root),
        "passed": not failed and not dangerous_guardrail,
        "errors": [f"{item.get('id')}: {err}" for item in failed for err in item.get("errors", [])]
        + [f"{item.get('id')}: guardrail violation" for item in dangerous_guardrail],
        "warnings": [f"{item.get('id')}: blocked {item.get('errors')}" for item in blocked],
        "provider_execution_performed": False,
        "patch_application_performed": patch_application_count > 0,
        "source_writes_performed": source_write_count > 0,
        "sqlite_write_performed": persistent_memory_write_count > 0,
        "persistent_memory_write_performed": persistent_memory_write_count > 0,
        "operational_sqlite_write_performed": operational_sqlite_write_count > 0,
        "operational_sqlite_write_count": operational_sqlite_write_count,
        "persistent_memory_write_count": persistent_memory_write_count,
        "operational_memory_clear_count": operational_memory_clear_count,
        "blender_runtime_execution_performed": False,
        "git_write_performed": False,
        "dry_run": bool(args.dry_run),
        "tool_request_count": len(tool_requests),
        "tool_execution_count": len(executed),
        "blocked_tool_count": len(blocked),
        "failed_tool_count": len(failed),
        "allowlisted_tools": sorted(TOOL_SPECS),
        "tool_results": results,
        "guardrails": {
            "free_shell_exposed": False,
            "allowlist_enforced": True,
            "provider_execution_performed": False,
            "patch_application_performed": patch_application_count > 0,
            "source_writes_performed": source_write_count > 0,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "operational_sqlite_write_allowed_under_output": True,
            "operational_sqlite_write_performed": operational_sqlite_write_count > 0,
            "operational_memory_clear_count": operational_memory_clear_count,
            "blender_runtime_touched": False,
            "git_write_performed": False,
            "manual_review_required": True,
        },
    }
