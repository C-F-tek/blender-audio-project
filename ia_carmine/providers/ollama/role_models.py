from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from ia_carmine.providers.ollama.config import DEFAULT_BASE_URL, bounded_keep_alive, find_ollama_exe
from ia_carmine._shared.ollama_server_process import ollama_host_env, ollama_listen_pid
from ia_carmine.providers.ollama.sdk_client import OllamaSdkClient, OllamaSdkError
from ia_carmine.providers.ollama.vulkan_devices import resolve_vulkan_visible_devices

ROLE_DEFAULTS = {
    "gpu1_planner": ("IA_CARMINE_GPU1_MODEL", "qwen3-coder:latest"),
    "gpu0_peer": ("IA_CARMINE_GPU0_MODEL", "qwen3:1.7b"),
}


def _option_source(argv: list[str], *options: str) -> str:
    for token in argv:
        for option in options:
            if token == option or token.startswith(f"{option}="):
                return "cli_arg"
    return "standalone_default"


def cli_config_sources(argv: list[str]) -> dict[str, str]:
    gpu1_env, _ = ROLE_DEFAULTS["gpu1_planner"]
    gpu0_env, _ = ROLE_DEFAULTS["gpu0_peer"]
    return {
        "gpu1_base_url": _option_source(argv, "--gpu1-base-url"),
        "gpu0_base_url": _option_source(argv, "--gpu0-base-url"),
        "gpu1_model": (
            _option_source(argv, "--gpu1-model")
            if _option_source(argv, "--gpu1-model") == "cli_arg"
            else (f"env:{gpu1_env}" if os.environ.get(gpu1_env, "").strip() else "standalone_default")
        ),
        "gpu0_model": (
            _option_source(argv, "--gpu0-model")
            if _option_source(argv, "--gpu0-model") == "cli_arg"
            else (f"env:{gpu0_env}" if os.environ.get(gpu0_env, "").strip() else "standalone_default")
        ),
        "gpu0_vulkan_visible_devices": _option_source(argv, "--gpu0-vulkan-visible-devices"),
        "keep_alive": _option_source(argv, "--keep-alive"),
        "num_ctx": _option_source(argv, "--num-ctx"),
        "ollama_gpu_layers": _option_source(argv, "--ollama-gpu-layers", "--ollama-num-gpu"),
        "max_new_tokens": _option_source(argv, "--max-new-tokens"),
    }


def role_model(role: str, explicit: str = "") -> str:
    env_name, default = ROLE_DEFAULTS[role]
    return explicit or os.environ.get(env_name, "").strip() or default


def model_alive(ps_payload: dict[str, Any], model: str) -> bool:
    models = ps_payload.get("models")
    for item in models if isinstance(models, list) else []:
        data = item if isinstance(item, dict) else getattr(item, "model_dump", lambda: {})()
        name = str(data.get("model") or data.get("name") or "")
        if name == model:
            return True
    return False


def ensure_role_models(
    *,
    gpu1_client: OllamaSdkClient,
    gpu0_client: OllamaSdkClient,
    gpu1_model: str = "",
    gpu0_model: str = "",
    pull_missing: bool = True,
    load: bool = True,
    keep_alive: str = "120s",
    num_ctx: int = 2048,
    gpu_layers: str | int | None = "all",
    max_new_tokens: int = 16,
    unload_after_check: bool = True,
) -> dict[str, Any]:
    keep_alive = bounded_keep_alive(keep_alive)
    gpu_layers_requested = gpu_layers_label(gpu_layers)
    num_gpu = gpu_layers_option(gpu_layers)
    models_before = {
        "gpu1_planner": sorted(set(gpu1_client.list_models())),
        "gpu0_peer": sorted(set(gpu0_client.list_models())),
    }
    roles = {
        "gpu1_planner": role_model("gpu1_planner", gpu1_model),
        "gpu0_peer": role_model("gpu0_peer", gpu0_model),
    }
    role_reports: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    clients = {"gpu1_planner": gpu1_client, "gpu0_peer": gpu0_client}
    for role, model in roles.items():
        report = _ensure_one_role(
            client=clients[role],
            role=role,
            model=model,
            models_before=set(models_before[role]),
            pull_missing=pull_missing,
            load=load,
            keep_alive=keep_alive,
            num_ctx=num_ctx,
            gpu_layers_requested=gpu_layers_requested,
            num_gpu=num_gpu,
            max_new_tokens=max_new_tokens,
        )
        role_reports[role] = report
    coexistence_ps = {role: clients[role].ps() for role in roles}
    for role, report in role_reports.items():
        report["alive_during_coexistence"] = model_alive(coexistence_ps[role], str(report["model"]))
        if report["errors"] or not report.get("alive_after_load"):
            errors.append(f"{role}:{report['model']}:not_alive_after_workload")
        if not report.get("alive_during_coexistence"):
            errors.append(f"{role}:{report['model']}:not_alive_during_coexistence")
    unload_reports = _unload_role_models(clients, roles) if unload_after_check else {}
    final_ps = {role: clients[role].ps() for role in roles}
    for role, report in role_reports.items():
        report.update(unload_reports.get(role, {}))
        report["alive_final"] = model_alive(final_ps[role], str(report["model"]))
        if unload_after_check and not report.get("unloaded_after_check"):
            errors.append(f"{role}:{report['model']}:not_unloaded_after_check")
    return {
        "schema_version": 1,
        "kind": "ollama_role_models",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "passed": not errors,
        "errors": errors,
        "roles": role_reports,
        "models_before": models_before,
        "coexistence_ps_payload": coexistence_ps,
        "final_ps_payload": final_ps,
        "coexistence_verified": all(bool(r.get("alive_during_coexistence")) for r in role_reports.values()),
        "provider_execution_performed": bool(load),
        "ollama_inactivity_unload_seconds": 120,
        "num_ctx": num_ctx,
        "effective_num_ctx": num_ctx,
        "ollama_gpu_layers_requested": gpu_layers_requested,
        "ollama_options_num_gpu": num_gpu,
        "unload_after_check": bool(unload_after_check),
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def _ensure_one_role(
    *,
    client: OllamaSdkClient,
    role: str,
    model: str,
    models_before: set[str],
    pull_missing: bool,
    load: bool,
    keep_alive: str,
    num_ctx: int,
    gpu_layers_requested: str,
    num_gpu: int | None,
    max_new_tokens: int,
) -> dict[str, Any]:
    report: dict[str, Any] = {
        "role": role,
        "model": model,
        "num_ctx": num_ctx,
        "effective_num_ctx": num_ctx,
        "ollama_gpu_layers_requested": gpu_layers_requested,
        "ollama_options_num_gpu": num_gpu,
        "present_before": model in models_before,
        "pull_performed": False,
        "load_performed": False,
        "alive_after": False,
        "alive_after_load": False,
        "unload_performed": False,
        "unloaded_after_check": False,
        "errors": [],
    }
    if model not in models_before and pull_missing:
        try:
            report["pull_result"] = client.pull(model)
            report["pull_performed"] = True
        except OllamaSdkError as exc:
            report["errors"].append(str(exc))
    if load and not report["errors"]:
        try:
            text = client.generate(
                model=model,
                prompt=f"IA-Carmine role {role}: reply READY in one short sentence.",
                keep_alive=keep_alive,
                temperature=0.0,
                num_predict=max_new_tokens,
                num_thread=None,
                num_ctx=num_ctx,
                num_gpu=num_gpu,
                think=False,
            )
            report["load_performed"] = True
            report["load_response_chars"] = len(text)
            report["last_generate_response"] = client.last_generate_response
        except OllamaSdkError as exc:
            report["errors"].append(str(exc))
    try:
        ps_payload = client.ps()
        report["ps_payload"] = ps_payload
        report["alive_after"] = model_alive(ps_payload, model)
        report["alive_after_load"] = report["alive_after"]
    except OllamaSdkError as exc:
        report["errors"].append(str(exc))
    return report


def _unload_role_models(
    clients: dict[str, OllamaSdkClient],
    roles: dict[str, str],
) -> dict[str, dict[str, Any]]:
    reports: dict[str, dict[str, Any]] = {}
    for role, model in roles.items():
        report: dict[str, Any] = {"unload_performed": False, "unloaded_after_check": False}
        try:
            clients[role].unload(model)
            after_unload = _wait_unloaded(clients[role], model)
            report["ps_after_unload"] = after_unload
            report["unload_performed"] = True
            report["unloaded_after_check"] = not model_alive(after_unload, model)
        except Exception as exc:  # noqa: BLE001 - unload proof must stay report-only.
            report["unload_error"] = f"{type(exc).__name__}: {exc}"
        reports[role] = report
    return reports


def _wait_unloaded(client: OllamaSdkClient, model: str) -> dict[str, Any]:
    payload: dict[str, Any] = {"models": []}
    for _ in range(8):
        time.sleep(0.5)
        payload = client.ps()
        if not model_alive(payload, model):
            return payload
    return payload


def gpu_layers_label(value: str | int | None) -> str:
    if value is None:
        return "default"
    text = str(value).strip().lower()
    if text in {"", "default", "auto"}:
        return "default"
    if text in {"all", "-1"}:
        return "all"
    return text


def gpu_layers_option(value: str | int | None) -> int | None:
    label = gpu_layers_label(value)
    if label == "default":
        return None
    if label == "all":
        return -1
    try:
        return int(label)
    except ValueError as exc:
        raise ValueError("--ollama-gpu-layers must be 'all', 'default', or an integer") from exc


def _write(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")


def _markdown(report: dict[str, Any]) -> str:
    lines = ["# Ollama Role Models", "", f"- Passed: `{report['passed']}`"]
    for role, item in report["roles"].items():
        lines.append(
            f"- `{role}`: model=`{item['model']}` alive_final=`{item.get('alive_final')}` "
            f"alive_after_load=`{item.get('alive_after_load')}` "
            f"alive_during_coexistence=`{item.get('alive_during_coexistence')}` "
            f"unloaded_after_check=`{item.get('unloaded_after_check')}` "
            f"pulled=`{item['pull_performed']}` loaded=`{item['load_performed']}`"
        )
    if report["errors"]:
        lines.append("\n## Errors")
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def start_gpu0_vulkan_server(
    *,
    base_url: str,
    repo_root: Path,
    visible_devices: str = "auto",
    startup_timeout: float = 20.0,
    restart_if_ready: bool = False,
) -> dict[str, Any]:
    selection = resolve_vulkan_visible_devices(visible_devices)
    client = OllamaSdkClient(base_url)
    log_dir = repo_root / "output" / "validation" / "ollama_gpu0_vulkan_server"
    if client.is_ready():
        if not restart_if_ready:
            stdout_log = log_dir / "stdout.log"
            stderr_log = log_dir / "stderr.log"
            return {
                "started": False,
                "ready": True,
                "base_url": base_url,
                "pid": ollama_listen_pid(base_url),
                "reason": "already_ready",
                "vulkan_device_selection": selection,
                "stdout_log": str(stdout_log) if stdout_log.is_file() else "",
                "stderr_log": str(stderr_log) if stderr_log.is_file() else "",
                "existing_server_requires_handoff_evidence": True,
            }
        stop_gpu0_vulkan_server(base_url)
    exe = find_ollama_exe()
    if not exe:
        return {
            "started": False,
            "ready": False,
            "base_url": base_url,
            "error": "ollama executable not found",
            "vulkan_device_selection": selection,
        }
    log_dir.mkdir(parents=True, exist_ok=True)
    stdout = (log_dir / "stdout.log").open("wb")
    stderr = (log_dir / "stderr.log").open("wb")
    env = os.environ.copy()
    env.update(
        {
            "OLLAMA_HOST": ollama_host_env(base_url),
            "OLLAMA_VULKAN": "1",
            "OLLAMA_LLM_LIBRARY": "vulkan",
            "GGML_VK_VISIBLE_DEVICES": str(selection["resolved"]),
            "CUDA_VISIBLE_DEVICES": "-1",
            "NVIDIA_VISIBLE_DEVICES": "none",
            "OLLAMA_DEBUG": "1",
            "OLLAMA_SCHED_SPREAD": "false",
        }
    )
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    process = subprocess.Popen(
        [str(exe), "serve"],
        cwd=str(repo_root),
        env=env,
        stdout=stdout,
        stderr=stderr,
        creationflags=creationflags,
    )
    deadline = time.time() + startup_timeout
    ready = False
    while time.time() < deadline:
        if client.is_ready():
            ready = True
            break
        if process.poll() is not None:
            break
        time.sleep(0.5)
    return {
        "started": True,
        "ready": ready,
        "base_url": base_url,
        "pid": process.pid,
        "vulkan_device_selection": selection,
        "env": {
            "OLLAMA_HOST": env["OLLAMA_HOST"],
            "OLLAMA_VULKAN": env["OLLAMA_VULKAN"],
            "OLLAMA_LLM_LIBRARY": env["OLLAMA_LLM_LIBRARY"],
            "GGML_VK_VISIBLE_DEVICES": env["GGML_VK_VISIBLE_DEVICES"],
            "CUDA_VISIBLE_DEVICES": env["CUDA_VISIBLE_DEVICES"],
            "NVIDIA_VISIBLE_DEVICES": env["NVIDIA_VISIBLE_DEVICES"],
        },
        "stdout_log": str(log_dir / "stdout.log"),
        "stderr_log": str(log_dir / "stderr.log"),
        "returncode": process.poll(),
    }


def stop_gpu0_vulkan_server(base_url: str) -> dict[str, Any]:
    pid = ollama_listen_pid(base_url)
    if not pid:
        return {"requested": True, "stopped": False, "reason": "no_listening_pid", "base_url": base_url}
    try:
        completed = subprocess.run(
            ["powershell", "-NoProfile", "-Command", f"Stop-Process -Id {int(pid)} -Force"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception:
        return {
            "requested": True,
            "stopped": False,
            "base_url": base_url,
            "pid": pid,
            "reason": "stop_process_exception",
        }
    time.sleep(1.0)
    still_listening = ollama_listen_pid(base_url)
    return {
        "requested": True,
        "stopped": not bool(still_listening),
        "base_url": base_url,
        "pid": pid,
        "returncode": completed.returncode,
        "stderr_tail": (completed.stderr or "")[-500:],
        "stdout_tail": (completed.stdout or "")[-500:],
        "still_listening_pid": still_listening,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--gpu1-base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--gpu0-base-url", default="http://127.0.0.1:11435")
    parser.add_argument("--gpu1-model", default="")
    parser.add_argument("--gpu0-model", default="")
    parser.add_argument("--start-gpu0-vulkan-server", action="store_true")
    parser.add_argument("--gpu0-vulkan-visible-devices", default="auto")
    parser.add_argument("--restart-gpu0-vulkan-server", action="store_true")
    parser.add_argument("--keep-gpu0-vulkan-server", action="store_true")
    parser.add_argument("--no-pull", action="store_true")
    parser.add_argument("--no-load", action="store_true")
    parser.add_argument("--keep-alive", default="120s")
    parser.add_argument("--keep-loaded-after-check", action="store_true")
    parser.add_argument("--num-ctx", type=int, default=2048)
    parser.add_argument("--ollama-gpu-layers", "--ollama-num-gpu", dest="ollama_gpu_layers", default="all")
    parser.add_argument("--max-new-tokens", type=int, default=16)
    parser.add_argument("--output", default="output/validation/ollama_role_models.json")
    parser.add_argument("--markdown-output", default="output/validation/ollama_role_models.md")
    raw_argv = sys.argv[1:]
    args = parser.parse_args(raw_argv)
    repo_root = Path(args.repo_root).resolve()
    gpu0_server = {"started": False, "ready": False, "reason": "not_requested"}
    if args.start_gpu0_vulkan_server:
        gpu0_server = start_gpu0_vulkan_server(
            base_url=args.gpu0_base_url,
            repo_root=repo_root,
            visible_devices=args.gpu0_vulkan_visible_devices,
            restart_if_ready=args.restart_gpu0_vulkan_server,
        )
    report = ensure_role_models(
        gpu1_client=OllamaSdkClient(args.gpu1_base_url),
        gpu0_client=OllamaSdkClient(args.gpu0_base_url),
        gpu1_model=args.gpu1_model,
        gpu0_model=args.gpu0_model,
        pull_missing=not args.no_pull,
        load=not args.no_load,
        keep_alive=args.keep_alive,
        num_ctx=args.num_ctx,
        gpu_layers=args.ollama_gpu_layers,
        max_new_tokens=args.max_new_tokens,
        unload_after_check=not args.keep_loaded_after_check,
    )
    report["gpu1_base_url"] = args.gpu1_base_url
    report["gpu0_base_url"] = args.gpu0_base_url
    report["config_sources"] = cli_config_sources(raw_argv)
    report["standalone_default_fields"] = [
        key for key, source in report["config_sources"].items() if source == "standalone_default"
    ]
    report["gpu0_vulkan_server"] = gpu0_server
    if args.start_gpu0_vulkan_server and not args.keep_gpu0_vulkan_server and gpu0_server.get("started"):
        report["gpu0_vulkan_server_stop"] = stop_gpu0_vulkan_server(args.gpu0_base_url)
    if args.start_gpu0_vulkan_server and not gpu0_server.get("ready"):
        report["passed"] = False
        report["errors"].append("gpu0_vulkan_server_not_ready")
    output = _resolve(repo_root, args.output)
    markdown = _resolve(repo_root, args.markdown_output)
    _write(output, report)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text(_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "output": str(output), "markdown": str(markdown)}, indent=2))
    return 0 if report["passed"] else 2


def _resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


if __name__ == "__main__":
    raise SystemExit(main())
