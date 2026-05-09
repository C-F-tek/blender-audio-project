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
    launcher = repo / "Tools/workflow/run_unified_local_ai_refactor.ps1"
    readme = repo / "Tools/workflow/README.md"
    intrinsic_contract = repo / "Tools/validation/check_real_product_intrinsic_capability_contract.py"
    runtime_mesh_contract = repo / "Tools/validation/check_real_product_runtime_mesh_contract.py"
    errors: list[str] = []

    text = wrapper.read_text(encoding="utf-8-sig", errors="replace") if wrapper.exists() else ""
    launcher_text = launcher.read_text(encoding="utf-8-sig", errors="replace") if launcher.exists() else ""
    readme_text = readme.read_text(encoding="utf-8-sig", errors="replace") if readme.exists() else ""
    intrinsic_contract_text = intrinsic_contract.read_text(encoding="utf-8-sig", errors="replace") if intrinsic_contract.exists() else ""
    runtime_mesh_contract_text = runtime_mesh_contract.read_text(encoding="utf-8-sig", errors="replace") if runtime_mesh_contract.exists() else ""

    required_tokens = {
        "wrapper_exists": wrapper.exists(),
        "delegates_to_unified_launcher": "run_unified_local_ai_refactor.ps1" in text,
        "requires_task_file": "[Parameter(Mandatory = $true)]" in text and "$TaskFile" in text,
        "uses_mode_all": '"-Mode", "all"' in text,
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
        "exposes_npu_micro_peer_mode": "[string]$NpuMicroStartMode = \"peer\"" in text,
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
        "does_not_force_push": "--force" not in text and "force-push" not in text.lower(),
        "launcher_has_task_ingress": "IA-CARMINE-TASK-INGRESS-CONTRACT-BEGIN" in launcher_text,
        "launcher_has_peer_manifest": "IA-CARMINE-HEAP-PEER-RUNTIME-MANIFEST-BEGIN" in launcher_text,
        "launcher_has_closure_audit": "IA-CARMINE-HEAP-EXCHANGE-CLOSURE-AUDIT-BEGIN" in launcher_text,
        "launcher_has_final_chain_contract": "IA-CARMINE-UNIFIED-CHAIN-CONTRACT-FINAL-GATE-BEGIN" in launcher_text,
        "preflight_validates_runtime_evidence_correlation_wiring": "run_runtime_evidence_correlation_launcher_wiring_smoke.py" in launcher_text or "run_runtime_evidence_correlation_launcher_wiring_smoke.py" in readme_text,
        "readme_documents_runtime_evidence_correlation_launcher": "RUNTIME-EVIDENCE-CORRELATION-LAUNCHER-HARDENING" in readme_text or "Runtime evidence correlation launcher hardening" in readme_text,
        "mandatory_preflight_gate": "run_real_product_preflight_gate.py" in text and "Mandatory real product preflight failed" in text,
        "does_not_expose_skip_preflight": "SkipPreflight" not in text,
        "exposes_preflight_timeout": "[int]$PreflightTimeoutSeconds" in text,
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
