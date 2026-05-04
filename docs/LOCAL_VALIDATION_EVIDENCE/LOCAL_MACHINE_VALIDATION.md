# Local Machine Validation Evidence Policy

## Purpose

This document defines how local-machine validation evidence must be produced, reviewed and shared with GitHub-only AI agents.

It complements the canonical refactor/full-toolbox procedures. It is not a replacement for task runbooks.

Use this file whenever a local run produces ignored artifacts under:

```text
output/**
renders/**
*.db
*.sqlite
*.sqlite3
```

The local machine may generate those artifacts, but only compact evidence should be committed.

## Canonical local validation flow

```text
run local validators / inventories / providers only when explicitly scoped
  -> write raw reports under output/**
  -> inspect summary fields locally
  -> build compact evidence bundle when needed
  -> validate compact evidence bundle
  -> commit only docs/LOCAL_VALIDATION_EVIDENCE/* compact outputs
  -> never commit raw output/**
```

## Required summary fields for local reports

Validation reports used as evidence should expose at least:

```text
schema_version
kind
repo_root
passed
errors
warnings
```

Provider/runtime reports should also expose, when relevant:

```text
provider_execution_performed
patch_application_performed
source_writes_performed
blender_runtime_executed
```

If older local reports are missing these fields, do not treat the whole task as failed automatically. Isolate the current task reports with `--report-file`.

## Report contract validation modes

Broad scan, useful for repository health but may fail on old local outputs:

```powershell
python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --output .\output\validation\validation_report_contract.json
```

Task-scoped scan, preferred for PR evidence:

```powershell
python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --report-file .\output\validation\markdown_inventory.json `
  --report-file .\output\validation\script_inventory.json `
  --report-file .\output\validation\docs_links.json `
  --output .\output\validation\validation_report_contract_task.json
```

Rule:

```text
Broad-scan failure on unrelated old output/validation files is technical debt.
Task-scoped failure on current reports is a blocker.
```

## Compact evidence policy

Allowed committed evidence:

```text
docs/LOCAL_VALIDATION_EVIDENCE/*.json
docs/LOCAL_VALIDATION_EVIDENCE/*.md
docs/LOCAL_VALIDATION_EVIDENCE/*.csv only when explicitly referenced by a compact bundle
```

Never commit:

```text
output/**
renders/**
*.db
*.sqlite
*.sqlite3
full raw provider transcripts unless compacted
large full analysis JSON unless explicitly approved
```

## Local-machine validation block

Recommended minimal validation for documentation/refactor PRs:

```powershell
python -m py_compile .\Tools\validation\build_markdown_inventory.py .\Tools\validation\build_script_inventory.py

python .\Tools\validation\build_markdown_inventory.py `
  --repo-root . `
  --output .\output\validation\markdown_inventory.json `
  --markdown-output .\output\validation\markdown_inventory.md

python .\Tools\validation\build_script_inventory.py `
  --repo-root . `
  --output .\output\validation\script_inventory.json `
  --csv-output .\output\validation\script_inventory.csv `
  --markdown-output .\output\validation\script_inventory.md

python .\Tools\validation\check_docs_links.py `
  --repo-root . `
  --output .\output\validation\docs_links.json

python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --report-file .\output\validation\markdown_inventory.json `
  --report-file .\output\validation\script_inventory.json `
  --report-file .\output\validation\docs_links.json `
  --output .\output\validation\validation_report_contract_task.json

git diff --check
git status --short
```

## Evidence handoff to GitHub-only AI

When reporting validation back to a GitHub-only AI or PR thread, include only compact summaries such as:

```text
report path
passed
kind
errors count
warnings count
provider_execution_performed
patch_application_performed
source_writes_performed
```

Example:

```text
docs_links.json: passed=True, errors={}, warnings={}
validation_report_contract_task.json: passed=True, report_count=3, errors={}, warnings={}
git diff --check: clean
git status --short: clean
```

Do not paste large raw JSON unless requested.

## Stop conditions

Stop and report if:

```text
current task-scoped contract validation fails
current docs links validation fails
raw output/** would be staged
compact evidence includes provider transcripts above review budget
patch application occurred without explicit request
Blender runtime executed outside explicit scope
```

## Relationship to 0 -> 10 refactor

The 0 -> 10 refactor procedure should include this file in its reading set and compact bundle artifacts whenever local validation evidence is produced.

For Markdown/doc refactor, also include:

```text
docs/LOCAL_AI_TASKS/code-refactor-md-lane-extension.md
```
