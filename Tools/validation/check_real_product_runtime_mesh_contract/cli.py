#!/usr/bin/env python3
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


def has_real_product_mode_contract(wrapper_text: str) -> bool:
    if '"-Mode", "all"' in wrapper_text:
        return True
    return (
        '"-Mode", $RealProductPostPreflightModes' in wrapper_text
        and "$RealProductPostPreflightModes" in wrapper_text
        and "official,provider" in wrapper_text
        and "patch_specs,evidence,contract,full_validation" in wrapper_text
    )


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
    # Runtime mesh naming contract after legacy cut:
    # - sqlite_fts_memory is the profile-visible capability token for
    #   shared memory/search/chunk evidence backed by SQLite surfaces.
    # - tool_agnostic_broker is the profile-visible capability token for
    #   the allowlisted broker that executes tools inside the heap universe.
    # These tokens are intentionally kept in the runtime-mesh contract so
    # run_real_product_profile_smoke.py validates the single universe route,
    # not a collection of isolated scripts.
    wrapper_text = read_text(repo_root / "Tools/workflow/_powershell/run_unified_real_product_pr.ps1")
    launcher_text = read_text(repo_root / "Tools/workflow/_powershell/run_unified_local_ai_refactor.ps1")
    intrinsic_text = read_text(
        repo_root / "Tools/validation/check_real_product_intrinsic_capability_contract/cli.py"
    )
    readiness_text = read_text(repo_root / "Tools/validation/check_review_pr_product_readiness/cli.py")
    prepare_text = read_text(repo_root / "Tools/ai/prepare_review_pr/cli.py")

    memory_sqlite_text = read_text(repo_root / "Tools/ai/agent_memory/sqlite_cli.py")
    broker_text = read_text(repo_root / "Tools/ai/agent_runtime_tool_broker/cli.py")
    broker_exec_text = read_text(repo_root / "Tools/ai/_shared/agent_runtime_tool_broker_execution.py")
    ollama_probe_text = read_text(repo_root / "Tools/ai/run_ollama_provider_probe.py")
    local_provider_probe_text = read_text(repo_root / "Tools/ai/run_local_provider_probe/cli.py")
    primary_advisory_text = read_text(repo_root / "Tools/ai/build_workload_quality_lane_routing/cli.py")
    openvino_gpu0_text = read_text(repo_root / "Tools/ai/build_openvino_gpu0_workload_report/cli.py")
    gpu0_companion_text = read_text(repo_root / "Tools/ai/build_gpu0_companion_task_lane/cli.py")
    npu_companion_text = read_text(repo_root / "Tools/ai/build_npu_micro_task_companion_report/cli.py")
    openvino_peer_topology_contract_text = read_text(
        repo_root / "Tools/validation/check_openvino_peer_topology_contract/cli.py"
    )
    heap_text = read_text(repo_root / "Tools/ai/provider_runtime_heap/cli.py")
    budget_text = read_text(repo_root / "Tools/ai/heap_provider_budget_governor/cli.py")
    invocation_text = read_text(repo_root / "Tools/ai/heap_provider_invocation_contract/cli.py")
    product_text = read_text(repo_root / "Tools/ai/build_heap_runtime_product_package/cli.py")
    completeness_gate_text = read_text(repo_root / "Tools/ai/run_heap_runtime_completeness_gate/cli.py")

    gpu1_provider_surface = "\n".join([ollama_probe_text, local_provider_probe_text]).lower()
    memory_surface = memory_sqlite_text.lower()
    heap_contract_surface = "\n".join(
        [heap_text, budget_text, invocation_text, completeness_gate_text]
    ).lower()

    checks: dict[str, bool] = {
        "task_md_in": has(wrapper_text, "[string]$TaskFile")
        and has(wrapper_text, '"-TaskFile", $TaskRel')
        and has(launcher_text, "IA-CARMINE-TASK-INGRESS-CONTRACT-BEGIN"),
        "heap_exchange_activation": has_real_product_mode_contract(wrapper_text)
        and has(launcher_text, "IA-CARMINE-HEAP-EXCHANGE-RUNTIME-ENTRY-ENSURE-BEGIN")
        and has(launcher_text, "IA-CARMINE-HEAP-EXCHANGE-PRE-REVIEW-BRIDGE-BEGIN"),
        "heap_provider_budget_governor": exists(
            repo_root, "Tools/ai/heap_provider_budget_governor/cli.py"
        )
        and has(budget_text, "ProviderBudgetConfig")
        and has(budget_text, "provider_lanes")
        and has(budget_text, "permit_allowed"),
        "heap_provider_invocation_contract": exists(
            repo_root, "Tools/ai/heap_provider_invocation_contract/cli.py"
        )
        and has(invocation_text, "expected_telemetry_contract")
        and has(invocation_text, "real_run_gate")
        and has(invocation_text, "broker_request"),
        "gpu1_primary_advisory": has(wrapper_text, "-UsePrimaryAdvisoryProvider")
        and has(wrapper_text, "-UseOllamaAdvisory")
        and has(wrapper_text, "-RunOllamaProbe")
        and (
            exists(repo_root, "Tools/ai/run_ollama_provider_probe.py")
            or exists(repo_root, "Tools/ai/run_local_provider_probe/cli.py")
        )
        and exists(repo_root, "Tools/ai/build_workload_quality_lane_routing/cli.py")
        and (
            "ollama" in gpu1_provider_surface
            or "provider" in gpu1_provider_surface
            or "probe" in gpu1_provider_surface
        )
        and (
            "primary" in primary_advisory_text.lower()
            or "advisory" in primary_advisory_text.lower()
        ),
        "gpu0_openvino_tool_workload": has(wrapper_text, "-RunOpenVinoGpu0Workload")
        and exists(repo_root, "Tools/ai/build_openvino_gpu0_workload_report/cli.py")
        and exists(repo_root, "Tools/ai/build_gpu0_companion_task_lane/cli.py")
        and ("openvino" in openvino_gpu0_text.lower())
        and ("gpu0" in openvino_gpu0_text.lower() or "gpu.0" in openvino_gpu0_text.lower())
        and ("companion" in gpu0_companion_text.lower()),
        "npu_peer_micro_lane": has(wrapper_text, "-NpuMicroStartMode")
        and has(wrapper_text, "-RunNpuProbe")
        and has(wrapper_text, "-RunNpuDecodeSmoke")
        and exists(repo_root, "Tools/ai/build_npu_micro_task_companion_report/cli.py")
        and ("npu" in npu_companion_text.lower())
        and ("startup" in wrapper_text.lower() or "peer" in wrapper_text.lower()),
        "shared_memory_evidence": has(wrapper_text, "-SaveInputsToMemoryDb")
        and has(wrapper_text, "-BuildEvidence")
        and has(launcher_text, "shared_memory_evidence")
        and exists(repo_root, "Tools/ai/build_shared_toolbox_ai_to_ai_bundle/cli.py")
        and exists(repo_root, "Tools/ai/build_heap_peer_runtime_manifest/cli.py"),
        "sqlite_runtime_memory": exists(repo_root, "Tools/ai/agent_memory/sqlite_cli.py")
        and ("sqlite" in memory_surface)
        and ("persistent" in memory_surface)
        and ("operational" in memory_surface)
        and exists(repo_root, "Tools/validation/run_runtime_sqlite_persistent_write_smoke/cli.py"),
        "tool_agnostic_broker": exists(repo_root, "Tools/ai/agent_runtime_tool_broker/cli.py")
        and exists(repo_root, "Tools/ai/_shared/agent_runtime_tool_broker_execution.py")
        and ("broker" in broker_text.lower())
        and ("execute" in broker_exec_text.lower() or "tool" in broker_exec_text.lower())
        and exists(repo_root, "Tools/validation/run_agent_runtime_tool_broker_smoke/cli.py")
        and exists(repo_root, "Tools/ai/build_runtime_tool_capability_manifest/cli.py")
        and exists(repo_root, "Tools/ai/build_runtime_tool_usage_telemetry/cli.py"),
        "direct_reasoning_assistance": exists(repo_root, "Tools/ai/_shared/runtime_tool_guidance.py")
        and exists(repo_root, "Tools/ai/provider_runtime_heap_broker_bridge/cli.py")
        and exists(repo_root, "Tools/ai/provider_runtime_heap_live_signals/cli.py")
        and exists(repo_root, "Tools/ai/build_provider_runtime_heap_telemetry/cli.py"),
        "runtime_flow_map_evidence": exists(repo_root, "Tools/ai/build_runtime_flow_map/cli.py")
        and has(launcher_text, "IA-CARMINE-RUNTIME-FLOW-MAP-BEGIN")
        and has(launcher_text, "build_runtime_flow_map.py")
        and has(launcher_text, "runtime_flow_"),
        "static_deterministic_script_lane": has(wrapper_text, "-GeneratePatchSpecs")
        and has(wrapper_text, "-BuildTaskPatchSuggestionReport")
        and (
            has(wrapper_text, "-ReviewPrApplyDeterministicSuggestions")
            or has(wrapper_text, "-ReviewPrFromGeneratedPatchSpecs")
        )
        and exists(repo_root, "Tools/ai/build_deterministic_recommendations/cli.py")
        and exists(repo_root, "Tools/ai/build_patch_specs_from_proposals/cli.py"),
        "heap_exchange_close": has(launcher_text, "IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-BEGIN")
        and has(launcher_text, "IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-AFTER-PATCH-SUGGESTION-BEGIN")
        and has(launcher_text, "IA-CARMINE-HEAP-EXCHANGE-LIFECYCLE-GATE-END")
        and exists(repo_root, "Tools/ai/build_heap_exchange_runtime_exit/cli.py")
        and exists(repo_root, "Tools/validation/check_heap_exchange_runtime_lifecycle/cli.py"),
        "heap_runtime_completeness_gate": exists(
            repo_root, "Tools/ai/run_heap_runtime_completeness_gate/cli.py"
        )
        and exists(repo_root, "Tools/validation/run_heap_runtime_completeness_gate_smoke/cli.py")
        and "product_signal" in heap_contract_surface
        and "broker_request" in heap_contract_surface
        and "gpu1_provider_planner" in heap_contract_surface
        and "gpu0_provider_peer" in heap_contract_surface
        and "npu_micro_task_auditor" in heap_contract_surface
        and "provider_teamwork_universe_required" in heap_contract_surface,
        "heap_runtime_product_package": exists(
            repo_root, "Tools/ai/build_heap_runtime_product_package/cli.py"
        )
        and has(product_text, "heap_runtime_product_package")
        and has(product_text, "heap_runtime_product_manifest")
        and has(product_text, "heap_runtime_product_readiness"),
        "product_readiness": has(launcher_text, "review_pr_product_readiness")
        and has(readiness_text, "prepare_review_pr_ready")
        and has(readiness_text, "has_concrete_product"),
        "prepare_review_pr_product": has(launcher_text, "build_review_pr_prepare_args")
        and has(launcher_text, "Prepare review branch and PR")
        and has(prepare_text, "gh")
        and has(prepare_text, "pr")
        and has(prepare_text, "create"),
        "final_testable_pr": has(wrapper_text, "-ReviewPrPush")
        and has(wrapper_text, "-ReviewPrCreate")
        and has(wrapper_text, "-ReviewPrDraft")
        and has(prepare_text, "--create-pr")
        and has(prepare_text, "--draft-pr"),
        "intrinsic_contract_present": exists(
            repo_root, "Tools/validation/check_real_product_intrinsic_capability_contract/cli.py"
        )
        and has(intrinsic_text, "real_product_intrinsic_capability_contract"),
        "openvino_peer_topology_contract": exists(
            repo_root, "Tools/validation/check_openvino_peer_topology_contract/cli.py"
        )
        and exists(repo_root, "Tools/validation/run_openvino_peer_topology_contract_smoke/cli.py")
        and has(openvino_peer_topology_contract_text, "openvino_peer_topology_contract")
        and has(openvino_peer_topology_contract_text, "runtime_workload_targets_gpu0_only")
        and has(
            openvino_peer_topology_contract_text, "npu_micro_uses_runtime_context_and_tool_broker"
        ),
    }

    capability_order = [
        "task_md_in",
        "heap_exchange_activation",
        "heap_provider_budget_governor",
        "heap_provider_invocation_contract",
        "gpu1_primary_advisory",
        "gpu0_openvino_tool_workload",
        "npu_peer_micro_lane",
        "shared_memory_evidence",
        "sqlite_runtime_memory",
        "tool_agnostic_broker",
        "direct_reasoning_assistance",
        "runtime_flow_map_evidence",
        "static_deterministic_script_lane",
        "heap_exchange_close",
        "heap_runtime_completeness_gate",
        "heap_runtime_product_package",
        "product_readiness",
        "prepare_review_pr_product",
        "final_testable_pr",
        "intrinsic_contract_present",
        "openvino_peer_topology_contract",
    ]

    runtime_route = [
        "Task MD IN",
        "heap/exchange activation",
        "provider budget governor",
        "provider invocation contract",
        "GPU1 primary advisory",
        "GPU0 OpenVINO/tool workload",
        "NPU peer micro lane",
        "shared memory / sqlite_fts_memory / tool_agnostic_broker / direct reasoning assistance",
        "runtime flow map evidence",
        "static deterministic script/product lane",
        "heap runtime completeness gate",
        "heap runtime product package",
        "heap/exchange CLOSE",
        "product readiness",
        "prepare_review_pr.py",
        "PR finale testabile",
    ]

    errors = [
        f"missing runtime mesh capability: {name}"
        for name in capability_order
        if not checks.get(name)
    ]
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
            "sqlite_surface_has_sqlite": "sqlite" in memory_surface,
            "sqlite_runtime_memory_present": exists(repo_root, "Tools/ai/agent_memory/sqlite_cli.py"),
            "ollama_probe_file_present": exists(repo_root, "Tools/ai/run_ollama_provider_probe.py"),
            "local_provider_probe_file_present": exists(
                repo_root, "Tools/ai/run_local_provider_probe/cli.py"
            ),
            "gpu1_provider_surface_mentions_ollama": "ollama" in gpu1_provider_surface,
            "gpu1_provider_surface_mentions_provider_or_probe": "provider" in gpu1_provider_surface
            or "probe" in gpu1_provider_surface,
            "openvino_gpu0_mentions_openvino": "openvino" in openvino_gpu0_text.lower(),
            "openvino_gpu0_mentions_gpu0": "gpu0" in openvino_gpu0_text.lower()
            or "gpu.0" in openvino_gpu0_text.lower(),
            "npu_companion_mentions_npu": "npu" in npu_companion_text.lower(),
            "heap_budget_governor_present": exists(
                repo_root, "Tools/ai/heap_provider_budget_governor/cli.py"
            ),
            "heap_invocation_contract_present": exists(
                repo_root, "Tools/ai/heap_provider_invocation_contract/cli.py"
            ),
            "heap_runtime_product_package_present": exists(
                repo_root, "Tools/ai/build_heap_runtime_product_package/cli.py"
            ),
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
    parser.add_argument(
        "--output", default="output/validation/real_product_runtime_mesh_contract.json"
    )
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
