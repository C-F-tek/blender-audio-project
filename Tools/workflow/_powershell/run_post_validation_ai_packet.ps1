param(
    [string]$RepoRoot = ".",
    [ValidateSet("core", "npu", "docs")]
    [string]$Profile = "core",
    [string]$OutputDir = "output/ai_pipeline",
    [string]$Basename = "repository_update_suggestions",
    [string]$ProposalBasename = "repository_change_proposals",
    [string[]]$ContextFile = @(),
    [string[]]$ReportFile = @(),
    [switch]$UseOllama,
    [switch]$UsePrimaryAdvisoryProvider,
    [switch]$RequireConcreteProposals,
    [string]$Model = "",
    [int]$MaxContextChars = 6000
)

$ErrorActionPreference = "Stop"

$PythonEnvScript = Join-Path $PSScriptRoot "python_env.ps1"
. $PythonEnvScript
$RepoRootPath = Resolve-Path $RepoRoot
Set-Location $RepoRootPath
$PacketPythonExe = Use-WorkflowPython -RepoRoot $RepoRootPath

Write-Host "=== Build post-validation AI work packet ==="
Write-Host "Repo: $RepoRootPath"
Write-Host "Python: $PacketPythonExe"
Write-Host "Profile: $Profile"
Write-Host "OutputDir: $OutputDir"
Write-Host "Basename: $Basename"
Write-Host "ProposalBasename: $ProposalBasename"

$QualityReport = "output/validation/ai_workload_report_quality.json"
$LaneRoutingReport = "output/validation/ai_workload_quality_lane_routing.json"
$LaneRoutingMarkdown = "output/validation/ai_workload_quality_lane_routing.md"
$NpuDecodeRemediationReport = "output/validation/npu_decode_quality_remediation.json"
$UseResolvedOllama = [bool]$UseOllama
$PrimaryAdvisoryProvider = "none"
$PrimaryAdvisoryComputeLane = "none"

if (Test-Path $QualityReport) {
    Write-Host ""
    Write-Host "=== Build workload quality lane routing report ==="
    $RoutingArgs = @(
        "-m", "ia_carmine.cli", "build_workload_quality_lane_routing",
        "--repo-root", ".",
        "--quality-report", $QualityReport,
        "--output", $LaneRoutingReport,
        "--markdown-output", $LaneRoutingMarkdown
    )
    foreach ($Path in $ContextFile) {
        $RoutingArgs += @("--context-file", $Path)
    }
    & $PacketPythonExe @RoutingArgs

    if (Test-Path $LaneRoutingReport) {
        $RoutingJson = Get-Content $LaneRoutingReport -Raw | ConvertFrom-Json
        if ($null -ne $RoutingJson.primary_advisory_provider) {
            $PrimaryAdvisoryProvider = [string]$RoutingJson.primary_advisory_provider.provider
            $PrimaryAdvisoryComputeLane = [string]$RoutingJson.primary_advisory_provider.compute_lane
            if ([string]::IsNullOrWhiteSpace($PrimaryAdvisoryProvider)) {
                $PrimaryAdvisoryProvider = "none"
            }
            if ([string]::IsNullOrWhiteSpace($PrimaryAdvisoryComputeLane)) {
                $PrimaryAdvisoryComputeLane = "none"
            }
        }
        if ($UsePrimaryAdvisoryProvider) {
            if ($PrimaryAdvisoryProvider -eq "ollama" -and $PrimaryAdvisoryComputeLane -eq "gpu_cuda") {
                $UseResolvedOllama = $true
                Write-Host "Primary advisory provider enabled: ollama on gpu_cuda"
            } else {
                Write-Warning "Primary advisory provider was requested, but no usable Ollama/GPU lane is available. Provider execution remains disabled."
            }
        }
    }

    Write-Host ""
    Write-Host "=== Build NPU decode remediation report ==="
    & $PacketPythonExe -m Tools.validation check_npu_decode_quality_remediation `
        --repo-root . `
        --quality-report $QualityReport `
        --output $NpuDecodeRemediationReport
} else {
    Write-Host ""
    Write-Warning "Skipping workload quality routing/remediation: $QualityReport not found."
    if ($UsePrimaryAdvisoryProvider) {
        Write-Warning "Primary advisory provider was requested, but quality routing is unavailable. Provider execution remains disabled."
    }
}

$ArgsList = @(
    "-m", "ia_carmine.cli", "suggest_repository_updates",
    "--repo-root", ".",
    "--profile", $Profile,
    "--output-dir", $OutputDir,
    "--basename", $Basename,
    "--max-context-chars", "$MaxContextChars"
)

foreach ($Path in $ContextFile) {
    $ArgsList += @("--context-file", $Path)
}

foreach ($Path in $ReportFile) {
    $ArgsList += @("--report-file", $Path)
}

if (Test-Path $LaneRoutingReport) {
    $ArgsList += @("--report-file", $LaneRoutingReport)
}

if (Test-Path $NpuDecodeRemediationReport) {
    $ArgsList += @("--report-file", $NpuDecodeRemediationReport)
}

if ($UseResolvedOllama) {
    $ArgsList += "--use-ollama"
}

if ($Model -ne "") {
    $ArgsList += @("--model", $Model)
}

& $PacketPythonExe @ArgsList

$ProposalArgs = @(
    "-m", "ia_carmine.cli", "build_repository_change_proposals",
    "--repo-root", ".",
    "--profile", $Profile,
    "--output-dir", $OutputDir,
    "--basename", $ProposalBasename
)

foreach ($Path in $ReportFile) {
    $ProposalArgs += @("--report-file", $Path)
}

if (Test-Path $LaneRoutingReport) {
    $ProposalArgs += @("--report-file", $LaneRoutingReport)
}

if (Test-Path $NpuDecodeRemediationReport) {
    $ProposalArgs += @("--report-file", $NpuDecodeRemediationReport)
}

if ($RequireConcreteProposals) {
    $ProposalArgs += "--require-concrete-proposals"
}

& $PacketPythonExe @ProposalArgs

Write-Host ""
Write-Host "Generated:"
Write-Host "  $OutputDir\$Basename.json"
Write-Host "  $OutputDir\$Basename.md"
Write-Host "  $OutputDir\${Basename}_manifest.json"
Write-Host "  $OutputDir\$ProposalBasename.json"
Write-Host "  $OutputDir\$ProposalBasename.md"
if (Test-Path $LaneRoutingReport) {
    Write-Host "  $LaneRoutingReport"
    Write-Host "  $LaneRoutingMarkdown"
}
if (Test-Path $NpuDecodeRemediationReport) {
    Write-Host "  $NpuDecodeRemediationReport"
}
Write-Host ""
Write-Host "Primary advisory provider: $PrimaryAdvisoryProvider / $PrimaryAdvisoryComputeLane"
Write-Host "Primary advisory provider execution requested: $UsePrimaryAdvisoryProvider"
Write-Host "Concrete repository proposals required: $RequireConcreteProposals"
Write-Host "Ollama advisory execution used: $UseResolvedOllama"
Write-Host "These reports are advisory only. Review before applying changes."
