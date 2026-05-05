# AI Selective Planner

The selective planner is a report-only control layer for the local AI orchestration workflow.

It reads compact, Git-trackable inputs and recommends the next validation and patch-spec steps without applying code changes and without starting provider workloads.

This document is a contract/positioning document, not a command catalog. Current executable commands live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/validation/README.md
```

## Purpose

The current prototype answers this question:

```text
Given the latest context pack, evidence, telemetry, capability manifest and provider diagnostics, what should be validated or specified next?
```

It is intentionally conservative. It separates:

```text
context collection
dry-run planning evidence
real provider evidence
runtime telemetry and capability context
validator recommendations
patch-spec recommendations
local-only commands
GitHub-only actions
```

## Full-run planner doctrine

Selective planning is a supporting lane behind the unified local-AI flow.

If planner output is produced from full-run evidence, it must preserve the **TUTTO SU TUTTO** interpretation of that run. `quick`, `balanced`, `deep` and `custom` are intensity differences only; planner recommendations must not treat a quick full run as a partial-scope run.

Telemetry is an obligatory completeness accessory for planner inputs and patch-spec recommendations. It does not replace evidence or patch plans; it explains whether the source lanes executed, failed, degraded, were blocked, were disabled or were planned-only.

A planner recommendation that cites full-run evidence should include or reference:

```text
evidence artifacts
patch-plan or patch-spec artifacts
runtime tool usage telemetry
runtime tool capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
```

## Entry point policy

Broad planning runs should be selected through the unified launcher.

Focused direct invocation of the selective planner is allowed only when debugging the planner or validating its specific report contract. Do not promote this planner as a separate active 0-to-10 entrypoint.

## Default inputs

| Input | Default path | Role |
|---|---|---|
| Context pack evidence | `docs/LOCAL_VALIDATION_EVIDENCE/project_self_improvement_context_pack_evidence.json` with Markdown fallback | Confirms bounded AI context, no source writes and no provider execution. |
| Dry-run matrix evidence | `docs/LOCAL_VALIDATION_EVIDENCE/ai_pipeline_dry_run_matrix_evidence.json` | Confirms planned-only matrix coverage. |
| Real GPU/NPU evidence | `docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_v2_evidence.json` | Confirms provider execution evidence and lane decisions. |
| Runtime tool usage telemetry | `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.json` | Confirms tool execution, failure and blocked counts when broker lane ran. |
| Runtime capability manifest | `docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_<STAMP>.json` | Confirms which tools/capabilities were available and under which guardrails. |
| Full toolbox telemetry summary | `docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_<STAMP>.json` | Confirms provider, GPU/NPU, broker, patch-plan and guardrail state. |
| Shared AI-to-AI bundle/final summary | `docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.json` and `output/analysis/shared_toolbox_ai_to_ai_final_summary_<STAMP>.json` | Production handoff surface for next AI/operator. |
| Validation report contract | `output/validation/validation_report_contract.json` | Optional local ignored validation health input. |
| Execution plans | `docs/EXECUTION_PLANS/active/` | Detects active linked plans. |
| Tech debt tracker | `docs/TECH_DEBT_TRACKER.md` | Detects known follow-up markers. |

The validation report contract and final summary may live under ignored `output/**`; when missing in GitHub-only mode, the planner emits a risk/warning rather than inventing local results.

## Output contract

The JSON plan uses:

```text
schema_version
kind: selective_execution_plan
generated_at
repo_root
apply_mode: report_only
provider_execution_performed: false
patch_application_performed: false
inputs
provider_evidence_summary
telemetry_summary
capability_manifest_summary
dry_run_summary
validation_health
recommended_validators
recommended_patch_specs
blocked_actions
local_only_actions_for_carmine
github_only_actions_for_ai
risks
next_command_set
passed
errors
warnings
```

All recommended patch specs remain:

```text
manual_review_only
candidate_spec_only
telemetry_required_for_full_run_evidence
```

## Provider and telemetry policy

The planner must not execute providers.

Provider execution is valid only when Carmine runs the explicit local command set through the unified launcher/provider lanes. Ollama/GPU remains the primary advisory lane only when evidence confirms the quality gate. OpenVINO/NPU remains a probe, guardrail and decode-diagnostic lane until a dedicated promotion milestone exists.

For evidence-derived plans, the planner must not infer provider success from file existence alone. It must inspect or require:

```text
provider_advisory_state
provider_failure_detected
provider_failure_reasons
degraded_provider_components
deterministic_recovery_used
workload_quality_routing_ok
quality_gate_passed
```

## Evidence and patch-spec completeness

When fresh real GPU/NPU or full-toolbox evidence is needed, use the unified launcher runbook. Do not start from legacy provider wrappers as primary entrypoints.

Commit only compact evidence intended for GitHub review, normally under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
```

Do not commit:

```text
output/**
output/patch_specs/**
*.db
*.sqlite
renders/**
```

## Forbidden behavior

The selective planner must not:

- apply patches;
- write source replacements;
- enqueue patch specs for automatic apply;
- run Blender;
- run FFmpeg;
- execute Ollama/OpenVINO/GPU/NPU providers implicitly;
- edit generated indexes manually;
- edit full analysis JSON files;
- change provider prompts, models, temperatures or orchestration behavior;
- treat a patch-spec recommendation as complete when its full-run evidence lacks telemetry/capability context.

## Next iterations

1. Add validator scoring and ranking.
2. Add stricter evidence freshness heuristics when stable date policy exists.
3. Add a generator that converts `recommended_patch_specs` into draft patch specs, still without replacements.
4. Add formal provider evidence quality gates before any provider promotion work.
5. Add telemetry completeness scoring for evidence-derived patch-spec recommendations.
