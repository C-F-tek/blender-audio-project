from __future__ import annotations

from .common import *  # noqa: F403
from .proposal_models import proposal
from .provider_checks import workload_quality_decision

def ai_workload_quality_remediation_proposal(
    by_kind: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    quality_summary = workload_quality_decision(by_kind)
    usable = ", ".join(quality_summary.get("usable_lanes") or []) or "none"
    unusable = ", ".join(quality_summary.get("unusable_lanes") or []) or "none"
    return proposal(
        proposal_id="P-AI-WORKLOAD-REPORT-QUALITY-GATE",
        priority="P1",
        area="local_ai_workloads",
        title="Gate AI workload reports before using them as advisory context",
        rationale=(
            f"AI workload report quality found usable lanes: {usable}; unusable lanes: {unusable}. "
            "Downstream packets and proposals should trust only usable workload reports and keep unusable lanes limited to probes until their decoding/configuration is fixed."
        ),
        target_files=[
            "Tools/validation/ai_workload/report_quality/cli.py",
            "Tools/npu/provider_mesh/npu_review_runner/cli.py",
            "Tools/ai/repository_product/repository_update_suggestions/cli.py",
            "Tools/ai/repository_product/repository_change_proposals/cli.py",
            "Tools/validation/README.md",
            "docs/JSON_SCHEMAS.md",
        ],
        change_type="workload_quality_gate",
        evidence_summary={"workload_quality_decision": quality_summary},
        sketch=[
            "Keep Ollama/GPU workload reports as primary advisory context when classified usable.",
            "Exclude or clearly mark NPU/OpenVINO generated reports as unusable when they are numeric/hex-like or non-linguistic.",
            "Do not disable NPU preflight/probe; only prevent low-quality NPU generation output from influencing suggestions.",
            "Add report metadata that distinguishes availability, execution and output usability.",
        ],
        validation=[
            "python -m Tools.validation check_ai_workload_report_quality --repo-root . --output .\\output\\validation\\ai_workload_report_quality.json",
            "python -m Tools.workflow run_post_validation_ai_packet -Profile npu -OutputDir output/ai_packets -Basename npu_ollama_real_workload_after_tests -ProposalBasename npu_ollama_real_workload_proposals -ContextFile output/ai_packets/npu_real_workload_report.md,output/ai_packets/ollama_gpu_real_workload_report.md -ReportFile output/validation/ai_workload_report_quality.json,output/validation/local_ai_resource_lanes.json,output/validation/provider_result_report.json,output/validation/local_provider_probe.json,output/validation/npu_runtime_output_manifest.json",
        ],
        stop_conditions=[
            "Any change would execute providers implicitly or by default.",
            "Any change would hide a failing/unusable AI workload report instead of reporting it.",
            "Any change would alter NPU/Ollama model configuration, prompt prose or provider orchestration.",
        ],
    )

def provider_report_adoption_proposal() -> dict[str, Any]:
    return proposal(
        proposal_id="P-RUNTIME-SAFE-PROVIDER-REPORT-ADOPTION",
        priority="P2",
        area="npu_backend",
        title="Adopt provider result reports in runtime-safe observability",
        rationale=(
            "Resource lanes, runtime-output manifest, provider-result parsing and explicit local provider probes are green. "
            "The next safe step is to let runtime-adjacent tooling consume already-produced provider results as reports, "
            "without executing providers or changing legacy runtime behavior."
        ),
        target_files=[
            "Tools/npu/dual_ai_pipeline/cli.py",
            "Tools/npu/pipeline/providers.py",
            "Tools/npu/pipeline/reports.py",
            "Tools/validation/check_provider_result_parsing/cli.py",
            "Tools/validation/pipeline/npu_pipeline_modules_check/cli.py",
            "Tools/npu/pipeline/README.md",
            "docs/JSON_SCHEMAS.md",
        ],
        change_type="runtime_safe_report_adoption",
        sketch=[
            "Add a runtime-safe helper that turns already-obtained provider payloads into provider_result_report JSON.",
            "Do not call Ollama, NPU, GPU, OpenVINO generation or provider sessions from the legacy runtime path.",
            "Write reports under output/validation or an explicitly report-only output path.",
            "Expose provider_execution_performed accurately: false for parsed legacy/simulated payloads, true only for explicit probe tools.",
            "Add smoke/unit validation that proves report adoption does not modify prompt prose, model selection, temperature or legacy outputs.",
        ],
        validation=[
            "python -m Tools.validation check_provider_result_parsing --repo-root . --output .\\output\\validation\\provider_result_parsing.json",
            "python -m Tools.npu build_provider_result_report --repo-root . --use-samples --output .\\output\\validation\\provider_result_report.json",
            "python -m Tools.ai run_local_provider_probe --repo-root . --run-ollama --run-npu --output .\\output\\validation\\local_provider_probe.json",
            "python -m Tools.workflow run_npu_pipeline_helper_validation",
        ],
        stop_conditions=[
            "Any change would execute providers from the legacy runtime path.",
            "Any change would alter prompt prose, model, temperature or provider orchestration.",
            "Any change would touch Blender runtime, Ready To Jazz, full analysis JSON or generated indexes by hand.",
            "Any report cannot distinguish parsed existing payloads from explicit provider execution.",
        ],
    )

def post_validation_loop_hardening_proposal() -> dict[str, Any]:
    return proposal(
        proposal_id="P-POST-VALIDATION-LOOP-HARDENING",
        priority="P2",
        area="workflow_core",
        title="Harden the post-validation report/packet/proposal loop",
        rationale=(
            "Resource lanes, runtime-output manifest, provider parsing, explicit provider probes and runtime-safe provider report adoption are green. "
            "The next safe milestone is consolidating the internal loop so future coding/test cycles produce stable reports, packets, proposals and stop conditions without adding new runtime features."
        ),
        target_files=[
            "Tools/workflow/_powershell/run_local_validation_after_refactor.ps1",
            "Tools/workflow/_powershell/run_npu_pipeline_helper_validation.ps1",
            "Tools/workflow/_powershell/run_post_validation_ai_packet.ps1",
            "Tools/ai/repository_product/repository_update_suggestions/cli.py",
            "Tools/ai/repository_product/repository_change_proposals/cli.py",
            "Tools/validation/README.md",
            "WORKFLOW.md",
            "docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md",
            "docs/JSON_SCHEMAS.md",
        ],
        change_type="post_validation_loop_hardening",
        sketch=[
            "Include provider_result_report in standard NPU packet/proposal validation commands everywhere it is relevant.",
            "Ensure local full validation summaries point to packet and proposal outputs consistently.",
            "Add a compact loop-health report that states which reports are missing, stale, passing or blocking.",
            "Keep generated outputs under output/ and keep source changes separate from local report generation.",
            "Document the canonical order: validation -> resource/probe reports -> runtime-safe provider report -> packet -> proposals -> reindex.",
        ],
        validation=[
            "python -m Tools.validation check_provider_result_parsing --repo-root . --output .\\output\\validation\\provider_result_parsing.json",
            "python -m Tools.npu build_provider_result_report --repo-root . --use-samples --output .\\output\\validation\\provider_result_report.json",
            "python -m Tools.ai check_local_resource_lanes --repo-root . --parallel --output .\\output\\validation\\local_ai_resource_lanes.json --markdown-output .\\output\\validation\\local_ai_resource_lanes.md",
            "python -m Tools.ai run_local_provider_probe --repo-root . --run-ollama --run-npu --output .\\output\\validation\\local_provider_probe.json",
            "python -m Tools.workflow run_local_validation_after_refactor -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2",
        ],
        stop_conditions=[
            "Any change would add new provider execution to default validation without an explicit flag.",
            "Any change would auto-apply proposal patches or commit generated reports.",
            "Any change would mix local generated outputs with source files or generated indexes.",
            "Any change would broaden permissions, network access, secrets or authentication behavior.",
        ],
    )

def default_npu_observability_proposal() -> dict[str, Any]:
    return proposal(
        proposal_id="P-NEXT-NPU-OBSERVABILITY",
        priority="P2",
        area="npu_backend",
        title="Add additive NPU observability before provider execution changes",
        rationale="Current reports do not indicate blocking failures. The next safe app-agnostic step is deeper observability, not provider behavior changes.",
        target_files=[
            "Tools/npu/provider_mesh/runtime_output_manifest/cli.py",
            "Tools/ai/check_local_resource_lanes/cli.py",
            "Tools/ai/repository_product/repository_update_suggestions/cli.py",
            "docs/JSON_SCHEMAS.md",
            "Tools/validation/README.md",
        ],
        change_type="observability_extension",
        sketch=[
            "Include runtime-output manifest and resource-lane reports in the default NPU packet profile.",
            "Add proposal generation output next to packet JSON/Markdown.",
            "Keep every output advisory and generated under output/.",
        ],
        validation=[
            "python -m Tools.workflow run_npu_pipeline_helper_validation",
            "python -m Tools.ai check_local_resource_lanes --repo-root . --parallel --output .\\output\\validation\\local_ai_resource_lanes.json --markdown-output .\\output\\validation\\local_ai_resource_lanes.md",
            "python -m Tools.workflow run_post_validation_ai_packet -Profile npu -OutputDir output/ai_packets -Basename npu_after_tests -ReportFile output/validation/local_ai_resource_lanes.json -ReportFile output/validation/npu_runtime_output_manifest.json",
        ],
        stop_conditions=[
            "Any change requires modifying provider execution, prompt prose, Blender runtime or generated indexes manually."
        ],
    )
