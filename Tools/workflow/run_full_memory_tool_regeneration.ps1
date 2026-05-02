param(
    [string]$RepoRoot = ".",
    [ValidateSet("basic", "refactor", "full_refactor")]
    [string]$Profile = "full_refactor",
    [string]$Objective = "Regenerate IA-Carmine memory, runtime tools and context from current repository state.",
    [string]$Stamp = "",
    [string]$OutputRoot = "output",
    [string]$EvidenceDir = "docs/LOCAL_VALIDATION_EVIDENCE",
    [switch]$ClearOperational,
    [switch]$SkipBroker,
    [switch]$SkipCodeInterpreter,
    [switch]$SkipBundle,
    [int]$TimeoutSeconds = 300,
    [int]$MaxIncludedArtifactChars = 16000,
    [int]$MaxIncludedArtifacts = 24
)

$ErrorActionPreference = "Stop"
$RepoRootPath = Resolve-Path $RepoRoot
Set-Location $RepoRootPath

if ($Stamp -eq "") {
    $Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
}

$env:PYTHONPATH = (Get-Location).Path

$AiPipelineDir = Join-Path $OutputRoot "ai_pipeline"
$ValidationDir = Join-Path $OutputRoot "validation"
$AnalysisDir = Join-Path $OutputRoot "analysis"
$RuntimeToolDir = Join-Path $OutputRoot "ai_runtime_tools"
$RunToolDir = Join-Path $RuntimeToolDir "full_memory_tool_regeneration_$Stamp"

New-Item -ItemType Directory -Force -Path $AiPipelineDir, $ValidationDir, $AnalysisDir, $RuntimeToolDir, $RunToolDir, $EvidenceDir | Out-Null

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

function Add-ExistingPath {
    param(
        [System.Collections.ArrayList]$List,
        [string]$Path
    )
    if (Test-Path $Path) {
        [void]$List.Add($Path)
    }
}

$Reports = [System.Collections.ArrayList]@()
$Artifacts = [System.Collections.ArrayList]@()

$MemoryInventoryJson = ".\$AiPipelineDir\full_memory_tool_regeneration_${Stamp}_agent_memory_inventory.json"
$MemoryInventoryMd = ".\$AiPipelineDir\full_memory_tool_regeneration_${Stamp}_agent_memory_inventory.md"
$ToolInventoryJson = ".\$AiPipelineDir\full_memory_tool_regeneration_${Stamp}_agnostic_tool_inventory.json"
$ToolInventoryMd = ".\$AiPipelineDir\full_memory_tool_regeneration_${Stamp}_agnostic_tool_inventory.md"
$PersistentStatusJson = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_persistent_memory_status.json"
$PersistentStatusMd = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_persistent_memory_status.md"
$OperationalStatusJson = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_operational_memory_status.json"
$OperationalStatusMd = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_operational_memory_status.md"
$PolicyJson = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_memory_routing_policy.json"
$PolicyMd = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_memory_routing_policy.md"
$BrokerRequest = ".\$RuntimeToolDir\full_memory_tool_regeneration_${Stamp}_tool_requests.json"
$BrokerJson = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_runtime_tool_broker.json"
$BrokerMd = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_runtime_tool_broker.md"
$TransientJson = ".\$AiPipelineDir\full_memory_tool_regeneration_${Stamp}_transient_request_context.json"
$TransientMd = ".\$AiPipelineDir\full_memory_tool_regeneration_${Stamp}_transient_request_context.md"
$LineCountCsv = ".\$EvidenceDir\full_memory_tool_regeneration_python_line_count_$Stamp.csv"
$LineCountJson = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_python_line_count.json"
$LineCountMd = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_python_line_count.md"
$CodeInterpreterJson = ".\$AnalysisDir\full_memory_tool_regeneration_${Stamp}_code_interpreter.json"
$CodeInterpreterMd = ".\$AnalysisDir\full_memory_tool_regeneration_${Stamp}_code_interpreter.md"
$PythonSyntaxJson = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_python_syntax.json"
$ValidationContractJson = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_validation_report_contract.json"
$BrokerSmokeJson = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_runtime_tool_broker_smoke.json"
$BrokerSmokeMd = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_runtime_tool_broker_smoke.md"
$PolicySmokeJson = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_memory_routing_policy_smoke.json"
$PolicySmokeMd = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_memory_routing_policy_smoke.md"
$WorkflowJson = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_workflow.json"
$WorkflowMd = ".\$ValidationDir\full_memory_tool_regeneration_${Stamp}_workflow.md"
$BundleBase = "full_memory_tool_regeneration_bundle_$Stamp"
$BundleJson = ".\$EvidenceDir\$BundleBase.json"
$BundleMd = ".\$EvidenceDir\$BundleBase.md"

Write-Host "=== Full memory/tool regeneration ==="
Write-Host "Repo: $RepoRootPath"
Write-Host "Stamp: $Stamp"
Write-Host "Profile: $Profile"
Write-Host "Objective: $Objective"

Invoke-RepoPython -Label "Persistent memory inventory" -ArgsList @(
    ".\Tools\ai\build_agent_memory_inventory.py",
    "--repo-root", ".",
    "--objective", $Objective,
    "--output", $MemoryInventoryJson,
    "--markdown-output", $MemoryInventoryMd
)

Invoke-RepoPython -Label "Agnostic tool inventory" -ArgsList @(
    ".\Tools\ai\build_agent_agnostic_tool_inventory.py",
    "--repo-root", ".",
    "--output", $ToolInventoryJson,
    "--markdown-output", $ToolInventoryMd
)

Invoke-RepoPython -Label "Persistent SQLite memory status" -ArgsList @(
    ".\Tools\ai\agent_runtime_sqlite_memory.py",
    "--repo-root", ".",
    "--action", "status",
    "--scope", "persistent",
    "--output", $PersistentStatusJson,
    "--markdown-output", $PersistentStatusMd
)

Invoke-RepoPython -Label "Operational SQLite memory status" -ArgsList @(
    ".\Tools\ai\agent_runtime_sqlite_memory.py",
    "--repo-root", ".",
    "--action", "status",
    "--scope", "operational",
    "--output", $OperationalStatusJson,
    "--markdown-output", $OperationalStatusMd
)

$PolicyArgs = @(
    ".\Tools\ai\agent_memory_routing_policy.py",
    "--repo-root", ".",
    "--objective", $Objective,
    "--profile", $Profile,
    "--remember-note", "Full regeneration cycle: runtime broker, operational memory and transient context are available.",
    "--promotion-candidate", "Runtime broker and memory routing may be stable workflow primitives after evidence review.",
    "--broker-request-output", $BrokerRequest,
    "--output", $PolicyJson,
    "--markdown-output", $PolicyMd
)
if ($ClearOperational) {
    $PolicyArgs += "--clear-operational"
}
Invoke-RepoPython -Label "Memory routing policy" -ArgsList $PolicyArgs

if (-not $SkipBroker) {
    Invoke-RepoPython -Label "Runtime tool broker" -ArgsList @(
        ".\Tools\ai\agent_runtime_tool_broker.py",
        "--repo-root", ".",
        "--request-file", $BrokerRequest,
        "--tool-output-dir", ".\$RunToolDir",
        "--timeout-seconds", "$TimeoutSeconds",
        "--output", $BrokerJson,
        "--markdown-output", $BrokerMd
    )
} else {
    Write-Warning "Skipping broker execution by request."
}

$TransientArgs = @(
    ".\Tools\ai\build_agent_transient_request_context.py",
    "--repo-root", ".",
    "--objective", "Full memory/tool regeneration context for IA-Carmine.",
    "--memory-note", "Persistent memory is read-only. Operational memory is scratch. Runtime tools are brokered by allowlist.",
    "--report-file", $MemoryInventoryJson,
    "--report-file", $ToolInventoryJson,
    "--report-file", $PersistentStatusJson,
    "--report-file", $OperationalStatusJson,
    "--report-file", $PolicyJson,
    "--output", $TransientJson,
    "--markdown-output", $TransientMd
)
if ((Test-Path $BrokerJson) -and (-not $SkipBroker)) {
    $TransientArgs += @("--report-file", $BrokerJson)
}
Invoke-RepoPython -Label "Transient request context" -ArgsList $TransientArgs

Invoke-RepoPython -Label "Full Python line-count inventory" -ArgsList @(
    ".\Tools\validation\build_python_line_count_csv.py",
    "--repo-root", ".",
    "--csv-output", $LineCountCsv,
    "--report-output", $LineCountJson,
    "--markdown-output", $LineCountMd
)

if (-not $SkipCodeInterpreter) {
    Invoke-RepoPython -Label "Code interpreter/static report" -ArgsList @(
        ".\Tools\ai\build_code_interpreter_report.py",
        "--repo-root", ".",
        "--input", "Tools/ai",
        "--input", "Tools/validation",
        "--input", "Tools/workflow",
        "--input", "Tools/npu",
        "--output", $CodeInterpreterJson,
        "--markdown-output", $CodeInterpreterMd
    )
} else {
    Write-Warning "Skipping code interpreter report by request."
}

Invoke-RepoPython -Label "Python syntax validation" -ArgsList @(
    ".\Tools\validation\check_python_syntax.py",
    "--repo-root", ".",
    "--output", $PythonSyntaxJson
)

$ContractArgs = @(
    ".\Tools\validation\check_validation_report_contract.py",
    "--repo-root", ".",
    "--output", $ValidationContractJson
)
foreach ($Path in @(
    $MemoryInventoryJson,
    $ToolInventoryJson,
    $PersistentStatusJson,
    $OperationalStatusJson,
    $PolicyJson,
    $BrokerJson,
    $TransientJson,
    $LineCountJson,
    $CodeInterpreterJson,
    $PythonSyntaxJson
)) {
    if (Test-Path $Path) {
        $ContractArgs += @("--report-file", $Path)
    }
}
Invoke-RepoPython -Label "Validation report contract" -ArgsList $ContractArgs

Invoke-RepoPython -Label "Runtime broker smoke" -ArgsList @(
    ".\Tools\validation\run_agent_runtime_tool_broker_smoke.py",
    "--repo-root", ".",
    "--output", $BrokerSmokeJson,
    "--markdown-output", $BrokerSmokeMd
)

Invoke-RepoPython -Label "Memory routing policy smoke" -ArgsList @(
    ".\Tools\validation\run_agent_memory_routing_policy_smoke.py",
    "--repo-root", ".",
    "--output", $PolicySmokeJson,
    "--markdown-output", $PolicySmokeMd
)

foreach ($Path in @(
    $MemoryInventoryJson, $ToolInventoryJson, $PersistentStatusJson, $OperationalStatusJson,
    $PolicyJson, $BrokerJson, $TransientJson, $LineCountJson, $CodeInterpreterJson,
    $PythonSyntaxJson, $ValidationContractJson, $BrokerSmokeJson, $PolicySmokeJson
)) {
    Add-ExistingPath -List $Reports -Path $Path
}

foreach ($Path in @(
    ".\docs\LOCAL_AI_TASKS\full-memory-tool-regeneration-procedure.md",
    ".\Tools\workflow\run_full_memory_tool_regeneration.ps1",
    $MemoryInventoryMd, $ToolInventoryMd, $PersistentStatusMd, $OperationalStatusMd,
    $PolicyMd, $BrokerMd, $TransientMd, $LineCountMd, $LineCountCsv,
    $CodeInterpreterMd, $BrokerSmokeMd, $PolicySmokeMd
)) {
    Add-ExistingPath -List $Artifacts -Path $Path
}

$WorkflowErrors = @()
foreach ($Path in $Reports) {
    try {
        $Data = Get-Content $Path -Raw | ConvertFrom-Json
        if ($null -ne $Data.passed -and $Data.passed -eq $false) {
            $WorkflowErrors += "${Path}: passed=false"
        }
    } catch {
        $WorkflowErrors += "${Path}: failed to parse workflow report input: $($_.Exception.Message)"
    }
}
$WorkflowPassed = ($WorkflowErrors.Count -eq 0)

$WorkflowReport = [ordered]@{
    schema_version = 1
    kind = "full_memory_tool_regeneration_workflow"
    generated_at = (Get-Date).ToString("s")
    repo_root = "$RepoRootPath"
    stamp = $Stamp
    profile = $Profile
    objective = $Objective
    passed = $WorkflowPassed
    errors = @($WorkflowErrors)
    warnings = @()
    provider_execution_performed = $false
    patch_application_performed = $false
    source_writes_performed = $false
    sqlite_write_performed = $false
    persistent_memory_write_performed = $false
    operational_sqlite_write_allowed_under_output = $true
    report_count = $Reports.Count
    artifact_count = $Artifacts.Count
    reports = @($Reports)
    artifacts = @($Artifacts)
    bundle_json = $null
    bundle_markdown = $null
    guardrails = [ordered]@{
        provider_execution_performed = $false
        patch_application_performed = $false
        sqlite_write_performed = $false
        persistent_memory_write_performed = $false
        operational_memory_allowed_under_output = $true
        blender_runtime_touched = $false
        git_write_performed = $false
        manual_review_required_for_persistent_promotion = $true
    }
}

$WorkflowReport | ConvertTo-Json -Depth 8 | Set-Content -Path $WorkflowJson -Encoding UTF8

$ReportLines = @($Reports | ForEach-Object { "- ``$_``" })
$ArtifactLines = @($Artifacts | ForEach-Object { "- ``$_``" })
$WorkflowMarkdown = @(
    "# Full Memory / Tool Regeneration Workflow",
    "",
    "- Passed: ``$WorkflowPassed``",
    "- Stamp: ``$Stamp``",
    "- Profile: ``$Profile``",
    "- Report count: ``$($Reports.Count)``",
    "- Artifact count: ``$($Artifacts.Count)``",
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

if (-not $SkipBundle) {
    $BundleArgs = @(
        "-m", "Tools.ai.build_github_evidence_bundle",
        "--repo-root", ".",
        "--basename", $BundleBase,
        "--output-dir", $EvidenceDir,
        "--report", (($Reports | ForEach-Object { [string]$_ }) -join ",")
    )
    foreach ($Artifact in $Artifacts) {
        $BundleArgs += @("--artifact", [string]$Artifact)
    }
    $BundleArgs += @(
        "--max-included-artifact-chars", "$MaxIncludedArtifactChars",
        "--max-included-artifacts", "$MaxIncludedArtifacts"
    )
    Invoke-RepoPython -Label "Compact evidence bundle" -ArgsList $BundleArgs

    if (Test-Path $BundleJson) {
        $WorkflowReport.bundle_json = $BundleJson
    }
    if (Test-Path $BundleMd) {
        $WorkflowReport.bundle_markdown = $BundleMd
    }
    $WorkflowReport | ConvertTo-Json -Depth 8 | Set-Content -Path $WorkflowJson -Encoding UTF8
} else {
    Write-Warning "Skipping compact bundle by request."
}

Write-Host ""
Write-Host "Generated workflow summary:"
Write-Host "  $WorkflowJson"
Write-Host "  $WorkflowMd"
if (Test-Path $BundleJson) { Write-Host "  $BundleJson" }
if (Test-Path $BundleMd) { Write-Host "  $BundleMd" }
Write-Host ""
Write-Host "Git policy: commit only compact evidence under docs/LOCAL_VALIDATION_EVIDENCE if needed; do not commit output/**, *.db or *.sqlite."
