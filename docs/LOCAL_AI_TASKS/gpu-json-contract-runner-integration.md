# GPU JSON Contract Runner Integration

## Purpose

Plan and validation notes for integrating `Tools.ai._shared.gpu_planner_json_contract.validate_model_response_contract()` into the real GPU planning runners.

Target runners:

```text
Tools/ai/run_agent_gpu_deep_planning_review.py
Tools/ai/run_agent_gpu_deep_planning_supervised.py
```

## Current safe bridge

Before changing the long-running provider path, use:

```text
Tools/ai/replay_gpu_planner_json_contract.py
```

This replays already captured GPU planner raw responses through the contract helper.

It does not run providers and does not write source files.

## Command

```powershell
python -m Tools.ai replay_gpu_planner_json_contract `
  --repo-root . `
  --gpu-report ".\output\ai_pipeline\project_complete_20260502-195523_parallel_gpu.json" `
  --output ".\output\analysis\gpu_json_contract_replay_20260502-195523.json" `
  --markdown-output ".\output\analysis\gpu_json_contract_replay_20260502-195523.md"
```

## Expected report fields

```text
replayed_round_count
contract_reason_counts
context_echo_detected_count
json_parse_failure_count
model_output_schema_mismatch_count
valid_recommendation_output_count
```

## Integration target

Once replay confirms useful classifications, update the runner parsing flow:

```text
model response
-> validate_model_response_contract(response, evidence_ready_for_manual_patch_count)
-> parsed response from contract result when valid
-> round diagnostics include contract fields
-> aggregate diagnostics use classified reasons
```

## New reason precedence

Prefer this ordering when no valid recommendations survive:

```text
context_echo_detected
json_parse_failure
model_output_schema_mismatch
recommendations_filtered_out
evidence_ready_but_no_gpu_plan
valid_json_empty_recommendations
```

`repair_attempt_failed` should remain only as a legacy/compatibility signal when older reports are inspected.

## Guardrails

```text
no provider/model settings change in the runner integration PR
no automatic patch application
no source writes through patch runner
no Blender runtime execution
no SQLite/database writes
manual review required
```

## Bundle rule

Include only compact evidence:

```text
GPU JSON contract replay report
this integration note
small smoke/compile evidence
```

Do not include raw GPU output directly unless truncated by the bundle builder.
