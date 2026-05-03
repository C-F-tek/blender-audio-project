# Documentation Map and Pruning Plan

## Purpose

This document is the control point for pruning and updating Markdown documentation in the repository.

The goal is to avoid adding another isolated Markdown file every time the project evolves. Any new stable document must either update an existing canonical document or explicitly retire/supersede older material.

This file is report-only. It does not authorize deletion by itself.

## Source baseline

Observed entry points on `master`:

```text
AGENTS.md
README.md
WORKFLOW.md
docs/README.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md
Tools/validation/README.md
Tools/npu/pipeline/README.md
```

Current project identity is broader than the historical Blender/audio repository name. The active architecture is local AI orchestration, provider-lane routing, evidence bundles, telemetry, repository consistency, deterministic recommendations and manual-review patch planning.

## Canonical entrypoint chain

| Rank | File | Role | Keep concise? | Notes |
|---:|---|---|---|---|
| 1 | `AGENTS.md` | Mandatory machine contract for AI agents. | Yes | Must stay hard-guardrail focused. Avoid duplicating detailed runbooks here. |
| 2 | `README.md` | Human project identity and high-level architecture. | Yes | Should describe the project and point to workflows, not duplicate every command. |
| 3 | `WORKFLOW.md` | Root operational workflow. | Yes | Should define lifecycle and validation blocks. Move long scenario-specific runs to task docs. |
| 4 | `docs/README.md` | Documentation index. | Yes | This is the stable MD map index. Every maintained stable doc should appear here or be intentionally excluded. |
| 5 | `docs/LOCAL_AI_RUN_BOOTSTRAP.md` | Local AI bootstrap contract. | Medium | Only local-run prerequisites and reading set. |
| 6 | `docs/LOCAL_AI_TASKS/README.md` | Task entrypoint index. | Yes | Only current task routing and historical task classification. |
| 7 | `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` | Canonical full-toolbox runbook. | No, but structured | This is allowed to be long because it is procedural. |
| 8 | `docs/LOCAL_AI_TASKS/shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md` | Current AI-to-AI next-task handoff. | Medium | Should stay repo-native and should supersede external handoff blobs. |
| 9 | `Tools/validation/README.md` | Validation command catalog. | Medium | Command catalog only; architectural policy belongs in docs. |
| 10 | `Tools/npu/pipeline/README.md` | NPU helper package contract. | Medium | Package-local contract only. |

## Repository Markdown families

| Family | Path pattern | Owner document | Lifecycle |
|---|---|---|---|
| Machine/human entrypoints | `AGENTS.md`, `README.md`, `WORKFLOW.md` | This file + `docs/README.md` | Canonical |
| Stable project documentation | `docs/*.md` | `docs/README.md` | Maintained source docs |
| Local AI task entrypoints | `docs/LOCAL_AI_TASKS/*.md` | `docs/LOCAL_AI_TASKS/README.md` | Current or historical tasks |
| Execution plans | `docs/EXECUTION_PLANS/**/*.md` | `docs/EXECUTION_PLANS/README.md` | State records |
| Compact validation evidence | `docs/LOCAL_VALIDATION_EVIDENCE/*.md` | Evidence bundle builders | Snapshot evidence, not source docs |
| Tool READMEs | `Tools/**/README.md` | Nearest package/tool owner | Package-local docs |
| Generated/index context | `indexAI/**/*.md`, `Tools/npu/npu_code_*.md` | Generators | Regenerated, not hand-maintained source |
| Blender application docs | `Scripting/**/*.md` | Package README / Blender domain docs | Application-domain docs |
| Root historical/policy notes | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md`, `CHANGELOG.md` | Root index or explicit references | Retain only if linked from canonical docs |

## Current duplication map

| Topic | Current repeated locations | Canonical target | Pruning rule |
|---|---|---|---|
| Provider lane policy | `AGENTS.md`, `README.md`, `WORKFLOW.md`, `docs/README.md`, `LOCAL_AI_TASKS/*` | `AGENTS.md` for hard rule, `WORKFLOW.md` for operation | Keep one-line pointers elsewhere. |
| Full-toolbox procedure | `WORKFLOW.md`, `docs/README.md`, `docs/LOCAL_AI_TASKS/README.md`, full-toolbox task file | `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` | Entry points link to it, not copy command blocks. |
| Evidence bundle requirements | `README.md`, `WORKFLOW.md`, `docs/README.md`, full-toolbox task file, handoff docs | `WORKFLOW.md` + full-toolbox task | Stable rule in `WORKFLOW.md`; run-specific list in task/evidence bundle. |
| Patch bundle policy | Root policy note, task docs, handoffs | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` | Do not duplicate ZIP structure everywhere. |
| Historical Blender role | `README.md`, `AGENTS.md`, `docs/README.md`, `MODULE_MAP.md` | `README.md` + `MODULE_MAP.md` | Keep overview once; detailed package docs under `Scripting/`. |
| Validation commands | `WORKFLOW.md`, `Tools/validation/README.md`, task docs | `Tools/validation/README.md` | Task docs list only focused task commands. |

## Missing evidence and tooling

The current docs have indexes and link validators, but the following controls were missing before this cleanup pass:

| Missing item | Why it matters | Resolution in this PR |
|---|---|---|
| Repository-wide Markdown inventory | We need evidence of all `.md` files before deciding what is missing, duplicated or obsolete. | Added `Tools/validation/build_markdown_inventory.py`. |
| Stable lifecycle labels for Markdown families | Evidence snapshots, runbooks and stable docs were easy to mix in review. | This document defines lifecycle classes. |
| Add-before-prune rule | New docs could be added without retiring or superseding older material. | This document defines the rule below. |
| Missing-index report | A doc can exist without appearing in a canonical index. | Inventory script reports `requires_index_review`. |
| Prune-candidate report | Misc Markdown can drift without owner/lifecycle. | Inventory script reports `prune_candidates`. |

## Add-before-prune rule

When adding a new Markdown file:

1. Decide whether the content belongs in an existing canonical document.
2. If a new file is still needed, add it to the correct owner index.
3. Mark the older overlapping document as one of:
   - `superseded by <path>`
   - `historical evidence`
   - `application-domain only`
   - `generated, do not hand-edit`
   - `delete candidate, requires explicit approval`
4. Do not delete files in the same pass unless the user explicitly approves deletion.
5. Run Markdown inventory and docs link validation.
6. Commit only the updated docs/source/evidence intended for review.

## Pruning policy

Safe without explicit deletion:

```text
- Update indexes.
- Add superseded/historical notes.
- Move task guidance into the canonical task index.
- Replace repeated command blocks with links to canonical runbooks.
- Generate inventory/evidence under output/validation.
```

Requires explicit user confirmation:

```text
- Delete Markdown files.
- Move files across major folders.
- Remove historical evidence.
- Remove runbooks still referenced by task files.
```

Never treat as manually maintained source:

```text
docs/LOCAL_VALIDATION_EVIDENCE/*.md
indexAI/**/*.md
Tools/npu/npu_code_context.md
Tools/npu/npu_code_index.md
output/**/*.md
```

## Inventory command

Use this before broad Markdown cleanup:

```powershell
python .\Tools\validation\build_markdown_inventory.py `
  --repo-root . `
  --output .\output\validation\markdown_inventory.json `
  --markdown-output .\output\validation\markdown_inventory.md
```

Then validate normal documentation links:

```powershell
python .\Tools\validation\check_docs_links.py `
  --repo-root . `
  --output .\output\validation\docs_links.json

python .\Tools\validation\check_validation_report_contract.py `
  --repo-root . `
  --output .\output\validation\validation_report_contract.json

git diff --check
```

## First cleanup sequence

1. Generate the Markdown inventory.
2. Review `missing_index[]` first.
3. Update `docs/README.md` and `docs/LOCAL_AI_TASKS/README.md` only for files that are intentionally maintained.
4. For historical task docs, keep them indexed as historical unless they are explicitly superseded.
5. For compact evidence docs, keep them out of stable reading order; evidence belongs in evidence bundles, not canonical onboarding.
6. Collapse repeated command blocks from entrypoints into links to canonical runbooks.
7. Only after the map is clean, propose explicit delete/move candidates in a separate PR.

## Acceptance criteria for this documentation lane

A documentation cleanup PR is acceptable when:

```text
- the entrypoint chain is explicit;
- every stable maintained MD file is indexed or intentionally excluded;
- generated/evidence MD files are not treated as source docs;
- each new MD addition supersedes, updates or links an older overlapping doc;
- no output/**, renders/**, *.db or *.sqlite files are committed;
- docs link validation and markdown inventory run locally;
- deletion candidates are listed but not deleted without explicit approval.
```
