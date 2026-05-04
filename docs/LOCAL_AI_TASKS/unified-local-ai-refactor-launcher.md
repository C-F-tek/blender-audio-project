# Unified Local AI Refactor Launcher

This is the canonical operator-facing runbook for `Tools/workflow/run_unified_local_ai_refactor.ps1`.

It replaces scattered 0-to-10 operating profiles as the active entrypoint. Historical 0-to-10 documents may remain as evidence or background, but new local AI runs should start here unless the user explicitly requests a legacy script.

## Absolute first instruction

Before running or modifying this launcher, read and obey:

```text
AGENTS.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
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

Custom intensity:

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
  -ProviderMaxContextChars 9000 `
  -ContextPackMaxTotalChars 32000 `
  -ContextPackMaxFileChars 2500 `
  -AgentStateMaxMemoryChars 12000 `
  -Model gpt-oss:20b `
  -SkipGitSync `
  -NoBranch
```

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
| `validation` | Run broader local validation wrapper. |
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
| `quick` | Fast validation/proposal loop, about 5 minutes when providers cooperate. | Lower rounds, files, context, tokens and keep-alive. |
| `balanced` | Default practical full run. | Current project defaults. |
| `deep` | Heavier full review. | Larger context, more rounds and larger memory/context pack surfaces. |
| `custom` | Operator-defined. | Use explicit numeric parameters. |

Legacy/full-toolbox inherited parameters exposed by the launcher:

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

These parameters exist so the unified launcher can replace older standalone 0-to-10/full-toolbox scripts without losing intensity control.

## External controls planned for the next launcher patch

The next patch should add CLI pass-through controls for all major input/output surfaces:

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

These controls are documented as the next step because the operator must be able to choose phase, intensity, input context, report inputs, artifact inputs and output destinations from the launch command.

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

The manifest must include:

```text
selected modes
full_0_to_10_requested
run_intensity
profile/model
Python executable and PYTHONPATH
intensity parameters
provider flags
workload_quality_report
workload_quality_routing_ok
primary_provider_requested
multistep_provider_workflow_requested
ollama_probe_requested
npu_probe_requested
npu_decode_smoke_requested
memory_in_enabled
memory_out_enabled
quality_gate_passed
context_files
report_files
phase_status
phase_reports
warnings
errors
patch_application_performed=false
```

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
