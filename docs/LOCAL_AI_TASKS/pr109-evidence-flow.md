# PR109 evidence flow

## Purpose

This note gives the short operational flow for PR #109 after GitHub-only preparation, local wiring, post-wiring evidence generation and before merge review.

It complements:

```text
docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md
```

## Completed flow

```text
entry Markdown / PR state
-> sync official PR branch
-> local compile and hygiene gate
-> controlled local wiring
-> focused single-run validators
-> collect raw reports under ignored output/**
-> build compact evidence bundle under docs/LOCAL_VALIDATION_EVIDENCE/
-> validate compact bundle
-> stage only source wiring + compact evidence
-> push PR branch
-> GitHub audit from committed evidence
-> final docs refresh
-> merge review
```

## Entry sources

```text
PR: #109
branch: codex/design-code-patch-plan-lane
audit note: docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md
module execution note: docs/LOCAL_AI_TASKS/pr109-pythonpath-module-execution-note-2026-05-02.md
wired orchestrator: ia_carmine/product/repository_product/github_evidence_bundle.py
```

PR #110 / `codex/refactor-workspace-109` is scratch-only and must not be merged.

## Run levels

```text
focused run = py_compile + check_python_syntax + static report + bundle validation
multi run = selected validator batch over ia_carmine and Tools/validation
macro run = broader local validation runner / dry-run matrix when workstation time allows
```

For PR #109 final review, the focused run and compact post-wiring bundle are the required evidence. Multi/macro runs remain future optional validation layers.

## Evidence boundary

Raw evidence remains local and ignored:

```text
output/validation/*.json
output/analysis/*.json
output/analysis/*.md
output/patch_specs/*.json
output/patch_specs/*.md
```

Git-tracked evidence is compact, bounded and timestamped:

```text
docs/LOCAL_VALIDATION_EVIDENCE/<purpose>_<YYYYMMDD-HHMMSS>.json
docs/LOCAL_VALIDATION_EVIDENCE/<purpose>_<YYYYMMDD-HHMMSS>.md
```

## Push boundary

Allowed to stage:

```text
reviewed source/doc changes
compact evidence bundle JSON/Markdown
small task notes
```

Forbidden to stage:

```text
raw output/**
full analysis JSON
SQLite/database files
runtime media
render outputs
large provider transcripts
```

## Post-wiring evidence

Committed post-wiring bundle:

```text
docs/LOCAL_VALIDATION_EVIDENCE/pr109_after_wiring_bundle_20260502-192916.json
docs/LOCAL_VALIDATION_EVIDENCE/pr109_after_wiring_bundle_20260502-192916.md
```

Expected/observed decision boundary:

```text
artifact_manifest_built=true
included_artifacts_built=true
included_artifact_count=4
provider_execution_seen=false
selected_chunks_evidence_seen=true
selected_chunks_built=true
budget_respected=true
```

`patch_plan_summary_seen=false` is acceptable for this final post-wiring bundle because it contains syntax and static interpreter reports, not a native patch-plan report.

## Merge gate

PR #109 can be merged only when:

```text
local wiring commit is pushed
fresh compact evidence bundle is pushed
bundle evidence confirms no provider execution and no patch auto-apply
GitHub reports PR #109 mergeable
review threads are resolved
manual review confirms no raw output/** or forbidden artifacts are committed
```
