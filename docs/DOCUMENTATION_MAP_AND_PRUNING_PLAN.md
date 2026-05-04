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

No other Markdown file should be treated as a first reading step unless a task file explicitly scopes it.

## Source-of-truth hierarchy

Markdown must not become more authoritative than the script, validator or runtime code it describes.

Use this hierarchy when resolving conflicts:

| Rank | Source | Authority |
|---:|---|---|
| 1 | Runtime/source code | Actual behavior and supported contracts. |
| 2 | Workflow scripts | Official local command entrypoints and parameters. |
| 3 | Validation scripts | Report schemas, required fields and pass/fail behavior. |
| 4 | Nearest package/tool README | Package-local usage and ownership. |
| 5 | `docs/README.md` | Reading order and stable documentation index. |
| 6 | Task runbooks | Task-specific orchestration instructions. |
| 7 | Historical/evidence/generated docs | Context only; never current truth. |

Rules:

```text
if Markdown command examples disagree with script parameters, the script wins
if a task runbook duplicates a long command block, prefer a script wrapper or canonical runbook link
if a Markdown file references a script path, the path must exist or be marked historical/superseded
if a document describes generated indexes, the generator and index policy are authoritative
if a historical report describes repo state, current repo inspection and validation reports win
```

Future validator target:

```text
Tools/validation/check_docs_script_references.py
```

Expected role:

```text
scan Markdown for .py/.ps1/.sh/.bat/.cmd references
extract python/powershell command blocks
verify referenced files exist
flag output/**, stale or non-canonical script references
flag long command blocks that should move to official wrappers or canonical runbooks
emit JSON and Markdown reports under output/validation
```

## Repository Markdown families

| Family | Pattern | Owner | Lifecycle |
|---|---|---|---|
| Root entrypoints | `AGENTS.md`, `README.md`, `WORKFLOW.md` | Root flow | `canonical_entrypoint` |
| Root community controls | `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, GitHub templates | GitHub/repository controls | `repository_community_control` |
| Stable docs | `docs/*.md` | `docs/README.md` | `maintained_source_doc` |
| Task runbooks | `docs/LOCAL_AI_TASKS/*.md` | `docs/LOCAL_AI_TASKS/README.md` | `current_or_historical_task` or `historical_task_record` |
| Historical project handoffs/reports | Dated or superseded reports under `docs/` | `docs/README.md` historical section | `historical_project_record` |
| Execution plans | `docs/EXECUTION_PLANS/**/*.md` | `docs/EXECUTION_PLANS/README.md` | `state_record` |
| Evidence | `docs/LOCAL_VALIDATION_EVIDENCE/*` | Evidence builders | `evidence_snapshot`; not source docs |
| Tool READMEs | `Tools/**/README.md` | Nearest tool/package | `maintained_source_doc` or package-local context |
| Generated/index context | `indexAI/**/*.md`, `Tools/npu/npu_code_*.md`, generated NPU chunks | Generators/package README | `generated_context`; do not hand-edit |
| Superseded local/root guides | Root guides replaced by current docs | Canonical replacement path | `superseded_by_canonical_doc` |
| Blender/application docs | `Scripting/**/*.md` | Package README | Application-domain only |
| Local tool history | `.aider.chat.history.md` and equivalent local logs | Local tools | `local_history_delete_candidate`; delete requires approval |

## Inventory tools

Run these before broad documentation cleanup or refactor planning:

```powershell
python .\Tools\validation\build_markdown_inventory.py --repo-root . --output .\output\validation\markdown_inventory.json --markdown-output .\output\validation\markdown_inventory.md
python .\Tools\validation\build_script_inventory.py --repo-root . --output .\output\validation\script_inventory.json --csv-output .\output\validation\script_inventory.csv --markdown-output .\output\validation\script_inventory.md
```

Inventory roles:

| Tool | Purpose | Output policy |
|---|---|---|
| `build_markdown_inventory.py` | Classify `.md` files by family/lifecycle, missing index status, prune candidates, long-file status and control-character diagnostics. | Local `output/**` unless converted to compact evidence. |
| `build_script_inventory.py` | Censisce scripts/tools with language, category, lines, description, functions, classes and methods. | Local `output/**`; CSV is for refactor review, not automatic source change. |

The script inventory must be included in future refactor evidence together with the existing Python line-count CSV. Line count shows size; script inventory shows callable surface and intent.

## Inventory lifecycle classes

The Markdown inventory may emit these lifecycle values:

| Lifecycle | Meaning | Action |
|---|---|---|
| `canonical_entrypoint` | First-path file in the reading chain. | Keep short; link outward. |
| `maintained_source_doc` | Stable documentation currently maintained. | Must be indexed from `docs/README.md` or nearest owner README. |
| `repository_community_control` | GitHub/community control docs and templates. | Keep out of prune candidates unless explicitly replaced. |
| `current_or_historical_task` | Task runbook requiring owner review. | Index in `LOCAL_AI_TASKS/README.md` or classify as historical. |
| `historical_task_record` | Past local-AI task/handoff retained for continuity. | Do not use as default reading path. |
| `historical_project_record` | Past project report/handoff replaced by current docs/live inspection. | Keep only as historical reference; list replacement/current docs. |
| `state_record` | Execution-plan state. | Keep under execution-plan owner. |
| `evidence_snapshot` | Git-trackable compact evidence. | Not source documentation. |
| `generated_context` | Generated/index/chunk context. | Regenerate; do not hand-edit. |
| `tool_context_review` | Tool-local context requiring owner/package review. | Link from nearest tool README or demote to generated context. |
| `superseded_by_canonical_doc` | Retained legacy guide with explicit replacement. | Do not delete without approval; prefer canonical replacement. |
| `local_history_delete_candidate` | Local tool history/log material. | Delete only with explicit approval. |
| `review_needed` | Not yet classified. | Inspect before indexing or pruning. |

## Oversize and corruption diagnostics

Long Markdown is technical debt because it is hard to open, hard to review through GitHub/API and unsafe as a first reading surface.

Inventory thresholds:

| Field | Meaning |
|---|---|
| `split_recommended` | File is at or above 400 lines. Prefer split, summary or demotion. |
| `hard_review_required` | File is at or above 700 lines. It must not be a default entrypoint. |
| `control_character_count` | Non-whitespace control characters were found. Treat as copy/paste or escaping corruption until reviewed. |

Rules:

```text
canonical entrypoints should stay short
long procedural content belongs in task runbooks only
long evidence/generated chunks must be classified as evidence/generated, not source docs
long historical reports must point to current replacement docs
control-character files require focused cleanup before being promoted
```

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
| Git/GitHub local workflow | `docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md` | Root/local legacy guides should point here as superseded. |
| Code consultation status | `PROJECT_STATUS_POINT.md`, `MODULE_MAP.md`, `REFACTORING_AND_REUSE_PLAN.md`, live repo inspection | Long consultation reports are historical, not current truth. |
| Script-backed commands | Official workflow/validation scripts | Markdown examples must not override script parameters. |

## Add-before-prune rule

When adding or updating Markdown:

1. Check whether the content belongs in an existing canonical file.
2. If a new file is needed, add it to the correct index.
3. Mark older overlap as one of:
   - `superseded_by_canonical_doc`
   - `historical_project_record`
   - `historical_task_record`
   - `application-domain only`
   - `generated_context`
   - `evidence_snapshot`
   - `local_history_delete_candidate`
4. Replace repeated commands with links to canonical runbooks or official script wrappers.
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
Tools/npu/npu_music_chunks/**/*.md
output/**/*.md
```

## First cleanup sequence

1. Reduce root entrypoints to a single reading flow.
2. Preserve long command blocks only in canonical task runbooks or official script wrappers.
3. Add Markdown and script inventories to the workflow/refactor evidence path.
4. Use inventory output to identify missing-index, long-file, control-character and prune candidates.
5. Mark obsolete material before any deletion.
6. Add script-reference validation before any broad command-block rewrite.
7. Create a separate deletion PR only after explicit approval.

## Acceptance criteria

```text
single reading flow is explicit
root entrypoints are shorter than before
stable docs are indexed or intentionally excluded
evidence/generated MD is not treated as source documentation
historical reports point to current replacement docs
legacy guides point to canonical replacements
long Markdown files are surfaced by inventory before refactor/prune decisions
control-character corruption is surfaced before promotion
script/tool inventory is available for refactor planning
Markdown does not override script-backed behavior
script-reference validation is planned before broad command-block rewrites
no output/**, renders/**, *.db or *.sqlite files are committed
no deletion is performed without explicit approval
```
