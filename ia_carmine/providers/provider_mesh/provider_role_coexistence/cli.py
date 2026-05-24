from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from ia_carmine.providers.ollama.sdk_client import OllamaSdkClient
from ia_carmine.providers.ollama.role_models import (
    gpu_layers_label,
    gpu_layers_option,
    model_alive,
    start_gpu0_vulkan_server,
    stop_gpu0_vulkan_server,
)
from ia_carmine.providers.provider_mesh.runtime.python_runtime import command_env


def _config_sources(argv: list[str]) -> dict[str, str]:
    def source(*options: str) -> str:
        for token in argv:
            for option in options:
                if token == option or token.startswith(f"{option}="):
                    return "cli_arg"
        return "standalone_default"

    return {
        "gpu1_base_url": source("--gpu1-base-url"),
        "gpu0_base_url": source("--gpu0-base-url"),
        "gpu1_model": source("--gpu1-model"),
        "gpu0_model": source("--gpu0-model"),
        "gpu0_vulkan_visible_devices": source("--gpu0-vulkan-visible-devices"),
        "keep_alive": source("--keep-alive"),
        "num_ctx": source("--num-ctx"),
        "ollama_gpu_layers": source("--ollama-gpu-layers", "--ollama-num-gpu"),
        "max_new_tokens": source("--max-new-tokens"),
        "npu_hold_seconds": source("--npu-hold-seconds"),
        "npu_timeout_seconds": source("--npu-timeout-seconds"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--child-npu", action="store_true")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--python-exe", default="")
    parser.add_argument("--gpu1-base-url", default="http://127.0.0.1:11434")
    parser.add_argument("--gpu0-base-url", default="http://127.0.0.1:11435")
    parser.add_argument("--gpu1-model", default="qwen2.5-coder:14b")
    parser.add_argument("--gpu0-model", default="qwen3:1.7b")
    parser.add_argument("--gpu0-vulkan-visible-devices", default="auto")
    parser.add_argument("--keep-alive", default="120s")
    parser.add_argument("--num-ctx", type=int, default=2048)
    parser.add_argument("--ollama-gpu-layers", "--ollama-num-gpu", dest="ollama_gpu_layers", default="all")
    parser.add_argument("--max-new-tokens", type=int, default=8)
    parser.add_argument("--npu-model-dir", default="")
    parser.add_argument("--npu-hold-seconds", type=float, default=8.0)
    parser.add_argument("--npu-timeout-seconds", type=float, default=90.0)
    parser.add_argument("--handoff-provider-loop", action="store_true")
    parser.add_argument("--output", default="output/validation/provider_role_coexistence.json")
    parser.add_argument("--markdown-output", default="output/validation/provider_role_coexistence.md")
    raw_argv = sys.argv[1:]
    args = parser.parse_args(raw_argv)
    if args.child_npu:
        return _child_npu()
    args._config_sources = _config_sources(raw_argv)
    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root, args)
    output = _resolve(repo_root, args.output)
    markdown = _resolve(repo_root, args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    markdown.write_text(_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "output": str(output), "markdown": str(markdown)}, indent=2))
    return 0 if report["passed"] else 2


def build_report(repo_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    errors: list[str] = []
    gpu0_server = start_gpu0_vulkan_server(
        base_url=args.gpu0_base_url,
        repo_root=repo_root,
        visible_devices=args.gpu0_vulkan_visible_devices,
        restart_if_ready=True,
    )
    gpu1 = _load_ollama_role(
        OllamaSdkClient(args.gpu1_base_url),
        "gpu1_planner",
        args.gpu1_model,
        args.keep_alive,
        args.num_ctx,
        args.ollama_gpu_layers,
        args.max_new_tokens,
    )
    gpu0 = _load_ollama_role(
        OllamaSdkClient(args.gpu0_base_url),
        "gpu0_peer",
        args.gpu0_model,
        args.keep_alive,
        args.num_ctx,
        args.ollama_gpu_layers,
        args.max_new_tokens,
    )
    npu = _start_npu_child(repo_root, args)
    coexistence = {
        "gpu1_ps": OllamaSdkClient(args.gpu1_base_url).ps(),
        "gpu0_ps": OllamaSdkClient(args.gpu0_base_url).ps(),
        "npu_ready": npu.get("ready_payload", {}),
    }
    gpu1["alive_during_coexistence"] = model_alive(coexistence["gpu1_ps"], args.gpu1_model)
    gpu0["alive_during_coexistence"] = model_alive(coexistence["gpu0_ps"], args.gpu0_model)
    npu_alive = bool(npu.get("ready_payload", {}).get("model_loaded"))
    if not gpu1["alive_during_coexistence"]:
        errors.append("gpu1_not_alive_during_triple_coexistence")
    if not gpu0["alive_during_coexistence"]:
        errors.append("gpu0_not_alive_during_triple_coexistence")
    if not npu_alive:
        errors.append("npu_not_loaded_during_triple_coexistence")
    if args.handoff_provider_loop:
        unload = {
            "gpu1": _deferred_unload(args.gpu1_base_url, args.gpu1_model),
            "gpu0": _deferred_unload(args.gpu0_base_url, args.gpu0_model),
        }
    else:
        unload = {
            "gpu1": _unload_ollama_role(args.gpu1_base_url, args.gpu1_model),
            "gpu0": _unload_ollama_role(args.gpu0_base_url, args.gpu0_model),
        }
    npu_exit = _wait_npu_exit(npu.get("process"))
    gpu0_stop = (
        _deferred_gpu0_server_stop(args.gpu0_base_url)
        if args.handoff_provider_loop
        else (stop_gpu0_vulkan_server(args.gpu0_base_url) if gpu0_server.get("started") else {})
    )
    if not args.handoff_provider_loop and not unload["gpu1"]["unloaded"]:
        errors.append("gpu1_not_unloaded_after_probe")
    if not args.handoff_provider_loop and not unload["gpu0"]["unloaded"]:
        errors.append("gpu0_not_unloaded_after_probe")
    if not npu_exit.get("exited"):
        errors.append("npu_child_not_exited_after_probe")
    return {
        "schema_version": 1,
        "kind": "provider_role_coexistence",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "handoff_provider_loop": bool(args.handoff_provider_loop),
        "provider_inactivity_unload_seconds": 120,
        "config_sources": getattr(args, "_config_sources", {}),
        "standalone_default_fields": [
            key
            for key, source in getattr(args, "_config_sources", {}).items()
            if source == "standalone_default"
        ],
        "coexistence_verified": bool(gpu1["alive_during_coexistence"] and gpu0["alive_during_coexistence"] and npu_alive),
        "roles": {"gpu1_planner": gpu1, "gpu0_peer": gpu0, "npu_micro_task_auditor": npu.get("ready_payload", {})},
        "coexistence_snapshot": coexistence,
        "unload": unload,
        "npu_exit": npu_exit,
        "gpu0_vulkan_server": gpu0_server,
        "gpu0_vulkan_server_stop": gpu0_stop,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def _load_ollama_role(
    client: OllamaSdkClient,
    role: str,
    model: str,
    keep_alive: str,
    num_ctx: int,
    gpu_layers: str | int | None,
    tokens: int,
) -> dict[str, Any]:
    gpu_layers_requested = gpu_layers_label(gpu_layers)
    num_gpu = gpu_layers_option(gpu_layers)
    text = client.generate(
        model=model,
        prompt=f"IA-Carmine {role} coexistence probe: reply READY.",
        keep_alive=keep_alive,
        temperature=0.0,
        num_predict=max(4, int(tokens)),
        num_thread=None,
        num_ctx=num_ctx,
        num_gpu=num_gpu,
        think=False,
    )
    return {
        "role": role,
        "model": model,
        "provider_backend": "ollama",
        "provider_compute_device": "ollama/gpu1" if role == "gpu1_planner" else "ollama/gpu0-vulkan",
        "num_ctx": num_ctx,
        "effective_num_ctx": num_ctx,
        "ollama_gpu_layers_requested": gpu_layers_requested,
        "ollama_options_num_gpu": num_gpu,
        "load_performed": True,
        "boot_probe_performed": True,
        "boot_loaded": True,
        "workload_verified_at_boot": False,
        "provider_work_verified": False,
        "provider_stage": "boot_probe",
        "response_text": text,
        "last_generate_response": client.last_generate_response,
    }


def _start_npu_child(repo_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    python_exe = Path(args.python_exe).expanduser() if args.python_exe else Path(sys.executable)
    ready_path = repo_root / "output" / "validation" / "provider_role_coexistence_npu_ready.json"
    ready_path.parent.mkdir(parents=True, exist_ok=True)
    if ready_path.exists():
        ready_path.unlink()
    payload = {
        "model_dir": args.npu_model_dir,
        "device": "NPU",
        "ready_path": str(ready_path),
        "hold_seconds": max(1.0, float(args.npu_hold_seconds)),
        "max_new_tokens": max(2, int(args.max_new_tokens)),
    }
    process = subprocess.Popen(
        [str(python_exe), "-m", "ia_carmine.providers.provider_mesh.provider_role_coexistence.cli", "--child-npu"],
        cwd=str(repo_root),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=command_env(repo_root),
    )
    assert process.stdin is not None
    process.stdin.write(json.dumps(payload, ensure_ascii=False))
    process.stdin.close()
    process.stdin = None
    deadline = time.time() + float(args.npu_timeout_seconds)
    ready_payload: dict[str, Any] = {}
    while time.time() < deadline:
        if ready_path.is_file():
            ready_payload = json.loads(ready_path.read_text(encoding="utf-8"))
            break
        if process.poll() is not None:
            break
        time.sleep(0.25)
    return {"process": process, "ready_payload": ready_payload, "ready_path": str(ready_path)}


def _child_npu() -> int:
    payload = json.loads(sys.stdin.read() or "{}")
    started = time.perf_counter()
    result: dict[str, Any]
    try:
        import openvino as ov  # noqa: PLC0415
        import openvino_genai as genai  # noqa: PLC0415
        core = ov.Core()
        devices = list(core.available_devices)
        device = str(payload.get("device") or "NPU")
        if device not in devices:
            raise RuntimeError(f"{device} not in available devices: {devices}")
        pipe = genai.LLMPipeline(str(payload["model_dir"]), device, MAX_PROMPT_LEN=512, MIN_RESPONSE_LEN=1)
        text = str(pipe.generate("IA-Carmine NPU coexistence probe: READY.", max_new_tokens=int(payload["max_new_tokens"]))).strip()
        result = {
            "role": "npu_micro_task_auditor",
            "provider_backend": "openvino",
            "provider_compute_device": "openvino/NPU",
            "model": Path(str(payload["model_dir"])).name,
            "model_loaded": True,
            "boot_probe_performed": True,
            "boot_loaded": True,
            "workload_verified_at_boot": False,
            "provider_work_verified": False,
            "provider_stage": "boot_probe",
            "device_verified": True,
            "devices": devices,
            "response_text": text,
            "elapsed_sec_to_ready": round(time.perf_counter() - started, 4),
        }
        Path(str(payload["ready_path"])).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        time.sleep(float(payload.get("hold_seconds") or 1.0))
        del pipe
    except Exception as exc:  # noqa: BLE001
        result = {"model_loaded": False, "device_verified": False, "errors": [f"{type(exc).__name__}: {exc}"]}
        Path(str(payload.get("ready_path") or "npu_ready.json")).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return 2
    return 0


def _unload_ollama_role(base_url: str, model: str) -> dict[str, Any]:
    client = OllamaSdkClient(base_url)
    client.unload(model)
    payload: dict[str, Any] = {"models": []}
    for _ in range(10):
        time.sleep(0.4)
        payload = client.ps()
        if not model_alive(payload, model):
            return {"unloaded": True, "ps": payload}
    return {"unloaded": False, "ps": payload}


def _deferred_unload(base_url: str, model: str) -> dict[str, Any]:
    return {
        "unloaded": False,
        "deferred_until_provider_cleanup": True,
        "base_url": base_url,
        "model": model,
    }


def _deferred_gpu0_server_stop(base_url: str) -> dict[str, Any]:
    return {
        "stopped": False,
        "deferred_until_provider_cleanup": True,
        "base_url": base_url,
    }


def _wait_npu_exit(process: Any) -> dict[str, Any]:
    if process is None:
        return {"exited": False, "reason": "process_missing"}
    try:
        stdout, stderr = process.communicate(timeout=20)
        return {"exited": True, "returncode": process.returncode, "stdout_tail": stdout[-1000:], "stderr_tail": stderr[-1000:]}
    except subprocess.TimeoutExpired:
        process.terminate()
        return {"exited": False, "reason": "timeout_terminated"}


def _resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def _markdown(report: dict[str, Any]) -> str:
    return (
        "# Provider Role Coexistence\n\n"
        f"- Passed: `{report.get('passed')}`\n"
        f"- Coexistence verified: `{report.get('coexistence_verified')}`\n"
        f"- GPU1 alive: `{report.get('roles', {}).get('gpu1_planner', {}).get('alive_during_coexistence')}`\n"
        f"- GPU0 alive: `{report.get('roles', {}).get('gpu0_peer', {}).get('alive_during_coexistence')}`\n"
        f"- NPU loaded: `{report.get('roles', {}).get('npu_micro_task_auditor', {}).get('model_loaded')}`\n"
        f"- Handoff provider loop: `{report.get('handoff_provider_loop')}`\n"
        f"- Unload seconds: `{report.get('provider_inactivity_unload_seconds')}`\n"
    )


if __name__ == "__main__":
    raise SystemExit(main())
