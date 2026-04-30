# Dry-Run Matrix Contract Follow-ups

## Status

active

## Goal

Plan the next additive checks for `Tools/validation/check_ai_dry_run_matrix_contract.py` and stage a wider local dry-run matrix for workstation validation.

## GitHub-only scope

This task now includes one safe code change to expand `Tools/ai/run_pipeline_dry_run_matrix.py` planning coverage.

Allowed now:

```text
document expected additive checks
record warning-first validation strategy
identify local report samples needed before strict checks
add dry-run-only matrix cases that do not execute Blender, NPU, GPU or FFmpeg
```

Forbidden now:

```text
no strict validator changes
no dry-run matrix execution claim
no local output report assumptions
no Blender/audio/GPU/NPU validation claims
```

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
| `with_chunks` | Verify semantic code chunk stage planning. |
| `with_music_summary_planned` | Verify music intermediate stage planning with a deliberately missing analysis path because dry-run should not execute it. |
| `with_npu_review_planned` | Verify optional NPU artifact review stage planning without executing NPU workloads. |
| `with_gpu_command_planned` | Verify optional GPU command planning without executing GPU workloads. |
| `full_planning_surface` | Verify the widest planned CPU/NPU/GPU dry-run surface without executing heavy workloads. |
| `with_agent_state_packet` | Optional case only when a local packet exists. |

## Candidate additive contract checks

Future checks should be introduced as warnings first unless a field is already part of the documented minimum contract.

| Candidate check | Proposed severity first | Reason | Local sample needed |
|---|---|---|---|
| `case_count == len(results)` | error if currently guaranteed, otherwise warning first | Prevent matrix summary drift. | `output/ai_pipeline/dry_run_matrix_report.json` |
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

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
python .\Tools\validation\check_ai_dry_run_matrix_contract.py --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --artifact-report .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\generated_artifact_path_policy_from_matrix.json
```

## Risk

Medium if checks become strict too early.

Low for the expanded matrix itself because every new case uses `--dry-run`.

Mitigation:

```text
warning-first rollout
unknown future fields accepted
path checks delegated to generated artifact path policy
local sample review before strict enforcement
all NPU/GPU-related cases remain planned-only through --dry-run
```

## Local validation status

```text
Local workstation validation pending.
```
