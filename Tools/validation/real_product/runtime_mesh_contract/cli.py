#!/usr/bin/env python3
"""Validate the canonical runtime mesh behind ``python -m ia_carmine.cli run``."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""


def exists(repo_root: Path, rel: str) -> bool:
    return (repo_root / rel).exists()


def has(text: str, token: str) -> bool:
    return token in text


def ordered_tokens(text: str, *tokens: str) -> bool:
    positions = [text.find(token) for token in tokens]
    return all(position >= 0 for position in positions) and positions == sorted(positions)


def ordered_lane_specs(text: str) -> bool:
    return ordered_tokens(
        text,
        '"lane": "gpu1_planner"',
        '"lane": "gpu0_peer"',
        '"lane": "npu_micro_task_auditor"',
    ) or ordered_tokens(
        text,
        '"lane": GPU1_LANE',
        '"lane": GPU0_LANE',
        '"lane": NPU_LANE',
    )


def write_markdown(report: dict[str, Any], output: Path) -> str:
    lines = ["# Real Product Runtime Mesh Contract", "", f"- Passed: `{report.get('passed')}`", ""]
    for key in report.get("capability_order") or []:
        lines.append(f"- `{key}`: `{report.get(key)}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    return write_text_report("\n".join(lines) + "\n", output)


def build_report(repo_root: Path) -> dict[str, Any]:
    dispatch = read_text(repo_root / "ia_carmine/dispatch.py")
    run_cli = read_text(repo_root / "ia_carmine/runtime/run/cli.py")
    profiles = read_text(repo_root / "ia_carmine/runtime/run/profiles/heap_runtime_launcher_profiles.json")
    profile_builder = read_text(repo_root / "ia_carmine/product/operator_product_core/profiles.py")
    runner = read_text(repo_root / "ia_carmine/product/operator_product_core/runner.py")
    heap_gate = read_text(repo_root / "ia_carmine/runtime/heap_runtime/completeness_gate/cli.py")
    heap_run_loop = read_text(repo_root / "ia_carmine/runtime/heap_gate/run_loop.py")
    heap_run_loop_metrics = read_text(repo_root / "ia_carmine/runtime/heap_gate/run_loop_metrics.py")
    budget = read_text(repo_root / "ia_carmine/runtime/heap_provider/budget_governor/cli.py")
    invocation = read_text(repo_root / "ia_carmine/runtime/heap_provider/invocation_contract/cli.py")
    product_package = read_text(repo_root / "ia_carmine/runtime/heap_runtime/product_package/cli.py")
    broker_registry = read_text(repo_root / "ia_carmine/runtime/runtime_tool/broker/registry.py")
    broker_builders = read_text(repo_root / "ia_carmine/runtime/runtime_tool/broker/runtime_builders.py")
    broker_bridge = read_text(repo_root / "ia_carmine/runtime/provider_runtime_blackboard/broker_bridge/cli.py")
    memory = read_text(repo_root / "ia_carmine/memory/agent_memory/sqlite_cli.py")
    flow_map = read_text(repo_root / "ia_carmine/runtime/runtime_universe/flow_map/cli.py")
    matrix = read_text(repo_root / "ia_carmine/runtime/heap_gate/matrix_lab.py")
    matrix_evidence = read_text(repo_root / "ia_carmine/runtime/heap_gate/matrix_lab_evidence.py")
    matrix_tool = read_text(repo_root / "ia_carmine/runtime/heap_runtime/code_execution_tool/cli.py")
    synthesis = read_text(repo_root / "ia_carmine/product/patch_product/candidate_synthesis/cli.py")
    synthesis_evidence = read_text(
        repo_root / "ia_carmine/product/patch_product/candidate_synthesis/evidence_diff.py"
    )
    final_product = read_text(repo_root / "ia_carmine/_shared/heap_final_code_product.py")
    final_readable_product = read_text(repo_root / "ia_carmine/product/code_product/final_readable_product/cli.py")
    provider_loop = read_text(repo_root / "ia_carmine/_shared/provider_tool_loop.py")
    provider_commands = "\n".join(
        (
            read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_commands.py"),
            read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_command_specs.py"),
            read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_time.py"),
        )
    )
    provider_execution = read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_execution.py")
    provider_absorption = read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_report_absorption.py")
    provider_collection = read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_process_collection.py")
    provider_runtime = "\n".join((provider_execution, provider_absorption, provider_collection))
    provider_teamwork_packet = read_text(repo_root / "ia_carmine/runtime/heap_gate/provider_teamwork_packet.py")
    heap_context_launcher = read_text(repo_root / "ia_carmine/runtime/heap_context_closure/launcher.py")
    startup_context = read_text(repo_root / "ia_carmine/runtime/heap_gate/startup_context.py")
    startup_manifest_context = read_text(
        repo_root / "ia_carmine/runtime/heap_gate/startup_manifest_context.py"
    )

    checks: dict[str, bool] = {
        "task_md_in": has(run_cli, "--request-file") and has(profile_builder, "--request-file"),
        "heap_exchange_activation": has(profile_builder, "heap_context_closure")
        and has(profiles, "universe_roles")
        and has(profiles, "block_pointer_protocol"),
        "heap_provider_budget_governor": exists(repo_root, "ia_carmine/runtime/heap_provider/budget_governor/cli.py")
        and has(budget, "ProviderBudgetConfig")
        and has(budget, "provider_lanes"),
        "heap_provider_invocation_contract": exists(
            repo_root, "ia_carmine/runtime/heap_provider/invocation_contract/cli.py"
        )
        and has(invocation, "expected_evidence_event_contract")
        and has(invocation, "broker_request"),
        "gpu1_primary_advisory": has(profiles, "gpu1_planner")
        and has(provider_loop, "GPU1 HEAP PARTICIPATION MODE"),
        "gpu0_ollama_vulkan_tool_workload": has(profiles, "gpu0_reviewer_refiner")
        and has(provider_commands, "build_ollama_gpu0_peer_report")
        and has(provider_commands, "ollama_gpu0_vulkan_required_openvino_gpu0_forbidden"),
        "npu_peer_micro_lane": has(profiles, "npu_auditor")
        and has(provider_loop, "IA_CARMINE_NPU_MODEL_DIR"),
        "shared_memory_evidence": exists(repo_root, "ia_carmine/context/agent_context/shared_toolbox_bundle/cli.py")
        and exists(repo_root, "ia_carmine/context/agent_context/semantic_evidence_chunks/cli.py"),
        "sqlite_runtime_memory": exists(repo_root, "ia_carmine/memory/agent_memory/sqlite_cli.py")
        and "sqlite" in memory.lower(),
        "tool_agnostic_broker": "synthesize_patch_candidates" in broker_registry
        and "run_heap_code_execution_matrix" in broker_registry,
        "direct_reasoning_assistance": exists(repo_root, "ia_carmine/_shared/runtime_tool_guidance.py")
        and has(broker_bridge, "provider_runtime_broker_bridge"),
        "runtime_flow_map_evidence": exists(repo_root, "ia_carmine/runtime/runtime_universe/flow_map/cli.py")
        and has(flow_map, "ia_carmine_runtime_flow_build"),
        "static_deterministic_script_lane": has(matrix, "code_execution_matrix_targets")
        and has(matrix_evidence, "code_execution_matrix_metric_count"),
        "matrix_consumes_provider_diff_evidence": has(matrix, "evidence_report")
        and has(broker_registry, "evidence_report")
        and has(broker_builders, "--evidence-report")
        and has(matrix_tool, "--evidence-report")
        and has(synthesis, "build_evidence_candidates")
        and has(synthesis_evidence, "diff --git")
        and has(synthesis_evidence, "git apply")
        and has(synthesis_evidence, "missing_from_verified"),
        "heap_exchange_close": has(runner, "operator_product_launcher_run.json")
        and has(runner, "operator_product_lab_summary.json"),
        "heap_runtime_completeness_gate": has(heap_run_loop, "provider_teamwork_universe_required")
        and has(heap_run_loop, "gpu1_provider_planner")
        and has(heap_run_loop, "gpu0_provider_peer")
        and has(heap_run_loop, "npu_micro_task_auditor")
        and has(heap_gate, "HeapRuntimeCompletenessGate"),
        "startup_manifest_primary_data_plane": has(heap_context_launcher, "--startup-manifest")
        and has(heap_gate, "--startup-manifest")
        and has(startup_context, "compact_manifest_context")
        and has(startup_manifest_context, "artifact_reference_only_not_ingested")
        and has(provider_commands, "--startup-manifest"),
        "heap_runtime_product_package": exists(repo_root, "ia_carmine/runtime/heap_runtime/product_package/cli.py")
        and has(product_package, "heap_runtime_product_package"),
        "product_readiness": has(runner, "launcher_passed")
        and has(runner, "code_product_metrics")
        and has(final_product, "render_code_product_section")
        and has(final_readable_product, "real_code_product_ready")
        and has(final_readable_product, "final_product_blockers")
        and has(final_readable_product, "truncation_marker"),
        "prepare_review_pr_product": '"agent_review_prepare_pr"' in dispatch,
        "final_testable_pr": has(runner, "code_product_metrics") and has(runner, "review_report"),
        "intrinsic_contract_present": exists(
            repo_root, "Tools/validation/real_product/intrinsic_capability_contract/cli.py"
        ),
        "openvino_peer_topology_contract": exists(
            repo_root, "Tools/validation/provider_mesh/openvino_peer_topology_contract/cli.py"
        ),
        "gpu0_npu_provider_contract": exists(
            repo_root, "Tools/validation/provider_mesh/openvino_peer_topology_contract/cli.py"
        )
        and has(provider_commands, "build_ollama_gpu0_peer_report")
        and has(provider_commands, "build_npu_micro_task_companion_report")
        and ordered_lane_specs(provider_commands)
        and has(provider_commands, "--require-ollama-gpu-residency")
        and has(provider_commands, "--leader-packet")
        and has(provider_absorption, "provider_work_verified")
        and has(heap_run_loop_metrics, "provider_semantic_missing_required_lanes")
        and has(provider_execution, "provider_launch_manifest")
        and has(provider_execution, "provider_teamwork_leader_packet")
        and has(provider_execution, "build_provider_teamwork_leader_packet")
        and has(provider_teamwork_packet, "gpu1_primary_advisory_leader")
        and has(provider_teamwork_packet, "heap_universe_contract")
        and has(provider_teamwork_packet, "same_heap_teamwork_contract")
        and has(provider_teamwork_packet, "pointer_contract")
        and has(provider_teamwork_packet, "resume_from_block_id")
        and has(provider_teamwork_packet, "gpu1_authority")
        and has(provider_teamwork_packet, "gpu0_peer_authority")
        and has(provider_teamwork_packet, "npu_peer_authority")
        and has(provider_teamwork_packet, "GPU1 commands final synthesis")
        and (
            has(provider_teamwork_packet, "parallel peer")
            or has(provider_teamwork_packet, "unified_parallel_execution")
        )
        and has(provider_teamwork_packet, "requires_concrete_rewrite")
        and has(provider_teamwork_packet, "NO_PATCHABLE_TARGET")
        and has(provider_teamwork_packet, "startup_artifacts")
        and has(provider_teamwork_packet, "broker_tool_evidence")
        and has(provider_teamwork_packet, "source_allowlist_contract")
        and has(provider_teamwork_packet, "startup_context_plane")
        and has(provider_teamwork_packet, "artifact_reference_only_not_runtime_database")
        and has(provider_runtime, "started_at")
        and has(provider_absorption, "provider_process_id")
        and has(provider_runtime, "provider_teamwork_unified_parallel"),
    }
    order = [
        "task_md_in",
        "heap_exchange_activation",
        "heap_provider_budget_governor",
        "heap_provider_invocation_contract",
        "gpu1_primary_advisory",
        "gpu0_ollama_vulkan_tool_workload",
        "npu_peer_micro_lane",
        "shared_memory_evidence",
        "sqlite_runtime_memory",
        "tool_agnostic_broker",
        "direct_reasoning_assistance",
        "runtime_flow_map_evidence",
        "static_deterministic_script_lane",
        "matrix_consumes_provider_diff_evidence",
        "heap_exchange_close",
        "heap_runtime_completeness_gate",
        "startup_manifest_primary_data_plane",
        "heap_runtime_product_package",
        "product_readiness",
        "prepare_review_pr_product",
        "final_testable_pr",
        "intrinsic_contract_present",
        "openvino_peer_topology_contract",
        "gpu0_npu_provider_contract",
    ]
    errors = [f"missing runtime mesh capability: {name}" for name in order if not checks.get(name)]
    return {
        "schema_version": 1,
        "kind": "real_product_runtime_mesh_contract",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "capability_order": order,
        "failed_capabilities": [name for name in order if not checks.get(name)],
        "runtime_route": [
            "Task MD IN",
            "python -m ia_carmine.cli run",
            "heap_context_closure",
            "GPU1/GPU0/NPU provider lanes",
            "runtime broker and deterministic validators",
            "CODE_PRODUCT_FULL_PATCH and final readable product",
        ],
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
