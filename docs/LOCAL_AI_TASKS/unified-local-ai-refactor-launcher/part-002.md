<!-- IA-CARMINE-MD-SPLIT: part -->
# unified-local-ai-refactor-launcher — parte 002 di 002

Sorgente indice: [`../unified-local-ai-refactor-launcher.md`](../unified-local-ai-refactor-launcher.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

## Full0To10 parameterized mode

`-Full0To10` resolves the full run-unica mode set automatically and must not ask for interactive mode selection.

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
CSV/count surfaces from inventory lanes
discovery/index drift visibility when relevant
```

`-Full0To10` does not enable the legacy NPU auditor provider. The production provider mesh starts GPU1, GPU0 peer support, NPU micro support and deterministic/broker bootstrap together inside the full-toolbox orchestrator; pass `-RunLegacyNpuAuditorProvider` only for diagnostics or old-vs-new comparison runs.

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

## Strict real-run activation and diagnostics

The launcher currently has strict real-run activation. Any non-smoke/non-reset real run may be promoted to the TUTTO SU TUTTO lane unless the operator explicitly passes:

```text
-NoStrictRealRunActivation
```

This is intentional for real product runs, but it is wrong for phase-by-phase diagnostics.

Observed diagnostic case on 2026-05-07:

```text
-Mode md without -NoStrictRealRunActivation started run_agent_review_full_toolbox_decision_loop.py
-Mode md without -NoStrictRealRunActivation started run_agent_gpu_npu_parallel_orchestrator.py
-Mode md without -NoStrictRealRunActivation started run_agent_gpu_deep_planning_supervised.py
-Mode md without -NoStrictRealRunActivation started an Ollama runner
```

Therefore, every smoke matrix or single-phase investigation must include:

```text
-SkipGitSync
-NoBranch
-AllowDirty
-NoStrictRealRunActivation
-Prod
-NoExecutionTail
```

Use strict activation only for real product/full runs. Do not use it to diagnose isolated `md`, `json`, `python`, `contract`, `chunks`, `context_pack` or `agent_state` phases.

### Correct single-phase diagnostic command

```powershell
$Stamp = "debug_python_nostrict_$(Get-Date -Format 'yyyyMMdd-HHmmss')"

powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -RepoRoot . `
  -Mode python `
  -TaskFile .\docs\LOCAL_AI_TASKS\pr206-patch-suggestion-product-full-run-2026-05-07.md `
  -Stamp $Stamp `
  -SkipGitSync `
  -NoBranch `
  -AllowDirty `
  -NoStrictRealRunActivation `
  -Prod `
  -NoExecutionTail
```

Expected for isolated diagnostics:

```text
No run_agent_gpu_npu_parallel_orchestrator.py
No run_agent_gpu_deep_planning_supervised.py
No Ollama runner
No provider/GPU/NPU subprocess unless the selected mode is provider or Full0To10
```

### Correct matrix argument block

```powershell
$Args = @(
  "-NoProfile",
  "-ExecutionPolicy", "Bypass",
  "-File", ".\Tools\workflow\run_unified_local_ai_refactor.ps1",
  "-RepoRoot", ".",
  "-Mode", $Case.Mode,
  "-TaskFile", $Task,
  "-Stamp", $Stamp,
  "-SkipGitSync",
  "-NoBranch",
  "-AllowDirty",
  "-NoStrictRealRunActivation",
  "-Prod",
  "-NoExecutionTail"
)
```

If the process list contains `run_agent_gpu*`, `run_npu*`, `run_agent_review_full_toolbox*` or `ollama.exe runner` during an isolated `md/json/python/contract` diagnostic, the diagnostic command is wrong or strict activation was not disabled.

### Cleanup command for contaminated diagnostics

Use this only to stop local diagnostic/provider processes. It does not delete files and does not change Git state.

```powershell
Get-CimInstance Win32_Process |
  Where-Object {
    $_.CommandLine -match "diag_|run_unified_local_ai_refactor|run_agent_gpu|run_npu|run_agent_review_full_toolbox|ollama.exe runner"
  } |
  ForEach-Object {
    Write-Host "Killing PID $($_.ProcessId) $($_.Name)"
    Stop-Process -Id $_.ProcessId -Force
  }
```

Then verify:

```powershell
ollama ps
nvidia-smi
```

## Run intensity parameters

All intensity presets preserve run-unica coverage. Intensity changes capacity, not scope.

| Intensity | Intended use | Effective behavior |
|---|---|---|
| `quick` | Fast full-coverage validation/proposal loop, about 5 minutes when providers cooperate. | Lower legacy-lane rounds, files, context, tokens and keep-alive while still running every Full0To10 lane. |
| `balanced` | Default practical complete run. | Current project defaults with every Full0To10 lane enabled unless explicitly disabled. |
| `deep` | Heavier complete review. | Larger legacy-lane context, more rounds and larger memory/context profile values with every Full0To10 lane enabled unless explicitly disabled. |
| `custom` | Operator-defined capacity. | Use explicit numeric parameters without reducing the Full0To10 lane set. |

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
-RunLegacyNpuAuditorProvider
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
Budget/round/file/context/token knobs are wired into the legacy full-toolbox integrated lane. NPU auditor knobs affect legacy provider execution only when -RunLegacyNpuAuditorProvider is supplied.
The production Full0To10 mesh passes GPU0/NPU startup-support settings to run_agent_gpu_npu_parallel_orchestrator.py and records round_000/overlap evidence before telemetry and bundle finalization.
RunIntensity presets update ProviderMaxContextChars, ContextPackMaxTotalChars, ContextPackMaxFileChars and AgentStateMaxMemoryChars in the manifest.
The subordinate context_pack, agent_state, official adapter and Ollama packet calls still need one more patch to pass every external/intensity knob through instead of using their current hardcoded/default values.
```

Do not claim full pass-through configurability until the external-controls follow-up lands.

## External controls planned for a follow-up launcher patch

The follow-up patch should add CLI pass-through controls for all major input/output surfaces and finish wiring the already-declared intensity parameters into subordinate calls:

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

Provider execution is explicit when the operator selects `-Full0To10`, `-UseOllamaAdvisory`, `-UsePrimaryAdvisoryProvider` or provider modes/flags.

Under `-Full0To10`, provider/probe/workload-quality lanes are included by default unless explicitly disabled or diagnosed unavailable. They are not additional per-lane opt-ins.

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
commit indexAI/code_chunks/**
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
Tools/validation/build_markdown_inventory.py
Tools/validation/build_script_inventory.py
Tools/validation/check_docs_links.py
Tools/validation/check_validation_report_contract.py
Tools/ai/build_agent_state_packet.py
Tools/ai/agent_state.py
Tools/npu/build_semantic_code_chunks.py
Tools/ai/build_ai_context_pack.py
```

If a tool is referenced in documentation but not available in the repository, either remove that reference or mark it clearly as future/optional. Do not describe non-existent capabilities as active.
