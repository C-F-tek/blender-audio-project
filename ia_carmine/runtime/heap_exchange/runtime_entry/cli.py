#!/usr/bin/env python3
"""Build the heap/exchange runtime entry envelope.

This tool does not schedule the dynamic center of the run. It creates an
observable runtime session entry that records the task, context artifacts and
available lanes so GPU/provider/NPU/adapter phases can publish into one shared
exchange surface.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ia_carmine.runtime.heap_exchange.io import append_jsonl


def load_json(path: Path | None) -> tuple[dict[str, Any] | None, str | None]:
    if path is None:
        return None, "not provided"
    if not path.exists():
        return None, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, "json root is not an object"
    return data, None


def rel(repo_root: Path, path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def repo_path(repo_root: Path, raw: str) -> Path | None:
    if not raw:
        return None
    path = Path(raw)
    return path if path.is_absolute() else repo_root / path


def discover_first(repo_root: Path, patterns: list[str]) -> Path | None:
    for pattern in patterns:
        matches = sorted(
            repo_root.glob(pattern),
            key=lambda item: item.stat().st_mtime if item.exists() else 0,
            reverse=True,
        )
        if matches:
            return matches[0]
    return None


def write_public_event(observer_dir: Path | None, event: dict[str, Any]) -> None:
    if observer_dir is None:
        return
    payload = {
        "kind": "ai_public_exchange_event",
        "schema_version": 1,
        "lane": "heap_exchange",
        "speaker": "runtime_entry",
        "event_type": event.get("kind", "heap_entry"),
        "summary": event.get("summary", "heap/exchange runtime entry registered"),
        "source_file": event.get("source_file", ""),
        "raw_thinking_exposed": False,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "stamp": event.get("stamp", ""),
    }
    append_jsonl(observer_dir / "ai_public_events.jsonl", payload)


def lane(
    name: str,
    role: str,
    available: bool,
    source: str = "",
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "name": name,
        "role": role,
        "available": bool(available),
        "source": source,
        "details": details or {},
    }


def bool_from_report(report: dict[str, Any] | None, key: str) -> bool:
    return bool(report and report.get(key) is True)


def build_lanes(
    gpu0_report: dict[str, Any] | None,
    official_report: dict[str, Any] | None,
    workload_report: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    devices = []
    if gpu0_report:
        raw_devices = gpu0_report.get("available_devices")
        if isinstance(raw_devices, list):
            devices = [str(item) for item in raw_devices]

    official_passed = bool(
        official_report
        and (official_report.get("passed") is True or official_report.get("status") == "passed")
    )
    workload_ok = bool(workload_report and workload_report.get("passed") is True)

    return [
        lane(
            "gpu0",
            "ollama_vulkan_peer_reviewer_lane",
            bool_from_report(gpu0_report, "provider_device_verified")
            or "gpu0-vulkan" in str((gpu0_report or {}).get("provider_compute_device") or ""),
            "ollama_gpu0_peer_report",
            {
                "selected_device": (gpu0_report or {}).get("provider_compute_device", ""),
                "workload_passed": bool_from_report(gpu0_report, "provider_work_verified"),
            },
        ),
        lane(
            "gpu1",
            "reserved_or_provider_lane",
            bool_from_report(gpu0_report, "openvino_gpu1_reserved_visible") or "GPU.1" in devices,
            "openvino_device_visibility",
            {"reserved_visible": bool_from_report(gpu0_report, "openvino_gpu1_reserved_visible")},
        ),
        lane(
            "npu",
            "microoperation_efficiency_peer_lane",
            "NPU" in devices or bool((official_report or {}).get("npu_probe_requested")),
            "openvino_device_visibility_or_official_adapter",
            {
                "device_visible": "NPU" in devices,
                "audit_role": "deterministic_script_lane_not_dynamic_npu_peer",
            },
        ),
        lane(
            "deterministic_audit",
            "deterministic_script_audit_lane_reusable_before_heap_exchange_closure",
            True,
            "repository_validation_scripts",
            {
                "dynamic_npu_peer_role": "microoperation_efficiency",
                "audit_lane": "deterministic_script",
            },
        ),
        lane(
            "ollama_provider",
            "primary_advisory_provider_lane",
            official_passed or workload_ok,
            "official_adapter_or_workload_quality",
            {
                "official_passed": official_passed,
                "workload_quality_passed": workload_ok,
            },
        ),
        lane(
            "official_adapter",
            "task_interpreter_lane",
            official_passed,
            "official_phase_report",
            {
                "status": (official_report or {}).get("status", ""),
                "return_code": (official_report or {}).get("return_code", ""),
            },
        ),
        lane(
            "context_memory",
            "context_and_agent_state_lane",
            True,
            "context_pack_and_agent_state",
            {},
        ),
    ]


def build_knowledge_surface(
    lanes: list[dict[str, Any]], artifacts: dict[str, str]
) -> dict[str, Any]:
    available_lanes = [item["name"] for item in lanes if item.get("available")]
    return {
        "source_of_knowledge": "heap_exchange",
        "knowledge_surface": "shared_runtime_heap_blackboard",
        "routing_model": "dynamic_exchange_not_static_chain",
        "dynamic_exchange_pipeline": True,
        "static_chain_invocation_performed": False,
        "guided_chain_call_sequence_required": False,
        "lane_interaction_is_runtime_routed": True,
        "lane_autonomy_model": "gpu1_gpu0_npu_provider_lanes_publish_and_consume_exchange_evidence",
        "deterministic_boundaries": {
            "in_controlled": True,
            "loop_dynamic": True,
            "out_deterministic": True,
        },
        "available_lanes": available_lanes,
        "input_artifacts": artifacts,
    }


def main() -> int:
    try:
        from ia_carmine._shared.heap_exchange_runtime_entry_cli import main as cli_main
    except ModuleNotFoundError:
        from ia_carmine._shared.heap_exchange_runtime_entry_cli import main as cli_main
    return cli_main()


if __name__ == "__main__":
    raise SystemExit(main())
