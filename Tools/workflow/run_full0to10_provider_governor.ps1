param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation/full0to10_provider_governor",
    [string]$Request = "Valuta se GPU/Ollama può ricevere run permit con NPU auditor e GPU.0 diagnostic nel Full0To10.",
    [switch]$OperatorIntent,
    [switch]$AllowProviderGeneration,
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

$Summary = Join-Path $OutputPath "full0to10_provider_governor.from_cli.json"
$Args = @(
    "--repo-root", $RepoRoot,
    "--output-dir", $OutputPath,
    "--request", $Request,
    "--timeout-seconds", $TimeoutSeconds,
    "--output", $Summary
)

if ($OperatorIntent) { $Args += "--operator-intent" }
if ($AllowProviderGeneration) { $Args += "--allow-provider-generation" }
if ($NoExternalProbes) { $Args += "--no-external-probes" }

& python (Join-Path $RepoRoot "Tools/ai/build_full0to10_provider_governor.py") @Args
if ($LASTEXITCODE -ne 0) {
    throw "Full0To10 provider governor failed with exit code $LASTEXITCODE"
}

Write-Host "[OK] Provider governor JSON: $Summary"
Write-Host "[OK] Provider governor MD: $(Join-Path $OutputPath 'full0to10_provider_governor.md')"
