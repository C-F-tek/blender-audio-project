param(
    [string]$RepoRoot = ".",
    [string]$Bundle,
    [string]$EvidenceDir = "docs/LOCAL_VALIDATION_EVIDENCE",
    [string]$OutputDir = "output/validation/full0to10_manifest_contract_gate",
    [int]$Workers = 6
)

$ErrorActionPreference = "Stop"

function Resolve-RepoPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Base,
        [Parameter(Mandatory = $true)]
        [string]$PathValue
    )

    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return $PathValue
    }

    return (Join-Path $Base $PathValue)
}

$RepoRoot = (Resolve-Path $RepoRoot).Path
$OutputPath = Resolve-RepoPath -Base $RepoRoot -PathValue $OutputDir
$EvidencePath = Resolve-RepoPath -Base $RepoRoot -PathValue $EvidenceDir

New-Item -ItemType Directory -Force -Path $OutputPath | Out-Null

$ManifestJson = Join-Path $OutputPath "full0to10_run_manifest.json"
$ManifestMd = Join-Path $OutputPath "full0to10_run_manifest.md"
$ContractJson = Join-Path $OutputPath "full0to10_bundle_contract_validation.json"
$ContractMd = Join-Path $OutputPath "full0to10_bundle_contract_validation.md"

$Python = "python"

& $Python (Join-Path $RepoRoot "Tools/ai/build_full0to10_run_manifest.py") `
    --repo-root $RepoRoot `
    --scan-root "docs/LOCAL_VALIDATION_EVIDENCE" `
    --scan-root "output/validation" `
    --scan-root "output/ai_pipeline" `
    --scan-root "output/ai_packets" `
    --scan-root "output/patch_specs" `
    --workers $Workers `
    --output $ManifestJson `
    --markdown-output $ManifestMd

if (-not $Bundle) {
    $Candidates = Get-ChildItem $EvidencePath -Filter "*bundle*.json" -File -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending
    if ($Candidates.Count -gt 0) {
        $Bundle = $Candidates[0].FullName
    }
}

if (-not $Bundle) {
    throw "Bundle path not supplied and no bundle candidate found."
}

$BundlePath = Resolve-RepoPath -Base $RepoRoot -PathValue $Bundle

& $Python (Join-Path $RepoRoot "Tools/validation/check_full0to10_bundle_contracts.py") `
    --repo-root $RepoRoot `
    --bundle $BundlePath `
    --evidence-dir $EvidencePath `
    --output $ContractJson `
    --markdown-output $ContractMd

Write-Host "[OK] Manifest: $ManifestJson"
Write-Host "[OK] Contract: $ContractJson"
