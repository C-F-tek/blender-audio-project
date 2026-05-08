param(
    [string]$RepoRoot = ".",
    [string]$PatchSpecs = "output/validation/full0to10_auto_refactor_plan/full0to10_auto_refactor_patch_specs.json",
    [string]$OutputDir = "output/validation/full0to10_markdown_split_shadow",
    [string]$ShadowRoot = "",
    [switch]$ApplyShadow,
    [int]$MaxSpecs = 0,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ForwardedArgs = @()
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

function Assert-ShadowRootSafe {
    param([string]$Root, [string]$Shadow)
    $OutputValidation = (Resolve-Path (Join-Path $Root "output/validation")).Path
    $ShadowFull = [System.IO.Path]::GetFullPath($Shadow)
    if (-not $ShadowFull.StartsWith($OutputValidation, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Markdown split shadow root must stay under output/validation. Got: $ShadowFull"
    }
}

$RepoRoot = (Resolve-Path $RepoRoot).Path
$PatchSpecsPath = Resolve-RepoPath -Base $RepoRoot -PathValue $PatchSpecs
$OutputPath = Resolve-RepoPath -Base $RepoRoot -PathValue $OutputDir
if (-not $ShadowRoot) {
    $ShadowRoot = Join-Path $OutputPath "shadow_files"
}
$ShadowRootPath = Resolve-RepoPath -Base $RepoRoot -PathValue $ShadowRoot

New-Item -ItemType Directory -Force -Path (Join-Path $RepoRoot "output/validation") | Out-Null
New-Item -ItemType Directory -Force -Path $OutputPath, $ShadowRootPath | Out-Null
Assert-ShadowRootSafe -Root $RepoRoot -Shadow $ShadowRootPath

$Args = @(
    "--repo-root", $RepoRoot,
    "--patch-specs", $PatchSpecsPath,
    "--output-dir", $OutputPath,
    "--shadow-root", $ShadowRootPath
)

if ($ApplyShadow) {
    $Args += "--apply-shadow"
}
if ($MaxSpecs -gt 0) {
    $Args += @("--max-specs", $MaxSpecs)
}
if ($ForwardedArgs.Count -gt 0) {
    $Args += $ForwardedArgs
}

$ScriptPath = Join-Path $RepoRoot "Tools/ai/apply_full0to10_markdown_split_patch_specs.py"
& $WorkflowPythonExe $ScriptPath @Args
$ExitCode = $LASTEXITCODE

if ($ExitCode -ne 0) {
    throw "Full0To10 Markdown split shadow failed with exit code $ExitCode"
}

Write-Host "[OK] Markdown split shadow output: $OutputPath"
Write-Host "[OK] Markdown split shadow files: $ShadowRootPath"

