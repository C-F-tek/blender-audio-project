#!/usr/bin/env python3
"""Build the heap/exchange runtime entry envelope.

This tool does not schedule the dynamic center of the run. It creates an
observable runtime session entry that records the task, context artifacts and
available lanes so GPU/provider/NPU/adapter phases can publish into one shared
exchange surface.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    from report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore


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
        matches = sorted(repo_root.glob(pattern), key=lambda item: item.stat().st_mtime if item.exists() else 0, reverse=True)
        if matches:
            return matches[0]
    return None


def append_jsonl(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    event = dict(event)
    event.setdefault("timestamp", datetime.now().isoformat(timespec="seconds"))
    path.open("a", encoding="utf-8", newline="\n").write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


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


def lane(name: str, role: str, available: bool, source: str = "", details: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "name": name,
        "role": role,
        "available": bool(available),
        "source": source,
        "details": details or {},
    }


def bool_from_report(report: dict[str, Any] | None, key: str) -> bool:
    return bool(report and report.get(key) is True)


def build_lanes(gpu0_report: dict[str, Any] | None, official_report: dict[str, Any] | None, workload_report: dict[str, Any] | None) -> list[dict[str, Any]]:
    devices = []
    if gpu0_report:
        raw_devices = gpu0_report.get("available_devices")
        if isinstance(raw_devices, list):
            devices = [str(item) for item in raw_devices]

    official_passed = bool(official_report and (official_report.get("passed") is True or official_report.get("status") == "passed"))
    workload_ok = bool(workload_report and workload_report.get("passed") is True)

    return [
        lane(
            "gpu0",
            "companion_workload_lane",
            bool_from_report(gpu0_report, "openvino_gpu0_visible") or "GPU.0" in devices,
            "openvino_gpu0_workload_report",
            {"selected_device": (gpu0_report or {}).get("selected_device", ""), "workload_passed": bool_from_report(gpu0_report, "openvino_gpu0_workload_passed")},
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
            {"device_visible": "NPU" in devices, "audit_role": "deterministic_script_lane_not_dynamic_npu_peer"},
        ),
        lane(
            "deterministic_audit",
            "deterministic_script_audit_lane_reusable_before_heap_exchange_closure",
            True,
            "repository_validation_scripts",
            {"dynamic_npu_peer_role": "microoperation_efficiency", "audit_lane": "deterministic_script"},
        ),
        lane(
            "ollama_provider",
            "primary_advisory_provider_lane",
            official_passed or workload_ok,
            "official_adapter_or_workload_quality",
            {"official_passed": official_passed, "workload_quality_passed": workload_ok},
        ),
        lane(
            "official_adapter",
            "task_interpreter_lane",
            official_passed,
            "official_phase_report",
            {"status": (official_report or {}).get("status", ""), "return_code": (official_report or {}).get("return_code", "")},
        ),
        lane(
            "context_memory",
            "context_and_agent_state_lane",
            True,
            "context_pack_and_agent_state",
            {},
        ),
    ]


def build_knowledge_surface(lanes: list[dict[str, Any]], artifacts: dict[str, str]) -> dict[str, Any]:
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


def render_markdown(report: dict[str, Any]) -> str:
    knowledge = report.get("knowledge_surface") or {}
    lines = [
        "# Heap Exchange Runtime Entry",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Stamp: `{report.get('stamp')}`",
        f"- Task file: `{report.get('task_file')}`",
        f"- Knowledge source: `{knowledge.get('source_of_knowledge', report.get('source_of_knowledge', ''))}`",
        f"- Routing model: `{knowledge.get('routing_model', '')}`",
        "",
        "## Runtime rule",
        "",
        "The task and inputs are controlled at entry. The center of the run is dynamic and may use the registered lanes according to current routing logic. Exit must produce concrete reviewable product or fail honestly.",
        "",
        "## Knowledge surface",
        "",
        "The heap/exchange is the source of runtime knowledge. GPU1, GPU0, NPU, provider, shared-memory and deterministic lanes publish into and consume from this shared surface; entry does not prescribe a static call chain. NPU is the microoperation/efficiency peer in the dynamic loop; complete audit remains a deterministic/script lane reusable before heap/exchange closure.",
        "",
        "## Lanes",
        "",
        "| Lane | Role | Available | Source |",
        "|---|---|---:|---|",
    ]
    for item in report.get("lanes", []):
        lines.append(f"| `{item.get('name')}` | {item.get('role')} | `{item.get('available')}` | {item.get('source')} |")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--task-file", default="")
    parser.add_argument("--context-pack", default="")
    parser.add_argument("--agent-state", default="")
    parser.add_argument("--gpu0-report", default="")
    parser.add_argument("--official-report", default="")
    parser.add_argument("--workload-quality-report", default="")
    parser.add_argument("--observer-dir", default="")
    parser.add_argument("--runtime-state", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown-output", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    stamp = args.stamp
    packets_dir = repo_root / "output" / "ai_packets" / stamp

    task_file = repo_path(repo_root, args.task_file)
    context_pack = repo_path(repo_root, args.context_pack) or discover_first(repo_root, [f"output/ai_context_packs/*{stamp}*.json", f"output/ai_context_packs/*{stamp}*.md"])
    agent_state = repo_path(repo_root, args.agent_state) or discover_first(repo_root, [f"output/ai_packets/{stamp}/*agent_state*.json", f"output/validation/*agent_state*{stamp}*.json"])
    gpu0_report_path = repo_path(repo_root, args.gpu0_report) or (repo_root / f"output/validation/openvino_gpu0_workload_{stamp}.json")
    official_report_path = repo_path(repo_root, args.official_report) or (repo_root / f"output/validation/{stamp}_phase_official.json")
    workload_report_path = repo_path(repo_root, args.workload_quality_report) or (repo_root / "output/validation/ai_workload_report_quality.json")
    observer_dir = repo_path(repo_root, args.observer_dir) or discover_first(repo_root, [f"output/local_ai_runs/*{stamp}*_observer"])
    runtime_state = repo_path(repo_root, args.runtime_state) or (packets_dir / "heap_exchange_runtime_state.jsonl")
    output = repo_path(repo_root, args.output) or (packets_dir / "heap_exchange_runtime_entry.json")
    markdown_output = repo_path(repo_root, args.markdown_output) or (packets_dir / "heap_exchange_runtime_entry.md")

    gpu0_report, gpu0_error = load_json(gpu0_report_path)
    official_report, official_error = load_json(official_report_path)
    workload_report, workload_error = load_json(workload_report_path)

    warnings = []
    for name, path, error in (
        ("gpu0_report", gpu0_report_path, gpu0_error),
        ("official_report", official_report_path, official_error),
        ("workload_quality_report", workload_report_path, workload_error),
    ):
        if error not in (None, "not provided"):
            warnings.append(f"{name}: {rel(repo_root, path)} {error}")

    lanes = build_lanes(gpu0_report, official_report, workload_report)
    available_count = sum(1 for item in lanes if item["available"])
    artifact_map = {
        "task_file": rel(repo_root, task_file),
        "context_pack": rel(repo_root, context_pack),
        "agent_state": rel(repo_root, agent_state),
        "runtime_state": rel(repo_root, runtime_state),
        "observer_dir": rel(repo_root, observer_dir),
    }
    knowledge_surface = build_knowledge_surface(lanes, artifact_map)
    errors = []
    if task_file is not None and not task_file.exists():
        errors.append(f"task file missing: {rel(repo_root, task_file)}")
    if available_count < 2:
        errors.append("fewer than two runtime lanes are available; heap/exchange entry would be non-operational")

    report = {
        "schema_version": 1,
        "kind": "heap_exchange_runtime_entry",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "stamp": stamp,
        "repo_root": repo_root.as_posix(),
        "task_file": artifact_map["task_file"],
        "context_pack": artifact_map["context_pack"],
        "agent_state": artifact_map["agent_state"],
        "runtime_state": artifact_map["runtime_state"],
        "observer_dir": artifact_map["observer_dir"],
        "source_of_knowledge": "heap_exchange",
        "center_is_dynamic": True,
        "dynamic_exchange_pipeline": True,
        "static_chain_invocation_performed": False,
        "entry_controls_inputs_only": True,
        "exit_must_produce_concrete_product": True,
        "knowledge_surface": knowledge_surface,
        "lanes": lanes,
        "available_lane_count": available_count,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
    }

    write_json_report(report, resolve_output_path(repo_root, output.as_posix()))
    write_text_report(render_markdown(report), resolve_output_path(repo_root, markdown_output.as_posix()))

    append_jsonl(runtime_state, {"kind": "heap_entry", "schema_version": 1, "stamp": stamp, "summary": "heap/exchange runtime entry registered", "entry": rel(repo_root, output)})
    append_jsonl(runtime_state, {"kind": "knowledge_surface_registered", "schema_version": 1, "stamp": stamp, "source_of_knowledge": "heap_exchange", "routing_model": knowledge_surface["routing_model"]})
    for item in lanes:
        append_jsonl(runtime_state, {"kind": "lane_registered", "schema_version": 1, "stamp": stamp, "lane": item["name"], "role": item["role"], "available": item["available"]})
    write_public_event(observer_dir, {"kind": "heap_entry", "stamp": stamp, "summary": f"heap/exchange entry registered with {available_count} available lanes", "source_file": rel(repo_root, output)})

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
