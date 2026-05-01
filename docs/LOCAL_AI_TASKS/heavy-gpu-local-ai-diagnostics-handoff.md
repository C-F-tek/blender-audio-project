# Heavy GPU Local AI Diagnostics Handoff

## Purpose

This Markdown task is the handoff file for a heavier local GPU/Ollama diagnostic run.

It extends the standard GPU/NPU parallel evidence workflow with deeper local-AI requests, richer analysis expectations, CSV-based source-size awareness and stricter empty-recommendation interpretation.

Use this file as the task prompt/context for the local AI before launching or reviewing a GPU/NPU run.

## Required reading order

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/gpu-npu-parallel-evidence-runbook.md
docs/LOCAL_AI_TASKS/improve-gpu-planner-nonempty-recommendations.md
docs/LOCAL_AI_TASKS/heavy-gpu-local-ai-diagnostics-handoff.md
docs/LOCAL_VALIDATION_EVIDENCE/gpu_planner_nonempty_recommendations_evidence.md
docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260501-215122.csv
Tools/ai/run_agent_gpu_deep_planning_review.py
Tools/ai/run_agent_gpu_deep_planning_supervised.py
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py
Tools/ai/build_agent_review_patch_plan.py
Tools/ai/build_github_evidence_bundle.py
Tools/validation/run_agent_review_patch_plan_smoke.py
Tools/validation/check_github_evidence_bundle.py
```

If any instruction conflicts with `AGENTS.md`, preserve `AGENTS.md` and stop with a conflict report.

## Human request

Run or review a heavier local GPU/Ollama diagnostic workflow.

The local AI must not only execute the normal runbook. It must perform a deeper task analysis over the GPU planner, including round-by-round interpretation, empty-recommendation diagnostics, fallback confirmation, evidence quality, source-size prioritization from the Python line-count CSV and next safe patch opportunities.

## CSV evidence role

The CSV file is Git-trackable source-size evidence:

```text
docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260501-215122.csv
```

The local AI must use it to:

```text
rank large Python files by line count
identify high-complexity planning targets
avoid spending heavy GPU budget only on tiny helper files
cross-check whether GPU recommendations cover the largest/riskiest AI workflow files
separate Blender runtime monoliths from AI pipeline tooling
```

The CSV must not be treated as a patch plan. It is context/evidence only.

## Scope

Focus on the AI planning/evidence pipeline only:

```text
Tools/ai/run_agent_gpu_deep_planning_review.py
Tools/ai/run_agent_gpu_deep_planning_supervised.py
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py
Tools/ai/build_agent_review_patch_plan.py
Tools/ai/build_github_evidence_bundle.py
Tools/validation/run_agent_review_patch_plan_smoke.py
Tools/validation/check_github_evidence_bundle.py
docs/LOCAL_AI_TASKS/
docs/LOCAL_VALIDATION_EVIDENCE/
docs/JSON_SCHEMAS.md
Tools/validation/README.md
```

Out-of-scope unless explicitly requested:

```text
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/main_ready_to_jazz_wow_youtube.py
old script legacy/**
Blender runtime execution
rendering or media output generation
```

## Guardrails

```text
no automatic patch application
no output/** commit
no SQLite DB commit
no Blender runtime
no generated index manual edit
no full analysis JSON modification
no model/provider/temperature setting changes unless explicitly requested
no NPU advisory promotion
no OpenVINO GPU as primary advisory lane
manual-review-only
provider execution only when explicitly requested by the run command
```

Expected report semantics:

```text
patch_application_performed: false
source_writes_performed: false
manual_review_required: true
```

## Required local input reports

Before the heavy analysis, verify these exist:

```text
output/ai_pipeline/agent_review_evidence_sufficiency.json
output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review_v3.json
output/ai_pipeline/local_ai_core_tool_activation_agent_memory_inventory.json
output/ai_pipeline/local_ai_core_tool_activation_agnostic_tool_inventory.json
output/ai_pipeline/local_ai_core_tool_activation_transient_request_context.json
output/ai_packets/gpu_planner_nonempty_recommendations_advisory_manifest.json
output/ai_packets/gpu_planner_nonempty_recommendations_proposals.json
docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260501-215122.csv
```

If a required report is missing, stop and report which regeneration command is needed. Do not invent missing evidence.

## Heavy task requirements for the local AI

The local AI must produce a written technical assessment after the run, not only raw JSON.

Required analysis sections:

```text
1. Run health
2. GPU planner behavior
3. Round-by-round recommendation diagnostics
4. Empty recommendation root-cause classification
5. Evidence sufficiency vs GPU output comparison
6. Fallback patch-plan confirmation
7. NPU audit usefulness and non-blocking behavior
8. CSV-driven source-size/complexity prioritization
9. Guardrail compliance
10. Report/schema gaps still visible
11. Recommended next safe patch or documentation task
```

## 1. Run health

Assess:

```text
orchestrator passed
gpu_returncode
gpu_round_count
npu_audit_count
npu_audit_success_count
gpu_review_blocked_by_npu
provider_execution_performed
patch_application_performed
source_writes_performed
```

## 2. GPU planner behavior

Inspect the GPU report and explicitly capture:

```text
recommendation_count
raw_recommendation_candidate_count
filtered_recommendation_count
json_parse_error_count
repair_attempt_count
empty_recommendations_reason
evidence_ready_for_manual_patch_count
recommended_next_layer
fallback_patch_plan_recommended
```

## 3. Round-by-round diagnostics

For every GPU round, inspect:

```text
round
json_ok
parse_error
repair_attempt_count
raw_recommendation_candidate_count
filtered_recommendation_count
recommendation_count
empty_recommendations_reason
recommended_next_layer
```

Classify every round into one of:

```text
usable_plan_round
valid_json_empty_recommendations
evidence_ready_but_no_gpu_plan
json_parse_failure
repair_attempt_failed
model_output_missing_required_fields
recommendations_filtered_out
provider_error
```

## 4. Empty recommendation root-cause classification

If final `recommendation_count == 0`, choose exactly one final classification:

```text
evidence_ready_but_no_gpu_plan
valid_json_empty_recommendations
json_parse_failure
repair_attempt_failed
model_output_missing_required_fields
recommendations_filtered_out
insufficient_evidence
provider_runtime_failure
```

Expected healthy diagnostic for the current known case:

```text
evidence_ready_but_no_gpu_plan
```

This is acceptable if the fallback patch-plan works.

## 5. Evidence sufficiency vs GPU output comparison

Compare:

```text
evidence_sufficiency.ready_for_manual_patch_count
GPU recommendation_count
fallback patch_plan_count
```

Expected current target:

```text
evidence_sufficiency ready candidates > 0
GPU recommendation_count may be 0
fallback patch_plan_count should be > 0
fallback_used should be true
```

## 6. Fallback patch-plan confirmation

Run or inspect the fallback patch-plan smoke and report:

```text
passed
patch_plan_count
fallback_used
provider_execution_performed
patch_application_performed
manual_review_required
```

If `evidence_ready_for_manual_patch_count > 0` and `recommendation_count == 0`, fallback must be recommended.

## 7. NPU audit usefulness

NPU must remain a checkpoint auditor only.

Inspect:

```text
npu_audit_count
npu_audit_success_count
classification per audit
provider_execution_requested
provider_load_attempted
provider_execution_succeeded
provider_execution_performed
dependency_missing
gpu_review_blocked
warnings
```

Acceptable NPU behavior:

```text
GPU continues while NPU audits run.
NPU failure or timeout is warning-only unless it reveals a guardrail breach.
NPU output does not become the primary advisory source.
```

## 8. CSV-driven source-size/complexity prioritization

Read `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260501-215122.csv` and identify:

```text
top 20 Python files by line count
top AI pipeline files by line count
top validation files by line count
top workflow files by line count
large Blender runtime files that must not be patched in this task
large legacy files that should not dominate current AI pipeline planning
```

The local AI must explicitly answer:

```text
Did the GPU planner inspect the highest-value AI pipeline files?
Did it waste context on out-of-scope legacy/runtime files?
Which large AI workflow files should be prioritized in a future focused run?
```

Recommended priority buckets from CSV:

```text
AI pipeline: Tools/ai/**
Validation: Tools/validation/**
Workflow: Tools/workflow/**
NPU helpers: Tools/npu/**
Runtime/Blender: Scripting/** and old script legacy/**, read-only unless explicitly requested
```

## 9. Guardrail compliance

Confirm:

```text
patch_application_performed: false
source_writes_performed: false
manual_review_required: true
no output/** committed
no SQLite committed
no Blender runtime executed
no OpenVINO GPU primary advisory lane
no NPU advisory promotion
```

## 10. Report/schema gaps

List any missing or weak report fields.

Prefer additive fixes such as:

```text
new diagnostic field
new markdown summary line
new validator warning
new evidence bundle summary field
new CSV-aware context selection note
```

Do not recommend broad rewrites unless evidence proves they are needed.

## 11. Next safe patch/documentation task

The final recommendation must be one of:

```text
no_code_change_needed_collect_evidence
update_report_markdown_only
update_schema_docs_only
add_validator_warning
add_gpu_profile_preset_docs
add_gpu_profile_wrapper_manual_review_only
build_patch_plan_from_existing_evidence
add_csv_aware_context_selection_docs
```

Do not recommend direct source patch application.

## Heavy GPU run profile

Use the standard run first if the local machine is not ready.

Use this heavy profile only when explicitly approved for a longer run:

```powershell
python .\Tools\ai\run_agent_gpu_npu_parallel_orchestrator.py `
  --repo-root . `
  --budget-minutes 60 `
  --max-rounds 36 `
  --files-per-round 12 `
  --max-context-files 360 `
  --max-chars-per-file 10000 `
  --max-new-tokens 6400 `
  --keep-alive 70m `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --refined-review .\output\ai_pipeline\local_ai_core_tool_activation_megalithic_refined_review_v3.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_agent_memory_inventory.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_agnostic_tool_inventory.json `
  --report-file .\output\ai_pipeline\local_ai_core_tool_activation_transient_request_context.json `
  --report-file .\output\ai_packets\gpu_planner_nonempty_recommendations_advisory_manifest.json `
  --report-file .\output\ai_packets\gpu_planner_nonempty_recommendations_proposals.json `
  --context-root docs `
  --context-root Tools\ai `
  --context-root Tools\validation `
  --context-root Tools\workflow `
  --run-npu-auditor-provider `
  --npu-auditor-every-rounds 6 `
  --max-concurrent-npu-audits 1 `
  --npu-auditor-timeout-seconds 600 `
  --npu-max-context-chars 14000 `
  --npu-max-prompt-chars 1800 `
  --npu-max-new-tokens 512 `
  --npu-final-wait-seconds 120 `
  --checkpoint-dir .\output\ai_pipeline\gpu_planner_heavy_diagnostics_checkpoints `
  --gpu-output .\output\ai_pipeline\gpu_planner_heavy_diagnostics_parallel_gpu.json `
  --gpu-markdown-output .\output\ai_pipeline\gpu_planner_heavy_diagnostics_parallel_gpu.md `
  --output .\output\ai_pipeline\gpu_planner_heavy_diagnostics_orchestrator.json `
  --markdown-output .\output\ai_pipeline\gpu_planner_heavy_diagnostics_orchestrator.md
```

## Standard post-run inspection commands

```powershell
$orch = Get-Content .\output\ai_pipeline\gpu_planner_heavy_diagnostics_orchestrator.json -Raw | ConvertFrom-Json
$gpu = Get-Content $orch.gpu_output -Raw | ConvertFrom-Json

$orch |
  Select-Object kind, passed, provider_execution_performed, patch_application_performed, elapsed_seconds, gpu_returncode, npu_audit_count, npu_audit_success_count

$orch.gpu_summary
$orch.decision

$gpu |
  Select-Object kind, passed, round_count, recommendation_count, raw_recommendation_candidate_count, filtered_recommendation_count, json_parse_error_count, repair_attempt_count, empty_recommendations_reason, evidence_ready_for_manual_patch_count, recommended_next_layer

$gpu.rounds |
  Select-Object round, json_ok, repair_attempt_count, raw_recommendation_candidate_count, filtered_recommendation_count, recommendation_count, empty_recommendations_reason, recommended_next_layer |
  Format-Table -AutoSize

Import-Csv .\docs\LOCAL_VALIDATION_EVIDENCE\python_line_count_20260501-215122.csv |
  Sort-Object {[int]$_.Lines} -Descending |
  Select-Object -First 20
```

## Fallback smoke after heavy run

```powershell
python .\Tools\validation\run_agent_review_patch_plan_smoke.py `
  --repo-root . `
  --orchestrator .\output\ai_pipeline\gpu_planner_heavy_diagnostics_orchestrator.json `
  --evidence .\output\ai_pipeline\agent_review_evidence_sufficiency.json `
  --expect-fallback `
  --output .\output\validation\agent_review_patch_plan_smoke.json `
  --markdown-output .\output\validation\agent_review_patch_plan_smoke.md
```

## Evidence bundle after heavy run

Only compact Git-trackable evidence may be committed.

```powershell
python .\Tools\ai\build_github_evidence_bundle.py `
  --repo-root . `
  --basename gpu_planner_heavy_diagnostics_evidence `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report .\output\patch_specs\agent_review_patch_plan.json `
  --report .\output\validation\agent_review_patch_plan_smoke.json `
  --report .\output\validation\validation_report_contract.json `
  --report .\output\ai_pipeline\gpu_planner_heavy_diagnostics_orchestrator.json `
  --report .\output\ai_pipeline\gpu_planner_heavy_diagnostics_parallel_gpu.json

python .\Tools\validation\check_github_evidence_bundle.py `
  --repo-root . `
  --bundle .\docs\LOCAL_VALIDATION_EVIDENCE\gpu_planner_heavy_diagnostics_evidence.json `
  --output .\output\validation\gpu_planner_heavy_diagnostics_evidence_validation.json
```

## Final validation

```powershell
python .\Tools\validation\check_python_syntax.py `
  --repo-root . `
  --output .\output\validation\python_syntax.json

python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --output .\output\validation\validation_report_contract.json

git diff --check
git status --short
```

## Stop conditions

```text
missing required evidence reports
missing CSV line-count evidence
provider execution needed but not explicitly approved
would require output/** commit
would require SQLite write
would require Blender runtime
would require model/provider setting changes without explicit approval
would promote NPU to advisory primary lane
```
