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

## Unified full product phase

The full product phase is still owned by this launcher. Do not run the internal Python tools as the normal product interface.

The launcher product flow is:

```text
Task Markdown
-> launcher-owned Stamp
-> Full0To10 provider/tool/broker/validator/evidence loop
-> BuildTaskPatchSuggestionReport
-> ReviewPrApplyDeterministicSuggestions
-> product-vs-supplemental validation
-> PrepareReviewPr
-> draft GitHub PR
```

Relevant launcher product flags:

```text
-BuildTaskPatchSuggestionReport
-ReviewPrApplyDeterministicSuggestions
-PrepareReviewPr
-ReviewPrBranch <CARMINEai/...>
-ReviewPrBaseBranch master
-ReviewPrTitle <title>
-ReviewPrCommitMessage <message>
-ReviewPrPush
-ReviewPrCreate
```

`$Stamp` is a single launcher variable. The launcher receives or creates it once, then propagates it to internal tools and report paths. Do not create a second unrelated stamp for patch apply, evidence, PR prep or provider reports.

`$BudgetMinutes` is a launcher capacity knob. It changes the available time budget for the run; it must not reduce semantic scope. Use it with `-RunIntensity` to control duration while keeping provider/tool/broker/validator lanes selected.

`ReviewPrIncludePath` is an emergency/additive override only. The product path should derive staged source/doc paths from the `patch_suggestion_bundle_apply` report generated in the same launcher run.

PRs created by the review phase should be draft unless explicitly promoted later after human review.

## Current product command shape

Use this shape from the repository root. Replace only the task file and PR title/message.

```powershell
$Stamp = "full_product_$(Get-Date -Format 'yyyyMMdd-HHmmss')"
$Task = ".\docs\LOCAL_AI_TASKS\<TASK_MD_REALE>.md"
$BudgetMinutes = 45

$env:IA_CARMINE_PYTHON = (Resolve-Path ".\.venv\Scripts\python.exe").Path
$env:PYTHONPATH = (Resolve-Path ".").Path

powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -RepoRoot . `
  -TaskFile $Task `
  -Stamp $Stamp `
  -Profile core `
  -Model qwen2.5-coder:14b `
  -Full0To10 `
  -RunIntensity balanced `
  -BudgetMinutes $BudgetMinutes `
  -BuildTaskPatchSuggestionReport `
  -ReviewPrApplyDeterministicSuggestions `
  -PrepareReviewPr `
  -ReviewPrBranch "CARMINEai/full-product-$Stamp" `
  -ReviewPrBaseBranch "master" `
  -ReviewPrTitle "feat(ai): full product review $Stamp" `
  -ReviewPrCommitMessage "feat(ai): apply full product review" `
  -ReviewPrPush `
  -ReviewPrCreate `
  -ContinueOnValidationError
```

`-ContinueOnValidationError` is acceptable for this product lane only when provider degradation is captured in reports and the deterministic patch/apply/PR phase can still produce a reviewable product. It must not hide missing product reports, unsafe staging, failed deterministic patch application, failed commit/push or failed PR creation.

## Complete launcher parameter inventory

Source: `Tools/workflow/run_unified_local_ai_refactor.ps1` `param(...)` block.

### Repository, task and output identity

```text
-RepoRoot
-Mode
-TaskFile
-TaskBranch
-Stamp
-OutputDir
-EvidenceDir
-AiPacketsRoot
-AiPacketsDir
```

### Profile, model, intensity and budget

```text
-Profile                     # core | npu | docs
-Model
-RunIntensity                # quick | balanced | deep | custom
-BudgetMinutes
-MaxRounds
-FilesPerRound
-MaxContextFiles
-MaxCharsPerFile
-MaxNewTokens
-KeepAlive
```

### NPU / provider capacity knobs

```text
-NpuAuditorEveryRounds
-NpuAuditorTimeoutSeconds
-NpuMaxContextChars
-NpuMaxPromptChars
-NpuMaxNewTokens
-NpuFinalWaitSeconds
-NpuMicroStartMode           # startup | deferred | live-seed-only | peer | post-gpu-provider | disabled
-ProviderMaxContextChars
-MaxContextChars
```

### Recommendation, patch-plan and repository consistency limits

```text
-MinRecommendations
-MinPatchPlans
-MaxRecommendations
-MaxPatchPlans
-RepositoryConsistencyMapWorkers
```

### Context pack and memory sizing

```text
-ContextPackMaxTotalChars
-ContextPackMaxFileChars
-AgentStateMaxMemoryChars
-MemoryDb
-SaveInputsToMemoryDb
-NoMemoryWrite
```

### Python and operator/session controls

```text
-PythonExe
-Interactive
-SkipGitSync
-NoBranch
-AllowDirty
-DryRun
-ContinueOnValidationError
-NoStrictRealRunActivation
-Prod
-NoExecutionTail
```

### Full0To10 and provider lanes

```text
-Full0To10
-BuildWorkloadQualityReport
-UseOllamaAdvisory
-UsePrimaryAdvisoryProvider
-RunMultistepProviderWorkflow
-RunLegacyFullToolboxIntegrated
-RunLegacyNpuAuditorProvider
-RunOllamaProbe
-RunNpuProbe
-RunNpuDecodeSmoke
-RunOpenVinoGpu0Workload
```

### Explicit lane disablers

```text
-NoOllamaProbe
-NoNpuProbe
-NoNpuDecodeSmoke
-NoMultistepProvider
-NoWorkloadQuality
-NoEvidence
-NoPatchSpecs
```

### Evidence, patch specs and context breadth

```text
-BuildEvidence
-GeneratePatchSpecs
-FullContextGoldenPath
-OfficialAdapterTimeoutSeconds
-SkipOfficialAdapter
```

### Reset and generated artifact cleanup

```text
-ResetBeforeDate
-ApplyReset
-ConfirmResetText
-IncludeMemoryReset
-IncludeGeneratedIndexReset
```

### Matrix/smoke controls

```text
-MatrixWorkers
-RepeatCases
```

### LightFull0To10 profile

```text
-LightFull0To10
-LightFull0To10OutputDir
-LightFull0To10NoExternalProbes
```

### Review PR product controls

```text
-BuildTaskPatchSuggestionReport
-ReviewPrApplyDeterministicSuggestions
-PrepareReviewPr
-ReviewPrBranch
-ReviewPrBaseBranch
-ReviewPrRemote
-ReviewPrTitle
-ReviewPrCommitMessage
-ReviewPrIncludePath
-ReviewPrPush
-ReviewPrCreate
```

## Run intensity parameters

All intensity presets preserve run-unica coverage. Intensity changes capacity, not scope.

| Intensity | Intended use | Effective behavior |
|---|---|---|
| `quick` | Fast full-coverage validation/proposal loop, about 5 minutes when providers cooperate. | Lower legacy-lane rounds, files, context, tokens and keep-alive while still running every Full0To10 lane. |
| `balanced` | Default practical complete run. | Current project defaults with every Full0To10 lane enabled unless explicitly disabled. |
| `deep` | Heavier complete review. | Larger legacy-lane context, more rounds and larger memory/context profile values with every Full0To10 lane enabled unless explicitly disabled. |
| `custom` | Operator-defined capacity. | Use explicit numeric parameters without reducing the Full0To10 lane set. |

Current wiring status:

```text
Budget/round/file/context/token knobs are wired into the legacy full-toolbox integrated lane.
NPU auditor knobs affect legacy provider execution only when -RunLegacyNpuAuditorProvider is supplied.
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
no direct source patch application
no direct commit/push/merge
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

The manifest must remain the first machine-readable entrypoint for the run. Long evidence bundles are not the first interface.

For the compact contract, see:

```text
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
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
review PR product requested but patch apply report, safe changed paths, commit, push or PR creation fails
reset apply requested without exact confirmation text
working tree dirty and -AllowDirty was not supplied
```

## Guardrails

The launcher is report/proposal-only by default.

It must not:

```text
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

Patch application, commit, push and draft PR creation are allowed only when the explicit review-PR product flags are supplied and branch/path policies pass.

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
Tools/ai/build_task_patch_suggestion_report.py
Tools/ai/apply_patch_suggestion_bundle.py
Tools/ai/prepare_review_pr.py
Tools/validation/check_patch_suggestion_product_separation.py
```

If a tool is referenced in documentation but not available in the repository, either remove that reference or mark it clearly as future/optional. Do not describe non-existent capabilities as active.
