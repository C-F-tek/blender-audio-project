#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""


def exists(repo_root: Path, rel: str) -> bool:
    return (repo_root / rel).exists()


def has(text: str, token: str) -> bool:
    return token in text


def write_markdown(report: dict[str, Any], output: Path) -> str:
    lines = [
        "# Real Product Runtime Mesh Contract",
        "",
        f"- Passed: `{report.get('passed')}`",
        "",
        "## Mesh capabilities",
        "",
    ]
    for key in report.get("capability_order") or []:
        lines.append(f"- `{key}`: `{report.get(key)}`")
    lines.extend(["", "## Runtime route", ""])
    for item in report.get("runtime_route") or []:
        lines.append(f"- {item}")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in report["warnings"])
    return write_text_report("\n".join(lines) + "\n", output)


def build_report(repo_root: Path) -> dict[str, Any]:
    wrapper = repo_root / "Tools/workflow/run_unified_real_product_pr.ps1"
    launcher = repo_root / "Tools/workflow/run_unified_local_ai_refactor.ps1"
    intrinsic = repo_root / "Tools/validation/check_real_product_intrinsic_capability_contract.py"
    readiness = repo_root / "Tools/validation/check_review_pr_product_readiness.py"
    prepare = repo_root / "Tools/ai/prepare_review_pr.py"

    wrapper_text = read_text(wrapper)
    launcher_text = read_text(launcher)
    intrinsic_text = read_text(intrinsic)
    readiness_text = read_text(readiness)
    prepare_text = read_text(prepare)

    memory_sqlite_text = read_text(repo_root / "Tools/ai/agent_runtime_sqlite_memory.py")
    full_memory_text = read_text(repo_root / "Tools/ai/full0to10_memory_tool.py")
    sqlite_schema_text = read_text(repo_root / "Tools/ai/full0to10_sqlite_memory/schema.py")
    sqlite_search_text = read_text(repo_root / "Tools/ai/full0to10_sqlite_memory/search.py")
    sqlite_ingest_text = read_text(repo_root / "Tools/ai/full0to10_sqlite_memory/ingest.py")
    sqlite_memory_smoke_text = read_text(repo_root / "Tools/validation/run_full0to10_sqlite_memory_smoke.py")
    sqlite_hybrid_smoke_text = read_text(repo_root / "Tools/validation/run_full0to10_sqlite_embedding_hybrid_smoke.py")
    sqlite_fts_surface = "\n".join(
        [
            memory_sqlite_text,
            full_memory_text,
            sqlite_schema_text,
            sqlite_search_text,
            sqlite_ingest_text,
            sqlite_memory_smoke_text,
            sqlite_hybrid_smoke_text,
        ]
    ).lower()
    broker_text = read_text(repo_root / "Tools/ai/agent_runtime_tool_broker.py")
    broker_exec_text = read_text(repo_root / "Tools/ai/agent_runtime_tool_broker_execution.py")
    ollama_probe_text = read_text(repo_root / "Tools/ai/run_ollama_provider_probe.py")
    primary_advisory_text = read_text(repo_root / "Tools/ai/build_workload_quality_lane_routing.py")
    openvino_gpu0_text = read_text(repo_root / "Tools/ai/build_openvino_gpu0_workload_report.py")
    gpu0_companion_text = read_text(repo_root / "Tools/ai/build_gpu0_companion_task_lane.py")
    npu_companion_text = read_text(repo_root / "Tools/ai/build_npu_micro_task_companion_report.py")
    local_provider_probe_text = read_text(repo_root / "Tools/ai/run_local_provider_probe.py")
    hardware_ollama_text = read_text(repo_root / "Tools/ai/full0to10_hardware_capability/ollama.py")
    gpu1_provider_surface = "\n".join([ollama_probe_text, local_provider_probe_text, hardware_ollama_text]).lower()

    checks: dict[str, bool] = {
        "task_md_in": has(wrapper_text, "[string]$TaskFile")
        and has(wrapper_text, '"-TaskFile", $TaskRel')
        and has(launcher_text, "IA-CARMINE-TASK-INGRESS-CONTRACT-BEGIN"),

        "heap_exchange_activation": has(wrapper_text, '"-Mode", "all"')
        and has(launcher_text, "IA-CARMINE-HEAP-EXCHANGE-RUNTIME-ENTRY-ENSURE-BEGIN")
        and has(launcher_text, "IA-CARMINE-HEAP-EXCHANGE-PRE-REVIEW-BRIDGE-BEGIN"),

        "gpu1_primary_advisory": has(wrapper_text, "-UsePrimaryAdvisoryProvider")
        and has(wrapper_text, "-UseOllamaAdvisory")
        and has(wrapper_text, "-RunOllamaProbe")
        and (
            exists(repo_root, "Tools/ai/run_ollama_provider_probe.py")
            or exists(repo_root, "Tools/ai/run_local_provider_probe.py")
            or exists(repo_root, "Tools/ai/full0to10_hardware_capability/ollama.py")
        )
        and exists(repo_root, "Tools/ai/build_workload_quality_lane_routing.py")
        and (
            "ollama" in gpu1_provider_surface
            or "provider" in gpu1_provider_surface
            or "probe" in gpu1_provider_surface
        )
        and ("primary" in primary_advisory_text.lower() or "advisory" in primary_advisory_text.lower()),

        "gpu0_openvino_tool_workload": has(wrapper_text, "-RunOpenVinoGpu0Workload")
        and exists(repo_root, "Tools/ai/build_openvino_gpu0_workload_report.py")
        and exists(repo_root, "Tools/ai/build_gpu0_companion_task_lane.py")
        and ("openvino" in openvino_gpu0_text.lower())
        and ("gpu0" in openvino_gpu0_text.lower() or "gpu.0" in openvino_gpu0_text.lower())
        and ("companion" in gpu0_companion_text.lower()),

        "npu_peer_micro_lane": has(wrapper_text, '[string]$NpuMicroStartMode = "peer"')
        and has(wrapper_text, "-NpuMicroStartMode")
        and has(wrapper_text, "-RunNpuProbe")
        and has(wrapper_text, "-RunNpuDecodeSmoke")
        and exists(repo_root, "Tools/ai/build_npu_micro_task_companion_report.py")
        and ("npu" in npu_companion_text.lower())
        and ("peer" in wrapper_text.lower()),

        "shared_memory_evidence": has(wrapper_text, "-SaveInputsToMemoryDb")
        and has(wrapper_text, "-BuildEvidence")
        and has(launcher_text, "shared_memory_evidence")
        and exists(repo_root, "Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py")
        and exists(repo_root, "Tools/ai/build_heap_peer_runtime_manifest.py"),

        "sqlite_fts_memory": exists(repo_root, "Tools/ai/agent_runtime_sqlite_memory.py")
        and exists(repo_root, "Tools/ai/full0to10_memory_tool.py")
        and exists(repo_root, "Tools/ai/full0to10_sqlite_memory/schema.py")
        and exists(repo_root, "Tools/ai/full0to10_sqlite_memory/search.py")
        and exists(repo_root, "Tools/ai/full0to10_sqlite_memory/ingest.py")
        and ("fts5" in sqlite_fts_surface or "full0to10_sqlite_memory" in sqlite_fts_surface)
        and exists(repo_root, "Tools/validation/run_full0to10_sqlite_memory_smoke.py")
        and exists(repo_root, "Tools/validation/run_full0to10_sqlite_embedding_hybrid_smoke.py"),

        "tool_agnostic_broker": exists(repo_root, "Tools/ai/agent_runtime_tool_broker.py")
        and exists(repo_root, "Tools/ai/agent_runtime_tool_broker_execution.py")
        and ("broker" in broker_text.lower())
        and ("execute" in broker_exec_text.lower() or "tool" in broker_exec_text.lower())
        and exists(repo_root, "Tools/validation/run_agent_runtime_tool_broker_smoke.py")
        and exists(repo_root, "Tools/ai/build_runtime_tool_capability_manifest.py")
        and exists(repo_root, "Tools/ai/build_runtime_tool_usage_telemetry.py"),

        "direct_reasoning_assistance": exists(repo_root, "Tools/ai/runtime_tool_guidance.py")
        and exists(repo_root, "Tools/ai/provider_runtime_heap_broker_bridge.py")
        and exists(repo_root, "Tools/ai/provider_runtime_heap_live_signals.py")
        and exists(repo_root, "Tools/ai/build_provider_runtime_heap_telemetry.py"),

        "static_deterministic_script_lane": has(wrapper_text, "-GeneratePatchSpecs")
        and has(wrapper_text, "-BuildTaskPatchSuggestionReport")
        and has(wrapper_text, "-ReviewPrApplyDeterministicSuggestions")
        and exists(repo_root, "Tools/ai/build_deterministic_recommendations.py")
        and exists(repo_root, "Tools/ai/build_patch_specs_from_proposals.py"),

        "heap_exchange_close": has(launcher_text, "IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-BEGIN")
        and has(launcher_text, "IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-AFTER-PATCH-SUGGESTION-BEGIN")
        and has(launcher_text, "IA-CARMINE-HEAP-EXCHANGE-LIFECYCLE-GATE-END")
        and exists(repo_root, "Tools/ai/build_heap_exchange_runtime_exit.py")
        and exists(repo_root, "Tools/validation/check_heap_exchange_runtime_lifecycle.py"),

        "product_readiness": has(launcher_text, "review_pr_product_readiness")
        and has(readiness_text, "prepare_review_pr_ready")
        and has(readiness_text, "has_concrete_product"),

        "prepare_review_pr_product": has(launcher_text, "Tools/ai/build_review_pr_prepare_args.py")
        and has(launcher_text, "Prepare review branch and PR")
        and has(prepare_text, "gh")
        and has(prepare_text, "pr")
        and has(prepare_text, "create"),

        "final_testable_pr": has(wrapper_text, "-ReviewPrPush")
        and has(wrapper_text, "-ReviewPrCreate")
        and has(wrapper_text, "-ReviewPrDraft")
        and has(prepare_text, "--create-pr")
        and has(prepare_text, "--draft-pr"),

        "intrinsic_contract_present": exists(repo_root, "Tools/validation/check_real_product_intrinsic_capability_contract.py")
        and has(intrinsic_text, "real_product_intrinsic_capability_contract"),
    }

    capability_order = [
        "task_md_in",
        "heap_exchange_activation",
        "gpu1_primary_advisory",
        "gpu0_openvino_tool_workload",
        "npu_peer_micro_lane",
        "shared_memory_evidence",
        "sqlite_fts_memory",
        "tool_agnostic_broker",
        "direct_reasoning_assistance",
        "static_deterministic_script_lane",
        "heap_exchange_close",
        "product_readiness",
        "prepare_review_pr_product",
        "final_testable_pr",
        "intrinsic_contract_present",
    ]

    runtime_route = [
        "Task MD IN",
        "heap/exchange activation",
        "GPU1 primary advisory",
        "GPU0 OpenVINO/tool workload",
        "NPU peer micro lane",
        "shared memory / SQLite FTS / tool broker / direct reasoning assistance",
        "static deterministic script/product lane",
        "heap/exchange CLOSE",
        "product readiness",
        "prepare_review_pr.py",
        "PR finale testabile",
    ]

    errors = [f"missing runtime mesh capability: {name}" for name in capability_order if not checks.get(name)]
    failed_capabilities = [name for name in capability_order if not checks.get(name)]

    return {
        "schema_version": 1,
        "kind": "real_product_runtime_mesh_contract",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "capability_order": capability_order,
        "failed_capabilities": failed_capabilities,
        "runtime_route": runtime_route,
        "diagnostics": {
            "sqlite_fts_surface_has_fts5": "fts5" in sqlite_fts_surface,
            "sqlite_fts_surface_has_package": "full0to10_sqlite_memory" in sqlite_fts_surface,
            "sqlite_schema_present": exists(repo_root, "Tools/ai/full0to10_sqlite_memory/schema.py"),
            "sqlite_search_present": exists(repo_root, "Tools/ai/full0to10_sqlite_memory/search.py"),
            "sqlite_ingest_present": exists(repo_root, "Tools/ai/full0to10_sqlite_memory/ingest.py"),
            "ollama_probe_file_present": exists(repo_root, "Tools/ai/run_ollama_provider_probe.py"),
            "local_provider_probe_file_present": exists(repo_root, "Tools/ai/run_local_provider_probe.py"),
            "hardware_ollama_file_present": exists(repo_root, "Tools/ai/full0to10_hardware_capability/ollama.py"),
            "gpu1_provider_surface_mentions_ollama": "ollama" in gpu1_provider_surface,
            "gpu1_provider_surface_mentions_provider_or_probe": "provider" in gpu1_provider_surface or "probe" in gpu1_provider_surface,
            "ollama_probe_path_declares_ollama": "ollama" in "Tools/ai/run_ollama_provider_probe.py".lower(),
            "ollama_probe_mentions_ollama": "ollama" in ollama_probe_text.lower(),
            "ollama_probe_mentions_provider_or_probe": "provider" in ollama_probe_text.lower() or "probe" in ollama_probe_text.lower(),
            "openvino_gpu0_mentions_openvino": "openvino" in openvino_gpu0_text.lower(),
            "openvino_gpu0_mentions_gpu0": "gpu0" in openvino_gpu0_text.lower() or "gpu.0" in openvino_gpu0_text.lower(),
            "npu_companion_mentions_npu": "npu" in npu_companion_text.lower(),
        },
        **checks,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "passed": not errors,
        "errors": errors,
        "warnings": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/real_product_runtime_mesh_contract.json")
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    output = resolve_output_path(repo_root, args.output)
    write_json_report(report, output)
    if args.markdown_output:
        write_markdown(report, resolve_output_path(repo_root, args.markdown_output))
    print(write_json_report(report), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
