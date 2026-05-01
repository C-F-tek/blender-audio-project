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
    [string]$ChunkQuery = "",
    [string[]]$ChunkPathBoost = @(),
    [string]$SelectedChunksBasename = "",
    [int]$MaxSelectedChunks = 20,
    [int]$MaxSelectedChunkChars = 24000,
    [int]$MaxSelectedChunkExcerptChars = 2500,
    [switch]$BuildSelectedChunksEvidence,
    [string]$SelectedChunksEvidenceBasename = "",
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

function Resolve-ExistingPath {
    param([string]$PathValue)
    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return (Resolve-Path $PathValue).Path
    }
    return (Resolve-Path (Join-Path (Get-Location) $PathValue)).Path
}

function Resolve-PlannedPath {
    param([string]$PathValue)
    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return [System.IO.Path]::GetFullPath($PathValue)
    }
    return [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $PathValue))
}

function Get-RepoRelativePath {
    param(
        [string]$Root,
        [string]$PathValue
    )
    $full = [System.IO.Path]::GetFullPath($PathValue)
    $rootFull = [System.IO.Path]::GetFullPath($Root)
    if (-not $rootFull.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
        $rootFull = $rootFull + [System.IO.Path]::DirectorySeparatorChar
    }
    if ($full.StartsWith($rootFull, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $full.Substring($rootFull.Length).Replace("\", "/")
    }
    return $full.Replace("\", "/")
}

function Invoke-CommandChecked {
    param(
        [string]$Label,
        [scriptblock]$Block
    )
    Write-Host ""
    Write-Host "=== $Label ==="
    if ($DryRun) {
        Write-Host "[DRY-RUN] Skipped execution."
        return
    }
    & $Block
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE"
    }
}

function Add-ContextFileIfPresent {
    param(
        [string[]]$Current,
        [string]$PathValue,
        [string]$Root
    )
    if ([string]::IsNullOrWhiteSpace($PathValue)) {
        return $Current
    }
    $full = Resolve-PlannedPath $PathValue
    if (-not (Test-Path -LiteralPath $full -PathType Leaf)) {
        Write-Warning "Context file not found, not adding: $PathValue"
        return $Current
    }
    $rel = Get-RepoRelativePath $Root $full
    if ($Current -notcontains $rel) {
        return @($Current + $rel)
    }
    return $Current
}

function Normalize-ContextFiles {
    param([string[]]$Values)
    $seen = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
    $normalized = @()
    foreach ($value in $Values) {
        $item = [string]$value
        if ([string]::IsNullOrWhiteSpace($item)) {
            continue
        }
        $item = $item.Trim().Replace("\", "/")
        if ($seen.Add($item)) {
            $normalized += $item
        }
    }
    return $normalized
}

function New-SafeName {
    param([string]$Value, [string]$Fallback)
    $safe = [regex]::Replace(($Value.ToLowerInvariant()), "[^a-z0-9._-]+", "_").Trim("._-")
    if ([string]::IsNullOrWhiteSpace($safe)) { return $Fallback }
    return $safe
}

$RepoRootPath = Resolve-ExistingPath $RepoRoot
Set-Location $RepoRootPath

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
if ([string]::IsNullOrWhiteSpace($AgentStateObjective)) {
    $AgentStateObjective = "Run local AI task $Basename with task Markdown, memory, semantic chunks and bounded context."
}
if ([string]::IsNullOrWhiteSpace($ChunkQuery)) {
    $ChunkQuery = $AgentStateObjective
}

$SelectedChunksJson = "output/ai_context_packs/$SelectedChunksBasename.json"
$SelectedChunksMd = "output/ai_context_packs/$SelectedChunksBasename.md"
$SelectedChunksValidationJson = "output/validation/${SelectedChunksBasename}_selected_chunks.json"
$SelectedChunksEvidenceJson = "docs/LOCAL_VALIDATION_EVIDENCE/$SelectedChunksEvidenceBasename.json"
$SelectedChunksEvidenceMd = "docs/LOCAL_VALIDATION_EVIDENCE/$SelectedChunksEvidenceBasename.md"

$ContextFiles = @($PromptRel)
if ($TaskRel -ne "") { $ContextFiles += $TaskRel }

foreach ($extra in $ExtraContextFile) {
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue $extra -Root $RepoRootPath
}
$ContextFiles = Normalize-ContextFiles $ContextFiles

$EnrichmentOutputs = [ordered]@{
    semantic_chunks_manifest = ""
    semantic_chunks_json = ""
    selected_chunks_json = ""
    selected_chunks_markdown = ""
    selected_chunks_validation_json = ""
    selected_chunks_evidence_json = ""
    selected_chunks_evidence_markdown = ""
    context_pack_json = ""
    context_pack_markdown = ""
    context_pack_evidence_json = ""
    agent_state_json = ""
    agent_state_markdown = ""
    agent_state_memory_manifest = ""
    memory_db = $MemoryDb.Replace("\", "/")
}

if ($BuildSemanticChunks) {
    Invoke-CommandChecked -Label "Build semantic code chunks" -Block {
        python .\Tools\npu\build_semantic_code_chunks.py --repo-root .
    }
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue "indexAI/code_chunks/semantic_code_chunks_manifest.json" -Root $RepoRootPath
    $ContextFiles = Normalize-ContextFiles $ContextFiles
    $EnrichmentOutputs.semantic_chunks_manifest = "indexAI/code_chunks/semantic_code_chunks_manifest.json"
    $EnrichmentOutputs.semantic_chunks_json = "indexAI/code_chunks/semantic_code_chunks.json"
}

if ($SelectSemanticChunks) {
    $SelectArgs = @(
        ".\Tools\ai\select_semantic_code_chunks.py",
        "--repo-root", ".",
        "--query", $ChunkQuery,
        "--output", $SelectedChunksJson,
        "--markdown-output", $SelectedChunksMd,
        "--max-chunks", "$MaxSelectedChunks",
        "--max-total-chars", "$MaxSelectedChunkChars",
        "--max-excerpt-chars", "$MaxSelectedChunkExcerptChars"
    )
    foreach ($boost in $ChunkPathBoost) {
        $SelectArgs += @("--path-boost", $boost)
    }
    Invoke-CommandChecked -Label "Select focused semantic code chunks" -Block {
        python @SelectArgs
    }
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue $SelectedChunksMd -Root $RepoRootPath
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue $SelectedChunksJson -Root $RepoRootPath
    $ContextFiles = Normalize-ContextFiles $ContextFiles
    $EnrichmentOutputs.selected_chunks_json = $SelectedChunksJson
    $EnrichmentOutputs.selected_chunks_markdown = $SelectedChunksMd
}
elseif ($BuildSelectedChunksEvidence) {
    throw "-BuildSelectedChunksEvidence requires -SelectSemanticChunks so the selected-chunks bundle exists."
}

if ($BuildSelectedChunksEvidence) {
    Invoke-CommandChecked -Label "Validate selected semantic chunks and build compact evidence" -Block {
        python .\Tools\validation\check_selected_semantic_chunks.py `
            --repo-root . `
            --bundle $SelectedChunksJson `
            --output $SelectedChunksValidationJson `
            --evidence-output $SelectedChunksEvidenceJson `
            --markdown-output $SelectedChunksEvidenceMd `
            --max-total-chars $MaxSelectedChunkChars
    }
    $EnrichmentOutputs.selected_chunks_validation_json = $SelectedChunksValidationJson
    $EnrichmentOutputs.selected_chunks_evidence_json = $SelectedChunksEvidenceJson
    $EnrichmentOutputs.selected_chunks_evidence_markdown = $SelectedChunksEvidenceMd
}

if ($BuildContextPack) {
    Invoke-CommandChecked -Label "Build bounded AI context pack" -Block {
        python .\Tools\ai\build_ai_context_pack.py `
            --repo-root . `
            --profile $ContextPackProfile `
            --basename $ContextPackBasename `
            --evidence-basename $ContextPackEvidenceBasename `
            --max-total-chars $ContextPackMaxTotalChars `
            --max-file-chars $ContextPackMaxFileChars
    }
    $ContextPackJson = "output/ai_context_packs/$ContextPackBasename.json"
    $ContextPackMd = "output/ai_context_packs/$ContextPackBasename.md"
    $ContextPackEvidenceJson = "docs/LOCAL_VALIDATION_EVIDENCE/$ContextPackEvidenceBasename.json"
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue $ContextPackMd -Root $RepoRootPath
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue $ContextPackJson -Root $RepoRootPath
    $ContextFiles = Normalize-ContextFiles $ContextFiles
    $EnrichmentOutputs.context_pack_json = $ContextPackJson
    $EnrichmentOutputs.context_pack_markdown = $ContextPackMd
    $EnrichmentOutputs.context_pack_evidence_json = $ContextPackEvidenceJson
}

if ($BuildAgentStatePacket) {
    $ContextFiles = Normalize-ContextFiles $ContextFiles
    $AgentArgs = @(
        ".\Tools\ai\build_agent_state_packet.py",
        "--repo-root", ".",
        "--objective", $AgentStateObjective,
        "--output-dir", $AgentStateRel,
        "--packet-name", $AgentStateBasename,
        "--max-memory-chars", "$AgentStateMaxMemoryChars",
        "--memory-db", $MemoryDb
    )
    if ($SaveInputsToMemoryDb) { $AgentArgs += "--save-inputs-to-memory-db" }
    $AgentArgs += @("--memory-note", "Local AI enrichment run. Preserve report-only defaults, explicit providers, NPU guardrail role and no patch apply.")
    foreach ($context in $ContextFiles) {
        $AgentArgs += @("--include-file", $context)
    }
    Invoke-CommandChecked -Label "Build agent state packet with SQLite memory" -Block {
        python @AgentArgs
    }
    $AgentStateJson = "$AgentStateRel/$AgentStateBasename.json"
    $AgentStateMd = "$AgentStateRel/$AgentStateBasename.md"
    $AgentStateManifest = "$AgentStateRel/${AgentStateBasename}_memory_manifest.json"
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue $AgentStateMd -Root $RepoRootPath
    $ContextFiles = Add-ContextFileIfPresent -Current $ContextFiles -PathValue $AgentStateJson -Root $RepoRootPath
    $ContextFiles = Normalize-ContextFiles $ContextFiles
    $EnrichmentOutputs.agent_state_json = $AgentStateJson
    $EnrichmentOutputs.agent_state_markdown = $AgentStateMd
    $EnrichmentOutputs.agent_state_memory_manifest = $AgentStateManifest
}

$ContextFiles = Normalize-ContextFiles $ContextFiles

$ReportFiles = @(
    "output/validation/docs_links.json",
    "output/validation/execution_plan_status.json",
    "output/validation/validation_report_contract.json",
    "output/validation/python_syntax.json"
)
if ($BuildSelectedChunksEvidence) {
    $ReportFiles += $SelectedChunksValidationJson
}

Write-Host "=== Local AI task via project pipeline ==="
Write-Host "Repo: $RepoRootPath"
Write-Host "Prompt: $PromptRel"
Write-Host "Task: $TaskRel"
Write-Host "Pipeline output: $PipelineRel"
Write-Host "Profile: $Profile"
Write-Host "Context files: $($ContextFiles -join ', ')"
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

if ($RunMultistepProviderWorkflow) {
    $MultistepArgs = @(
        "-NoProfile", "-ExecutionPolicy", "Bypass",
        "-File", ".\Tools\workflow\run_parallel_ai_provider_multistep.ps1",
        "-RepoRoot", ".",
        "-Profile", $Profile,
        "-OutputDir", $PipelineRel,
        "-Basename", $MultistepBasename,
        "-ProposalBasename", $MultistepProposalBasename,
        "-EvidenceBasename", $MultistepEvidenceBasename,
        "-ContextFile", ($ContextFiles -join ","),
        "-MaxContextChars", "$MaxContextChars"
    )
    if ($RunOllamaProbe) { $MultistepArgs += "-RunOllamaProbe" }
    if ($RunNpuProbe) { $MultistepArgs += "-RunNpuProbe" }
    if ($RunNpuDecodeSmoke) { $MultistepArgs += "-RunNpuDecodeSmoke" }
    if ($UsePrimaryAdvisoryProvider) { $MultistepArgs += "-UsePrimaryAdvisoryProvider" }
    if ($Model -ne "") { $MultistepArgs += @("-Model", $Model) }

    Invoke-CommandChecked -Label "Run explicit multistep provider workflow" -Block { powershell.exe @MultistepArgs }
}

$PacketArgs = @(
    "-NoProfile", "-ExecutionPolicy", "Bypass",
    "-File", ".\Tools\workflow\run_post_validation_ai_packet.ps1",
    "-RepoRoot", ".",
    "-Profile", $Profile,
    "-OutputDir", $PipelineRel,
    "-Basename", $Basename,
    "-ProposalBasename", $ProposalBasename,
    "-ContextFile", ($ContextFiles -join ","),
    "-ReportFile", ($ReportFiles -join ","),
    "-MaxContextChars", "$MaxContextChars"
)
if ($UsePrimaryAdvisoryProvider) { $PacketArgs += "-UsePrimaryAdvisoryProvider" }
if ($Model -ne "") { $PacketArgs += @("-Model", $Model) }

Invoke-CommandChecked -Label "Build advisory packet and repository proposals" -Block { powershell.exe @PacketArgs }

$ProposalPath = Join-Path $PipelineDir "$ProposalBasename.json"
$ProposalRel = Get-RepoRelativePath $RepoRootPath $ProposalPath
$ProposalValidationOutput = "output/validation/${Basename}_repository_change_proposals_contract.json"

if (Test-Path -LiteralPath $ProposalPath -PathType Leaf) {
    Invoke-CommandChecked -Label "Validate repository change proposals" -Block {
        python .\Tools\validation\check_repository_change_proposals.py --repo-root . --proposal $ProposalRel --output $ProposalValidationOutput
    }
}
else {
    Write-Warning "Proposal file was not produced: $ProposalRel"
}

if ($GeneratePatchSpecs -and (Test-Path -LiteralPath $ProposalPath -PathType Leaf)) {
    $PatchBasename = "${Basename}_patch_specs"
    $PatchManifest = "output/patch_specs/${PatchBasename}_manifest.json"
    Invoke-CommandChecked -Label "Build draft patch specs from proposals" -Block {
        python .\Tools\ai\build_patch_specs_from_proposals.py --repo-root . --proposal $ProposalRel --output-dir output\patch_specs --basename $PatchBasename
    }
    Invoke-CommandChecked -Label "Validate draft patch specs" -Block {
        python .\Tools\validation\check_patch_spec_drafts.py --repo-root . --manifest $PatchManifest --output "output/validation/${Basename}_patch_spec_drafts.json"
    }
}

if ($BuildEvidence) {
    if ([string]::IsNullOrWhiteSpace($EvidenceBasename)) { $EvidenceBasename = "${Basename}_evidence" }
    Invoke-CommandChecked -Label "Build compact GitHub evidence bundle" -Block {
        python .\Tools\ai\build_github_evidence_bundle.py --repo-root . --basename $EvidenceBasename
    }
}

$ManifestPath = Join-Path $PipelineDir "${Basename}_adapter_manifest.json"
$Manifest = [ordered]@{
    schema_version = 1
    kind = "local_ai_task_pipeline_adapter_manifest"
    generated_at = (Get-Date -Format o)
    repo_root = $RepoRootPath
    prompt_file = $PromptRel
    task_file = $TaskRel
    pipeline_output_dir = $PipelineRel
    profile = $Profile
    basename = $Basename
    proposal_basename = $ProposalBasename
    context_files = $ContextFiles
    context_file_count = $ContextFiles.Count
    enrichment_requested = [ordered]@{
        build_semantic_chunks = [bool]$BuildSemanticChunks
        select_semantic_chunks = [bool]$SelectSemanticChunks
        build_selected_chunks_evidence = [bool]$BuildSelectedChunksEvidence
        chunk_query = $ChunkQuery
        max_selected_chunks = $MaxSelectedChunks
        max_selected_chunk_chars = $MaxSelectedChunkChars
        selected_chunks_evidence_basename = $SelectedChunksEvidenceBasename
        build_context_pack = [bool]$BuildContextPack
        context_pack_profile = $ContextPackProfile
        build_agent_state_packet = [bool]$BuildAgentStatePacket
        memory_db = $MemoryDb.Replace("\", "/")
        save_inputs_to_memory_db = [bool]$SaveInputsToMemoryDb
        extra_context_file_count = $ExtraContextFile.Count
    }
    enrichment_outputs = $EnrichmentOutputs
    multistep_provider_workflow_requested = [bool]$RunMultistepProviderWorkflow
    multistep_basename = $MultistepBasename
    multistep_proposal_basename = $MultistepProposalBasename
    multistep_evidence_basename = $MultistepEvidenceBasename
    run_ollama_probe = [bool]$RunOllamaProbe
    run_npu_probe = [bool]$RunNpuProbe
    run_npu_decode_smoke = [bool]$RunNpuDecodeSmoke
    provider_execution_requested = [bool]($UsePrimaryAdvisoryProvider -or $RunOllamaProbe -or $RunNpuProbe -or $RunNpuDecodeSmoke)
    patch_application_performed = $false
    provider_execution_performed_by_adapter = $false
    build_evidence_requested = [bool]$BuildEvidence
    generate_patch_specs_requested = [bool]$GeneratePatchSpecs
    outputs = [ordered]@{
        packet_json = "$PipelineRel/$Basename.json"
        packet_markdown = "$PipelineRel/$Basename.md"
        proposals_json = "$PipelineRel/$ProposalBasename.json"
        proposals_markdown = "$PipelineRel/$ProposalBasename.md"
        proposal_validation = $ProposalValidationOutput
        selected_chunks_validation_json = $SelectedChunksValidationJson
        selected_chunks_evidence_json = $SelectedChunksEvidenceJson
        selected_chunks_evidence_markdown = $SelectedChunksEvidenceMd
        multistep_packet_json = "$PipelineRel/$MultistepBasename.json"
        multistep_packet_markdown = "$PipelineRel/$MultistepBasename.md"
        multistep_proposals_json = "$PipelineRel/$MultistepProposalBasename.json"
        multistep_proposals_markdown = "$PipelineRel/$MultistepProposalBasename.md"
        multistep_evidence_json = "docs/LOCAL_VALIDATION_EVIDENCE/$MultistepEvidenceBasename.json"
        evidence_json = "docs/LOCAL_VALIDATION_EVIDENCE/$EvidenceBasename.json"
    }
    warnings = @()
    errors = @()
}
($Manifest | ConvertTo-Json -Depth 10) | Set-Content -LiteralPath $ManifestPath -Encoding UTF8

Write-Host ""
Write-Host "[OK] Local pipeline adapter complete" -ForegroundColor Green
Write-Host "[OK] Manifest: $(Get-RepoRelativePath $RepoRootPath $ManifestPath)"
Write-Host "[OK] Packet:   $PipelineRel/$Basename.md"
Write-Host "[OK] Proposal: $PipelineRel/$ProposalBasename.md"
Write-Host "[OK] Context files: $($ContextFiles.Count)"
Write-Host "[OK] Multistep requested: $RunMultistepProviderWorkflow"
Write-Host "[OK] Provider execution requested: $($UsePrimaryAdvisoryProvider -or $RunOllamaProbe -or $RunNpuProbe -or $RunNpuDecodeSmoke)"
Write-Host "[OK] Patch application performed: False"
