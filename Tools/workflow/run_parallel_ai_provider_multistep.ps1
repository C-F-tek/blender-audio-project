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
    [switch]$RunNpuDecodeSmoke,
    [switch]$UsePrimaryAdvisoryProvider,
    [string]$Model = "",
    [string]$PythonExe = "",
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
Write-Host "NPU decode smoke: $RunNpuDecodeSmoke"
Write-Host "Primary advisory provider: $UsePrimaryAdvisoryProvider"

$QualityReport = "output/validation/ai_workload_report_quality.json"
$LaneRoutingReport = "output/validation/ai_workload_quality_lane_routing.json"
$LaneRoutingMarkdown = "output/validation/ai_workload_quality_lane_routing.md"
$NpuDecodeRemediationReport = "output/validation/npu_decode_quality_remediation.json"
$NpuDecodeSmokeReport = "output/validation/npu_decode_smoke_diagnostic.json"
$LocalProviderProbeReport = "output/validation/local_provider_probe.json"

Write-Host ""
Write-Host "=== Step 1: workload quality gate ==="
& $ProviderPythonExe .\Tools\validation\check_ai_workload_report_quality.py `
    --repo-root . `
    --output $QualityReport

Write-Host ""
Write-Host "=== Step 2: parallel provider probes / diagnostics ==="
$Jobs = @()
if ($RunOllamaProbe -or $RunNpuProbe) {
    $ProbeArgs = @(
        ".\Tools\ai\run_local_provider_probe.py",
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
    $Jobs += Start-Job -Name "provider_probe" -ScriptBlock {
        param([string[]]$ArgsList, [string]$PythonExe, [string]$PythonPath)
        Set-Location $using:RepoRootPath
        $env:IA_CARMINE_PYTHON = $PythonExe
        $env:PYTHONPATH = $PythonPath
        if (Test-Path -LiteralPath $PythonExe -PathType Leaf) {
            $env:PATH = (Split-Path -Parent $PythonExe) + [System.IO.Path]::PathSeparator + $env:PATH
        }
        & $PythonExe @ArgsList
    } -ArgumentList (,$ProbeArgs), $ProviderPythonExe, ([string]$RepoRootPath)
}

if ($RunNpuDecodeSmoke) {
    $SmokeArgs = @(
        ".\Tools\ai\run_npu_decode_smoke_diagnostic.py",
        "--repo-root", ".",
        "--run-npu",
        "--output", $NpuDecodeSmokeReport,
        "--text-output", "output/ai_packets/npu_decode_smoke_output.md"
    )
    $Jobs += Start-Job -Name "npu_decode_smoke" -ScriptBlock {
        param([string[]]$ArgsList, [string]$PythonExe, [string]$PythonPath)
        Set-Location $using:RepoRootPath
        $env:IA_CARMINE_PYTHON = $PythonExe
        $env:PYTHONPATH = $PythonPath
        if (Test-Path -LiteralPath $PythonExe -PathType Leaf) {
            $env:PATH = (Split-Path -Parent $PythonExe) + [System.IO.Path]::PathSeparator + $env:PATH
        }
        & $PythonExe @ArgsList
    } -ArgumentList (,$SmokeArgs), $ProviderPythonExe, ([string]$RepoRootPath)
} else {
    & $ProviderPythonExe .\Tools\ai\run_npu_decode_smoke_diagnostic.py `
        --repo-root . `
        --output $NpuDecodeSmokeReport
}

foreach ($Job in $Jobs) {
    Receive-Job -Job $Job -Wait -AutoRemoveJob
}

Write-Host ""
Write-Host "=== Step 3: quality-based routing and NPU remediation ==="
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
& $ProviderPythonExe @RoutingArgs

& $ProviderPythonExe .\Tools\validation\check_npu_decode_quality_remediation.py `
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
& $ProviderPythonExe .\Tools\ai\build_github_evidence_bundle.py `
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
