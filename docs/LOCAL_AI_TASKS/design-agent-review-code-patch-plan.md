# Local AI Task — Design agent-review code patch-plan lane

## Purpose

Design the next safe extension after documentation patch plans: a report-only code patch-plan lane.

This task does not implement code changes. It prepares the contract and validation criteria for a future implementation PR.

## Source documents

Read first:

```text
docs/AGENT_REVIEW_CODE_PATCH_PLAN.md
docs/CONTRACT_DRIFT_VALIDATION.md, if present on the active branch
docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md
docs/JSON_SCHEMAS.md
Tools/validation/README.md
```

Evidence/sizing hint:

```text
docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260501-215122.csv
```

Treat the CSV as a review-prioritization hint only. It may be stale after later commits.

## Guardrails

```text
Do not write to master directly.
Do not merge without explicit maintainer command.
Do not use git add .
Do not commit output/**.
Do not execute Blender runtime.
Do not execute providers implicitly.
Do not apply patches automatically.
Do not create runtime files only because stale documentation mentions them.
Do not promote NPU to primary advisory.
Do not use OpenVINO GPU as primary lane.
```

## Desired architecture

The future lane should produce a report shaped like:

```text
kind = agent_review_code_patch_plan
apply_mode = report_only_manual_review_code_patch_plan
provider_execution_performed = false
patch_application_performed = false
source_writes_performed = false
manual_review_required = true
```

The report may contain code patch candidates, but those candidates remain manual-review-only.

## Design tasks

1. Confirm whether an equivalent code patch-plan implementation already exists.
2. If not, document the missing implementation as future work.
3. Define the report schema and smoke validator expectations.
4. Define forbidden targets and stop conditions.
5. Define evidence bundle summary expectations.
6. Keep the implementation PR separate from this design task.

## Search commands

```powershell
Select-String -Path .\Tools\ai\*.py, .\Tools\validation\*.py `
  -Pattern "code_patch|patch_application_performed|source_writes_performed|manual_review|apply_mode|proposed_patch|unified_diff|agent_review_code_patch_plan" `
  -CaseSensitive:$false

Get-ChildItem .\Tools -Recurse -File |
  Where-Object { $_.Name -match "patch|apply|review|agent|code" } |
  Select-Object FullName
```

## Validation for a design-only PR

```powershell
python -m Tools.validation check_docs_links --repo-root . --output .\output\validation\docs_links.json
python -m Tools.validation check_validation_report_contract --repo-root . --output .\output\validation\validation_report_contract.json
git diff --check
git status --short
```

## Expected output of this task

Minimum:

```text
docs/AGENT_REVIEW_CODE_PATCH_PLAN.md
docs/LOCAL_AI_TASKS/design-agent-review-code-patch-plan.md
```

No source implementation is required for this task.

## Promotion path after design review

A later implementation PR may add:

```text
Tools/ai/agent_review/code_patch_plan_cli.py
Tools/validation/agent_review/code_patch_plan_smoke/cli.py
docs/JSON_SCHEMAS.md update
Tools/validation/README.md update
```

That later PR must include script line counts for any created or modified code files.
