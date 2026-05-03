param(
    [string]$RepoRoot = ".",
    [string]$Stamp = "",
    [string]$OutputRoot = "output",
    [string]$EvidenceDir = "docs/LOCAL_VALIDATION_EVIDENCE",
    [switch]$RunGpuNpuProvider,
    [switch]$SkipMemoryReload,
    [switch]$SkipPostValidationPacket,
    [switch]$SkipSharedToolboxBundle,
    [int]$BudgetMinutes = 30,
    [int]$MaxRounds = 20,
    [int]$FilesPerRound = 8,
    [int]$MaxContextFiles = 220,
    [int]$MaxCharsPerFile = 6000,
    [int]$MaxNewTokens = 3600,
    [string]$KeepAlive = "35m",
    [int]$NpuAuditorEveryRounds = 3,
    [int]$NpuAuditorTimeoutSeconds = 420,
    [int]$NpuMaxContextChars = 8000,
    [int]$NpuMaxPromptChars = 1200,
    [int]$NpuMaxNewTokens = 384,
    [int]$NpuFinalWaitSeconds = 180,
    [int]$MinRecommendations = 1,
    [int]$MinPatchPlans = 1
)

$ErrorActionPreference = "Stop"
$RepoRootPath = Resolve-Path $RepoRoot
Set-Location $RepoRootPath

if ($Stamp -eq "") {
    $Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
}

$env:PYTHONPATH = (Get-Location).Path

function Read-JsonFile {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        return $null
    }
    return Get-Content $Path -Raw | ConvertFrom-Json
}

function Add-ExistingPath {
    param(
        [System.Collections.ArrayList]$List,
        [string]$Path
    )
    if ($Path -and (Test-Path $Path)) {
        [void]$List.Add($Path)
    }
}

function Invoke-RepoPython {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$ArgsList,
        [string]$Label = "python"
    )
    Write-Host ""
    Write-Host "=== $Label ==="
    python @ArgsList
}

$WorkflowJson = ".\output\validation\agent_review_full_toolbox_decision_loop_${Stamp}_workflow.json"
$WorkflowMd = ".\output\validation\agent_review_full_toolbox_decision_loop_${Stamp}_workflow.md"
$DecisionLoopJson = ".\output\ai_pipeline\full_toolbox_${Stamp}_agent_review_decision_loop.json"
$WarningPolicyJson = ".\output\validation\agent_review_warning_policy_${Stamp}.json"
$WarningPolicyMd = ".\output\validation\agent_review_warning_policy_${Stamp}.md"
$IntegratedJson = ".\output\validation\agent_review_full_toolbox_decision_loop_${Stamp}_integrated.json"
$IntegratedMd = ".\output\validation\agent_review_full_toolbox_decision_loop_${Stamp}_integrated.md"
$FinalContractJson = ".\output\validation\validation_report_contract_full_toolbox_integrated_$Stamp.json"

$RunnerParams = @{
    RepoRoot = "."
    Stamp = $Stamp
    OutputRoot = $OutputRoot
    EvidenceDir = $EvidenceDir
    BudgetMinutes = $BudgetMinutes
    MaxRounds = $MaxRounds
    FilesPerRound = $FilesPerRound
    MaxContextFiles = $MaxContextFiles
    MaxCharsPerFile = $MaxCharsPerFile
    MaxNewTokens = $MaxNewTokens
    KeepAlive = $KeepAlive
    NpuAuditorEveryRounds = $NpuAuditorEveryRounds
    NpuAuditorTimeoutSeconds = $NpuAuditorTimeoutSeconds
    NpuMaxContextChars = $NpuMaxContextChars
    NpuMaxPromptChars = $NpuMaxPromptChars
    NpuMaxNewTokens = $NpuMaxNewTokens
    NpuFinalWaitSeconds = $NpuFinalWaitSeconds
    MinRecommendations = $MinRecommendations
    MinPatchPlans = $MinPatchPlans
}
if ($RunGpuNpuProvider) { $RunnerParams.RunGpuNpuProvider = $true }
if ($SkipMemoryReload) { $RunnerParams.SkipMemoryReload = $true }
if ($SkipPostValidationPacket) { $RunnerParams.SkipPostValidationPacket = $true }
if ($SkipSharedToolboxBundle) { $RunnerParams.SkipSharedToolboxBundle = $true }

Write-Host "=== Integrated Agent Review Full Toolbox Decision Loop ==="
Write-Host "Repo: $RepoRootPath"
Write-Host "Stamp: $Stamp"
Write-Host "RunGpuNpuProvider: $RunGpuNpuProvider"
Write-Host "Integration: base workflow + agent_review_warning_policy ledger"

& .\Tools\workflow\run_agent_review_full_toolbox_decision_loop.ps1 @RunnerParams

$Workflow = Read-JsonFile $WorkflowJson
if (-not $Workflow) {
    throw "Missing base workflow report: $WorkflowJson"
}
if (-not (Test-Path $DecisionLoopJson)) {
    throw "Missing decision loop report: $DecisionLoopJson"
}

$ReportFiles = [System.Collections.ArrayList]@()
foreach ($Path in $Workflow.reports) {
    Add-ExistingPath -List $ReportFiles -Path ([string]$Path)
}
Add-ExistingPath -List $ReportFiles -Path $WorkflowJson
Add-ExistingPath -List $ReportFiles -Path $DecisionLoopJson

$WarningArgs = @(
    ".\Tools\ai\agent_review_warning_policy.py",
    "--repo-root", ".",
    "--decision-report", $DecisionLoopJson,
    "--final-report", $WorkflowJson,
    "--min-recommendations", "$MinRecommendations",
    "--min-patch-plans", "$MinPatchPlans",
    "--output", $WarningPolicyJson,
    "--markdown-output", $WarningPolicyMd
)
foreach ($Report in $ReportFiles) {
    $WarningArgs += @("--report-file", [string]$Report)
}
Invoke-RepoPython -Label "Integrated warning policy ledger" -ArgsList $WarningArgs

$WarningPolicy = Read-JsonFile $WarningPolicyJson
if (-not $WarningPolicy) {
    throw "Missing warning policy report: $WarningPolicyJson"
}

$Decision = Read-JsonFile $DecisionLoopJson
$BaseErrors = @()
foreach ($ErrorItem in @($Workflow.errors)) {
    $BaseErrors += [string]$ErrorItem
}
$FatalErrors = @()
foreach ($ErrorItem in @($WarningPolicy.errors)) {
    $FatalErrors += [string]$ErrorItem
}
$IntegratedWarnings = @()
foreach ($WarningItem in @($Workflow.warnings)) {
    $IntegratedWarnings += [string]$WarningItem
}
foreach ($WarningItem in @($WarningPolicy.warnings)) {
    $IntegratedWarnings += [string]$WarningItem
}

$RecoveredByPolicy = ($WarningPolicy.passed -eq $true -and $WarningPolicy.decision_recovered -eq $true)
$IntegratedPassed = ($RecoveredByPolicy -and $FatalErrors.Count -eq 0)
if (-not $IntegratedPassed -and $BaseErrors.Count -gt 0) {
    foreach ($ErrorItem in $BaseErrors) {
        if ($FatalErrors -notcontains $ErrorItem) {
            $FatalErrors += $ErrorItem
        }
    }
}

$IntegratedReport = [ordered]@{
    schema_version = 1
    kind = "agent_review_full_toolbox_decision_loop_integrated"
    generated_at = (Get-Date).ToString("s")
    repo_root = "$RepoRootPath"
    stamp = $Stamp
    passed = $IntegratedPassed
    errors = @($FatalErrors)
    warnings = @($IntegratedWarnings)
    provider_execution_performed = [bool]$RunGpuNpuProvider
    patch_application_performed = $false
    source_writes_performed = $false
    sqlite_write_performed = $false
    persistent_memory_write_performed = $false
    manual_review_required = $true
    base_workflow_passed = $Workflow.passed
    warning_policy_passed = $WarningPolicy.passed
    decision_recovered = $WarningPolicy.decision_recovered
    recommendation_count = if ($Decision) { $Decision.recommendation_count } else { $null }
    patch_plan_count = if ($Decision) { $Decision.patch_plan_count } else { $null }
    deterministic_synthesizer_used = if ($Decision) { $Decision.deterministic_synthesizer_used } else { $null }
    patch_plan_fallback_used = if ($Decision) { $Decision.patch_plan_fallback_used } else { $null }
    input_nonfatal_warning_count = $WarningPolicy.input_nonfatal_warning_count
    fatal_report_failure_count = $WarningPolicy.fatal_report_failure_count
    warning_level_counts = $WarningPolicy.warning_level_counts
    warning_classification_counts = $WarningPolicy.warning_classification_counts
    input_nonfatal_warnings = @($WarningPolicy.input_nonfatal_warnings)
    fatal_report_failures = @($WarningPolicy.fatal_report_failures)
    workflow = $WorkflowJson
    warning_policy = $WarningPolicyJson
    decision_report = $DecisionLoopJson
    evidence_to_commit = @($Workflow.evidence_to_commit)
    guardrails = [ordered]@{
        report_only = $true
        warning_policy_integrated = $true
        provider_execution_requires_explicit_flag = $true
        run_gpu_npu_provider = [bool]$RunGpuNpuProvider
        patch_application_performed = $false
        source_writes_performed = $false
        sqlite_write_performed = $false
        persistent_memory_write_performed = $false
        blender_runtime_execution_performed = $false
        raw_output_commit_allowed = $false
    }
}
$IntegratedReport | ConvertTo-Json -Depth 12 | Set-Content -Path $IntegratedJson -Encoding UTF8

$InputWarningLines = @()
foreach ($Item in @($WarningPolicy.input_nonfatal_warnings)) {
    $InputWarningLines += "- ``$($Item.level)`` ``$($Item.path)``: $($Item.reason)"
}
if ($InputWarningLines.Count -eq 0) {
    $InputWarningLines += "- none"
}

$FatalLines = @()
foreach ($Item in @($WarningPolicy.fatal_report_failures)) {
    $FatalLines += "- ``$($Item.level)`` ``$($Item.path)``: $($Item.reason)"
}
if ($FatalLines.Count -eq 0) {
    $FatalLines += "- none"
}

$Markdown = @(
    "# Integrated Agent Review Full Toolbox Decision Loop",
    "",
    "- Passed: ``$IntegratedPassed``",
    "- Stamp: ``$Stamp``",
    "- Base workflow passed: ``$($Workflow.passed)``",
    "- Warning policy passed: ``$($WarningPolicy.passed)``",
    "- Decision recovered: ``$($WarningPolicy.decision_recovered)``",
    "- Recommendation count: ``$($IntegratedReport.recommendation_count)``",
    "- Patch plan count: ``$($IntegratedReport.patch_plan_count)``",
    "- Input-nonfatal warning count: ``$($WarningPolicy.input_nonfatal_warning_count)``",
    "- Fatal report failure count: ``$($WarningPolicy.fatal_report_failure_count)``",
    "- Provider execution performed: ``$([bool]$RunGpuNpuProvider)``",
    "- Patch application performed: ``False``",
    "- SQLite write performed: ``False``",
    "- Persistent memory write performed: ``False``",
    "",
    "## Input-nonfatal warnings",
    ""
) + $InputWarningLines + @(
    "",
    "## Fatal report failures",
    ""
) + $FatalLines
$Markdown | Set-Content -Path $IntegratedMd -Encoding UTF8

Invoke-RepoPython -Label "Integrated scoped validation report contract" -ArgsList @(
    ".\Tools\validation\check_validation_report_contract.py",
    "--repo-root", ".",
    "--report-file", $IntegratedJson,
    "--report-file", $WarningPolicyJson,
    "--output", $FinalContractJson
)

Write-Host ""
Write-Host "=== Integrated full toolbox decision loop summary ==="
Write-Host "Integrated: $IntegratedJson"
Write-Host "Markdown: $IntegratedMd"
Write-Host "Warning policy: $WarningPolicyJson"
Write-Host "Passed: $IntegratedPassed"
Write-Host "Recommendation count: $($IntegratedReport.recommendation_count)"
Write-Host "Patch plan count: $($IntegratedReport.patch_plan_count)"
Write-Host "Input-nonfatal warning count: $($WarningPolicy.input_nonfatal_warning_count)"
Write-Host "Fatal report failure count: $($WarningPolicy.fatal_report_failure_count)"
Write-Host ""
Write-Host "Git policy: stage only docs/LOCAL_VALIDATION_EVIDENCE outputs listed in integrated.evidence_to_commit. Do not stage output/**, *.db or *.sqlite."
