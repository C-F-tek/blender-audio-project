# Agent Review Code Patch Plan

## Purpose

This document defines the report-only lane for turning repository review evidence into safe, manual-review code patch plans.

The goal is to extend the current documentation patch-plan workflow toward code editing without enabling automatic source mutation.

This lane may describe code edits and related documentation follow-up work. It must not apply either code or documentation patches automatically.

## Relationship to existing lanes

Existing documentation patch-plan lane:

```text
local evidence / review reports
  -> Tools/ai/build_agent_review_patch_plan.py
  -> output/patch_specs/agent_review_patch_plan.json
  -> Tools/validation/run_agent_review_patch_plan_smoke.py
  -> manual-review documentation edits
  -> Git-trackable evidence bundle
```

Code patch-plan lane:

```text
code_contract_drift report
  -> Tools/ai/build_agent_review_code_patch_plan.py
  -> output/patch_specs/agent_review_code_patch_plan.json
  -> Tools/validation/run_agent_review_code_patch_plan_smoke.py
  -> manual review
  -> optional small hand-applied code PR
```

Complete code edit proposal helper:

```text
manual-review code patch plan item
  -> Tools/ai/code_edit_proposal_helpers.py
  -> code_edit_proposal metadata
  -> validators + stop conditions
  -> human applies or rejects the edit in a separate implementation step
```

Documentation follow-up bridge:

```text
agent_review_code_patch_plan report
  -> Tools/ai/build_code_patch_docs_followup.py
  -> output/patch_specs/agent_review_code_docs_followup.json
  -> manual-review documentation queue
```

The bridge lets code-plan output notify the documentation lane. It is not an apply queue.

## Required default behavior

```text
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
manual_review_required = true
apply_mode = report_only_manual_review_code_patch_plan
```

For complete code edit proposals:

```text
kind = code_edit_proposal
apply_mode = report_only_manual_review_code_edit_proposal
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
manual_review_required = true
```

For docs follow-up reports:

```text
kind = agent_review_code_docs_followup
apply_mode = report_only_manual_review_docs_followup
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
manual_review_required = true
```

A report that violates these defaults should fail validation unless the task explicitly authorizes a later, separate reviewed implementation phase.

## JSON report shape

```json
{
  "schema_version": 1,
  "kind": "agent_review_code_patch_plan",
  "passed": true,
  "provider_execution_performed": false,
  "patch_application_performed": false,
  "source_writes_performed": false,
  "apply_mode": "report_only_manual_review_code_patch_plan",
  "manual_review_required": true,
  "patch_plan_count": 0,
  "code_patch_plans": [],
  "errors": [],
  "warnings": []
}
```

Each `code_patch_plans[]` item should be small and reviewable:

```json
{
  "id": "code_patch_001",
  "area": "validation",
  "risk": "low",
  "status": "ready_for_manual_review",
  "target_files": ["Tools/validation/example.py"],
  "rationale": "Why the edit is needed.",
  "edit_strategy": "How the edit should be made.",
  "proposed_patch": "optional bounded preview only",
  "validation_commands": [
    "python Tools/validation/check_python_syntax.py --repo-root . --output output/validation/python_syntax.json",
    "python Tools/validation/check_validation_report_contract.py --repo-root . --output output/validation/validation_report_contract.json",
    "git diff --check"
  ],
  "stop_conditions": [
    "Stop if the target file does not exist unless the task explicitly authorizes a new source file.",
    "Stop if the patch touches output/**.",
    "Stop if validation fails.",
    "Stop if Blender runtime execution is required."
  ],
  "manual_review_required": true
}
```

## Complete code edit proposal helper

Helper:

```text
Tools/ai/code_edit_proposal_helpers.py
```

This helper is the first coding-complete primitive for the code-editor lane. It does not apply edits. It builds a complete proposal object containing:

```text
target path
target metadata: exists, suffix, line_count, sha256
edit kind: no_op, structured_edit, unified_diff
bounded unified diff preview
structured operations
rationale
edit strategy
validation commands
stop conditions
manual review status
```

Supported edit kinds:

```text
no_op
structured_edit
unified_diff
```

Supported structured operations:

```text
replace
insert_after
insert_before
delete
append
```

A complete proposal must remain metadata-only:

```text
source_writes_performed = false
patch_application_performed = false
provider_execution_performed = false
```

The helper validates that target files do not escape the repository, do not target blocked artifacts, and include validators. For Python targets it automatically adds:

```powershell
python -m py_compile .\<target-file>
```

alongside repository validators:

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract.json
git diff --check
```

A unified-diff proposal must reference the normalized target file and include standard diff markers:

```text
---
+++
@@
```

The helper rejects or flags proposals that mention blocked fragments such as:

```text
output/
renders/
.sqlite
.db
full_analysis
analysis_full
```

## Builder, fixtures and smoke validator

Builder:

```text
Tools/ai/build_agent_review_code_patch_plan.py
```

Fixture inputs:

```text
Tools/ai/fixtures/code_contract_drift_fixture.json
Tools/ai/fixtures/agent_review_code_patch_plan_fixture.json
```

Smoke validator:

```text
Tools/validation/run_agent_review_code_patch_plan_smoke.py
```

Build from fixture:

```powershell
python .\Tools\ai\build_agent_review_code_patch_plan.py `
  --repo-root . `
  --code-contract-drift-report .\Tools\ai\fixtures\code_contract_drift_fixture.json `
  --output .\output\patch_specs\agent_review_code_patch_plan_fixture_built.json `
  --markdown-output .\output\patch_specs\agent_review_code_patch_plan_fixture_built.md
```

Validate fixture report:

```powershell
python .\Tools\validation\run_agent_review_code_patch_plan_smoke.py `
  --repo-root . `
  --report .\Tools\ai\fixtures\agent_review_code_patch_plan_fixture.json `
  --output .\output\validation\agent_review_code_patch_plan_smoke.json
```

Validate generated report:

```powershell
python .\Tools\validation\run_agent_review_code_patch_plan_smoke.py `
  --repo-root . `
  --report .\output\patch_specs\agent_review_code_patch_plan_fixture_built.json `
  --output .\output\validation\agent_review_code_patch_plan_smoke_built.json
```

The builder and smoke validator preserve:

```text
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
```

They do not apply patches, run providers, run Blender or write source files.

## Documentation follow-up bridge

When a code patch plan proposes code changes, the docs follow-up bridge emits a related documentation review queue.

Bridge:

```text
Tools/ai/build_code_patch_docs_followup.py
```

Run:

```powershell
python .\Tools\ai\build_code_patch_docs_followup.py `
  --repo-root . `
  --code-patch-plan .\output\patch_specs\agent_review_code_patch_plan_fixture_built.json `
  --output .\output\patch_specs\agent_review_code_docs_followup.json `
  --markdown-output .\output\patch_specs\agent_review_code_docs_followup.md
```

The bridge maps code target areas to likely documentation surfaces, for example:

| Code area/path | Candidate docs |
|---|---|
| `Tools/validation/**` | `Tools/validation/README.md`, `docs/JSON_SCHEMAS.md`, `docs/CONTRACT_DRIFT_VALIDATION.md` |
| `Tools/workflow/**` | `docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md`, `docs/LOCAL_AI_TASKS/README.md`, `WORKFLOW.md` |
| `Tools/ai/**` | `docs/AGENT_REVIEW_CODE_PATCH_PLAN.md`, `docs/JSON_SCHEMAS.md`, `docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md` |
| `Tools/npu/**` | `docs/LOCAL_AI_WORKFLOW.md`, `docs/LOCAL_WORKSTATION_TARGET.md`, `docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md` |

Docs follow-up suggestions remain manual-review-only. They should be reviewed after the related code patch plan is accepted or materially changed.

## Allowed targets

A code patch plan may target source files only when all conditions hold:

```text
file exists, unless the task explicitly authorizes a new source file
file is not under output/**
file is not generated index content
file is not full analysis JSON
file is not a SQLite/database artifact
edit is small and target-specific
validation commands are listed
stop conditions are explicit
```

## Blocked targets

The code patch-plan lane must reject or mark blocked any plan touching:

```text
output/**
*.db
*.sqlite
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
full_analysis*.json
*analysis_full*.json
Blender runtime execution paths without explicit runtime task scope
provider credentials, secrets, billing, permissions or repository visibility
```

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
