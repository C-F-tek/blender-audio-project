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
    [string]$Model = "",
    [int]$MaxContextChars = 6000
)

$ErrorActionPreference = "Stop"

$RepoRootPath = Resolve-Path $RepoRoot
Set-Location $RepoRootPath

Write-Host "=== Build post-validation AI work packet ==="
Write-Host "Repo: $RepoRootPath"
Write-Host "Profile: $Profile"
Write-Host "OutputDir: $OutputDir"
Write-Host "Basename: $Basename"
Write-Host "ProposalBasename: $ProposalBasename"

$QualityReport = "output/validation/ai_workload_report_quality.json"
$LaneRoutingReport = "output/validation/ai_workload_quality_lane_routing.json"
$LaneRoutingMarkdown = "output/validation/ai_workload_quality_lane_routing.md"
$NpuDecodeRemediationReport = "output/validation/npu_decode_quality_remediation.json"

if (Test-Path $QualityReport) {
    Write-Host ""
    Write-Host "=== Build workload quality lane routing report ==="
    $RoutingArgs = @(
        ".\Tools\ai\build_workload_quality_lane_routing.py",
        "--repo-root", ".",
        "--quality-report", $QualityReport,
        "--output", $LaneRoutingReport,
        "--markdown-output", $LaneRoutingMarkdown
    )
    foreach ($Path in $ContextFile) {
        $RoutingArgs += @("--context-file", $Path)
    }
    python @RoutingArgs

    Write-Host ""
    Write-Host "=== Build NPU decode remediation report ==="
    python .\Tools\validation\check_npu_decode_quality_remediation.py `
        --repo-root . `
        --quality-report $QualityReport `
        --output $NpuDecodeRemediationReport
} else {
    Write-Host ""
    Write-Warning "Skipping workload quality routing/remediation: $QualityReport not found."
}

$ArgsList = @(
    ".\Tools\ai\suggest_repository_updates.py",
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

if ($UseOllama) {
    $ArgsList += "--use-ollama"
}

if ($Model -ne "") {
    $ArgsList += @("--model", $Model)
}

python @ArgsList

$ProposalArgs = @(
    ".\Tools\ai\build_repository_change_proposals.py",
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

python @ProposalArgs

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
Write-Host "These reports are advisory only. Review before applying changes."
