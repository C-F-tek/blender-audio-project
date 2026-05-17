param(
    [string]$RepoRoot = ".",
    [string]$Stamp = "",
    [string]$Objective = "Prepare IA-Carmine memory/tool/GPU/NPU preflight evidence for a report-only local AI cycle.",
    [string]$OutputRoot = "output",
    [string]$EvidenceDir = "docs/LOCAL_VALIDATION_EVIDENCE",
    [switch]$SkipMemoryInventory,
    [switch]$SkipCodeInterpreter,
    [switch]$SkipGpuContractSmoke,
    [switch]$SkipSharedToolboxBundleSmoke,
    [switch]$SkipRefactorDuplicationAudit,
    [switch]$EnableNpuProviderEnvironmentCheck,
    [string[]]$InputAuditReport = @(),
    [string[]]$ExtraReport = @(),
    [string[]]$ExtraArtifact = @(),
    [switch]$WriteCompactBundle,
    [int]$TimeoutSeconds = 300,
    [int]$MaxIncludedArtifactChars = 16000,
    [int]$MaxIncludedArtifacts = 40
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "python_env.ps1")
$RepoRootPath = Resolve-Path $RepoRoot
Set-Location $RepoRootPath
if ($Stamp -eq "") {
    $Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
}
$null = Use-WorkflowPython -RepoRoot $RepoRootPath

$AiPipelineDir = Join-Path $OutputRoot "ai_pipeline"
$ValidationDir = Join-Path $OutputRoot "validation"
$AnalysisDir = Join-Path $OutputRoot "analysis"
$EvidencePath = $EvidenceDir
New-Item -ItemType Directory -Force -Path $AiPipelineDir, $ValidationDir, $AnalysisDir, $EvidencePath | Out-Null

function Invoke-RepoPython {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$ArgsList,
        [string]$Label = "python"
    )
    Write-Host ""
    Write-Host "=== $Label ==="
    Invoke-WorkflowPython $ArgsList
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

function Read-JsonOrNull {
    param([string]$Path)
    if (-not (Test-Path $Path)) { return $null }
    try {
        return Get-Content $Path -Raw | ConvertFrom-Json
    } catch {
        return $null
    }
}

$Reports = [System.Collections.ArrayList]@()
$Artifacts = [System.Collections.ArrayList]@()
$Warnings = [System.Collections.ArrayList]@()
$Errors = [System.Collections.ArrayList]@()

$MemoryInventoryJson = ".\$AiPipelineDir\ai_cycle_startup_${Stamp}_agent_memory_inventory.json"
$MemoryInventoryMd = ".\$AiPipelineDir\ai_cycle_startup_${Stamp}_agent_memory_inventory.md"
$ToolInventoryJson = ".\$AiPipelineDir\ai_cycle_startup_${Stamp}_agnostic_tool_inventory.json"
$ToolInventoryMd = ".\$AiPipelineDir\ai_cycle_startup_${Stamp}_agnostic_tool_inventory.md"
$PersistentStatusJson = ".\$ValidationDir\ai_cycle_startup_${Stamp}_persistent_memory_status.json"
$PersistentStatusMd = ".\$ValidationDir\ai_cycle_startup_${Stamp}_persistent_memory_status.md"
$OperationalStatusJson = ".\$ValidationDir\ai_cycle_startup_${Stamp}_operational_memory_status.json"
$OperationalStatusMd = ".\$ValidationDir\ai_cycle_startup_${Stamp}_operational_memory_status.md"
$LineCountCsv = ".\$ValidationDir\ai_cycle_startup_python_line_count_$Stamp.csv"
$LineCountJson = ".\$ValidationDir\ai_cycle_startup_${Stamp}_python_line_count.json"
$LineCountMd = ".\$ValidationDir\ai_cycle_startup_${Stamp}_python_line_count.md"
$LineCountAllMd = ".\$ValidationDir\ai_cycle_startup_all_python_files_$Stamp.md"
$CodeInterpreterJson = ".\$AnalysisDir\ai_cycle_startup_${Stamp}_code_interpreter.json"
$CodeInterpreterMd = ".\$AnalysisDir\ai_cycle_startup_${Stamp}_code_interpreter.md"
$PythonSyntaxJson = ".\$ValidationDir\ai_cycle_startup_${Stamp}_python_syntax.json"
$GpuContractJson = ".\$ValidationDir\ai_cycle_startup_${Stamp}_gpu_contract_smoke.json"
$GpuContractMd = ".\$ValidationDir\ai_cycle_startup_${Stamp}_gpu_contract_smoke.md"
$SharedBundleSmokeJson = ".\$ValidationDir\ai_cycle_startup_${Stamp}_shared_toolbox_bundle_smoke.json"
$SharedBundleSmokeMd = ".\$ValidationDir\ai_cycle_startup_${Stamp}_shared_toolbox_bundle_smoke.md"
$MemoryRoutingJson = ".\$ValidationDir\ai_cycle_startup_${Stamp}_memory_routing_policy.json"
$MemoryRoutingMd = ".\$ValidationDir\ai_cycle_startup_${Stamp}_memory_routing_policy.md"
$NpuEnvJson = ".\$ValidationDir\ai_cycle_startup_${Stamp}_npu_provider_environment.json"
$NpuEnvMd = ".\$ValidationDir\ai_cycle_startup_${Stamp}_npu_provider_environment.md"
$DupAuditJson = ".\$AnalysisDir\ai_cycle_startup_${Stamp}_refactor_duplication_audit.json"
$DupAuditMd = ".\$AnalysisDir\ai_cycle_startup_${Stamp}_refactor_duplication_audit.md"
$WorkflowJson = ".\$ValidationDir\ai_cycle_startup_${Stamp}_workflow.json"
$WorkflowMd = ".\$ValidationDir\ai_cycle_startup_${Stamp}_workflow.md"
$BundleBase = "ai_cycle_startup_preflight_bundle_$Stamp"
$BundleJson = ".\$EvidencePath\$BundleBase.json"
$BundleMd = ".\$EvidencePath\$BundleBase.md"

Write-Host "=== IA-Carmine startup/preflight ==="
Write-Host "Repo: $RepoRootPath"
Write-Host "Stamp: $Stamp"
Write-Host "Objective: $Objective"
Write-Host "Provider execution default: disabled"
Write-Host "Patch application: disabled"

if (-not $SkipMemoryInventory) {
    Invoke-RepoPython -Label "Agent memory inventory" -ArgsList @(
        "-m", "Tools.ai", "build_agent_memory_inventory",
        "--repo-root", ".",
        "--objective", $Objective,
        "--output", $MemoryInventoryJson,
        "--markdown-output", $MemoryInventoryMd
    )
} else {
    [void]$Warnings.Add("Memory inventory skipped by request.")
}

Invoke-RepoPython -Label "Agnostic tool inventory" -ArgsList @(
    "-m", "Tools.ai", "build_agent_agnostic_tool_inventory",
    "--repo-root", ".",
    "--output", $ToolInventoryJson,
    "--markdown-output", $ToolInventoryMd
)

Invoke-RepoPython -Label "Persistent memory status" -ArgsList @(
    "-m", "Tools.ai", "agent_runtime_sqlite_memory",
    "--repo-root", ".",
    "--action", "status",
    "--scope", "persistent",
    "--output", $PersistentStatusJson,
    "--markdown-output", $PersistentStatusMd
)

Invoke-RepoPython -Label "Operational memory status" -ArgsList @(
    "-m", "Tools.ai", "agent_runtime_sqlite_memory",
    "--repo-root", ".",
    "--action", "status",
    "--scope", "operational",
    "--output", $OperationalStatusJson,
    "--markdown-output", $OperationalStatusMd
)

Invoke-RepoPython -Label "Python line-count CSV regeneration" -ArgsList @(
    "-m", "Tools.validation", "build_python_line_count_csv",
    "--repo-root", ".",
    "--csv-output", $LineCountCsv,
    "--report-output", $LineCountJson,
    "--markdown-output", $LineCountMd
)

$LineCountReport = Read-JsonOrNull $LineCountJson
if ($null -ne $LineCountReport -and $LineCountReport.csv_written) {
    $LineCountCsv = $LineCountReport.csv_written
}

if (Test-Path $LineCountCsv) {
    Invoke-RepoPython -Label "Full Python line-count Markdown inventory" -ArgsList @(
        "-m", "Tools.validation.build_full_python_line_count_markdown",
        "--repo-root", ".",
        "--stamp", $Stamp,
        "--csv", $LineCountCsv,
        "--output", $LineCountAllMd,
        "--report-output", ".\$ValidationDir\ai_cycle_startup_${Stamp}_full_python_line_count_markdown.json"
    )
} else {
    [void]$Errors.Add("Line-count CSV was not created: $LineCountCsv")
}

if (-not $SkipCodeInterpreter) {
    Invoke-RepoPython -Label "Code interpreter/static report" -ArgsList @(
        "-m", "Tools.ai.build_code_interpreter_report",
        "--repo-root", ".",
        "--input", "Tools/ai",
        "--input", "Tools/validation",
        "--input", "Tools/workflow",
        "--input", "Tools/npu",
        "--output", $CodeInterpreterJson,
        "--markdown-output", $CodeInterpreterMd
    )
} else {
    [void]$Warnings.Add("Code interpreter report skipped by request.")
}

Invoke-RepoPython -Label "Python syntax validation" -ArgsList @(
    "-m", "Tools.validation.check_python_syntax",
    "--repo-root", ".",
    "--output", $PythonSyntaxJson
)

if (-not $SkipGpuContractSmoke) {
    Invoke-RepoPython -Label "GPU planner JSON contract smoke" -ArgsList @(
        "-m", "Tools.validation", "run_gpu_planner_json_contract_smoke",
        "--repo-root", ".",
        "--output", $GpuContractJson,
        "--markdown-output", $GpuContractMd
    )
} else {
    [void]$Warnings.Add("GPU contract smoke skipped by request.")
}

if (-not $SkipSharedToolboxBundleSmoke) {
    Invoke-RepoPython -Label "Shared toolbox bundle smoke" -ArgsList @(
        "-m", "Tools.validation", "run_shared_toolbox_ai_to_ai_bundle_smoke",
        "--repo-root", ".",
        "--output", $SharedBundleSmokeJson,
        "--markdown-output", $SharedBundleSmokeMd
    )
} else {
    [void]$Warnings.Add("Shared toolbox bundle smoke skipped by request.")
}

Invoke-RepoPython -Label "Memory routing policy" -ArgsList @(
    "-m", "Tools.ai", "agent_memory_routing_policy",
    "--repo-root", ".",
    "--objective", $Objective,
    "--profile", "full_refactor",
    "--output", $MemoryRoutingJson,
    "--markdown-output", $MemoryRoutingMd
)

if ($EnableNpuProviderEnvironmentCheck) {
    Invoke-RepoPython -Label "NPU provider environment preflight" -ArgsList @(
        "-m", "Tools.ai", "check_npu_provider_environment",
        "--repo-root", ".",
        "--output", $NpuEnvJson,
        "--markdown-output", $NpuEnvMd
    )
} else {
    [void]$Warnings.Add("NPU provider environment preflight skipped; pass -EnableNpuProviderEnvironmentCheck to run it.")
}

if (-not $SkipRefactorDuplicationAudit) {
    $DupArgs = @(
        "-m", "Tools.ai", "build_refactor_duplication_audit",
        "--repo-root", ".",
        "--stamp", $Stamp,
        "--line-count-report", $LineCountJson,
        "--python-syntax-report", $PythonSyntaxJson,
        "--memory-routing-report", $MemoryRoutingJson,
        "--output", $DupAuditJson,
        "--markdown-output", $DupAuditMd
    )
    if (Test-Path $CodeInterpreterJson) { $DupArgs += @("--code-interpreter-report", $CodeInterpreterJson) }
    if (Test-Path $SharedBundleSmokeJson) { $DupArgs += @("--bundle-smoke-report", $SharedBundleSmokeJson) }
    foreach ($Path in $InputAuditReport) {
        if (Test-Path $Path) {
            $DupArgs += @("--input-audit-report", $Path)
        } else {
            [void]$Warnings.Add("Input audit report missing: $Path")
        }
    }
    Invoke-RepoPython -Label "Refactor duplication audit" -ArgsList $DupArgs
} else {
    [void]$Warnings.Add("Refactor duplication audit skipped by request.")
}

foreach ($Path in @(
    $MemoryInventoryJson, $ToolInventoryJson, $PersistentStatusJson, $OperationalStatusJson,
    $LineCountJson, $CodeInterpreterJson, $PythonSyntaxJson, $GpuContractJson,
    $SharedBundleSmokeJson, $MemoryRoutingJson, $NpuEnvJson, $DupAuditJson
)) {
    Add-ExistingPath -List $Reports -Path $Path
}
foreach ($Path in $InputAuditReport) { Add-ExistingPath -List $Reports -Path $Path }
foreach ($Path in $ExtraReport) { Add-ExistingPath -List $Reports -Path $Path }

foreach ($Path in @(
    ".\Tools\workflow\run_ai_cycle_startup_preflight.ps1",
    ".\docs\LOCAL_AI_TASKS\shared-toolbox-refactor-duplication-audit-next-task-2026-05-03.md",
    $MemoryInventoryMd, $ToolInventoryMd, $PersistentStatusMd, $OperationalStatusMd,
    $LineCountMd, $LineCountCsv, $LineCountAllMd, $CodeInterpreterMd,
    $GpuContractMd, $SharedBundleSmokeMd, $MemoryRoutingMd, $NpuEnvMd, $DupAuditMd
)) {
    Add-ExistingPath -List $Artifacts -Path $Path
}
foreach ($Path in $InputAuditReport) { Add-ExistingPath -List $Artifacts -Path $Path }
foreach ($Path in $ExtraArtifact) { Add-ExistingPath -List $Artifacts -Path $Path }

foreach ($Path in $Reports) {
    $Data = Read-JsonOrNull $Path
    if ($null -eq $Data) {
        [void]$Warnings.Add("Report could not be parsed: $Path")
        continue
    }
    if ($null -ne $Data.passed -and $Data.passed -eq $false) {
        [void]$Errors.Add("Report failed: $Path")
    }
    if ($Data.patch_application_performed -eq $true) { [void]$Errors.Add("patch_application_performed=True in $Path") }
    if ($Data.sqlite_write_performed -eq $true) { [void]$Errors.Add("sqlite_write_performed=True in $Path") }
    if ($Data.persistent_memory_write_performed -eq $true) { [void]$Errors.Add("persistent_memory_write_performed=True in $Path") }
}

$WorkflowPassed = ($Errors.Count -eq 0)
$WorkflowReport = [ordered]@{
    schema_version = 1
    kind = "ai_cycle_startup_preflight_workflow"
    generated_at = (Get-Date).ToString("s")
    repo_root = "$RepoRootPath"
    stamp = $Stamp
    objective = $Objective
    passed = $WorkflowPassed
    errors = @($Errors)
    warnings = @($Warnings)
    provider_execution_performed = $false
    patch_application_performed = $false
    source_writes_performed = $false
    sqlite_write_performed = $false
    persistent_memory_write_performed = $false
    blender_runtime_execution_performed = $false
    report_count = $Reports.Count
    artifact_count = $Artifacts.Count
    line_count_csv = $LineCountCsv
    line_count_all_markdown = $LineCountAllMd
    input_audit_reports = @($InputAuditReport)
    extra_reports = @($ExtraReport)
    extra_artifacts = @($ExtraArtifact)
    reports = @($Reports)
    artifacts = @($Artifacts)
    compact_bundle_requested = [bool]$WriteCompactBundle
    bundle_json = $null
    bundle_markdown = $null
    guardrails = [ordered]@{
        report_only_by_default = $true
        provider_execution_default = "disabled"
        patch_application_performed = $false
        sqlite_write_performed = $false
        persistent_memory_write_performed = $false
        blender_runtime_touched = $false
        git_write_performed = $false
        output_commit_allowed = $false
    }
}

$WorkflowReport | ConvertTo-Json -Depth 10 | Set-Content -Path $WorkflowJson -Encoding UTF8
$ReportLines = @($Reports | ForEach-Object { "- ``$_``" })
$ArtifactLines = @($Artifacts | ForEach-Object { "- ``$_``" })
$WorkflowMarkdown = @(
    "# IA-Carmine AI Cycle Startup Preflight",
    "",
    "- Passed: ``$WorkflowPassed``",
    "- Stamp: ``$Stamp``",
    "- Objective: ``$Objective``",
    "- Report count: ``$($Reports.Count)``",
    "- Artifact count: ``$($Artifacts.Count)``",
    "- Line-count CSV: ``$LineCountCsv``",
    "- Full line-count Markdown: ``$LineCountAllMd``",
    "- Provider execution performed: ``False``",
    "- Patch application performed: ``False``",
    "- SQLite write performed: ``False``",
    "- Persistent memory write performed: ``False``",
    "",
    "## Reports",
    ""
) + $ReportLines + @(
    "",
    "## Artifacts",
    ""
) + $ArtifactLines
$WorkflowMarkdown | Set-Content -Path $WorkflowMd -Encoding UTF8
Add-ExistingPath -List $Reports -Path $WorkflowJson
Add-ExistingPath -List $Artifacts -Path $WorkflowMd

if ($WriteCompactBundle) {
    $BundleArgs = @(
        "-m", "Tools.ai.build_shared_toolbox_ai_to_ai_bundle",
        "--repo-root", ".",
        "--stamp", $Stamp,
        "--basename", $BundleBase,
        "--output-dir", $EvidencePath,
        "--validate-bundle",
        "--max-included-artifact-chars", "$MaxIncludedArtifactChars",
        "--max-included-artifacts", "$MaxIncludedArtifacts"
    )
    foreach ($Report in $Reports) {
        $BundleArgs += @("--report", [string]$Report)
    }
    foreach ($Artifact in $Artifacts) {
        $BundleArgs += @("--artifact", [string]$Artifact)
    }
    Invoke-RepoPython -Label "Startup compact evidence bundle" -ArgsList $BundleArgs
    if (Test-Path $BundleJson) { $WorkflowReport.bundle_json = $BundleJson }
    if (Test-Path $BundleMd) { $WorkflowReport.bundle_markdown = $BundleMd }
    $WorkflowReport | ConvertTo-Json -Depth 10 | Set-Content -Path $WorkflowJson -Encoding UTF8
}

Write-Host ""
Write-Host "Generated startup/preflight summary:"
Write-Host "  $WorkflowJson"
Write-Host "  $WorkflowMd"
Write-Host "  line_count_csv=$LineCountCsv"
Write-Host "  line_count_all_markdown=$LineCountAllMd"
if (Test-Path $BundleJson) { Write-Host "  $BundleJson" }
if (Test-Path $BundleMd) { Write-Host "  $BundleMd" }
Write-Host ""
Write-Host "Git policy: do not commit output/**, *.db, *.sqlite or renders/**. Commit only selected compact evidence under docs/LOCAL_VALIDATION_EVIDENCE when explicitly needed."
