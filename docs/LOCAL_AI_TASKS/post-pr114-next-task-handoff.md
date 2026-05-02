# Post-PR114 Next Task Handoff

## Purpose

Operational handoff for the next AI/tooling tasks after PR #109, PR #111, PR #112, PR #113 and PR #114.

This document exists to prevent the next task from restarting architecture analysis from scratch.

Use it as the first local/context document before touching the next GPU planner integration PR.

## Current merged baseline

```text
master includes PR #109: manual-review code patch plan lane and GitHub evidence bundle refactor
master includes PR #111: GPU repair-failure recommendation report
master includes PR #112: GPU planner JSON contract helper and smoke
master includes PR #113: GPU/NPU sync analyzer, balanced profile, bundle retention policy
master includes PR #114: GPU planner JSON contract replay on historical outputs
```

Latest relevant merge:

```text
28c600a6fecb2ab56be6b9951a9de72adf2ffbab
Merge PR #114: feat(ai): replay GPU planner JSON contract on real outputs
```

## Critical evidence from the reference complete run

Reference run:

```text
project_complete_20260502-195523
```

Original GPU/NPU behavior:

```text
GPU round count: 24
NPU audit count: 5
NPU audit success count: 5
GPU recommendation count: 0
GPU raw recommendation candidate count: 0
GPU filtered recommendation count: 0
legacy empty reason: repair_attempt_failed
evidence ready for manual patch count: 12
fallback patch plan count: 12
```

PR #114 replay evidence refined the failure diagnosis:

```text
replayed_round_count=24
json_parse_failure=22
model_output_schema_mismatch=2
context_echo_detected=0
valid_recommendation_output=0
```

Interpretation:

```text
The historical GPU output mostly failed as malformed/truncated JSON, with two rounds producing parseable but schema-invalid output. The old repair_attempt_failed aggregate was too coarse.
```

## Current helper/tool inventory relevant to next work

```text
Tools/ai/gpu_planner_json_contract.py
Tools/validation/run_gpu_planner_json_contract_smoke.py
Tools/ai/replay_gpu_planner_json_contract.py
Tools/ai/build_gpu_repair_failure_recommendation.py
Tools/ai/analyze_gpu_npu_run_sync.py
Tools/ai/build_agent_review_patch_plan.py
Tools/ai/build_github_evidence_bundle.py
Tools/validation/check_github_evidence_bundle.py
```

Important docs:

```text
docs/LOCAL_AI_TASKS/gpu-planner-json-contract-hardening.md
docs/LOCAL_AI_TASKS/gpu-json-contract-runner-integration.md
docs/LOCAL_AI_TASKS/gpu-npu-balanced-run-profile.md
docs/LOCAL_AI_TASKS/post-pr111-ai-planner-feature-roadmap.md
docs/LOCAL_VALIDATION_EVIDENCE/README.md
```

## Next recommended PR

Title:

```text
feat(ai): wire GPU planner JSON contract into runner diagnostics
```

Primary target:

```text
Tools/ai/run_agent_gpu_deep_planning_review.py
```

Secondary target only if needed:

```text
Tools/ai/run_agent_gpu_deep_planning_supervised.py
```

Reason:

```text
The supervised runner currently depends on the base GPU planning behavior. Start with the base runner and only touch supervised wiring if the code path requires explicit propagation.
```

## Required behavior change

Current legacy path:

```text
model response
-> parse_model_json_with_diagnostics()
-> recommendation_diagnostics_for_round()
-> aggregate_recommendation_diagnostics()
-> empty_recommendations_reason often collapses to repair_attempt_failed
```

Target path:

```text
model response
-> validate_model_response_contract(response, evidence_ready_for_manual_patch_count)
-> parsed response from contract result when schema is usable
-> round diagnostics include contract_* fields
-> aggregate diagnostics prefers explicit contract reasons
```

## Required output fields to add or preserve

Add where practical:

```text
contract_json_ok
contract_schema_ok
contract_context_echo_detected
contract_empty_recommendations_reason
contract_parse_error
contract_schema_errors
contract_raw_response_sha256
contract_top_level_keys
contract_valid_recommendation_count
contract_invalid_recommendation_count
```

Preserve existing compatibility fields:

```text
json_ok
parse_error
repair_attempt_count
raw_recommendation_candidate_count
filtered_recommendation_count
recommendation_count
empty_recommendations_reason
evidence_ready_for_manual_patch_count
recommended_next_layer
```

## Reason precedence for aggregate empty output

Prefer this order when no valid recommendations survive:

```text
context_echo_detected
json_parse_failure
model_output_schema_mismatch
recommendations_filtered_out
evidence_ready_but_no_gpu_plan
valid_json_empty_recommendations
```

Use `repair_attempt_failed` only as legacy compatibility when reading older reports, not as the primary new classifier.

## Prompt hardening is a separate PR

Do not mix runner diagnostic wiring with prompt rewriting.

The next PR should focus on diagnostics/classification only.

A later PR can change prompt shape, for example:

```text
JSON-only footer
explicit no files/content_preview top-level output
compact retry lane
schema-only response example
```

## GPU/NPU balance baseline

PR #113 established the measured skew:

```text
gpu_round_count=24
npu_audit_count=5
npu_audit_success_count=5
npu_audit_round_coverage=0.208
avg_gpu_round_seconds=29.425
avg_npu_audit_seconds=124.8
npu_to_gpu_avg_duration_ratio=4.241
```

Balanced profile candidate for future complete run:

```text
--max-rounds 20
--files-per-round 8
--max-context-files 220
--max-chars-per-file 6000
--max-new-tokens 3600
--npu-auditor-every-rounds 3
--npu-auditor-timeout-seconds 420
--npu-max-context-chars 8000
--npu-max-prompt-chars 1200
--npu-max-new-tokens 384
--npu-final-wait-seconds 180
```

Do not change provider/model settings in the diagnostic wiring PR.

## Bundle retention law

Follow:

```text
docs/LOCAL_VALIDATION_EVIDENCE/README.md
```

Main rule:

```text
commit the smallest bundle that proves the decision
```

For the next PR, commit only one final compact evidence bundle unless an after-fix bundle is required.

## Local validation sequence for the next PR

Minimum local validation after wiring:

```powershell
python -m py_compile .\Tools\ai\run_agent_gpu_deep_planning_review.py .\Tools\ai\gpu_planner_json_contract.py
python -m py_compile .\Tools\ai\replay_gpu_planner_json_contract.py
python .\Tools\validation\run_gpu_planner_json_contract_smoke.py `
  --repo-root . `
  --output .\output\validation\gpu_planner_json_contract_smoke_<STAMP>.json `
  --markdown-output .\output\validation\gpu_planner_json_contract_smoke_<STAMP>.md
python .\Tools\ai\replay_gpu_planner_json_contract.py `
  --repo-root . `
  --gpu-report .\output\ai_pipeline\project_complete_20260502-195523_parallel_gpu.json `
  --output .\output\analysis\gpu_json_contract_replay_after_wiring_<STAMP>.json `
  --markdown-output .\output\analysis\gpu_json_contract_replay_after_wiring_<STAMP>.md
```

If a provider run is needed, use the complete-run procedure only after the wiring PR merges.

## Evidence bundle for the next PR

Recommended compact bundle inputs:

```text
output/validation/gpu_planner_json_contract_smoke_<STAMP>.json
output/analysis/gpu_json_contract_replay_after_wiring_<STAMP>.json
docs/LOCAL_AI_TASKS/post-pr114-next-task-handoff.md
docs/LOCAL_AI_TASKS/gpu-json-contract-runner-integration.md
```

Do not include raw `output/**` files directly outside the bundle.

## Stop conditions

Stop if:

```text
runner wiring requires a large rewrite of run_agent_gpu_deep_planning_review.py
contract helper changes break the existing smoke
supervised runner requires unclear behavior changes
bundle exceeds retention policy limits
any step suggests automatic patch application
any step suggests provider/model setting changes in this diagnostic PR
```

## Next tasks after runner diagnostic wiring

Recommended order:

```text
1. Prompt hardening: JSON-only footer and no context echo output
2. Compact prompt retry lane for failed full-context GPU rounds
3. Recommendation schema validator integration into merge/filter logic
4. Provider agreement matrix
5. AI improvement impressions extractor
6. Issue/task candidate pack
7. Reusable project-agnostic AI pipeline profiles
8. Complete-run manifest
9. Bundle quality score
10. Evidence bundle retention inventory report-only tool
```
