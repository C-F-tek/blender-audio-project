param(
    [string]$RepoRoot = ".",
    [string]$OutputDir = "output/validation/full0to10_hardware_tool_capability",
    [int]$TimeoutSeconds = 8,
    [switch]$NoExternalProbes
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

$Json = Join-Path $OutputPath "full0to10_hardware_tool_capability.json"
$Md = Join-Path $OutputPath "full0to10_hardware_tool_capability.md"

$Args = @(
    "--repo-root", $RepoRoot,
    "--timeout-seconds", $TimeoutSeconds,
    "--output", $Json,
    "--markdown-output", $Md
)

if ($NoExternalProbes) {
    $Args += "--no-external-probes"
}

& $WorkflowPythonExe (Join-Path $RepoRoot "Tools/ai/build_full0to10_hardware_tool_capability.py") @Args

Write-Host "[OK] Hardware/tool capability JSON: $Json"
Write-Host "[OK] Hardware/tool capability MD: $Md"

