<#
.SYNOPSIS
  Run the local validation workflow after AI-assisted refactors.

.DESCRIPTION
  This script is intentionally local and non-destructive. It pulls the latest
  repository state, runs validation checks, runs the AI pipeline dry-run matrix,
  regenerates AI/NPU indexes, and writes a compact execution log.

  It does not commit or push automatically.

.USAGE
  powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1

  powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull

  powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -ContinueOnError
#>

param(
    [switch]$SkipPull,
    [switch]$ContinueOnError,
    [string]$RepoRoot = ".",
    [string]$LogDir = "output/local_validation"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-RepoRoot {
    param([string]$Path)
    return (Resolve-Path -LiteralPath $Path).Path
}

function New-LogDirectory {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Force -Path $Path | Out-Null
    }
}

function Write-Section {
    param([string]$Title)
    $line = "`n=== $Title ==="
    Write-Host $line -ForegroundColor Cyan
    Add-Content -LiteralPath $script:MainLog -Value $line
}

function Invoke-Step {
    param(
        [string]$Name,
        [string]$Command,
        [string[]]$Arguments
    )

    Write-Section $Name
    $started = Get-Date
    Add-Content -LiteralPath $script:MainLog -Value ("Started: " + $started.ToString("o"))
    Add-Content -LiteralPath $script:MainLog -Value ("Command: " + $Command + " " + ($Arguments -join " "))

    $oldErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        & $Command @Arguments 2>&1 | ForEach-Object {
            $line = $_.ToString()
            Write-Host $line
            Add-Content -LiteralPath $script:MainLog -Value $line
        }
        $exitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $oldErrorActionPreference
    }

    if ($null -eq $exitCode) {
        $exitCode = 0
    }

    $ended = Get-Date
    Add-Content -LiteralPath $script:MainLog -Value ("Ended: " + $ended.ToString("o"))
    Add-Content -LiteralPath $script:MainLog -Value ("ExitCode: " + $exitCode)

    $script:Results += [pscustomobject]@{
        name = $Name
        command = $Command
        args = $Arguments
        started = $started.ToString("o")
        ended = $ended.ToString("o")
        exit_code = $exitCode
        passed = ($exitCode -eq 0)
    }

    if (($exitCode -ne 0) -and (-not $ContinueOnError)) {
        throw "Step failed: $Name with exit code $exitCode"
    }
}

$repo = Resolve-RepoRoot $RepoRoot
Set-Location $repo

$logPath = Join-Path $repo $LogDir
New-LogDirectory $logPath

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$script:MainLog = Join-Path $logPath "local_validation_$stamp.log"
$summaryJson = Join-Path $logPath "local_validation_$stamp.json"
$summaryMd = Join-Path $logPath "local_validation_$stamp.md"
$script:Results = @()

Add-Content -LiteralPath $script:MainLog -Value "Local validation started: $(Get-Date -Format o)"
Add-Content -LiteralPath $script:MainLog -Value "Repo: $repo"

try {
    if (-not $SkipPull) {
        Invoke-Step -Name "git pull --rebase" -Command "git" -Arguments @("pull", "--rebase", "origin", "master")
    }

    Invoke-Step -Name "git status before validation" -Command "git" -Arguments @("status")
    Invoke-Step -Name "python syntax validation" -Command "python" -Arguments @(".\Tools\validation\check_python_syntax.py", "--repo-root", ".")
    Invoke-Step -Name "ai pipeline module smoke validation" -Command "python" -Arguments @(".\Tools\validation\check_ai_pipeline_modules.py", "--repo-root", ".", "--output", ".\output\validation\ai_pipeline_modules.json")
    Invoke-Step -Name "refactor status consistency validation" -Command "python" -Arguments @(".\Tools\validation\check_refactor_status_consistency.py", "--repo-root", ".", "--output", ".\output\validation\refactor_status_consistency.json")
    Invoke-Step -Name "documentation links validation" -Command "python" -Arguments @(".\Tools\validation\check_docs_links.py", "--repo-root", ".", "--output", ".\output\validation\docs_links.json")
    Invoke-Step -Name "agent memory policy validation" -Command "python" -Arguments @(".\Tools\validation\check_agent_memory_policy.py", "--repo-root", ".", "--output", ".\output\validation\agent_memory_policy.json")
    Invoke-Step -Name "blender shared compatibility smoke" -Command "python" -Arguments @(".\Tools\validation\check_blender_shared_compat_smoke.py", "--repo-root", ".", "--output", ".\output\validation\blender_shared_compat_smoke.json")
    Invoke-Step -Name "ai pipeline dry-run matrix" -Command "python" -Arguments @(".\Tools\ai\run_pipeline_dry_run_matrix.py", "--repo-root", ".", "--continue-on-error")
    Invoke-Step -Name "package structure validation" -Command "python" -Arguments @(".\Tools\validation\check_package_structure.py", "--repo-root", ".")
    Invoke-Step -Name "json artifact validation" -Command "python" -Arguments @(".\Tools\validation\check_json_artifacts.py", "--repo-root", ".")
    Invoke-Step -Name "build project ai index" -Command "python" -Arguments @(".\Tools\npu\build_project_ai_index.py")
    Invoke-Step -Name "build npu code context" -Command "python" -Arguments @(".\Tools\npu\build_npu_code_context.py")
    Invoke-Step -Name "git diff stat after validation" -Command "git" -Arguments @("diff", "--stat")
    Invoke-Step -Name "git status after validation" -Command "git" -Arguments @("status")

    $failedSteps = @($script:Results | Where-Object { -not $_.passed })
    $passed = ($failedSteps.Count -eq 0)
}
catch {
    $passed = $false
    Add-Content -LiteralPath $script:MainLog -Value ("ERROR: " + $_.Exception.Message)
    Write-Host ("ERROR: " + $_.Exception.Message) -ForegroundColor Red
}

$summary = [pscustomobject]@{
    schema_version = 1
    generated_at = (Get-Date).ToString("o")
    repo_root = $repo
    passed = $passed
    log_path = $script:MainLog
    ai_pipeline_modules_report = (Join-Path $repo "output\validation\ai_pipeline_modules.json")
    refactor_status_consistency_report = (Join-Path $repo "output\validation\refactor_status_consistency.json")
    docs_links_report = (Join-Path $repo "output\validation\docs_links.json")
    agent_memory_policy_report = (Join-Path $repo "output\validation\agent_memory_policy.json")
    blender_shared_compat_smoke_report = (Join-Path $repo "output\validation\blender_shared_compat_smoke.json")
    dry_run_matrix_json = (Join-Path $repo "output\ai_pipeline\dry_run_matrix_report.json")
    dry_run_matrix_markdown = (Join-Path $repo "output\ai_pipeline\dry_run_matrix_report.md")
    steps = $script:Results
}

$summary | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $summaryJson -Encoding UTF8

$md = @()
$md += "# Local Validation After Refactor"
$md += ""
$md += ("- Generated at: {0}" -f $summary.generated_at)
$md += ("- Passed: {0}" -f $passed)
$md += ("- Repo: {0}" -f $repo)
$md += ("- Log: {0}" -f $script:MainLog)
$md += ("- AI module report: {0}" -f $summary.ai_pipeline_modules_report)
$md += ("- Refactor status consistency report: {0}" -f $summary.refactor_status_consistency_report)
$md += ("- Docs links report: {0}" -f $summary.docs_links_report)
$md += ("- Agent memory policy report: {0}" -f $summary.agent_memory_policy_report)
$md += ("- Blender shared compatibility smoke report: {0}" -f $summary.blender_shared_compat_smoke_report)
$md += ("- Dry-run matrix JSON: {0}" -f $summary.dry_run_matrix_json)
$md += ("- Dry-run matrix Markdown: {0}" -f $summary.dry_run_matrix_markdown)
$md += ""
$md += "## Steps"
$md += ""
$md += "| Step | Passed | Exit code |"
$md += "|---|---:|---:|"
foreach ($step in $script:Results) {
    $md += ("| {0} | {1} | {2} |" -f $step.name, $step.passed, $step.exit_code)
}
$md += ""
$md += "## Next manual commands"
$md += ""
$md += "Run these commands from the repository root:"
$md += ""
$md += "    git status"
$md += "    git diff --stat"
$md += "    Get-Content .\output\validation\ai_pipeline_modules.json -Raw"
$md += "    Get-Content .\output\validation\refactor_status_consistency.json -Raw"
$md += "    Get-Content .\output\validation\docs_links.json -Raw"
$md += "    Get-Content .\output\validation\agent_memory_policy.json -Raw"
$md += "    Get-Content .\output\validation\blender_shared_compat_smoke.json -Raw"
$md += "    Get-Content .\output\ai_pipeline\dry_run_matrix_report.md -Raw"
$md | Set-Content -LiteralPath $summaryMd -Encoding UTF8

Write-Host ""
Write-Host "Validation completed." -ForegroundColor Green
Write-Host "Passed: $passed"
Write-Host "Log: $script:MainLog"
Write-Host "Summary JSON: $summaryJson"
Write-Host "Summary MD: $summaryMd"

if ($passed) {
    exit 0
}
exit 2
