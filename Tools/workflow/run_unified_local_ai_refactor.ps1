<#
.SYNOPSIS
  Console-style unified launcher for IA-Carmine local AI refactor workflows.

.DESCRIPTION
  This is the single independent entrypoint for choosing what to run over the
  same task Markdown input.

  It behaves like a small console installer: if -Mode is omitted or -Interactive
  is passed, it prints available phases and asks what to execute. The selected
  phases are then normalized and executed in a fixed safe order.

  Logical order when multiple phases are selected:
    baseline -> smoke -> validation -> md -> json -> python -> chunks -> context_pack -> agent_state -> official -> provider -> patch_specs -> evidence -> full_validation -> final_contract

  The script is report/proposal-only. It does not apply patches, run Blender,
  run FFmpeg, commit, push or merge.

.EXAMPLES
  Interactive console selection:
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 -Interactive

  Comma-separated modes:
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 -Mode smoke,md,python,contract,full_validation

  Array-like modes:
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 -Mode smoke md python contract full_validation

  Full combined advisory run:
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 -Mode all -UseOllamaAdvisory -UsePrimaryAdvisoryProvider -GeneratePatchSpecs
#>
[CmdletBinding()]
param(
    [string[]]$Mode = @(),

    [string]$TaskFile = ".\docs\LOCAL_AI_TASKS\docs-md-obsolete-pruning-next-step.md",
    [string]$TaskBranch = "",
    [string]$Stamp = "",
    [ValidateSet("core", "npu", "docs")]
    [string]$Profile = "docs",
    [string]$Model = "gpt-oss:20b",
    [int]$MaxContextChars = 12000,

    [switch]$Interactive,
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

$ModeOrder = @(
    "baseline",
    "smoke",
    "validation",
    "md",
    "json",
    "python",
    "chunks",
    "context_pack",
    "agent_state",
    "official",
    "provider",
    "patch_specs",
    "evidence",
    "contract",
    "full_validation"
)

$ModeDescriptions = [ordered]@{
    baseline = "Compile core inventory/contract tools and prepare run state. Always executed."
    smoke = "Fast smoke checks: git diff --check and startup_check.py when available."
    validation = "Run broad local validation after refactor when the project wrapper exists."
    md = "Build Markdown inventory, docs link report and Markdown cleanup evidence."
    json = "Validate task-scoped JSON/report contracts for reports produced in this run."
    python = "Build full script/tool inventory with CSV/Markdown review surfaces."
    chunks = "Build/select semantic chunks for focused code/document context."
    context_pack = "Build bounded AI context pack for backend/core/provider work."
    agent_state = "Build local agent-state packet and optional SQLite-memory handoff context."
    official = "Run the official project-owned local AI task pipeline adapter."
    provider = "Run explicit advisory/provider path; Ollama remains advisory unless separately applied later."
    patch_specs = "Generate review-only patch specs from proposals. No apply."
    evidence = "Build compact GitHub evidence bundle when explicitly requested."
    contract = "Run current task-scoped report-contract validation."
    full_validation = "Final git diff/status and post-run consistency checks."
    all = "Run every available phase in safe order."
}

$ModeAliases = @{
    py = "python"
    ps1 = "python"
    scripts = "python"
    script = "python"
    markdown = "md"
    docs = "md"
    documentazione = "md"
    report = "json"
    reports = "json"
    json_contract = "json"
    provider_advisory = "provider"
    ollama = "provider"
    gpu = "provider"
    npu = "provider"
    planner = "official"
    patch_planner = "patch_specs"
    patch_plan = "patch_specs"
    tests = "validation"
    test = "validation"
    validate = "validation"
    validate_all = "full_validation"
    full = "all"
}

function Show-LauncherIntro {
    Write-Host ""
    Write-Host "IA-Carmine Unified Local AI Refactor Launcher" -ForegroundColor Cyan
    Write-Host "================================================"
    Write-Host "One task Markdown input; selectable phases; report/proposal-only by default."
    Write-Host ""
    Write-Host "What this launcher can do:"
    Write-Host "  - inventory and triage Markdown documentation;"
    Write-Host "  - inventory Python/PowerShell/shell/tool scripts;"
    Write-Host "  - validate JSON/report contracts;"
    Write-Host "  - run smoke and broad validation wrappers;"
    Write-Host "  - build semantic chunks, context packs and agent-state packets;"
    Write-Host "  - call the official local AI pipeline adapter;"
    Write-Host "  - optionally run Ollama/advisory provider paths;"
    Write-Host "  - optionally generate review-only patch specs/evidence."
    Write-Host ""
    Write-Host "Hard guardrails: no patch apply, no commit, no push, no merge, no Blender runtime, no FFmpeg runtime."
    Write-Host ""
}

function Show-ModeCatalog {
    Write-Host "Available modes:" -ForegroundColor Cyan
    foreach ($name in ($ModeDescriptions.Keys)) {
        Write-Host ("  {0,-15} {1}" -f $name, $ModeDescriptions[$name])
    }
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  smoke,md,python,contract,full_validation"
    Write-Host "  md,json,python,official,patch_specs"
    Write-Host "  all"
    Write-Host ""
}

function Normalize-ModeList {
    param([string[]]$Values)

    $items = @()
    foreach ($value in $Values) {
        if ([string]::IsNullOrWhiteSpace($value)) { continue }
        foreach ($part in ([string]$value).Split(",")) {
            $item = $part.Trim().ToLowerInvariant()
            if ([string]::IsNullOrWhiteSpace($item)) { continue }
            if ($ModeAliases.ContainsKey($item)) { $item = $ModeAliases[$item] }
            $items += $item
        }
    }

    if ($items.Count -eq 0) { return @() }
    if ($items -contains "all") { return @($ModeOrder | Where-Object { $_ -ne "baseline" }) }

    $unknown = @($items | Where-Object { $ModeDescriptions.Keys -notcontains $_ })
    if ($unknown.Count -gt 0) {
        throw "Unknown mode(s): $($unknown -join ', '). Use -Interactive to list modes."
    }

    $ordered = @()
    foreach ($known in $ModeOrder) {
        if ($known -eq "baseline") { continue }
        if ($items -contains $known -and $ordered -notcontains $known) { $ordered += $known }
    }
    return $ordered
}

function Read-InteractiveModes {
    Show-ModeCatalog
    $answer = Read-Host "Select modes"
    return Normalize-ModeList @($answer)
}

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
    return $ResolvedModes -contains $Name
}

function New-SafeModeName {
    if ($ResolvedModes.Count -eq 0) { return "interactive" }
    return (($ResolvedModes | Sort-Object -Unique) -join "_")
}

function Add-ExistingContextFile {
    param([string[]]$Current, [string]$PathValue)
    if ([string]::IsNullOrWhiteSpace($PathValue)) { return $Current }
    if (-not (Test-Path -LiteralPath $PathValue -PathType Leaf)) { return $Current }
    $normalized = $PathValue.Replace("\", "/").TrimStart("./")
    if ($Current -contains $normalized) { return $Current }
    return @($Current + $normalized)
}

function Add-OptionalModeFromTool {
    param([string]$ModeName, [string]$ToolPath, [ref]$Warnings)
    if ((Test-ModeEnabled $ModeName) -and -not (Test-Path -LiteralPath $ToolPath -PathType Leaf)) {
        $Warnings.Value += "Mode '$ModeName' requested but tool is missing: $ToolPath"
        return $false
    }
    return $true
}

Show-LauncherIntro

$RepoRoot = Resolve-RepoRoot
Set-Location $RepoRoot
$env:PYTHONPATH = $RepoRoot

if ($Interactive -or $Mode.Count -eq 0) {
    $ResolvedModes = Read-InteractiveModes
} else {
    $ResolvedModes = Normalize-ModeList $Mode
}

if ($ResolvedModes.Count -eq 0) {
    throw "No modes selected. Use -Interactive or -Mode all."
}

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

$Warnings = @()
[void](Add-OptionalModeFromTool "validation" ".\Tools\workflow\run_local_validation_after_refactor.ps1" ([ref]$Warnings))
[void](Add-OptionalModeFromTool "smoke" ".\Tools\workflow\startup_check.py" ([ref]$Warnings))
[void](Add-OptionalModeFromTool "chunks" ".\Tools\npu\build_semantic_code_chunks.py" ([ref]$Warnings))
[void](Add-OptionalModeFromTool "context_pack" ".\Tools\ai\build_ai_context_pack.py" ([ref]$Warnings))
[void](Add-OptionalModeFromTool "agent_state" ".\Tools\ai\build_agent_state_packet.py" ([ref]$Warnings))

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

Write-Host "[INFO] Resolved modes: $($ResolvedModes -join ',')"
Write-Host "[INFO] Stamp: $Stamp"
Write-Host "[INFO] Branch: $TaskBranch"
Write-Host "[INFO] TaskFile: $TaskFile"
Write-Host "[INFO] RunDir: $RunDir"
Write-Host "[INFO] Ollama advisory: $UseOllamaAdvisory"
Write-Host "[INFO] Primary advisory provider: $UsePrimaryAdvisoryProvider"
Write-Host "[INFO] Multistep provider workflow: $RunMultistepProviderWorkflow"
Write-Host "[INFO] Patch specs: $GeneratePatchSpecs"

if ($Warnings.Count -gt 0) {
    foreach ($warning in $Warnings) { Write-Warning $warning }
}

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

if (Test-ModeEnabled "validation") {
    if (Test-Path .\Tools\workflow\run_local_validation_after_refactor.ps1) {
        $ValidationArgs = @("-ExecutionPolicy", "Bypass", "-File", ".\Tools\workflow\run_local_validation_after_refactor.ps1", "-SkipPull", "-MatrixWorkers", "$MatrixWorkers", "-RepeatCases", "$RepeatCases")
        if ($ContinueOnValidationError) { $ValidationArgs += "-ContinueOnError" }
        $PhaseStatus.local_validation_after_refactor = Invoke-Checked "Run local validation after refactor" { powershell.exe @ValidationArgs } -SoftFail:$ContinueOnValidationError
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

if (Test-ModeEnabled "json") {
    $JsonContract = "$ValidationDir/validation_report_contract_json_${ModeName}_$Stamp.json"
    $Args = @(".\Tools\validation\check_validation_report_contract.py", "--repo-root", ".", "--output", $JsonContract)
    foreach ($Report in $ReportFiles) { $Args += @("--report-file", $Report) }
    $PhaseStatus.json_contract = Invoke-Checked "Validate current JSON/report contracts" { python @Args } -SoftFail:$ContinueOnValidationError
    $ReportFiles += $JsonContract
    $PhaseReports.json_contract = $JsonContract
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

if (Test-ModeEnabled "chunks") {
    $PhaseStatus.semantic_chunks = Invoke-Checked "Build semantic code chunks" {
        python .\Tools\npu\build_semantic_code_chunks.py --repo-root .
    } -SoftFail:$ContinueOnValidationError
    $ContextFiles = Add-ExistingContextFile $ContextFiles "indexAI/code_chunks/semantic_code_chunks_manifest.json"
}

if (Test-ModeEnabled "context_pack") {
    $ContextPackBase = "unified_${ModeName}_context_pack_$Stamp"
    $PhaseStatus.context_pack = Invoke-Checked "Build AI context pack" {
        python .\Tools\ai\build_ai_context_pack.py --repo-root . --profile core_ai_backend --basename $ContextPackBase --evidence-basename "${ContextPackBase}_evidence" --max-total-chars 64000 --max-file-chars 4000
    } -SoftFail:$ContinueOnValidationError
    $ContextFiles = Add-ExistingContextFile $ContextFiles "output/ai_context_packs/$ContextPackBase.md"
    $ContextFiles = Add-ExistingContextFile $ContextFiles "output/ai_context_packs/$ContextPackBase.json"
}

if (Test-ModeEnabled "agent_state") {
    $AgentStateDir = "$PipelineDir/agent_state"
    New-Item -ItemType Directory -Force -Path $AgentStateDir | Out-Null
    $AgentStateBase = "unified_${ModeName}_agent_state_$Stamp"
    $PhaseStatus.agent_state = Invoke-Checked "Build agent state packet" {
        python .\Tools\ai\build_agent_state_packet.py --repo-root . --objective "Unified local AI refactor run $ModeName" --output-dir $AgentStateDir --packet-name $AgentStateBase --max-memory-chars 24000 --memory-note "Unified launcher report-only run."
    } -SoftFail:$ContinueOnValidationError
    $ContextFiles = Add-ExistingContextFile $ContextFiles "$AgentStateDir/$AgentStateBase.md"
    $ContextFiles = Add-ExistingContextFile $ContextFiles "$AgentStateDir/$AgentStateBase.json"
}

$FinalContract = "$ValidationDir/validation_report_contract_${ModeName}_$Stamp.json"
if ((Test-ModeEnabled "contract") -or $ReportFiles.Count -gt 0) {
    $ContractArgs = @(".\Tools\validation\check_validation_report_contract.py", "--repo-root", ".", "--output", $FinalContract)
    foreach ($Report in $ReportFiles) { $ContractArgs += @("--report-file", $Report) }
    $PhaseStatus.task_scoped_contract = Invoke-Checked "Validate task-scoped reports" { python @ContractArgs } -SoftFail:$ContinueOnValidationError
    $ReportFiles += $FinalContract
    $PhaseReports.task_scoped_contract = $FinalContract
}

$ContextFiles = Add-ExistingContextFile $ContextFiles $TaskFile
$ContextFiles = Add-ExistingContextFile $ContextFiles "docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md"
$ContextFiles = Add-ExistingContextFile $ContextFiles "docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md"
$ContextFiles = Add-ExistingContextFile $ContextFiles "docs/LOCAL_AI_TASKS/code-refactor-local-machine-validation-addendum.md"

if ((Test-ModeEnabled "official") -or (Test-ModeEnabled "provider") -or (Test-ModeEnabled "patch_specs") -or (Test-ModeEnabled "evidence") -or $UseOllamaAdvisory -or $UsePrimaryAdvisoryProvider -or $RunMultistepProviderWorkflow -or $GeneratePatchSpecs -or $BuildEvidence) {
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
        "-MaxContextChars", "$MaxContextChars,
        "-ExtraContextFile", ($ContextFiles -join ",")
    )
    if ($Model -ne "") { $RunnerArgs += @("-Model", $Model) }
    if ($FullContextGoldenPath) { $RunnerArgs += "-FullContextGoldenPath" }
    if ($UsePrimaryAdvisoryProvider -or $UseOllamaAdvisory -or (Test-ModeEnabled "provider")) { $RunnerArgs += "-UsePrimaryAdvisoryProvider" }
    if ($RunMultistepProviderWorkflow) { $RunnerArgs += "-RunMultistepProviderWorkflow" }
    if ($RunOllamaProbe) { $RunnerArgs += "-RunOllamaProbe" }
    if ($RunNpuProbe) { $RunnerArgs += "-RunNpuProbe" }
    if ($RunNpuDecodeSmoke) { $RunnerArgs += "-RunNpuDecodeSmoke" }
    if ($BuildEvidence -or (Test-ModeEnabled "evidence")) { $RunnerArgs += "-BuildEvidence" }
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
    mode = $ResolvedModes
    mode_name = $ModeName
    available_modes = @($ModeDescriptions.Keys)
    profile = $Profile
    model = $Model
    stamp = $Stamp
    task_file = $TaskFile.Replace("\", "/")
    task_branch = $TaskBranch
    run_dir = $RunDir.Replace("\", "/")
    provider_execution_requested = [bool]($UseOllamaAdvisory -or $UsePrimaryAdvisoryProvider -or $RunMultistepProviderWorkflow -or $RunOllamaProbe -or $RunNpuProbe -or $RunNpuDecodeSmoke -or (Test-ModeEnabled "provider"))
    patch_application_performed = $false
    patch_specs_requested = [bool]($GeneratePatchSpecs -or (Test-ModeEnabled "patch_specs"))
    build_evidence_requested = [bool]($BuildEvidence -or (Test-ModeEnabled "evidence"))
    context_files = $ContextFiles
    report_files = $ReportFiles
    phase_status = $PhaseStatus
    phase_reports = $PhaseReports
    warnings = $Warnings
    errors = @()
}
($Manifest | ConvertTo-Json -Depth 10) | Set-Content -LiteralPath $ManifestPath -Encoding UTF8

Write-Host ""
Write-Host "[OK] Unified local-AI launcher complete" -ForegroundColor Green
Write-Host "[OK] Manifest: $ManifestPath"
Write-Host "[OK] Mode: $($ResolvedModes -join ',')"
Write-Host "[OK] Provider execution requested: $($Manifest.provider_execution_requested)"
Write-Host "[OK] Patch specs requested: $($Manifest.patch_specs_requested)"
Write-Host "[OK] Patch application performed: False"
Write-Host "[OK] Reports: $($ReportFiles -join ', ')"
Write-Host "[OK] Context files: $($ContextFiles -join ', ')"
