"""Static contract checks for heap runtime completeness wiring."""

from __future__ import annotations

from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""


def validate_contract_only(repo_root: Path) -> list[str]:
    files = {
        "gate": read_text(repo_root / "Tools/ai/heap_runtime/completeness_gate/cli.py"),
        "run_loop": read_text(repo_root / "Tools/ai/heap_gate/run_loop.py"),
        "provider_commands": "\n".join(
            (
                read_text(repo_root / "Tools/ai/heap_gate/provider_commands.py"),
                read_text(repo_root / "Tools/ai/heap_gate/provider_command_specs.py"),
                read_text(repo_root / "Tools/ai/heap_gate/provider_time.py"),
            )
        ),
        "provider_execution": read_text(repo_root / "Tools/ai/heap_gate/provider_execution.py"),
        "provider_absorption": read_text(repo_root / "Tools/ai/heap_gate/provider_report_absorption.py"),
        "startup_context": read_text(repo_root / "Tools/ai/heap_gate/startup_context.py"),
        "startup_manifest": read_text(repo_root / "Tools/ai/heap_gate/startup_manifest_context.py"),
        "matrix_lab": read_text(repo_root / "Tools/ai/heap_gate/matrix_lab.py"),
    }
    checks = {
        "startup_manifest_cli": "--startup-manifest" in files["gate"],
        "startup_manifest_primary": "compact_manifest_context" in files["startup_context"],
        "startup_md_reference_only": "artifact_reference_only_not_ingested"
        in files["startup_manifest"],
        "gpu1_lane": '"lane": "gpu1_planner"' in files["provider_commands"],
        "gpu0_lane": '"lane": "gpu0_peer"' in files["provider_commands"],
        "npu_lane": '"lane": "npu_micro_task_auditor"' in files["provider_commands"],
        "concurrent_provider_teamwork": "concurrent_provider_teamwork"
        in files["provider_execution"],
        "provider_launch_manifest": "provider_launch_manifest" in files["provider_execution"],
        "provider_process_evidence": "provider_process_id" in files["provider_absorption"]
        and "started_at" in files["provider_absorption"],
        "provider_required_when_enabled": "provider_teamwork_universe_required"
        in files["run_loop"],
        "matrix_consumes_evidence": "evidence_report" in files["matrix_lab"],
    }
    return [
        f"missing heap runtime completeness contract: {key}"
        for key, ok in checks.items()
        if not ok
    ]
