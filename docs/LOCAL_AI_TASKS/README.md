# Local AI Tasks

Markdown entrypoints for non-interactive local AI runs.

Every task file must point back to:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
```

If a task conflicts with `AGENTS.md`, preserve hard guardrails and stop with a conflict report.

## Canonical local AI entrypoint

The active 0-to-10 entrypoint is now the unified launcher:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Canonical full run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity balanced `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

Quick run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity quick `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

Deep run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity deep `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

The unified launcher replaces scattered active 0-to-10 runbooks. Legacy documents remain useful as historical background, but agents should not start from them unless the user explicitly asks for a legacy/manual procedure.

## Visibility-first rule

Every local-AI run must be inspectable from compact surfaces before opening detailed evidence.

Required reading order:

```text
1. launcher command
2. unified_local_ai_refactor_manifest.json
3. phase_status / phase_reports
4. compact Markdown or CSV summaries
5. detailed evidence only when needed
```

A run is not considered operationally clear if the next agent must open a giant bundle to understand what happened.

Each active phase should expose at least one visible output:

```text
phase_status
phase_reports
context_files
report_files
compact Markdown summary
CSV/JSON inventory
```

## Length policy

Active docs must remain readable. Long files are allowed only when they are generated evidence or historical snapshots with a compact manifest.

| File type | Preferred maximum | Required action when exceeded |
|---|---:|---|
| Active operator runbook | ~500 lines | Split, summarize or move verbose content to supporting docs. |
| Maintained source documentation | ~700 lines | Add structure or split into subordinate docs. |
| Generated compact evidence | ~1200 lines | Add manifest/summary and classify as evidence. |
| Large historical/evidence bundle | Any size only if unavoidable | Must not be used as the first operational entrypoint. |

Policy:

```text
No active runbook should require opening an 8000-line bundle.
Do not create new monolithic AI-to-AI bundles without a companion manifest.
Do not use generated evidence snapshots as canonical workflow docs.
Prefer manifest + index + focused report over one huge Markdown file.
```

## Function/tool visibility map

Current unified-flow tools and their visibility surfaces:

| Area | Tool/script | Visible output |
|---|---|---|
| Unified launcher | `Tools/workflow/run_unified_local_ai_refactor.ps1` | run manifest with selected modes, flags, reports, context and phase status. |
| Markdown inventory | `Tools/validation/build_markdown_inventory.py` | JSON and Markdown inventory. |
| Link validation | `Tools/validation/check_docs_links.py` | JSON link report. |
| Script inventory | `Tools/validation/build_script_inventory.py` | JSON, CSV and Markdown function/class inventory. |
| Report contracts | `Tools/validation/check_validation_report_contract.py` | JSON contract report. |
| Workload quality | `Tools/validation/check_ai_workload_report_quality.py` | `ai_workload_report_quality.json`. |
| Semantic chunks | `Tools/npu/build_semantic_code_chunks.py` | semantic chunk manifest. |
| Context pack | `Tools/ai/build_ai_context_pack.py` | bounded Markdown/JSON context pack and evidence summary. |
| Agent state/memory | `Tools/ai/build_agent_state_packet.py` | agent-state packet and optional SQLite memory handoff. |
| Official adapter | `Tools/workflow/run_local_ai_task_via_pipeline.ps1` | packet/proposals and adapter manifest. |
| Ollama advisory | `Tools/workflow/run_post_validation_ai_packet.ps1` | advisory packet/proposals and manifest. |
| Multistep provider | `Tools/workflow/run_parallel_ai_provider_multistep.ps1` | provider workflow report/proposals when selected. |
| Legacy integrated lane | `Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1` | integrated full-toolbox report when selected. |
| Reset | unified launcher reset mode | reset plan JSON/Markdown. |

If a tool is referenced in docs but missing from the repository, mark it optional/future or remove the reference in the same change.

## First entrypoints

| User intent | Start here |
|---|---|
| Full selectable 0-to-10 local AI workflow | `unified-local-ai-refactor-launcher.md` with `-Full0To10` |
| Fast 5-minute style full loop | `unified-local-ai-refactor-launcher.md` with `-Full0To10 -RunIntensity quick` |
| Deep full-toolbox/provider loop | `unified-local-ai-refactor-launcher.md` with `-Full0To10 -RunIntensity deep` |
| Custom intensity/limits | `unified-local-ai-refactor-launcher.md` with `-RunIntensity custom` and explicit numeric knobs |
| Interactive phase picker | `unified-local-ai-refactor-launcher.md` with `-Interactive` |
| Local generated-artifact cleanup/reset | `unified-local-ai-refactor-launcher.md` with `-Mode reset` |
| Documentation cleanup, Markdown pruning, obsolete/redundant MD review | `unified-local-ai-refactor-launcher.md` with `-Mode md,contract,full_validation` |
| GPU/NPU evidence diagnostics | `unified-local-ai-refactor-launcher.md`; legacy details may be read from `gpu-npu-parallel-evidence-runbook.md` |
| Full-context local AI/NPU golden path | `unified-local-ai-refactor-launcher.md`; legacy details may be read from `full-context-ai-npu-golden-path.md` |

## Current maintained task files

| File | Status | Purpose |
|---|---|---|
| `unified-local-ai-refactor-launcher.md` | canonical active | Operator guide for one entrypoint: selectable phases, `-Full0To10`, intensity profiles, reset planning, SQLite memory, semantic chunks, context packs, provider advisory, patch specs and validation. |
| `docs-md-obsolete-pruning-next-step.md` | active task input | Follow-up triage task for obsolete/superseded Markdown after the entrypoint reduction baseline. |
| `validation-readme-reduction-next-step.md` | active follow-up | Reduce `Tools/validation/README.md` to a compact catalog and remove long procedural/control-character-prone blocks. |
| `next-chat-unified-launcher-external-controls.md` | active follow-up | Add external CLI controls for launcher output dirs, context/report/artifact inputs and basenames. |
| `gpu-npu-parallel-evidence-runbook.md` | supporting/legacy detail | GPU/NPU evidence and planner diagnostics background. Prefer unified launcher for execution. |
| `full-context-ai-npu-golden-path.md` | supporting/legacy detail | Full-context local AI/NPU path background. Prefer unified launcher for execution. |
| `full-context-golden-docs-contract.md` | supporting contract | Contract validation for the full-context golden path. |
| `apply-agent-review-doc-patch-plan.md` | scoped helper | Apply low-risk documentation patch plans after manual review. |
| `consistency-local-ai-contracts-and-powershell.md` | scoped helper | Compare local AI contract docs with PowerShell runners. |
| `selected-review-workflow-ai-tools-patch-specs.md` | scoped helper | Review workflow/AI tools for safe patch-spec candidates. |
| `enrich-local-ai-memory-chunks-context-wrapper.md` | supporting/memory detail | Plan memory, semantic chunks, context packs and wrapper enrichment. |
| `improve-gpu-planner-nonempty-recommendations.md` | supporting diagnostic | GPU planner non-empty recommendation diagnostics. |
| `heavy-gpu-local-ai-diagnostics-handoff.md` | historical handoff | Handoff for heavy local GPU diagnostics when GitHub-only agents cannot execute providers. |

## Superseded active-start runbooks

These files may remain as historical expansion or scoped design references, but must not be treated as the first operational path anymore:

```text
full-toolbox-0-to-10-semi-automatic-procedure.md
code-refactor-0-to-10-procedure.md
code-refactor-local-machine-validation-addendum.md
code-refactor-md-lane-extension.md
```

Current policy:

```text
Use run_unified_local_ai_refactor.ps1 as the operator entrypoint.
Use old 0-to-10 docs only to understand historical details or specific validation semantics.
Do not create new parallel 0-to-10 entrypoints unless the user explicitly asks for a separate runner.
```

## Unified launcher flow

The preferred single operator entrypoint is:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 -Interactive
```

The same launcher also accepts explicit modes:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Mode md,python,chunks,context_pack,agent_state,official,provider,patch_specs,contract,full_validation `
  -UseOllamaAdvisory `
  -UsePrimaryAdvisoryProvider `
  -GeneratePatchSpecs
```

Supported modes include:

```text
smoke
reset
validation
md
json
python
chunks
context_pack
agent_state
official
provider
patch_specs
evidence
contract
full_validation
all
```

The safe combined order is:

```text
baseline -> smoke -> reset -> validation -> md -> json -> python -> chunks -> context_pack -> agent_state -> workload_quality -> legacy_full_toolbox_integrated -> official -> provider -> patch_specs -> evidence -> contract -> full_validation
```

## Full0To10 rule

`-Full0To10` must include every major step by default. Missing phases are allowed only when the operator explicitly disables them with a `-No*` flag.

Expected default full profile:

```text
pipeline adapter ufficiale eseguito
packet/proposals generati
Ollama advisory usato
patch specs creati e validati
primary provider routing completo
workload quality routing presente
multistep provider workflow richiesto
probe Ollama/NPU richiesti
context pack presente
SQLite memory IN/OUT presente quando non disabilitata
quality gate registrato nel manifest
patch_application_performed=false
```

Disablers:

```text
-NoOllamaProbe
-NoNpuProbe
-NoNpuDecodeSmoke
-NoMultistepProvider
-NoWorkloadQuality
-NoMemoryWrite
-NoEvidence
-NoPatchSpecs
```

## SQLite memory / context enrichment must be explicit

SQLite-backed memory is an active local-AI enrichment capability, not a future placeholder.

Relevant files:

```text
Tools/ai/agent_state.py
Tools/ai/build_agent_state_packet.py
Tools/ai/review_agent_memory.py
Tools/ai/agent_memory_policy.py
Tools/npu/build_semantic_code_chunks.py
Tools/ai/build_ai_context_pack.py
docs/LOCAL_AI_TASKS/enrich-local-ai-memory-chunks-context-wrapper.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Default memory DB path used by the local flow:

```text
indexAI/agent_memory/agent_memory.sqlite
```

Policy:

```text
SQLite DB files are local/private runtime state.
Do not commit .sqlite/.db files.
Do not remove SQLite-memory references from docs unless the tools are actually removed from the repo.
If a referenced tool is missing, mark it optional/future or remove the reference immediately.
```

## Reset mode policy

Reset mode is for local generated artifacts, not source cleanup.

Default reset behavior:

```text
plan only
no deletion
writes local_ai_reset_plan_*.json/.md under output/validation
```

Deletion requires both:

```text
-ApplyReset
-ConfirmResetText "DELETE LOCAL AI ARTIFACTS"
```

Reset may include memory/generated-index candidates only when explicitly requested:

```text
-IncludeMemoryReset
-IncludeGeneratedIndexReset
```

## Local validation evidence policy

The local-machine validation contract lives at:

```text
docs/LOCAL_VALIDATION_EVIDENCE/LOCAL_MACHINE_VALIDATION.md
```

Use it whenever a run creates ignored local reports under `output/**` and needs a Git-trackable compact evidence handoff.

## Historical task files

These remain useful as past state or scoped handoffs, but should not become the first reading path unless explicitly referenced:

```text
issue-57-docs-congruence-cleanup.md
issue-62-hybrid-master-ai-local-pipeline.md
post-pr*.md
next-chat-handoff-*.md
shared-*-next-task-*.md
project-complete-*.md
```

Historical files may be marked `superseded` or `historical` in future cleanup, but deletion requires explicit user approval.

## Inventory commands used by current flows

```powershell
python .\Tools\validation\build_markdown_inventory.py --repo-root . --output .\output\validation\markdown_inventory.json --markdown-output .\output\validation\markdown_inventory.md
python .\Tools\validation\build_script_inventory.py --repo-root . --output .\output\validation\script_inventory.json --csv-output .\output\validation\script_inventory.csv --markdown-output .\output\validation\script_inventory.md
```

`build_script_inventory.py` complements the older Python line-count CSV: it adds descriptions, functions, classes, methods, language and category for the full script/tool surface.

## Agent anti-laziness checklist

Before editing local-AI flow docs or wrappers, check these files explicitly:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1
Tools/workflow/run_local_ai_task_via_pipeline.ps1
Tools/workflow/run_post_validation_ai_packet.ps1
Tools/workflow/run_parallel_ai_provider_multistep.ps1
Tools/validation/check_ai_workload_report_quality.py
Tools/ai/build_agent_state_packet.py
Tools/ai/agent_state.py
Tools/npu/build_semantic_code_chunks.py
Tools/ai/build_ai_context_pack.py
docs/LOCAL_AI_TASKS/enrich-local-ai-memory-chunks-context-wrapper.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

If a documented tool is not present, do not pretend it is available. Either remove the reference or mark it explicitly as optional/future with a stop condition.
