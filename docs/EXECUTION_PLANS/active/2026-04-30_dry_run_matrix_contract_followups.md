# Dry-Run Matrix Contract Follow-ups

## Status

active

## Goal

Plan the next additive checks for `Tools/validation/check_ai_dry_run_matrix_contract.py` without making strict implementation changes yet.

## GitHub-only scope

This is a planning task only.

Allowed now:

```text
document expected additive checks
record warning-first validation strategy
identify local report samples needed before strict checks
```

Forbidden now:

```text
no strict validator changes
no dry-run matrix execution claim
no local output report assumptions
no Blender/audio/GPU/NPU validation claims
```

## Candidate additive checks

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

When implementing, keep changes small:

1. add one or two warning-first checks;
2. update `Tools/validation/README.md` and `docs/QUALITY_GATE.md`;
3. run local dry-run matrix first;
4. run contract validator against the generated report;
5. keep PR body explicit about local validation logs.

## Required local validation later

```powershell
python .\Tools\ai\run_pipeline_dry_run_matrix.py --repo-root . --continue-on-error
python .\Tools\validation\check_ai_dry_run_matrix_contract.py --repo-root . --output .\output\validation\ai_dry_run_matrix_contract.json
python .\Tools\validation\check_generated_artifact_path_policy.py --repo-root . --artifact-report .\output\ai_pipeline\dry_run_matrix_report.json --output .\output\validation\generated_artifact_path_policy_from_matrix.json
```

## Risk

Medium if checks become strict too early.

Mitigation:

```text
warning-first rollout
unknown future fields accepted
path checks delegated to generated artifact path policy
local sample review before strict enforcement
```

## Local validation status

```text
Local workstation validation pending.
```
