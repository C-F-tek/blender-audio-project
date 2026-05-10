#!/usr/bin/env python3
"""Static smoke for the real product PR profile wrapper."""
from __future__ import annotations

import argparse
from pathlib import Path

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/real_product_profile_smoke.json")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    wrapper = repo / "Tools/workflow/run_unified_real_product_pr.ps1"
    adapter = repo / "Tools/workflow/run_local_ai_task_via_pipeline.ps1"
    adapter_validation = repo / "Tools/workflow/run_local_ai_task_via_pipeline/validation.ps1"
    launcher = repo / "Tools/workflow/run_unified_local_ai_refactor.ps1"
    readme = repo / "Tools/workflow/README.md"
    intrinsic_contract = repo / "Tools/validation/check_real_product_intrinsic_capability_contract.py"
    runtime_mesh_contract = repo / "Tools/validation/check_real_product_runtime_mesh_contract.py"
    live_provider_gate = repo / "Tools/validation/check_real_product_live_provider_gate.py"
    errors: list[str] = []

    text = wrapper.read_text(encoding="utf-8-sig", errors="replace") if wrapper.exists() else ""
    adapter_text = adapter.read_text(encoding="utf-8-sig", errors="replace") if adapter.exists() else ""
    adapter_validation_text = adapter_validation.read_text(encoding="utf-8-sig", errors="replace") if adapter_validation.exists() else ""
    launcher_text = launcher.read_text(encoding="utf-8-sig", errors="replace") if launcher.exists() else ""
    readme_text = readme.read_text(encoding="utf-8-sig", errors="replace") if readme.exists() else ""
    intrinsic_contract_text = intrinsic_contract.read_text(encoding="utf-8-sig", errors="replace") if intrinsic_contract.exists() else ""
    runtime_mesh_contract_text = runtime_mesh_contract.read_text(encoding="utf-8-sig", errors="replace") if runtime_mesh_contract.exists() else ""
    live_provider_gate_text = live_provider_gate.read_text(encoding="utf-8-sig", errors="replace") if live_provider_gate.exists() else ""

    task_file_contract = (
        ("[Parameter(Mandatory = $true)]" in text and "$TaskFile" in text)
        or ('[string]$TaskFile = ""' in text and "-ProcessGateTask" in text and "New-HeapExchangeProcessGateTask" in text)
    )
    mode_contract = (
        '"-Mode", "all"' in text
        or (
            '"-Mode", $RealProductPostPreflightModes' in text
            and "$RealProductPostPreflightModes" in text
            and "official,provider" in text
            and "patch_specs,evidence,contract,full_validation" in text
        )
    )

    required_tokens = {
        "wrapper_exists": wrapper.exists(),
        "delegates_to_unified_launcher": "run_unified_local_ai_refactor.ps1" in text,
        "requires_task_file": task_file_contract,
        "uses_real_product_mode_contract": mode_contract,
        "enables_primary_provider": "-UsePrimaryAdvisoryProvider" in text,
        "enables_multistep_provider": "-RunMultistepProviderWorkflow" in text,
        "enables_gpu0_workload": "-RunOpenVinoGpu0Workload" in text,
        "enables_npu_probe": "-RunNpuProbe" in text,
        "enables_npu_decode": "-RunNpuDecodeSmoke" in text,
        "enables_evidence": "-BuildEvidence" in text,
        "enables_patch_specs": "-GeneratePatchSpecs" in text,
        "enables_task_patch_suggestion": "-BuildTaskPatchSuggestionReport" in text,
        "enables_prepare_review_pr": "-PrepareReviewPr" in text,
        "enables_runtime_evidence_correlation": "-BuildRuntimeEvidenceCorrelation" in text,
        "launcher_exposes_runtime_evidence_correlation": "[switch]$BuildRuntimeEvidenceCorrelation" in launcher_text,
        "launcher_has_runtime_evidence_correlation_final_marker": "IA-CARMINE-RUNTIME-EVIDENCE-CORRELATION-FINAL-BEGIN" in launcher_text,
        "launcher_invokes_runtime_evidence_correlation_validator": "check_runtime_evidence_correlation.py" in launcher_text,
        "manifest_schema_requires_runtime_evidence_correlation_report": "runtime_evidence_correlation_requested" in launcher_text and "runtime_evidence_correlation" in launcher_text,
        "preflight_validates_manifest_runtime_correlation_schema": "run_unified_manifest_runtime_evidence_correlation_smoke.py" in readme_text or "run_unified_manifest_runtime_evidence_correlation_smoke.py" in launcher_text,
        "review_pr_final_product_contract_exists": (repo / "Tools/validation/check_review_pr_final_product_contract.py").exists(),
        "single_entry_exit_process_gate": "-ProcessGateTask" in text and "New-HeapExchangeProcessGateTask" in text,
        "single_exit_validates_review_pr_product": "[switch]$ValidateFinalReviewPrProduct" in text and "check_review_pr_final_product_contract.py" in text,
        "preflight_validates_review_pr_final_product_contract": "run_review_pr_final_product_contract_smoke.py" in readme_text or "run_review_pr_final_product_contract_smoke.py" in launcher_text,
        "supports_review_pr_push": "-ReviewPrPush" in text,
        "supports_review_pr_create": "-ReviewPrCreate" in text,
        "supports_review_pr_draft": "-ReviewPrDraft" in text,
        "guards_create_pr_requires_push": "-CreatePr requires -Push" in text,
        "readme_no_stale_draft_limitation": "does not create draft PRs yet" not in readme_text,
        "readme_documents_draft_support": "supports draft PR creation" in readme_text,
        "intrinsic_contract_exists": intrinsic_contract.exists(),
        "intrinsic_contract_mentions_heap_exchange": "heap_exchange_activation" in intrinsic_contract_text,
        "intrinsic_contract_mentions_gpu0_gpu1_npu": "gpu1_primary_advisory" in intrinsic_contract_text and "gpu0_openvino_workload" in intrinsic_contract_text and "npu_peer_micro_lane" in intrinsic_contract_text,
        "runtime_mesh_contract_exists": runtime_mesh_contract.exists(),
        "runtime_mesh_contract_mentions_sqlite_broker": "sqlite_fts_memory" in runtime_mesh_contract_text and "tool_agnostic_broker" in runtime_mesh_contract_text,
        "runtime_mesh_contract_mentions_direct_reasoning": "direct_reasoning_assistance" in runtime_mesh_contract_text,
        "runtime_flow_map_builder_exists": (repo / "Tools/ai/build_runtime_flow_map.py").exists(),
        "launcher_invokes_runtime_flow_map": "IA-CARMINE-RUNTIME-FLOW-MAP-BEGIN" in launcher_text and "build_runtime_flow_map.py" in launcher_text and "runtime_flow_" in launcher_text,
        "supports_generated_patch_specs": "-ReviewPrFromGeneratedPatchSpecs" in text,
        "supports_deterministic_suggestions": "-ReviewPrApplyDeterministicSuggestions" in text,
        "saves_inputs_to_memory": "-SaveInputsToMemoryDb" in text,
        "exposes_python_exe": "[string]$PythonExe" in text and "-PythonExe" in text,
        "exposes_budget_minutes": "[int]$BudgetMinutes" in text and "-BudgetMinutes" in text,
        "exposes_max_rounds": "[int]$MaxRounds" in text and "-MaxRounds" in text,
        "exposes_files_per_round": "[int]$FilesPerRound" in text and "-FilesPerRound" in text,
        "exposes_max_context_files": "[int]$MaxContextFiles" in text and "-MaxContextFiles" in text,
        "exposes_max_chars_per_file": "[int]$MaxCharsPerFile" in text and "-MaxCharsPerFile" in text,
        "exposes_max_new_tokens": "[int]$MaxNewTokens" in text and "-MaxNewTokens" in text,
        "exposes_keep_alive": "[string]$KeepAlive" in text and "-KeepAlive" in text,
        "exposes_npu_micro_peer_mode": (
            "[string]$NpuMicroStartMode = \"startup\"" in text
            or "[string]$NpuMicroStartMode = \"peer\"" in text
        )
        and "'startup'" in text
        and "'peer'" in text,
        "forwards_npu_micro_start_mode": "-NpuMicroStartMode" in text,
        "exposes_provider_max_context": "[int]$ProviderMaxContextChars" in text and "-ProviderMaxContextChars" in text,
        "exposes_context_pack_total": "[int]$ContextPackMaxTotalChars" in text and "-ContextPackMaxTotalChars" in text,
        "exposes_context_pack_file": "[int]$ContextPackMaxFileChars" in text and "-ContextPackMaxFileChars" in text,
        "exposes_agent_state_memory": "[int]$AgentStateMaxMemoryChars" in text and "-AgentStateMaxMemoryChars" in text,
        "exposes_max_recommendations": "[int]$MaxRecommendations" in text and "-MaxRecommendations" in text,
        "exposes_max_patch_plans": "[int]$MaxPatchPlans" in text and "-MaxPatchPlans" in text,
        "exposes_official_adapter_timeout": "[int]$OfficialAdapterTimeoutSeconds" in text and "-OfficialAdapterTimeoutSeconds" in text,
        "exposes_observer_consoles": "[switch]$OpenObserverConsoles" in text and "-OpenObserverConsoles" in text,
        "exposes_extended_observers": "[switch]$OpenExtendedObserverConsoles" in text and "-OpenExtendedObserverConsoles" in text,
        "exposes_observer_refresh": "[int]$ObserverRefreshSeconds" in text and "-ObserverRefreshSeconds" in text,
        "does_not_merge": "gh pr merge" not in text and "git merge" not in text,
        "does_not_force_push": "git push --force" not in text and "--force-with-lease" not in text,
        "launcher_has_task_ingress": "IA-CARMINE-TASK-INGRESS-CONTRACT-BEGIN" in launcher_text,
        "launcher_has_peer_manifest": "IA-CARMINE-HEAP-PEER-RUNTIME-MANIFEST-BEGIN" in launcher_text,
        "launcher_has_closure_audit": "IA-CARMINE-HEAP-EXCHANGE-CLOSURE-AUDIT-BEGIN" in launcher_text,
        "launcher_has_final_chain_contract": "IA-CARMINE-UNIFIED-CHAIN-CONTRACT-FINAL-GATE-BEGIN" in launcher_text,
                "provider_probe_no_fallback_gate": "IA-CARMINE-PROVIDER-PROBE-NO-FALLBACK-BEGIN" in launcher_text and "ProviderProbeSoftFail" in launcher_text,
        "ollama_workload_no_fallback_gate": "IA-CARMINE-OLLAMA-WORKLOAD-NO-FALLBACK-BEGIN" in launcher_text,
        "live_provider_gate_exists": live_provider_gate.exists(),
        "live_provider_gate_requires_execution": "provider probe did not perform live provider execution" in live_provider_gate_text,
        "live_provider_gate_requires_ollama_lane": "--require-ollama" in live_provider_gate_text and "required provider lane did not pass" in live_provider_gate_text,
        "launcher_uses_stamped_provider_probe": "local_provider_probe_{0}.json" in launcher_text,
        "launcher_invokes_live_provider_gate": "IA-CARMINE-REAL-PRODUCT-LIVE-PROVIDER-GATE-BEGIN" in launcher_text and "check_real_product_live_provider_gate.py" in launcher_text,
        "adapter_requires_concrete_patch_specs": "IA-CARMINE-STRICT-REAL-PRODUCT-PATCH-SPECS-BEGIN" in adapter_validation_text and "--require-concrete" in adapter_validation_text,
        "adapter_requires_provider_backed_specs": "--require-provider-execution" in adapter_validation_text,
        "patch_spec_builder_has_strict_cli": "--require-concrete" in (repo / "Tools/ai/build_patch_specs_from_proposals.py").read_text(encoding="utf-8-sig", errors="replace") and "--require-provider-execution" in (repo / "Tools/ai/build_patch_specs_from_proposals.py").read_text(encoding="utf-8-sig", errors="replace"),
"preflight_validates_runtime_evidence_correlation_wiring": "run_runtime_evidence_correlation_launcher_wiring_smoke.py" in launcher_text or "run_runtime_evidence_correlation_launcher_wiring_smoke.py" in readme_text,
        "readme_documents_runtime_evidence_correlation_launcher": "RUNTIME-EVIDENCE-CORRELATION-LAUNCHER-HARDENING" in readme_text or "Runtime evidence correlation launcher hardening" in readme_text,
                "wrapper_forwards_real_product_profile": '"-Profile", "core"' in text,
        "wrapper_forwards_official_max_context": "IA-CARMINE-REAL-PRODUCT-OFFICIAL-MAX-CONTEXT-BEGIN" in text and "-MaxContextChars" in text,
        "official_adapter_exists": adapter.exists(),
        "official_adapter_real_product_context": "IA-CARMINE-REAL-PRODUCT-OFFICIAL-CONTEXT-BEGIN" in adapter_text,
        "official_adapter_enables_context_pack": "$BuildContextPack = $true" in adapter_text,
        "official_adapter_enables_agent_state": "$BuildAgentStatePacket = $true" in adapter_text,
        "official_adapter_adds_real_product_docs": "real-product-run-doc-index-2026-05-10.md" in adapter_text and "problems-and-hygiene-candidates-2026-05-10.md" in adapter_text,
"mandatory_preflight_gate": "run_real_product_preflight_gate.py" in text and "Mandatory real product preflight failed" in text,
        "does_not_expose_skip_preflight": "SkipPreflight" not in text,
        "exposes_preflight_timeout": "[int]$PreflightTimeoutSeconds" in text,
        "bounded_prerun_reset_helper_exists": (repo / "Tools/workflow/run_local_ai_artifact_reset.py").exists(),
        "uses_bounded_prerun_reset_helper": "run_local_ai_artifact_reset.py" in text,
        "bounded_prerun_reset_passes_active_stamp": "--active-stamp" in text and "$Stamp" in text,
        "bounded_prerun_reset_writes_report": "prerun_local_ai_reset_" in text,
        "exposes_prerun_artifact_reset": "[switch]$ResetLocalAiArtifactsBeforeRun" in text and "Invoke-LocalAiArtifactReset" in text,
        "prerun_reset_uses_bounded_helper": "-ResetLocalAiArtifactsBeforeRun" in text and "run_local_ai_artifact_reset.py" in text,
        "prerun_reset_supports_memory_and_index": "-ResetLocalAiMemoryBeforeRun" in text and "-ResetGeneratedIndexBeforeRun" in text and "run_local_ai_artifact_reset.py" in text,
        "prerun_reset_requires_main_switch_for_memory_index": "reset_flags_require_artifact_reset" in text,
    }

    for name, passed in required_tokens.items():
        if not passed:
            errors.append(f"missing real product profile token: {name}")

    report = {
        "schema_version": 1,
        "kind": "real_product_profile_smoke",
        "repo_root": repo.as_posix(),
        "passed": not errors,
        "wrapper": wrapper.as_posix(),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "checks": required_tokens,
        "errors": errors,
        "warnings": [],
    }

    output = resolve_output_path(repo, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
