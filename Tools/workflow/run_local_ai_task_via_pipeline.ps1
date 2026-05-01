<#
.SYNOPSIS
  Run a local Markdown AI task through the project-owned report-only AI pipeline.

.DESCRIPTION
  This adapter is the preferred project-owned runner target for
  Tools/workflow/run_local_ai_markdown_task.ps1.

  It consumes the generated local_ai_prompt.md plus the task Markdown file,
  then invokes the repository's report-only/proposal-only AI packet pipeline.

  Default mode does not execute providers, does not apply patches, does not run
  Blender, does not run FFmpeg and does not edit source files.

  Provider execution remains explicit through -UsePrimaryAdvisoryProvider and
  -RunMultistepProviderWorkflow. NPU remains probe / guardrail / decode
  diagnostic. Ollama/GPU remains primary advisory behind the quality gate.

.EXAMPLE
  .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 `
    -PromptFile .\output\local_ai_runs\run\local_ai_prompt.md `
    -TaskFile .\docs\LOCAL_AI_TASKS\issue-62-hybrid-master-ai-local-pipeline.md `
    -RunDir .\output\local_ai_runs\run

.EXAMPLE
  .\Tools\workflow\run_local_ai_task_via_pipeline.ps1 `
    -PromptFile .\output\local_ai_runs\run\local_ai_prompt.md `
    -TaskFile .\docs\LOCAL_AI_TASKS\issue-62-hybrid-master-ai-local-pipeline.md `
    -RunDir .\output\local_ai_runs\run `
    -RunMultistepProviderWorkflow `
    -RunOllamaProbe `
    -RunNpuProbe `
    -RunNpuDecodeSmoke `
    -UsePrimaryAdvisoryProvider `
    -BuildEvidence
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
New-Item -ItemType Directory -Force -Path $PipelineDir | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $RepoRootPath "output/validation") | Out-Null

$PromptRel = Get-RepoRelativePath $RepoRootPath $PromptPath
$PipelineRel = Get-RepoRelativePath $RepoRootPath $PipelineDir
$TaskRel = ""
if ($TaskPath -ne "") {
    $TaskRel = Get-RepoRelativePath $RepoRootPath $TaskPath
}

if ([string]::IsNullOrWhiteSpace($MultistepBasename)) {
    $MultistepBasename = "${Basename}_multistep"
}
if ([string]::IsNullOrWhiteSpace($MultistepProposalBasename)) {
    $MultistepProposalBasename = "${Basename}_multistep_proposals"
}
if ([string]::IsNullOrWhiteSpace($MultistepEvidenceBasename)) {
    $MultistepEvidenceBasename = "${Basename}_multistep_evidence"
}

$ContextFiles = @($PromptRel)
if ($TaskRel -ne "") {
    $ContextFiles += $TaskRel
}

$ReportFiles = @(
    "output/validation/docs_links.json",
    "output/validation/execution_plan_status.json",
    "output/validation/validation_report_contract.json",
    "output/validation/python_syntax.json"
)

Write-Host "=== Local AI task via project pipeline ==="
Write-Host "Repo: $RepoRootPath"
Write-Host "Prompt: $PromptRel"
Write-Host "Task: $TaskRel"
Write-Host "Pipeline output: $PipelineRel"
Write-Host "Profile: $Profile"
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
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
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
    if ($RunOllamaProbe) {
        $MultistepArgs += "-RunOllamaProbe"
    }
    if ($RunNpuProbe) {
        $MultistepArgs += "-RunNpuProbe"
    }
    if ($RunNpuDecodeSmoke) {
        $MultistepArgs += "-RunNpuDecodeSmoke"
    }
    if ($UsePrimaryAdvisoryProvider) {
        $MultistepArgs += "-UsePrimaryAdvisoryProvider"
    }
    if ($Model -ne "") {
        $MultistepArgs += @("-Model", $Model)
    }

    Invoke-CommandChecked -Label "Run explicit multistep provider workflow" -Block {
        powershell.exe @MultistepArgs
    }
}

$PacketArgs = @(
    "-NoProfile",
    "-ExecutionPolicy", "Bypass",
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
if ($UsePrimaryAdvisoryProvider) {
    $PacketArgs += "-UsePrimaryAdvisoryProvider"
}
if ($Model -ne "") {
    $PacketArgs += @("-Model", $Model)
}

Invoke-CommandChecked -Label "Build advisory packet and repository proposals" -Block {
    powershell.exe @PacketArgs
}

$ProposalPath = Join-Path $PipelineDir "$ProposalBasename.json"
$ProposalRel = Get-RepoRelativePath $RepoRootPath $ProposalPath
$ProposalValidationOutput = "output/validation/${Basename}_repository_change_proposals_contract.json"

if (Test-Path -LiteralPath $ProposalPath -PathType Leaf) {
    Invoke-CommandChecked -Label "Validate repository change proposals" -Block {
        python .\Tools\validation\check_repository_change_proposals.py `
            --repo-root . `
            --proposal $ProposalRel `
            --output $ProposalValidationOutput
    }
}
else {
    Write-Warning "Proposal file was not produced: $ProposalRel"
}

if ($GeneratePatchSpecs -and (Test-Path -LiteralPath $ProposalPath -PathType Leaf)) {
    $PatchBasename = "${Basename}_patch_specs"
    $PatchManifest = "output/patch_specs/${PatchBasename}_manifest.json"
    Invoke-CommandChecked -Label "Build draft patch specs from proposals" -Block {
        python .\Tools\ai\build_patch_specs_from_proposals.py `
            --repo-root . `
            --proposal $ProposalRel `
            --output-dir output\patch_specs `
            --basename $PatchBasename
    }
    Invoke-CommandChecked -Label "Validate draft patch specs" -Block {
        python .\Tools\validation\check_patch_spec_drafts.py `
            --repo-root . `
            --manifest $PatchManifest `
            --output "output/validation/${Basename}_patch_spec_drafts.json"
    }
}

if ($BuildEvidence) {
    if ([string]::IsNullOrWhiteSpace($EvidenceBasename)) {
        $EvidenceBasename = "${Basename}_evidence"
    }
    Invoke-CommandChecked -Label "Build compact GitHub evidence bundle" -Block {
        python .\Tools\ai\build_github_evidence_bundle.py `
            --repo-root . `
            --basename $EvidenceBasename
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
($Manifest | ConvertTo-Json -Depth 8) | Set-Content -LiteralPath $ManifestPath -Encoding UTF8

Write-Host ""
Write-Host "[OK] Local pipeline adapter complete" -ForegroundColor Green
Write-Host "[OK] Manifest: $(Get-RepoRelativePath $RepoRootPath $ManifestPath)"
Write-Host "[OK] Packet:   $PipelineRel/$Basename.md"
Write-Host "[OK] Proposal: $PipelineRel/$ProposalBasename.md"
Write-Host "[OK] Multistep requested: $RunMultistepProviderWorkflow"
Write-Host "[OK] Provider execution requested: $($UsePrimaryAdvisoryProvider -or $RunOllamaProbe -or $RunNpuProbe -or $RunNpuDecodeSmoke)"
Write-Host "[OK] Patch application performed: False"
