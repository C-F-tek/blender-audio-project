<#
.SYNOPSIS
  Prepare and optionally launch a non-interactive local AI task from a Markdown entrypoint.

.DESCRIPTION
  This wrapper is intentionally runner-agnostic. It reads AGENTS.md,
  docs/LOCAL_AI_RUN_BOOTSTRAP.md and a task file under docs/LOCAL_AI_TASKS/,
  then writes a bounded local run packet under output/local_ai_runs/.

  If -RunnerCommand is provided, the command is executed after placeholder
  substitution. No provider/GPU/NPU execution is performed by this wrapper.

  The preferred project-owned runner is python -m Tools.workflow run_local_ai_task_via_pipeline.
  External runners such as Codex CLI may still be used by the master/control-plane
  AI workflow during the transition, but they are not the default local runner path.

.EXAMPLE
  python -m Tools.workflow run_local_ai_markdown_task `
    -TaskFile .\docs\LOCAL_AI_TASKS\issue-57-docs-congruence-cleanup.md `
    -TaskBranch codex/docs-congruence-cleanup

.EXAMPLE
  python -m Tools.workflow run_local_ai_markdown_task `
    -TaskFile .\docs\LOCAL_AI_TASKS\issue-62-hybrid-master-ai-local-pipeline.md `
    -TaskBranch codex/hybrid-local-pipeline-runner `
    -RunnerCommand 'python -m Tools.workflow run_local_ai_task_via_pipeline -PromptFile "{PROMPT_FILE}" -TaskFile "{TASK_FILE}" -RunDir "{RUN_DIR}"'
#>
[CmdletBinding()]
param(
    [string]$TaskFile = "docs/LOCAL_AI_TASKS/issue-57-docs-congruence-cleanup.md",
    [string]$TaskBranch = "",
    [string]$RunnerCommand = "",
    [string]$OutputDir = "output/local_ai_runs",
    [switch]$SkipGitSync,
    [switch]$NoBranch,
    [switch]$AllowDirty,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

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

function Resolve-ExistingRepoPath {
    param(
        [string]$RepoRoot,
        [string]$PathValue
    )
    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return (Resolve-Path $PathValue).Path
    }
    return (Resolve-Path (Join-Path $RepoRoot $PathValue)).Path
}

function Resolve-PlannedRepoPath {
    param(
        [string]$RepoRoot,
        [string]$PathValue
    )
    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return [System.IO.Path]::GetFullPath($PathValue)
    }
    return [System.IO.Path]::GetFullPath((Join-Path $RepoRoot $PathValue))
}

function Get-RepoRelativePath {
    param(
        [string]$RepoRoot,
        [string]$PathValue
    )
    $full = [System.IO.Path]::GetFullPath($PathValue)
    $root = [System.IO.Path]::GetFullPath($RepoRoot)
    if (-not $root.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
        $root = $root + [System.IO.Path]::DirectorySeparatorChar
    }
    if ($full.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $full.Substring($root.Length).Replace("\", "/")
    }
    return $full.Replace("\", "/")
}

function Read-RequiredText {
    param([string]$PathValue)
    if (-not (Test-Path -LiteralPath $PathValue -PathType Leaf)) {
        throw "required file missing: $PathValue"
    }
    return Get-Content -LiteralPath $PathValue -Raw -Encoding UTF8
}

function Assert-CleanWorkingTree {
    param([switch]$AllowDirtyTree)
    $status = (& git status --porcelain)
    if ($LASTEXITCODE -ne 0) {
        throw "git status failed"
    }
    if (-not $AllowDirtyTree -and $status) {
        Write-Host "[ERROR] Working tree has unrelated changes:" -ForegroundColor Red
        $status | ForEach-Object { Write-Host $_ }
        throw "working tree is not clean; rerun with -AllowDirty only when the task explicitly covers these changes"
    }
}

function New-SafeSlug {
    param([string]$Value)
    $slug = [regex]::Replace($Value.ToLowerInvariant(), "[^a-z0-9._-]+", "-").Trim("-", ".", "_")
    if ([string]::IsNullOrWhiteSpace($slug)) {
        return "local-ai-task"
    }
    return $slug
}

$repoRoot = Resolve-RepoRoot
Set-Location $repoRoot

$agentsPath = Resolve-ExistingRepoPath $repoRoot "AGENTS.md"
$bootstrapPath = Resolve-ExistingRepoPath $repoRoot "docs/LOCAL_AI_RUN_BOOTSTRAP.md"
$taskPath = Resolve-ExistingRepoPath $repoRoot $TaskFile

$taskRelative = Get-RepoRelativePath $repoRoot $taskPath
$taskSlug = New-SafeSlug ([System.IO.Path]::GetFileNameWithoutExtension($taskPath))
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$runBaseDir = Resolve-PlannedRepoPath $repoRoot $OutputDir
$runDir = Join-Path $runBaseDir "${timestamp}_${taskSlug}"
New-Item -ItemType Directory -Force -Path $runDir | Out-Null

Assert-CleanWorkingTree -AllowDirtyTree:$AllowDirty

if (-not $SkipGitSync) {
    Invoke-Git -GitArgs @("fetch", "origin")
    Invoke-Git -GitArgs @("switch", "master")
    Invoke-Git -GitArgs @("pull", "--ff-only", "origin", "master")
}

if (-not $NoBranch -and -not [string]::IsNullOrWhiteSpace($TaskBranch)) {
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

$branch = (& git branch --show-current).Trim()
$headSha = (& git rev-parse HEAD).Trim()
$agentsText = Read-RequiredText $agentsPath
$bootstrapText = Read-RequiredText $bootstrapPath
$taskText = Read-RequiredText $taskPath

$promptPath = Join-Path $runDir "local_ai_prompt.md"
$manifestPath = Join-Path $runDir "local_ai_run_manifest.json"
$procedurePath = Join-Path $runDir "local_ai_run_procedure.md"

$prompt = @"
# Local AI Non-Interactive Run Packet

This packet was generated by `python -m Tools.workflow run_local_ai_markdown_task`.

The AI runner must obey the repository contract below before planning, editing or validating.

## Invocation metadata

- Repository root: `$repoRoot`
- Branch: `$branch`
- HEAD: `$headSha`
- Task file: `$taskRelative`
- Provider execution requested by wrapper: `false`
- Runner command supplied: `$([bool](-not [string]::IsNullOrWhiteSpace($RunnerCommand)))`

## Primary instruction

Read and obey the following sections in order:

1. `AGENTS.md`
2. `docs/LOCAL_AI_RUN_BOOTSTRAP.md`
3. task file `$taskRelative`

If any section conflicts, preserve hard guardrails from `AGENTS.md` and stop with a conflict report.

---

# AGENTS.md

```markdown
$agentsText
```

---

# docs/LOCAL_AI_RUN_BOOTSTRAP.md

```markdown
$bootstrapText
```

---

# $taskRelative

```markdown
$taskText
```
"@

$prompt | Set-Content -LiteralPath $promptPath -Encoding UTF8

$pipelineExample = "python -m Tools.workflow run_local_ai_task_via_pipeline -PromptFile `"{PROMPT_FILE}`" -TaskFile `"{TASK_FILE}`" -RunDir `"{RUN_DIR}`""

$procedure = @"
# Local AI Run Procedure

Generated: $(Get-Date -Format o)

## Prepared files

```text
$(Get-RepoRelativePath $repoRoot $promptPath)
$(Get-RepoRelativePath $repoRoot $manifestPath)
```

## Default wrapper command

```powershell
python -m Tools.workflow run_local_ai_markdown_task `
  -TaskFile .$([System.IO.Path]::DirectorySeparatorChar)$($taskRelative.Replace('/', [System.IO.Path]::DirectorySeparatorChar)) `
  -TaskBranch $TaskBranch
```

## Preferred project-owned runner

The preferred local runner is the repository pipeline adapter:

```powershell
python -m Tools.workflow run_local_ai_markdown_task `
  -TaskFile .$([System.IO.Path]::DirectorySeparatorChar)$($taskRelative.Replace('/', [System.IO.Path]::DirectorySeparatorChar)) `
  -TaskBranch $TaskBranch `
  -RunnerCommand '$pipelineExample'
```

This mode creates advisory packets/proposals through repository tools. It does not apply patches and does not execute providers unless explicit provider flags are passed to the adapter.

## Runner command placeholder contract

Available placeholders:

```text
{REPO_ROOT}
{TASK_FILE}
{PROMPT_FILE}
{MANIFEST_FILE}
{RUN_DIR}
{BRANCH}
```

External runners can still be used by the master/control-plane workflow during the transition, but they are not the default local path.

## No runner mode

If `-RunnerCommand` is omitted, this wrapper only prepares the packet. Use:

```text
$(Get-RepoRelativePath $repoRoot $promptPath)
```

as the input file for a local runner.
"@

$procedure | Set-Content -LiteralPath $procedurePath -Encoding UTF8

$manifest = [ordered]@{
    schema_version = 1
    kind = "local_ai_markdown_task_wrapper_run"
    generated_at = (Get-Date -Format o)
    repo_root = $repoRoot
    branch = $branch
    head_sha = $headSha
    task_file = $taskRelative
    agents_file = "AGENTS.md"
    bootstrap_file = "docs/LOCAL_AI_RUN_BOOTSTRAP.md"
    preferred_runner = "python -m Tools.workflow run_local_ai_task_via_pipeline"
    run_dir = (Get-RepoRelativePath $repoRoot $runDir)
    prompt_file = (Get-RepoRelativePath $repoRoot $promptPath)
    procedure_file = (Get-RepoRelativePath $repoRoot $procedurePath)
    provider_execution_performed = $false
    runner_command_supplied = -not [string]::IsNullOrWhiteSpace($RunnerCommand)
    dry_run = [bool]$DryRun
    errors = @()
    warnings = @()
}

($manifest | ConvertTo-Json -Depth 6) | Set-Content -LiteralPath $manifestPath -Encoding UTF8

Write-Host "[OK] Local AI task packet prepared" -ForegroundColor Green
Write-Host "[OK] Prompt:    $(Get-RepoRelativePath $repoRoot $promptPath)"
Write-Host "[OK] Manifest:  $(Get-RepoRelativePath $repoRoot $manifestPath)"
Write-Host "[OK] Procedure: $(Get-RepoRelativePath $repoRoot $procedurePath)"
Write-Host "[OK] Branch:    $branch"

if (-not [string]::IsNullOrWhiteSpace($RunnerCommand)) {
    $command = $RunnerCommand
    $command = $command.Replace("{REPO_ROOT}", $repoRoot)
    $command = $command.Replace("{TASK_FILE}", $taskPath)
    $command = $command.Replace("{PROMPT_FILE}", $promptPath)
    $command = $command.Replace("{MANIFEST_FILE}", $manifestPath)
    $command = $command.Replace("{RUN_DIR}", $runDir)
    $command = $command.Replace("{BRANCH}", $branch)

    Write-Host "[runner] $command"
    if (-not $DryRun) {
        powershell.exe -NoProfile -ExecutionPolicy Bypass -Command $command
        if ($LASTEXITCODE -ne 0) {
            throw "runner command failed with exit code $LASTEXITCODE"
        }
    }
    else {
        Write-Host "[DRY-RUN] Runner command not executed."
    }
}
else {
    Write-Host "[INFO] No -RunnerCommand supplied; packet generation only."
}
