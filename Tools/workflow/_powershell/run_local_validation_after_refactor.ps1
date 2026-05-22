<#
.SYNOPSIS
  Run the local validation workflow after AI-assisted refactors.

.DESCRIPTION
  This script is intentionally local and non-destructive. It pulls the latest
  repository state, runs validation checks, runs the AI pipeline dry-run matrix,
  regenerates AI/NPU indexes, writes a compact execution log, and builds an
  advisory post-validation AI work packet.

  It does not commit or push automatically.

.USAGE
  python -m Tools.workflow run_local_validation_after_refactor

  python -m Tools.workflow run_local_validation_after_refactor -SkipPull

  python -m Tools.workflow run_local_validation_after_refactor -ContinueOnError

  python -m Tools.workflow run_local_validation_after_refactor -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2

  Optional local Ollama advisory packet:

  python -m Tools.workflow run_local_validation_after_refactor -SkipPull -ContinueOnError -BuildAiPacket -UseOllama
#>

param(
    [switch]$SkipPull,
    [switch]$ContinueOnError,
    [switch]$BuildAiPacket = $true,
    [switch]$UseOllama,
    [string]$OllamaModel = "",
    [string]$RepoRoot = ".",
    [string]$LogDir = "output/local_validation",
    [int]$MatrixWorkers = 8,
    [int]$RepeatCases = 1
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$PythonEnvScript = Join-Path $PSScriptRoot "python_env.ps1"
. $PythonEnvScript

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
$ValidationPythonExe = Use-WorkflowPython -RepoRoot $repo

$logPath = Join-Path $repo $LogDir
New-LogDirectory $logPath

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$script:MainLog = Join-Path $logPath "local_validation_$stamp.log"
$summaryJson = Join-Path $logPath "local_validation_$stamp.json"
$summaryMd = Join-Path $logPath "local_validation_$stamp.md"
$script:Results = @()

Add-Content -LiteralPath $script:MainLog -Value "Local validation started: $(Get-Date -Format o)"
Add-Content -LiteralPath $script:MainLog -Value "Repo: $repo"
Add-Content -LiteralPath $script:MainLog -Value "MatrixWorkers: $MatrixWorkers"
Add-Content -LiteralPath $script:MainLog -Value "RepeatCases: $RepeatCases"
Add-Content -LiteralPath $script:MainLog -Value "BuildAiPacket: $BuildAiPacket"
Add-Content -LiteralPath $script:MainLog -Value "UseOllama: $UseOllama"
Add-Content -LiteralPath $script:MainLog -Value "Python: $ValidationPythonExe"

try {
    if (-not $SkipPull) {
        Invoke-Step -Name "git pull --rebase" -Command "git" -Arguments @("pull", "--rebase", "origin", "master")
    }

    Invoke-Step -Name "git status before validation" -Command "git" -Arguments @("status")
    Invoke-Step -Name "python syntax validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_python_syntax", "--repo-root", ".", "--output", ".\output\validation\python_syntax.json")
    Invoke-Step -Name "ai model json validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_ai_model_json", "--repo-root", ".", "--output", ".\output\validation\ai_model_json.json")
    Invoke-Step -Name "ai pipeline module smoke validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_ai_pipeline_modules", "--repo-root", ".", "--output", ".\output\validation\ai_pipeline_modules.json")
    Invoke-Step -Name "npu pipeline module smoke validation" -Command "python" -Arguments @("-m", "Tools.validation", "npu_pipeline_modules_check", "--repo-root", ".", "--output", ".\output\validation\npu_pipeline_modules.json")
    Invoke-Step -Name "npu pipeline helper unit tests" -Command "python" -Arguments @("-m", "Tools.validation", "check_npu_pipeline_helper_tests", "--repo-root", ".", "--output", ".\output\validation\npu_pipeline_helper_tests.json")
    Invoke-Step -Name "npu pipeline docs validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_npu_pipeline_docs", "--repo-root", ".", "--output", ".\output\validation\npu_pipeline_docs.json")
    Invoke-Step -Name "execution plan status validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_execution_plan_status", "--repo-root", ".", "--output", ".\output\validation\execution_plan_status.json")
    Invoke-Step -Name "ai dry-run matrix case definition validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_ai_dry_run_matrix_cases", "--repo-root", ".", "--output", ".\output\validation\ai_dry_run_matrix_cases.json")
    Invoke-Step -Name "generated python policy validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_generated_python_policy", "--repo-root", ".", "--output", ".\output\validation\generated_python_policy.json")
    Invoke-Step -Name "generated blender script policy validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_generated_blender_script_policy", "--repo-root", ".", "--output", ".\output\validation\generated_blender_script_policy.json")
    Invoke-Step -Name "refactor status consistency validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_refactor_status_consistency", "--repo-root", ".", "--output", ".\output\validation\refactor_status_consistency.json")
    Invoke-Step -Name "documentation links validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_docs_links", "--repo-root", ".", "--output", ".\output\validation\docs_links.json")
    Invoke-Step -Name "agent memory policy validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_agent_memory_policy", "--repo-root", ".", "--output", ".\output\validation\agent_memory_policy.json")
    Invoke-Step -Name "blender shared compatibility smoke" -Command "python" -Arguments @("-m", "Tools.validation", "check_blender_shared_compat_smoke", "--repo-root", ".", "--output", ".\output\validation\blender_shared_compat_smoke.json")
    Invoke-Step -Name "ai pipeline dry-run matrix" -Command "python" -Arguments @("-m", "ia_carmine.cli", "pipeline_dry_run_matrix", "--repo-root", ".", "--continue-on-error", "--matrix-workers", $MatrixWorkers.ToString(), "--repeat-cases", $RepeatCases.ToString())
    Invoke-Step -Name "ai pipeline schema-v6 report contract validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_ai_pipeline_report_contract", "--repo-root", ".", "--report", ".\output\ai_pipeline\dry_run_matrix\base\ai_pipeline_dry_run_report.json", "--require-dry-run", "--output", ".\output\validation\ai_pipeline_report_contract.json")
    Invoke-Step -Name "ai dry-run matrix contract validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_ai_dry_run_matrix_contract", "--repo-root", ".", "--output", ".\output\validation\ai_dry_run_matrix_contract.json")
    Invoke-Step -Name "ai dry-run matrix output consistency validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_ai_dry_run_matrix_outputs", "--repo-root", ".", "--output", ".\output\validation\ai_dry_run_matrix_outputs.json")
    Invoke-Step -Name "generated artifact path policy validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_generated_artifact_path_policy", "--repo-root", ".", "--artifact-report", ".\output\ai_pipeline\dry_run_matrix_report.json", "--output", ".\output\validation\generated_artifact_path_policy.json")
    Invoke-Step -Name "package structure validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_package_structure", "--repo-root", ".", "--output", ".\output\validation\package_structure.json")
    Invoke-Step -Name "json artifact validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_json_artifacts", "--repo-root", ".", "--output", ".\output\validation\json_artifacts.json")
    Invoke-Step -Name "validation report contract validation" -Command "python" -Arguments @("-m", "Tools.validation", "check_validation_report_contract", "--repo-root", ".", "--output", ".\output\validation\validation_report_contract.json")
    Invoke-Step -Name "build project ai index" -Command "python" -Arguments @("-m", "Tools.npu", "build_project_ai_index")
    Invoke-Step -Name "build npu code context" -Command "python" -Arguments @("-m", "Tools.npu", "build_npu_code_context")

    if ($BuildAiPacket) {
        $packetArgs = @("-m", "Tools.workflow", "run_post_validation_ai_packet", "-RepoRoot", ".")
        if ($UseOllama) {
            $packetArgs += "-UseOllama"
        }
        if ($OllamaModel -ne "") {
            $packetArgs += @("-Model", $OllamaModel)
        }
        Invoke-Step -Name "post-validation ai work packet" -Command $ValidationPythonExe -Arguments $packetArgs
    }

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
    matrix_workers = $MatrixWorkers
    repeat_cases = $RepeatCases
    build_ai_packet = [bool]$BuildAiPacket
    use_ollama = [bool]$UseOllama
    log_path = $script:MainLog
    ai_model_json_report = (Join-Path $repo "output\validation\ai_model_json.json")
    ai_pipeline_modules_report = (Join-Path $repo "output\validation\ai_pipeline_modules.json")
    npu_pipeline_modules_report = (Join-Path $repo "output\validation\npu_pipeline_modules.json")
    npu_pipeline_helper_tests_report = (Join-Path $repo "output\validation\npu_pipeline_helper_tests.json")
    npu_pipeline_docs_report = (Join-Path $repo "output\validation\npu_pipeline_docs.json")
    execution_plan_status_report = (Join-Path $repo "output\validation\execution_plan_status.json")
    ai_dry_run_matrix_cases_report = (Join-Path $repo "output\validation\ai_dry_run_matrix_cases.json")
    ai_pipeline_report_contract_report = (Join-Path $repo "output\validation\ai_pipeline_report_contract.json")
    ai_dry_run_matrix_outputs_report = (Join-Path $repo "output\validation\ai_dry_run_matrix_outputs.json")
    validation_report_contract_report = (Join-Path $repo "output\validation\validation_report_contract.json")
    generated_python_policy_report = (Join-Path $repo "output\validation\generated_python_policy.json")
    generated_artifact_path_policy_report = (Join-Path $repo "output\validation\generated_artifact_path_policy.json")
    generated_blender_script_policy_report = (Join-Path $repo "output\validation\generated_blender_script_policy.json")
    refactor_status_consistency_report = (Join-Path $repo "output\validation\refactor_status_consistency.json")
    docs_links_report = (Join-Path $repo "output\validation\docs_links.json")
    agent_memory_policy_report = (Join-Path $repo "output\validation\agent_memory_policy.json")
    blender_shared_compat_smoke_report = (Join-Path $repo "output\validation\blender_shared_compat_smoke.json")
    ai_dry_run_matrix_contract_report = (Join-Path $repo "output\validation\ai_dry_run_matrix_contract.json")
    dry_run_matrix_json = (Join-Path $repo "output\ai_pipeline\dry_run_matrix_report.json")
    dry_run_matrix_markdown = (Join-Path $repo "output\ai_pipeline\dry_run_matrix_report.md")
    repository_update_suggestions_json = (Join-Path $repo "output\ai_pipeline\repository_update_suggestions.json")
    repository_update_suggestions_markdown = (Join-Path $repo "output\ai_pipeline\repository_update_suggestions.md")
    steps = $script:Results
}

$summary | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $summaryJson -Encoding UTF8

$md = @()
$md += "# Local Validation After Refactor"
$md += ""
$md += ("- Generated at: {0}" -f $summary.generated_at)
$md += ("- Passed: {0}" -f $passed)
$md += ("- Repo: {0}" -f $repo)
$md += ("- Matrix workers: {0}" -f $MatrixWorkers)
$md += ("- Repeat cases: {0}" -f $RepeatCases)
$md += ("- Build AI packet: {0}" -f $BuildAiPacket)
$md += ("- Use Ollama: {0}" -f $UseOllama)
$md += ("- Log: {0}" -f $script:MainLog)
$md += ("- AI model JSON report: {0}" -f $summary.ai_model_json_report)
$md += ("- AI module report: {0}" -f $summary.ai_pipeline_modules_report)
$md += ("- NPU module report: {0}" -f $summary.npu_pipeline_modules_report)
$md += ("- NPU helper tests report: {0}" -f $summary.npu_pipeline_helper_tests_report)
$md += ("- NPU docs report: {0}" -f $summary.npu_pipeline_docs_report)
$md += ("- Execution plan status report: {0}" -f $summary.execution_plan_status_report)
$md += ("- AI dry-run matrix cases report: {0}" -f $summary.ai_dry_run_matrix_cases_report)
$md += ("- AI pipeline schema-v6 report contract report: {0}" -f $summary.ai_pipeline_report_contract_report)
$md += ("- AI dry-run matrix outputs report: {0}" -f $summary.ai_dry_run_matrix_outputs_report)
$md += ("- Validation report contract report: {0}" -f $summary.validation_report_contract_report)
$md += ("- Generated Python policy report: {0}" -f $summary.generated_python_policy_report)
$md += ("- Generated artifact path policy report: {0}" -f $summary.generated_artifact_path_policy_report)
$md += ("- Generated Blender script policy report: {0}" -f $summary.generated_blender_script_policy_report)
$md += ("- Refactor status consistency report: {0}" -f $summary.refactor_status_consistency_report)
$md += ("- Docs links report: {0}" -f $summary.docs_links_report)
$md += ("- Agent memory policy report: {0}" -f $summary.agent_memory_policy_report)
$md += ("- Blender shared compatibility smoke report: {0}" -f $summary.blender_shared_compat_smoke_report)
$md += ("- AI dry-run matrix contract report: {0}" -f $summary.ai_dry_run_matrix_contract_report)
$md += ("- Dry-run matrix JSON: {0}" -f $summary.dry_run_matrix_json)
$md += ("- Dry-run matrix Markdown: {0}" -f $summary.dry_run_matrix_markdown)
$md += ("- Repository update suggestions JSON: {0}" -f $summary.repository_update_suggestions_json)
$md += ("- Repository update suggestions Markdown: {0}" -f $summary.repository_update_suggestions_markdown)
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
$md += "    Get-Content .\output\validation\ai_model_json.json -Raw"
$md += "    Get-Content .\output\validation\ai_pipeline_modules.json -Raw"
$md += "    Get-Content .\output\validation\npu_pipeline_modules.json -Raw"
$md += "    Get-Content .\output\validation\npu_pipeline_helper_tests.json -Raw"
$md += "    Get-Content .\output\validation\npu_pipeline_docs.json -Raw"
$md += "    Get-Content .\output\validation\execution_plan_status.json -Raw"
$md += "    Get-Content .\output\validation\ai_dry_run_matrix_cases.json -Raw"
$md += "    Get-Content .\output\validation\ai_pipeline_report_contract.json -Raw"
$md += "    Get-Content .\output\validation\ai_dry_run_matrix_outputs.json -Raw"
$md += "    Get-Content .\output\validation\validation_report_contract.json -Raw"
$md += "    Get-Content .\output\validation\generated_python_policy.json -Raw"
$md += "    Get-Content .\output\validation\generated_artifact_path_policy.json -Raw"
$md += "    Get-Content .\output\validation\generated_blender_script_policy.json -Raw"
$md += "    Get-Content .\output\validation\refactor_status_consistency.json -Raw"
$md += "    Get-Content .\output\validation\docs_links.json -Raw"
$md += "    Get-Content .\output\validation\agent_memory_policy.json -Raw"
$md += "    Get-Content .\output\validation\blender_shared_compat_smoke.json -Raw"
$md += "    Get-Content .\output\validation\ai_dry_run_matrix_contract.json -Raw"
$md += "    Get-Content .\output\ai_pipeline\dry_run_matrix_report.md -Raw"
$md += "    Get-Content .\output\ai_pipeline\repository_update_suggestions.md -Raw"
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
