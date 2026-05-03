# Documentation Map and Pruning Plan

## Purpose

Control point for reducing Markdown redundancy and keeping one clear reading flow.

The goal is not to add more documentation. The goal is to make each Markdown file have a lifecycle, owner and reading position. New stable material must update an existing canonical document or explicitly mark older material as superseded, historical, generated or delete-candidate.

This file is report-only. It does not authorize deletion by itself.

## Canonical entrypoint chain

| Rank | File | Role | Rule |
|---:|---|---|---|
| 1 | `AGENTS.md` | Hard AI/agent contract | Keep short; guardrails only. |
| 2 | `README.md` | Human project identity | Keep short; link to workflows. |
| 3 | `WORKFLOW.md` | Operational lifecycle | Keep short; no scenario-specific long runs. |
| 4 | `docs/README.md` | Documentation index | Single reading flow and doc family map. |
| 5 | `docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md` | Markdown lifecycle and pruning policy | Cleanup control point. |
| 6 | `docs/LOCAL_AI_RUN_BOOTSTRAP.md` | Local checkout bootstrap | Local-run prerequisites. |
| 7 | `docs/LOCAL_AI_TASKS/README.md` | Task routing | Current vs historical task entrypoints. |
| 8 | `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` | Full toolbox runbook | Long procedural doc allowed. |
| 9 | `docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md` | Code/refactor runbook | Long procedural doc allowed. |
| 10 | `Tools/validation/README.md` | Validator catalog | Tool commands and contracts only. |

## Repository Markdown families

| Family | Pattern | Owner | Lifecycle |
|---|---|---|---|
| Root entrypoints | `AGENTS.md`, `README.md`, `WORKFLOW.md` | Root flow | Canonical, concise |
| Stable docs | `docs/*.md` | `docs/README.md` | Maintained source docs |
| Task runbooks | `docs/LOCAL_AI_TASKS/*.md` | `docs/LOCAL_AI_TASKS/README.md` | Current or historical |
| Execution plans | `docs/EXECUTION_PLANS/**/*.md` | `docs/EXECUTION_PLANS/README.md` | State records |
| Evidence | `docs/LOCAL_VALIDATION_EVIDENCE/*` | Evidence builders | Snapshot evidence, not source docs |
| Tool READMEs | `Tools/**/README.md` | Nearest tool/package | Package-local |
| Generated/index context | `indexAI/**/*.md`, `Tools/npu/npu_code_*.md` | Generators | Regenerated, not hand-edited |
| Blender/application docs | `Scripting/**/*.md` | Package README | Application-domain only |

## Inventory tools

Run these before broad documentation cleanup or refactor planning:

```powershell
python .\Tools\validation\build_markdown_inventory.py --repo-root . --output .\output\validation\markdown_inventory.json --markdown-output .\output\validation\markdown_inventory.md
python .\Tools\validation\build_script_inventory.py --repo-root . --output .\output\validation\script_inventory.json --csv-output .\output\validation\script_inventory.csv --markdown-output .\output\validation\script_inventory.md
```

Inventory roles:

| Tool | Purpose | Output policy |
|---|---|---|
| `build_markdown_inventory.py` | Classify `.md` files by family/lifecycle, missing index status and prune candidates. | Local `output/**` unless converted to compact evidence. |
| `build_script_inventory.py` | Censisce scripts/tools with language, category, lines, description, functions, classes and methods. | Local `output/**`; CSV is for refactor review, not automatic source change. |

The script inventory must be included in future refactor evidence together with the existing Python line-count CSV. Line count shows size; script inventory shows callable surface and intent.

## Duplication map

| Topic | Canonical target | Pruning rule |
|---|---|---|
| Provider lane policy | `AGENTS.md` for hard rule, `WORKFLOW.md` for lifecycle | Other docs link or summarize one line. |
| Full-toolbox procedure | `LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` | No copied command blocks in entrypoints. |
| Code/refactor procedure | `LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md` | Include line-count and script inventory evidence. |
| Evidence bundle policy | `WORKFLOW.md` and full-toolbox runbook | Evidence snapshots are not source docs. |
| Patch bundle policy | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` plus full-toolbox runbook | Do not duplicate generated bundle internals everywhere. |
| Historical Blender role | `README.md` and `MODULE_MAP.md` | Detailed instructions stay under Blender/domain docs. |
| Validation command catalog | `Tools/validation/README.md` | Task docs list only focused commands. |

## Add-before-prune rule

When adding or updating Markdown:

1. Check whether the content belongs in an existing canonical file.
2. If a new file is needed, add it to the correct index.
3. Mark older overlap as one of:
   - `superseded by <path>`
   - `historical evidence`
   - `application-domain only`
   - `generated, do not hand-edit`
   - `delete candidate, requires explicit approval`
4. Replace repeated commands with links to canonical runbooks.
5. Run Markdown inventory and docs link validation.
6. Do not delete files without explicit user approval.

## Safe cleanup actions

Allowed without deletion:

```text
shorten root entrypoints
update indexes
mark historical/superseded/domain-only status
replace copied command blocks with canonical links
add or update report-only inventory tooling
open PRs for review
```

Requires explicit user approval:

```text
delete Markdown files
move files across major folders
remove historical evidence
remove runbooks still referenced by task indexes
```

Never treat as manually maintained source:

```text
docs/LOCAL_VALIDATION_EVIDENCE/*.md
indexAI/**/*.md
Tools/npu/npu_code_context.md
Tools/npu/npu_code_index.md
output/**/*.md
```

## First cleanup sequence

1. Reduce root entrypoints to a single reading flow.
2. Preserve long command blocks only in canonical task runbooks.
3. Add Markdown and script inventories to the workflow/refactor evidence path.
4. Use inventory output to identify missing-index and prune candidates.
5. Mark obsolete material before any deletion.
6. Create a separate deletion PR only after explicit approval.

## Acceptance criteria

```text
single reading flow is explicit
root entrypoints are shorter than before
stable docs are indexed or intentionally excluded
evidence/generated MD is not treated as source documentation
script/tool inventory is available for refactor planning
no output/**, renders/**, *.db or *.sqlite files are committed
no deletion is performed without explicit approval
```
