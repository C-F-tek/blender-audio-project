"""Common IO, path, process, and revision-context helpers."""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from ia_carmine._shared.live_flow_monitor import run_monitored_command
from ia_carmine._shared.process_tree import terminate_process_tree

DEFAULT_REQUEST = (
    "Esegui heap runtime con proposal chunks multi-parte. "
    "Non comprimere tutto nella sola risposta GPU1: salva blocchi par1/par2/par3, "
    "fai review GPU0 dei blocchi non operativi, fai micro-audit NPU se disponibile, "
    "usa debug lab e chiudi con composer finale su file persistenti."
)

REQUIRED_COMPOSER_JSON = "heap_final_proposal_composer.json"
REVISION_CONTEXT_MARKER = "EXTERNAL HEAP REVISION CONTEXT FROM PREVIOUS RUN"
WINDOWS_PROVIDER_STATUS_TIMEOUT_SECONDS = 1
OLLAMA_STOP_TIMEOUT_SECONDS = 5


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def resolve_repo_root(value: str) -> Path:
    return Path(value).resolve()


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def resolve_project_python(repo_root: Path, explicit: str = "") -> str:
    if explicit:
        return str(Path(explicit).resolve())
    for candidate in (
        repo_root / ".venv" / "Scripts" / "python.exe",
        repo_root / "venv" / "Scripts" / "python.exe",
        repo_root / ".venv314" / "Scripts" / "python.exe",
    ):
        if candidate.exists():
            return str(candidate.resolve())
    return sys.executable


def resolve_repo_file(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)


def load_operator_request(repo_root: Path, inline_request: str, request_file: str) -> tuple[str, str]:
    if not request_file:
        return inline_request, ""
    path = resolve_repo_file(repo_root, request_file)
    try:
        return path.read_text(encoding="utf-8-sig"), str(path)
    except Exception as exc:
        raise SystemExit(f"cannot read --request-file {path}: {type(exc).__name__}: {exc}") from exc


def run_command(
    command: list[str],
    repo_root: Path,
    timeout_seconds: int | None = None,
    *,
    flow_dir: Path | None = None,
    phase: str = "heap_context_closure_command",
) -> dict[str, Any]:
    return run_monitored_command(
        command,
        repo_root,
        timeout_seconds=timeout_seconds,
        flow_dir=flow_dir,
        status_name="heap_context_closure_live_flow",
        phase=phase,
        tail_chars=4000,
        keyboard_interrupt="exit",
    )


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


class _ProcessPidRef:
    def __init__(self, pid: int) -> None:
        self.pid = pid

    def kill(self) -> None:
        try:
            os.kill(self.pid, signal.SIGTERM if os.name == "nt" else 9)
        except BaseException:
            pass

    def terminate(self) -> None:
        try:
            os.kill(self.pid, signal.SIGTERM if os.name == "nt" else 15)
        except BaseException:
            pass


def terminate_provider_launch_manifest_processes(
    *,
    run_dir: Path,
    repo_root: Path,
    reason: str,
) -> dict[str, Any]:
    """Best-effort final cleanup for provider children listed in launch manifests."""

    provider_dir = run_dir / "provider_teamwork"
    manifests = sorted(provider_dir.glob("provider_launch_manifest*.json"))
    boot_reports = sorted(provider_dir.glob("provider_role_coexistence*.json"))
    report: dict[str, Any] = {
        "schema_version": 1,
        "kind": "provider_launch_manifest_orphan_cleanup",
        "reason": reason,
        "run_dir": str(run_dir),
        "manifest_count": len(manifests),
        "boot_report_count": len(boot_reports),
        "checked": [],
        "terminated": [],
        "skipped": [],
    }
    for manifest in manifests:
        payload = load_json(manifest)
        provider_models: list[tuple[str, str]] = []
        gpu0_base_urls: list[str] = []
        for lane in payload.get("lanes") or []:
            if not isinstance(lane, dict):
                continue
            provider_model = str(lane.get("provider_model") or "").strip()
            compute_device = str(lane.get("provider_compute_device") or "")
            provider_base_url = str(lane.get("provider_base_url") or "").strip()
            if "gpu0-vulkan" in compute_device:
                provider_base_url = provider_base_url or "http://127.0.0.1:11435"
                if provider_base_url not in gpu0_base_urls:
                    gpu0_base_urls.append(provider_base_url)
            elif not provider_base_url:
                provider_base_url = "http://127.0.0.1:11434"
            model_ref = (provider_model, provider_base_url)
            if provider_model and model_ref not in provider_models:
                provider_models.append(model_ref)
            pid = _safe_pid(lane.get("pid"))
            item = {
                "manifest": str(manifest),
                "lane": lane.get("lane"),
                "requirement": lane.get("requirement"),
                "pid": pid,
            }
            report["checked"].append(item)
            if pid <= 0:
                report["skipped"].append({**item, "reason": "missing_pid"})
                continue
            try:
                status = _provider_process_status(pid, repo_root)
            except BaseException as exc:  # noqa: BLE001 - cleanup must survive operator interrupts.
                status = {
                    "alive": True,
                    "safe_to_terminate": True,
                    "image_name": "",
                    "command_line": "",
                    "status_lookup_failed": True,
                    "status_lookup_error": type(exc).__name__,
                }
            item.update(status)
            if not status.get("alive"):
                report["skipped"].append({**item, "reason": "not_alive"})
                continue
            if not status.get("safe_to_terminate"):
                report["skipped"].append({**item, "reason": "pid_not_recognized_as_run_provider"})
                continue
            terminate_process_tree(_ProcessPidRef(pid))
            report["terminated"].append({**item, "reason": reason})
        for model, base_url in provider_models:
            stopped = _stop_ollama_model(model, base_url)
            if stopped:
                report.setdefault("ollama_models_stopped", []).append(model)
        for base_url in gpu0_base_urls:
            report.setdefault("gpu0_vulkan_server_stop", []).append(
                _stop_gpu0_vulkan_server(base_url)
            )
    for boot_report in boot_reports:
        _cleanup_provider_boot_handoff_report(boot_report, report)
    report["performed"] = bool(
        report["checked"]
        or report.get("boot_handoff_unload_checked")
        or report.get("gpu0_vulkan_server_stop")
    )
    report["terminated_count"] = len(report["terminated"])
    report["skipped_count"] = len(report["skipped"])
    write_json(run_dir / "provider_orphan_cleanup.json", report)
    return report


def _cleanup_provider_boot_handoff_report(path: Path, report: dict[str, Any]) -> None:
    payload = load_json(path)
    unload = payload.get("unload") if isinstance(payload.get("unload"), dict) else {}
    for role, item in unload.items():
        if not isinstance(item, dict) or not item.get("deferred_until_provider_cleanup"):
            continue
        model = str(item.get("model") or "").strip()
        base_url = str(item.get("base_url") or "").strip()
        if model and _stop_ollama_model(model, base_url):
            report.setdefault("ollama_models_stopped", []).append(model)
        report.setdefault("boot_handoff_unload_checked", []).append(
            {"source": str(path), "role": role, "model": model, "base_url": base_url}
        )
    stop = payload.get("gpu0_vulkan_server_stop")
    stop = stop if isinstance(stop, dict) else {}
    if stop.get("deferred_until_provider_cleanup"):
        base_url = str(stop.get("base_url") or "http://127.0.0.1:11435")
        report.setdefault("gpu0_vulkan_server_stop", []).append(
            _stop_gpu0_vulkan_server(base_url)
        )


def _safe_pid(value: Any) -> int:
    try:
        return int(value or 0)
    except BaseException:
        return 0


def _provider_process_status(pid: int, repo_root: Path) -> dict[str, Any]:
    if os.name == "nt":
        return _windows_provider_process_status(pid, repo_root)
    try:
        os.kill(pid, 0)
    except KeyboardInterrupt:
        raise
    except BaseException:
        return {"alive": False, "safe_to_terminate": False, "image_name": "", "command_line": ""}
    return {"alive": True, "safe_to_terminate": True, "image_name": "", "command_line": ""}


def _windows_provider_process_status(pid: int, repo_root: Path) -> dict[str, Any]:
    image_name = ""
    command_line = ""
    try:
        task = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
            capture_output=True,
            text=True,
            check=False,
            timeout=WINDOWS_PROVIDER_STATUS_TIMEOUT_SECONDS,
        )
        lines = [line.strip() for line in (task.stdout or "").splitlines() if line.strip()]
        if task.returncode != 0 or not lines or not lines[0].startswith('"'):
            return {"alive": False, "safe_to_terminate": False, "image_name": "", "command_line": ""}
        image_name = (lines[0].split(",", 1)[0] or "").strip().strip('"')
    except BaseException as exc:  # noqa: BLE001 - cleanup must not block termination.
        return {
            "alive": True,
            "safe_to_terminate": True,
            "image_name": "",
            "command_line": "",
            "status_lookup_failed": True,
            "status_lookup_error": type(exc).__name__,
        }
    try:
        ps = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                f"(Get-CimInstance Win32_Process -Filter \"ProcessId={pid}\").CommandLine",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=WINDOWS_PROVIDER_STATUS_TIMEOUT_SECONDS,
        )
        command_line = (ps.stdout or "").strip()
    except BaseException:
        command_line = ""
    normalized = command_line.lower()
    repo = str(repo_root).lower()
    provider_command = (
        repo in normalized
        or "ia_carmine" in normalized
        or "build_ollama_gpu0_peer_report" in normalized
        or "build_npu_micro_task_companion_report" in normalized
        or "build_local_provider_probe" in normalized
    )
    safe = image_name.lower().startswith("python") and (provider_command or not command_line)
    return {
        "alive": True,
        "safe_to_terminate": safe,
        "image_name": image_name,
        "command_line": command_line[:1000],
    }


def _stop_ollama_model(model: str, base_url: str = "") -> bool:
    try:
        env = os.environ.copy()
        if base_url:
            env["OLLAMA_HOST"] = base_url
        result = subprocess.run(
            ["ollama", "stop", model],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            check=False,
            timeout=OLLAMA_STOP_TIMEOUT_SECONDS,
            env=env,
        )
        return result.returncode == 0
    except BaseException:
        return False


def _stop_gpu0_vulkan_server(base_url: str) -> dict[str, Any]:
    try:
        from ia_carmine.providers.ollama.role_models import stop_gpu0_vulkan_server

        return stop_gpu0_vulkan_server(base_url)
    except BaseException as exc:  # noqa: BLE001 - cleanup evidence only.
        return {"stopped": False, "base_url": base_url, "error": f"{type(exc).__name__}: {exc}"}


def write_documents_run_manifest(
    *,
    documents_root: str,
    repo_root: Path,
    run_dir: Path,
    stamp: str,
    request_file: str,
    status: str,
) -> str:
    if not documents_root:
        return ""
    documents_dir = Path(documents_root).expanduser().resolve(strict=False)
    documents_dir.mkdir(parents=True, exist_ok=True)
    manifest = documents_dir / "RUN_IN_PROGRESS.json"
    payload = {
        "schema_version": 1,
        "kind": "operator_documents_run_manifest",
        "stamp": stamp,
        "status": status,
        "repo_root": str(repo_root),
        "run_dir": str(run_dir),
        "request_file": request_file,
        "code_product_expected": str(documents_dir / "CODE_PRODUCT_FULL_PATCH.md"),
        "final_readable_expected": str(documents_dir / "FINAL_READABLE_PRODUCT.md"),
    }
    write_json(manifest, payload)
    return str(manifest)


def is_complete_heap_run_dir(path: Path) -> bool:
    return (
        path.is_dir()
        and path.name.startswith("heap_context_closure_")
        and (path / REQUIRED_COMPOSER_JSON).exists()
    )


def latest_revision_context(repo_root: Path) -> tuple[Path | None, dict[str, Any], str]:
    validation_dir = repo_root / "output" / "validation"
    if not validation_dir.exists():
        return None, {}, "none"
    candidates = sorted(
        [
            run_dir / "external_heap_revision_context.json"
            for run_dir in validation_dir.iterdir()
            if is_complete_heap_run_dir(run_dir)
            and (run_dir / "external_heap_revision_context.json").exists()
        ],
        key=lambda path: path.stat().st_mtime if path.exists() else 0,
        reverse=True,
    )
    if not candidates:
        return None, {}, "none"
    path = candidates[0].resolve()
    return path, load_json(path), "latest_complete_heap_context_closure_with_composer_json"


def resolve_revision_context(repo_root: Path, value: str) -> tuple[Path | None, dict[str, Any], str]:
    mode = str(value or "auto_latest").strip()
    if not mode or mode.lower() in {"off", "none", "false", "0"}:
        return None, {}, "off"
    if mode == "auto_latest":
        return latest_revision_context(repo_root)
    path = Path(mode)
    if not path.is_absolute():
        path = repo_root / path
    path = path.resolve()
    return path, load_json(path), "explicit_revision_context"
