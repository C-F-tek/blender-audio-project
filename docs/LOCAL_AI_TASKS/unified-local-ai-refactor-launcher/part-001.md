<!-- IA-CARMINE-MD-SPLIT: part -->
# unified-local-ai-refactor-launcher — parte 001 di 002

Sorgente indice: [`../unified-local-ai-refactor-launcher.md`](../unified-local-ai-refactor-launcher.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

# Unified Local AI Refactor Launcher

This is the canonical operator-facing runbook for `Tools/workflow/run_unified_local_ai_refactor.ps1`.

It is the **run unica** entrypoint. Historical 0-to-10 documents are not active entrypoints. If legacy behavior is needed, it must be reached as a selected launcher lane or recovered from git history/compact evidence for forensic comparison.

## Absolute first instruction

Before running or modifying this launcher, read and obey:

```text
AGENTS.md
CHATGPT.md
CHATGPT/README.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

If any of these files are missing, stop. Do not infer their contents.

## Run unica doctrine

The primary model is one parameterized run:

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters
-No* flags = explicit opt-out from selected lanes
```

`-Full0To10` means the whole active perimeter. `-RunIntensity quick|balanced|deep|custom` changes budgets, limits, context, rounds, tokens and keep-alive; it must not change semantic scope.

CSV/count, discovery and index-repair visibility are evidence surfaces in the run-unica perimeter when relevant.

## Canonical commands

Balanced run-unica / TUTTO SU TUTTO:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity balanced `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

Quick run-unica with reduced budget:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity quick `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

Deep run-unica with expanded budget:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity deep `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

Custom run-unica with explicit operator parameters:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity custom `
  -BudgetMinutes 5 `
  -MaxRounds 4 `
  -FilesPerRound 4 `
  -MaxContextFiles 80 `
  -MaxCharsPerFile 4000 `
  -MaxNewTokens 1600 `
  -KeepAlive 8m `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

## Coverage rule: TUTTO SU TUTTO

Every `-Full0To10` run variation is a whole-perimeter run.

All run-unica variations must still cover, unless an explicit `-No*` flag disables a capability or a lane is diagnosed unavailable:

```text
Markdown inventory and docs links
JSON/report contract validation
Python/script inventory
Python line-count CSV/MD surface
function/class/method inventory CSV surface
semantic chunks
selected chunk evidence when available
context pack
agent-state and memory handoff
repository consistency and validation evidence
auto-discovery/index drift evidence when relevant
index repair plan/report when relevant
runtime tool broker telemetry
runtime tool capability manifest
provider probes and provider diagnostics
GPU/Ollama advisory path
NPU probe/decode diagnostics
multistep provider workflow
legacy full-toolbox integrated lane
workload quality routing
patch-spec generation and validation
compact evidence bundle
final validation
shared AI-to-AI bundle summary
```

A quick run-unica is therefore TUTTO SU TUTTO with smaller budgets, not a partial smoke. A smoke run remains a separate `smoke` mode and must not be represented as a full run.

A run-unica report is incomplete if a core lane is missing without one of these conditions:

```text
explicit -No* disabler
clear unavailable-tool/provider failure recorded in manifest, warnings or phase report
DryRun planned-but-not-executed state
documented operator exclusion
```

## One-flow rule

All local-AI execution variants are launcher modes, parameters, presets or flags.

This includes:

```text
quick tests
smoke tests
complete runs
deep runs
custom parameterized runs
provider runs
Ollama advisory
NPU probes
multistep provider workflow
SQLite memory handoff
context packs
semantic chunks
selected chunk evidence
patch-spec generation
runtime broker telemetry
runtime capability manifest
CSV/count surfaces
auto-discovery/index repair visibility
reset cleanup
full validation
legacy full-toolbox integrated behavior
```

Do not promote or document a second active operator entrypoint. Supporting wrappers may exist, but they must be called by the launcher or explicitly documented as implementation detail.

## What the launcher is

The launcher is a console-style selector and orchestrator for local AI project work. It controls what phases run and how much capacity they use.

It covers:

```text
Markdown inventory and link validation
JSON/report contract validation
Python/script inventory
CSV/count evidence surfaces
discovery/index drift and repair planning evidence
semantic chunks
bounded context packs
agent-state packet and optional SQLite memory input/output
official local AI task pipeline adapter
Ollama advisory
primary provider routing
multistep provider workflow
Ollama/NPU probes
review-only patch specs
compact evidence
final validation
local generated-artifact reset planning
```

## Contract document

The compact machine-readable contract for the launcher manifest is:

```text
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

Use that document for manifest fields, Full0To10 status semantics, quality-gate requirements, memory fields and future external-controls fields. `docs/JSON_SCHEMAS.md` is a broad historical schema/catalog notebook and should not be the first entrypoint for launcher-specific work.

## Visibility contract: functions, tools, phases and evidence

The unified launcher must make every important action visible through machine-readable and human-readable outputs. No phase may be hidden behind a long opaque bundle.

For each selected phase, the run should expose at least one of:

```text
phase_status entry in unified_local_ai_refactor_manifest.json
phase_reports entry in unified_local_ai_refactor_manifest.json
context_files entry in unified_local_ai_refactor_manifest.json
report_files entry in unified_local_ai_refactor_manifest.json
compact Markdown summary
CSV/JSON inventory with stable path references
```

The required visibility surfaces are:

| Area | Tool/script | Expected visible output |
|---|---|---|
| Launcher manifest | `Tools/workflow/run_unified_local_ai_refactor.ps1` | `unified_local_ai_refactor_manifest.json` with selected parameters, flags, status, reports and context files. |
| Markdown inventory | `Tools/validation/build_markdown_inventory.py` | JSON plus Markdown inventory, including long-file classification when available. |
| Link validation | `Tools/validation/check_docs_links.py` | JSON docs-link report. |
| Script/tool inventory | `Tools/validation/build_script_inventory.py` | JSON, CSV and Markdown surfaces for script/function/class visibility. |
| Python line count | broker/runtime line-count helper and validation reports | CSV and Markdown line-count surfaces. |
| Function/class/method inventory | `Tools/validation/build_script_inventory.py` | CSV/JSON callable-surface evidence for refactor/reuse review. |
| Auto-discovery/index repair | scanner/index validators and repair planners | Report-only discovery/index drift or repair-plan report. |
| Report contract | `Tools/validation/check_validation_report_contract.py` | JSON contract report for current run artifacts. |
| Workload quality | `Tools/validation/check_ai_workload_report_quality.py` | `ai_workload_report_quality.json` when provider routing is requested or Full0To10 selected. |
| Semantic chunks | `Tools/npu/build_semantic_code_chunks.py` | semantic chunk manifest, not only raw chunk files. |
| Selected chunks | selected chunk validator/evidence lane | selected chunk evidence when available. |
| Context pack | `Tools/ai/build_ai_context_pack.py` | bounded context pack Markdown/JSON and evidence summary. |
| Agent state / memory | `Tools/ai/build_agent_state_packet.py` | agent-state packet and optional SQLite memory handoff manifest. |
| Official pipeline adapter | `Tools/workflow/run_local_ai_task_via_pipeline.ps1` | packet/proposal manifest under the run pipeline directory. |
| Ollama advisory | `Tools/workflow/run_post_validation_ai_packet.ps1` | advisory packet/proposals plus manifest under AI pipeline output. |
| Multistep provider | `Tools/workflow/run_parallel_ai_provider_multistep.ps1` | provider workflow report/proposals when selected. |
| Legacy integrated lane | `Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1` | integrated full-toolbox report when `-Full0To10` enables it. |
| Runtime broker | `Tools/ai/agent_runtime_tool_broker.py` | runtime broker report consumed by telemetry. |
| Runtime telemetry | `Tools/ai/build_runtime_tool_usage_telemetry.py` | runtime tool usage telemetry JSON/MD. |
| Runtime capability manifest | `Tools/ai/build_runtime_tool_capability_manifest.py` | runtime tool capability manifest JSON/MD. |
| Full toolbox telemetry summary | `Tools/ai/build_full_toolbox_run_telemetry_summary.py` | full toolbox run telemetry summary JSON/MD. |
| Shared AI-to-AI bundle | `Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py` | shared bundle and final summary. |
| Patch specs | patch-spec builder/validator wrappers invoked by the pipeline | review-only patch-spec manifest and validation report. |
| Reset | launcher reset mode | reset plan JSON/Markdown; deletion only with explicit confirmation. |

When adding a new phase or wrapper, update this table and the manifest contract in the same PR.

## Large Markdown and readability policy

Large local-AI artifacts are allowed only as generated evidence, schema catalogs, historical/supporting references or application-domain docs, not as first-read operational entrypoints.

Policy owner:

```text
docs/LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md
```

Policy:

```text
Normal maintained docs should stay compact and navigable.
Generated evidence may be longer, but must have a compact index/manifest.
Long Markdown files must be classified by inventory and either split, summarized or marked as historical/evidence/catalog/application-domain.
No active runbook should require opening an 8000-line bundle before the manifest/summary has been read.
Do not create new monolithic AI-to-AI bundles without a companion summary and deterministic manifest.
Do not commit output/**, SQLite DBs or raw local cache files.
```

Operational thresholds:

| File type | Preferred maximum | Required action when exceeded |
|---|---:|---|
| Active operator runbook | ~500 lines | Split into task-specific docs or move verbose evidence to generated artifacts. |
| Maintained source documentation | ~700 lines | Add table of contents, split sections or create subordinate docs. |
| Generated compact evidence | ~1200 lines | Add a summary/manifest and classify as evidence snapshot. |
| Large historical/evidence/catalog bundle | Any size only if unavoidable | Must be classified, indexed and not used as the first operational entrypoint. |

A document that is too long to open quickly is not an acceptable primary interface.

## What a valid run-unica Full0To10 means

A run-unica `-Full0To10` run is valid only when the requested capabilities are either completed or explicitly disabled by a `-No*` flag, diagnosed unavailable, represented as dry-run planned state or excluded by a documented operator decision.

Expected true/default states for `-Full0To10`:

```text
pipeline adapter ufficiale eseguito
packet/proposals generati
Ollama advisory usato or explicitly diagnosed unavailable/degraded
patch specs creati e validati
primary provider routing completo
workload quality routing presente
multistep provider workflow richiesto
probe Ollama/NPU richiesti
context pack presente
SQLite memory IN/OUT presente quando non disabilitata
quality gate registrato nel manifest
runtime broker telemetry presente
runtime capability manifest presente
CSV/count surfaces presenti quando inventory lanes run
discovery/index drift surfaces presenti quando rilevanti
patch_application_performed=false
```

If `-UsePrimaryAdvisoryProvider` or `-Full0To10` is used, the launcher must not silently degrade when workload quality routing is missing. It must build `output/validation/ai_workload_report_quality.json` or fail clearly. In `-DryRun`, it may mark that generation as planned.

## Active modes

Safe execution order:

```text
baseline
  -> smoke
  -> reset
  -> validation
  -> md
  -> json
  -> python
  -> chunks
  -> context_pack
  -> agent_state
  -> workload_quality
  -> legacy_full_toolbox_integrated
  -> official
  -> provider
  -> multistep provider/probes
  -> patch_specs
  -> evidence
  -> contract
  -> full_validation
```

Mode catalog:

| Mode | Purpose |
|---|---|
| `smoke` | Fast health checks. |
| `reset` | Plan or explicitly apply cleanup of old local generated artifacts. |
| `validation` | Run broader local validation wrapper through launcher selection. |
| `md` | Build Markdown inventory and docs link report. |
| `json` | Validate JSON/report contracts from the current run. |
| `python` | Build script/tool inventory with CSV and Markdown outputs. |
| `chunks` | Build semantic chunks for focused context. |
| `context_pack` | Build bounded AI context packs. |
| `agent_state` | Build local agent-state packet and optional SQLite-backed memory context. |
| `official` | Run the project-owned local AI task pipeline adapter. |
| `provider` | Run advisory/provider path. |
| `patch_specs` | Generate review-only patch specs from proposals. |
| `evidence` | Build compact evidence artifacts when requested. |
| `contract` | Validate task-scoped reports. |
| `full_validation` | Final diff/status and consistency checks. |
| `all` | Run all standard safe phases. |
