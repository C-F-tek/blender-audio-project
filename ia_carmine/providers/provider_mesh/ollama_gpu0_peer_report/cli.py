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

from ia_carmine._shared.provider_ollama_probe import run_ollama_probe
from ia_carmine.providers.ollama.role_models import (
    start_gpu0_vulkan_server,
    stop_gpu0_vulkan_server,
)

DEFAULT_GPU0_OLLAMA_BASE_URL = "http://127.0.0.1:11435"


def read_text(repo_root: Path, value: str) -> str:
    if not value:
        return ""
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.read_text(encoding="utf-8-sig", errors="replace")


def request_text(repo_root: Path, args: argparse.Namespace) -> str:
    if args.request_file:
        return read_text(repo_root, args.request_file)
    if args.task_file:
        return read_text(repo_root, args.task_file)
    return str(args.request or "")


def render_peer_prompt(request: str, leader_packet: dict[str, Any]) -> str:
    leader = json.dumps(leader_packet, ensure_ascii=False)[:1800] if leader_packet else "{}"
    return (
        "IA-Carmine GPU0 peer reviewer/refiner lane. You are not OpenVINO. "
        "You run through Ollama on the GPU0/Vulkan lane and must produce useful "
        "review/refinement evidence for GPU1. Use ollama-python native tool calls "
        "only when broker evidence is explicitly needed.\n\n"
        f"OPERATOR_REQUEST:\n{request[:3500]}\n\n"
        f"GPU1_LEADER_PACKET:\n{leader}\n\n"
        "Return peer-review evidence with concrete risks, target refs if known, "
        "and whether GPU1 should continue, backtrack, or ask broker tools."
    )


def load_leader_packet(repo_root: Path, value: str) -> dict[str, Any]:
    if not value:
        return {}
    try:
        return json.loads(read_text(repo_root, value))
    except Exception:
        return {}


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
        f"- Ollama base URL: `{report.get('ollama_base_url')}`",
        f"- Vulkan visible device: `{selection.get('resolved')}`",
        f"- Vulkan target: `{target.get('deviceName')}`",
        f"- Runtime Intel inference: `{runtime_log.get('runner_inference_intel')}`",
        f"- Unload verified: `{report.get('ollama_unload_verified')}`",
        f"- Native tool calls: `{report.get('native_tool_call_count')}`",
        f"- Rejection reason: `{report.get('provider_rejection_reason')}`",
        "",
        "## Response",
        "",
        str(report.get("response_text") or ""),
    ]
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/ollama_gpu0_peer.json")
    parser.add_argument("--markdown-output", default="output/validation/ollama_gpu0_peer.md")
    parser.add_argument("--base-url", default=DEFAULT_GPU0_OLLAMA_BASE_URL)
    parser.add_argument("--no-start-gpu0-vulkan-server", action="store_true")
    parser.add_argument("--gpu0-vulkan-visible-devices", default="auto")
    parser.add_argument("--restart-gpu0-vulkan-server", action="store_true")
    parser.add_argument("--keep-gpu0-vulkan-server", action="store_true")
    parser.add_argument("--model", default="auto")
    parser.add_argument("--request", default="")
    parser.add_argument("--request-file", default="")
    parser.add_argument("--task-file", default="")
    parser.add_argument("--leader-packet", default="")
    parser.add_argument("--max-new-tokens", type=int, default=384)
    parser.add_argument("--ollama-num-ctx", type=int, default=8192)
    parser.add_argument("--ollama-gpu-layers", default="all")
    parser.add_argument("--ollama-num-thread", type=int, default=None)
    parser.add_argument("--ollama-context-candidates", default="8192,4096")
    parser.add_argument("--keep-alive", default="120s")
    parser.add_argument("--strict-provider-model", action="store_true")
    parser.add_argument("--operator-gpu-observation", default="")
    parser.add_argument("--require-ollama-gpu-residency", action="store_true", default=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    request = request_text(repo_root, args)
    leader_packet = load_leader_packet(repo_root, args.leader_packet)
    prompt = render_peer_prompt(request, leader_packet)
    gpu0_server = {"started": False, "ready": False, "reason": "disabled"}
    if not args.no_start_gpu0_vulkan_server:
        gpu0_server = start_gpu0_vulkan_server(
            base_url=args.base_url,
            repo_root=repo_root,
            visible_devices=args.gpu0_vulkan_visible_devices,
            restart_if_ready=args.restart_gpu0_vulkan_server,
        )
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
        gpu0_vulkan_policy_verified=_gpu0_vulkan_policy_verified(gpu0_server),
    )
    runtime_log = _runtime_log_evidence(gpu0_server)
    workload_verified = _gpu0_workload_verified(report, runtime_log)
    report.update(
        {
            "schema_version": 1,
            "kind": "ollama_gpu0_peer_report",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "repo_root": str(repo_root),
            "ollama_base_url": args.base_url,
            "gpu0_vulkan_server": gpu0_server,
            "gpu0_vulkan_runtime_log": runtime_log,
            "ollama_gpu0_vulkan_required": True,
            "gpu0_windows_lane": "Windows GPU0 / Intel(R) Graphics",
            "gpu0_vulkan_workload_verified": workload_verified,
            "openvino_gpu0_used": False,
        }
    )
    if not gpu0_server.get("ready"):
        report.setdefault("errors", []).append("gpu0_vulkan_server_not_ready")
        report["passed"] = False
    if not workload_verified:
        report.setdefault("errors", []).append("gpu0_ollama_vulkan_no_verified_workload")
        report["passed"] = False
        report["provider_work_verified"] = False
        report["provider_rejection_reason"] = "gpu0_ollama_vulkan_no_verified_workload"
        report["product_blocked_reason"] = "gpu0_ollama_vulkan_no_verified_workload"
    if gpu0_server.get("started") and not args.keep_gpu0_vulkan_server:
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


def _gpu0_workload_verified(report: dict[str, Any], runtime_log: dict[str, Any]) -> bool:
    return bool(
        report.get("gpu0_vulkan_policy_verified")
        and report.get("ollama_unload_verified")
        and int(report.get("eval_count") or 0) > 0
        and runtime_log.get("runner_inference_intel")
    )


if __name__ == "__main__":
    raise SystemExit(main())
