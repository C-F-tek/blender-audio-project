# PR109 evidence flow

## Purpose

This note gives the short operational flow for PR #109 after GitHub-only preparation and before merge review.

It complements:

```text
docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md
```

## Flow

```text
entry Markdown / PR state
-> sync official PR branch
-> local compile and hygiene gate
-> controlled local wiring
-> focused single-run validators
-> optional multi-run / macro validators
-> collect raw reports under ignored output/**
-> build compact evidence bundle under docs/LOCAL_VALIDATION_EVIDENCE/
-> validate compact bundle
-> stage only source wiring + compact evidence
-> push PR branch
-> GitHub audit from committed evidence
```

## Entry sources

```text
PR: #109
branch: codex/design-code-patch-plan-lane
audit note: docs/LOCAL_AI_TASKS/pr109-prelocal-github-only-audit.md
replacement-ready orchestrator: Tools/ai/github_evidence_bundle_build_github_evidence_bundle_ready.py
final target orchestrator: Tools/ai/build_github_evidence_bundle.py
```

PR #110 / `codex/refactor-workspace-109` is scratch-only and must not be merged.

## Run levels

```text
focused run = py_compile + check_python_syntax + static report + bundle validation
multi run = selected validator batch over Tools/ai and Tools/validation
macro run = broader local validation runner / dry-run matrix when workstation time allows
```

Start with the focused run. Move to multi/macro only after the focused run is green.

## Evidence boundary

Raw evidence remains local and ignored:

```text
output/validation/*.json
output/analysis/*.json
output/analysis/*.md
output/patch_specs/*.json
output/patch_specs/*.md
```

Git-tracked evidence must be compact, bounded and timestamped:

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

## Required post-wiring evidence

After locally copying the replacement-ready orchestrator over `Tools/ai/build_github_evidence_bundle.py`, build a fresh bundle and confirm at least:

```text
patch_plan_summary_seen=true
artifact_manifest_built=true
included_artifacts_built=true
included_artifact_count>=1
provider_execution_seen=false
```

## Merge gate

Do not merge PR #109 to `master` until:

```text
local wiring commit is pushed
fresh compact evidence bundle is pushed
bundle validation passes
manual review confirms no raw output/** or forbidden artifacts are staged
```
