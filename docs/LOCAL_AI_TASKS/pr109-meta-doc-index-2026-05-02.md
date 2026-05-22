# PR109 meta-documentation index — 2026-05-02

## Purpose

Compact index of PR #109 meta-documents created during GitHub-only preparation.

Use this file as the first read when resuming locally.

## Read order

```text
1. docs/LOCAL_AI_TASKS/pr109-pre-return-status-2026-05-02.md
2. docs/LOCAL_AI_TASKS/pr109-pythonpath-module-execution-note-2026-05-02.md
3. docs/LOCAL_AI_TASKS/pr109-docs-only-phase-log-2026-05-02.md
4. docs/LOCAL_AI_TASKS/pr109-evidence-flow.md
5. docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md
6. docs/LOCAL_AI_TASKS/open-pr-triage-2026-05-02.md
7. docs/LOCAL_AI_TASKS/open-issue-triage-2026-05-02.md
```

## File purposes

### `pr109-pre-return-status-2026-05-02.md`

```text
single-page snapshot
current PR stack
hard blocker
what to do / what not to do at workstation
```

### `pr109-pythonpath-module-execution-note-2026-05-02.md`

```text
PYTHONPATH setup for modularized Tools.* imports
preferred python -m execution style
bundle rebuild example using package-style execution
```

### `pr109-docs-only-phase-log-2026-05-02.md`

```text
GitHub-only docs/metadata phase boundary
completed docs-only tasks
explicit stop condition before local validation resumes
```

### `pr109-evidence-flow.md`

```text
short operational evidence flow
run levels: focused, multi, macro
raw evidence versus compact Git evidence boundary
merge gate
```

### `pr109-prelocal-github-only-audit.md`

```text
detailed audit
local command blocks
wiring sequence
bundle rebuild sequence
long touched-file inventory
```

### `open-pr-triage-2026-05-02.md`

```text
open and closed PR state
recommended PR ordering
PR #110 scratch-only handling
```

### `open-issue-triage-2026-05-02.md`

```text
open issues #57 and #104
future queue
risk classification for docs cleanup versus provider/GPU work
```

## Local resume rule

Do not start with merge/rebase/cleanup. Start with sync, status, diff check and compile gates from the pre-return status note.

When running modularized `Tools.*` entry points directly from PowerShell, set:

```powershell
$env:PYTHONPATH = (Get-Location).Path
```

Prefer package execution:

```powershell
python -m ia_carmine.product.repository_product.github_evidence_bundle --help
python -m Tools.validation check_github_evidence_bundle --help
```
