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
| 8 | `docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` | Unified local AI entrypoint | Canonical active local AI / 0-to-10 runbook. |
| 9 | `docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md` | Current code/tool/evidence flow | Launcher, provider, broker, telemetry, bundle and evidence flow. |
| 10 | `docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md` | Tool placement audit | Repository-wide tool/candidate classification, including non-canonical scripts. |
| 11 | `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` | Tool promotion guide | Rules for project-tool, broker-tool and full-run-lane promotion. |
| 12 | `docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md` | Audio/media guardrail | Prevents unintended media output in AI/tooling runs. |
| 13 | `Tools/validation/README.md` | Validator catalog | Tool commands and contracts only. |

Legacy monolithic 0-to-10 runbooks have been removed or demoted from the active documentation set. The unified launcher is now the only active 0-to-10 entrypoint.

Historical detail, when needed, must come from:

```text
git history
compact evidence under docs/LOCAL_VALIDATION_EVIDENCE/
scoped task handoffs that are explicitly referenced by the current task
```

Do not recreate parallel active-start runbooks for full-toolbox, code-refactor or Markdown-refactor flows.

## TUTTO SU TUTTO pruning rule

Markdown that describes a full local-AI run must preserve **TUTTO SU TUTTO**.

Allowed distinctions:

```text
quick    = full scope with reduced budget
balanced = full scope with standard budget
deep     = full scope with expanded budget
custom   = full scope with operator-defined budget
smoke    = separate non-full mode
```

Prune or rewrite docs that imply a quick full run is a partial run, that legacy wrappers are first entrypoints, or that a full run may silently skip core lanes.

The perimeter of `tutto` is expandable. When new stable lanes or data surfaces are added, update the canonical docs and demote older docs that describe a smaller stale perimeter as historical/supporting.

## Visibility-first documentation rule

A local-AI run must be understandable from compact, indexed surfaces before opening detailed evidence.

Required reading order:

```text
launcher command
unified_local_ai_refactor_manifest.json
phase_status / phase_reports
runtime tool telemetry and capability manifest
full toolbox telemetry summary
production AI-to-AI bundle
compact Markdown or CSV summaries
detailed evidence only when needed
```

Every active phase should expose at least one visible output:

```text
phase_status
phase_reports
context_files
report_files
compact Markdown summary
CSV/JSON inventory
runtime broker telemetry when broker tools are involved
runtime capability manifest when broker/capability data is relevant
full toolbox telemetry summary for production AI-to-AI handoff
```

Do not use a long generated bundle as the first operational interface.

## Telemetry-first pruning rule

Telemetry is a maintained documentation concern because it controls how future AI agents interpret a run.

Docs are stale if they encourage any of these patterns:

```text
infer success from output file existence alone
treat broker telemetry as optional after a broker lane ran
hide provider degradation outside the AI-to-AI handoff
omit capability manifests from full-run communication
claim patch/source writes happened without telemetry evidence
claim a lane succeeded without executed/failed/blocked/degraded fields
```

Canonical telemetry handoff surfaces:

```text
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
```

## Length and readability policy

| File type | Preferred maximum | Required action when exceeded |
|---|---:|---|
| Active operator runbook | ~500 lines | Split, summarize or move verbose detail to supporting docs. |
| Maintained source documentation | ~700 lines | Add structure or split into subordinate docs. |
| Generated compact evidence | ~1200 lines | Add manifest/summary and classify as evidence. |
| Large historical/evidence bundle | Any size only if unavoidable | Must be indexed and must not be the first operational entrypoint. |

Policy:

```text
No active runbook should require opening an 8000-line bundle.
Generated evidence may be long only if it has a compact manifest/summary.
Prefer manifest + index + focused report over one huge Markdown file.
Do not create new monolithic AI-to-AI bundles without companion manifests.
```

## Repository Markdown families

| Family | Pattern | Owner | Lifecycle |
|---|---|---|---|
| Root entrypoints | `AGENTS.md`, `README.md`, `WORKFLOW.md` | Root flow | Canonical, concise |
| Stable docs | `docs/*.md` | `docs/README.md` | Maintained source docs |
| Task runbooks | `docs/LOCAL_AI_TASKS/*.md` | `docs/LOCAL_AI_TASKS/README.md` | Current task input, supporting detail or historical handoff |
| Current code/tool flow | `docs/LOCAL_AI_TASKS/current-code-flow-guide-*.md` | Local AI task index | Current launcher/provider/broker/telemetry/bundle/evidence flow |
| Tool governance | `docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-*.md`, `docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-*.md` | Local AI task index | Tool discovery, classification, promotion and insertion |
| Runtime broker telemetry | `docs/LOCAL_AI_TASKS/fix-final-runtime-broker-telemetry-task-*.md`, `docs/LOCAL_AI_TASKS/post-broker-runtime-telemetry-followup-*.md` | Local AI task index | Historical/validated P0 task and follow-up evidence; not an open P0 unless a newer run regresses. |
| Audio/media output guardrail | `docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-*.md` | Local AI task index | Guardrail for AI/tooling runs |
| Execution plans | `docs/EXECUTION_PLANS/**/*.md` | `docs/EXECUTION_PLANS/README.md` | State records |
| Evidence | `docs/LOCAL_VALIDATION_EVIDENCE/*` | Evidence builders | Snapshot evidence, not source docs |
| Tool READMEs | `Tools/**/README.md` | Nearest tool/package | Package-local |
| Generated/index context | `indexAI/**/*.md`, `Tools/npu/npu_code_*.md` | Generators | Regenerated, not hand-edited |
| Blender/application docs | `Scripting/**/*.md` | Package README | Application-domain only |

## Inventory tools

Run inventories before broad documentation cleanup or refactor planning. The command owner is the unified launcher runbook and `Tools/validation/README.md`, not this pruning map.

Inventory roles:

| Tool | Purpose | Output policy |
|---|---|---|
| `build_markdown_inventory.py` | Classify `.md` files by family/lifecycle, missing index status, length class and prune candidates. | Local `output/**` unless converted to compact evidence. |
| `build_script_inventory.py` | Censisce scripts/tools with language, category, lines, description, functions, classes and methods. | Local `output/**`; CSV is for refactor review, not automatic source change. |
| `tool-inventory-placement-audit-2026-05-05.md` | Classifies canonical and non-canonical tool candidates across the full repository. | Maintained source doc. |
| `project-tool-promotion-and-insertion-guide-2026-05-05.md` | Defines promotion rules for project tools, broker tools and full-run lanes. | Maintained source doc. |

The script inventory must be included in future refactor evidence together with Python line-count CSV. Line count shows size; script inventory shows callable surface and intent.

## Duplication map

| Topic | Canonical target | Pruning rule |
|---|---|---|
| Provider lane policy | `AGENTS.md` for hard rule, `WORKFLOW.md` for lifecycle | Other docs link or summarize one line. |
| Unified full 0-to-10 procedure | `LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` | No copied command blocks in entrypoints. |
| TUTTO SU TUTTO doctrine | `AGENTS.md`, `README.md`, `WORKFLOW.md`, `UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` | Other docs may summarize but must not narrow scope. |
| Current code/tool/evidence flow | `LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md` | Other docs link or summarize. |
| Telemetry-first AI handoff | `LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md`, `LOCAL_AI_WORKFLOW.md`, `DATA_FLOW.md` | Do not scatter conflicting success criteria. |
| Runtime broker telemetry validated state | `PROJECT_STATUS_POINT.md` and `fix-final-runtime-broker-telemetry-task-2026-05-05.md` | Do not relabel as open unless newer evidence regresses. |
| Tool discovery and promotion | `LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md`, `LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md` | Do not duplicate tool registry logic across old handoffs. |
| Audio/media output guardrail | `LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md` | Other docs link to it; do not bury media side-effect policy in run logs. |
| Historical full-toolbox procedure | git history / compact evidence | Do not restore as active runbook. Extract only compact durable rules into canonical docs. |
| Historical code/refactor procedure | git history / compact evidence | Do not restore as active runbook. Keep line-count/script-inventory semantics in unified flow. |
| Evidence bundle policy | `WORKFLOW.md` and unified launcher runbook | Evidence snapshots are not source docs. |
| Patch bundle policy | `AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md` plus unified launcher runbook | Do not duplicate generated bundle internals everywhere. |
| Historical Blender role | `README.md` and `MODULE_MAP.md` | Detailed instructions stay under Blender/domain docs. |
| Validation command catalog | `Tools/validation/README.md` | Task docs list only focused commands. |
| Tool/function visibility | `LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md` and tool placement audit | Every active phase needs manifest/report/summary surface. |

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
5. Run Markdown inventory and docs link validation when local execution is available.
6. Do not delete files without explicit user approval.

## Safe cleanup actions

Allowed without deletion:

```text
shorten root entrypoints
update indexes
mark historical/superseded/domain-only status
replace copied command blocks with canonical links
add or update report-only inventory tooling
add visibility/length policy
add guardrails for provider/runtime/broker/media side effects
update telemetry-first handoff rules
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

## Audio/media output pruning rule

Normal AI/tooling docs must not imply that full-run validation, broker telemetry, provider diagnostics, tool promotion or patch planning may produce media output.

If a document describes audio playback, audio export, FFmpeg encoding, muxing, Blender render or media generation, classify it as one of:

```text
application-domain doc
historical evidence
explicit media runtime task
guardrail breach report
```

Do not link media-runtime instructions from current local-AI operator entrypoints unless the task explicitly enters the Blender/audio application domain.

## Current cleanup sequence

1. Keep root entrypoints focused on the single reading flow.
2. Keep the canonical unified launcher as the only active full 0-to-10 command surface.
3. Keep TUTTO SU TUTTO and expandable perimeter doctrine visible in canonical docs.
4. Keep broker telemetry, capability manifest, provider quality and full toolbox telemetry visible in compact surfaces.
5. Keep no-audio/media output policy visible in entrypoints and task routing.
6. Add Markdown and script inventories to workflow/refactor evidence paths.
7. Use inventory output to identify missing-index, long-file and prune candidates.
8. Remove obsolete monolithic active-start docs after explicit approval.
9. Validate links and report contracts after deletion when local execution is available.

## Acceptance criteria

```text
single reading flow is explicit
unified launcher is the active 0-to-10 entrypoint
TUTTO SU TUTTO remains full-scope across quick/balanced/deep/custom intensities
expandable perimeter is documented for new stable lanes/data surfaces
root entrypoints are shorter than before
stable docs are indexed or intentionally excluded
evidence/generated MD is not treated as source documentation
script/tool inventory is available for refactor planning
tool placement and promotion docs are indexed
each active phase exposes status/report/summary visibility
runtime broker telemetry is surfaced when relevant
runtime capability manifest is surfaced when relevant
full toolbox telemetry summary is included in AI-to-AI handoff
telemetry is used before declaring run success/failure/degradation
audio/media output is forbidden in normal AI/tooling runs
long files are classified and not used as primary entrypoints
no output/**, renders/**, generated media, *.db or *.sqlite files are committed
no obsolete monolithic 0-to-10 runbook remains indexed as active documentation
```
