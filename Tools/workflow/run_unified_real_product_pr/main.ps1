if ($CreatePr -and -not $Push) {
    Stop-RealProductLauncher -Code "create_pr_requires_push" -Message "-CreatePr requires -Push because prepare_review_pr.py needs the branch on the remote" -Root $RepoRoot -StampValue $Stamp
}
if ($DraftPr -and -not $CreatePr) {
    Stop-RealProductLauncher -Code "draft_pr_requires_create_pr" -Message "-DraftPr requires -CreatePr" -Root $RepoRoot -StampValue $Stamp
}
if (($ResetLocalAiMemoryBeforeRun -or $ResetGeneratedIndexBeforeRun) -and -not $ResetLocalAiArtifactsBeforeRun) {
    Stop-RealProductLauncher -Code "reset_flags_require_artifact_reset" -Message "-ResetLocalAiMemoryBeforeRun and -ResetGeneratedIndexBeforeRun require -ResetLocalAiArtifactsBeforeRun." -Root $RepoRoot -StampValue $Stamp
}
if ($ResetLocalAiArtifactsRetentionDays -lt 0) {
    Stop-RealProductLauncher -Code "invalid_reset_retention_days" -Message "-ResetLocalAiArtifactsRetentionDays must be zero or greater." -Root $RepoRoot -StampValue $Stamp
}

if ($CreatePr) { $ValidateFinalReviewPrProduct = $true }

$ResolvedRepoRoot = Resolve-RepoRoot -Root $RepoRoot
Set-Location $ResolvedRepoRoot

if ([string]::IsNullOrWhiteSpace($Stamp)) {
    $Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
}

$GeneratedProcessGateTask = $false
if ([string]::IsNullOrWhiteSpace($TaskFile)) {
    if (-not $ProcessGateTask) {
        Stop-RealProductLauncher -Code "task_file_required" -Message "-TaskFile is required unless -ProcessGateTask is used." -Root $ResolvedRepoRoot -StampValue $Stamp
    }

    $TaskFile = New-HeapExchangeProcessGateTask -Root $ResolvedRepoRoot -StampValue $Stamp
    $GeneratedProcessGateTask = $true
}
elseif ($ProcessGateTask) {
    Write-Warning "-ProcessGateTask was provided together with -TaskFile; using the explicit task file."
}

$TaskPath = if ([System.IO.Path]::IsPathRooted($TaskFile)) {
    Resolve-Path -LiteralPath $TaskFile
}
else {
    Resolve-Path -LiteralPath (Join-Path $ResolvedRepoRoot $TaskFile)
}
$TaskRel = Get-RepoRelativePath -Root $ResolvedRepoRoot -PathValue $TaskPath.Path

if ($GeneratedProcessGateTask -and -not $AllowDirty) {
    $DirtyAfterGeneratedTask = (& git status --short)
    if (-not [string]::IsNullOrWhiteSpace($DirtyAfterGeneratedTask)) {
        Write-Host "[ERROR] Generated process gate task dirtied the repository:" -ForegroundColor Red
        Write-Host $DirtyAfterGeneratedTask
        Stop-RealProductLauncher -Code "generated_task_dirty_tree" -Message "Generated process gate task must live under ignored output/**." -Root $ResolvedRepoRoot -StampValue $Stamp
    }
}

$Slug = New-SafeSlug ([System.IO.Path]::GetFileNameWithoutExtension($TaskPath.Path))
if ([string]::IsNullOrWhiteSpace($TaskBranch)) {
    $TaskBranch = "CARMINEai/real-product-$Slug-$Stamp"
}

$Launcher = Join-Path $ResolvedRepoRoot "Tools/workflow/_powershell/run_unified_local_ai_refactor.ps1"
if (-not (Test-Path -LiteralPath $Launcher -PathType Leaf)) {
    Stop-RealProductLauncher -Code "unified_launcher_missing" -Message "Unified launcher missing: $Launcher" -Root $ResolvedRepoRoot -StampValue $Stamp -DetailPath $Launcher
}

$PreflightGate = Join-Path $ResolvedRepoRoot "Tools/validation/run_real_product_preflight_gate/cli.py"
if (-not (Test-Path -LiteralPath $PreflightGate -PathType Leaf)) {
    Stop-RealProductLauncher -Code "mandatory_preflight_missing" -Message "Mandatory real product preflight gate missing: $PreflightGate" -Root $ResolvedRepoRoot -StampValue $Stamp -DetailPath $PreflightGate
}

$ResolvedPythonExe = $PythonExe
if ([string]::IsNullOrWhiteSpace($ResolvedPythonExe)) {
    if (-not [string]::IsNullOrWhiteSpace($env:IA_CARMINE_PYTHON)) {
        $ResolvedPythonExe = $env:IA_CARMINE_PYTHON
    }
    elseif (Test-Path -LiteralPath (Join-Path $ResolvedRepoRoot ".venv/Scripts/python.exe") -PathType Leaf) {
        $ResolvedPythonExe = Join-Path $ResolvedRepoRoot ".venv/Scripts/python.exe"
    }
    else {
        $ResolvedPythonExe = "python"
    }
}

if ($ResetLocalAiArtifactsBeforeRun) {
    Invoke-LocalAiArtifactReset `
        -Root $ResolvedRepoRoot `
        -LauncherPath $Launcher `
        -RetentionDays $ResetLocalAiArtifactsRetentionDays `
        -IncludeMemory ([bool]$ResetLocalAiMemoryBeforeRun) `
        -IncludeGeneratedIndex ([bool]$ResetGeneratedIndexBeforeRun) `
        -PythonPath $ResolvedPythonExe
}

$PreflightOutput = Join-Path $ResolvedRepoRoot "output/validation/real_product_profile_preflight_$Stamp.json"
$PreflightMarkdown = Join-Path $ResolvedRepoRoot "output/validation/real_product_profile_preflight_$Stamp.md"

Write-Host "=== IA-Carmine mandatory real product preflight ==="
Write-Host "Preflight gate: $PreflightGate"
Write-Host "Preflight timeout seconds: $PreflightTimeoutSeconds"
Write-Host "Python: $ResolvedPythonExe"
& $ResolvedPythonExe $PreflightGate `
    --repo-root $ResolvedRepoRoot `
    --output $PreflightOutput `
    --markdown-output $PreflightMarkdown `
    --timeout-seconds $PreflightTimeoutSeconds

if ($LASTEXITCODE -ne 0) {
    Stop-RealProductLauncher -Code "mandatory_preflight_failed" -Message "Mandatory real product preflight failed. See $PreflightOutput" -Root $ResolvedRepoRoot -StampValue $Stamp -DetailPath $PreflightOutput
}

Write-Host "[OK] Mandatory real product preflight passed: $PreflightOutput"
Write-Host ""

$RealProductPostPreflightModes = "smoke,reset,md,json,python,chunks,context_pack,agent_state,official,provider,patch_specs,evidence,contract,full_validation"

$script:LauncherArgs = @(
    "-NoProfile", "-ExecutionPolicy", "Bypass",
    "-File", $Launcher,
    "-RepoRoot", $ResolvedRepoRoot,
    "-TaskFile", $TaskRel,
    "-TaskBranch", $TaskBranch,
    "-Stamp", $Stamp,
    "-Mode", $RealProductPostPreflightModes,
    "-RunIntensity", $RunIntensity,
    "-Model", $Model,
    "-Profile", "core",

    "-UseOllamaAdvisory",
    "-UsePrimaryAdvisoryProvider",
    "-RunMultistepProviderWorkflow",
    "-RunOllamaProbe",
    "-RunNpuProbe",
    "-RunNpuDecodeSmoke",
    "-RunOpenVinoGpu0Workload",
    "-BuildEvidence",
    "-GeneratePatchSpecs",
    "-BuildTaskPatchSuggestionReport",
    "-PrepareReviewPr",
    "-BuildRuntimeEvidenceCorrelation",
    "-ReviewPrBranch", $TaskBranch,
    "-ReviewPrBaseBranch", "master",
    "-ReviewPrTitle", "feat(ai): real product review $Slug $Stamp",
    "-ReviewPrCommitMessage", "feat(ai): prepare real product review",
    "-ReviewPrMaxAppliedPatches", ([string]$ReviewPrMaxAppliedPatches),
    "-SaveInputsToMemoryDb"
)

Add-OptionalLauncherArg -Name "-PythonExe" -Value $PythonExe
Add-LauncherArg -Name "-BudgetMinutes" -Value ([string]$BudgetMinutes)
Add-LauncherArg -Name "-MaxRounds" -Value ([string]$MaxRounds)
Add-LauncherArg -Name "-FilesPerRound" -Value ([string]$FilesPerRound)
Add-LauncherArg -Name "-MaxContextFiles" -Value ([string]$MaxContextFiles)
Add-LauncherArg -Name "-MaxCharsPerFile" -Value ([string]$MaxCharsPerFile)
Add-LauncherArg -Name "-MaxNewTokens" -Value ([string]$MaxNewTokens)
Add-LauncherArg -Name "-KeepAlive" -Value $KeepAlive
Add-LauncherArg -Name "-NpuMicroStartMode" -Value $NpuMicroStartMode
Add-LauncherArg -Name "-ProviderMaxContextChars" -Value ([string]$ProviderMaxContextChars)

# IA-CARMINE-REAL-PRODUCT-OFFICIAL-MAX-CONTEXT-BEGIN
$OfficialAdapterMaxContextChars = $ProviderMaxContextChars
if ($OfficialAdapterMaxContextChars -le 0) {
    $OfficialAdapterMaxContextChars = 14000
}
Add-LauncherArg -Name "-MaxContextChars" -Value ([string]$OfficialAdapterMaxContextChars)
# IA-CARMINE-REAL-PRODUCT-OFFICIAL-MAX-CONTEXT-END
Add-LauncherArg -Name "-ContextPackMaxTotalChars" -Value ([string]$ContextPackMaxTotalChars)
Add-LauncherArg -Name "-ContextPackMaxFileChars" -Value ([string]$ContextPackMaxFileChars)
Add-LauncherArg -Name "-AgentStateMaxMemoryChars" -Value ([string]$AgentStateMaxMemoryChars)
Add-LauncherArg -Name "-MaxRecommendations" -Value ([string]$MaxRecommendations)
Add-LauncherArg -Name "-MaxPatchPlans" -Value ([string]$MaxPatchPlans)
Add-LauncherArg -Name "-OfficialAdapterTimeoutSeconds" -Value ([string]$OfficialAdapterTimeoutSeconds)
Add-LauncherArg -Name "-ObserverRefreshSeconds" -Value ([string]$ObserverRefreshSeconds)

Add-LauncherSwitch -Name "-OpenObserverConsoles" -Enabled ([bool]$OpenObserverConsoles)
Add-LauncherSwitch -Name "-OpenExtendedObserverConsoles" -Enabled ([bool]$OpenExtendedObserverConsoles)

if ($UseGeneratedPatchSpecs) {
    $script:LauncherArgs += "-ReviewPrFromGeneratedPatchSpecs"
}
else {
    $script:LauncherArgs += "-ReviewPrApplyDeterministicSuggestions"
}

Add-LauncherSwitch -Name "-ReviewPrPush" -Enabled ([bool]$Push)
Add-LauncherSwitch -Name "-ReviewPrCreate" -Enabled ([bool]$CreatePr)
Add-LauncherSwitch -Name "-ReviewPrDraft" -Enabled ([bool]$DraftPr)
Add-LauncherSwitch -Name "-AllowDirty" -Enabled ([bool]$AllowDirty)
Add-LauncherSwitch -Name "-SkipGitSync" -Enabled ([bool]$SkipGitSync)
Add-LauncherSwitch -Name "-DryRun" -Enabled ([bool]$DryRun)

Write-Host "=== IA-Carmine real product profile ==="
Write-Host "Repo: $ResolvedRepoRoot"
Write-Host "Task: $TaskRel"
Write-Host "Branch: $TaskBranch"
Write-Host "Stamp: $Stamp"
Write-Host "Run intensity: $RunIntensity"
Write-Host "Model: $Model"
Write-Host "Budget minutes: $BudgetMinutes"
Write-Host "Max rounds: $MaxRounds"
Write-Host "Files per round: $FilesPerRound"
Write-Host "Max context files: $MaxContextFiles"
Write-Host "Max chars per file: $MaxCharsPerFile"
Write-Host "Max new tokens: $MaxNewTokens"
Write-Host "NPU micro start mode: $NpuMicroStartMode"
Write-Host "Provider max context chars: $ProviderMaxContextChars"
Write-Host "Official adapter max context chars: $OfficialAdapterMaxContextChars"
Write-Host "Context pack max total chars: $ContextPackMaxTotalChars"
Write-Host "Context pack max file chars: $ContextPackMaxFileChars"
Write-Host "Agent state max memory chars: $AgentStateMaxMemoryChars"
Write-Host "Max recommendations: $MaxRecommendations"
Write-Host "Max patch plans: $MaxPatchPlans"
Write-Host "Official adapter timeout seconds: $OfficialAdapterTimeoutSeconds"
Write-Host "Preflight timeout seconds: $PreflightTimeoutSeconds"
Write-Host "Pre-run local AI reset: $ResetLocalAiArtifactsBeforeRun"
Write-Host "Pre-run reset retention days: $ResetLocalAiArtifactsRetentionDays"
Write-Host "Pre-run memory reset: $ResetLocalAiMemoryBeforeRun"
Write-Host "Pre-run generated index reset: $ResetGeneratedIndexBeforeRun"
Write-Host "Observer consoles: $OpenObserverConsoles"
Write-Host "Extended observer consoles: $OpenExtendedObserverConsoles"
Write-Host "Observer refresh seconds: $ObserverRefreshSeconds"
Write-Host "Push: $Push"
Write-Host "Create PR: $CreatePr"
Write-Host "Draft PR: $DraftPr"
Write-Host "Use generated patch specs: $UseGeneratedPatchSpecs"
Write-Host "Post-preflight modes: $RealProductPostPreflightModes"
Write-Host ""
Write-Host "[RUN] powershell.exe $($script:LauncherArgs -join ' ')"

& powershell.exe @script:LauncherArgs
$LauncherExitCode = $LASTEXITCODE
if ($LauncherExitCode -ne 0) {
    exit $LauncherExitCode
}

if ($ValidateFinalReviewPrProduct -and -not $DryRun) {
    $FinalProductContract = Join-Path $ResolvedRepoRoot "Tools/validation/check_review_pr_final_product_contract/cli.py"
    if (-not (Test-Path -LiteralPath $FinalProductContract -PathType Leaf)) {
        Stop-RealProductLauncher -Code "final_product_contract_missing" -Message "Review PR final product contract missing: $FinalProductContract" -Root $ResolvedRepoRoot -StampValue $Stamp -DetailPath $FinalProductContract
    }

    $ReviewReportCandidates = @()
    $ReviewReportCandidates += Get-ChildItem -Path (Join-Path $ResolvedRepoRoot "output/validation") -Filter ("review_pr_prepare_*_{0}.json" -f $Stamp) -File -ErrorAction SilentlyContinue
    $ReviewReportCandidates += Get-ChildItem -Path (Join-Path $ResolvedRepoRoot "output/validation") -Filter ("*review_pr_prepare*{0}*.json" -f $Stamp) -File -ErrorAction SilentlyContinue
    $ReviewReport = $ReviewReportCandidates |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1

    if ($null -eq $ReviewReport) {
        Stop-RealProductLauncher -Code "review_pr_prepare_report_missing" -Message "review_pr_prepare report not found for stamp $Stamp" -Root $ResolvedRepoRoot -StampValue $Stamp
    }

    $FinalProductJson = Join-Path $ResolvedRepoRoot ("output/validation/review_pr_final_product_contract_remote_{0}.json" -f $Stamp)
    $FinalProductMd = Join-Path $ResolvedRepoRoot ("output/validation/review_pr_final_product_contract_remote_{0}.md" -f $Stamp)

    $FinalProductArgs = @(
        $FinalProductContract,
        "--repo-root", $ResolvedRepoRoot,
        "--review-pr-report", $ReviewReport.FullName,
        "--output", $FinalProductJson,
        "--markdown-output", $FinalProductMd
    )

    if ($CreatePr) {
        $FinalProductArgs += "--require-remote-pr"
    }

    & $ResolvedPythonExe @FinalProductArgs
    $FinalProductExitCode = $LASTEXITCODE
    if ($FinalProductExitCode -ne 0) {
        Stop-RealProductLauncher -Code "review_pr_final_product_contract_failed" -Message "Review PR final product contract failed. See $FinalProductJson" -Root $ResolvedRepoRoot -StampValue $Stamp -DetailPath $FinalProductJson
    }

    $ReviewPrReport = Get-Content -LiteralPath $ReviewReport.FullName -Raw | ConvertFrom-Json
    Write-Host "[OK] Review PR final product contract passed: $FinalProductJson"
    if (-not [string]::IsNullOrWhiteSpace([string]$ReviewPrReport.github_pr_url)) {
        Write-Host "[OK] Review PR URL: $($ReviewPrReport.github_pr_url)"
    }
    if (-not [string]::IsNullOrWhiteSpace([string]$ReviewPrReport.product_commit)) {
        Write-Host "[OK] Product commit: $($ReviewPrReport.product_commit)"
    }
}

exit 0
