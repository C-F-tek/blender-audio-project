from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

repo_root_for_import = Path(__file__).resolve().parents[2]
if str(repo_root_for_import) not in sys.path:
    sys.path.insert(0, str(repo_root_for_import))

from ia_carmine.runtime.heap_exchange.runtime_entry.cli import (
    append_jsonl,
    build_knowledge_surface,
    build_lanes,
    discover_first,
    load_json,
    rel,
    repo_path,
    write_public_event,
)
from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report


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
        lines.append(
            f"| `{item.get('name')}` | {item.get('role')} | `{item.get('available')}` | {item.get('source')} |"
        )
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
    paths = _resolve_entry_paths(repo_root, args)
    gpu0_report, gpu0_error = load_json(paths["gpu0_report_path"])
    official_report, official_error = load_json(paths["official_report_path"])
    workload_report, workload_error = load_json(paths["workload_report_path"])
    warnings = _input_warnings(
        repo_root,
        (
            ("gpu0_report", paths["gpu0_report_path"], gpu0_error),
            ("official_report", paths["official_report_path"], official_error),
            ("workload_quality_report", paths["workload_report_path"], workload_error),
        ),
    )
    lanes = build_lanes(gpu0_report, official_report, workload_report)
    available_count = sum(1 for item in lanes if item["available"])
    artifact_map = _artifact_map(repo_root, paths)
    knowledge_surface = build_knowledge_surface(lanes, artifact_map)
    errors = _entry_errors(repo_root, paths["task_file"], available_count)
    report = _report(args, repo_root, artifact_map, knowledge_surface, lanes, available_count, errors, warnings)
    _write_outputs(repo_root, paths, report)
    _append_runtime_events(repo_root, args.stamp, paths, report, available_count, lanes, knowledge_surface)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


def _resolve_entry_paths(repo_root: Path, args: argparse.Namespace) -> dict[str, Path | None]:
    stamp = args.stamp
    packets_dir = repo_root / "output" / "ai_packets" / stamp
    return {
        "task_file": repo_path(repo_root, args.task_file),
        "context_pack": repo_path(repo_root, args.context_pack)
        or discover_first(repo_root, [f"output/ai_context_packs/*{stamp}*.json", f"output/ai_context_packs/*{stamp}*.md"]),
        "agent_state": repo_path(repo_root, args.agent_state)
        or discover_first(repo_root, [f"output/ai_packets/{stamp}/*agent_state*.json", f"output/validation/*agent_state*{stamp}*.json"]),
        "gpu0_report_path": repo_path(repo_root, args.gpu0_report)
        or repo_root / f"output/validation/ollama_gpu0_peer_{stamp}.json",
        "official_report_path": repo_path(repo_root, args.official_report)
        or repo_root / f"output/validation/{stamp}_phase_official.json",
        "workload_report_path": repo_path(repo_root, args.workload_quality_report)
        or repo_root / "output/validation/ai_workload_report_quality.json",
        "observer_dir": repo_path(repo_root, args.observer_dir)
        or discover_first(repo_root, [f"output/local_ai_runs/*{stamp}*_observer"]),
        "runtime_state": repo_path(repo_root, args.runtime_state)
        or packets_dir / "heap_exchange_runtime_state.jsonl",
        "output": repo_path(repo_root, args.output) or packets_dir / "heap_exchange_runtime_entry.json",
        "markdown_output": repo_path(repo_root, args.markdown_output)
        or packets_dir / "heap_exchange_runtime_entry.md",
    }


def _input_warnings(repo_root: Path, items: tuple[tuple[str, Path | None, str | None], ...]) -> list[str]:
    warnings = []
    for name, path, error in items:
        if error not in (None, "not provided"):
            warnings.append(f"{name}: {rel(repo_root, path)} {error}")
    return warnings


def _artifact_map(repo_root: Path, paths: dict[str, Path | None]) -> dict[str, str]:
    return {
        "task_file": rel(repo_root, paths["task_file"]),
        "context_pack": rel(repo_root, paths["context_pack"]),
        "agent_state": rel(repo_root, paths["agent_state"]),
        "runtime_state": rel(repo_root, paths["runtime_state"]),
        "observer_dir": rel(repo_root, paths["observer_dir"]),
    }


def _entry_errors(repo_root: Path, task_file: Path | None, available_count: int) -> list[str]:
    errors = []
    if task_file is not None and not task_file.exists():
        errors.append(f"task file missing: {rel(repo_root, task_file)}")
    if available_count < 2:
        errors.append("fewer than two runtime lanes are available; heap/exchange entry would be non-operational")
    return errors


def _report(
    args: argparse.Namespace,
    repo_root: Path,
    artifact_map: dict[str, str],
    knowledge_surface: dict[str, Any],
    lanes: list[dict[str, Any]],
    available_count: int,
    errors: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "kind": "heap_exchange_runtime_entry",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "stamp": args.stamp,
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


def _write_outputs(repo_root: Path, paths: dict[str, Path | None], report: dict[str, Any]) -> None:
    output = paths["output"]
    markdown_output = paths["markdown_output"]
    assert output is not None
    assert markdown_output is not None
    write_json_report(report, resolve_output_path(repo_root, output.as_posix()))
    write_text_report(render_markdown(report), resolve_output_path(repo_root, markdown_output.as_posix()))


def _append_runtime_events(
    repo_root: Path,
    stamp: str,
    paths: dict[str, Path | None],
    report: dict[str, Any],
    available_count: int,
    lanes: list[dict[str, Any]],
    knowledge_surface: dict[str, Any],
) -> None:
    runtime_state = paths["runtime_state"]
    observer_dir = paths["observer_dir"]
    output = paths["output"]
    assert runtime_state is not None
    append_jsonl(runtime_state, {"kind": "heap_entry", "schema_version": 1, "stamp": stamp, "summary": "heap/exchange runtime entry registered", "entry": rel(repo_root, output)})
    append_jsonl(runtime_state, {"kind": "knowledge_surface_registered", "schema_version": 1, "stamp": stamp, "source_of_knowledge": "heap_exchange", "routing_model": knowledge_surface["routing_model"]})
    for item in lanes:
        append_jsonl(runtime_state, {"kind": "lane_registered", "schema_version": 1, "stamp": stamp, "lane": item["name"], "role": item["role"], "available": item["available"]})
    write_public_event(observer_dir, {"kind": "heap_entry", "stamp": stamp, "summary": f"heap/exchange entry registered with {available_count} available lanes", "source_file": rel(repo_root, output)})
