param(
    [string]$RepoRoot = ".",
    [string]$RunReport = "output/validation/light_full0to10_evidence/full0to10_light_evidence_only_run.json",
    [string]$OutputDir = "output/validation/light_full0to10_profile_gate",
    [switch]$Strict
)

$ErrorActionPreference = "Stop"

function Resolve-RepoPath {
    param([string]$Base, [string]$PathValue)
    if ([System.IO.Path]::IsPathRooted($PathValue)) { return $PathValue }
    return (Join-Path $Base $PathValue)
}

$RepoRoot = (Resolve-Path $RepoRoot).Path
$RunReportPath = Resolve-RepoPath -Base $RepoRoot -PathValue $RunReport
$OutputPath = Resolve-RepoPath -Base $RepoRoot -PathValue $OutputDir
New-Item -ItemType Directory -Force -Path $OutputPath | Out-Null

$Builder = Join-Path $RepoRoot "Tools/ai/build_full0to10_light_profile_promotion.py"
$Summary = Join-Path $OutputPath "full0to10_light_profile_promotion.from_gate.json"
& python $Builder --run-report $RunReportPath --output-dir $OutputPath --output $Summary
$ExitCode = $LASTEXITCODE

Write-Host ("[OK] Light profile gate JSON: {0}" -f $Summary)

if ($Strict -and $ExitCode -ne 0) {
    throw "Light profile gate failed in strict mode."
}
