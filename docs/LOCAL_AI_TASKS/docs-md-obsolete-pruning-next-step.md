# Local AI Entrypoint: Markdown Obsolete Pruning Next Step

This task starts after the entrypoint reduction and script inventory PR.

## Purpose

Continue Markdown cleanup by identifying obsolete, superseded and historical files without deleting anything automatically.

The objective is a reviewable patch bundle or PR that contains:

```text
single reading flow validation
Markdown inventory summary
script/tool inventory summary
obsolete/superseded candidates
historical task classification
candidate deletion list requiring explicit approval
validator/catalog cleanup proposal
```

## Required reading order

```text
AGENTS.md
README.md
WORKFLOW.md
docs/README.md
docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
Tools/validation/README.md
docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md
```

If any required file is missing, stop and report.

## Scope

Allowed:

```text
mark Markdown files as historical or superseded
replace duplicated command blocks with links
update indexes
produce compact evidence
produce patch bundle proposal
shorten Tools/validation/README.md into a catalog if local patch apply is available
```

Forbidden without explicit approval:

```text
delete files
move files across major folders
remove evidence snapshots
rewrite generated indexes manually
commit output/**
run Blender
run providers
merge to master
```

## Preflight

```powershell
git fetch origin
git switch master
git pull --ff-only origin master
git status --short
$env:PYTHONPATH = (Get-Location).Path
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
```

Create a branch:

```powershell
git switch -c codex/docs-md-obsolete-pruning-$Stamp
```

## Inventories

```powershell
python .\Tools\validation\build_markdown_inventory.py `
  --repo-root . `
  --output .\output\validation\markdown_inventory_$Stamp.json `
  --markdown-output .\output\validation\markdown_inventory_$Stamp.md

python .\Tools\validation\build_script_inventory.py `
  --repo-root . `
  --output .\output\validation\script_inventory_$Stamp.json `
  --csv-output .\output\validation\script_inventory_$Stamp.csv `
  --markdown-output .\output\validation\script_inventory_$Stamp.md
```

Inspect:

```powershell
$MdInv = Get-Content ".\output\validation\markdown_inventory_$Stamp.json" -Raw | ConvertFrom-Json
$ScriptInv = Get-Content ".\output\validation\script_inventory_$Stamp.json" -Raw | ConvertFrom-Json

$MdInv | Select-Object passed, markdown_count, missing_index_count, prune_candidate_count, errors, warnings
$MdInv.category_counts
$MdInv.lifecycle_counts
$MdInv.missing_index | Select-Object path, category, lifecycle, lines, heading | Format-Table -AutoSize
$MdInv.prune_candidates | Select-Object path, category, lifecycle, lines, heading | Format-Table -AutoSize

$ScriptInv | Select-Object passed, script_count, syntax_warning_count, errors, warnings
$ScriptInv.category_counts
```

## Obsolete triage rules

Classify every candidate as exactly one:

| Status | Meaning |
|---|---|
| `canonical` | Part of the single reading flow. Keep concise. |
| `maintained` | Stable source doc, indexed from `docs/README.md`. |
| `task-current` | Current task runbook, indexed from `docs/LOCAL_AI_TASKS/README.md`. |
| `task-historical` | Past state/handoff, preserved but not primary reading path. |
| `evidence-snapshot` | Compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/`; not source doc. |
| `generated-context` | Generated/index context; do not hand-edit. |
| `domain-only` | Blender/application-domain doc. Read only for that task area. |
| `superseded` | Replaced by a canonical/current doc. Keep marker; deletion later requires approval. |
| `delete-candidate` | Safe-looking removal candidate, but do not delete without explicit approval. |

## Required triage report

Create or update a stable report only if it is indexed:

```text
docs/DOCUMENTATION_OBSOLETE_TRIAGE.md
```

Required sections:

```text
inventory summary
single reading flow check
stable docs requiring index update
task-current list
task-historical list
evidence snapshot exclusion list
generated-context exclusion list
superseded candidates
delete candidates requiring approval
Tools/validation README reduction plan
next patch bundle contents
validation results
```

## Tools/validation README reduction plan

If reducing `Tools/validation/README.md`, preserve only:

```text
purpose
common report contract
core validator catalog
inventory builder catalog
AI/provider/report validator catalog
NPU/helper validator catalog
Blender/generated-file validator catalog
standard minimal validation block
guardrails
```

Move or link long procedural blocks to existing canonical runbooks instead of keeping them in the README.

## Validation

```powershell
python -m py_compile .\Tools\validation\build_markdown_inventory.py .\Tools\validation\build_script_inventory.py
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links_$Stamp.json
python .\Tools\validation\check_validation_report_contract.py --repo-root . --output .\output\validation\validation_report_contract_$Stamp.json
git diff --check
git status --short
```

## Optional compact evidence bundle

Do not commit raw `output/**`.

If evidence is needed for GitHub-only review, build a compact bundle using the existing evidence tooling and include these inputs:

```text
output/validation/markdown_inventory_$Stamp.json
output/validation/markdown_inventory_$Stamp.md
output/validation/script_inventory_$Stamp.json
output/validation/script_inventory_$Stamp.csv
output/validation/script_inventory_$Stamp.md
output/validation/docs_links_$Stamp.json
output/validation/validation_report_contract_$Stamp.json
docs/DOCUMENTATION_OBSOLETE_TRIAGE.md
```

Expected committed evidence, only if needed:

```text
docs/LOCAL_VALIDATION_EVIDENCE/docs_md_obsolete_triage_bundle_$Stamp.json
docs/LOCAL_VALIDATION_EVIDENCE/docs_md_obsolete_triage_bundle_$Stamp.md
```

## Acceptance criteria

```text
no file deleted
single reading flow preserved
obsolete/superseded candidates listed
script inventory included in refactor evidence path
Tools/validation README reduction either applied or listed as next patch
local validation commands included
raw output/** not committed
```
