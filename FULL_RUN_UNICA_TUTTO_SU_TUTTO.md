# IA-Carmine — FULL RUN UNICA / TUTTO SU TUTTO

Root-level launcher reference for the canonical full run.

Canonical procedure:

```text
docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
```

Patch-plan task for the current run:

```text
docs/LOCAL_AI_TASKS/full-run-unica-tutto-su-tutto-patch-plan-task.md
```

## Policy

```text
FULL RUN UNICA = TUTTO SU TUTTO
```

The canonical run activates every declared runtime/tool/provider/advisory/evidence/patch-spec/memory lane unless an explicit maintenance/debug `-No*` flag disables one.

Do not use these flags in the canonical run:

```text
-NoStrictRealRunActivation
-NoOllamaProbe
-NoNpuProbe
-NoNpuDecodeSmoke
-NoMultistepProvider
-NoWorkloadQuality
-NoMemoryWrite
-NoEvidence
-NoPatchSpecs
```

The run remains report/proposal oriented until a separate explicit patch-apply command is issued.

Destructive or irreversible operations are not runtime lanes and still require an explicit separate command:

```text
delete
force-push
rewrite history
merge to master/protected branch
deploy production
change secrets
change permissions
change billing
change repository visibility
```

## Naming rule: output-dir

Use directory terminology consistently:

```text
PowerShell launcher variable: $OutputDir
Future launcher parameter:   -OutputDir
Python CLI directory arg:    --output-dir
```

Do not invent `output-root` in new Python CLIs unless a tool already exposes it.

Important exception from current evidence:

```text
Tools/validation/check_ai_workload_report_quality.py currently exposes:
  --repo-root
  --report
  --output

It does not expose:
  --report-dir
```

So the current failure must be fixed by either:

```text
A. adding --report-dir support to check_ai_workload_report_quality.py; or
B. changing the launcher to expand $AiPacketsDir files and pass repeated --report arguments.
```

## First evidence from current run attempt

Observed during the `20260504-233106` full-run attempt:

```text
=== Generate provider workload probe inputs ===
AVVISO: Generate provider workload probe inputs failed with exit code 2
AVVISO: Ollama probe did not pass; Ollama workload report not written.

=== Build AI workload quality routing report ===

=== Validate task-scoped reports ===

=== Generate provider workload probe inputs ===
AVVISO: Generate provider workload probe inputs failed with exit code 2
AVVISO: Ollama probe did not pass; Ollama workload report not written.

=== Build AI workload quality routing report ===
usage: check_ai_workload_report_quality.py [-h] [--repo-root REPO_ROOT]
                                           [--report REPORT] [--output OUTPUT]
check_ai_workload_report_quality.py: error: unrecognized arguments: --report-dir output\ai_packets\20260504-233106
```

Immediate diagnostic meaning:

```text
- provider workload probe input generation failed before a valid Ollama workload report was produced;
- the Ollama workload report was not written;
- the workload-quality phase then called check_ai_workload_report_quality.py with unsupported --report-dir;
- this is a launcher/checker CLI contract mismatch and must be included in the patch plan.
```

## Complete launcher variable inventory

### Repository and task variables

```powershell
$RepoRoot = "C:\Users\carmi\blender\blender-audio-project"
$Branch = "codex/unified-local-ai-refactor-launcher"
$TaskFile = ".\docs\LOCAL_AI_TASKS\full-run-unica-tutto-su-tutto-patch-plan-task.md"
$Profile = "core"
$Model = "gpt-oss:20b"
```

### Stamp/version variables

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$DataStamp = $Stamp
```

### Input directory variables

```powershell
$InputDir = "."
$InputDocsDir = ".\docs"
$InputChatGptDir = ".\CHATGPT"
$InputToolsAiDir = ".\Tools\ai"
$InputToolsValidationDir = ".\Tools\validation"
$InputToolsWorkflowDir = ".\Tools\workflow"
$InputToolsNpuDir = ".\Tools\npu"
$InputScriptingV61bDir = ".\Scripting\v61b"
$InputScriptingSharedDir = ".\Scripting\shared"
```

### Output directory variables

```powershell
$OutputDir = ".\output"
$ValidationDir = Join-Path $OutputDir "validation"
$AiPipelineDir = Join-Path $OutputDir "ai_pipeline"
$AnalysisDir = Join-Path $OutputDir "analysis"
$PatchSpecsDir = Join-Path $OutputDir "patch_specs"
$LocalAiRunsDir = Join-Path $OutputDir "local_ai_runs"
$AiContextPacksDir = Join-Path $OutputDir "ai_context_packs"
```

### Git-trackable compact evidence directory

```powershell
$EvidenceDir = ".\docs\LOCAL_VALIDATION_EVIDENCE"
```

### AI packet directory variables

```powershell
$AiPacketsRoot = Join-Path $OutputDir "ai_packets"
$AiPacketsDir = Join-Path $AiPacketsRoot $DataStamp
```

### Local patch-bundle directory variables

```powershell
$PatchBundlesDir = Join-Path $ValidationDir "patch_bundles"
```

Never commit:

```text
output/**
output/validation/patch_bundles/**
renders/**
*.db
*.sqlite
*.sqlite3
```

### Provider/GPU planner variables

```powershell
$BudgetMinutes = 30
$MaxRounds = 300
$FilesPerRound = 8
$MaxContextFiles = 620
$MaxCharsPerFile = 12000
$MaxNewTokens = 4600
$KeepAlive = "35m"
```

### NPU auditor variables

```powershell
$NpuAuditorEveryRounds = 3
$NpuAuditorTimeoutSeconds = 420
$NpuMaxContextChars = 8000
$NpuMaxPromptChars = 1200
$NpuMaxNewTokens = 384
$NpuFinalWaitSeconds = 180
```

### Recommendation and patch-plan variables

```powershell
$MinRecommendations = 1
$MinPatchPlans = 1
$MaxRecommendations = 220
$MaxPatchPlans = 220
```

### Context, repository consistency and memory variables

```powershell
$RepositoryConsistencyMapWorkers = 8
$ContextPackMaxTotalChars = 84000
$ContextPackMaxFileChars = 4000
$AgentStateMaxMemoryChars = 34000
$MaxContextChars = 12000
$MemoryDb = ".\indexAI\agent_memory\agent_memory.sqlite"
```

### Matrix/smoke variables

```powershell
$MatrixWorkers = 12
$RepeatCases = 2
```

### Expected output report path variables

```powershell
$IntegratedReport = Join-Path $ValidationDir "agent_review_full_toolbox_decision_loop_${Stamp}_integrated.json"
$WorkflowReport = Join-Path $ValidationDir "agent_review_full_toolbox_decision_loop_${Stamp}_workflow.json"
$DecisionLoopReport = Join-Path $AiPipelineDir "full_toolbox_${Stamp}_agent_review_decision_loop.json"
$PatchPlanReport = Join-Path $PatchSpecsDir "full_toolbox_${Stamp}_agent_review_patch_plan.json"
$OrchestratorReport = Join-Path $AiPipelineDir "full_toolbox_${Stamp}_orchestrator.json"
$GpuReport = Join-Path $AiPipelineDir "full_toolbox_${Stamp}_parallel_gpu.json"
$EvidenceSufficiencyReport = Join-Path $AiPipelineDir "agent_review_evidence_sufficiency.json"
```

## Canonical full launcher script

```powershell
# ============================================================
# IA-Carmine — FULL RUN UNICA / TUTTO SU TUTTO
# ============================================================

$RepoRoot = "C:\Users\carmi\blender\blender-audio-project"
Set-Location $RepoRoot

$Branch = "codex/unified-local-ai-refactor-launcher"
$TaskFile = ".\docs\LOCAL_AI_TASKS\full-run-unica-tutto-su-tutto-patch-plan-task.md"
$Profile = "core"
$Model = "gpt-oss:20b"

$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$DataStamp = $Stamp

$InputDir = "."
$InputDocsDir = ".\docs"
$InputChatGptDir = ".\CHATGPT"
$InputToolsAiDir = ".\Tools\ai"
$InputToolsValidationDir = ".\Tools\validation"
$InputToolsWorkflowDir = ".\Tools\workflow"
$InputToolsNpuDir = ".\Tools\npu"
$InputScriptingV61bDir = ".\Scripting\v61b"
$InputScriptingSharedDir = ".\Scripting\shared"

$OutputDir = ".\output"
$ValidationDir = Join-Path $OutputDir "validation"
$AiPipelineDir = Join-Path $OutputDir "ai_pipeline"
$AnalysisDir = Join-Path $OutputDir "analysis"
$PatchSpecsDir = Join-Path $OutputDir "patch_specs"
$LocalAiRunsDir = Join-Path $OutputDir "local_ai_runs"
$AiContextPacksDir = Join-Path $OutputDir "ai_context_packs"

$EvidenceDir = ".\docs\LOCAL_VALIDATION_EVIDENCE"
$AiPacketsRoot = Join-Path $OutputDir "ai_packets"
$AiPacketsDir = Join-Path $AiPacketsRoot $DataStamp
$PatchBundlesDir = Join-Path $ValidationDir "patch_bundles"

$BudgetMinutes = 30
$MaxRounds = 300
$FilesPerRound = 8
$MaxContextFiles = 620
$MaxCharsPerFile = 12000
$MaxNewTokens = 4600
$KeepAlive = "35m"

$NpuAuditorEveryRounds = 3
$NpuAuditorTimeoutSeconds = 420
$NpuMaxContextChars = 8000
$NpuMaxPromptChars = 1200
$NpuMaxNewTokens = 384
$NpuFinalWaitSeconds = 180

$MinRecommendations = 1
$MinPatchPlans = 1
$MaxRecommendations = 220
$MaxPatchPlans = 220

$RepositoryConsistencyMapWorkers = 8
$ContextPackMaxTotalChars = 84000
$ContextPackMaxFileChars = 4000
$AgentStateMaxMemoryChars = 34000
$MaxContextChars = 12000
$MemoryDb = ".\indexAI\agent_memory\agent_memory.sqlite"

$MatrixWorkers = 12
$RepeatCases = 2

# Preflight: canonical full run must start from a clean source tree.
git status --short

powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Mode all `
  -Full0To10 `
  -Stamp $Stamp `
  -TaskFile $TaskFile `
  -TaskBranch $Branch `
  -AiPacketsRoot $AiPacketsRoot `
  -AiPacketsDir $AiPacketsDir `
  -Profile $Profile `
  -Model $Model `
  -RunIntensity custom `
  -BudgetMinutes $BudgetMinutes `
  -MaxRounds $MaxRounds `
  -FilesPerRound $FilesPerRound `
  -MaxContextFiles $MaxContextFiles `
  -MaxCharsPerFile $MaxCharsPerFile `
  -MaxNewTokens $MaxNewTokens `
  -KeepAlive $KeepAlive `
  -NpuAuditorEveryRounds $NpuAuditorEveryRounds `
  -NpuAuditorTimeoutSeconds $NpuAuditorTimeoutSeconds `
  -NpuMaxContextChars $NpuMaxContextChars `
  -NpuMaxPromptChars $NpuMaxPromptChars `
  -NpuMaxNewTokens $NpuMaxNewTokens `
  -NpuFinalWaitSeconds $NpuFinalWaitSeconds `
  -MinRecommendations $MinRecommendations `
  -MinPatchPlans $MinPatchPlans `
  -MaxRecommendations $MaxRecommendations `
  -MaxPatchPlans $MaxPatchPlans `
  -RepositoryConsistencyMapWorkers $RepositoryConsistencyMapWorkers `
  -ContextPackMaxTotalChars $ContextPackMaxTotalChars `
  -ContextPackMaxFileChars $ContextPackMaxFileChars `
  -AgentStateMaxMemoryChars $AgentStateMaxMemoryChars `
  -MaxContextChars $MaxContextChars `
  -MemoryDb $MemoryDb `
  -MatrixWorkers $MatrixWorkers `
  -RepeatCases $RepeatCases
```

## Post-run inspection

```powershell
$IntegratedReport = Join-Path $ValidationDir "agent_review_full_toolbox_decision_loop_${Stamp}_integrated.json"
$WorkflowReport = Join-Path $ValidationDir "agent_review_full_toolbox_decision_loop_${Stamp}_workflow.json"
$DecisionLoopReport = Join-Path $AiPipelineDir "full_toolbox_${Stamp}_agent_review_decision_loop.json"
$PatchPlanReport = Join-Path $PatchSpecsDir "full_toolbox_${Stamp}_agent_review_patch_plan.json"

Get-Content $IntegratedReport -Raw |
  ConvertFrom-Json |
  Select-Object passed, provider_execution_performed, recommendation_count, patch_plan_count, base_workflow_passed, warning_policy_passed, decision_recovered

Get-Content $DecisionLoopReport -Raw |
  ConvertFrom-Json |
  Select-Object passed, recommendation_count, patch_plan_count, deterministic_synthesizer_used, patch_plan_fallback_used, errors, warnings

Get-Content $PatchPlanReport -Raw |
  ConvertFrom-Json |
  Select-Object passed, patch_plan_count, manual_review_required, provider_execution_performed, patch_application_performed, source_writes_performed

git status --short
```

## Patch-plan requirements from the current evidence

The next AI-generated patch plan must include at least:

```text
1. Fix provider workload probe input generation failure.
2. Fix check_ai_workload_report_quality.py CLI mismatch:
   - add --report-dir support; or
   - stop passing --report-dir and pass explicit --report files.
3. Add launcher-level -OutputDir and -EvidenceDir or document why they remain script variables only.
4. Wire OutputDir/EvidenceDir into integrated/base workflow where supported.
5. Preserve FULL RUN UNICA / TUTTO SU TUTTO behavior.
6. Preserve report/proposal-only default: no patch apply without explicit apply command.
```

## Big patch launcher contract

This repository now treats the root full-run script as the executable reference for the canonical all-lanes run.

Contract additions:

- `$OutputDir` is the PowerShell launcher variable for local runtime output.
- `-OutputDir` is the launcher parameter to be wired by the workflow.
- Python tools continue to use `--output-dir` when they accept an output directory.
- `$EvidenceDir` is the compact evidence directory.
- `$AiPacketsRoot` defaults to `$OutputDir/ai_packets` when not explicitly supplied.
- `$AiPacketsDir` defaults to `$AiPacketsRoot/$DataStamp` when not explicitly supplied.
- Early failure-tail evidence must work even before the normal run manifest is fully built.
- `check_ai_workload_report_quality.py` must accept `--report-dir` and report `report_dir_cli_supported=true`.

The previous observed failure is therefore classified as a launcher/checker contract regression if it reappears after this patch.
