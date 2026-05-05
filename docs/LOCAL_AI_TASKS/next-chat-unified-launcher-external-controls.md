# Next chat handoff — Unified launcher external controls

## Repository

- Repository: `C-F-tek/blender-audio-project`
- Branch: `codex/unified-local-ai-refactor-launcher`
- PR: #187
- Current objective: finish replacing parallel 0-to-10 workflows with one selectable unified launcher.

## Current confirmed state

The unified launcher already supports:

```text
-Full0To10
selectable modes
explicit -No* disablers
.venv Python resolution
PYTHONPATH set to repo root
dry-run without interactive mode prompt
dry-run tolerance for planned workload quality report
legacy full-toolbox 0-to-10 controls inherited into the unified launcher
-RunIntensity quick|balanced|deep|custom
legacy full toolbox integrated lane via run_agent_review_full_toolbox_decision_loop_integrated.ps1
no automatic patch apply
no automatic commit/push/merge
no Blender/FFmpeg execution
manifest fields for full_0_to_10_requested, run_intensity, workload_quality_routing_ok, quality_gate_passed, memory_in_enabled and memory_out_enabled
```

Recent relevant commits on this branch:

```text
e09abbf feat(workflow): inherit legacy full toolbox 0-to-10 controls
d3f1bd9 docs(workflow): document unified full 0-to-10 launcher
1143c7c docs(ai): make unified launcher the canonical 0-to-10 entrypoint
b3f1ac3 docs: point root README to unified local AI launcher
74b6a9b docs: update agent contract for unified 0-to-10 launcher
c2e1c1a docs: route local AI workflows through unified launcher
d3c2796 docs: update documentation index for unified 0-to-10 launcher
1199242 docs(workflow): clarify current launcher parameter wiring
```

## Verified code-reference state

Compared against `Tools/workflow/run_unified_local_ai_refactor.ps1` in PR #187.

Current exposed parameters include:

```text
-RunIntensity
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
-MemoryDb
-SaveInputsToMemoryDb
-MatrixWorkers
-RepeatCases
```

Confirmed wiring:

```text
BudgetMinutes, MaxRounds, FilesPerRound, MaxContextFiles, MaxCharsPerFile, MaxNewTokens, KeepAlive and NPU auditor knobs are passed to run_agent_review_full_toolbox_decision_loop_integrated.ps1.
Full0To10 enables UseOllamaAdvisory, UsePrimaryAdvisoryProvider, FullContextGoldenPath, BuildWorkloadQualityReport, RunMultistepProviderWorkflow, RunOllamaProbe, RunNpuProbe, RunNpuDecodeSmoke, SaveInputsToMemoryDb, BuildEvidence, GeneratePatchSpecs and RunLegacyFullToolboxIntegrated unless disabled.
Manifest records full_0_to_10_requested, run_intensity, intensity parameters, workload_quality_routing_ok, memory_in_enabled, memory_out_enabled and quality_gate_passed.
```

Confirmed gaps to fix next:

```text
ContextPackMaxTotalChars is exposed but context_pack still calls build_ai_context_pack.py with --max-total-chars 64000.
ContextPackMaxFileChars is exposed but context_pack still calls build_ai_context_pack.py with --max-file-chars 4000.
AgentStateMaxMemoryChars is exposed but agent_state still calls build_agent_state_packet.py with --max-memory-chars 24000.
ProviderMaxContextChars is exposed and preset-adjusted but official adapter and Ollama packet still use MaxContextChars.
Output paths are still hardcoded to output/local_ai_runs, output/validation, output/ai_pipeline and output/patch_specs.
Official/Ollama/context-pack basenames are still generated internally and cannot yet be overridden from CLI.
External context/report/artifact files are not yet accepted from CLI.
```

## User requirement for next step

Add external CLI controls for all relevant paths and basenames. The launcher must allow the operator to choose inputs, outputs, reports, contexts and artifact paths at launch time.

Main target:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Do not modify large historical evidence snapshots. Do not convert old long 0-to-10 documents in this step unless explicitly requested.

## Parameters to add

Add these parameters to the launcher:

```powershell
[string]$OutputRoot = "output"
[string]$ValidationOutputDir = ""
[string]$AiPipelineOutputDir = ""
[string]$AiPacketsOutputDir = ""
[string]$PatchSpecOutputDir = ""
[string]$LocalRunsOutputDir = ""
[string]$EvidenceOutputDir = "docs/LOCAL_VALIDATION_EVIDENCE"

[string[]]$ExternalContextFile = @()
[string[]]$ExternalReportFile = @()
[string[]]$ExternalArtifactFile = @()

[string]$OfficialBasename = ""
[string]$OfficialProposalBasename = ""
[string]$OllamaBasename = ""
[string]$OllamaProposalBasename = ""
[string]$MultistepBasename = ""
[string]$MultistepProposalBasename = ""
[string]$ContextPackBasename = ""
[string]$ContextPackEvidenceBasename = ""
```

## Required behavior

After `Set-Location $RepoRoot`, resolve default directories:

```powershell
if ([string]::IsNullOrWhiteSpace($ValidationOutputDir)) { $ValidationOutputDir = Join-Path $OutputRoot "validation" }
if ([string]::IsNullOrWhiteSpace($AiPipelineOutputDir)) { $AiPipelineOutputDir = Join-Path $OutputRoot "ai_pipeline" }
if ([string]::IsNullOrWhiteSpace($AiPacketsOutputDir)) { $AiPacketsOutputDir = Join-Path $OutputRoot "ai_packets" }
if ([string]::IsNullOrWhiteSpace($PatchSpecOutputDir)) { $PatchSpecOutputDir = Join-Path $OutputRoot "patch_specs" }
if ([string]::IsNullOrWhiteSpace($LocalRunsOutputDir)) { $LocalRunsOutputDir = Join-Path $OutputRoot "local_ai_runs" }
```

Normalize path separators to `/` for manifest readability.

Replace hardcoded paths where safe:

```text
output/local_ai_runs       -> $LocalRunsOutputDir
output/validation          -> $ValidationOutputDir
output/ai_pipeline         -> $AiPipelineOutputDir
output/ai_packets          -> $AiPacketsOutputDir
output/patch_specs         -> $PatchSpecOutputDir
docs/LOCAL_VALIDATION_EVIDENCE -> $EvidenceOutputDir
```

Add external context/report files into the run:

```powershell
foreach ($PathValue in @($ExternalContextFile)) {
    $ContextFiles = Add-ExistingContextFile $ContextFiles $PathValue
}

foreach ($PathValue in @($ExternalReportFile)) {
    if (Test-Path -LiteralPath $PathValue -PathType Leaf) {
        $ReportFiles += $PathValue
    }
}
```

External artifacts should be recorded in manifest and optionally passed to evidence builders when the current wrapper supports it. They must not be applied automatically.

## Basename behavior

Default basenames should be generated only if the operator did not pass them:

```powershell
if ([string]::IsNullOrWhiteSpace($OfficialBasename)) { $OfficialBasename = "unified_${ModeName}_$Stamp" }
if ([string]::IsNullOrWhiteSpace($OfficialProposalBasename)) { $OfficialProposalBasename = "unified_${ModeName}_proposals_$Stamp" }

if ([string]::IsNullOrWhiteSpace($OllamaBasename)) { $OllamaBasename = "unified_${ModeName}_ollama_$Stamp" }
if ([string]::IsNullOrWhiteSpace($OllamaProposalBasename)) { $OllamaProposalBasename = "unified_${ModeName}_ollama_proposals_$Stamp" }

if ([string]::IsNullOrWhiteSpace($MultistepBasename)) { $MultistepBasename = "unified_${ModeName}_multistep_$Stamp" }
if ([string]::IsNullOrWhiteSpace($MultistepProposalBasename)) { $MultistepProposalBasename = "unified_${ModeName}_multistep_proposals_$Stamp" }

if ([string]::IsNullOrWhiteSpace($ContextPackBasename)) { $ContextPackBasename = "unified_${ModeName}_context_pack_$Stamp" }
if ([string]::IsNullOrWhiteSpace($ContextPackEvidenceBasename)) { $ContextPackEvidenceBasename = "${ContextPackBasename}_evidence" }
```

## Required wiring replacements

These replacements are mandatory, not optional:

```text
context_pack call:
  "--max-total-chars", "64000" -> "--max-total-chars", "$ContextPackMaxTotalChars"
  "--max-file-chars", "4000" -> "--max-file-chars", "$ContextPackMaxFileChars"

agent_state call:
  "--max-memory-chars", "24000" -> "--max-memory-chars", "$AgentStateMaxMemoryChars"

official adapter call:
  "-MaxContextChars", "$MaxContextChars" -> chosen official/provider context variable, defaulting to $ProviderMaxContextChars or $MaxContextChars.

Ollama packet call:
  "-MaxContextChars", "$MaxContextChars" -> chosen Ollama/provider context variable, defaulting to $ProviderMaxContextChars or $MaxContextChars.

output dirs:
  $RunDir = "output/local_ai_runs/..." -> $LocalRunsOutputDir
  $ValidationDir = "output/validation" -> $ValidationOutputDir
  New-Item output/ai_pipeline -> $AiPipelineOutputDir
  output/patch_specs references -> $PatchSpecOutputDir where used by generated patch-spec phases.
```

## Manifest additions

Add these manifest fields:

```powershell
output_root = $OutputRoot
validation_output_dir = $ValidationOutputDir
ai_pipeline_output_dir = $AiPipelineOutputDir
ai_packets_output_dir = $AiPacketsOutputDir
patch_spec_output_dir = $PatchSpecOutputDir
local_runs_output_dir = $LocalRunsOutputDir
evidence_output_dir = $EvidenceOutputDir

external_context_files = @($ExternalContextFile)
external_report_files = @($ExternalReportFile)
external_artifact_files = @($ExternalArtifactFile)

official_basename = $OfficialBasename
official_proposal_basename = $OfficialProposalBasename
ollama_basename = $OllamaBasename
ollama_proposal_basename = $OllamaProposalBasename
multistep_basename = $MultistepBasename
multistep_proposal_basename = $MultistepProposalBasename
context_pack_basename = $ContextPackBasename
context_pack_evidence_basename = $ContextPackEvidenceBasename
```

## Important constraints

- No triple-quote / heredoc patch style in chat.
- Prefer atomic PowerShell replacements or a repository patch bundle file.
- Do not touch evidence snapshots.
- Do not delete files.
- Do not merge PR.
- Do not apply generated patch specs automatically.
- Keep `.venv/` ignored and untracked.
- Always run parser validation after patch.

## Validation commands

Parser validation:

```powershell
$null = [scriptblock]::Create((Get-Content .\Tools\workflow\run_unified_local_ai_refactor.ps1 -Raw))
```

Search inserted controls:

```powershell
Select-String -Path .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Pattern 'ExternalContextFile|ExternalReportFile|ExternalArtifactFile|OutputRoot|ValidationOutputDir|OfficialBasename|OllamaBasename|MultistepBasename|ContextPackBasename|external_context_files' |
  Select-Object LineNumber, Line
```

Dry-run with external controls:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Full0To10 `
  -RunIntensity quick `
  -OutputRoot output `
  -ValidationOutputDir output/validation `
  -AiPipelineOutputDir output/ai_pipeline `
  -AiPacketsOutputDir output/ai_packets `
  -PatchSpecOutputDir output/patch_specs `
  -LocalRunsOutputDir output/local_ai_runs `
  -EvidenceOutputDir docs/LOCAL_VALIDATION_EVIDENCE `
  -OfficialBasename test_official_20260504 `
  -OfficialProposalBasename test_official_proposals_20260504 `
  -OllamaBasename test_ollama_20260504 `
  -OllamaProposalBasename test_ollama_proposals_20260504 `
  -ContextPackBasename test_context_pack_20260504 `
  -ContextPackEvidenceBasename test_context_pack_evidence_20260504 `
  -ExternalContextFile .\docs\LOCAL_AI_TASKS\docs-md-obsolete-pruning-next-step.md `
  -ExternalReportFile .\output\validation\legacy_0_to_10_references.csv `
  -Model gpt-oss:20b `
  -DryRun `
  -SkipGitSync `
  -NoBranch `
  -AllowDirty
```

Additional wiring validation after patch:

```powershell
Select-String -Path .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -Pattern '64000|4000|24000|output/local_ai_runs|output/validation|output\\ai_pipeline|output/ai_pipeline' |
  Select-Object LineNumber, Line
```

Expected: only acceptable defaults in parameter declarations, not hardcoded subordinate call arguments.

Git checks:

```powershell
git diff --check
git status --short
```

Commit message:

```text
feat(workflow): expose external controls in unified launcher
```

## Known untracked file from previous run

This file may still be present and should not be committed for the launcher PR unless explicitly needed:

```text
docs/LOCAL_VALIDATION_EVIDENCE/unified_agent_state_chunks_context_pack_contract_full_validation_json_md_official_patch_specs_provider_python_context_pack_20260504-142409_evidence.md
```

Recommended cleanup if still untracked:

```powershell
Remove-Item .\docs\LOCAL_VALIDATION_EVIDENCE\unified_agent_state_chunks_context_pack_contract_full_validation_json_md_official_patch_specs_provider_python_context_pack_20260504-142409_evidence.md -Force -ErrorAction SilentlyContinue
```
