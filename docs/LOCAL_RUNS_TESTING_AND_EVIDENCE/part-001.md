<!-- IA-CARMINE-MD-SPLIT: part -->
# LOCAL_RUNS_TESTING_AND_EVIDENCE — parte 001 di 002

Sorgente indice: [`../LOCAL_RUNS_TESTING_AND_EVIDENCE.md`](../LOCAL_RUNS_TESTING_AND_EVIDENCE.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

# Local Runs, Testing and Evidence Guide

## Purpose

This guide defines the common operating model for local IA-Carmine runs, GitHub-driven Markdown task startup, validation phases, `output/**` handling and evidence bundle promotion.

Use it as the general policy layer for local test gates and effective runs. Task-specific documents may add stricter steps, but should not weaken these rules.

## Core principles

Local AI work must be:

```text
reproducible from Markdown task files
provider-explicit
report-first
manual-review-first
artifact-bundled
safe to inspect from GitHub
safe to rerun locally
```

Default constraints:

```text
no implicit provider execution
no implicit Blender runtime
no automatic patch application
no full analysis JSON commit
no SQLite/database commit
no output/** commit
no git add .
no force-push
no merge to master without explicit command
```

## Starting from GitHub Markdown

A local run should start from a GitHub-tracked Markdown task whenever possible.

Preferred task sources:

```text
docs/LOCAL_AI_TASKS/*.md
docs/LOCAL_RUNS_TESTING_AND_EVIDENCE.md
docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md
docs/AGENT_REVIEW_CODE_PATCH_PLAN.md
docs/CONTRACT_DRIFT_VALIDATION.md
```

Basic startup sequence:

```powershell
cd C:\Users\carmi\blender\blender-audio-project

git fetch origin
git status --short
git branch --show-current
git log --oneline -5
```

If testing a PR branch:

```powershell
git switch <branch-name>
git pull --ff-only origin <branch-name>
git status --short
```

If testing multiple PRs together, create a local integration branch:

```powershell
git switch master
git pull --ff-only origin master
git switch -c local/<purpose>-integration
```

For stacked local testing, merge PR branches with explicit commits between merges:

```powershell
git merge --no-ff --no-commit origin/<first-pr-branch>
git diff --check
git commit -m "test: stack first PR for local validation"

git merge --no-ff --no-commit origin/<second-pr-branch>
git diff --check
git commit -m "test: stack second PR for local validation"
```

Do not push local integration branches unless there is a deliberate need to share the integration state.

## Test run versus effective run

### Test run

A test run validates commands, report contracts and artifact structure.

Allowed outputs:

```text
output/validation/*.json
output/validation/*.md
output/patch_specs/*.json
output/patch_specs/*.md
docs/LOCAL_VALIDATION_EVIDENCE/<compact-test-evidence>.json
docs/LOCAL_VALIDATION_EVIDENCE/<compact-test-evidence>.md
docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_<stamp>.csv
```

Test runs must remain provider-free unless a task explicitly requests a provider probe.

### Effective run

An effective run may produce real review outputs intended for manual promotion.

Effective runs still default to:

```text
manual review required
provider execution explicit
patch application disabled unless separately authorized
source writes disabled unless the task is explicitly an implementation branch
```

Effective run evidence should still be compacted before versioning.

## Output directory policy

`output/**` is a local working area.

Allowed in `output/**`:

```text
raw validator JSON
raw validator Markdown
patch-spec drafts
local dry-run manifests
intermediate agent review reports
runtime-local diagnostics
```

Forbidden to commit from `output/**`:

```text
all output/** files by default
full analysis JSON
large raw review JSON
runtime media
Blender outputs
SQLite/database files
provider raw transcripts unless explicitly reviewed and compacted
```

Before any commit:

```powershell
git status --short
git diff --cached --name-only
```

If any `output/**` file is staged, stop and unstage it:

```powershell
git restore --staged output
```

## Compact evidence policy

Only compact, reviewable artifacts belong in Git by default.

Preferred evidence directory:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
```

Allowed evidence types:

```text
macro validation bundle JSON
macro validation bundle Markdown
python line-count CSV with timestamp
small curated fixture JSON
small schema/contract evidence
```

Avoid versioning mutable latest files unless there is a deliberate reason:

```text
python_line_count_latest.csv
latest.json
latest.md
```

Prefer timestamped files:

```text
python_line_count_YYYYMMDD-HHMMSS.csv
macro_pr108_pr109_validation_YYYYMMDD-HHMMSS.json
macro_pr108_pr109_validation_YYYYMMDD-HHMMSS.md
```

## Python line-count evidence

Generate fresh line-count evidence after meaningful script changes or before macro promotion:

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

python .\Tools\validation\build_python_line_count_csv.py `
  --repo-root . `
  --csv-output ".\docs\LOCAL_VALIDATION_EVIDENCE\python_line_count_$Stamp.csv" `
  --report-output .\output\validation\python_line_count_macro.json `
  --markdown-output .\output\validation\python_line_count_macro.md
```

Use the CSV to prioritize refactor candidates:

```text
large + unrelated legacy file = do not touch during focused PR
medium-size new file = good refactor candidate
new shared patterns = extract common helper
high-risk runtime file = require separate implementation branch
```

## Standard validation phases

A robust local validation run should use layers.

### Syntax and basic repository hygiene

```powershell
python .\Tools\validation\check_python_syntax.py `
  --repo-root . `
  --output .\output\validation\python_syntax_macro.json

git diff --check
```

### Documentation hygiene

```powershell
python .\Tools\validation\check_docs_links.py `
  --repo-root . `
  --output .\output\validation\docs_links_macro.json

# Removed obsolete check_markdown_command_hygiene.py command; the script is not tracked in current master. Use check_docs_links.py plus check_validation_report_contract.py for this gate.
```

### Contract drift

```powershell
python .\Tools\validation\check_code_contract_drift.py `
  --repo-root . `
  --output .\output\validation\code_contract_drift.json `
  --markdown-output .\output\validation\code_contract_drift.md

python .\Tools\validation\check_docs_contract_drift.py `
  --repo-root . `
  --output .\output\validation\docs_contract_drift.json `
  --markdown-output .\output\validation\docs_contract_drift.md
```

### Agnostic context stack

```powershell
python .\Tools\validation\check_core_activation_agnostic_contract.py `
  --repo-root . `
  --output .\output\validation\core_activation_agnostic_contract.json `
  --markdown-output .\output\validation\core_activation_agnostic_contract.md

python .\Tools\validation\run_agnostic_context_stack_smoke.py `
  --repo-root . `
  --dry-run `
  --output .\output\validation\agnostic_context_stack_smoke_dryrun.json `
  --markdown-output .\output\validation\agnostic_context_stack_smoke_dryrun.md
```

### Code patch-plan lane

```powershell
python .\Tools\ai\build_agent_review_code_patch_plan.py `
  --repo-root . `
  --code-contract-drift-report .\output\validation\code_contract_drift.json `
  --output .\output\patch_specs\agent_review_code_patch_plan_macro.json `
  --markdown-output .\output\patch_specs\agent_review_code_patch_plan_macro.md

python .\Tools\validation\run_agent_review_code_patch_plan_smoke.py `
  --repo-root . `
  --report .\output\patch_specs\agent_review_code_patch_plan_macro.json `
  --output .\output\validation\agent_review_code_patch_plan_smoke_macro_built.json

python .\Tools\ai\build_code_patch_docs_followup.py `
  --repo-root . `
  --code-patch-plan .\output\patch_specs\agent_review_code_patch_plan_macro.json `
  --output .\output\patch_specs\agent_review_code_docs_followup_macro.json `
  --markdown-output .\output\patch_specs\agent_review_code_docs_followup_macro.md

python .\Tools\ai\build_code_patch_artifact_pack.py `
  --repo-root . `
  --code-patch-plan .\output\patch_specs\agent_review_code_patch_plan_macro.json `
  --docs-followup .\output\patch_specs\agent_review_code_docs_followup_macro.json `
  --output .\output\validation\code_patch_artifact_pack_macro.json `
  --markdown-output .\output\validation\code_patch_artifact_pack_macro.md
```

## Test bundle construction

A test bundle proves that validators and report contracts passed.

Use one stamp across the run:

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
```

Build the report list dynamically so optional reports do not break the bundle:

```powershell
$Reports = @(
  ".\output\validation\python_syntax_macro.json",
  ".\output\validation\python_line_count_macro.json",
  ".\output\validation\docs_links_macro.json",
  ".\output\validation\markdown_command_hygiene_macro.json",
  ".\output\validation\core_activation_agnostic_contract.json",
  ".\output\validation\agnostic_context_stack_smoke_dryrun.json",
  ".\output\validation\agent_review_code_patch_plan_smoke_macro_built.json",
  ".\output\validation\code_patch_artifact_pack_macro.json",
  ".\output\validation\json_artifacts_macro.json",
  ".\output\validation\validation_report_contract_macro.json",
  ".\output\validation\github_evidence_bundle_macro.json",
  ".\output\validation\code_contract_drift.json",
  ".\output\validation\docs_contract_drift.json"
) | Where-Object { Test-Path $_ }
```

Build the compact evidence bundle:

```powershell
python .\Tools\ai\build_github_evidence_bundle.py `
  --repo-root . `
  --basename macro_validation_$Stamp `
  --output-dir docs/LOCAL_VALIDATION_EVIDENCE `
  --report ($Reports -join ',')
```

Validate the bundle:

```powershell
python .\Tools\validation\check_github_evidence_bundle.py `
  --repo-root . `
  --bundle ".\docs\LOCAL_VALIDATION_EVIDENCE\macro_validation_$Stamp.json" `
  --output ".\output\validation\macro_validation_${Stamp}_bundle_validation.json"
```
