# Patch Suggestion Review Workflow

Status: active operating guide  
Date: 2026-05-07  
Scope: patch-note proposal ledgers, proposal-core bundle handoff and safe conversion into reviewed patch waves.

## Purpose

A `patch_notes_quality_product_<stamp>.json` file is a proposal ledger. It is not a patch bundle and must not be applied directly.

A `proposal_core` inside a GitHub evidence bundle is the compact, durable form of that same ledger. It exists so a later AI/session can inspect the proposals without reopening huge raw reports.

## Required Inputs

The review workflow starts from one of these artifacts:

```text
docs/LOCAL_VALIDATION_EVIDENCE/patch_notes_quality_product_<stamp>.json
docs/LOCAL_VALIDATION_EVIDENCE/patch_notes_quality_product_<stamp>.md
summary.proposal_core inside a GitHub evidence bundle
```

The minimum fields required for a proposal to be actionable are:

```text
id
area
target_files
summary
edit_strategy
validation_commands
stop_conditions
manual_review_required
```

## Lane Order

Review proposals in this order:

```text
1. python_python
2. python_doc
3. doc_doc
4. doc_python
```

This order prioritizes correctness of live code before documentation hygiene.

## Lane Semantics

### python_python

Use for real Python code problems, such as missing import modules or missing imported symbols.

Before applying:

```text
verify the target Python file exists on current branch
verify the imported module/symbol is still missing
reject stale findings when the module/path already exists
prefer minimal compatibility modules or corrected imports
validate with py_compile and targeted smoke
```

### python_doc

Use when a documented Python script lacks an obvious smoke/check/test.

Preferred patch:

```text
add small report-only smoke wrappers under Tools/validation
avoid importing or executing provider-heavy target modules unless safe
use py_compile-oriented checks when the goal is syntax/availability
preserve no-provider, no-Blender, no-FFmpeg and no-DB guardrails
```

### doc_doc

Use for Markdown-to-Markdown references.

Before applying:

```text
filter generated evidence references
filter fenced-code tree diagrams and placeholder paths
fix only active docs or convert obsolete sections to design-only status
avoid rewriting historical evidence bundles
```

### doc_python

Use for Markdown references to Python/PowerShell/script paths.

Before applying:

```text
confirm the referenced command is intended to be executable
separate examples/design notes from live commands
replace obsolete commands with design-only language when no wrapper exists
never create runtime wrappers only to satisfy stale docs
```

## Patch Conversion Rule

A proposal becomes a patch only after this sequence:

```text
proposal ledger entry
current-branch verification
stale/noise filtering
manual risk decision
small patch bundle or branch diff
py_compile/smoke/diff validation
reviewed commit/PR
```

If verification shows the reported issue is already fixed, do not patch. Record a stale-suggestion review note when useful.

## Evidence Policy

Allowed to commit:

```text
compact patch notes quality product JSON/MD
compact patch plan quality product JSON/MD
runtime telemetry summaries
capability manifests
proposal-core bundle summaries
manual stale-suggestion review docs
```

Not allowed to commit:

```text
output/**
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
*.db
*.sqlite
raw provider heap/runtime dumps
cloud_semantic_deterministic_chunks directories
```

## Bundle Handoff Requirement

When a patch-notes quality product participates in a GitHub evidence bundle, the compact bundle must carry:

```text
summary.proposal_core.patch_note_count
summary.proposal_core.area_counts
summary.proposal_core.notes[]
```

The proposal core must be complete enough to drive the next patch wave without needing chat memory.

## Stop Conditions

Stop before patching when:

```text
target file is missing or generated
finding is stale on current master
proposal has no target_files
proposal has no validation commands
patch would run Blender, FFmpeg, provider execution or DB writes
patch would modify output/** or generated evidence directories
patch requires secret, permission, billing, visibility or deploy changes
```

## Validation Template

Use the narrowest validation that proves the patch:

```powershell
python -m py_compile <changed-python-files>
python <targeted-smoke> --repo-root .
git diff --check
git status --short
```

For docs-only waves:

```powershell
git diff --check
python -m py_compile .\Tools\validation\check_docs_links.py
```

## Operational Note

Historical patch-note products can become stale after later PRs. Always refresh findings against the current branch before generating a patch bundle.
