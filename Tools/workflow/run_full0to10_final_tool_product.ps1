param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation/full0to10_final_tool_product",
    [string]$Request = "Costruisci il pacchetto prodotto finale Full0To10 orientato a SQLite FTS5, runtime tools, GPU/Ollama, NPU/OpenVINO e quality gate.",
    [switch]$NoExternalProbes,
    [int]$TimeoutSeconds = 8
)

$ErrorActionPreference = "Stop"


# IA-CARMINE-REPO-PYTHON-POLICY-BEGIN
$RepoRootForWorkflowPython = (& git rev-parse --show-toplevel 2>$null)
if ([string]::IsNullOrWhiteSpace($RepoRootForWorkflowPython)) {
    $RepoRootForWorkflowPython = (Resolve-Path ".").Path
} else {
    $RepoRootForWorkflowPython = (Resolve-Path $RepoRootForWorkflowPython.Trim()).Path
}
. (Join-Path $RepoRootForWorkflowPython "Tools/workflow/python_env.ps1")
$WorkflowPythonExe = Use-WorkflowPython -RepoRoot $RepoRootForWorkflowPython
# IA-CARMINE-REPO-PYTHON-POLICY-END
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

$Manifest = Join-Path $OutputPath "full0to10_final_tool_product_manifest.from_cli.json"
$Args = @(
    "--repo-root", $RepoRoot,
    "--output-dir", $OutputPath,
    "--request", $Request,
    "--timeout-seconds", $TimeoutSeconds,
    "--output", $Manifest
)

if ($NoExternalProbes) {
    $Args += "--no-external-probes"
}

& $WorkflowPythonExe (Join-Path $RepoRoot "Tools/ai/build_full0to10_final_tool_product.py") @Args
if ($LASTEXITCODE -ne 0) {
    throw "Full0To10 final tool product build failed with exit code $LASTEXITCODE"
}

Write-Host "[OK] Final tool product manifest: $Manifest"
Write-Host "[OK] Final tool product markdown: $(Join-Path $OutputPath 'full0to10_final_tool_product.md')"

