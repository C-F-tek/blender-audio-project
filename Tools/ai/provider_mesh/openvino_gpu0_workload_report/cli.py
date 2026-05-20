#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any
from Tools.ai._shared.provider_tool_loop import openvino_tool_loop_report
from Tools.ai.provider_mesh.hardware_capability.workloads import run_openvino_gpu0_tensor_test
def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()
def read_json_file(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - reported as provider evidence.
        return {"_read_error": f"{type(exc).__name__}: {exc}"}
def read_text_file(repo_root: Path, value: str) -> str:
    return resolve_path(repo_root, value).read_text(encoding="utf-8-sig", errors="replace")
def startup_context_preview(
    repo_root: Path, startup_manifest: str, task_file: str, max_chars: int
) -> tuple[str, str]:
    manifest_path = resolve_path(repo_root, startup_manifest) if startup_manifest else None
    if manifest_path and manifest_path.is_file():
        payload = read_json_file(manifest_path)
        artifacts = payload.get("artifacts") if isinstance(payload.get("artifacts"), dict) else {}
        compact = {
            "source": "startup_manifest",
            "startup_manifest": str(startup_manifest),
            "request_preview": str(payload.get("request_preview") or "")[:800],
            "request_sha256": payload.get("request_sha256"),
            "input_ready_before_heap": payload.get("input_ready_before_heap"),
            "startup_reload_degraded": payload.get("startup_reload_degraded"),
            "context_file_count": payload.get("context_file_count"),
            "artifact_keys": sorted(str(key) for key in artifacts)[:80],
            "task_file_mode": "artifact_reference_only_not_runtime_database",
        }
        return json.dumps(compact, ensure_ascii=False, indent=2)[:max_chars], "startup_manifest"
    file_path = resolve_path(repo_root, task_file) if task_file else None
    if file_path and file_path.is_file():
        return file_path.read_text(encoding="utf-8", errors="replace")[:max_chars], "task_file"
    return "", "none"
def render_leader_peer_prompt(
    request: str, leader_packet: dict[str, Any], direct_startup_context: str
) -> str:
    if not leader_packet:
        return "\n".join(
            part
            for part in (
                request,
                "DIRECT_STARTUP_CONTEXT_FROM_CONTEXT_RELOAD:",
                direct_startup_context[:1600],
            )
            if part.strip()
        )
    contract = leader_packet.get("same_heap_teamwork_contract")
    contract_text = "; ".join(str(item) for item in contract[:5]) if isinstance(contract, list) else ""
    propagation = leader_packet.get("propagation_contract")
    propagation_text = "; ".join(str(item) for item in propagation[:5]) if isinstance(propagation, list) else ""
    pointer = leader_packet.get("pointer_contract") if isinstance(leader_packet.get("pointer_contract"), dict) else {}
    time_counter = leader_packet.get("time_counter_contract") if isinstance(leader_packet.get("time_counter_contract"), dict) else {}
    universe = leader_packet.get("runtime_universe") if isinstance(leader_packet.get("runtime_universe"), dict) else {}
    universe_summary = universe.get("summary") if isinstance(universe.get("summary"), dict) else {}
    startup_plane = leader_packet.get("startup_context_plane")
    startup_artifacts = leader_packet.get("startup_artifacts")
    startup_keys = (
        ", ".join(sorted(str(key) for key in startup_artifacts.keys())[:10])
        if isinstance(startup_artifacts, dict)
        else ""
    )
    return "\n".join(
        part
        for part in (
            "GPU0 peer lane. Consume the GPU1 primary advisor leader packet.",
            f"OPERATOR_REQUEST: {request}",
            f"GPU1_LEADER_ROLE: {leader_packet.get('role')}",
            f"SAME_HEAP_TEAMWORK_CONTRACT: {contract_text}",
            f"HEAP_UNIVERSE_SUMMARY: {universe_summary}",
            f"STARTUP_CONTEXT_PLANE: {startup_plane}",
            f"DIRECT_STARTUP_CONTEXT_FROM_CONTEXT_RELOAD: {direct_startup_context[:1600]}",
            f"STARTUP_ARTIFACT_KEYS: {startup_keys}",
            f"POINTER_CONTRACT: {pointer}",
            f"TIME_COUNTER_CONTRACT: {time_counter}",
            f"PROPAGATION_CONTRACT: {propagation_text}",
            f"SOURCE_PATH_ALLOWLIST_CONTRACT: {str(leader_packet.get('source_allowlist_contract') or '')[:1200]}",
            f"GPU1_REVISION_FEEDBACK: {str(leader_packet.get('revision_feedback') or '')[:700]}",
        )
        if part.strip()
    )
def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# OpenVINO GPU.0 observable support workload",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Provider execution performed: `{report.get('provider_execution_performed')}`",
        f"- Device workload execution performed: `{report.get('device_workload_execution_performed')}`",
        f"- Semantic provider required: `{report.get('semantic_provider_required')}`",
        f"- Semantic provider execution performed: `{report.get('semantic_provider_execution_performed')}`",
        f"- Semantic provider model loaded: `{report.get('semantic_provider_model_loaded')}`",
        f"- Semantic provider classification: `{report.get('semantic_provider_classification')}`",
        f"- Production support: `{report.get('production_support')}`",
        f"- Iterations: `{report.get('iterations')}`",
        f"- Minimum seconds: `{report.get('min_seconds')}`",
        f"- Requested role: `{report.get('requested_role')}`",
        f"- Startup manifest: `{report.get('startup_manifest')}`",
        f"- Startup context source: `{report.get('startup_context_source')}`",
        f"- Startup context consumed: `{report.get('startup_context_consumed')}`",
        f"- Leader packet consumed: `{report.get('leader_packet_consumed')}`",
        f"- Leader packet: `{report.get('leader_packet')}`",
        f"- Leader packet heap universe contract: `{report.get('leader_packet_heap_universe_contract')}`",
        f"- Leader packet pointer contract: `{report.get('leader_packet_pointer_contract')}`",
        f"- Leader packet time counter: `{report.get('leader_packet_time_counter_contract')}`",
        f"- Leader packet startup artifacts: `{report.get('leader_packet_startup_artifacts_count')}`",
        f"- Leader packet broker tool evidence: `{report.get('leader_packet_broker_tool_evidence_count')}`",
        f"- GPU.0 visible: `{report.get('openvino_gpu0_visible')}`",
        f"- GPU.0 probe performed: `{report.get('openvino_gpu0_probe_performed')}`",
        f"- GPU.0 workload performed: `{report.get('openvino_gpu0_workload_performed')}`",
        f"- GPU.0 workload passed: `{report.get('openvino_gpu0_workload_passed')}`",
        f"- GPU.0 role: `{report.get('openvino_gpu0_role')}`",
        f"- GPU.0 support lane: `{report.get('openvino_gpu0_support_lane')}`",
        f"- OpenVINO native tool loop requested: `{report.get('native_tool_loop_requested')}`",
        f"- OpenVINO native tool loop supported: `{report.get('native_tool_loop_supported')}`",
        f"- OpenVINO native tool calls: `{report.get('native_tool_call_count')}`",
        f"- GPU.0 observable workload required: `{report.get('openvino_gpu0_observable_workload_required')}`",
        f"- GPU.0 observable workload passed: `{report.get('openvino_gpu0_observable_workload_passed')}`",
        f"- GPU.0 sustained requested: `{report.get('openvino_gpu0_sustained_workload_requested')}`",
        f"- GPU.0 sustained performed: `{report.get('openvino_gpu0_sustained_workload_performed')}`",
        f"- GPU.0 iterations requested: `{report.get('openvino_gpu0_sustained_iterations_requested')}`",
        f"- GPU.0 iterations performed: `{report.get('openvino_gpu0_sustained_iterations_performed')}`",
        f"- GPU.0 min seconds requested: `{report.get('openvino_gpu0_sustained_min_seconds_requested')}`",
        f"- GPU.1 reserved visible: `{report.get('openvino_gpu1_reserved_visible')}`",
        f"- GPU.1 workload performed: `{report.get('openvino_gpu1_workload_performed')}`",
        f"- Selected device: `{report.get('selected_device')}`",
        f"- Available devices: `{report.get('available_devices')}`",
        f"- Elapsed seconds: `{report.get('elapsed_seconds')}`",
        f"- Compile seconds: `{report.get('compile_seconds')}`",
        f"- Inference seconds: `{report.get('inference_seconds')}`",
        "",
        "## Output preview",
        "",
        str(report.get("output_preview") or ""),
        "",
        "## Errors",
    ]
    errors = report.get("errors") or []
    lines.extend([f"- {item}" for item in errors] or ["- none"])
    lines.extend(["", "## Warnings"])
    warnings = report.get("warnings") or []
    lines.extend([f"- {item}" for item in warnings] or ["- none"])
    lines.append("")
    return "\n".join(lines)
def classify_request(text: str) -> str:
    normalized = " ".join(str(text or "").strip().lower().split())
    if not normalized:
        return "none"
    greetings = {"ciao", "salve", "buongiorno", "buonasera", "hello", "hi", "hey"}
    if normalized in greetings:
        return "casual_greeting"
    if any(
        token in normalized
        for token in ("errore", "traceback", "bug", "crash", "fallisce", "non funziona")
    ):
        return "debug_request"
    if any(token in normalized for token in ("patch", "modifica", "codice", "script", "repo")):
        return "repo_work_request"
    return "general_request"
def build_gpu0_peer_response(report: dict[str, Any]) -> dict[str, Any]:
    request = str(report.get("request_input") or "").strip()
    classification = classify_request(request)
    workload_ok = bool(
        report.get("openvino_gpu0_observable_workload_passed")
        or report.get("openvino_gpu0_workload_passed")
    )
    device = str(report.get("selected_device") or "GPU.0")
    iterations = int(report.get("openvino_gpu0_sustained_iterations_performed") or 0)
    infer_s = float(report.get("inference_seconds") or 0.0)
    preview = str(report.get("output_preview") or "").strip()
    errors = report.get("errors") if isinstance(report.get("errors"), list) else []
    warnings = report.get("warnings") if isinstance(report.get("warnings"), list) else []
    if not workload_ok:
        decision = "blocked_peer_evidence"
        summary = f"GPU0 peer non può contribuire: workload non osservabile; errors={len(errors)} warnings={len(warnings)}."
    elif classification == "casual_greeting":
        decision = "observe_only_for_greeting"
        summary = (
            f"GPU0 peer ha eseguito il tool OpenVINO su {device}: "
            f"iterations={iterations}, inference_seconds={infer_s:.6f}, output_preview={preview}. "
            "Ruolo: confermare che per un saluto casuale non serve computazione grafica aggiuntiva."
        )
    elif classification in {"debug_request", "repo_work_request"}:
        decision = "peer_review_refinement_available"
        summary = (
            f"GPU0 peer ha eseguito il tool OpenVINO su {device}: "
            f"iterations={iterations}, inference_seconds={infer_s:.6f}, output_preview={preview}. "
            "Ruolo: peer reviewer/refiner pronto a supportare analisi runtime/acceleratore, senza diventare planner primario."
        )
    else:
        decision = "peer_observation_available"
        summary = (
            f"GPU0 peer ha eseguito il tool OpenVINO su {device}: "
            f"iterations={iterations}, inference_seconds={infer_s:.6f}, output_preview={preview}. "
            "Ruolo: contributo osservazionale disponibile per la sintesi GPU1."
        )

    return {
        "request_classification": classification,
        "role_decision": decision,
        "tool_used": "run_openvino_gpu0_tensor_test",
        "tool_result_summary": summary,
        "response_text": summary,
    }
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/openvino_gpu0_workload.json")
    parser.add_argument("--markdown-output", default="output/validation/openvino_gpu0_workload.md")
    parser.add_argument("--iterations", type=int, default=180)
    parser.add_argument("--min-seconds", type=float, default=6.0)
    parser.add_argument("--role", default="observable_secondary_accelerator")
    parser.add_argument(
        "--request",
        default="",
        help="Optional heap request observed by GPU.0 peer lane.",
    )
    parser.add_argument("--request-file", default="")
    parser.add_argument("--startup-manifest", default="")
    parser.add_argument("--task-file", default="")
    parser.add_argument("--max-context-chars", type=int, default=4000)
    parser.add_argument("--production-support", action="store_true", default=True)
    parser.add_argument("--allow-non-observable", action="store_true")
    parser.add_argument("--tool-loop-timeout-seconds", type=float, default=30.0)
    parser.add_argument("--tool-loop-max-new-tokens", type=int, default=128)
    parser.add_argument("--require-semantic-provider", action="store_true")
    parser.add_argument("--leader-packet", default="", help="GPU1 primary advisor leader packet.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = run_openvino_gpu0_tensor_test(
        iterations=args.iterations,
        min_seconds=args.min_seconds,
        role=args.role,
        production_support=args.production_support,
    )
    report["production_support"] = bool(args.production_support)
    report["iterations"] = int(args.iterations)
    report["min_seconds"] = float(args.min_seconds)
    report["requested_role"] = str(args.role)
    request_input = read_text_file(repo_root, args.request_file) if args.request_file else str(args.request or "").strip()
    report["request_input"] = request_input
    report["request_file"] = str(args.request_file or "")
    report["request_transport"] = "operator_request_file" if args.request_file else "inline_cli"
    startup_context, startup_context_source = startup_context_preview(
        repo_root, args.startup_manifest, args.task_file, args.max_context_chars
    )
    report["startup_manifest"] = str(args.startup_manifest or "")
    report["task_file"] = str(args.task_file or "")
    report["startup_context_source"] = startup_context_source
    report["startup_context_consumed"] = startup_context_source == "startup_manifest"
    report["startup_context_preview_chars"] = len(startup_context)
    leader_packet_path = resolve_path(repo_root, args.leader_packet) if args.leader_packet else None
    leader_packet = read_json_file(leader_packet_path) if leader_packet_path else {}
    report["leader_packet"] = str(args.leader_packet or "")
    report["leader_packet_required"] = bool(args.leader_packet)
    report["leader_packet_kind"] = str(leader_packet.get("kind") or "")
    report["leader_packet_role"] = str(leader_packet.get("role") or "")
    report["leader_packet_heap_universe_contract"] = bool(leader_packet.get("heap_universe_contract"))
    report["leader_packet_pointer_contract"] = bool(leader_packet.get("pointer_contract"))
    report["leader_packet_time_counter_contract"] = bool(leader_packet.get("time_counter_contract"))
    report["leader_packet_startup_artifacts_count"] = len(leader_packet.get("startup_artifacts") or {})
    report["leader_packet_broker_tool_evidence_count"] = len(
        leader_packet.get("broker_tool_evidence") or []
    )
    report["leader_packet_error"] = str(leader_packet.get("_read_error") or "")
    report["leader_packet_consumed"] = bool(
        leader_packet
        and not leader_packet.get("_read_error")
        and leader_packet.get("role") == "gpu1_primary_advisory_leader"
        and leader_packet.get("heap_universe_contract")
        and leader_packet.get("pointer_contract")
    )
    if leader_packet.get("_read_error"):
        report.setdefault("errors", []).append(f"leader packet unreadable: {leader_packet['_read_error']}")
        report["passed"] = False
    report["openvino_gpu0_observable_workload_required"] = not bool(args.allow_non_observable)
    report["openvino_gpu0_observable_workload_passed"] = bool(
        report.get("openvino_gpu0_workload_performed")
        and report.get("openvino_gpu0_sustained_workload_performed")
        and int(report.get("openvino_gpu0_sustained_iterations_performed") or 0)
        >= int(args.iterations)
        and float(report.get("inference_seconds") or 0.0) >= min(0.05, float(args.min_seconds))
    )
    if args.production_support:
        report["openvino_gpu0_role"] = str(args.role)
        report["openvino_gpu0_not_primary_advisory"] = False
    if (
        report["openvino_gpu0_observable_workload_required"]
        and not report["openvino_gpu0_observable_workload_passed"]
    ):
        report.setdefault("errors", []).append(
            "GPU.0 workload was not observable enough for real product peer evidence."
        )
        report["passed"] = False
    tool_loop = openvino_tool_loop_report(
        repo_root=repo_root,
        prompt=render_leader_peer_prompt(
            report["request_input"] or "Call the broker tool needed to validate a heap code product.",
            leader_packet,
            startup_context,
        ),
        timeout_seconds=args.tool_loop_timeout_seconds,
        max_new_tokens=args.tool_loop_max_new_tokens,
        device="GPU.0",
    )
    report["openvino_native_tool_loop"] = tool_loop
    report["native_tool_loop_provider"] = "openvino_genai"
    report["native_tool_loop_requested"] = bool(tool_loop.get("native_tool_loop_requested"))
    report["native_tool_loop_supported"] = bool(tool_loop.get("native_tool_loop_supported"))
    report["native_tool_loop_performed"] = bool(tool_loop.get("native_tool_loop_performed"))
    report["native_tool_call_count"] = int(tool_loop.get("native_tool_call_count") or 0)
    report["tool_calls"] = tool_loop.get("tool_calls") or []
    report["device_workload_execution_performed"] = bool(
        report.get("openvino_gpu0_workload_performed")
        or report.get("openvino_gpu0_probe_performed")
    )
    report["semantic_provider_required"] = bool(args.require_semantic_provider)
    report["semantic_provider_model_dir"] = str(tool_loop.get("model_dir") or "")
    report["semantic_provider_model_dir_source"] = str(tool_loop.get("model_dir_source") or "")
    report["semantic_provider_classification"] = str(tool_loop.get("classification") or "")
    report["semantic_provider_model_discovered"] = bool(
        report["semantic_provider_model_dir"]
        and report["semantic_provider_model_dir_source"] != "missing"
    )
    report["semantic_child_failed"] = bool(
        report["semantic_provider_model_discovered"]
        and not tool_loop.get("native_tool_loop_performed")
        and str(tool_loop.get("classification") or "").endswith("_error")
    )
    report["semantic_provider_model_loaded"] = bool(tool_loop.get("native_tool_loop_performed"))
    report["semantic_provider_execution_performed"] = bool(
        tool_loop.get("native_tool_loop_supported")
        and tool_loop.get("native_tool_loop_performed")
    )
    if (
        report["native_tool_loop_requested"]
        and report["native_tool_call_count"] <= 0
        and tool_loop.get("classification") != "openvino_native_tool_call_incomplete"
    ):
        report.setdefault("errors", []).append(
            str(tool_loop.get("classification") or "openvino_native_tool_call_missing")
        )
        report["passed"] = False
    if report["semantic_provider_required"] and not report["semantic_provider_execution_performed"]:
        if report["semantic_provider_model_discovered"]:
            report.setdefault("errors", []).append(
                "GPU.0 semantic provider model was discovered but the OpenVINO child "
                f"tool loop failed: {report['semantic_provider_classification']}."
            )
        else:
            report.setdefault("errors", []).append(
                "GPU.0 semantic provider model was not discovered/executed; configure a valid "
                "OpenVINO GenAI model dir via IA_CARMINE_GPU0_COMPANION_MODEL_DIR or "
                "IA_CARMINE_OPENVINO_TOOL_MODEL_DIR."
            )
        report["passed"] = False
    if report["leader_packet_required"] and not report["leader_packet_consumed"]:
        report.setdefault("errors", []).append(
            "GPU.0 peer did not consume a valid GPU1 primary advisor leader packet."
        )
        report["passed"] = False
    report.update(build_gpu0_peer_response(report))
    report["repo_root"] = str(repo_root)
    output = resolve_path(repo_root, args.output)
    markdown = resolve_path(repo_root, args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(
        json.dumps(
            {
                "passed": report.get("passed"),
                "output": str(output),
                "markdown": str(markdown),
            },
            indent=2,
        )
    )
    return 0 if report.get("passed") else 2
if __name__ == "__main__":
    raise SystemExit(main())
