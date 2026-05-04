# Unified Local AI Refactor Launcher

This is the canonical operator-facing runbook for `Tools/workflow/run_unified_local_ai_refactor.ps1`.

It replaces scattered 0-to-10 operating profiles as the active entrypoint. Historical 0-to-10 documents are not active entrypoints. If legacy behavior is needed, it must be reached as a selected launcher lane or recovered from git history/compact evidence for forensic comparison.

## Absolute first instruction

Before running or modifying this launcher, read and obey:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

If any of these files are missing, stop. Do not infer their contents.

## Canonical command

Full selectable 0-to-10 flow:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity balanced `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

Quick 5-minute style run:

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

Custom legacy-lane intensity:

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

## One-flow rule

All local-AI execution profiles are launcher profiles, modes or flags.

This includes:

```text
quick tests
smoke tests
full runs
deep runs
provider runs
Ollama advisory
NPU probes
multistep provider workflow
SQLite memory handoff
context packs
semantic chunks
patch-spec generation
reset cleanup
full validation
legacy full-toolbox integrated behavior
```

Do not promote or document a second active operator entrypoint. Supporting wrappers may exist, but they must be called by the launcher or explicitly documented as implementation detail.

## What the launcher is

The launcher is a console-style selector and orchestrator for local AI project work. It controls what phases run and how much intensity they use.

It covers:

```text
Markdown inventory and link validation
JSON/report contract validation
Python/script inventory
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

Use that document for manifest fields, Full0To10 status semantics, quality-gate requirements, memory fields and future external-controls fields. `docs/JSON_SCHEMAS.md` remains the broad historical schema/reference file and should not be the first entrypoint for launcher-specific work.

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
| Launcher manifest | `Tools/workflow/run_unified_local_ai_refactor.ps1` | `unified_local_ai_refactor_manifest.json` with selected modes, flags, status, reports and context files. |
| Markdown inventory | `Tools/validation/build_markdown_inventory.py` | JSON plus Markdown inventory, including long-file classification when available. |
| Link validation | `Tools/validation/check_docs_links.py` | JSON docs-link report. |
| Script/tool inventory | `Tools/validation/build_script_inventory.py` | JSON, CSV and Markdown surfaces for script/function/class visibility. |
| Report contract | `Tools/validation/check_validation_report_contract.py` | JSON contract report for current run artifacts. |
| Workload quality | `Tools/validation/check_ai_workload_report_quality.py` | `ai_workload_report_quality.json` when provider routing is requested. |
| Semantic chunks | `Tools/npu/build_semantic_code_chunks.py` | semantic chunk manifest, not only raw chunk files. |
| Context pack | `Tools/ai/build_ai_context_pack.py` | bounded context pack Markdown/JSON and evidence summary. |
| Agent state / memory | `Tools/ai/build_agent_state_packet.py` | agent-state packet and optional SQLite memory handoff manifest. |
| Official pipeline adapter | `Tools/workflow/run_local_ai_task_via_pipeline.ps1` | packet/proposal manifest under the run pipeline directory. |
| Ollama advisory | `Tools/workflow/run_post_validation_ai_packet.ps1` | advisory packet/proposals plus manifest under AI pipeline output. |
| Multistep provider | `Tools/workflow/run_parallel_ai_provider_multistep.ps1` | provider workflow report/proposals when selected. |
| Legacy integrated lane | `Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1` | integrated full-toolbox report when `-Full0To10` enables it. |
| Patch specs | patch-spec builder/validator wrappers invoked by the pipeline | review-only patch-spec manifest and validation report. |
| Reset | launcher reset mode | reset plan JSON/Markdown; deletion only with explicit confirmation. |

When adding a new phase or wrapper, update this table and the manifest contract in the same PR.

## Length and readability policy

Large local-AI artifacts are allowed only as generated evidence, not as normal first-read documentation. The operator and the next AI agent must be able to understand a run from compact manifests before opening long files.

Policy:

```text
Normal maintained docs should stay compact and navigable.
Generated evidence may be longer, but must have a compact index/manifest.
Long Markdown files must be classified by inventory and either split, summarized or marked as historical/evidence.
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
| Large historical/evidence bundle | Any size only if unavoidable | Must be historical/evidence, indexed, and not used as the first operational entrypoint. |

A document that is too long to open quickly is not an acceptable primary interface. The primary interface is always:

```text
launcher command
manifest
phase reports
compact summary
then detailed evidence only when needed
```

## What a valid Full0To10 run means

A full 0-to-10 run is valid only when the requested capabilities are either completed or explicitly disabled by a `-No*` flag.

Expected true/default states for `-Full0To10`:

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

## Full0To10 profile

`-Full0To10` resolves the full mode set automatically and must not ask for interactive mode selection.

It enables, unless explicitly disabled:

```text
md,json,python,chunks,context_pack,agent_state,official,provider,patch_specs,evidence,contract,full_validation
UseOllamaAdvisory
UsePrimaryAdvisoryProvider
BuildWorkloadQualityReport
RunMultistepProviderWorkflow
RunOllamaProbe
RunNpuProbe
RunNpuDecodeSmoke
FullContextGoldenPath
BuildEvidence
GeneratePatchSpecs
SaveInputsToMemoryDb
RunLegacyFullToolboxIntegrated
```

Explicit disablers:

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

A disabled phase must appear as intentionally disabled, not missing by accident.

## Run intensity profiles

| Intensity | Intended use | Effective profile |
|---|---|---|
| `quick` | Fast validation/proposal loop, about 5 minutes when providers cooperate. | Lower legacy-lane rounds, files, context, tokens and keep-alive. |
| `balanced` | Default practical full run. | Current project defaults. |
| `deep` | Heavier full review. | Larger legacy-lane context, more rounds and larger memory/context profile values. |
| `custom` | Operator-defined. | Use explicit numeric parameters. |

Legacy/full-toolbox inherited parameters currently exposed by the launcher:

```text
-BudgetMinutes
-MaxRounds
-FilesPerRound
-MaxContextFiles
-MaxCharsPerFile
-MaxNewTokens
-KeepAlive
-NpuAuditorEveryRounds
-NpuAuditorTimeoutSeconds
-NpuMaxContextChars
-NpuMaxPromptChars
-NpuMaxNewTokens
-NpuFinalWaitSeconds
-MinRecommendations
-MinPatchPlans
-MaxRecommendations
-MaxPatchPlans
-RepositoryConsistencyMapWorkers
-ProviderMaxContextChars
-ContextPackMaxTotalChars
-ContextPackMaxFileChars
-AgentStateMaxMemoryChars
```

Current wiring status:

```text
Budget/round/file/context/token/NPU auditor knobs are wired into the legacy full-toolbox integrated lane.
RunIntensity presets update ProviderMaxContextChars, ContextPackMaxTotalChars, ContextPackMaxFileChars and AgentStateMaxMemoryChars in the manifest.
The subordinate context_pack, agent_state, official adapter and Ollama packet calls still need one more patch to pass every external/intensity knob through instead of using their current hardcoded/default values.
```

Do not claim full pass-through configurability until the next external-controls patch lands.

## External controls planned for the next launcher patch

The next patch should add CLI pass-through controls for all major input/output surfaces and finish wiring the already-declared intensity parameters into subordinate calls:

```text
-OutputRoot
-ValidationOutputDir
-AiPipelineOutputDir
-AiPacketsOutputDir
-PatchSpecOutputDir
-LocalRunsOutputDir
-EvidenceOutputDir
-ExternalContextFile
-ExternalReportFile
-ExternalArtifactFile
-OfficialBasename
-OfficialProposalBasename
-OllamaBasename
-OllamaProposalBasename
-MultistepBasename
-MultistepProposalBasename
-ContextPackBasename
-ContextPackEvidenceBasename
```

This patch must also replace these current hardcoded/default subordinate values:

```text
context pack: --max-total-chars 64000 -> $ContextPackMaxTotalChars
context pack: --max-file-chars 4000 -> $ContextPackMaxFileChars
agent state: --max-memory-chars 24000 -> $AgentStateMaxMemoryChars
official adapter: -MaxContextChars $MaxContextChars -> chosen provider/official context value
Ollama packet: -MaxContextChars $MaxContextChars -> chosen provider/Ollama context value
output dirs: output/local_ai_runs, output/validation, output/ai_pipeline, output/patch_specs -> external directory parameters
basenames: generated defaults -> operator-supplied basename parameters when provided
```

## SQLite memory policy

SQLite memory is an active local AI enrichment capability.

Relevant files:

```text
Tools/ai/agent_state.py
Tools/ai/build_agent_state_packet.py
Tools/ai/review_agent_memory.py
Tools/ai/agent_memory_policy.py
```

Default memory DB path:

```text
indexAI/agent_memory/agent_memory.sqlite
```

Policy:

```text
SQLite DB files are local/private runtime state.
Do not commit .sqlite/.db files.
Do not commit output/** files.
Commit only compact evidence or documented summaries when explicitly allowed.
```

`-SaveInputsToMemoryDb` is expected in `-Full0To10` unless `-NoMemoryWrite` is supplied.

## Provider and Ollama behavior

Provider execution must be explicit through `-Full0To10`, `-UseOllamaAdvisory`, `-UsePrimaryAdvisoryProvider` or the provider modes/flags.

Expected provider role:

```text
advisory/recommendation/proposal generation only
no automatic source patch application
no automatic commit/push
```

Ollama advisory is local advisory. Primary provider routing requires workload quality routing.

## Legacy full-toolbox lane

The unified launcher may call the integrated legacy full-toolbox lane through:

```text
Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1
```

This is not a separate operator entrypoint anymore. It is an internal selectable lane of the unified launcher so legacy full-toolbox controls remain available without splitting the workflow.

## Reset mode

`reset` is for local generated artifacts and stale run outputs.

Default behavior is plan-only. Real deletion requires both:

```text
-ApplyReset
-ConfirmResetText "DELETE LOCAL AI ARTIFACTS"
```

Reset may include memory/generated-index candidates only when explicitly requested:

```text
-IncludeMemoryReset
-IncludeGeneratedIndexReset
```

Never delete source files, docs, scripts, branch history or tracked project files through reset mode.

## Output contract

Every run writes:

```text
output/local_ai_runs/<stamp>_<mode>_unified/pipeline/unified_local_ai_refactor_manifest.json
```

The current manifest includes these verified fields:

```text
schema_version
kind
generated_at
repo_root
mode
mode_name
full_0_to_10_requested
available_modes
profile
model
run_intensity
legacy/intensity parameters
python_exe
python_exe_requested
pythonpath
ia_carmine_python_env
stamp
task_file
task_branch
run_dir
provider_execution_requested
primary_provider_requested
workload_quality_report
workload_quality_routing_ok
multistep_provider_workflow_requested
ollama_probe_requested
npu_probe_requested
npu_decode_smoke_requested
memory_in_enabled
memory_out_enabled
quality_gate_passed
reset_apply_requested
patch_application_performed=false
patch_specs_requested
build_evidence_requested
memory_db
save_inputs_to_memory_db
context_files
report_files
phase_status
phase_reports
warnings
errors
```

For the compact contract, see:

```text
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

After the external-controls patch, the manifest must also include selected external paths, basenames and external context/report/artifact inputs.

## Stop conditions

Stop or report failure if a requested phase needs a missing tool:

```text
agent_state requested but build_agent_state_packet.py or agent_state.py is missing
chunks requested but build_semantic_code_chunks.py is missing
context_pack requested but build_ai_context_pack.py is missing
provider requested but run_post_validation_ai_packet.ps1 is missing
official requested but run_local_ai_task_via_pipeline.ps1 is missing
primary provider requested but workload quality routing cannot be generated
reset apply requested without exact confirmation text
working tree dirty and -AllowDirty was not supplied
```

## Guardrails

The launcher is report/proposal-only by default.

It must not:

```text
apply patches automatically
commit
push
merge
force-push
rewrite history
run Blender runtime
run FFmpeg runtime
delete local artifacts unless explicit reset confirmation is supplied
commit SQLite DB files
commit output/** files
create long primary runbooks or monolithic evidence without a compact manifest
```

## Agent instruction

A lazy agent must not skip this mapping.

Before proposing changes to this launcher or to the local AI flow, explicitly check:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1
Tools/workflow/run_parallel_ai_provider_multistep.ps1
Tools/workflow/run_local_ai_task_via_pipeline.ps1
Tools/workflow/run_post_validation_ai_packet.ps1
Tools/validation/check_ai_workload_report_quality.py
Tools/ai/build_agent_state_packet.py
Tools/ai/agent_state.py
Tools/npu/build_semantic_code_chunks.py
Tools/ai/build_ai_context_pack.py
```

If a tool is referenced in documentation but not available in the repository, either remove that reference or mark it clearly as future/optional. Do not describe non-existent capabilities as active.
