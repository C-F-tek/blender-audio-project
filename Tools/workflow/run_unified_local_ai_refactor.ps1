<#
.SYNOPSIS
  Unified local-AI launcher for refactor, documentation cleanup, inventories, validation, smoke tests and advisory providers.

.DESCRIPTION
  One independent entrypoint with one task Markdown input. The operator chooses modes.

  Logical order when multiple modes are selected:
    baseline -> smoke -> validation -> md -> json -> python -> official -> provider -> patch_specs -> full_validation -> final_contract

  The script is report/proposal-only. It does not apply patches, run Blender, run FFmpeg, commit or push.
#>
[CmdletBinding()]
param(
    [ValidateSet("md", "json", "python", "official", "provider", "patch_specs", "smoke", "validation", "contract", "full_validation", "all")]
    [string[]]$Mode = @("all"),

    [string]$TaskFile = ".\docs\LOCAL_AI_TASKS\docs-md-obsolete-pruning-next-step.md",
    [string]$TaskBranch = "",
    [string]$Stamp = "",
    [ValidateSet("core", "npu", "docs")]
    [string]$Profile = "docs",
    [string]$Model = "gpt-oss:20b",
    [int]$MaxContextChars = 12000,

    [switch]$SkipGitSync,
    [switch]$NoBranch,
    [switch]$AllowDirty,
    [switch]$DryRun,

    [switch]$UseOllamaAdvisory,
    [switch]$UsePrimaryAdvisoryProvider,
    [switch]$RunMultistepProviderWorkflow,
    [switch]$RunOllamaProbe,
    [switch]$RunNpuProbe,
    [switch]$RunNpuDecodeSmoke,
    [switch]$BuildEvidence,
    [switch]$GeneratePatchSpecs,
    [switch]$FullContextGoldenPath,
    [switch]$ContinueOnValidationError,
    [int]$MatrixWorkers = 12,
    [int]$RepeatCases = 2
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-Git {
    param([string[]]$GitArgs)
    Write-Host "[git] git $($GitArgs -join ' ')"
    if ($DryRun) { return }
    & git @GitArgs
    if ($LASTEXITCODE -ne 0) { throw "git command failed: git $($GitArgs -join ' ')" }
}

function Invoke-Checked {
    param([string]$Label, [scriptblock]$Block, [switch]$SoftFail)
    Write-Host ""
    Write-Host "=== $Label ==="
    if ($DryRun) { Write-Host "[DRY-RUN] Skipped execution."; return $true }
    & $Block
    if ($LASTEXITCODE -ne 0) {
        if ($SoftFail) { Write-Warning "$Label failed with exit code $LASTEXITCODE"; return $false }
        throw "$Label failed with exit code $LASTEXITCODE"
    }
    return $true
}

function Resolve-RepoRoot {
    $root = (& git rev-parse --show-toplevel 2>$null)
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($root)) { throw "Run inside a Git repository checkout." }
    return (Resolve-Path $root.Trim()).Path
}

function Assert-FileExists {
    param([string]$PathValue)
    if (-not (Test-Path -LiteralPath $PathValue -PathType Leaf)) { throw "required file missing: $PathValue" }
}

function Test-ModeEnabled {
    param([string]$Name)
    return ($Mode -contains "all") -or ($Mode -contains $Name)
}

function New-SafeModeName {
    if ($Mode -contains "all") { return "all" }
    return (($Mode | Sort-Object -Unique) -join "_")
}

function Add-ExistingContextFile {
    param([string[]]$Current, [string]$PathValue)
    if ([string]::IsNullOrWhiteSpace($PathValue)) { return $Current }
    if (-not (Test-Path -LiteralPath $PathValue -PathType Leaf)) { return $Current }
    $normalized = $PathValue.Replace("\", "/").TrimStart("./")
    if ($Current -contains $normalized) { return $Current }
    return @($Current + $normalized)
}

$RepoRoot = Resolve-RepoRoot
Set-Location $RepoRoot
$env:PYTHONPATH = $RepoRoot

if ([string]::IsNullOrWhiteSpace($Stamp)) { $Stamp = Get-Date -Format "yyyyMMdd-HHmmss" }
$ModeName = New-SafeModeName
if ([string]::IsNullOrWhiteSpace($TaskBranch)) { $TaskBranch = "codex/local-ai-$ModeName-$Stamp" }

$Required = @(
    "AGENTS.md",
    "README.md",
    "WORKFLOW.md",
    "docs/README.md",
    "docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md",
    "Tools/validation/build_markdown_inventory.py",
    "Tools/validation/build_script_inventory.py",
    "Tools/validation/check_docs_links.py",
    "Tools/validation/check_validation_report_contract.py",
    "Tools/workflow/run_local_ai_task_via_pipeline.ps1",
    "Tools/workflow/run_post_validation_ai_packet.ps1",
    $TaskFile
)
foreach ($Path in $Required) { Assert-FileExists $Path }

$Status = (& git status --porcelain)
if ($LASTEXITCODE -ne 0) { throw "git status failed" }
if (-not $AllowDirty -and $Status) {
    Write-Host "[ERROR] Working tree has local changes:" -ForegroundColor Red
    $Status | ForEach-Object { Write-Host $_ }
    throw "working tree is not clean; rerun with -AllowDirty only when intended"
}

if (-not $SkipGitSync) {
    Invoke-Git @("fetch", "origin")
    Invoke-Git @("switch", "master")
    Invoke-Git @("pull", "--ff-only", "origin", "master")
}

if (-not $NoBranch) {
    $ExistingBranch = (& git branch --list $TaskBranch)
    if ($LASTEXITCODE -ne 0) { throw "git branch lookup failed" }
    if ($ExistingBranch) { Invoke-Git @("switch", $TaskBranch) } else { Invoke-Git @("switch", "-c", $TaskBranch) }
}

$RunDir = "output/local_ai_runs/${Stamp}_${ModeName}_unified"
$PipelineDir = "$RunDir/pipeline"
$ValidationDir = "output/validation"
New-Item -ItemType Directory -Force -Path $PipelineDir | Out-Null
New-Item -ItemType Directory -Force -Path $ValidationDir | Out-Null
New-Item -ItemType Directory -Force -Path "output/ai_pipeline" | Out-Null

$ContextFiles = @()
$ReportFiles = @()
$PhaseReports = [ordered]@{}
$PhaseStatus = [ordered]@{}

Write-Host "[INFO] Unified local-AI launcher"
Write-Host "[INFO] Mode: $($Mode -join ',')"
Write-Host "[INFO] Stamp: $Stamp"
Write-Host "[INFO] Branch: $TaskBranch"
Write-Host "[INFO] TaskFile: $TaskFile"
Write-Host "[INFO] RunDir: $RunDir"
Write-Host "[INFO] Ollama advisory: $UseOllamaAdvisory"
Write-Host "[INFO] Primary advisory provider: $UsePrimaryAdvisoryProvider"
Write-Host "[INFO] Multistep provider workflow: $RunMultistepProviderWorkflow"
Write-Host "[INFO] Patch specs: $GeneratePatchSpecs"

$PhaseStatus.baseline_compile = Invoke-Checked "Baseline compile validation/inventory tools" {
    python -m py_compile `
        .\Tools\validation\build_markdown_inventory.py `
        .\Tools\validation\build_script_inventory.py `
        .\Tools\validation\check_validation_report_contract.py
}

if (Test-ModeEnabled "smoke") {
    $PhaseStatus.git_diff_check_initial = Invoke-Checked "Initial git diff --check" { git diff --check } -SoftFail:$ContinueOnValidationError
    if (Test-Path .\Tools\workflow\startup_check.py) {
        $StartupCheck = "$ValidationDir/startup_check_${ModeName}_$Stamp.json"
        $PhaseStatus.startup_check = Invoke-Checked "Startup smoke check" {
            python .\Tools\workflow\startup_check.py --repo-root . --output $StartupCheck
        } -SoftFail:$ContinueOnValidationError
        if (Test-Path $StartupCheck) { $ReportFiles += $StartupCheck; $PhaseReports.startup_check = $StartupCheck }
    }
}

if (Test-ModeEnabled "md") {
    $MarkdownJson = "$ValidationDir/markdown_inventory_${ModeName}_$Stamp.json"
    $MarkdownMd = "$ValidationDir/markdown_inventory_${ModeName}_$Stamp.md"
    $DocsLinks = "$ValidationDir/docs_links_${ModeName}_$Stamp.json"
    $PhaseStatus.markdown_inventory = Invoke-Checked "Build Markdown inventory" {
        python .\Tools\validation\build_markdown_inventory.py --repo-root . --output $MarkdownJson --markdown-output $MarkdownMd
    }
    $PhaseStatus.docs_links = Invoke-Checked "Check docs links" {
        python .\Tools\validation\check_docs_links.py --repo-root . --output $DocsLinks
    } -SoftFail:$ContinueOnValidationError
    $ReportFiles += @($MarkdownJson, $DocsLinks)
    $ContextFiles = Add-ExistingContextFile $ContextFiles $MarkdownMd
    $PhaseReports.markdown_inventory = $MarkdownJson
    $PhaseReports.docs_links = $DocsLinks
}

if (Test-ModeEnabled "python") {
    $ScriptJson = "$ValidationDir/script_inventory_${ModeName}_$Stamp.json"
    $ScriptCsv = "$ValidationDir/script_inventory_${ModeName}_$Stamp.csv"
    $ScriptMd = "$ValidationDir/script_inventory_${ModeName}_$Stamp.md"
    $PhaseStatus.script_inventory = Invoke-Checked "Build script/tool inventory" {
        python .\Tools\validation\build_script_inventory.py --repo-root . --output $ScriptJson --csv-output $ScriptCsv --markdown-output $ScriptMd
    }
    $ReportFiles += $ScriptJson
    $ContextFiles = Add-ExistingContextFile $ContextFiles $ScriptMd
    $PhaseReports.script_inventory = $ScriptJson
    $PhaseReports.script_inventory_csv = $ScriptCsv
}

if (Test-ModeEnabled "validation") {
    if (Test-Path .\Tools\workflow\run_local_validation_after_refactor.ps1) {
        $ValidationArgs = @("-ExecutionPolicy", "Bypass", "-File", ".\Tools\workflow\run_local_validation_after_refactor.ps1", "-SkipPull", "-MatrixWorkers", "$MatrixWorkers", "-RepeatCases", "$RepeatCases")
        if ($ContinueOnValidationError) { $ValidationArgs += "-ContinueOnError" }
        $PhaseStatus.local_validation_after_refactor = Invoke-Checked "Run local validation after refactor" { powershell.exe @ValidationArgs } -SoftFail:$ContinueOnValidationError
    } else {
        Write-Warning "Tools/workflow/run_local_validation_after_refactor.ps1 not found; validation mode falls back to contract checks."
    }
}

if (Test-ModeEnabled "json") {
    $JsonContract = "$ValidationDir/validation_report_contract_json_${ModeName}_$Stamp.json"
    $Args = @(".\Tools\validation\check_validation_report_contract.py", "--repo-root", ".", "--output", $JsonContract)
    foreach ($Report in $ReportFiles) { $Args += @("--report-file", $Report) }
    $PhaseStatus.json_contract = Invoke-Checked "Validate current JSON/report contracts" { python @Args } -SoftFail:$ContinueOnValidationError
    $ReportFiles += $JsonContract
    $PhaseReports.json_contract = $JsonContract
}

$FinalContract = "$ValidationDir/validation_report_contract_${ModeName}_$Stamp.json"
$ContractArgs = @(".\Tools\validation\check_validation_report_contract.py", "--repo-root", ".", "--output", $FinalContract)
foreach ($Report in $ReportFiles) { $ContractArgs += @("--report-file", $Report) }
$PhaseStatus.task_scoped_contract = Invoke-Checked "Validate task-scoped reports" { python @ContractArgs } -SoftFail:$ContinueOnValidationError
$ReportFiles += $FinalContract
$PhaseReports.task_scoped_contract = $FinalContract

$ContextFiles = Add-ExistingContextFile $ContextFiles $TaskFile
$ContextFiles = Add-ExistingContextFile $ContextFiles "docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md"
$ContextFiles = Add-ExistingContextFile $ContextFiles "docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md"
$ContextFiles = Add-ExistingContextFile $ContextFiles "docs/LOCAL_AI_TASKS/code-refactor-local-machine-validation-addendum.md"

if ((Test-ModeEnabled "official") -or (Test-ModeEnabled "provider") -or (Test-ModeEnabled "patch_specs") -or $UseOllamaAdvisory -or $UsePrimaryAdvisoryProvider -or $RunMultistepProviderWorkflow -or $GeneratePatchSpecs -or $BuildEvidence) {
    $BaseName = "unified_${ModeName}_$Stamp"
    $ProposalBaseName = "unified_${ModeName}_proposals_$Stamp"
    $RunnerArgs = @(
        "-NoProfile", "-ExecutionPolicy", "Bypass",
        "-File", ".\Tools\workflow\run_local_ai_task_via_pipeline.ps1",
        "-PromptFile", $TaskFile,
        "-TaskFile", $TaskFile,
        "-RunDir", $RunDir,
        "-Profile", $Profile,
        "-Basename", $BaseName,
        "-ProposalBasename", $ProposalBaseName,
        "-MaxContextChars", "$MaxContextChars",
        "-ExtraContextFile", ($ContextFiles -join ",")
    )
    if ($Model -ne "") { $RunnerArgs += @("-Model", $Model) }
    if ($FullContextGoldenPath) { $RunnerArgs += "-FullContextGoldenPath" }
    if ($UsePrimaryAdvisoryProvider -or $UseOllamaAdvisory -or (Test-ModeEnabled "provider")) { $RunnerArgs += "-UsePrimaryAdvisoryProvider" }
    if ($RunMultistepProviderWorkflow) { $RunnerArgs += "-RunMultistepProviderWorkflow" }
    if ($RunOllamaProbe) { $RunnerArgs += "-RunOllamaProbe" }
    if ($RunNpuProbe) { $RunnerArgs += "-RunNpuProbe" }
    if ($RunNpuDecodeSmoke) { $RunnerArgs += "-RunNpuDecodeSmoke" }
    if ($BuildEvidence) { $RunnerArgs += "-BuildEvidence" }
    if ($GeneratePatchSpecs -or (Test-ModeEnabled "patch_specs")) { $RunnerArgs += "-GeneratePatchSpecs" }
    if ($DryRun) { $RunnerArgs += "-DryRun" }

    $PhaseStatus.official_pipeline = Invoke-Checked "Run official local AI pipeline adapter" { powershell.exe @RunnerArgs } -SoftFail:$ContinueOnValidationError
    $PhaseReports.official_packet = "$PipelineDir/$BaseName.json"
    $PhaseReports.official_proposals = "$PipelineDir/$ProposalBaseName.json"
}

if ($UseOllamaAdvisory -or (Test-ModeEnabled "provider")) {
    $OllamaBase = "unified_${ModeName}_ollama_$Stamp"
    $OllamaProposalBase = "unified_${ModeName}_ollama_proposals_$Stamp"
    $PostArgs = @(
        "-NoProfile", "-ExecutionPolicy", "Bypass",
        "-File", ".\Tools\workflow\run_post_validation_ai_packet.ps1",
        "-Profile", $Profile,
        "-OutputDir", "output\ai_pipeline",
        "-Basename", $OllamaBase,
        "-ProposalBasename", $OllamaProposalBase,
        "-ContextFile", ($ContextFiles -join ","),
        "-ReportFile", ($ReportFiles -join ","),
        "-UseOllama",
        "-Model", $Model,
        "-MaxContextChars", "$MaxContextChars"
    )
    if ($UsePrimaryAdvisoryProvider) { $PostArgs += "-UsePrimaryAdvisoryProvider" }
    $PhaseStatus.ollama_advisory = Invoke-Checked "Run Ollama advisory packet" { powershell.exe @PostArgs } -SoftFail:$ContinueOnValidationError
    $PhaseReports.ollama_packet = "output/ai_pipeline/$OllamaBase.json"
    $PhaseReports.ollama_proposals = "output/ai_pipeline/$OllamaProposalBase.json"
}

if (Test-ModeEnabled "full_validation") {
    $PhaseStatus.git_diff_check_final = Invoke-Checked "Final git diff --check" { git diff --check } -SoftFail:$ContinueOnValidationError
    $PhaseStatus.git_status_final = Invoke-Checked "Final git status --short" { git status --short } -SoftFail:$ContinueOnValidationError
}

$ManifestPath = "$PipelineDir/unified_local_ai_refactor_manifest.json"
$Manifest = [ordered]@{
    schema_version = 1
    kind = "unified_local_ai_refactor_manifest"
    generated_at = (Get-Date -Format o)
    repo_root = $RepoRoot
    mode = $Mode
    mode_name = $ModeName
    profile = $Profile
    model = $Model
    stamp = $Stamp
    task_file = $TaskFile.Replace("\", "/")
    task_branch = $TaskBranch
    run_dir = $RunDir.Replace("\", "/")
    provider_execution_requested = [bool]($UseOllamaAdvisory -or $UsePrimaryAdvisoryProvider -or $RunMultistepProviderWorkflow -or $RunOllamaProbe -or $RunNpuProbe -or $RunNpuDecodeSmoke -or (Test-ModeEnabled "provider"))
    patch_application_performed = $false
    patch_specs_requested = [bool]($GeneratePatchSpecs -or (Test-ModeEnabled "patch_specs"))
    build_evidence_requested = [bool]$BuildEvidence
    context_files = $ContextFiles
    report_files = $ReportFiles
    phase_status = $PhaseStatus
    phase_reports = $PhaseReports
    warnings = @()
    errors = @()
}
($Manifest | ConvertTo-Json -Depth 10) | Set-Content -LiteralPath $ManifestPath -Encoding UTF8

Write-Host ""
Write-Host "[OK] Unified local-AI launcher complete" -ForegroundColor Green
Write-Host "[OK] Manifest: $ManifestPath"
Write-Host "[OK] Mode: $($Mode -join ',')"
Write-Host "[OK] Provider execution requested: $($Manifest.provider_execution_requested)"
Write-Host "[OK] Patch specs requested: $($Manifest.patch_specs_requested)"
Write-Host "[OK] Patch application performed: False"
Write-Host "[OK] Reports: $($ReportFiles -join ', ')"
Write-Host "[OK] Context files: $($ContextFiles -join ', ')"
