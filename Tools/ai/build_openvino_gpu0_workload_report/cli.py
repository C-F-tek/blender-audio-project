#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from tools.ai.provider_tool_loop import openvino_tool_loop_report
from tools.ai.runtime_hardware_capability.workloads import run_openvino_gpu0_tensor_test


def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# OpenVINO GPU.0 observable support workload",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Provider execution performed: `{report.get('provider_execution_performed')}`",
        f"- Production support: `{report.get('production_support')}`",
        f"- Iterations: `{report.get('iterations')}`",
        f"- Minimum seconds: `{report.get('min_seconds')}`",
        f"- Requested role: `{report.get('requested_role')}`",
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
        decision = "diagnostic_peer_available"
        summary = (
            f"GPU0 peer ha eseguito il tool OpenVINO su {device}: "
            f"iterations={iterations}, inference_seconds={infer_s:.6f}, output_preview={preview}. "
            "Ruolo: lane diagnostica pronta a supportare analisi runtime/acceleratore, senza diventare planner primario."
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
    parser.add_argument("--production-support", action="store_true", default=True)
    parser.add_argument("--allow-non-observable", action="store_true")
    parser.add_argument("--tool-loop-timeout-seconds", type=float, default=30.0)
    parser.add_argument("--tool-loop-max-new-tokens", type=int, default=128)
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
    report["request_input"] = str(args.request or "").strip()
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
        prompt=report["request_input"]
        or "Call the broker tool needed to validate a heap code product.",
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
    if (
        report["native_tool_loop_requested"]
        and report["native_tool_call_count"] <= 0
        and tool_loop.get("classification") != "openvino_native_tool_call_incomplete"
    ):
        report.setdefault("errors", []).append(
            str(tool_loop.get("classification") or "openvino_native_tool_call_missing")
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
