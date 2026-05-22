param(
    [string]$RepoRoot = ".",
    [ValidateSet("core", "npu", "docs")]
    [string]$Profile = "npu",
    [string]$OutputDir = "output/ai_packets",
    [string]$Basename = "parallel_gpu_npu_multistep",
    [string]$ProposalBasename = "parallel_gpu_npu_multistep_proposals",
    [string]$EvidenceBasename = "parallel_gpu_npu_multistep_evidence",
    [string[]]$ContextFile = @(
        "output/ai_packets/npu_real_workload_report.md",
        "output/ai_packets/ollama_gpu_real_workload_report.md"
    ),
    [string[]]$ReportFile = @(
        "output/validation/ai_workload_report_quality.json",
        "output/validation/local_ai_resource_lanes.json",
        "output/validation/provider_result_report.json",
        "output/validation/local_provider_probe.json",
        "output/validation/npu_runtime_output_manifest.json"
    ),
    [switch]$RunOllamaProbe,
    [switch]$RunNpuProbe,
    [switch]$UsePrimaryAdvisoryProvider,
    [string]$Model = "",
    [string]$PythonExe = "",
    [string]$NpuPythonExe = "",
    [int]$MaxContextChars = 6000
)

$ErrorActionPreference = "Stop"

$PythonEnvScript = Join-Path $PSScriptRoot "python_env.ps1"
. $PythonEnvScript
$RepoRootPath = Resolve-Path $RepoRoot
Set-Location $RepoRootPath
if (-not [string]::IsNullOrWhiteSpace($PythonExe)) {
    $ProviderPythonExe = (Resolve-Path -LiteralPath $PythonExe).Path
} else {
    $ProviderPythonExe = Use-WorkflowPython -RepoRoot $RepoRootPath
}
if ([string]::IsNullOrWhiteSpace($NpuPythonExe)) {
    $NpuPythonExe = $env:SPAZIOTEMPO_NPU_PYTHON
}
$ResolvedNpuPythonExe = $NpuPythonExe
$env:IA_CARMINE_PYTHON = $ProviderPythonExe
$env:PYTHONPATH = [string]$RepoRootPath
if (Test-Path -LiteralPath $ProviderPythonExe -PathType Leaf) {
    $env:PATH = (Split-Path -Parent $ProviderPythonExe) + [System.IO.Path]::PathSeparator + $env:PATH
}

Write-Host "=== Parallel GPU/NPU multistep AI workflow ==="
Write-Host "Repo: $RepoRootPath"
Write-Host "Python: $ProviderPythonExe"
Write-Host "Profile: $Profile"
Write-Host "Basename: $Basename"
Write-Host "GPU/Ollama probe: $RunOllamaProbe"
Write-Host "NPU/OpenVINO probe: $RunNpuProbe"
Write-Host "Primary advisory provider: $UsePrimaryAdvisoryProvider"

$QualityReport = "output/validation/ai_workload_report_quality.json"
$LaneRoutingReport = "output/validation/ai_workload_quality_lane_routing.json"
$LaneRoutingMarkdown = "output/validation/ai_workload_quality_lane_routing.md"
$NpuDecodeRemediationReport = "output/validation/npu_decode_quality_remediation.json"
$LocalProviderProbeReport = "output/validation/local_provider_probe.json"

Write-Host ""
Write-Host "=== Step 1: workload quality gate ==="
& $ProviderPythonExe -m Tools.validation check_ai_workload_report_quality `
    --repo-root . `
    --output $QualityReport

Write-Host ""
Write-Host "=== Step 2: parallel provider probes ==="
# Provider probe background jobs disabled here: provider probe arguments must remain argv-safe.
if ($RunOllamaProbe -or $RunNpuProbe) {
    $ProbeArgs = @(
        "-m", "ia_carmine.cli", "run_local_provider_probe",
        "--repo-root", ".",
        "--output", $LocalProviderProbeReport
    )
    if ($RunOllamaProbe) {
        $ProbeArgs += "--run-ollama"
    }
    if ($RunNpuProbe) {
        $ProbeArgs += "--run-npu"
    }
    if ($Model -ne "") {
        $ProbeArgs += @("--model", $Model)
    }
    if (-not [string]::IsNullOrWhiteSpace($ResolvedNpuPythonExe)) {
        $ProbeArgs += @("--npu-python-exe", $ResolvedNpuPythonExe)
    }
    & $ProviderPythonExe @ProbeArgs
    if ($LASTEXITCODE -ne 0) {
        throw "provider_probe failed with exit code $LASTEXITCODE"
    }
}

Write-Host ""
Write-Host "=== Step 3: quality-based routing and NPU remediation ==="
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
& $ProviderPythonExe @RoutingArgs

& $ProviderPythonExe -m Tools.validation check_npu_decode_quality_remediation `
    --repo-root . `
    --quality-report $QualityReport `
    --output $NpuDecodeRemediationReport

Write-Host ""
Write-Host "=== Step 4: primary advisory packet/proposals ==="
$PacketArgs = @(
    "-ExecutionPolicy", "Bypass",
    "-File", ".\Tools\workflow\run_post_validation_ai_packet.ps1",
    "-Profile", $Profile,
    "-OutputDir", $OutputDir,
    "-Basename", $Basename,
    "-ProposalBasename", $ProposalBasename,
    "-MaxContextChars", "$MaxContextChars"
)

if ($ContextFile.Count -gt 0) {
    $PacketArgs += @("-ContextFile", ($ContextFile -join ","))
}
if ($ReportFile.Count -gt 0) {
    $PacketArgs += @("-ReportFile", ($ReportFile -join ","))
}
if ($UsePrimaryAdvisoryProvider) {
    $PacketArgs += "-UsePrimaryAdvisoryProvider"
}
if ($Model -ne "") {
    $PacketArgs += @("-Model", $Model)
}
powershell.exe @PacketArgs

Write-Host ""
Write-Host "=== Step 5: GitHub evidence bundle ==="
& $ProviderPythonExe -m ia_carmine build_github_evidence_bundle `
    --repo-root . `
    --basename $EvidenceBasename

Write-Host ""
Write-Host "Generated compact pushable evidence:"
Write-Host "  docs/LOCAL_VALIDATION_EVIDENCE/$EvidenceBasename.json"
Write-Host "  docs/LOCAL_VALIDATION_EVIDENCE/$EvidenceBasename.md"
Write-Host ""
Write-Host "Push evidence with:"
Write-Host "  git add docs/LOCAL_VALIDATION_EVIDENCE/"
Write-Host "  git commit -m \"test: add parallel gpu npu multistep evidence\""
Write-Host "  git push"
