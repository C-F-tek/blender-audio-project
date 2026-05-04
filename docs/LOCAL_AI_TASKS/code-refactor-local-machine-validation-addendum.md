# Code Refactor 0 -> 10: Local Machine Validation Addendum

This addendum patches the canonical procedure without replacing it.

Parent procedure:

```text
docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md
```

Required policy document:

```text
docs/LOCAL_VALIDATION_EVIDENCE/LOCAL_MACHINE_VALIDATION.md
```

## Why this addendum exists

The 0 -> 10 refactor procedure already produces many local reports under `output/**` and compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/`.

The missing piece was an explicit local-machine validation contract that distinguishes:

```text
current task-scoped validation failures -> blocker
old output/validation drift -> technical debt, not automatic blocker
raw output/** reports -> local-only
compact docs/LOCAL_VALIDATION_EVIDENCE/* -> Git-trackable review evidence
```

## Insert into step 1 reading set

When running the parent 0 -> 10 procedure, add these reads to the step `1. Read repository instructions and reference docs`:

```powershell
Get-Content .\docs\LOCAL_VALIDATION_EVIDENCE\LOCAL_MACHINE_VALIDATION.md -TotalCount 260
Get-Content .\docs\LOCAL_AI_TASKS\code-refactor-local-machine-validation-addendum.md -TotalCount 260
```

For Markdown/documentation refactors, also read:

```powershell
Get-Content .\docs\LOCAL_AI_TASKS\code-refactor-md-lane-extension.md -TotalCount 260
```

## 10-minute refactor run profile

Use this bounded profile when the objective is quick discovery, Markdown cleanup, script/tool inventory review, or a first-pass refactor proposal.

It is intentionally shorter than the canonical 30-minute balanced run and must preserve the same guardrails:

```text
manual-review-only
no automatic patch application
no Blender runtime
no raw output/** commit
provider execution only if explicitly requested by the parent run
```

Recommended 10-minute profile values for the parent `run_agent_gpu_npu_parallel_orchestrator.py` step:

```powershell
--budget-minutes 10 `
--max-rounds 8 `
--files-per-round 6 `
--max-context-files 120 `
--max-chars-per-file 5000 `
--max-new-tokens 2400 `
--keep-alive 15m `
--npu-auditor-every-rounds 3 `
--max-concurrent-npu-audits 1 `
--npu-auditor-timeout-seconds 240 `
--npu-max-context-chars 6000 `
--npu-max-prompt-chars 1000 `
--npu-max-new-tokens 256 `
--npu-final-wait-seconds 90
```

Use the 30-minute profile only after the 10-minute profile shows that the evidence inputs are clean and useful.

## Insert before final report-contract validation

The parent guide currently uses broad validation report contract scans. Keep them for health checks, but add a task-scoped validation pass for PR evidence.

Example task-scoped contract validation:

```powershell
python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --report-file ".\output\validation\python_syntax_code_refactor_final_$Stamp.json" `
  --report-file ".\output\validation\python_line_count_refactor_large_code_$Stamp.json" `
  --report-file ".\output\validation\code_refactor_ai_to_ai_bundle_${Stamp}_validation.json" `
  --output ".\output\validation\validation_report_contract_code_refactor_task_$Stamp.json"
```

For Markdown/doc refactor lanes, include:

```powershell
python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --report-file ".\output\validation\markdown_inventory_refactor_$Stamp.json" `
  --report-file ".\output\validation\script_inventory_refactor_$Stamp.json" `
  --report-file ".\output\validation\docs_links_$Stamp.json" `
  --output ".\output\validation\validation_report_contract_md_refactor_task_$Stamp.json"
```

Rule:

```text
Broad-scan failure on unrelated old output/validation reports is technical debt.
Task-scoped contract failure on current reports is a blocker.
```

## Insert into compact evidence bundle artifacts

When building a compact code-refactor or docs-refactor evidence bundle, include:

```text
docs/LOCAL_VALIDATION_EVIDENCE/LOCAL_MACHINE_VALIDATION.md
docs/LOCAL_AI_TASKS/code-refactor-local-machine-validation-addendum.md
```

For Markdown/doc refactors, also include:

```text
docs/LOCAL_AI_TASKS/code-refactor-md-lane-extension.md
output/validation/markdown_inventory_refactor_<STAMP>.json
output/validation/markdown_inventory_refactor_<STAMP>.md
output/validation/script_inventory_refactor_<STAMP>.json
output/validation/script_inventory_refactor_<STAMP>.csv
output/validation/script_inventory_refactor_<STAMP>.md
output/validation/validation_report_contract_md_refactor_task_<STAMP>.json
```

Do not commit raw `output/**`; only compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/` may be staged.

## Required local-machine report summary

Every final handoff from the local machine should include:

```text
git status --short
git diff --check
current task-scoped validation report contract result
current docs links result when Markdown was touched
compact evidence bundle validation result when a bundle was built
provider_execution_performed
patch_application_performed
source_writes_performed
Blender runtime status
```

## Stop conditions

Stop and report before PR if:

```text
current task-scoped report contract fails
current docs links validation fails after Markdown changes
raw output/** would be committed
compact evidence bundle validation fails
provider execution occurred outside explicit scope
Blender runtime executed outside explicit scope
```

## Acceptance criteria

```text
parent 0 -> 10 guide remains canonical
local validation policy is explicit and readable
current-task validation is separated from old output drift
compact evidence is defined as the GitHub handoff surface
Markdown lane includes both Markdown inventory and script inventory
10-minute profile is available for bounded first-pass refactor runs
```
