# Code Refactor 0 -> 10: Markdown Refactor Lane Extension

This file extends the canonical code refactor procedure with a documentation/Markdown lane.

Canonical parent guide:

```text
docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md
```

Do not run this as an independent procedure. Use it as an additional lane inside the existing 0 -> 10 refactor flow when the user asks for Markdown cleanup, obsolete-document pruning, documentation-flow reduction, or AI-readable documentation refactoring.

## Purpose

The local AI performs the actual review/refactor. This lane gives it deterministic evidence and boundaries for Markdown work:

```text
Markdown inventory
script/tool inventory
single reading flow
obsolete/superseded triage
patch bundle inputs
validation and stop conditions
```

## Scope

Allowed:

```text
reduce duplicated Markdown
replace repeated command blocks with canonical links
mark historical/superseded/domain-only status
update documentation indexes
prepare manual-review patch bundles
include script/tool inventory in refactor evidence
```

Forbidden without explicit human approval:

```text
delete Markdown files
move files across major folders
remove compact evidence snapshots
hand-edit generated indexes
commit output/**
run Blender
run providers implicitly
merge to master
```

## Insert point in the parent 0 -> 10 procedure

Run this lane after the parent guide has completed:

```text
0. Sync repository and shell setup
1. Read repository instructions and reference docs
2. Discover existing tools/helpers before proposing refactor
```

Then continue with this MD lane before provider-heavy planning.

## MD lane step A: build documentation and script inventories

```powershell
$MdRefactorStamp = $Stamp

python .\Tools\validation\build_markdown_inventory.py `
  --repo-root . `
  --output ".\output\validation\markdown_inventory_refactor_$MdRefactorStamp.json" `
  --markdown-output ".\output\validation\markdown_inventory_refactor_$MdRefactorStamp.md"

python .\Tools\validation\build_script_inventory.py `
  --repo-root . `
  --output ".\output\validation\script_inventory_refactor_$MdRefactorStamp.json" `
  --csv-output ".\output\validation\script_inventory_refactor_$MdRefactorStamp.csv" `
  --markdown-output ".\output\validation\script_inventory_refactor_$MdRefactorStamp.md"
```

Inspect the summaries:

```powershell
$MdInv = Get-Content ".\output\validation\markdown_inventory_refactor_$MdRefactorStamp.json" -Raw | ConvertFrom-Json
$ScriptInv = Get-Content ".\output\validation\script_inventory_refactor_$MdRefactorStamp.json" -Raw | ConvertFrom-Json

$MdInv | Select-Object passed, markdown_count, missing_index_count, prune_candidate_count, errors, warnings
$MdInv.category_counts
$MdInv.lifecycle_counts

$ScriptInv | Select-Object passed, script_count, syntax_warning_count, errors, warnings
$ScriptInv.category_counts
```

## MD lane step B: provide evidence to local AI

Add these files to the local AI/refactor context set:

```text
docs/README.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md
docs/LOCAL_AI_TASKS/code-refactor-md-lane-extension.md
output/validation/markdown_inventory_refactor_<STAMP>.json
output/validation/markdown_inventory_refactor_<STAMP>.md
output/validation/script_inventory_refactor_<STAMP>.json
output/validation/script_inventory_refactor_<STAMP>.csv
output/validation/script_inventory_refactor_<STAMP>.md
```

The local AI must treat:

```text
Markdown inventory -> documentation lifecycle and obsolete/superseded detection
Script inventory -> tool/script discovery and callable surface
Python line-count CSV -> size/complexity signal
```

## MD lane step C: classification required from local AI

For each Markdown candidate, the local AI must classify it as exactly one:

| Status | Meaning |
|---|---|
| `canonical` | Required in the single reading flow. |
| `maintained` | Stable source doc indexed from `docs/README.md`. |
| `task-current` | Current local AI task runbook. |
| `task-historical` | Past state or handoff; not primary reading path. |
| `evidence-snapshot` | Compact evidence; not source documentation. |
| `generated-context` | Generated/index context; do not hand-edit. |
| `domain-only` | Blender/application doc. Read only for that domain. |
| `superseded` | Replaced by a canonical/current doc. |
| `delete-candidate` | Candidate for later deletion; no delete in this lane. |

## MD lane step D: patch proposal rules

The local AI may propose a patch only if it includes:

```text
exact target files
before/after intent
line reduction estimate
risk classification
validation commands
stop conditions
whether deletion would be required later
```

Patch proposal style:

```text
one logical documentation seam per patch
entrypoint compression before deletion
historical/superseded markers before removal
no raw output/** commit
no generated-index hand edit
```

## MD lane step E: optional patch bundle inputs

When building a compact evidence/patch bundle, include these reports and artifacts if present:

```text
output/validation/markdown_inventory_refactor_<STAMP>.json
output/validation/markdown_inventory_refactor_<STAMP>.md
output/validation/script_inventory_refactor_<STAMP>.json
output/validation/script_inventory_refactor_<STAMP>.csv
output/validation/script_inventory_refactor_<STAMP>.md
output/validation/docs_links_<STAMP>.json
output/validation/validation_report_contract_<STAMP>.json
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/LOCAL_AI_TASKS/code-refactor-md-lane-extension.md
```

Do not commit the raw `output/**` files. Convert only selected summaries into compact evidence under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
```

## MD lane validation block

```powershell
python -m py_compile .\Tools\validation\build_markdown_inventory.py .\Tools\validation\build_script_inventory.py

python .\Tools\validation\check_docs_links.py `
  --repo-root . `
  --output ".\output\validation\docs_links_$MdRefactorStamp.json"

python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --output ".\output\validation\validation_report_contract_$MdRefactorStamp.json"

git diff --check
git status --short
```

## Expected output from local AI

The local AI should produce a concise refactor result with:

```text
inventory summary
single reading flow status
Markdown files touched
line count before/after for touched Markdown files
obsolete/superseded candidates not deleted
task-current vs task-historical classification
script/tool inventory summary
patch bundle contents or PR files
validation results
next deletion candidates requiring approval
```

## Acceptance criteria

```text
parent code-refactor guide remains canonical
MD lane is evidence-driven
script inventory is included in refactor context
Markdown redundancy is reduced or candidates are listed
obsolete files are classified before deletion
no deletion without explicit approval
no provider or Blender execution unless explicitly requested
```
