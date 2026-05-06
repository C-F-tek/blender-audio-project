#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[2]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def safe_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def compact_list(value: Any, limit: int = 8) -> list[Any]:
    return value[:limit] if isinstance(value, list) else []


def npu_support_lane_summary(npu: dict[str, Any], npu_broker: dict[str, Any]) -> dict[str, Any]:
    # Summarize NPU as non-blocking tool-support, not heavy authority.
    auditor = npu.get("npu_auditor") if isinstance(npu.get("npu_auditor"), dict) else {}
    classification = str(auditor.get("classification") or npu.get("classification") or "")
    tool_request_count = safe_int(npu.get("tool_request_count") or auditor.get("tool_request_count"))
    broker_execution_count = safe_int(npu_broker.get("tool_execution_count"))
    provider_performed = bool(npu.get("provider_execution_performed"))
    provider_requested = bool(npu.get("provider_execution_requested"))
    fallback_used = bool(npu.get("npu_deterministic_tool_fallback_used") or auditor.get("npu_deterministic_tool_fallback_used"))
    slow_or_degraded = bool(
        provider_requested
        and not provider_performed
        and (
            npu.get("provider_empty_response")
            or npu.get("dependency_missing")
            or classification in {"provider_empty_response", "unusable_output", "dependency_missing_openvino_genai", "npu_python_missing"}
        )
    )
    return {
        "role": "npu_non_blocking_tool_support_lane",
        "non_blocking": True,
        "blocking": False,
        "heavy_audit_authority": False,
        "tool_supply_support": bool(tool_request_count or broker_execution_count or fallback_used),
        "tool_request_count": tool_request_count,
        "broker_tool_execution_count": broker_execution_count,
        "provider_execution_requested": provider_requested,
        "provider_execution_performed": provider_performed,
        "provider_slow_or_degraded": slow_or_degraded,
        "classification": classification,
        "deterministic_fallback_used": fallback_used,
        "product_pass_blocker": False,
    }


def build_peer_mesh_visibility(
    primary: dict[str, Any],
    response: dict[str, Any],
    broker: dict[str, Any],
    npu: dict[str, Any],
    npu_broker: dict[str, Any],
    sources: list[dict[str, Any]],
) -> dict[str, Any]:
    # Record what each AI lane can see in the peer-exchange round.
    gpu0_tool_request_count = safe_int(response.get("tool_request_count"))
    gpu0_broker_execution_count = safe_int(broker.get("tool_execution_count"))
    npu_tool_request_count = safe_int(npu.get("tool_request_count"))
    npu_broker_execution_count = safe_int(npu_broker.get("tool_execution_count"))
    npu_seen = bool(npu)
    gpu0_seen = bool(response)
    gpu0_broker_seen = bool(broker)
    npu_broker_seen = bool(npu_broker)
    return {
        "schema_version": 1,
        "kind": "ai_peer_mesh_visibility",
        "all_lanes_visible": bool(primary and gpu0_seen and gpu0_broker_seen and (not npu_seen or npu_broker_seen)),
        "gpu1_sees_gpu0_response": gpu0_seen,
        "gpu1_sees_gpu0_broker_results": gpu0_broker_execution_count > 0,
        "gpu1_sees_npu_support_signal": npu_seen,
        "gpu1_sees_npu_broker_results": npu_broker_execution_count > 0,
        "gpu0_sees_gpu1_primary_advisory": bool(primary),
        "gpu0_sees_deterministic_reports": bool(sources),
        "gpu0_produces_tool_requests_for_gpu1": gpu0_tool_request_count > 0,
        "gpu0_tool_requests_broker_consumed": bool(gpu0_tool_request_count and gpu0_broker_execution_count > 0),
        "npu_sees_gpu1_gpu0_broker_context": npu_seen,
        "npu_support_tool_requests_available": npu_tool_request_count > 0,
        "npu_tool_requests_broker_consumed": bool(npu_tool_request_count and npu_broker_execution_count > 0),
        "deterministic_scripts_visible_to_gpu0": bool(sources),
        "runtime_tool_broker_visible_to_all_lanes": bool(gpu0_broker_seen or npu_broker_seen),
        "npu_non_blocking_support_lane": True,
    }


def primary_advisory(repo_root: Path, stamp: str, gpu_report_path: Path, gpu_markdown_path: Path) -> dict[str, Any]:
    gpu_report = read_json(gpu_report_path)
    round_count = safe_int(gpu_report.get("round_count"))
    provider_performed = bool(gpu_report.get("provider_execution_performed"))
    empty = bool(gpu_report.get("provider_empty_response"))
    classification = str(gpu_report.get("classification") or "")
    proven = bool(provider_performed and round_count > 0 and not empty and classification != "required_provider_artifact_missing")
    classifications: list[str] = []
    if not proven:
        classifications.append("gpu1_primary_advisory_not_proven")
    if empty:
        classifications.append("gpu1_primary_advisory_empty_response")
    if classification:
        classifications.append(f"gpu1_primary_classification:{classification}")
    return {
        "schema_version": 1,
        "kind": "gpu1_primary_advisory",
        "generated_at": now_iso(),
        "stamp": stamp,
        "role": "gpu1_master_planner_worker",
        "lane": "GPU1/Ollama/RTX5080",
        "passed": proven,
        "provider_execution_performed": provider_performed,
        "gpu_report": repo_rel(repo_root, gpu_report_path),
        "gpu_markdown": repo_rel(repo_root, gpu_markdown_path) if gpu_markdown_path.exists() else "",
        "gpu_report_exists": gpu_report_path.exists(),
        "round_count": round_count,
        "recommendation_count": safe_int(gpu_report.get("recommendation_count")),
        "runtime_tool_request_count": safe_int(gpu_report.get("runtime_tool_request_count")),
        "runtime_tool_execution_count": safe_int(gpu_report.get("runtime_tool_execution_count")),
        "provider_empty_response": empty,
        "classification": classification,
        "classifications": classifications,
        "errors": [] if proven else ["GPU1/Ollama primary advisory execution was not proven by the GPU report."],
        "warnings": [],
        "recommendations_preview": compact_list(gpu_report.get("recommendations")),
        "decision": gpu_report.get("decision") if isinstance(gpu_report.get("decision"), dict) else {},
        "guardrails": {
            "report_only": True,
            "gpu1_reserved_for_primary_ollama": True,
            "openvino_gpu1_workload_allowed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
        },
    }


def source_summaries(repo_root: Path, paths: list[str]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for raw in paths:
        path = resolve_output_path(repo_root, raw)
        data = read_json(path)
        summaries.append(
            {
                "path": repo_rel(repo_root, path),
                "exists": path.exists(),
                "kind": data.get("kind"),
                "passed": data.get("passed"),
                "classifications": data.get("classifications", []) if isinstance(data.get("classifications"), list) else [],
                "errors": compact_list(data.get("errors"), 5),
                "warnings": compact_list(data.get("warnings"), 5),
            }
        )
    return summaries


def build_tasks(primary: dict[str, Any], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failed_sources = [item for item in sources if item.get("passed") is False]
    tasks = [
        {
            "id": "gpu0_peer_primary_advisory_quality",
            "role": "companion_peer_worker",
            "objective": "Verify whether GPU1/Ollama planned and worked on usable primary advisory evidence.",
            "requires_semantic_model": False,
        },
        {
            "id": "gpu0_peer_runtime_tool_context",
            "role": "companion_peer_worker",
            "objective": "Request broker-controlled deterministic tool evidence for GPU1 planner follow-up.",
            "requires_semantic_model": False,
        },
        {
            "id": "gpu0_peer_patch_spec_readiness",
            "role": "companion_peer_worker",
            "objective": "Check whether recommendations, patch specs and validation evidence can support a review-only patch proposal.",
            "requires_semantic_model": False,
        },
    ]
    if not primary.get("passed"):
        tasks.append(
            {
                "id": "gpu0_peer_gpu1_degradation_root_cause",
                "role": "companion_peer_worker",
                "objective": "Summarize why GPU1 primary advisory is degraded before the run is accepted.",
                "requires_semantic_model": False,
            }
        )
    if failed_sources:
        tasks.append(
            {
                "id": "gpu0_peer_failed_report_triage",
                "role": "companion_peer_worker",
                "objective": "Triage failed deterministic reports and return compact blockers for GPU1.",
                "requires_semantic_model": False,
            }
        )
    return tasks


def tool_request_templates(source_paths: list[str], audit_source_paths: list[str]) -> list[dict[str, Any]]:
    joined_reports = ",".join(source_paths[:8])
    audit_reports = ",".join(audit_source_paths[:8])
    return [
        {
            "id": "gpu0_peer_code_interpreter_context",
            "tool": "build_code_interpreter_report",
            "reason": "GPU0 peer worker needs current code-structure context through the broker allowlist.",
            "args": {"input": "Tools/ai,Tools/validation,Tools/workflow,Tools/npu"},
            "source": "gpu0_peer_companion",
        },
        {
            "id": "gpu0_peer_report_contract_context",
            "tool": "check_validation_report_contract",
            "reason": "GPU0 peer worker needs report-contract status for the evidence it received.",
            "args": {"report_file": joined_reports} if joined_reports else {},
            "source": "gpu0_peer_companion",
        },
        {
            "id": "gpu0_peer_refactor_duplication_context",
            "tool": "build_refactor_duplication_audit",
            "reason": "GPU0 peer worker needs deterministic reuse/refactor overlap evidence.",
            "args": {"root": "Tools/ai,Tools/validation,Tools/workflow,Tools/npu", "report": audit_reports} if audit_reports else {"root": "Tools/ai,Tools/validation,Tools/workflow,Tools/npu"},
            "source": "gpu0_peer_companion",
        },
    ]


def build_exchange(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    primary_path = resolve_output_path(repo_root, args.primary_output.format(stamp=args.stamp))
    task_path = resolve_output_path(repo_root, args.task_output.format(stamp=args.stamp))
    response_path = resolve_output_path(repo_root, args.response_report.format(stamp=args.stamp)) if args.response_report else None
    broker_path = resolve_output_path(repo_root, args.broker_report.format(stamp=args.stamp)) if args.broker_report else None
    npu_path = resolve_output_path(repo_root, args.npu_report.format(stamp=args.stamp)) if args.npu_report else None
    npu_broker_path = resolve_output_path(repo_root, args.npu_broker_report.format(stamp=args.stamp)) if args.npu_broker_report else None
    contract_path = resolve_output_path(repo_root, args.contract_report.format(stamp=args.stamp)) if args.contract_report else None
    primary = primary_advisory(repo_root, args.stamp, resolve_output_path(repo_root, args.gpu_report), resolve_output_path(repo_root, args.gpu_markdown or ""))
    sources = source_summaries(repo_root, args.source_report)
    tasks = build_tasks(primary, sources)
    existing_source_paths = [item["path"] for item in sources if item.get("exists")]
    passed_source_paths = [item["path"] for item in sources if item.get("exists") and item.get("passed") is not False]
    templates = tool_request_templates(existing_source_paths, passed_source_paths)
    task_packet = {
        "schema_version": 1,
        "kind": "gpu0_peer_task_packet",
        "generated_at": now_iso(),
        "stamp": args.stamp,
        "source_lane": "gpu1_master_primary_advisory_worker",
        "target_lane": "gpu0_openvino_peer_worker",
        "passed": bool(tasks),
        "primary_advisory_report": repo_rel(repo_root, primary_path),
        "task_count": len(tasks),
        "tasks": tasks,
        "tool_request_templates": templates,
        "source_reports": sources,
        "peer_visibility": {
            "gpu0_sees_gpu1_primary_advisory": True,
            "gpu0_sees_deterministic_reports": bool(sources),
            "gpu0_produces_tool_requests_for_gpu1": True,
            "gpu0_must_return_response_for_gpu1": True,
            "gpu1_must_consume_gpu0_response": True,
            "npu_must_see_gpu1_gpu0_broker_context_when_present": True,
            "npu_is_non_blocking_tool_support_lane": True,
            "npu_slow_or_degraded_must_not_block_product": True,
            "runtime_tool_broker_required_for_tool_requests": True,
            "runtime_tool_broker_visible_to_gpu1_gpu0_npu": True,
        },
        "guardrails": {
            "report_only": True,
            "runtime_tool_broker_required_for_tool_requests": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "openvino_gpu1_workload_allowed": False,
        },
    }
    response = read_json(response_path) if response_path else {}
    broker = read_json(broker_path) if broker_path else {}
    npu = read_json(npu_path) if npu_path else {}
    npu_broker = read_json(npu_broker_path) if npu_broker_path else {}
    contract = read_json(contract_path) if contract_path else {}
    classifications = list(primary.get("classifications") or [])
    warnings: list[str] = []
    if response_path and response_path.exists():
        classifications.extend(str(item) for item in response.get("classifications", []) if item not in classifications)
    else:
        classifications.append("gpu1_gpu0_roundtrip_missing")
    tool_count = safe_int(response.get("tool_request_count"))
    broker_exec = safe_int(broker.get("tool_execution_count"))
    if tool_count and broker_exec <= 0:
        classifications.append("gpu0_tool_requests_not_broker_consumed")
    if npu_path and npu_path.exists():
        if npu.get("non_blocking") is not True:
            warnings.append("npu_micro_lane_present_but_non_blocking_flag_missing")
        if npu.get("decision", {}).get("npu_primary_advisory") is True:
            warnings.append("npu_micro_lane_attempted_primary_advisory_promotion")
    else:
        warnings.append("npu_micro_lane_missing_or_pending_non_blocking")
    collaboration_round = {
        "kind": "ai_peer_collaboration_round",
        "synchronized_visibility": True,
        "gpu1": {
            "role": "gpu1_master_planner_worker",
            "works_and_plans": True,
            "sees_gpu0_response": bool(response),
            "sees_gpu0_broker_results": broker_exec > 0,
            "sees_npu_micro_signal": bool(npu),
        },
        "gpu0": {
            "role": "gpu0_companion_tool_request_producer",
            "provider_execution_performed": bool(response.get("provider_execution_performed")),
            "produces_tool_requests": tool_count > 0,
            "broker_tool_executions": broker_exec,
        },
        "npu": {
            "role": "npu_support_tool_micro_lane_non_blocking",
            "non_blocking": True,
            "report_seen": bool(npu),
            "provider_execution_requested": bool(npu.get("provider_execution_requested")),
            "provider_execution_performed": bool(npu.get("provider_execution_performed")),
            "tool_request_count": safe_int(npu.get("tool_request_count")),
            "broker_tool_executions": safe_int(npu_broker.get("tool_execution_count")),
        },
        "deterministic_scripts": {
            "role": "tool_agnostic_heavy_audit_and_validation_authority",
            "source_report_count": len(sources),
        },
        "runtime_tool_broker": {
            "role": "controlled_tool_execution_for_gpu1_gpu0_npu_requests",
            "gpu0_tool_execution_count": broker_exec,
            "npu_tool_execution_count": safe_int(npu_broker.get("tool_execution_count")),
        },
    }
    npu_support_lane = npu_support_lane_summary(npu, npu_broker)
    peer_mesh_visibility = build_peer_mesh_visibility(primary, response, broker, npu, npu_broker, sources)
    collaboration_round["mesh_visibility"] = peer_mesh_visibility
    collaboration_round["npu_support_lane"] = npu_support_lane

    exchange = {
        "schema_version": 1,
        "kind": "ai_peer_exchange",
        "generated_at": now_iso(),
        "stamp": args.stamp,
        "passed": bool(primary.get("passed") and response.get("passed") is True and (not tool_count or broker_exec > 0)),
        "primary_advisory": primary,
        "task_packet": task_packet,
        "gpu0_response": response,
        "runtime_tool_broker": broker,
        "npu_micro_response": npu,
        "npu_runtime_tool_broker": npu_broker,
        "collaboration_round": collaboration_round,
        "peer_mesh_visibility": peer_mesh_visibility,
        "npu_support_lane": npu_support_lane,
        "contract": contract,
        "classifications": list(dict.fromkeys(classifications)),
        "errors": [],
        "warnings": warnings,
        "provider_execution_performed": bool(primary.get("provider_execution_performed") or response.get("provider_execution_performed") or npu.get("provider_execution_performed")),
        "patch_application_performed": False,
        "source_writes_performed": False,
        "paths": {
            "primary_advisory": repo_rel(repo_root, primary_path),
            "task_packet": repo_rel(repo_root, task_path),
            "gpu0_response": repo_rel(repo_root, response_path) if response_path else "",
            "gpu0_runtime_tool_broker": repo_rel(repo_root, broker_path) if broker_path else "",
            "npu_micro_response": repo_rel(repo_root, npu_path) if npu_path else "",
            "npu_runtime_tool_broker": repo_rel(repo_root, npu_broker_path) if npu_broker_path else "",
            "contract": repo_rel(repo_root, contract_path) if contract_path else "",
        },
        "guardrails": {
            "report_only": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "openvino_gpu1_workload_allowed": False,
            "npu_micro_lane_non_blocking": True,
        },
    }
    return {"primary": primary, "task_packet": task_packet, "exchange": exchange}


def render_primary(report: dict[str, Any]) -> str:
    return "\n".join([
        "# GPU1 Primary Advisory",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Provider execution performed: `{report.get('provider_execution_performed')}`",
        f"- Round count: `{report.get('round_count')}`",
        f"- Recommendation count: `{report.get('recommendation_count')}`",
        f"- Classifications: `{report.get('classifications')}`",
        "",
    ])


def render_exchange(report: dict[str, Any]) -> str:
    return "\n".join([
        "# AI Peer Exchange",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Provider execution performed: `{report.get('provider_execution_performed')}`",
        f"- Classifications: `{report.get('classifications')}`",
        f"- Task count: `{report.get('task_packet', {}).get('task_count')}`",
        f"- GPU0 response passed: `{report.get('gpu0_response', {}).get('passed')}`",
        f"- Broker executions: `{report.get('runtime_tool_broker', {}).get('tool_execution_count')}`",
        f"- NPU micro lane seen: `{bool(report.get('npu_micro_response'))}`",
        f"- NPU broker executions: `{report.get('npu_runtime_tool_broker', {}).get('tool_execution_count')}`",
        f"- Peer mesh all lanes visible: `{report.get('peer_mesh_visibility', {}).get('all_lanes_visible')}`",
        f"- NPU support tool supply: `{report.get('npu_support_lane', {}).get('tool_supply_support')}`",
        f"- NPU slow/degraded non-blocking: `{report.get('npu_support_lane', {}).get('provider_slow_or_degraded')}`",
        "",
    ])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--gpu-report", required=True)
    parser.add_argument("--gpu-markdown", default="")
    parser.add_argument("--source-report", action="append", default=[])
    parser.add_argument("--response-report", default="")
    parser.add_argument("--broker-report", default="")
    parser.add_argument("--npu-report", default="")
    parser.add_argument("--npu-broker-report", default="")
    parser.add_argument("--contract-report", default="")
    parser.add_argument("--primary-output", default="output/validation/gpu1_primary_advisory_{stamp}.json")
    parser.add_argument("--primary-markdown-output", default="output/validation/gpu1_primary_advisory_{stamp}.md")
    parser.add_argument("--task-output", default="output/validation/gpu0_peer_task_packet_{stamp}.json")
    parser.add_argument("--exchange-output", default="output/validation/ai_peer_exchange_{stamp}.json")
    parser.add_argument("--exchange-markdown-output", default="output/validation/ai_peer_exchange_{stamp}.md")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    built = build_exchange(args)
    primary_path = resolve_output_path(repo_root, args.primary_output.format(stamp=args.stamp))
    primary_md = resolve_output_path(repo_root, args.primary_markdown_output.format(stamp=args.stamp))
    task_path = resolve_output_path(repo_root, args.task_output.format(stamp=args.stamp))
    exchange_path = resolve_output_path(repo_root, args.exchange_output.format(stamp=args.stamp))
    exchange_md = resolve_output_path(repo_root, args.exchange_markdown_output.format(stamp=args.stamp))
    write_json_report(built["primary"], primary_path)
    write_text_report(render_primary(built["primary"]), primary_md)
    write_json_report(built["task_packet"], task_path)
    print(write_json_report(built["exchange"], exchange_path), end="")
    write_text_report(render_exchange(built["exchange"]), exchange_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
