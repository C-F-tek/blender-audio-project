<#
.SYNOPSIS
  Install or print a Windows Scheduled Task for weekly IA-Carmine local AI artifact cleanup.

.DESCRIPTION
  This helper schedules Tools/workflow/run_unified_local_ai_refactor.ps1 in reset mode.

  It targets local/generated artifacts only:
    - output/local_ai_runs/**
    - output/ai_pipeline/**
    - output/validation/**
    - output/ai_context_packs/**
    - output/patch_specs/**
    - indexAI/agent_memory/** when -IncludeMemoryReset is used
    - indexAI/code_chunks/** and indexAI/project_code_chunks/** when -IncludeGeneratedIndexReset is used

  It does not touch source files, docs, scripts, Git history, Blender runtime or FFmpeg runtime.

  By default this script prints the scheduled-task command only. Use -Install to register it.
#>
[CmdletBinding()]
param(
    [string]$TaskName = "IA-Carmine Weekly Local AI Reset",
    [ValidateSet("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")]
    [string]$DayOfWeek = "Monday",
    [string]$At = "03:30",
    [int]$RetentionDays = 7,
    [switch]$IncludeMemoryReset,
    [switch]$IncludeGeneratedIndexReset,
    [switch]$Install,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-RepoRoot {
    $root = (& git rev-parse --show-toplevel 2>$null)
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($root)) {
        throw "Run inside a Git repository checkout."
    }
    return (Resolve-Path $root.Trim()).Path
}

$RepoRoot = Resolve-RepoRoot
$Launcher = Join-Path $RepoRoot "Tools/workflow/run_unified_local_ai_refactor.ps1"
if (-not (Test-Path -LiteralPath $Launcher -PathType Leaf)) {
    throw "Launcher not found: $Launcher"
}

$cutoffExpression = "`$Cutoff = (Get-Date).AddDays(-$RetentionDays).Date"
$includeMemoryArg = if ($IncludeMemoryReset) { " -IncludeMemoryReset" } else { "" }
$includeIndexArg = if ($IncludeGeneratedIndexReset) { " -IncludeGeneratedIndexReset" } else { "" }

$inline = @"
Set-Location '$RepoRoot'; $cutoffExpression; powershell.exe -NoProfile -ExecutionPolicy Bypass -File '$Launcher' -Mode reset -ResetBeforeDate `$Cutoff$includeMemoryArg$includeIndexArg -ApplyReset -ConfirmResetText 'DELETE LOCAL AI ARTIFACTS' -SkipGitSync -NoBranch -AllowDirty
"@

$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument ("-NoProfile -ExecutionPolicy Bypass -Command " + [Management.Automation.Language.CodeGeneration]::QuoteArgument($inline))
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $DayOfWeek -At $At
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Write-Host "Weekly local AI reset scheduled-task plan" -ForegroundColor Cyan
Write-Host "Task name:      $TaskName"
Write-Host "Repository:     $RepoRoot"
Write-Host "Day/time:       $DayOfWeek $At"
Write-Host "Retention days: $RetentionDays"
Write-Host "Include memory: $IncludeMemoryReset"
Write-Host "Include index:  $IncludeGeneratedIndexReset"
Write-Host "Install:        $Install"
Write-Host ""
Write-Host "Inline command:"
Write-Host $inline
Write-Host ""

if (-not $Install) {
    Write-Host "[DRY-RUN] Scheduled task not installed. Re-run with -Install to register it."
    exit 0
}

$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing -and -not $Force) {
    throw "Scheduled task already exists: $TaskName. Use -Force to replace it."
}
if ($existing -and $Force) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Description "Weekly IA-Carmine local AI generated-artifact reset. Source files are not targeted."
Write-Host "[OK] Scheduled task installed: $TaskName" -ForegroundColor Green
