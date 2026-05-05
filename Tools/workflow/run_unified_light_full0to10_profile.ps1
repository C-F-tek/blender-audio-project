param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation/unified_light_full0to10_profile",
    [string]$TrackName = "current",
    [int]$MaxRepoQualityFiles = 180,
    [int]$TimeoutSeconds = 8,
    [switch]$NoExternalProbes,
    [switch]$Strict,
    [switch]$SkipFinalProduct
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
$RunDir = Join-Path $OutputPath "run"
$PromotionDir = Join-Path $OutputPath "promotion"
New-Item -ItemType Directory -Force -Path $RunDir, $PromotionDir | Out-Null

$RunArgs = @(
    "-RepoRoot", $RepoRoot,
    "-OutputDir", $RunDir,
    "-TrackName", $TrackName,
    "-MaxRepoQualityFiles", "$MaxRepoQualityFiles",
    "-TimeoutSeconds", "$TimeoutSeconds"
)

if ($NoExternalProbes) {
    $RunArgs += "-NoExternalProbes"
}
if ($Strict) {
    $RunArgs += "-Strict"
}
if ($SkipFinalProduct) {
    $RunArgs += "-SkipFinalProduct"
}

$LightRunScript = Join-Path $RepoRoot "Tools/workflow/run_full0to10_light_evidence_only.ps1"
Write-Host "[RUN] LightFull0To10 profile"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $LightRunScript @RunArgs
$LightExit = $LASTEXITCODE

$RunReport = Join-Path $RunDir "full0to10_light_evidence_only_run.json"
$PromotionJson = Join-Path $PromotionDir "full0to10_light_evidence_promotion.json"
$PromotionMd = Join-Path $PromotionDir "full0to10_light_evidence_promotion.md"

$SummaryScript = Join-Path $RepoRoot "Tools/ai/summarize_full0to10_light_evidence.py"
& python $SummaryScript --run-report $RunReport --output $PromotionJson --markdown-output $PromotionMd
$PromotionExit = $LASTEXITCODE

Write-Host ("[OK] Promotion JSON: {0}" -f $PromotionJson)
Write-Host ("[OK] Promotion MD: {0}" -f $PromotionMd)

if ($Strict -and ($LightExit -ne 0 -or $PromotionExit -ne 0)) {
    throw "Unified LightFull0To10 profile failed in strict mode."
}
