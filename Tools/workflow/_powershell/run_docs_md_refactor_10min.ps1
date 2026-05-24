<#
.SYNOPSIS
  Prepare a bounded 10-minute Markdown/refactor local-AI run.

.DESCRIPTION
  This wrapper wires the post-PR183 documentation/refactor lane into the existing
  local AI Markdown task launcher. It builds Markdown and script inventories,
  validates the current task-scoped local reports, then prepares or launches the
  local AI task packet for docs-md obsolete pruning.

  The wrapper is report-only. It does not apply patches, run Blender, commit
  output/**, or execute providers by itself. Provider execution is delegated only
  to the supplied runner command and remains governed by the task documents.
#>
[CmdletBinding()]
param(
    [string]$TaskBranch = "",
    [string]$Stamp = "",
    [switch]$SkipGitSync,
    [switch]$NoBranch,
    [switch]$AllowDirty,
    [switch]$DryRun,
    [switch]$LaunchRunner
)

Set-StrictMode -Version Latest
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
function Invoke-Git {
    param([string[]]$GitArgs)
    Write-Host "[git] git $($GitArgs -join ' ')"
    & git @GitArgs
    if ($LASTEXITCODE -ne 0) {
        throw "git command failed: git $($GitArgs -join ' ')"
    }
}

function Resolve-RepoRoot {
    $root = (& git rev-parse --show-toplevel 2>$null)
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($root)) {
        throw "This command must be run inside a Git repository checkout."
    }
    return (Resolve-Path $root.Trim()).Path
}

function Assert-FileExists {
    param([string]$PathValue)
    if (-not (Test-Path -LiteralPath $PathValue -PathType Leaf)) {
        throw "required file missing: $PathValue"
    }
}

function Assert-CleanWorkingTree {
    param([switch]$AllowDirtyTree)
    $status = (& git status --porcelain)
    if ($LASTEXITCODE -ne 0) {
        throw "git status failed"
    }
    if (-not $AllowDirtyTree -and $status) {
        Write-Host "[ERROR] Working tree has local changes:" -ForegroundColor Red
        $status | ForEach-Object { Write-Host $_ }
        throw "working tree is not clean; rerun with -AllowDirty only when those changes are intended input"
    }
}

$repoRoot = Resolve-RepoRoot
Set-Location $repoRoot

if ([string]::IsNullOrWhiteSpace($Stamp)) {
    $Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
}

if ([string]::IsNullOrWhiteSpace($TaskBranch)) {
    $TaskBranch = "codex/docs-md-obsolete-pruning-$Stamp"
}

$env:PYTHONPATH = $repoRoot

$requiredFiles = @(
    "AGENTS.md",
    "README.md",
    "WORKFLOW.md",
    "docs/README.md",
    "docs/DOCUMENTATION_MAP_AND_PRUNING_PLAN.md",
    "docs/LOCAL_AI_RUN_BOOTSTRAP.md",
    "docs/README.md",
    "docs/AI_DOCS_ENTRYPOINT.md",
    "docs/LOCAL_AI_TASKS/code-refactor-0-to-10-procedure.md",
    "docs/LOCAL_AI_TASKS/code-refactor-local-machine-validation-addendum.md",
    "docs/LOCAL_AI_TASKS/code-refactor-md-lane-extension.md",
    "docs/LOCAL_AI_TASKS/docs-md-obsolete-pruning-next-step.md",
    "docs/LOCAL_VALIDATION_EVIDENCE/LOCAL_MACHINE_VALIDATION.md",
    "Tools/validation/docs_hygiene/markdown_inventory/cli.py",
    "Tools/validation/docs_hygiene/build_script_inventory/cli.py",
    "Tools/workflow/run_local_ai_markdown_task.ps1",
    "Tools/workflow/run_local_ai_task_via_pipeline.ps1"
)

foreach ($file in $requiredFiles) {
    Assert-FileExists (Join-Path $repoRoot $file)
}

Assert-CleanWorkingTree -AllowDirtyTree:$AllowDirty

if (-not $SkipGitSync) {
    Invoke-Git -GitArgs @("fetch", "origin")
    Invoke-Git -GitArgs @("switch", "master")
    Invoke-Git -GitArgs @("pull", "--ff-only", "origin", "master")
}

if (-not $NoBranch) {
    $existingBranches = (& git branch --list $TaskBranch)
    if ($LASTEXITCODE -ne 0) {
        throw "git branch lookup failed"
    }
    if ($existingBranches) {
        Invoke-Git -GitArgs @("switch", $TaskBranch)
    }
    else {
        Invoke-Git -GitArgs @("switch", "-c", $TaskBranch)
    }
}

Write-Host "[INFO] Stamp:      $Stamp"
Write-Host "[INFO] TaskBranch: $TaskBranch"

& $WorkflowPythonExe -m py_compile `
    .\Tools\validation\docs_hygiene\markdown_inventory\cli.py `
    .\Tools\validation\docs_hygiene\build_script_inventory\cli.py
if ($LASTEXITCODE -ne 0) {
    throw "inventory py_compile failed"
}

$markdownInventoryJson = ".\output\validation\markdown_inventory_refactor_$Stamp.json"
$markdownInventoryMd = ".\output\validation\markdown_inventory_refactor_$Stamp.md"
$scriptInventoryJson = ".\output\validation\script_inventory_refactor_$Stamp.json"
$scriptInventoryCsv = ".\output\validation\script_inventory_refactor_$Stamp.csv"
$scriptInventoryMd = ".\output\validation\script_inventory_refactor_$Stamp.md"
$docsLinksJson = ".\output\validation\docs_links_$Stamp.json"
$contractJson = ".\output\validation\validation_report_contract_md_refactor_task_$Stamp.json"

& $WorkflowPythonExe -m Tools.validation build_markdown_inventory `
    --repo-root . `
    --output $markdownInventoryJson `
    --markdown-output $markdownInventoryMd
if ($LASTEXITCODE -ne 0) {
    throw "build_markdown_inventory failed"
}

& $WorkflowPythonExe -m Tools.validation build_script_inventory `
    --repo-root . `
    --output $scriptInventoryJson `
    --csv-output $scriptInventoryCsv `
    --markdown-output $scriptInventoryMd
if ($LASTEXITCODE -ne 0) {
    throw "build_script_inventory failed"
}

& $WorkflowPythonExe -m Tools.validation check_docs_links `
    --repo-root . `
    --output $docsLinksJson
if ($LASTEXITCODE -ne 0) {
    throw "check_docs_links failed"
}

& $WorkflowPythonExe -m Tools.validation check_validation_report_contract `
    --repo-root . `
    --report-file $markdownInventoryJson `
    --report-file $scriptInventoryJson `
    --report-file $docsLinksJson `
    --output $contractJson
if ($LASTEXITCODE -ne 0) {
    throw "task-scoped validation report contract failed"
}

$runnerCommand = 'python -m Tools.workflow run_local_ai_task_via_pipeline -PromptFile "{PROMPT_FILE}" -TaskFile "{TASK_FILE}" -RunDir "{RUN_DIR}"'
$taskFile = ".\docs\LOCAL_AI_TASKS\docs-md-obsolete-pruning-next-step.md"

$launcherArgs = @(
    "-m", "Tools.workflow", "run_local_ai_markdown_task",
    "-TaskFile", $taskFile,
    "-TaskBranch", $TaskBranch,
    "-RunnerCommand", $runnerCommand
)

if ($SkipGitSync) { $launcherArgs += "-SkipGitSync" }
if ($NoBranch) { $launcherArgs += "-NoBranch" }
if ($AllowDirty) { $launcherArgs += "-AllowDirty" }
if (-not $LaunchRunner -or $DryRun) { $launcherArgs += "-DryRun" }

Write-Host "[INFO] Preparing local AI Markdown task packet"
& $WorkflowPythonExe @launcherArgs
if ($LASTEXITCODE -ne 0) {
    throw "run_local_ai_markdown_task wrapper failed"
}

git diff --check
if ($LASTEXITCODE -ne 0) {
    throw "git diff --check failed"
}

$status = (& git status --short)
if ($LASTEXITCODE -ne 0) {
    throw "git status failed"
}

Write-Host ""
Write-Host "[OK] 10-minute Markdown/refactor local-AI packet workflow completed" -ForegroundColor Green
Write-Host "[OK] Stamp: $Stamp"
Write-Host "[OK] Branch: $((& git branch --show-current).Trim())"
Write-Host "[OK] Markdown inventory: $markdownInventoryJson"
Write-Host "[OK] Script inventory:   $scriptInventoryJson"
Write-Host "[OK] Script CSV:         $scriptInventoryCsv"
Write-Host "[OK] Docs links:         $docsLinksJson"
Write-Host "[OK] Contract:           $contractJson"
Write-Host "[OK] Runner launched:    $([bool]$LaunchRunner -and -not [bool]$DryRun)"
Write-Host ""
Write-Host "[INFO] git status --short:"
if ($status) {
    $status | ForEach-Object { Write-Host $_ }
}
else {
    Write-Host "<clean>"
}

Write-Host ""
Write-Host "[INFO] 10-minute provider profile to use if the local runner reaches orchestrator execution:"
Write-Host "--budget-minutes 10 --max-rounds 8 --files-per-round 6 --max-context-files 120 --max-chars-per-file 5000 --max-new-tokens 2400 --keep-alive 15m"
