# Dry-Run Matrix Contract Follow-ups

## Status

active

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

The matrix now plans these baseline cases before any optional agent-state packet case:

| Case | Purpose |
|---|---|
| `base` | Default safe dry-run with guardrail and smart context enabled. |
| `no_auto_remediation` | Verify planning without automatic guardrail remediation. |
| `no_npu_guardrail` | Verify planning when NPU guardrail is disabled. |
| `no_smart_context` | Verify planning when smart context is disabled. |
| `no_wave_review` | Verify planning when first-wave WAV entrypoint review is disabled. |
| `minimal_no_context_no_guardrail` | Verify the smallest no-op planning shape remains reportable. |
| `with_validation` | Verify validate-artifacts stage planning. |
| `validation_no_guardrail` | Verify validation planning when NPU guardrail is disabled. |
| `with_chunks` | Verify semantic code chunk stage planning. |
| `chunks_no_smart_context` | Verify chunk planning without smart context. |
| `with_music_summary_planned` | Verify music intermediate stage planning with a deterministic synthetic analysis JSON. |
| `music_no_smart_context` | Verify music intermediate planning when smart context is disabled. |
| `smart_context_small_budget` | Verify smart-context planning with a small packet/capsule budget. |
| `smart_context_large_budget` | Verify smart-context planning with a larger packet/capsule budget. |
| `custom_track_stem_ascii` | Verify planning with a custom ASCII track stem. |
| `custom_track_stem_spaces` | Verify slug/path planning with spaces in track stem. |
| `custom_smart_task_short` | Verify planning with a short custom smart-context task. |
| `guardrail_max_passes_zero` | Verify report planning when guardrail remediation max passes is zero. |
| `guardrail_max_passes_one_no_auto` | Verify guardrail planning with one max pass and auto-remediation disabled. |
| `guardrail_max_passes_four` | Verify report planning with a larger remediation pass budget. |
| `with_npu_review_workers_1` | Verify optional NPU artifact review stage planning with one worker. |
| `with_npu_review_workers_4` | Verify optional NPU artifact review stage planning with the recommended local worker cap. |
| `with_npu_review_workers_8_warning` | Verify high NPU worker planning emits warnings without executing NPU workloads. |
| `npu_review_without_guardrail` | Verify NPU review planning when NPU guardrail is disabled. |
| `with_gpu_command_planned` | Verify optional GPU command planning without executing GPU workloads. |
| `with_gpu_placeholder_command_planned` | Verify GPU command placeholder formatting for `{brief}` and `{output}` without execution. |
| `validation_chunks_music` | Verify combined validation, chunk and music-summary planning. |
| `full_planning_surface` | Verify the widest planned CPU/NPU/GPU dry-run surface without executing heavy workloads. |
| `full_planning_no_auto_remediation` | Verify widest planned dry-run surface with guardrail auto-remediation disabled. |
| `with_agent_state_packet` | Optional case only when a local packet exists. |

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
