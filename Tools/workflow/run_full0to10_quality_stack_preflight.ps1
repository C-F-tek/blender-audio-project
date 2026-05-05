param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation/full0to10_quality_stack_preflight",
    [string]$PatchSpecs,
    [switch]$NoExternalProbes,
    [int]$TimeoutSeconds = 8
)

$ErrorActionPreference = "Stop"

function Resolve-RepoPath {
    param([string]$Base, [string]$PathValue)
    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return $PathValue
    }
    return (Join-Path $Base $PathValue)
}

$RepoRoot = (Resolve-Path $RepoRoot).Path
$OutputPath = Resolve-RepoPath -Base $RepoRoot -PathValue $OutputDir
New-Item -ItemType Directory -Force -Path $OutputPath | Out-Null

$CapabilityDir = Join-Path $OutputPath "hardware_tool_capability"
$RegistryDir = Join-Path $OutputPath "runtime_tool_registry"
$GateDir = Join-Path $OutputPath "quality_gate"
New-Item -ItemType Directory -Force -Path $CapabilityDir, $RegistryDir, $GateDir | Out-Null

$CapabilityArgs = @(
    "--repo-root", $RepoRoot,
    "--timeout-seconds", $TimeoutSeconds,
    "--output", (Join-Path $CapabilityDir "full0to10_hardware_tool_capability.json"),
    "--markdown-output", (Join-Path $CapabilityDir "full0to10_hardware_tool_capability.md")
)
if ($NoExternalProbes) {
    $CapabilityArgs += "--no-external-probes"
}
& python (Join-Path $RepoRoot "Tools/ai/build_full0to10_hardware_tool_capability.py") @CapabilityArgs
if ($LASTEXITCODE -ne 0) { throw "hardware/tool capability failed" }

& python (Join-Path $RepoRoot "Tools/ai/build_full0to10_runtime_tool_registry.py") `
    --repo-root $RepoRoot `
    --output (Join-Path $RegistryDir "full0to10_runtime_tool_registry.json") `
    --markdown-output (Join-Path $RegistryDir "full0to10_runtime_tool_registry.md")
if ($LASTEXITCODE -ne 0) { throw "runtime tool registry failed" }

$GateArgs = @(
    "--repo-root", $RepoRoot,
    "--output", (Join-Path $GateDir "full0to10_quality_gate.json"),
    "--markdown-output", (Join-Path $GateDir "full0to10_quality_gate.md")
)
if ($PatchSpecs) {
    $PatchSpecsPath = Resolve-RepoPath -Base $RepoRoot -PathValue $PatchSpecs
    if (Test-Path $PatchSpecsPath) {
        $GateArgs += @("--patch-specs", $PatchSpecsPath)
    }
}
& python (Join-Path $RepoRoot "Tools/ai/build_full0to10_quality_gate.py") @GateArgs
if ($LASTEXITCODE -ne 0) { throw "quality gate failed" }

$SummaryJson = Join-Path $OutputPath "full0to10_quality_stack_preflight.json"
$SummaryMd = Join-Path $OutputPath "full0to10_quality_stack_preflight.md"
& python (Join-Path $RepoRoot "Tools/ai/build_full0to10_quality_stack_summary.py") `
    --repo-root $RepoRoot `
    --search-root $OutputPath `
    --output $SummaryJson `
    --markdown-output $SummaryMd
if ($LASTEXITCODE -ne 0) { throw "quality stack summary failed" }

Write-Host "[OK] Quality stack JSON: $SummaryJson"
Write-Host "[OK] Quality stack MD: $SummaryMd"
