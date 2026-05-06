# Dry-Run Matrix Contract Follow-ups

## Status

active

## Current review note — 2026-05-07

This is an old execution plan retained under `active/` for compatibility. The work described here was validated locally on 2026-05-01 and should be treated as **legacy active / relocation-needed**, not as the current primary runtime architecture task.

Do not use this plan as the current orchestration source of truth. Read first:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

The current runtime target is:

```text
shared runtime heap / blackboard
├─ GPU1 primary advisory / planner
├─ GPU0 coworker/helper OpenVINO
├─ NPU microtask responder
├─ broker unico executor
├─ semantic tools registry
├─ deterministic validators / CPU authority
└─ telemetry/event stream
```

Keep this plan as historical evidence until a separate explicit execution-plan cleanup moves it to `completed/`.

## Goal

Plan the next additive checks for `Tools/validation/check_ai_dry_run_matrix_contract.py` and stage a wider local dry-run matrix for workstation validation.

## GitHub-only scope

This task now includes safe code changes to expand `Tools/ai/run_pipeline_dry_run_matrix.py` planning coverage and run matrix cases concurrently.

Allowed now:

```text
document expected additive checks
record warning-first validation strategy
identify local report samples needed before strict checks
add dry-run-only matrix cases that do not execute Blender, NPU, GPU or FFmpeg
add matrix-level parallel execution for dry-run cases with isolated per-case output directories
```

Forbidden now:

```text
no strict validator changes
no dry-run matrix execution claim
no local output report assumptions
no Blender/audio/GPU/NPU validation claims
```

## Matrix execution model staged in PR #34

The matrix runner now supports:

```text
--matrix-workers N
```

Default:

```text
min(8, CPU count)
```

Use `--matrix-workers 1` for serial execution.

Each case writes to its own directory under:

```text
output/ai_pipeline/dry_run_matrix/<case_name>/
```

The final JSON report preserves deterministic case order even when cases execute concurrently.

A tiny deterministic sample analysis JSON is generated automatically under:

```text
output/ai_pipeline/dry_run_matrix_inputs/sample_analysis.json
```

It exists only to satisfy preflight for dry-run music-summary planning. It must not be treated as real audio analysis output.

## Expanded dry-run matrix cases staged in PR #34

The matrix now plans baseline cases for default, validation, chunks, music-summary, smart-context, custom track stem, guardrail and NPU/GPU planning surfaces.

The key invariant remains:

```text
all NPU/GPU-related cases are planned-only through --dry-run
no provider, Blender or FFmpeg runtime is executed by this matrix
```

## Candidate additive contract checks

Future checks should be introduced as warnings first unless a field is already part of the documented minimum contract.

| Candidate check | Proposed severity first | Reason | Local sample needed |
|---|---|---|---|
| `case_count == len(results)` | error if currently guaranteed, otherwise warning first | Prevent matrix summary drift. | `output/ai_pipeline/dry_run_matrix_report.json` |
| `planned_case_count >= case_count` | warning first | Distinguish planned cases from executed cases when serial stop-on-error is used. | Expanded matrix report. |
| `matrix_workers` positive integer | warning first | Records local concurrency level for reproducibility. | Expanded matrix report. |
| unique `results[].name` | warning | Duplicate case names make reports hard to read and automate. | Matrix report with all current cases. |
| `results[].duration_sec` numeric and non-negative | warning | Helps downstream timing analysis. | Matrix report. |
| `results[].returncode` integer | error if existing reports already comply | Core process result field. | Matrix report. |
| `results[].lanes` list or structured lane summary | warning | Needed for NPU/GPU/CPU planning but shape may evolve. | Individual case reports and matrix summary. |
| `results[].schedule` present and JSON-compatible | warning | Needed for pipeline scheduling review. | Matrix report. |
| `results[].agent_state_packet` optional object or null | warning | Optional metadata should not break older reports. | Matrix report with packet present and absent. |
| `results[].report_path` under allowed generated-artifact destinations | delegate to path policy | Avoid duplicating path-policy logic. | Matrix report plus path-policy validator output. |
| unknown future fields accepted | rule, not check | Preserve forward compatibility. | Not needed. |

## Main runtime architecture alignment

This matrix remains a dry-run/planned-evidence lane. When integrated with the main runtime architecture, it should publish or reference:

```text
planned phase schedule
planned lane usage
planned artifact paths
validator outcomes
telemetry/event-stream pointers when available
```

It must not claim real GPU1/GPU0/NPU execution unless current telemetry and provider diagnostics prove it.

## Implementation rule for later PR

When implementing stricter contract checks, keep changes small:

1. run the expanded local dry-run matrix first;
2. inspect `output/ai_pipeline/dry_run_matrix_report.json`;
3. add one or two warning-first checks;
4. update `Tools/validation/README.md` and `docs/QUALITY_GATE.md`;
5. run contract validator against the generated report;
6. keep PR body explicit about local validation logs.

## Required local validation later

Conservative serial run:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error --matrix-workers 1
python .\Tools\validation\check_ai_dry_run_matrix_contract.py --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --artifact-report .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\generated_artifact_path_policy_from_matrix.json
```

Parallel workstation run:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error --matrix-workers 8
python .\Tools\validation\check_ai_dry_run_matrix_contract.py --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --artifact-report .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\generated_artifact_path_policy_from_matrix.json
```

Aggressive local stress run for the high-end workstation:

```powershell
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error --matrix-workers 12
```

## Risk

Medium if future contract checks become strict too early.

Low-medium for the expanded matrix itself because every new case uses `--dry-run`, but parallel execution can expose report-path or output-isolation bugs. That is useful before stricter contract validation is added.

Mitigation:

```text
warning-first rollout
unknown future fields accepted
path checks delegated to generated artifact path policy
local sample review before strict enforcement
all NPU/GPU-related cases remain planned-only through --dry-run
per-case output directories isolate parallel runs
serial --matrix-workers 1 remains available
```

## Local validation status

```text
Local workstation validation passed on 2026-05-01.

Command:
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error --matrix-workers 12 --repeat-cases 2

Observed result:
case_count=80
planned_case_count=80
base_case_count=40
repeat_cases=2
matrix_workers=12
passed=true

Follow-up evidence:
docs/LOCAL_VALIDATION_EVIDENCE/ai_pipeline_dry_run_matrix_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/ai_pipeline_dry_run_matrix_evidence.md
```

## Follow-up

```text
Manual execution-plan cleanup should move this file from active/ to completed/ after explicit approval for file moves.
```
