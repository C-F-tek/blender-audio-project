<#
.SYNOPSIS
  Run a local Markdown AI task through the project-owned report-only AI pipeline.

.DESCRIPTION
  Preferred runner target for Tools/workflow/run_local_ai_markdown_task.ps1.

  It consumes local_ai_prompt.md plus the task Markdown file, optionally builds
  enrichment artifacts, and invokes report-only/proposal-only AI packet tools.

  Default mode does not execute providers, does not apply patches, does not run
  Blender, does not run FFmpeg and does not edit source files.

  Provider execution remains explicit through -UsePrimaryAdvisoryProvider and
  -RunMultistepProviderWorkflow. NPU remains probe / guardrail / decode
  diagnostic. Ollama/GPU remains primary advisory behind the quality gate.

  -FullContextGoldenPath is a safe preset. It expands to the standard local
  context enrichment options, selected-chunks evidence, context pack, agent state
  and enrichment plan. It does not enable provider execution, probes, multistep
  provider workflow, patch-spec generation or patch application by itself.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$PromptFile,

    [string]$TaskFile = "",
    [string]$RunDir = "",
    [string]$RepoRoot = ".",

    [ValidateSet("core", "npu", "docs")]
    [string]$Profile = "docs",

    [switch]$FullContextGoldenPath,

    [string]$Basename = "local_ai_task_pipeline",
    [string]$ProposalBasename = "local_ai_task_pipeline_proposals",
    [string]$EvidenceBasename = "",
    [string]$MultistepBasename = "",
    [string]$MultistepProposalBasename = "",
    [string]$MultistepEvidenceBasename = "",
    [string]$Model = "",
    [int]$MaxContextChars = 12000,

    [string[]]$ExtraContextFile = @(),
    [switch]$BuildSemanticChunks,
    [switch]$SelectSemanticChunks,
    [switch]$BuildSelectedChunksEvidence,
    [switch]$BuildEnrichmentPlan,
    [string]$EnrichmentPlanBasename = "",
    [string]$ChunkQuery = "",
    [string[]]$ChunkPathBoost = @(),
    [string]$SelectedChunksBasename = "",
    [string]$SelectedChunksEvidenceBasename = "",
    [int]$MaxSelectedChunks = 20,
    [int]$MaxSelectedChunkChars = 24000,
    [int]$MaxSelectedChunkExcerptChars = 2500,
    [switch]$BuildAgentStatePacket,
    [string]$MemoryDb = "indexAI/agent_memory/agent_memory.sqlite",
    [switch]$SaveInputsToMemoryDb,
    [string]$AgentStateObjective = "",
    [string]$AgentStateBasename = "",
    [int]$AgentStateMaxMemoryChars = 24000,
    [switch]$BuildContextPack,
    [string]$ContextPackProfile = "core_ai_backend",
    [string]$ContextPackBasename = "",
    [string]$ContextPackEvidenceBasename = "",
    [int]$ContextPackMaxTotalChars = 64000,
    [int]$ContextPackMaxFileChars = 4000,

    [switch]$UsePrimaryAdvisoryProvider,
    [switch]$RunMultistepProviderWorkflow,
    [switch]$RunOllamaProbe,
    [switch]$RunNpuProbe,
    [switch]$RunNpuDecodeSmoke,
    [switch]$BuildEvidence,
    [switch]$GeneratePatchSpecs,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$AdapterModuleDir = Join-Path $PSScriptRoot "run_local_ai_task_via_pipeline"
. (Join-Path $PSScriptRoot "python_env.ps1")
. (Join-Path $AdapterModuleDir "paths.ps1")
. (Join-Path $AdapterModuleDir "context.ps1")
. (Join-Path $AdapterModuleDir "validation.ps1")

$RepoRootPath = Resolve-ExistingPath $RepoRoot
Set-Location $RepoRootPath
$PipelinePythonExe = Use-WorkflowPython -RepoRoot $RepoRootPath
$env:IA_CARMINE_PYTHON = $PipelinePythonExe
$env:PYTHONPATH = [string]$RepoRootPath
if (Test-Path -LiteralPath $PipelinePythonExe -PathType Leaf) {
    $env:PATH = (Split-Path -Parent $PipelinePythonExe) + [System.IO.Path]::PathSeparator + $env:PATH
}

if ($FullContextGoldenPath) {
    $Profile = "npu"
    $BuildSemanticChunks = $true
    $SelectSemanticChunks = $true
    $BuildSelectedChunksEvidence = $true
    $BuildContextPack = $true
    $BuildAgentStatePacket = $true
    $BuildEnrichmentPlan = $true
    $SaveInputsToMemoryDb = $true

    if ($Basename -eq "local_ai_task_pipeline") { $Basename = "full_context_golden_local_ai_context" }
    if ($ProposalBasename -eq "local_ai_task_pipeline_proposals") { $ProposalBasename = "full_context_golden_local_ai_context_proposals" }
    if ([string]::IsNullOrWhiteSpace($SelectedChunksBasename)) { $SelectedChunksBasename = "full_context_golden_selected_chunks" }
    if ([string]::IsNullOrWhiteSpace($SelectedChunksEvidenceBasename)) { $SelectedChunksEvidenceBasename = "full_context_golden_selected_chunks_evidence" }
    if ([string]::IsNullOrWhiteSpace($ContextPackBasename)) { $ContextPackBasename = "full_context_golden_core_ai_backend" }
    if ([string]::IsNullOrWhiteSpace($ContextPackEvidenceBasename)) { $ContextPackEvidenceBasename = "full_context_golden_core_ai_backend_context_pack_evidence" }
    if ([string]::IsNullOrWhiteSpace($AgentStateBasename)) { $AgentStateBasename = "full_context_golden_agent_state" }
    if ([string]::IsNullOrWhiteSpace($EnrichmentPlanBasename)) { $EnrichmentPlanBasename = "full_context_golden_enrichment_plan" }
    if ([string]::IsNullOrWhiteSpace($ChunkQuery)) {
        $ChunkQuery = "workflow adapter local ai full context enrichment selected chunks sqlite memory provider multistep proposals validators npu knowledge broker context oracle retrieval ranking"
    }
    if ($ChunkPathBoost.Count -eq 0) {
        $ChunkPathBoost = @("Tools/workflow", "Tools/ai", "Tools/validation", "Tools/npu")
    }
    if ($MaxSelectedChunks -eq 20) { $MaxSelectedChunks = 24 }
    if ($MaxSelectedChunkChars -eq 24000) { $MaxSelectedChunkChars = 32000 }
    if ([string]::IsNullOrWhiteSpace($AgentStateObjective)) {
        $AgentStateObjective = "Run full-context local AI/NPU golden path and plan controlled complexity escalation while preserving Ollama/GPU as primary advisory and NPU as knowledge broker."
    }
}

if ($BuildSelectedChunksEvidence -and -not $SelectSemanticChunks) {
    throw "-BuildSelectedChunksEvidence requires -SelectSemanticChunks"
}

$PromptPath = Resolve-ExistingPath $PromptFile
$TaskPath = ""
if (-not [string]::IsNullOrWhiteSpace($TaskFile)) {
    $TaskPath = Resolve-ExistingPath $TaskFile
}

if ([string]::IsNullOrWhiteSpace($RunDir)) {
    $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $RunDir = "output/local_ai_runs/${stamp}_pipeline_adapter"
}
$RunDirPath = Resolve-PlannedPath $RunDir
$PipelineDir = Join-Path $RunDirPath "pipeline"
$AgentStateDir = Join-Path $PipelineDir "agent_state"
New-Item -ItemType Directory -Force -Path $PipelineDir | Out-Null
New-Item -ItemType Directory -Force -Path $AgentStateDir | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $RepoRootPath "output/validation") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $RepoRootPath "output/ai_pipeline") | Out-Null

$PromptRel = Get-RepoRelativePath $RepoRootPath $PromptPath
$PipelineRel = Get-RepoRelativePath $RepoRootPath $PipelineDir
$AgentStateRel = Get-RepoRelativePath $RepoRootPath $AgentStateDir
$TaskRel = ""
if ($TaskPath -ne "") {
    $TaskRel = Get-RepoRelativePath $RepoRootPath $TaskPath
}

if ([string]::IsNullOrWhiteSpace($MultistepBasename)) { $MultistepBasename = "${Basename}_multistep" }
if ([string]::IsNullOrWhiteSpace($MultistepProposalBasename)) { $MultistepProposalBasename = "${Basename}_multistep_proposals" }
if ([string]::IsNullOrWhiteSpace($MultistepEvidenceBasename)) { $MultistepEvidenceBasename = "${Basename}_multistep_evidence" }
if ([string]::IsNullOrWhiteSpace($ContextPackBasename)) { $ContextPackBasename = "${Basename}_context_pack" }
if ([string]::IsNullOrWhiteSpace($ContextPackEvidenceBasename)) { $ContextPackEvidenceBasename = "${Basename}_context_pack_evidence" }
if ([string]::IsNullOrWhiteSpace($SelectedChunksBasename)) { $SelectedChunksBasename = "${Basename}_selected_chunks" }
if ([string]::IsNullOrWhiteSpace($SelectedChunksEvidenceBasename)) { $SelectedChunksEvidenceBasename = "${SelectedChunksBasename}_evidence" }
if ([string]::IsNullOrWhiteSpace($AgentStateBasename)) { $AgentStateBasename = New-SafeName $Basename "local_ai_agent_state" }
if ([string]::IsNullOrWhiteSpace($EnrichmentPlanBasename)) { $EnrichmentPlanBasename = "${Basename}_enrichment_plan" }
if ([string]::IsNullOrWhiteSpace($AgentStateObjective)) {
    $AgentStateObjective = "Run local AI task $Basename with task Markdown, memory, semantic chunks and bounded context."
}
if ([string]::IsNullOrWhiteSpace($ChunkQuery)) {
    $ChunkQuery = $AgentStateObjective
}

. (Join-Path $AdapterModuleDir "enrichment.ps1")

$ReportFiles = @(
    "output/validation/docs_links.json",
    "output/validation/execution_plan_status.json",
    "output/validation/validation_report_contract.json",
    "output/validation/python_syntax.json"
)

Write-Host "=== Local AI task via project pipeline ==="
Write-Host "Repo: $RepoRootPath"
Write-Host "Python: $PipelinePythonExe"
Write-Host "Prompt: $PromptRel"
Write-Host "Task: $TaskRel"
Write-Host "Pipeline output: $PipelineRel"
Write-Host "Profile: $Profile"
Write-Host "Full context golden path preset: $FullContextGoldenPath"
Write-Host "Context files: $($ContextFiles -join ', ')"
Write-Host "Build enrichment plan: $BuildEnrichmentPlan"
Write-Host "Build semantic chunks: $BuildSemanticChunks"
Write-Host "Select semantic chunks: $SelectSemanticChunks"
Write-Host "Build selected chunks evidence: $BuildSelectedChunksEvidence"
Write-Host "Build context pack: $BuildContextPack"
Write-Host "Build agent state packet: $BuildAgentStatePacket"
Write-Host "Use primary advisory provider: $UsePrimaryAdvisoryProvider"
Write-Host "Run multistep provider workflow: $RunMultistepProviderWorkflow"
Write-Host "Run Ollama probe: $RunOllamaProbe"
Write-Host "Run NPU probe: $RunNpuProbe"
Write-Host "Run NPU decode smoke: $RunNpuDecodeSmoke"
Write-Host "Build evidence: $BuildEvidence"
Write-Host "Generate patch specs: $GeneratePatchSpecs"
Write-Host "Dry run: $DryRun"

$ValidationState = Invoke-LocalAiTaskPipelineValidation `
    -RunMultistepProviderWorkflow ([bool]$RunMultistepProviderWorkflow) `
    -RunOllamaProbe ([bool]$RunOllamaProbe) `
    -RunNpuProbe ([bool]$RunNpuProbe) `
    -RunNpuDecodeSmoke ([bool]$RunNpuDecodeSmoke) `
    -UsePrimaryAdvisoryProvider ([bool]$UsePrimaryAdvisoryProvider) `
    -GeneratePatchSpecs ([bool]$GeneratePatchSpecs) `
    -Model $Model `
    -Profile $Profile `
    -PipelineRel $PipelineRel `
    -PipelineDir $PipelineDir `
    -Basename $Basename `
    -ProposalBasename $ProposalBasename `
    -MultistepBasename $MultistepBasename `
    -MultistepProposalBasename $MultistepProposalBasename `
    -MultistepEvidenceBasename $MultistepEvidenceBasename `
    -ContextFiles $ContextFiles `
    -ReportFiles $ReportFiles `
    -MaxContextChars "$MaxContextChars" `
    -RepoRootPath $RepoRootPath `
    -PythonExe $PipelinePythonExe

$ProposalPath = $ValidationState.proposal_path
$ProposalRel = $ValidationState.proposal_rel
$ProposalValidationOutput = $ValidationState.proposal_validation_output
$PatchManifest = $ValidationState.patch_manifest
$PatchManifestMd = $ValidationState.patch_manifest_markdown

$EvidenceJson = ""
$EvidenceMd = ""
$EvidenceValidationOutput = ""
if ($BuildEvidence) {
    if ([string]::IsNullOrWhiteSpace($EvidenceBasename)) { $EvidenceBasename = "${Basename}_evidence" }
    $EvidenceJson = "docs/LOCAL_VALIDATION_EVIDENCE/$EvidenceBasename.json"
    $EvidenceMd = "docs/LOCAL_VALIDATION_EVIDENCE/$EvidenceBasename.md"
    $EvidenceValidationOutput = "output/validation/${EvidenceBasename}_validation.json"
}
$TelemetryJson = "$PipelineRel/${Basename}_telemetry.json"
$TelemetryMd = "$PipelineRel/${Basename}_telemetry.md"

. (Join-Path $AdapterModuleDir "manifest.ps1")
. (Join-Path $AdapterModuleDir "telemetry.ps1")
. (Join-Path $AdapterModuleDir "evidence.ps1")

Write-Host ""
Write-Host "[OK] Local pipeline adapter complete" -ForegroundColor Green
Write-Host "[OK] Manifest: $(Get-RepoRelativePath $RepoRootPath $ManifestPath)"
Write-Host "[OK] Telemetry: $TelemetryMd"
Write-Host "[OK] Packet:   $PipelineRel/$Basename.md"
Write-Host "[OK] Proposal: $PipelineRel/$ProposalBasename.md"
Write-Host "[OK] Context files: $(@(As-Array $ContextFiles).Count)"
Write-Host "[OK] Full context golden path preset: $FullContextGoldenPath"
Write-Host "[OK] Multistep requested: $RunMultistepProviderWorkflow"
Write-Host "[OK] Provider execution requested: $($UsePrimaryAdvisoryProvider -or $RunOllamaProbe -or $RunNpuProbe -or $RunNpuDecodeSmoke)"
Write-Host "[OK] Patch application performed: False"
