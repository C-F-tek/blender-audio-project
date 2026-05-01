# AI Selective Planner

The selective planner is a report-only control layer for the local AI orchestration workflow.

It reads compact, Git-trackable inputs and recommends the next validation and patch-spec steps without applying code changes and without starting provider workloads.

## Purpose

The current prototype answers this question:

```text
Given the latest context pack, dry-run evidence and GPU/NPU evidence, what should be validated or specified next?
```

It is intentionally conservative. It separates:

```text
context collection
dry-run planning evidence
real provider evidence
validator recommendations
patch-spec recommendations
local-only commands
GitHub-only actions
```

## Entry points

Build the plan:

```powershell
python .\Tools\ai\build_selective_execution_plan.py --repo-root . --output .\output\ai_pipeline\selective_execution_plan.json --markdown-output .\output\ai_pipeline\selective_execution_plan.md
```

Validate the plan:

```powershell
python .\Tools\validation\check_selective_execution_plan.py --repo-root . --plan .\output\ai_pipeline\selective_execution_plan.json --output .\output\validation\selective_execution_plan.json
```

## Default inputs

| Input | Default path | Role |
|---|---|---|
| Context pack evidence | `docs/LOCAL_VALIDATION_EVIDENCE/project_self_improvement_context_pack_evidence.json` with Markdown fallback | Confirms bounded AI context, no source writes and no provider execution. |
| Dry-run matrix evidence | `docs/LOCAL_VALIDATION_EVIDENCE/ai_pipeline_dry_run_matrix_evidence.json` | Confirms planned-only matrix coverage. |
| Real GPU/NPU evidence | `docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_v2_evidence.json` | Confirms provider execution evidence and lane decisions. |
| Validation report contract | `output/validation/validation_report_contract.json` | Optional local ignored validation health input. |
| Execution plans | `docs/EXECUTION_PLANS/active/` | Detects active linked plans. |
| Tech debt tracker | `docs/TECH_DEBT_TRACKER.md` | Detects known follow-up markers. |

The validation report contract usually lives under ignored `output/`; when it is missing in GitHub-only mode, the planner emits a risk/warning rather than inventing local results.

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

All recommended patch specs remain `manual_review_only` and `candidate_spec_only`.

## Provider policy

The planner must not execute providers.

Provider execution is valid only when Carmine runs the explicit local command set. Ollama/GPU remains the primary advisory lane only when evidence confirms the quality gate. OpenVINO/NPU remains a probe, guardrail and decode-diagnostic lane until a dedicated promotion milestone exists.

## Local evidence command set

When fresh real GPU/NPU evidence is needed:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_parallel_ai_provider_multistep.ps1 `
  -Profile npu `
  -RunOllamaProbe `
  -RunNpuProbe `
  -RunNpuDecodeSmoke `
  -UsePrimaryAdvisoryProvider `
  -Basename parallel_gpu_npu_selective_planner_real `
  -ProposalBasename parallel_gpu_npu_selective_planner_real_proposals `
  -EvidenceBasename parallel_gpu_npu_selective_planner_real_evidence

python .\Tools\ai\build_github_evidence_bundle.py --repo-root . --basename parallel_gpu_npu_selective_planner_real_evidence
python .\Tools\validation\check_github_evidence_bundle.py --repo-root . --output .\output\validation\github_evidence_bundle.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
```

Commit only compact evidence intended for GitHub review, normally under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
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
- change provider prompts, models, temperatures or orchestration behavior.

## Next iterations

1. Add validator scoring and ranking.
2. Add stricter evidence freshness heuristics when stable date policy exists.
3. Add a generator that converts `recommended_patch_specs` into draft patch specs, still without replacements.
4. Add formal provider evidence quality gates before any provider promotion work.
