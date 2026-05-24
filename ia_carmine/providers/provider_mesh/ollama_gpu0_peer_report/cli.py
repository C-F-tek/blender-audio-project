#!/usr/bin/env python3
"""Build GPU0 peer evidence through Ollama/Vulkan via ollama-python."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT_FOR_IMPORT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT_FOR_IMPORT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORT))

from ia_carmine._shared.file_backed_transport import (
    report_text,
    write_large_text_evidence,
    write_text_evidence_fields,
)
from ia_carmine._shared.provider_ollama_probe import run_ollama_probe
from ia_carmine.providers.ollama.role_models import (
    start_gpu0_vulkan_server,
    stop_gpu0_vulkan_server,
)
from ia_carmine.runtime.heap_gate.gpu0_secondary_decision import (
    bind_gpu0_secondary_to_gpu1_packet,
    gpu0_secondary_decision_text,
    parse_gpu0_secondary_response,
)
from ia_carmine.runtime.heap_gate.gpu1_closure_packet import (
    extract_gpu1_closure_decision_packet,
    gpu1_decision_packet_valid,
)

DEFAULT_GPU0_OLLAMA_BASE_URL = "http://127.0.0.1:11435"


def config_sources_from_argv(argv: list[str]) -> dict[str, str]:
    def source(*options: str) -> str:
        for token in argv:
            for option in options:
                if token == option or token.startswith(f"{option}="):
                    return "cli_arg"
        return "standalone_default"

    return {
        "base_url": source("--base-url"),
        "gpu0_vulkan_visible_devices": source("--gpu0-vulkan-visible-devices"),
        "model": source("--model"),
        "max_new_tokens": source("--max-new-tokens"),
        "ollama_num_ctx": source("--ollama-num-ctx"),
        "ollama_gpu_layers": source("--ollama-gpu-layers", "--ollama-num-gpu"),
        "ollama_context_candidates": source("--ollama-context-candidates"),
        "keep_alive": source("--keep-alive"),
        "require_ollama_gpu_residency": source("--require-ollama-gpu-residency"),
    }


def read_text(repo_root: Path, value: str) -> str:
    if not value:
        return ""
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.read_text(encoding="utf-8-sig", errors="replace")


def request_text(repo_root: Path, args: argparse.Namespace) -> str:
    parts: list[str] = []
    if args.request_file:
        parts.append("OPERATOR_REQUEST:\n" + read_text(repo_root, args.request_file))
    elif args.task_file:
        parts.append("TASK_FILE_CONTEXT:\n" + read_text(repo_root, args.task_file))
    elif args.request:
        parts.append("INLINE_REQUEST:\n" + str(args.request or ""))
    startup_text = startup_manifest_context(repo_root, args.startup_manifest)
    if startup_text:
        parts.append(startup_text)
    return "\n\n".join(parts).strip()


def startup_manifest_context(repo_root: Path, value: str) -> str:
    if not value:
        return ""
    try:
        payload = json.loads(read_text(repo_root, value))
    except Exception as exc:  # noqa: BLE001 - report-only context fallback.
        return f"STARTUP_MANIFEST_READ_ERROR: {type(exc).__name__}: {exc}"
    artifacts = payload.get("artifacts") if isinstance(payload.get("artifacts"), dict) else {}
    heap_task_file = str(payload.get("heap_task_file") or artifacts.get("heap_task_file") or "")
    compact = {
        "source": "startup_manifest",
        "request_sha256": payload.get("request_sha256"),
        "input_ready_before_heap": payload.get("input_ready_before_heap"),
        "startup_reload_degraded": payload.get("startup_reload_degraded"),
        "context_file_count": payload.get("context_file_count"),
        "artifact_keys": sorted(str(key) for key in artifacts)[:40],
        "heap_task_file": heap_task_file,
    }
    sections = ["STARTUP_MANIFEST_CONTEXT:\n" + json.dumps(compact, ensure_ascii=False, indent=2)]
    if heap_task_file:
        try:
            sections.append("HEAP_TASK_FILE_CONTEXT:\n" + read_text(repo_root, heap_task_file)[:5000])
        except Exception as exc:  # noqa: BLE001 - preserve compact failure evidence.
            sections.append(f"HEAP_TASK_FILE_READ_ERROR: {type(exc).__name__}: {exc}")
    return "\n\n".join(sections)


def render_peer_prompt(_request: str, leader_packet: dict[str, Any]) -> str:
    packet = extract_gpu1_closure_decision_packet(leader_packet)
    packet_json = json.dumps(packet, ensure_ascii=False, indent=2)[:2200] if packet else "{}"
    expected_block = str(packet.get("gpu1_block_id") or "")
    expected_revision = str(packet.get("gpu1_revision") or "")
    return (
        "IA-Carmine GPU0 secondary congruence/veto lane. GPU1 is the only "
        "closure owner and product author. You may evaluate only the post-gate "
        "GPU1_CLOSURE_DECISION_PACKET below. Do not use operator request text, "
        "historical context, target-file guesses, strategy, patches, generic_write, "
        "or NPU output as a decision source. Do not perform broad exploration, "
        "final synthesis, product closure, or a complete alternate plan. "
        "Return exactly one JSON object and "
        "nothing else.\n\n"
        "BROKER_NATIVE_TOOL_RULE: GPU0 may use the broker/native schema only for "
        "peer_refinement, veto, evidence_request, or generic_write peer evidence; "
        "generic_write can never close the product and always requires a later "
        "GPU1 pointer block to consume it.\n\n"
        "Required JSON keys: gpu0_decision, checked_block_id, checked_gpu1_revision, "
        "reviewed_gpu1_block_id, reviewed_revision, packet_fingerprint, "
        "review_target_pointer, missing_required_sections, incongruence_reasons, "
        "veto_reasons, required_gpu1_next_action.\n"
        "gpu0_decision must be exactly one of: congruent, veto, refine_required, "
        "incongruent.\n"
        f"checked_block_id must equal: {expected_block}\n"
        f"checked_gpu1_revision must equal: {expected_revision}\n"
        "Reasons must be anchored in packet.reject_reasons, packet.evidence_refs, "
        "or packet.target_files. Unanchored historical reasons such as "
        "product_readiness are not valid veto reasons.\n\n"
        f"GPU1_CLOSURE_DECISION_PACKET:\n{packet_json}\n\n"
        "Return only the JSON object."
    )


def load_leader_packet(repo_root: Path, value: str) -> dict[str, Any]:
    if not value:
        return {}
    try:
        return json.loads(read_text(repo_root, value))
    except Exception:
        return {}


def load_server_evidence(repo_root: Path, value: str, base_url: str = "") -> dict[str, Any]:
    if not value:
        return {}
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig", errors="replace"))
    except Exception:
        return {}
    return _server_evidence_from_payload(payload, str(path), base_url=base_url)


def resolve_server_evidence(repo_root: Path, value: str, base_url: str) -> dict[str, Any]:
    explicit = load_server_evidence(repo_root, value, base_url=base_url)
    if explicit:
        explicit["gpu0_server_evidence_source"] = "explicit_server_evidence"
        return explicit
    if not value:
        return {}
    evidence_path = Path(value)
    if not evidence_path.is_absolute():
        evidence_path = repo_root / evidence_path
    search_dir = evidence_path.parent
    if not search_dir.is_dir():
        return {}
    candidates = sorted(
        list(search_dir.glob("provider_role_coexistence*.json"))
        + list(search_dir.glob("gpu0_ollama_vulkan_peer*.json")),
        key=lambda item: item.stat().st_mtime if item.exists() else 0,
        reverse=True,
    )
    for candidate in candidates:
        if candidate == evidence_path:
            continue
        try:
            payload = json.loads(candidate.read_text(encoding="utf-8-sig", errors="replace"))
        except Exception:
            continue
        server = _server_evidence_from_payload(payload, str(candidate), base_url=base_url)
        if not server:
            continue
        source = (
            "inherited_verified_gpu0_peer"
            if str(payload.get("kind") or "") == "ollama_gpu0_peer_report"
            else "inherited_coexistence"
        )
        server["gpu0_server_evidence_source"] = source
        return server
    return {}


def _server_evidence_from_payload(payload: Any, source: str, *, base_url: str = "") -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    server: Any = payload.get("gpu0_vulkan_server")
    if not isinstance(server, dict):
        preflight = payload.get("provider_role_coexistence_preflight")
        preflight = preflight if isinstance(preflight, dict) else {}
        server = preflight.get("gpu0_vulkan_server")
    if not isinstance(server, dict):
        boot_gate = payload.get("provider_boot_gate")
        boot_gate = boot_gate if isinstance(boot_gate, dict) else {}
        server = boot_gate.get("gpu0_vulkan_server")
    if isinstance(server, dict):
        if base_url and server.get("base_url") and str(server.get("base_url")) != base_url:
            return {}
        if (
            str(payload.get("kind") or "") == "ollama_gpu0_peer_report"
            and payload.get("provider_work_verified") is not True
        ):
            return {}
        return {
            **server,
            "handoff_provider_loop": payload.get("handoff_provider_loop"),
            "server_evidence_source": source,
        }
    return {}


def merge_server_evidence(current: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    if not evidence:
        return current
    merged = dict(current)
    for key in ("env", "stderr_log", "stdout_log", "pid", "vulkan_device_selection"):
        if not merged.get(key) and evidence.get(key):
            merged[key] = evidence[key]
    for key in ("handoff_provider_loop", "server_evidence_source", "gpu0_server_evidence_source"):
        if evidence.get(key) is not None:
            merged[key] = evidence[key]
    if evidence.get("ready") is True and not merged.get("ready"):
        merged["ready"] = True
        merged["handoff_server_reused"] = True
        merged["inherited_ready_evidence"] = True
    return merged


def render_markdown(report: dict[str, Any]) -> str:
    server = report.get("gpu0_vulkan_server") if isinstance(report.get("gpu0_vulkan_server"), dict) else {}
    selection = server.get("vulkan_device_selection") if isinstance(server.get("vulkan_device_selection"), dict) else {}
    target = selection.get("target_device") if isinstance(selection.get("target_device"), dict) else {}
    runtime_log = report.get("gpu0_vulkan_runtime_log") if isinstance(report.get("gpu0_vulkan_runtime_log"), dict) else {}
    lines = [
        "# Ollama GPU0 Vulkan Peer Report",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Provider work verified: `{report.get('provider_work_verified')}`",
        f"- Provider backend: `{report.get('provider_backend')}`",
        f"- Provider compute device: `{report.get('provider_compute_device')}`",
        f"- Windows Task Manager device: `{report.get('windows_task_manager_device_hint')}`",
        f"- Device identity verified: `{report.get('device_identity_verified')}`",
        f"- Ollama base URL: `{report.get('ollama_base_url')}`",
        f"- Vulkan visible device: `{selection.get('resolved')}`",
        f"- Vulkan target: `{target.get('deviceName')}`",
        f"- Vulkan vendor: `{target.get('vendorID')}`",
        f"- Runtime Intel inference: `{runtime_log.get('runner_inference_intel')}`",
        f"- Unload verified: `{report.get('ollama_unload_verified')}`",
        f"- Unload deferred until production cleanup: `{report.get('provider_residency_deferred_until_production_cleanup')}`",
        f"- Native tool calls: `{report.get('native_tool_call_count')}`",
        f"- GPU0 secondary schema valid: `{report.get('gpu0_secondary_schema_valid')}`",
        f"- GPU0 decision: `{report.get('gpu0_decision')}`",
        f"- GPU0 model decision: `{report.get('gpu0_model_decision')}`",
        f"- GPU0 effective decision: `{report.get('gpu0_effective_decision')}`",
        f"- GPU0 checked current packet: `{report.get('gpu0_checked_current_packet')}`",
        f"- GPU1 packet valid: `{report.get('gpu1_closure_decision_packet_valid')}`",
        f"- GPU0 prompt scope: `{report.get('gpu0_prompt_scope')}`",
        f"- GPU0 server evidence source: `{report.get('gpu0_server_evidence_source')}`",
        f"- Rejection reason: `{report.get('provider_rejection_reason')}`",
        "",
        "## Structured Decision",
        "",
        str(report.get("response_text_tail") or ""),
    ]
    if report.get("free_text_evidence_tail"):
        lines.extend(["", "## Free Text Evidence", "", str(report.get("free_text_evidence_tail") or "")])
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report.get("errors", []))
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in report.get("warnings", []))
    return "\n".join(lines) + "\n"


def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def _leader_block_id(leader_packet: dict[str, Any]) -> str:
    packet = extract_gpu1_closure_decision_packet(leader_packet)
    value = str(packet.get("gpu1_block_id") or "").strip()
    if value:
        return value
    for key in ("block_id", "proposal_block_id", "current_block_id", "resume_from_block_id"):
        value = str(leader_packet.get(key) or "").strip()
        if value:
            return value
    return ""


def _leader_revision(leader_packet: dict[str, Any]) -> str:
    packet = extract_gpu1_closure_decision_packet(leader_packet)
    value = str(packet.get("gpu1_revision") or "").strip()
    if value:
        return value
    for key in ("revision", "provider_cycle_id", "review_for_gpu1_cycle"):
        value = leader_packet.get(key)
        if value is not None and str(value).strip():
            return str(value)
    return ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/ollama_gpu0_peer.json")
    parser.add_argument("--markdown-output", default="output/validation/ollama_gpu0_peer.md")
    parser.add_argument("--base-url", default=DEFAULT_GPU0_OLLAMA_BASE_URL)
    parser.add_argument("--server-evidence", default="")
    parser.add_argument("--no-start-gpu0-vulkan-server", action="store_true")
    parser.add_argument("--gpu0-vulkan-visible-devices", default="auto")
    parser.add_argument("--restart-gpu0-vulkan-server", action="store_true")
    parser.add_argument("--keep-gpu0-vulkan-server", action="store_true")
    parser.add_argument("--model", default="auto")
    parser.add_argument("--request", default="")
    parser.add_argument("--request-file", default="")
    parser.add_argument("--task-file", default="")
    parser.add_argument("--startup-manifest", default="")
    parser.add_argument("--leader-packet", default="")
    parser.add_argument("--max-new-tokens", type=int, default=384)
    parser.add_argument("--ollama-num-ctx", type=int, default=8192)
    parser.add_argument("--ollama-gpu-layers", default="all")
    parser.add_argument("--ollama-num-thread", type=int, default=None)
    parser.add_argument("--ollama-context-candidates", default="8192,4096")
    parser.add_argument("--keep-alive", default="120s")
    parser.add_argument("--defer-unload", action="store_true")
    parser.add_argument("--strict-provider-model", action="store_true")
    parser.add_argument("--operator-gpu-observation", default="")
    parser.add_argument("--require-ollama-gpu-residency", action="store_true", default=True)
    parser.add_argument("--canonical-run-provider-evidence", action="store_true")
    parser.add_argument("--canonical-run-fingerprint", default="")
    raw_argv = sys.argv[1:]
    args = parser.parse_args(raw_argv)
    config_sources = config_sources_from_argv(raw_argv)

    repo_root = Path(args.repo_root).resolve()
    request = ""
    leader_packet = load_leader_packet(repo_root, args.leader_packet)
    gpu1_packet = extract_gpu1_closure_decision_packet(leader_packet)
    prompt = render_peer_prompt(request, leader_packet)
    prompt_evidence = write_large_text_evidence(
        repo_root,
        resolve_path(repo_root, args.output).parent / "provider_prompt_artifacts",
        name="ollama_gpu0_peer_prompt",
        text=prompt,
        kind="provider_request_prompt",
        producer="ollama_gpu0_peer_report",
        suffix=".md",
    )
    server_evidence = resolve_server_evidence(repo_root, args.server_evidence, args.base_url)
    gpu0_server = {"started": False, "ready": False, "reason": "disabled"}
    if not args.no_start_gpu0_vulkan_server:
        gpu0_server = start_gpu0_vulkan_server(
            base_url=args.base_url,
            repo_root=repo_root,
            visible_devices=args.gpu0_vulkan_visible_devices,
            restart_if_ready=args.restart_gpu0_vulkan_server,
        )
    gpu0_server = merge_server_evidence(gpu0_server, server_evidence)
    report = run_ollama_probe(
        repo_root,
        args.model,
        prompt,
        max_new_tokens=args.max_new_tokens,
        num_ctx=args.ollama_num_ctx,
        gpu_layers=args.ollama_gpu_layers,
        num_thread=args.ollama_num_thread,
        keep_alive=args.keep_alive,
        require_gpu_residency=args.require_ollama_gpu_residency,
        context_candidates=args.ollama_context_candidates,
        strict_provider_model=args.strict_provider_model,
        operator_gpu_observation=args.operator_gpu_observation,
        lane="gpu0_peer",
        role="gpu0_peer_reviewer_refiner",
        base_url=args.base_url,
        prompt_ref=prompt_evidence.get("ref") or {},
        gpu0_vulkan_policy_verified=_gpu0_vulkan_policy_verified(gpu0_server),
        unload_model=not args.defer_unload,
    )
    output_parent = resolve_path(repo_root, args.output).parent
    raw_response_text = str(report_text(repo_root, report).get("text") or "")
    gpu0_secondary = parse_gpu0_secondary_response(
        raw_response_text,
        fallback_block_id=_leader_block_id(leader_packet),
        fallback_revision=_leader_revision(leader_packet),
        fallback_packet_fingerprint=str(gpu1_packet.get("packet_fingerprint") or ""),
    )
    gpu0_secondary = bind_gpu0_secondary_to_gpu1_packet(gpu0_secondary, leader_packet)
    report.update(write_text_evidence_fields(
        repo_root,
        output_parent / "provider_response_artifacts",
        prefix="gpu0_raw_response_text",
        name="gpu0_raw_response_text",
        text=raw_response_text,
        kind="gpu0_raw_response_text",
        producer="ollama_gpu0_peer_report",
        suffix=".md",
    ))
    report["gpu1_closure_decision_packet"] = gpu1_packet
    report["gpu1_closure_decision_packet_present"] = bool(gpu1_packet)
    report["gpu1_closure_decision_packet_valid"] = gpu1_decision_packet_valid(gpu1_packet)
    report["gpu0_prompt_scope"] = "post_gate_gpu1_closure_decision_packet_only"
    report["sidecar_scope_mode"] = "packet_review_only"
    report["sidecar_scope_contract"] = (
        "review_current_gpu1_packet_only_no_broad_exploration_no_final_synthesis"
    )
    report["gpu0_one_execution_per_packet"] = True
    report.update(gpu0_secondary)
    free_text_evidence = str(report.pop("free_text_evidence", "") or "")
    report.update(write_text_evidence_fields(
        repo_root,
        output_parent / "provider_response_artifacts",
        prefix="free_text_evidence",
        name="gpu0_free_text_evidence",
        text=free_text_evidence,
        kind="gpu0_free_text_evidence",
        producer="ollama_gpu0_peer_report",
        suffix=".md",
    ))
    report.update(write_text_evidence_fields(
        repo_root,
        output_parent / "provider_response_artifacts",
        prefix="response_text",
        name="gpu0_secondary_decision_text",
        text=gpu0_secondary_decision_text(gpu0_secondary),
        kind="gpu0_secondary_decision_text",
        producer="ollama_gpu0_peer_report",
        suffix=".md",
    ))
    runtime_log = _runtime_log_evidence(gpu0_server)
    device_identity = _gpu0_device_identity(gpu0_server)
    workload_verified = _gpu0_workload_verified(report, runtime_log, gpu0_server, device_identity)
    schema_valid = gpu0_secondary.get("gpu0_secondary_schema_valid") is True
    if workload_verified:
        report.update(
            {
                "provider_device_verified": True,
                "provider_compute_device": "ollama/gpu0-vulkan",
                "ollama_residency_verified": True,
                "ollama_compute_verified": True,
                "ollama_gpu_accelerated_verified": True,
                "full_gpu_residency_verified": True,
                "ollama_gpu_residency_status": "verified_by_gpu0_vulkan_handoff",
            }
        )
        report["replight_passed"] = True
        report["replight_blocked_reason"] = ""
        report["role_rejection_reason"] = ""
        report["errors"] = [
            error
            for error in report.get("errors", [])
            if error
            not in {
                "gpu0_ollama_vulkan_no_verified_workload",
                "gpu0_ollama_vulkan_unavailable",
                "gpu0_vulkan_server_not_ready",
                *({"gpu0_secondary_schema_invalid"} if schema_valid else set()),
            }
        ]
    report.update(
        {
            "schema_version": 1,
            "kind": "ollama_gpu0_peer_report",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "repo_root": str(repo_root),
            "config_sources": config_sources,
            "standalone_default_fields": [
                key for key, source in config_sources.items() if source == "standalone_default"
            ],
            "canonical_run_provider_evidence": bool(args.canonical_run_provider_evidence),
            "canonical_run_fingerprint": str(args.canonical_run_fingerprint or ""),
            "ollama_base_url": args.base_url,
            "gpu0_vulkan_server": gpu0_server,
            "gpu0_server_evidence_source": gpu0_server.get("gpu0_server_evidence_source")
            or gpu0_server.get("server_evidence_source")
            or "none",
            "gpu0_vulkan_runtime_log": runtime_log,
            **device_identity,
            "ollama_gpu0_vulkan_required": True,
            "gpu0_windows_lane": "Windows GPU0 / Intel(R) Graphics",
            "gpu0_vulkan_workload_verified": workload_verified,
            "provider_residency_deferred_until_production_cleanup": bool(args.defer_unload),
            "gpu0_vulkan_server_deferred_until_provider_cleanup": bool(args.defer_unload),
            "openvino_gpu0_used": False,
        }
    )
    if not gpu0_server.get("ready"):
        report.setdefault("errors", []).append("gpu0_vulkan_server_not_ready")
        report["passed"] = False
    if not device_identity.get("device_identity_verified"):
        report.setdefault("errors", []).append("gpu0_device_identity_unverified")
        report["passed"] = False
        report["provider_work_verified"] = False
        report["provider_rejection_reason"] = "gpu0_device_identity_unverified"
        report["product_blocked_reason"] = "gpu0_device_identity_unverified"
    if not workload_verified:
        report.setdefault("errors", []).append("gpu0_ollama_vulkan_no_verified_workload")
        report["passed"] = False
        report["provider_work_verified"] = False
        report["provider_rejection_reason"] = "gpu0_ollama_vulkan_no_verified_workload"
        report["product_blocked_reason"] = "gpu0_ollama_vulkan_no_verified_workload"
    elif not schema_valid:
        report.setdefault("errors", []).append("gpu0_secondary_schema_invalid")
        report["passed"] = False
        report["provider_work_verified"] = False
        report["provider_role_counted"] = False
        report["provider_rejection_reason"] = "gpu0_secondary_schema_invalid"
        report["product_blocked_reason"] = "gpu0_secondary_schema_invalid"
    else:
        gpu0_decision = str(
            report.get("gpu0_effective_decision") or report.get("gpu0_decision") or ""
        ).strip().lower()
        report["provider_work_verified"] = True
        report["provider_role_counted"] = True
        report["provider_rejection_reason"] = ""
        report["product_blocked_reason"] = ""
        report["sidecar_incongruent"] = gpu0_decision == "incongruent"
        report["sidecar_product_block_reason"] = (
            "gpu0_secondary_decision_incongruent"
            if report["sidecar_incongruent"]
            else ""
        )
        report["errors"] = [
            error
            for error in report.get("errors", [])
            if error != "gpu0_secondary_schema_invalid"
        ]
        report["passed"] = not bool(report.get("errors"))
    if gpu0_server.get("started") and not args.keep_gpu0_vulkan_server and not args.defer_unload:
        report["gpu0_vulkan_server_stop"] = stop_gpu0_vulkan_server(args.base_url)
    output = resolve_path(repo_root, args.output)
    markdown = resolve_path(repo_root, args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": report.get("passed"), "output": str(output), "markdown": str(markdown)}, indent=2))
    return 0 if report.get("passed") else 2


def _gpu0_vulkan_policy_verified(report: dict[str, Any]) -> bool:
    selection = report.get("vulkan_device_selection")
    selection = selection if isinstance(selection, dict) else {}
    target = selection.get("target_device") if isinstance(selection.get("target_device"), dict) else {}
    return bool(
        report.get("ready")
        and str(report.get("env", {}).get("OLLAMA_LLM_LIBRARY") or "").lower() == "vulkan"
        and str(report.get("env", {}).get("CUDA_VISIBLE_DEVICES") or "") == "-1"
        and (
            str(target.get("vendorID") or "").lower() == "0x8086"
            or "intel" in str(target.get("deviceName") or "").lower()
            or "integrated" in str(target.get("deviceType") or "").lower()
        )
    )


def _gpu0_device_identity(report: dict[str, Any]) -> dict[str, Any]:
    selection = report.get("vulkan_device_selection")
    selection = selection if isinstance(selection, dict) else {}
    target = selection.get("target_device") if isinstance(selection.get("target_device"), dict) else {}
    resolved = str(selection.get("resolved") or "").strip()
    vendor = str(target.get("vendorID") or "").strip().lower()
    name = str(target.get("deviceName") or "").strip()
    dtype = str(target.get("deviceType") or "").strip().lower()
    verified = bool(vendor == "0x8086" or "intel" in name.lower() or "integrated" in dtype)
    return {
        "logical_lane": "gpu0_peer",
        "provider_backend_device_id": f"vulkan:{resolved}" if resolved else "",
        "windows_task_manager_device_hint": "Windows GPU 0 / Intel(R) Graphics",
        "vulkan_visible_device": resolved,
        "vulkan_device_name": name,
        "vulkan_vendor_id": vendor,
        "device_identity_verified": verified,
    }


def _runtime_log_evidence(server_report: dict[str, Any]) -> dict[str, Any]:
    path = Path(str(server_report.get("stderr_log") or ""))
    if not path.is_file():
        return {"present": False, "intel_gpu_seen": False, "tail": ""}
    text = path.read_text(encoding="utf-8", errors="replace")[-12000:]
    return {
        "present": True,
        "intel_gpu_seen": "Intel(R) Graphics" in text
        or "8680677d-0600-0000-0002-000000000000" in text,
        "nvidia_gpu_seen": "NVIDIA GeForce RTX 5080" in text,
        "integrated_gpu_memory_seen": "Integrated GPU (Intel(R) Graphics)" in text,
        "runner_inference_intel": "ID:8680677d-0600-0000-0002-000000000000" in text
        or "8680677d-0600-0000-0002-000000000000 Library:Vulkan" in text,
        "tail": text[-3000:],
    }


def _gpu0_workload_verified(
    report: dict[str, Any],
    runtime_log: dict[str, Any],
    server_report: dict[str, Any],
    device_identity: dict[str, Any],
) -> bool:
    inherited_source = str(
        server_report.get("gpu0_server_evidence_source")
        or server_report.get("server_evidence_source")
        or ""
    )
    inherited_server = bool(
        server_report.get("ready")
        and device_identity.get("device_identity_verified")
        and inherited_source
        and inherited_source != "none"
    )
    return bool(
        report.get("gpu0_vulkan_policy_verified")
        and int(report.get("eval_count") or 0) > 0
        and (
            runtime_log.get("runner_inference_intel")
            or inherited_server
            or server_report.get("handoff_provider_loop")
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
