<!-- IA-CARMINE-MD-SPLIT: part -->
# README — parte 001 di 002

Sorgente indice: [`../README.md`](../README.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

# Local AI Tasks

Markdown task files and operator entrypoints for local AI work.

This index is a router, not a command source. Executable commands for full runs, quick tests, deep tests, reset, provider probes, memory, discovery repair, CSV/count surfaces and patch-spec generation live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

## Non-negotiable rule

There is one active local-AI operator entrypoint, now present on `master` after PR #187:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

All test/full-run/provider/memory/patch-spec/reset/discovery/index-repair flows must be expressed as launcher modes, profiles, flags or explicitly scoped helper tools behind the launcher.

Do not create or promote separate active-start runbooks for:

```text
full toolbox runs
code-refactor runs
Markdown-refactor runs
provider probes
full validation
quick tests
deep tests
reset cleanup
SQLite memory handoff
patch-spec generation
auto-discovery repair
index repair
CSV/count generation
```

Supporting wrappers may exist, but they are implementation lanes behind the launcher or explicitly scoped helper tools.

## Current active state

Current compact operational bridge:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
```

Current code-derived baseline:

```text
Baseline: master after PR #187 merge
Primary launcher: Tools/workflow/run_unified_local_ai_refactor.ps1
Next candidate PR: #192 feat(ai): add full0to10 report-only foundation checks
Evidence branch to mine/regenerate: #191 docs(ai): add Full0To10 quick evidence bundle 20260506-004242
Mode: review-only until explicit human instruction
```

Do not treat PR #187 as the current active branch anymore. It is now the merged launcher baseline.

Recent telemetry baseline:

```text
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
```

The earlier broker telemetry issue is historical/resolved unless a new regression is found.

## TUTTO SU TUTTO doctrine

Every full-run task must preserve whole-repository coverage: **TUTTO SU TUTTO**.

`quick`, `balanced`, `deep` and `custom` are budget/intensity profiles. They do not define smaller scopes. A quick full run still traverses all active full-run lanes with reduced capacity; it is not a smoke test.

The set of lanes is allowed to grow. When a new production-ready tool, broker capability, provider diagnostic, registry, evidence builder, memory/context surface, repository-consistency check, auto-discovery repair, index repair or CSV/count surface is promoted, update the full-run contract and this index so the new capability is either included in `tutto` or explicitly excluded.

## Current stable reading order

Use this order for current IA-Carmine local-AI work:

```text
1. CHATGPT/README.md
2. docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
3. docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
4. docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
5. docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
6. docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
7. docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
8. docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
9. docs/LOCAL_AI_TASKS/project-tool-registry.md
10. docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
11. docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
12. docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
13. FULL_RUN_UNICA_TUTTO_SU_TUTTO.md
```

Do not start from historical PR handoffs, legacy master-branch runbooks, or long semi-automatic procedure snapshots.

## Required context

Every active task file must preserve hard guardrails from:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
```

If a task conflicts with `AGENTS.md`, preserve hard guardrails and stop with a conflict report.

## Visibility-first rule

Every local-AI run must be inspectable from compact surfaces before opening detailed evidence.

Required reading order for a run:

```text
1. launcher command from unified-local-ai-refactor-launcher.md or FULL_RUN_UNICA_TUTTO_SU_TUTTO.md
2. unified_local_ai_refactor_manifest.json
3. phase_status / phase_reports
4. production bundle and telemetry summary
5. compact Markdown or CSV/count summaries
6. detailed evidence only when needed
```

A run is not operationally clear if the next agent must open a giant bundle to understand what happened.

Each active launcher phase must expose at least one visible output:

```text
phase_status
phase_reports
context_files
report_files
compact Markdown summary
CSV/JSON inventory
line-count CSV
function/class/method inventory CSV
index repair report
auto-discovery report
```

## Discovery, index repair and CSV/count surfaces

Discovery and count surfaces are part of `TUTTO SU TUTTO` when relevant. They provide fast, machine-readable evidence before an agent edits docs or code.

Required/expected surfaces include:

```text
Markdown inventory JSON/MD
script inventory JSON/CSV/MD
function/class/method inventory CSV
Python line-count CSV/MD
file line-limit JSON/MD report
semantic chunk manifest
selected chunk evidence
repository consistency map/smoke
auto-discovery or missing-index report when scanner/index drift is suspected
index repair plan/report when generated indexes are stale or missing
```

Policy:

```text
CSV/count outputs are evidence surfaces, not source authority.
Generated indexes and code chunks are not hand-maintained source.
Do not commit output/** or indexAI/code_chunks/**.
Commit only compact evidence under docs/LOCAL_VALIDATION_EVIDENCE when needed.
Index repair must be plan/report-first unless the user explicitly asks for regeneration or apply.
```

## 400-line policy for documentation and code

Maintained documentation and source files must stay small enough for human review and AI-assisted patching.

Hard limit:

```text
Markdown: <= 400 lines per active .md file
Python/PowerShell/scripts/source code: <= 400 lines per maintained source file
```

Markdown split rule:

```text
Keep the original file as a compact index.
Create a sibling folder named exactly like the file, including .md: <file>.md/.
Move detailed content into <file>.md/part-001.md, part-002.md, ...
Keep each part under 400 lines.
The index must list all parts and state that the document was split for the 400-line policy.
```

Code split rule:

```text
Keep public entrypoints/wrappers compact.
Move implementation into a same-purpose package or module folder.
Split by responsibility, not by arbitrary line number only.
Keep each module/file under 400 lines.
Preserve CLI/API compatibility unless the task explicitly allows breaking changes.
Report resulting line count for every created or modified code/script file.
```

Validator note:

```text
docs/LOCAL_AI_TASKS/file-line-limit-validator-2026-05-06.md
Tools/validation/check_file_line_limits.py
```

Existing files already over 400 lines are technical debt. Do not split them blindly during unrelated documentation work; refactor them progressively when touching that area for a code task.

## Function/tool visibility map

Current unified-flow tools and their visibility surfaces:

| Area | Tool/script | Visible output | Launcher status |
|---|---|---|---|
| Unified launcher | `Tools/workflow/run_unified_local_ai_refactor.ps1` | run manifest with selected modes, flags, reports, context and phase status | canonical |
| Markdown inventory | `Tools/validation/build_markdown_inventory.py` | JSON and Markdown inventory | `md` mode |
| Link validation | `Tools/validation/check_docs_links.py` | JSON link report | `md` / validation modes |
| Script inventory | `Tools/validation/build_script_inventory.py` | JSON, CSV and Markdown function/class inventory | `python` mode |
| Python line count | broker/runtime line-count helper and validation reports | CSV and Markdown line-count surfaces | inventory/evidence lane |
| File line-limit report | `Tools/validation/check_file_line_limits.py` | JSON and optional Markdown line-limit report | validation/evidence lane |
| Report contracts | `Tools/validation/check_validation_report_contract.py` | JSON contract report | `json` / `contract` modes |
| Workload quality | `Tools/validation/check_ai_workload_report_quality.py` | `ai_workload_report_quality.json` | provider quality gate |
| Semantic chunks | `Tools/npu/build_semantic_code_chunks.py` | semantic chunk manifest | `chunks` mode |
| Context pack | `Tools/ai/build_ai_context_pack.py` | bounded Markdown/JSON context pack and evidence summary | `context_pack` mode |
| Agent state/memory | `Tools/ai/build_agent_state_packet.py` | agent-state packet and optional SQLite memory handoff | `agent_state` mode |
| Auto-discovery/index repair | scanner/index validators and repair planners | report-only discovery/index repair reports | validation/refactor support lane |
| Official adapter | `Tools/workflow/run_local_ai_task_via_pipeline.ps1` | packet/proposals and adapter manifest | `official` mode |
| Ollama advisory | `Tools/workflow/run_post_validation_ai_packet.ps1` | advisory packet/proposals and manifest | `provider` / advisory flag |
| Multistep provider | `Tools/workflow/run_parallel_ai_provider_multistep.ps1` | provider workflow report/proposals | `provider` / Full0To10 flag |
| Integrated decision lane | `Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1` | integrated full-toolbox report when selected | supporting selected phase only, not entrypoint |
| Runtime broker | `Tools/ai/agent_runtime_tool_broker.py` | runtime tool broker JSON/MD report | supporting full-toolbox lane |
| Production bundle | `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` | shared toolbox AI-to-AI bundle and final summary | production handoff |
| Reset | unified launcher reset mode | reset plan JSON/Markdown | `reset` mode |
| Full0To10 recursive bundle ZIP | `Tools/ai/build_full_run_evidence_bundle_zip.py` in PR #192 | ZIP plus completeness report | candidate foundation layer |
| Runtime hardware capability manifest | `Tools/ai/build_runtime_hardware_capability_manifest.py` in PR #192 | CPU/GPU.0/NPU/NVIDIA report-only manifest | candidate foundation layer |
| Hardware delegation contract | `Tools/validation/check_runtime_hardware_delegation_contract.py` in PR #192 | report-only delegation contract validation | candidate foundation layer |
| Bundle completeness contract | `Tools/validation/check_full_run_bundle_completeness.py` in PR #192 | ZIP/completeness validation report | candidate foundation layer |

If a tool is referenced in docs but missing from the repository, mark it optional/future or remove the reference in the same change.

## Intent router

| User intent | Active path |
|---|---|
| Full selectable 0-to-10 local AI workflow | `FULL_RUN_UNICA_TUTTO_SU_TUTTO.md`, unified launcher runbook, `Full0To10` profile |
| Fast 5-minute style full loop | unified launcher runbook, quick/custom intensity |
| Deep full-toolbox/provider loop | unified launcher runbook, deep/custom intensity |
| Custom intensity/limits | unified launcher runbook, custom intensity and explicit numeric knobs |
| Interactive phase picker | unified launcher runbook, interactive mode |
| Local generated-artifact cleanup/reset | unified launcher runbook, reset mode |
| Documentation cleanup, Markdown pruning, obsolete/redundant MD review | unified launcher `md,json,contract,full_validation` phases plus this index |
| Refactor/reuse planning | `refactor-reuse-methods-classes-tools-planning.md` plus current runtime bundle and telemetry summaries |
| Auto-discovery/index repair | report-only discovery/index repair lanes; no generated index commit unless explicitly requested |
| CSV/count inventory | script inventory CSV and line-count CSV/MD surfaces through validation/inventory lanes |
| GPU/NPU evidence diagnostics | unified launcher provider/probe phases; current flow is in `current-code-flow-guide-2026-05-05.md` |
| Runtime broker telemetry regression review | `recent-telemetry-state-2026-05-05.md` first; historical fix docs only if a new regression appears |
| Audio/media output guardrail review | `no-audio-media-output-guardrail-2026-05-05.md` |
| Tool discovery and promotion | `tool-inventory-placement-audit-2026-05-05.md` and `project-tool-promotion-and-insertion-guide-2026-05-05.md` |
| Full-context local AI/NPU golden path | supporting background only; prefer unified launcher for execution |
| Blender/audio/render/encode output | Application-domain task only; not part of normal AI/tooling runs. |

## Maintained task files

| File | Status | Purpose |
|---|---|---|
| `current-operational-state-2026-05-05.md` | active bridge | Compact current state for post-#187 master, PR #192 candidate, PR #191 evidence branch, guardrails and source-of-truth hierarchy. |
| `file-line-limit-validator-2026-05-06.md` | active validator note | Compact contract for `Tools/validation/check_file_line_limits.py` and 400-line evidence policy. |
| `refactor-reuse-methods-classes-tools-planning.md` | active P1 task | Analyze method/class/helper/tool reuse, classify patch plans and keep patching review-only. |
| `refactor-reuse-full-run-documentation-coherence-2026-05-05.md` | active bridge | Coherence note for the refactor/reuse run and bundle. |
| `recent-telemetry-state-2026-05-05.md` | active baseline | Recent telemetry baseline for `073332` and `081141`; broker telemetry treated as resolved unless a regression appears. |
| `unified-local-ai-refactor-launcher.md` | canonical active | Operator guide for one entrypoint: selectable phases, `Full0To10`, intensity profiles, reset planning, SQLite memory, semantic chunks, context packs, provider advisory, patch specs and validation. |
| `full-toolbox-0-to-10-semi-automatic-procedure.md` | historical/supporting | Long pre-unified semi-automatic procedure snapshot. It contains useful forensic detail but must not override the unified launcher. |
| `fix-final-runtime-broker-telemetry-task-2026-05-05.md` | resolved/historical | Historical fix task for final broker telemetry preservation. Do not treat as current P0 unless investigating a regression. |
| `post-broker-runtime-telemetry-followup-2026-05-05.md` | resolved/historical | Historical diagnostic after run `20260505-002508`; superseded by later broker telemetry evidence. |
| `no-audio-media-output-guardrail-2026-05-05.md` | active guardrail | Prevents unintended audio playback/export, FFmpeg muxing, Blender render or media generation in AI/tooling runs. |
| `tool-inventory-placement-audit-2026-05-05.md` | active audit | Repository-wide tool/candidate audit, including tools outside `Tools/**`. |
| `project-tool-promotion-and-insertion-guide-2026-05-05.md` | active guide | How to promote scripts into project tools, broker tools and full-run lanes. |
| `project-tool-registry.md` | active registry | Current project-tool registry and promotion visibility surface. |
| `current-code-flow-guide-2026-05-05.md` | active guide | Current code flow from launcher to provider, broker, bundle and evidence. |
| `docs-md-obsolete-pruning-next-step.md` | active task input | Follow-up triage task for obsolete/superseded Markdown after the entrypoint reduction baseline. |
| `forgotten-scripts-documentation-audit.md` | active audit | Identify scripts that exist but are not visible enough in Markdown catalogs; classify without deleting. |
| `validation-readme-reduction-next-step.md` | active follow-up | Reduce `Tools/validation/README.md` to a compact catalog and remove long procedural/control-character-prone blocks. |
| `next-chat-unified-launcher-external-controls.md` | follow-up | Add external CLI controls for launcher output dirs, context/report/artifact inputs and basenames. Secondary to current refactor/reuse bundle inspection unless explicitly selected. |
| `gpu-npu-parallel-evidence-runbook.md` | supporting detail | GPU/NPU evidence and planner diagnostics background. Prefer unified launcher for execution. |
| `full-context-ai-npu-golden-path.md` | supporting detail | Full-context local AI/NPU path background. Prefer unified launcher for execution. |
| `full-context-golden-docs-contract.md` | supporting contract | Contract validation for the full-context golden path. |
| `apply-agent-review-doc-patch-plan.md` | scoped helper | Apply low-risk documentation patch plans after manual review. |
| `consistency-local-ai-contracts-and-powershell.md` | scoped helper | Compare local AI contract docs with PowerShell runners. |
| `selected-review-workflow-ai-tools-patch-specs.md` | scoped helper | Review workflow/AI tools for safe patch-spec candidates. |
| `enrich-local-ai-memory-chunks-context-wrapper.md` | supporting/memory detail | Plan memory, semantic chunks, context packs and wrapper enrichment. |
| `improve-gpu-planner-nonempty-recommendations.md` | supporting diagnostic | GPU planner non-empty recommendation diagnostics. |

## Removed superseded active-start runbooks

The following legacy active-start documents were removed because the stable layer now owns the active flow:

```text
post-pr114-next-task-handoff.md
next-chat-handoff-after-balanced-full-run-2026-05-02.md
next-chat-handoff-after-pr115-large-code-refactor-2026-05-02.md
heavy-gpu-local-ai-diagnostics-handoff.md
shared-toolbox-refactor-duplication-audit-next-task-2026-05-03.md
shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md
code-refactor-0-to-10-procedure.md
code-refactor-local-machine-validation-addendum.md
code-refactor-md-lane-extension.md
```

Current policy:

```text
Use run_unified_local_ai_refactor.ps1 as the only operator entrypoint.
Use current-operational-state-2026-05-05.md, FULL_RUN_UNICA_TUTTO_SU_TUTTO.md and current-code-flow-guide-2026-05-05.md for current flow.
Use refactor-reuse-methods-classes-tools-planning.md and current telemetry/evidence summaries for refactor/reuse passes.
Use tool-inventory-placement-audit-2026-05-05.md and project-tool-promotion-and-insertion-guide-2026-05-05.md for project-tool promotion.
Use no-audio-media-output-guardrail-2026-05-05.md to classify audio/media output side effects.
Do not create new parallel 0-to-10 entrypoints unless the user explicitly asks for a separate runner.
If historical details are needed, recover them from git history or compact evidence, not from active task docs.
```

## Full0To10 rule

`Full0To10` must include every major step by default. Missing phases are allowed only when the operator explicitly disables them with a `No*` flag.

Expected default full profile:

```text
pipeline adapter ufficiale eseguito
packet/proposals generati
Ollama advisory usato or explicitly diagnosed as degraded
patch specs creati e validati
primary provider routing completo or explicit recovered provider diagnostic
workload quality routing presente
multistep provider workflow richiesto
probe Ollama/NPU richiesti
context pack presente
SQLite memory IN/OUT presente quando non disabilitata
quality gate registrato nel manifest
runtime broker report produced and absorbed into telemetry
auto-discovery/index surfaces visible when selected or relevant
CSV/count surfaces produced by inventory lanes when selected
patch_application_performed=false
```

Explicit disablers are documented in the unified launcher runbook and launcher contract.

## Audio/media output guardrail

Normal AI/tooling runs must not produce application-domain media output.

For these task classes:

```text
documentation cleanup
provider diagnostics
tool promotion
broker telemetry
patch planning
evidence generation
repository validation
index repair planning
CSV/count inventory
```

forbidden side effects are:

```text
audio playback
audio export
WAV/MP3/AAC conversion
FFmpeg encode or mux operation
Blender render
video generation
media output side effect
```

Use `no-audio-media-output-guardrail-2026-05-05.md` for the detailed policy.
