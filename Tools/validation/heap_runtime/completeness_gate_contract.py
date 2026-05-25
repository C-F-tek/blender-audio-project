"""Static contract checks for heap runtime completeness wiring."""

from __future__ import annotations

from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""


def has_lane_spec(text: str, lane: str, constant: str) -> bool:
    return f'"lane": "{lane}"' in text or f'"lane": {constant}' in text


def validate_contract_only(repo_root: Path) -> list[str]:
    files = {
        "gate": read_text(repo_root / "ia_carmine/runtime/heap_runtime/completeness_gate/cli.py"),
        "run_loop": read_text(repo_root / "ia_carmine/runtime/heap_gate/run_loop.py"),
        "provider_commands": "\n".join(
            (
                read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_commands.py"),
                read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_command_specs.py"),
                read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_time.py"),
            )
        ),
        "provider_execution": read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_execution.py"),
        "provider_absorption": read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_report_absorption.py"),
        "gpu1_one_turn_gate": read_text(repo_root / "ia_carmine/runtime/heap_gate/gpu1_one_turn_gate.py"),
        "gpu1_chat_loop": read_text(repo_root / "ia_carmine/runtime/heap_gate/gpu1_native_tool_chat_loop.py"),
        "run_loop_metrics": "\n".join(
            (
                read_text(repo_root / "ia_carmine/runtime/heap_gate/run_loop_metrics.py"),
                read_text(repo_root / "ia_carmine/runtime/heap_gate/run_loop_metric_helpers.py"),
            )
        ),
        "terminal_invariants": read_text(repo_root / "ia_carmine/runtime/heap_gate/terminal_invariants.py"),
        "provider_selection": read_text(repo_root / "ia_carmine/_shared/ollama_provider_selection.py"),
        "ollama_config": read_text(repo_root / "ia_carmine/providers/ollama/config.py"),
        "startup_context": read_text(repo_root / "ia_carmine/runtime/heap_gate/startup_context.py"),
        "startup_manifest": read_text(repo_root / "ia_carmine/runtime/heap_gate/startup_manifest_context.py"),
        "matrix_lab": read_text(repo_root / "ia_carmine/runtime/heap_gate/matrix_lab.py"),
    }
    checks = {
        "startup_manifest_cli": "--startup-manifest" in files["gate"],
        "startup_manifest_primary": "compact_manifest_context" in files["startup_context"],
        "startup_md_reference_only": "artifact_reference_only_not_ingested"
        in files["startup_manifest"],
        "gpu1_lane": has_lane_spec(files["provider_commands"], "gpu1_planner", "GPU1_LANE"),
        "gpu0_lane": has_lane_spec(files["provider_commands"], "gpu0_peer", "GPU0_LANE"),
        "npu_lane": has_lane_spec(
            files["provider_commands"], "npu_micro_task_auditor", "NPU_LANE"
        ),
        "concurrent_provider_teamwork": (
            "concurrent_provider_teamwork" in files["provider_execution"]
            or "production_provider_window_all_lanes_started_before_residency_result"
            in files["provider_execution"]
            or "provider_teamwork_unified_parallel" in files["provider_execution"]
        ),
        "provider_launch_manifest": "provider_launch_manifest" in files["provider_execution"],
        "provider_process_evidence": "provider_process_id" in files["provider_absorption"]
        and "started_at" in files["provider_absorption"],
        "provider_required_when_enabled": "provider_teamwork_universe_required"
        in files["run_loop"],
        "matrix_consumes_evidence": "evidence_report" in files["matrix_lab"],
        "gpu1_one_turn_helper_exists": "kind = gpu1_one_turn_runtime_gate"
        in files["gpu1_one_turn_gate"]
        or "GATE_KIND = \"gpu1_one_turn_runtime_gate\"" in files["gpu1_one_turn_gate"],
        "gpu1_chat_loop_calls_one_turn_helper": "build_gpu1_one_turn_runtime_gate"
        in files["gpu1_chat_loop"],
        "provider_execution_blocks_sidecars_on_one_turn": "skipped_gpu1_one_turn_gate_failed"
        in files["provider_execution"],
        "run_loop_metrics_exposes_one_turn": "gpu1_one_turn_runtime_gate_passed"
        in files["run_loop_metrics"],
        "terminal_invariants_block_one_turn_missing": "gpu1_one_turn_runtime_gate_missing_or_failed"
        in files["terminal_invariants"],
        "no_runtime_preflight_import": "Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight"
        not in "\n".join(files.values()),
        "explicit_provider_model_exact_policy": "explicit_provider_model_exact"
        in files["provider_selection"]
        and "provider_model_explicit_required" in files["provider_selection"],
        "provider_selection_no_hardcoded_fallback": "FALLBACK_ORDER"
        not in files["provider_selection"]
        and "qwen2.5-coder:14b" not in files["provider_selection"]
        and "qwen2.5-coder:14b" not in files["ollama_config"],
    }
    return [
        f"missing heap runtime completeness contract: {key}"
        for key, ok in checks.items()
        if not ok
    ]
