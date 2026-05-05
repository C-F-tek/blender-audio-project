<!-- IA-CARMINE-MD-SPLIT: part -->
# AGENT_REVIEW_CODE_PATCH_PLAN — parte 002 di 002

Sorgente indice: [`../AGENT_REVIEW_CODE_PATCH_PLAN.md`](../AGENT_REVIEW_CODE_PATCH_PLAN.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

## Smoke validator expectations

The smoke validator checks:

```text
kind == agent_review_code_patch_plan
apply_mode == report_only_manual_review_code_patch_plan
manual_review_required == true
provider_execution_performed == false
patch_application_performed == false
source_writes_performed == false
patch_plan_count == len(code_patch_plans)
all target files are allowed or explicitly declared future/new-file candidates
all plans include validation_commands and stop_conditions
no forbidden path appears in target_files or proposed_patch metadata
```

The smoke validator must not:

```text
apply patches
run providers
run Blender
write source files
read ignored output/** reports unless explicitly supplied as input evidence
```

## Evidence bundle integration

The existing evidence bundle builder should summarize code patch-plan and docs follow-up reports in the same compact style used for documentation patch plans.

Recommended code-plan summary fields:

```text
patch_plan_count
manual_review_required
provider_execution_performed
patch_application_performed
source_writes_performed
plans[].id
plans[].area
plans[].risk
plans[].status
plans[].target_files
plans[].rationale
plans[].edit_strategy
plans[].validation_commands
plans[].stop_conditions
```

Recommended code edit proposal summary fields:

```text
id
target_file
edit_kind
manual_review_required
ready_for_manual_review
target_sha256
target_line_count
rationale
edit_strategy
validation_commands
stop_conditions
```

Recommended docs-follow-up summary fields:

```text
docs_followup_count
manual_review_required
provider_execution_performed
patch_application_performed
source_writes_performed
suggestions[].id
suggestions[].source_code_patch_plan_id
suggestions[].target_files
suggestions[].rationale
suggestions[].edit_strategy
```

The bundle may include `proposed_patch` only as a bounded preview. Full raw artifacts should remain local unless they are deliberately small, reviewed and Git-trackable.

## Line-count evidence usage

Use `docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260501-215122.csv` as a sizing hint before prioritizing code patch plans.

Large files require narrower patch scope. The CSV is useful but may be stale, so always inspect current file content before generating or applying any code patch.

## Guardrails

This lane must remain:

```text
report-only by default
manual-review-only
provider-free unless a separate explicit evidence step already ran
patch-application-free
source-write-free until a human-approved implementation phase
Blender-runtime-free
NPU advisory promotion-free
OpenVINO GPU primary-lane-free
```

## Recommended next implementation sequence

```text
1. Run code_contract_drift.
2. Build agent_review_code_patch_plan from the drift report.
3. Validate the code patch plan with run_agent_review_code_patch_plan_smoke.py.
4. Optionally build complete code_edit_proposal metadata for selected plan items.
5. Build agent_review_code_docs_followup from the code patch plan.
6. Review code and docs queues together.
7. Only then consider a separate hand-applied code/docs PR generated from reviewed plans.
```
