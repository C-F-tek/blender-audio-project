# Repository Hygiene Cleanup and Refactor Procedure — 2026-05-09

## Purpose

Define the automatic, reviewable procedure for keeping repository documentation, indexes, discovery surfaces and patch/refactor candidates coherent.

This is not a free-form delete pass. It is a controlled loop:

```text
discovery
  -> code-aware coherence
  -> hygiene classification
  -> split/refactor candidate map
  -> PatchKit cleanup bundle
  -> validators
  -> review PR
```

## Current doctrine

```text
read/reuse/code-driven first
classification before delete
delete only through allowlisted PatchKit bundle or explicit PR diff
refactor candidates are mapped before source changes
heap/exchange and patchkit docs are current product boundaries
old but useful material is routed or archived, not blindly removed
```

## Reused existing tools

| Tool | Role |
|---|---|
| `Tools/docs/build_code_aware_md_coherence.py` | Scans Markdown references/commands against current code and script args. |
| `Tools/docs/refactor_markdown_splits.py` | Migrates legacy split folders, splits monolithic Markdown and prunes explicit obsolete snapshots allowlist-only. |
| `Tools/docs/build_repo_hygiene_plan.py` | Builds a repo hygiene classification plan and optional PatchKit cleanup bundle. |
| `Tools/ai/patchkit/apply_patch_bundle.py` | Applies guarded idempotent patch bundles, now including marker-protected `delete_file`. |
| `Tools/validation/check_docs_links.py` | Validates Markdown links after classification/split/delete. |
| `Tools/validation/check_markdown_line_limits.py` | Validates Markdown line budgets. |
| `Tools/validation/check_file_line_limits.py` | Validates broader file line budgets. |
| `Tools/validation/run_patchkit_smoke.py` | Verifies PatchKit dry/apply/idempotency behavior. |

## Phase 1 — discovery and coherence report

```powershell
$RepoPy = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = (Resolve-Path .).Path

& $RepoPy .\Tools\docs\build_code_aware_md_coherence.py `
  --repo-root . `
  --output output\validation\md_code_coherence_report.json `
  --markdown-output output\validation\md_code_coherence_report.md
```

Use this report to detect:

```text
missing referenced files
stale command flags
active Markdown over line budget
historical/handoff references
placeholder or evidence-only references
```

## Phase 2 — hygiene classification and cleanup bundle generation

```powershell
& $RepoPy .\Tools\docs\build_repo_hygiene_plan.py `
  --repo-root . `
  --output output\validation\repo_hygiene_plan.json `
  --markdown-output output\validation\repo_hygiene_plan.md `
  --emit-patchkit-bundle patch_specs\repo_hygiene_cleanup\bundle.json
```

The plan classifies files as:

```text
current_oriented
historical_chat_handoff
obsolete_split_snapshot
obsolete_reference
historical_with_commands
oversized_current
oversized_noncanonical
legacy_split_layout
unclassified
```

Only high-confidence obsolete files with explicit markers become PatchKit `delete_file` operations.

## Phase 3 — split/refactor candidates

Use `refactor_markdown_splits.py` for structural hygiene:

```powershell
& $RepoPy .\Tools\docs\refactor_markdown_splits.py `
  --repo-root . `
  --migrate-legacy-splits `
  --split-monolithic `
  --output output\validation\markdown_refactor_report.json `
  --markdown-output output\validation\markdown_refactor_report.md
```

Apply only after reviewing the dry-run report:

```powershell
& $RepoPy .\Tools\docs\refactor_markdown_splits.py `
  --repo-root . `
  --apply `
  --migrate-legacy-splits `
  --split-monolithic `
  --output output\validation\markdown_refactor_report_apply.json `
  --markdown-output output\validation\markdown_refactor_report_apply.md
```

## Phase 4 — PatchKit cleanup bundle dry-run/apply

Dry-run first:

```powershell
& $RepoPy .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\repo_hygiene_cleanup\bundle.json `
  --dry-run `
  --output output\validation\repo_hygiene_patchkit_dry_run.json `
  --markdown-output output\validation\repo_hygiene_patchkit_dry_run.md
```

Apply only on a dedicated cleanup branch:

```powershell
& $RepoPy .\Tools\ai\patchkit\apply_patch_bundle.py `
  --repo-root . `
  --bundle .\patch_specs\repo_hygiene_cleanup\bundle.json `
  --output output\validation\repo_hygiene_patchkit_apply.json `
  --markdown-output output\validation\repo_hygiene_patchkit_apply.md
```

`delete_file` requires:

```text
operation = delete_file
allow_delete = true
required_marker present in target file
path not under denied generated/runtime prefixes
path not DB/SQLite
```

## Phase 5 — validation

```powershell
& $RepoPy -m py_compile `
  .\Tools\docs\build_repo_hygiene_plan.py `
  .\Tools\docs\build_code_aware_md_coherence.py `
  .\Tools\docs\refactor_markdown_splits.py `
  .\Tools\ai\patchkit\apply_patch_bundle.py `
  .\Tools\validation\run_patchkit_smoke.py

& $RepoPy .\Tools\validation\run_patchkit_smoke.py --repo-root .
& $RepoPy .\Tools\validation\check_docs_links.py --repo-root . --output output\validation\docs_links_after_hygiene.json
& $RepoPy .\Tools\validation\check_markdown_line_limits.py --repo-root . --max-lines 500 --output output\validation\markdown_line_limits_after_hygiene.json
& $RepoPy .\Tools\validation\check_file_line_limits.py --repo-root . --output output\validation\file_line_limits_after_hygiene.json

git diff --check
git status --short
```

## Review policy

Commit only:

```text
source/tool changes
procedure docs
PatchKit bundle specs/fragments when intentionally reviewed
actual file deletions from source tree when the PR is a cleanup PR
```

Do not commit:

```text
output/**
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
*.db
*.sqlite
*.sqlite3
```

## Refactor policy

This procedure may discover refactor candidates. It must not automatically perform broad refactors.

Refactor candidates should become one of:

```text
PatchKit bundle when the change is small, anchorable and idempotent
normal code PR when the change is semantic or multi-file
problems.md / TECH_DEBT_TRACKER entry when unresolved
split/refactor report when the issue is documentation structure
```

## Acceptance criteria

A cleanup/refactor PR is acceptable when:

```text
cleanup candidates come from generated plan or existing classified docs
all deletes are explicit and reviewable
no generated/runtime/DB paths are deleted by automation
PatchKit dry-run passes before apply
link and line-limit checks are run or listed as pending
PR body lists deleted/classified/refactored files
line counts are reported for touched scripts
```
