"""Support helpers for the Python full-toolbox decision-loop engine."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def rel(path: str | Path) -> str:
    return str(path).replace("/", "\\")


def read_json(path: str | Path) -> dict[str, Any] | None:
    target = Path(path)
    if not target.exists():
        return None
    try:
        data = json.loads(target.read_text(encoding="utf-8-sig"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: str | Path, lines: list[str]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def add_existing(items: list[str], path: str | Path | None) -> None:
    if path and Path(path).exists():
        value = str(path)
        if value not in items:
            items.append(value)


def git_output(repo_root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=repo_root, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def compact_artifact_stamp(stamp: str, max_chars: int = 56) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", stamp.strip() or "run").strip("._-")
    if len(safe) <= max_chars:
        return safe
    digest = hashlib.sha1(safe.encode("utf-8")).hexdigest()[:10]
    head = safe[: max(12, max_chars - len(digest) - 1)].rstrip("._-")
    return f"{head}-{digest}"


def is_windowsapps_python(path_value: str) -> bool:
    normalized = str(path_value).replace("\\", "/").lower()
    return "/windowsapps/" in normalized and "python" in Path(path_value).name.lower()


def normalize_python_candidate(path_value: str) -> str:
    candidate = Path(path_value)
    try:
        if candidate.is_file():
            return str(candidate.resolve())
    except OSError:
        return ""
    return ""


def resolve_python(repo_root: Path) -> str:
    env_python = os.environ.get("IA_CARMINE_PYTHON", "")
    candidates = [
        env_python,
        str(repo_root / ".venv/Scripts/python.exe"),
        str(repo_root / "venv/Scripts/python.exe"),
        str(repo_root / ".venv314/Scripts/python.exe"),
    ]

    current = normalize_python_candidate(sys.executable)
    if current and not is_windowsapps_python(current):
        candidates.append(current)

    for raw in candidates:
        if not raw:
            continue
        normalized = normalize_python_candidate(raw)
        if normalized:
            return normalized

    if sys.executable and not is_windowsapps_python(sys.executable):
        return sys.executable
    return "python"


@dataclass
class WorkflowContext:
    args: Any
    repo_root: Path
    python_exe: str
    paths: dict[str, str]
    reports: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def p(self, key: str) -> str:
        return self.paths[key]

    def run(self, label: str, command: list[str], *, timeout: int | None = None) -> int:
        print()
        print(f"=== {label} ===")
        env = os.environ.copy()
        env["IA_CARMINE_PYTHON"] = self.python_exe
        env["PYTHONPATH"] = str(self.repo_root)
        python_path = Path(self.python_exe)
        if python_path.is_file():
            python_dir = str(python_path.resolve().parent)
            env["PATH"] = python_dir + os.pathsep + env.get("PATH", "")
        completed = subprocess.run(command, cwd=self.repo_root, timeout=timeout, env=env)
        if completed.returncode != 0:
            self.warnings.append(f"{label} failed with exit code {completed.returncode}")
        return int(completed.returncode or 0)

    def run_python(self, label: str, args: list[str], *, timeout: int | None = None) -> int:
        return self.run(label, [self.python_exe, *args], timeout=timeout)

    def run_powershell(self, label: str, script: str, params: dict[str, Any]) -> int:
        # IA-CARMINE-PS-SPLAT-ARRAY-SAFE-BEGIN
        # Use PowerShell splatting syntax for list parameters. Passing a
        # Python list as repeated positional CLI arguments after ``-File`` can
        # make PowerShell bind later paths to unrelated positional parameters
        # such as MaxContextChars. The command string below keeps arrays
        # attached to their named parameter, e.g. ``-ReportFile @('a','b')``.
        def quote_ps(value: Any) -> str:
            return "'" + str(value).replace("'", "''") + "'"

        script_parts: list[str] = ["&", quote_ps(script)]
        for key, value in params.items():
            if isinstance(value, bool):
                if value:
                    script_parts.append(f"-{key}")
                continue

            if isinstance(value, (list, tuple)):
                values = [str(item) for item in value if item is not None and str(item) != ""]
                if values:
                    array_literal = "@(" + ", ".join(quote_ps(item) for item in values) + ")"
                    script_parts.append(f"-{key}")
                    script_parts.append(array_literal)
                continue

            if value is not None:
                script_parts.append(f"-{key}")
                script_parts.append(quote_ps(value))

        command_text = "$ErrorActionPreference = 'Stop'; " + " ".join(script_parts)
        command = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command_text]
        return self.run(label, command)
        # IA-CARMINE-PS-SPLAT-ARRAY-SAFE-END

def build_paths(stamp: str, evidence_dir: str) -> dict[str, str]:
    s = compact_artifact_stamp(stamp)
    p: dict[str, str] = {
        "artifact_stamp": s,
        "evidence": "output/ai_pipeline/agent_review_evidence_sufficiency.json",
        "evidence_md": "output/ai_pipeline/agent_review_evidence_sufficiency.md",
        "refined_review": "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review_v3.json",
        "memory_workflow": f"output/validation/full_memory_tool_regeneration_{s}_workflow.json",
        "memory_bundle_json": f"{evidence_dir}/full_memory_tool_regeneration_bundle_{s}.json",
        "memory_bundle_md": f"{evidence_dir}/full_memory_tool_regeneration_bundle_{s}.md",
        "memory_line_count_csv": f"{evidence_dir}/full_memory_tool_regeneration_python_line_count_{s}.csv",
        "line_count_json": f"output/validation/python_line_count_full_toolbox_{s}.json",
        "line_count_md": f"output/validation/python_line_count_full_toolbox_{s}.md",
        "line_count_all_md": f"output/validation/python_line_count_all_python_files_{s}.md",
        "python_syntax_json": f"output/validation/python_syntax_full_toolbox_{s}.json",
        "code_interpreter_json": f"output/analysis/code_interpreter_full_toolbox_{s}.json",
        "code_interpreter_md": f"output/analysis/code_interpreter_full_toolbox_{s}.md",
        "gpu_contract_smoke_json": f"output/validation/gpu_planner_json_contract_smoke_full_toolbox_{s}.json",
        "gpu_contract_smoke_md": f"output/validation/gpu_planner_json_contract_smoke_full_toolbox_{s}.md",
        "deterministic_smoke_json": f"output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_{s}.json",
        "deterministic_smoke_md": f"output/validation/deterministic_recommendation_synthesizer_smoke_full_toolbox_{s}.md",
        "decision_loop_smoke_json": f"output/validation/agent_review_decision_loop_smoke_full_toolbox_{s}.json",
        "decision_loop_smoke_md": f"output/validation/agent_review_decision_loop_smoke_full_toolbox_{s}.md",
        "npu_env_json": f"output/validation/npu_provider_environment_full_toolbox_{s}.json",
        "npu_env_md": f"output/validation/npu_provider_environment_full_toolbox_{s}.md",
        "openvino_governance_json": f"output/validation/openvino_hardware_governance_full_toolbox_{s}.json",
        "openvino_governance_md": f"output/validation/openvino_hardware_governance_full_toolbox_{s}.md",
        "repo_consistency_json": f"output/analysis/repository_consistency_map_full_toolbox_{s}.json",
        "repo_consistency_md": f"output/analysis/repository_consistency_map_full_toolbox_{s}.md",
        "repo_consistency_smoke_json": f"output/validation/repository_consistency_map_smoke_full_toolbox_{s}.json",
        "repo_consistency_smoke_md": f"output/validation/repository_consistency_map_smoke_full_toolbox_{s}.md",
        "orch_json": f"output/ai_pipeline/full_toolbox_{s}_orchestrator.json",
        "orch_md": f"output/ai_pipeline/full_toolbox_{s}_orchestrator.md",
        "gpu_json": f"output/ai_pipeline/full_toolbox_{s}_parallel_gpu.json",
        "gpu_md": f"output/ai_pipeline/full_toolbox_{s}_parallel_gpu.md",
        "checkpoint_dir": f"output/ai_pipeline/full_toolbox_{s}_checkpoints",
        "gpu_replay_json": f"output/analysis/gpu_json_contract_replay_full_toolbox_{s}.json",
        "gpu_replay_md": f"output/analysis/gpu_json_contract_replay_full_toolbox_{s}.md",
        "gpu_npu_sync_json": f"output/analysis/gpu_npu_run_sync_full_toolbox_{s}.json",
        "gpu_npu_sync_md": f"output/analysis/gpu_npu_run_sync_full_toolbox_{s}.md",
        "provider_contract_json": f"output/validation/provider_evidence_contract_full_toolbox_{s}.json",
        "provider_contract_md": f"output/validation/provider_evidence_contract_full_toolbox_{s}.md",
        "gpu0_companion_json": f"output/validation/gpu0_companion_task_lane_{s}.json",
        "gpu0_companion_md": f"output/validation/gpu0_companion_task_lane_{s}.md",
        "gpu0_companion_tools_json": f"output/validation/gpu0_companion_tool_requests_{s}.json",
        "gpu0_companion_contract_json": f"output/validation/gpu0_companion_contract_{s}.json",
        "gpu0_companion_contract_md": f"output/validation/gpu0_companion_contract_{s}.md",
        "gpu0_support_dir": f"output/ai_pipeline/gpu0_peer_support_parallel_{s}",
        "npu_support_dir": f"output/ai_pipeline/npu_micro_support_parallel_{s}",
        "gpu1_primary_json": f"output/validation/gpu1_primary_advisory_{s}.json",
        "gpu1_primary_md": f"output/validation/gpu1_primary_advisory_{s}.md",
        "gpu0_task_json": f"output/validation/gpu0_peer_task_packet_{s}.json",
        "gpu0_response_json": f"output/validation/gpu0_peer_response_{s}.json",
        "gpu0_response_md": f"output/validation/gpu0_peer_response_{s}.md",
        "gpu0_tools_json": f"output/validation/gpu0_tool_requests_{s}.json",
        "gpu0_broker_json": f"output/validation/gpu0_peer_runtime_tool_broker_{s}.json",
        "gpu0_broker_md": f"output/validation/gpu0_peer_runtime_tool_broker_{s}.md",
        "npu_micro_json": f"output/validation/npu_micro_peer_assistant_{s}.json",
        "npu_micro_md": f"output/validation/npu_micro_peer_assistant_{s}.md",
        "npu_context_md": f"output/ai_pipeline/npu_micro_peer_assistant_context_{s}.md",
        "npu_output_md": f"output/ai_pipeline/npu_micro_peer_assistant_output_{s}.md",
        "npu_notes_md": f"output/ai_pipeline/npu_micro_peer_assistant_notes_{s}.md",
        "npu_metadata_json": f"output/validation/npu_micro_peer_assistant_metadata_{s}.json",
        "npu_broker_json": f"output/validation/npu_micro_runtime_tool_broker_{s}.json",
        "npu_broker_md": f"output/validation/npu_micro_runtime_tool_broker_{s}.md",
        "peer_json": f"output/validation/ai_peer_exchange_{s}.json",
        "peer_md": f"output/validation/ai_peer_exchange_{s}.md",
        "peer_contract_json": f"output/validation/ai_peer_exchange_contract_{s}.json",
        "peer_contract_md": f"output/validation/ai_peer_exchange_contract_{s}.md",
        "recommendations_json": f"output/ai_pipeline/full_toolbox_{s}_deterministic_recommendations.json",
        "recommendations_md": f"output/ai_pipeline/full_toolbox_{s}_deterministic_recommendations.md",
        "bridge_json": f"output/ai_pipeline/full_toolbox_{s}_bridge_orchestrator.json",
        "patch_plan_json": f"output/patch_specs/full_toolbox_{s}_agent_review_patch_plan.json",
        "patch_plan_md": f"output/patch_specs/full_toolbox_{s}_agent_review_patch_plan.md",
        "patch_quality_json": f"{evidence_dir}/patch_plan_quality_product_{s}.json",
        "patch_quality_md": f"{evidence_dir}/patch_plan_quality_product_{s}.md",
        "patch_quality_fts_db": f"output/ai_runtime_memory/patch_plan_quality_product_{s}.sqlite",
        "patch_notes_quality_json": f"{evidence_dir}/patch_notes_quality_product_{s}.json",
        "patch_notes_quality_md": f"{evidence_dir}/patch_notes_quality_product_{s}.md",
        "patch_notes_quality_fts_db": f"output/ai_runtime_memory/patch_notes_quality_product_{s}.sqlite",
        "decision_json": f"output/ai_pipeline/full_toolbox_{s}_agent_review_decision_loop.json",
        "decision_md": f"output/ai_pipeline/full_toolbox_{s}_agent_review_decision_loop.md",
    }
    add_runtime_paths(p, s, evidence_dir)
    return p


def add_runtime_paths(p: dict[str, str], stamp: str, evidence_dir: str) -> None:
    s = stamp
    bundle_base = f"full_toolbox_agent_review_decision_loop_{s}"
    final_dir = f"output/validation/full0to10_final_tool_product_{s}"
    chunk_base = f"full_toolbox_{s}_cloud_semantic_deterministic"
    p.update(
        {
            "bundle_base": bundle_base,
            "bundle_json": f"{evidence_dir}/{bundle_base}.json",
            "bundle_md": f"{evidence_dir}/{bundle_base}.md",
            "bundle_validation_json": f"output/validation/full_toolbox_agent_review_decision_loop_{s}_bundle_validation.json",
            "final_python_syntax_json": f"output/validation/python_syntax_full_toolbox_final_{s}.json",
            "final_contract_json": f"output/validation/validation_report_contract_full_toolbox_final_{s}.json",
            "artifact_path_policy_json": f"{evidence_dir}/generated_artifact_path_policy_full_toolbox_{s}.json",
            "artifact_path_policy_md": f"{evidence_dir}/generated_artifact_path_policy_full_toolbox_{s}.md",
            "workflow_json": f"output/validation/agent_review_full_toolbox_decision_loop_{s}_workflow.json",
            "workflow_md": f"output/validation/agent_review_full_toolbox_decision_loop_{s}_workflow.md",
            "telemetry_json": f"{evidence_dir}/full_toolbox_run_telemetry_summary_{s}.json",
            "telemetry_md": f"{evidence_dir}/full_toolbox_run_telemetry_summary_{s}.md",
            "runtime_usage_json": f"{evidence_dir}/runtime_tool_usage_telemetry_{s}.json",
            "runtime_usage_md": f"{evidence_dir}/runtime_tool_usage_telemetry_{s}.md",
            "runtime_capability_json": f"{evidence_dir}/runtime_tool_capability_manifest_{s}.json",
            "runtime_capability_md": f"{evidence_dir}/runtime_tool_capability_manifest_{s}.md",
            "runtime_bootstrap_json": f"output/validation/runtime_tool_bootstrap_requests_{s}.json",
            "runtime_broker_json": f"output/validation/runtime_tool_broker_full_toolbox_{s}.json",
            "runtime_broker_md": f"output/validation/runtime_tool_broker_full_toolbox_{s}.md",
            "runtime_tool_dir": f"output/ai_runtime_tools/{s}",
            "heap_events": f"output/ai_runtime_heap/{s}/events.jsonl",
            "heap_snapshot_json": f"output/ai_runtime_heap/{s}/snapshot.json",
            "heap_snapshot_md": f"output/ai_runtime_heap/{s}/snapshot.md",
            "heap_from_peer_json": f"output/validation/provider_runtime_heap_from_peer_reports_{s}.json",
            "heap_from_peer_md": f"output/validation/provider_runtime_heap_from_peer_reports_{s}.md",
            "heap_telemetry_json": f"{evidence_dir}/provider_runtime_heap_telemetry_{s}.json",
            "heap_telemetry_md": f"{evidence_dir}/provider_runtime_heap_telemetry_{s}.md",
            "heap_init_json": f"output/validation/provider_runtime_heap_live_signals_init_{s}.json",
            "heap_init_md": f"output/validation/provider_runtime_heap_live_signals_init_{s}.md",
            "heap_gpu1_request_json": f"output/validation/provider_runtime_heap_live_signals_gpu1_request_{s}.json",
            "heap_gpu1_request_md": f"output/validation/provider_runtime_heap_live_signals_gpu1_request_{s}.md",
            "heap_broker_json": f"output/validation/provider_runtime_heap_live_signals_broker_results_{s}.json",
            "heap_broker_md": f"output/validation/provider_runtime_heap_live_signals_broker_results_{s}.md",
            "heap_npu_json": f"output/validation/provider_runtime_heap_live_signals_npu_support_{s}.json",
            "heap_npu_md": f"output/validation/provider_runtime_heap_live_signals_npu_support_{s}.md",
            "heap_catalog_json": f"output/validation/provider_runtime_heap_live_signals_tool_catalog_complete_{s}.json",
            "heap_catalog_md": f"output/validation/provider_runtime_heap_live_signals_tool_catalog_complete_{s}.md",
            "final_product_dir": final_dir,
            "final_product_json": f"output/validation/full0to10_final_tool_product_{s}.json",
            "final_product_manifest": f"{final_dir}/full0to10_final_tool_product_manifest.json",
            "final_product_md": f"{final_dir}/full0to10_final_tool_product.md",
            "final_product_evidence": f"{final_dir}/full0to10_final_tool_product_evidence_index.json",
            "final_product_readiness": f"{final_dir}/full0to10_final_tool_product_readiness.json",
            "final_product_readme": f"{final_dir}/README.md",
            "chunk_base": chunk_base,
            "chunk_dir": f"{evidence_dir}/{chunk_base}_chunks",
            "chunk_manifest_json": f"{evidence_dir}/{chunk_base}_chunk_manifest.json",
            "chunk_manifest_md": f"{evidence_dir}/{chunk_base}_chunk_manifest.md",
            "chunk_zip": f"output/validation/{chunk_base}_chunks.zip",
        }
    )
    p["gpu0_support_bootstrap"] = f"{p['gpu0_support_dir']}/round_000_gpu0_peer_support.json"
    p["npu_support_bootstrap"] = f"{p['npu_support_dir']}/round_000_npu_micro_support.json"


def write_line_inventory(csv_path: str, output_md: str, stamp: str) -> None:
    rows: list[dict[str, str]] = []
    with Path(csv_path).open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    rows.sort(key=lambda row: int(row.get("Lines") or 0), reverse=True)
    total = sum(int(row.get("Lines") or 0) for row in rows)
    lines = [
        "# Full Python Line Count Inventory",
        "",
        f"- Stamp: {stamp}",
        f"- CSV: {csv_path}",
        f"- File count: {len(rows)}",
        f"- Total Python lines: {total}",
        "- Visibility rule: all counted Python files are listed below; do not truncate to top 10/top 20.",
        "",
        "| Lines | File |",
        "|---:|---|",
    ]
    lines.extend(f"| {row.get('Lines')} | `{row.get('File')}` |" for row in rows)
    write_text(output_md, lines)
