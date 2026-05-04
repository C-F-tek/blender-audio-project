# Local AI Entrypoint: Markdown Obsolete Pruning Next Step

This task starts after the entrypoint reduction, unified launcher and script inventory PR work.

This file is a task brief. It is not a command catalog. Current executable commands live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

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
visibility/length policy compliance report
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
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/validation/README.md
```

Supporting historical references, read only when triaging old 0-to-10 duplication:

```text
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
add visibility-first and length-policy metadata to active docs
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

## Launcher route

Use the unified launcher for this task.

Required launcher phases:

```text
md
python
contract
full_validation
```

Optional phases when explicitly requested:

```text
context_pack
agent_state
evidence
patch_specs
provider
```

If provider-backed advisory is explicitly wanted later, use `Full0To10` or provider flags through the unified launcher. Do not start from legacy 0-to-10 runbooks as active entrypoints.

## Inventory ownership

Markdown and script inventories are produced by the launcher or by focused validator commands owned by `Tools/validation/README.md`.

For this task, report inventory results through compact surfaces:

```text
unified launcher manifest
phase_status
phase_reports
Markdown inventory summary
script inventory summary / CSV
triage report if created
```

## Visibility-first rule

Every report or proposed bundle must be readable from compact surfaces before opening detailed evidence.

Required order:

```text
launcher command
manifest or inventory summary
phase/report references
compact Markdown/CSV summary
detailed evidence only when needed
```

Do not create new monolithic AI-to-AI bundles without a companion manifest.

## Length policy

Active task files should remain compact.

| File type | Preferred maximum | Required action when exceeded |
|---|---:|---|
| Active task/runbook | ~500 lines | Split or link supporting docs. |
| Maintained source doc | ~700 lines | Add structure or split. |
| Generated compact evidence | ~1200 lines | Add manifest/summary. |
| Large evidence/historical bundle | Any size only if indexed | Never first entrypoint. |

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
visibility-first compliance check
length-policy compliance check
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
minimal validation ownership notes
guardrails
```

Move or link long procedural blocks to existing canonical runbooks instead of keeping them in the README.

## Optional compact evidence bundle

Do not commit raw `output/**`.

If evidence is needed for GitHub-only review, build a compact bundle through the unified launcher or evidence tooling and include only compact tracked summaries under:

```text
docs/LOCAL_VALIDATION_EVIDENCE/
```

## Acceptance criteria

```text
no file deleted unless explicitly approved
single reading flow preserved
unified launcher remains the active local-AI entrypoint
obsolete/superseded candidates listed
script inventory included in refactor evidence path
visibility-first compliance checked
length-policy compliance checked
Tools/validation README reduction either applied or listed as next patch
launcher validation evidence referenced
raw output/** not committed
```
