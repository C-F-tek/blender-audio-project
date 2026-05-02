# Agent Review Code Patch Plan

## Purpose

This document defines the proposed report-only lane for turning repository review evidence into safe, manual-review code patch plans.

The goal is to extend the current documentation patch-plan workflow toward code editing without enabling automatic source mutation.

This lane is design-first. It does not authorize a patch runner, provider execution, Blender runtime execution or direct writes to source files.

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

Proposed code patch-plan lane:

```text
local evidence / review reports
  -> agent_review_code_patch_plan report
  -> code patch smoke validator
  -> manual review
  -> optional small hand-applied code PR
  -> validators
  -> Git-trackable evidence bundle
```

The proposed lane may describe code edits. It must not apply them.

## Required default behavior

```text
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
manual_review_required = true
apply_mode = report_only_manual_review_code_patch_plan
```

A report that violates these defaults should fail validation unless the task explicitly authorizes a later, separate reviewed implementation phase.

## Proposed JSON report shape

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
  "proposed_patch": "optional unified diff or structured edit descriptor",
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

## Initial fixture and smoke validator

This design lane now includes a minimal fixture and smoke validator so the report contract can be tested before implementing a code patch-plan builder.

Fixture:

```text
Tools/ai/fixtures/agent_review_code_patch_plan_fixture.json
```

Smoke validator:

```text
Tools/validation/run_agent_review_code_patch_plan_smoke.py
```

Run:

```powershell
python .\Tools\validation\run_agent_review_code_patch_plan_smoke.py `
  --repo-root . `
  --report .\Tools\ai\fixtures\agent_review_code_patch_plan_fixture.json `
  --output .\output\validation\agent_review_code_patch_plan_smoke.json
```

The smoke validator checks the proposed contract and preserves:

```text
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
```

It validates the report shape only. It does not apply patches, run providers, run Blender or write source files.

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

## Proposed files for implementation phase

If this lane is implemented later, keep it separate from this design PR.

Candidate new files:

```text
Tools/ai/build_agent_review_code_patch_plan.py
```

Already introduced for contract validation in this design lane:

```text
Tools/ai/fixtures/agent_review_code_patch_plan_fixture.json
Tools/validation/run_agent_review_code_patch_plan_smoke.py
```

Candidate documentation updates:

```text
docs/JSON_SCHEMAS.md
docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md
Tools/validation/README.md
docs/LOCAL_AI_TASKS/README.md
```

Do not create the builder until the report contract and validator behavior are reviewed.

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

The existing evidence bundle builder should summarize code patch-plan reports in the same compact style used for documentation patch plans.

Recommended summary fields:

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
1. Review this design.
2. Add schema documentation for agent_review_code_patch_plan.
3. Validate the fixture with run_agent_review_code_patch_plan_smoke.py.
4. Add evidence-bundle summary support if needed.
5. Add a deterministic builder only after the report contract is accepted.
6. Only then consider a separate hand-applied code PR generated from a reviewed plan.
```
