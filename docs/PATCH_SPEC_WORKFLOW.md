# Patch Spec Workflow

## Status

Compact required workflow bridge for patch-spec and PatchKit work.

This file is required by the `project_self_improvement` context-pack profile and
is intentionally kept as a small routing document. It does not authorize source
writes by itself.

## Source-write boundary

Current controlled source-write mechanisms:

```text
patch_specs/<bundle>/bundle.json
patch_specs/<bundle>/fragments/*.py
patch_specs/<bundle>/fragments/*.ps1
Tools/ai/patchkit/apply_patch_bundle.py
Tools/ai/generated_patch_specs/apply_cli.py
```

Patch notes, proposal ledgers and generated summaries are review inputs only.
They must be converted into deterministic patch operations or branch diffs before
source files are modified.

## Standard local sequence

```powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = (Resolve-Path .).Path

& $RepoPy -m Tools.ai apply_patch_bundle `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json `
  --dry-run

& $RepoPy -m Tools.ai apply_patch_bundle `
  --repo-root . `
  --bundle .\patch_specs\<bundle>\bundle.json
```

## Required validation posture

Before a patch-spec or patch bundle is treated as reviewable:

```text
inspect current source
verify target files exist
avoid output/**, renders/**, *.db, *.sqlite, indexAI/code_chunks/**
run py_compile or focused validator when Python changes
run git diff --check
report resulting line counts for scripts/code
record unavailable/degraded provider lanes as evidence, not success
```

## Read next

```text
../AGENTS.md
AI_DOCS_ENTRYPOINT.md
LOCAL_AI_TASKS/patch-suggestion-review-workflow-2026-05-07.md
LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
../patch_specs/README.md
../Tools/ai/patchkit/apply_patch_bundle.py
```
