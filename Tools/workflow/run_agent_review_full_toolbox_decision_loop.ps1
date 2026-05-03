param(
    [string]$RepoRoot = ".",
    [string]$Stamp = "",
    [string]$OutputRoot = "output",
    [string]$EvidenceDir = "docs/LOCAL_VALIDATION_EVIDENCE",
    [switch]$RunGpuNpuProvider,
    [switch]$SkipMemoryReload,
    [switch]$SkipRepositoryConsistencyMap,
    [switch]$SkipPostValidationPacket,
    [switch]$SkipSharedToolboxBundle,
    [int]$BudgetMinutes = 30,
    [int]$MaxRounds = 20,
    [int]$FilesPerRound = 8,
    [int]$MaxContextFiles = 220,
    [int]$MaxCharsPerFile = 6000,
    [int]$MaxNewTokens = 3600,
    [string]$KeepAlive = "35m",
    [int]$NpuAuditorEveryRounds = 3,
    [int]$NpuAuditorTimeoutSeconds = 420,
    [int]$NpuMaxContextChars = 8000,
    [int]$NpuMaxPromptChars = 1200,
    [int]$NpuMaxNewTokens = 384,
    [int]$NpuFinalWaitSeconds = 180,
    [int]$MinRecommendations = 1,
    [int]$MinPatchPlans = 1
)

$ErrorActionPreference = "Stop"
$RepoRootPath = Resolve-Path $RepoRoot
Set-Location $RepoRootPath

if ($Stamp -eq "") {
    $Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
}

$env:PYTHONPATH = (Get-Location).Path

$AiPipelineDir = Join-Path $OutputRoot "ai_pipeline"
$AnalysisDir = Join-Path $OutputRoot "analysis"
$ValidationDir = Join-Path $OutputRoot "validation"
$PatchSpecDir = Join-Path $OutputRoot "patch_specs"
New-Item -ItemType Directory -Force -Path $AiPipelineDir, $AnalysisDir, $ValidationDir, $PatchSpecDir, $EvidenceDir | Out-Null

function Invoke-RepoPython {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$ArgsList,
        [string]$Label = "python"
    )
    Write-Host ""
    Write-Host "=== $Label ==="
    python @ArgsList
}

function Invoke-RepoPowerShell {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ScriptPath,
        [Parameter(Mandatory = $true)]
        [hashtable]$Params,
        [string]$Label = "powershell"
    )
    Write-Host ""
    Write-Host "=== $Label ==="
    & $ScriptPath @Params
}

function Add-ExistingPath {
    param(
        [System.Collections.ArrayList]$List,
        [string]$Path
    )
    if ($Path -and (Test-Path $Path)) {
        [void]$List.Add($Path)
    }
}

function Read-JsonFile {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        return $null
    }
    return Get-Content $Path -Raw | ConvertFrom-Json
}

$Reports = [System.Collections.ArrayList]@()
$Artifacts = [System.Collections.ArrayList]@()
$Warnings = [System.Collections.ArrayList]@()
$Errors = [System.Collections.ArrayList]@()

$Evidence = ".\output\ai_pipeline\agent_review_evidence_sufficiency.json"
$RefinedReview = ".\output\ai_pipeline\local_ai_core_tool_activation_megalithic_refined_review_v3.json"
$MemoryWorkflow = ".\output\validation\full_memory_tool_regeneration_${Stamp}_workflow.json"
$MemoryBundleJson = ".\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_bundle_${Stamp}.json"
$MemoryBundleMd = ".\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_bundle_${Stamp}.md"
$MemoryLineCountCsv = ".\docs\LOCAL_VALIDATION_EVIDENCE\full_memory_tool_regeneration_python_line_count_${Stamp}.csv"

$LineCountJson = ".\output\validation\python_line_count_full_toolbox_$Stamp.json"
$LineCountMd = ".\output\validation\python_line_count_full_toolbox_$Stamp.md"
$LineCountAllMd = ".\output\validation\python_line_count_all_python_files_$Stamp.md"
$PythonSyntaxJson = ".\output\validation\python_syntax_full_toolbox_$Stamp.json"
$CodeInterpreterJson = ".\output\analysis\code_interpreter_full_toolbox_$Stamp.json"
$CodeInterpreterMd = ".\output\analysis\code_interpreter_full_toolbox_$Stamp.md"
$GpuContractSmokeJson = ".\output\validation\gpu_planner_json_contract_smoke_full_toolbox_$Stamp.json"
$GpuContractSmokeMd = ".\output\validation\gpu_planner_json_contract_smoke_full_toolbox_$Stamp.md"
$DeterministicSmokeJson = ".\output\validation\deterministic_recommendation_synthesizer_smoke_full_toolbox_$Stamp.json"
$DeterministicSmokeMd = ".\output\validation\deterministic_recommendation_synthesizer_smoke_full_toolbox_$Stamp.md"
$DecisionLoopSmokeJson = ".\output\validation\agent_review_decision_loop_smoke_full_toolbox_$Stamp.json"
$DecisionLoopSmokeMd = ".\output\validation\agent_review_decision_loop_smoke_full_toolbox_$Stamp.md"
$NpuEnvJson = ".\output\validation\npu_provider_environment_full_toolbox_$Stamp.json"
$NpuEnvMd = ".\output\validation\npu_provider_environment_full_toolbox_$Stamp.md"
$RepositoryConsistencyJson = ".\output\analysis\repository_consistency_map_full_toolbox_$Stamp.json"
$RepositoryConsistencyMd = ".\output\analysis\repository_consistency_map_full_toolbox_$Stamp.md"
$RepositoryConsistencySmokeJson = ".\output\validation\repository_consistency_map_smoke_full_toolbox_$Stamp.json"
$RepositoryConsistencySmokeMd = ".\output\validation\repository_consistency_map_smoke_full_toolbox_$Stamp.md"

$OrchOut = ".\output\ai_pipeline\full_toolbox_${Stamp}_orchestrator.json"
$OrchMd = ".\output\ai_pipeline\full_toolbox_${Stamp}_orchestrator.md"
$GpuOut = ".\output\ai_pipeline\full_toolbox_${Stamp}_parallel_gpu.json"
$GpuMd = ".\output\ai_pipeline\full_toolbox_${Stamp}_parallel_gpu.md"
$CheckpointDir = ".\output\ai_pipeline\full_toolbox_${Stamp}_checkpoints"
$GpuReplayJson = ".\output\analysis\gpu_json_contract_replay_full_toolbox_$Stamp.json"
$GpuReplayMd = ".\output\analysis\gpu_json_contract_replay_full_toolbox_$Stamp.md"
$GpuNpuSyncJson = ".\output\analysis\gpu_npu_run_sync_full_toolbox_$Stamp.json"
$GpuNpuSyncMd = ".\output\analysis\gpu_npu_run_sync_full_toolbox_$Stamp.md"

$RecommendationsJson = ".\output\ai_pipeline\full_toolbox_${Stamp}_deterministic_recommendations.json"
$RecommendationsMd = ".\output\ai_pipeline\full_toolbox_${Stamp}_deterministic_recommendations.md"
$BridgeJson = ".\output\ai_pipeline\full_toolbox_${Stamp}_bridge_orchestrator.json"
$PatchPlanJson = ".\output\patch_specs\full_toolbox_${Stamp}_agent_review_patch_plan.json"
$PatchPlanMd = ".\output\patch_specs\full_toolbox_${Stamp}_agent_review_patch_plan.md"
$DecisionLoopJson = ".\output\ai_pipeline\full_toolbox_${Stamp}_agent_review_decision_loop.json"
$DecisionLoopMd = ".\output\ai_pipeline\full_toolbox_${Stamp}_agent_review_decision_loop.md"

$BundleBase = "full_toolbox_agent_review_decision_loop_$Stamp"
$BundleJson = ".\docs\LOCAL_VALIDATION_EVIDENCE\$BundleBase.json"
$BundleMd = ".\docs\LOCAL_VALIDATION_EVIDENCE\$BundleBase.md"
$BundleValidationJson = ".\output\validation\full_toolbox_agent_review_decision_loop_${Stamp}_bundle_validation.json"
$FinalPythonSyntaxJson = ".\output\validation\python_syntax_full_toolbox_final_$Stamp.json"
$FinalContractJson = ".\output\validation\validation_report_contract_full_toolbox_final_$Stamp.json"
$WorkflowJson = ".\output\validation\agent_review_full_toolbox_decision_loop_${Stamp}_workflow.json"
$WorkflowMd = ".\output\validation\agent_review_full_toolbox_decision_loop_${Stamp}_workflow.md"

Write-Host "=== Agent Review Full Toolbox Decision Loop ==="
Write-Host "Repo: $RepoRootPath"
Write-Host "Stamp: $Stamp"
Write-Host "RunGpuNpuProvider: $RunGpuNpuProvider"
Write-Host "SkipRepositoryConsistencyMap: $SkipRepositoryConsistencyMap"
Write-Host "Guardrail: report-only decision loop; provider execution only when -RunGpuNpuProvider is explicitly supplied."

if (-not $SkipMemoryReload) {
    Invoke-RepoPowerShell -Label "Full memory/tool regeneration" -ScriptPath ".\Tools\workflow\run_full_memory_tool_regeneration.ps1" -Params @{
        RepoRoot = "."
        Stamp = $Stamp
        Profile = "full_refactor"
        Objective = "Reload IA-Carmine full toolbox context before agent review full toolbox decision-loop run."
    }
} else {
    [void]$Warnings.Add("memory/tool regeneration skipped by request")
}

Invoke-RepoPython -Label "Full Python line-count inventory" -ArgsList @(
    ".\Tools\validation\build_python_line_count_csv.py",
    "--repo-root", ".",
    "--timestamped",
    "--report-output", $LineCountJson,
    "--markdown-output", $LineCountMd
)

$LineCountReport = Read-JsonFile $LineCountJson
$LineCountCsv = $LineCountReport.csv_written
if (-not $LineCountCsv) {
    throw "Unable to resolve line-count CSV from $LineCountJson"
}

$Rows = Import-Csv $LineCountCsv | Sort-Object {[int]$_.Lines} -Descending
$TotalLines = ($Rows | Measure-Object -Property Lines -Sum).Sum
$FileCount = ($Rows | Measure-Object).Count
$LineInventory = @()
$LineInventory += "# Full Python Line Count Inventory"
$LineInventory += ""
$LineInventory += "- Stamp: $Stamp"
$LineInventory += "- CSV: $LineCountCsv"
$LineInventory += "- File count: $FileCount"
$LineInventory += "- Total Python lines: $TotalLines"
$LineInventory += "- Visibility rule: all counted Python files are listed below; do not truncate to top 10/top 20."
$LineInventory += ""
$LineInventory += "| Lines | File |"
$LineInventory += "|---:|---|"
foreach ($Row in $Rows) {
    $LineInventory += "| $($Row.Lines) | ``$($Row.File)`` |"
}
$LineInventory | Set-Content -Path $LineCountAllMd -Encoding UTF8

Invoke-RepoPython -Label "Python syntax validation" -ArgsList @(
    "-m", "Tools.validation.check_python_syntax",
    "--repo-root", ".",
    "--output", $PythonSyntaxJson
)

Invoke-RepoPython -Label "Code interpreter/static report" -ArgsList @(
    "-m", "Tools.ai.build_code_interpreter_report",
    "--repo-root", ".",
    "--input", "Tools/ai",
    "--input", "Tools/validation",
    "--input", "Tools/npu",
    "--input", "Tools/workflow",
    "--input", "Scripting/v61b",
    "--input", "Scripting/shared",
    "--output", $CodeInterpreterJson,
    "--markdown-output", $CodeInterpreterMd
)

Invoke-RepoPython -Label "Contract script compile" -ArgsList @(
    "-m", "py_compile",
    ".\Tools\ai\gpu_planner_json_contract.py",
    ".\Tools\ai\replay_gpu_planner_json_contract.py",
    ".\Tools\ai\analyze_gpu_npu_run_sync.py",
    ".\Tools\ai\build_deterministic_recommendations.py",
    ".\Tools\ai\build_agent_review_patch_plan.py",
    ".\Tools\ai\run_agent_review_decision_loop.py",
    ".\Tools\ai\build_repository_consistency_map.py",
    ".\Tools\validation\run_repository_consistency_map_smoke.py",
    ".\Tools\validation\run_gpu_planner_json_contract_smoke.py",
    ".\Tools\validation\run_deterministic_recommendation_synthesizer_smoke.py",
    ".\Tools\validation\run_agent_review_decision_loop_smoke.py"
)

Invoke-RepoPython -Label "GPU planner JSON contract smoke" -ArgsList @(
    ".\Tools\validation\run_gpu_planner_json_contract_smoke.py",
    "--repo-root", ".",
    "--output", $GpuContractSmokeJson,
    "--markdown-output", $GpuContractSmokeMd
)

Invoke-RepoPython -Label "Deterministic recommendation synthesizer smoke" -ArgsList @(
    ".\Tools\validation\run_deterministic_recommendation_synthesizer_smoke.py",
    "--repo-root", ".",
    "--output", $DeterministicSmokeJson,
    "--markdown-output", $DeterministicSmokeMd
)

Invoke-RepoPython -Label "Agent review decision-loop smoke" -ArgsList @(
    ".\Tools\validation\run_agent_review_decision_loop_smoke.py",
    "--repo-root", ".",
    "--output", $DecisionLoopSmokeJson,
    "--markdown-output", $DecisionLoopSmokeMd
)

Invoke-RepoPython -Label "NPU provider environment preflight" -ArgsList @(
    ".\Tools\ai\check_npu_provider_environment.py",
    "--repo-root", ".",
    "--output", $NpuEnvJson,
    "--markdown-output", $NpuEnvMd
)

if (-not $SkipRepositoryConsistencyMap) {
    Invoke-RepoPython -Label "Repository consistency map" -ArgsList @(
        ".\Tools\ai\build_repository_consistency_map.py",
        "--repo-root", ".",
        "--output", $RepositoryConsistencyJson,
        "--markdown-output", $RepositoryConsistencyMd
    )

    Invoke-RepoPython -Label "Repository consistency map smoke" -ArgsList @(
        ".\Tools\validation\run_repository_consistency_map_smoke.py",
        "--repo-root", ".",
        "--output", $RepositoryConsistencySmokeJson,
        "--markdown-output", $RepositoryConsistencySmokeMd
    )
} else {
    [void]$Warnings.Add("repository consistency map skipped by request")
}

if ($RunGpuNpuProvider) {
    Invoke-RepoPython -Label "GPU primary advisory + NPU auditor orchestrator" -ArgsList @(
        ".\Tools\ai\run_agent_gpu_npu_parallel_orchestrator.py",
        "--repo-root", ".",
        "--budget-minutes", "$BudgetMinutes",
        "--max-rounds", "$MaxRounds",
        "--files-per-round", "$FilesPerRound",
        "--max-context-files", "$MaxContextFiles",
        "--max-chars-per-file", "$MaxCharsPerFile",
        "--max-new-tokens", "$MaxNewTokens",
        "--keep-alive", $KeepAlive,
        "--evidence", $Evidence,
        "--refined-review", $RefinedReview,
        "--report-file", ".\output\ai_pipeline\local_ai_core_tool_activation_agent_memory_inventory.json",
        "--report-file", ".\output\ai_pipeline\local_ai_core_tool_activation_agnostic_tool_inventory.json",
        "--report-file", ".\output\ai_pipeline\local_ai_core_tool_activation_transient_request_context.json",
        "--report-file", ".\output\ai_packets\gpu_planner_nonempty_recommendations_advisory_manifest.json",
        "--report-file", ".\output\ai_packets\gpu_planner_nonempty_recommendations_proposals.json",
        "--report-file", $RepositoryConsistencyJson,
        "--report-file", $RepositoryConsistencySmokeJson,
        "--report-file", $CodeInterpreterJson,
        "--report-file", $LineCountJson,
        "--report-file", $PythonSyntaxJson,
        "--report-file", $GpuContractSmokeJson,
        "--report-file", $DeterministicSmokeJson,
        "--report-file", $DecisionLoopSmokeJson,
        "--report-file", $NpuEnvJson,
        "--report-file", $MemoryWorkflow,
        "--context-root", "docs",
        "--context-root", "Tools\ai",
        "--context-root", "Tools\validation",
        "--context-root", "Tools\workflow",
        "--context-root", "Tools\npu",
        "--context-root", "Scripting\v61b",
        "--context-root", "Scripting\shared",
        "--context-root", $LineCountAllMd,
        "--run-npu-auditor-provider",
        "--npu-auditor-every-rounds", "$NpuAuditorEveryRounds",
        "--max-concurrent-npu-audits", "1",
        "--npu-auditor-timeout-seconds", "$NpuAuditorTimeoutSeconds",
        "--npu-max-context-chars", "$NpuMaxContextChars",
        "--npu-max-prompt-chars", "$NpuMaxPromptChars",
        "--npu-max-new-tokens", "$NpuMaxNewTokens",
        "--npu-final-wait-seconds", "$NpuFinalWaitSeconds",
        "--checkpoint-dir", $CheckpointDir,
        "--gpu-output", $GpuOut,
        "--gpu-markdown-output", $GpuMd,
        "--output", $OrchOut,
        "--markdown-output", $OrchMd
    )
} else {
    [void]$Warnings.Add("GPU/NPU provider orchestrator skipped; rerun with -RunGpuNpuProvider for full provider execution.")
    if ((Test-Path ".\output\ai_pipeline\post_pr167_retry_pass_20260503-143243_orchestrator.json") -and (Test-Path ".\output\ai_pipeline\post_pr167_retry_pass_20260503-143243_parallel_gpu.json")) {
        $OrchOut = ".\output\ai_pipeline\post_pr167_retry_pass_20260503-143243_orchestrator.json"
        $GpuOut = ".\output\ai_pipeline\post_pr167_retry_pass_20260503-143243_parallel_gpu.json"
    }
}

if (Test-Path $GpuOut) {
    Invoke-RepoPython -Label "Replay GPU planner JSON contract" -ArgsList @(
        ".\Tools\ai\replay_gpu_planner_json_contract.py",
        "--repo-root", ".",
        "--gpu-report", $GpuOut,
        "--output", $GpuReplayJson,
        "--markdown-output", $GpuReplayMd
    )
}

if (Test-Path $OrchOut) {
    Invoke-RepoPython -Label "Analyze GPU/NPU run sync" -ArgsList @(
        ".\Tools\ai\analyze_gpu_npu_run_sync.py",
        "--repo-root", ".",
        "--orchestrator", $OrchOut,
        "--output", $GpuNpuSyncJson,
        "--markdown-output", $GpuNpuSyncMd
    )
}

$ToolReports = @(
    $RepositoryConsistencyJson,
    $RepositoryConsistencySmokeJson,
    $CodeInterpreterJson,
    $LineCountJson,
    $PythonSyntaxJson,
    $GpuContractSmokeJson,
    $DeterministicSmokeJson,
    $DecisionLoopSmokeJson,
    $NpuEnvJson,
    $GpuReplayJson,
    $GpuNpuSyncJson,
    $MemoryWorkflow
) | Where-Object { Test-Path $_ }

$DecisionArgs = @(
    ".\Tools\ai\run_agent_review_decision_loop.py",
    "--repo-root", ".",
    "--evidence", $Evidence,
    "--orchestrator", $OrchOut,
    "--gpu-report", $GpuOut,
    "--recommendations-output", $RecommendationsJson,
    "--recommendations-markdown", $RecommendationsMd,
    "--bridge-orchestrator-output", $BridgeJson,
    "--patch-plan-output", $PatchPlanJson,
    "--patch-plan-markdown", $PatchPlanMd,
    "--output", $DecisionLoopJson,
    "--markdown-output", $DecisionLoopMd,
    "--min-recommendations", "$MinRecommendations",
    "--min-patch-plans", "$MinPatchPlans"
)
foreach ($Report in $ToolReports) {
    $DecisionArgs += @("--tool-report", $Report)
}
Invoke-RepoPython -Label "Agent review decision loop" -ArgsList $DecisionArgs

if (-not $SkipPostValidationPacket) {
    $ContextFiles = @(
        ".\docs\LOCAL_AI_TASKS\code-refactor-0-to-10-procedure.md",
        ".\docs\LOCAL_AI_TASKS\gpu-npu-parallel-evidence-runbook.md",
        ".\docs\LOCAL_AI_TASKS\project-complete-ai-to-ai-procedure.md",
        ".\Tools\ai\run_agent_review_decision_loop.py",
        ".\Tools\ai\build_deterministic_recommendations.py",
        ".\Tools\ai\build_agent_review_patch_plan.py",
        ".\Tools\ai\run_agent_gpu_npu_parallel_orchestrator.py",
        ".\Tools\validation\run_agent_review_decision_loop_smoke.py",
        $RepositoryConsistencyMd,
        $RepositoryConsistencySmokeMd,
        $LineCountAllMd,
        $CodeInterpreterMd,
        $GpuReplayMd,
        $GpuNpuSyncMd,
        $DecisionLoopMd,
        $PatchPlanMd
    ) | Where-Object { Test-Path $_ }
    $ReportFiles = @(
        $OrchOut,
        $GpuOut,
        $RepositoryConsistencyJson,
        $RepositoryConsistencySmokeJson,
        $CodeInterpreterJson,
        $LineCountJson,
        $PythonSyntaxJson,
        $GpuContractSmokeJson,
        $DeterministicSmokeJson,
        $DecisionLoopSmokeJson,
        $NpuEnvJson,
        $GpuReplayJson,
        $GpuNpuSyncJson,
        $RecommendationsJson,
        $BridgeJson,
        $DecisionLoopJson,
        $PatchPlanJson,
        $MemoryWorkflow
    ) | Where-Object { Test-Path $_ }
    Invoke-RepoPowerShell -Label "Post-validation AI packet" -ScriptPath ".\Tools\workflow\run_post_validation_ai_packet.ps1" -Params @{
        Profile = "core"
        ContextFile = $ContextFiles
        ReportFile = $ReportFiles
    }
} else {
    [void]$Warnings.Add("post-validation AI packet skipped by request")
}

if (-not $SkipSharedToolboxBundle) {
    Invoke-RepoPython -Label "Shared toolbox AI-to-AI bundle" -ArgsList @(
        "-m", "Tools.ai.build_shared_toolbox_ai_to_ai_bundle",
        "--repo-root", ".",
        "--stamp", $Stamp,
        "--output-dir", $EvidenceDir,
        "--validate-bundle",
        "--recursive-max-files", "160",
        "--chunk-large-files-lines", "200"
    )
} else {
    [void]$Warnings.Add("shared toolbox bundle skipped by request")
}

$ReportFilesForBundle = @(
    $OrchOut,
    $GpuOut,
    $RepositoryConsistencyJson,
    $RepositoryConsistencySmokeJson,
    $CodeInterpreterJson,
    $LineCountJson,
    $PythonSyntaxJson,
    $GpuContractSmokeJson,
    $DeterministicSmokeJson,
    $DecisionLoopSmokeJson,
    $NpuEnvJson,
    $GpuReplayJson,
    $GpuNpuSyncJson,
    $RecommendationsJson,
    $BridgeJson,
    $DecisionLoopJson,
    $PatchPlanJson,
    ".\output\ai_pipeline\repository_change_proposals.json",
    ".\output\ai_packets\gpu_planner_nonempty_recommendations_advisory.json",
    ".\output\ai_packets\gpu_planner_nonempty_recommendations_proposals.json",
    $MemoryWorkflow
) | Where-Object { Test-Path $_ }

$BundleArgs = @(
    "-m", "Tools.ai.build_github_evidence_bundle",
    "--repo-root", ".",
    "--basename", $BundleBase,
    "--output-dir", $EvidenceDir,
    "--report", (($ReportFilesForBundle | ForEach-Object { [string]$_ }) -join ","),
    "--artifact", ".\docs\LOCAL_AI_TASKS\code-refactor-0-to-10-procedure.md",
    "--artifact", ".\docs\LOCAL_AI_TASKS\gpu-npu-parallel-evidence-runbook.md",
    "--artifact", ".\Tools\ai\run_agent_review_decision_loop.py",
    "--artifact", ".\Tools\validation\run_agent_review_decision_loop_smoke.py",
    "--artifact", $RepositoryConsistencyMd,
    "--artifact", $RepositoryConsistencySmokeMd,
    "--artifact", $LineCountAllMd,
    "--artifact", $LineCountCsv,
    "--artifact", $DecisionLoopMd,
    "--artifact", $PatchPlanMd,
    "--max-included-artifact-chars", "16000",
    "--max-included-artifacts", "24"
)
Invoke-RepoPython -Label "Full toolbox GitHub evidence bundle" -ArgsList $BundleArgs

Invoke-RepoPython -Label "Validate full toolbox GitHub evidence bundle" -ArgsList @(
    "-m", "Tools.validation.check_github_evidence_bundle",
    "--repo-root", ".",
    "--bundle", $BundleJson,
    "--output", $BundleValidationJson
)

Invoke-RepoPython -Label "Final Python syntax validation" -ArgsList @(
    "-m", "Tools.validation.check_python_syntax",
    "--repo-root", ".",
    "--output", $FinalPythonSyntaxJson
)

Invoke-RepoPython -Label "Final scoped validation report contract" -ArgsList @(
    ".\Tools\validation\check_validation_report_contract.py",
    "--repo-root", ".",
    "--report-file", $DecisionLoopSmokeJson,
    "--report-file", $RepositoryConsistencySmokeJson,
    "--report-file", $FinalPythonSyntaxJson,
    "--report-file", $BundleValidationJson,
    "--output", $FinalContractJson
)

foreach ($Path in @(
    $MemoryWorkflow, $RepositoryConsistencyJson, $RepositoryConsistencySmokeJson, $LineCountJson, $PythonSyntaxJson, $CodeInterpreterJson, $GpuContractSmokeJson,
    $DeterministicSmokeJson, $DecisionLoopSmokeJson, $NpuEnvJson, $OrchOut, $GpuOut, $GpuReplayJson,
    $GpuNpuSyncJson, $RecommendationsJson, $BridgeJson, $DecisionLoopJson, $PatchPlanJson,
    $BundleValidationJson, $FinalPythonSyntaxJson, $FinalContractJson
)) {
    Add-ExistingPath -List $Reports -Path $Path
}
foreach ($Path in @(
    $MemoryBundleJson, $MemoryBundleMd, $MemoryLineCountCsv, $RepositoryConsistencyMd, $RepositoryConsistencySmokeMd, $LineCountAllMd, $LineCountCsv,
    $CodeInterpreterMd, $GpuContractSmokeMd, $DeterministicSmokeMd, $DecisionLoopSmokeMd,
    $NpuEnvMd, $OrchMd, $GpuMd, $GpuReplayMd, $GpuNpuSyncMd, $RecommendationsMd,
    $DecisionLoopMd, $PatchPlanMd, $BundleJson, $BundleMd
)) {
    Add-ExistingPath -List $Artifacts -Path $Path
}

foreach ($ReportPath in $Reports) {
    $Data = Read-JsonFile $ReportPath
    if ($Data -and ($null -ne $Data.passed) -and ($Data.passed -eq $false)) {
        [void]$Errors.Add("${ReportPath}: passed=false")
    }
}

$DecisionSummary = Read-JsonFile $DecisionLoopJson
$BundleValidation = Read-JsonFile $BundleValidationJson
$WorkflowPassed = ($Errors.Count -eq 0)
$WorkflowReport = [ordered]@{
    schema_version = 1
    kind = "agent_review_full_toolbox_decision_loop_workflow"
    generated_at = (Get-Date).ToString("s")
    repo_root = "$RepoRootPath"
    stamp = $Stamp
    passed = $WorkflowPassed
    errors = @($Errors)
    warnings = @($Warnings)
    provider_execution_performed = [bool]$RunGpuNpuProvider
    patch_application_performed = $false
    source_writes_performed = $false
    sqlite_write_performed = $false
    persistent_memory_write_performed = $false
    manual_review_required = $true
    recommendation_count = if ($DecisionSummary) { $DecisionSummary.recommendation_count } else { $null }
    patch_plan_count = if ($DecisionSummary) { $DecisionSummary.patch_plan_count } else { $null }
    deterministic_synthesizer_used = if ($DecisionSummary) { $DecisionSummary.deterministic_synthesizer_used } else { $null }
    patch_plan_fallback_used = if ($DecisionSummary) { $DecisionSummary.patch_plan_fallback_used } else { $null }
    bundle_validation_passed = if ($BundleValidation) { $BundleValidation.passed } else { $null }
    report_count = $Reports.Count
    artifact_count = $Artifacts.Count
    reports = @($Reports)
    artifacts = @($Artifacts)
    evidence_to_commit = @(
        $MemoryBundleJson,
        $MemoryBundleMd,
        $MemoryLineCountCsv,
        $LineCountCsv,
        $BundleJson,
        $BundleMd,
        ".\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_ai_to_ai_bundle_$Stamp.json",
        ".\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_ai_to_ai_bundle_$Stamp.md"
    ) | Where-Object { Test-Path $_ }
    guardrails = [ordered]@{
        provider_execution_requires_explicit_flag = $true
        run_gpu_npu_provider = [bool]$RunGpuNpuProvider
        patch_application_performed = $false
        source_writes_performed = $false
        sqlite_write_performed = $false
        persistent_memory_write_performed = $false
        blender_runtime_execution_performed = $false
        raw_output_commit_allowed = $false
    }
}
$WorkflowReport | ConvertTo-Json -Depth 8 | Set-Content -Path $WorkflowJson -Encoding UTF8

$EvidenceLines = @($WorkflowReport.evidence_to_commit | ForEach-Object { "- ``$_``" })
$WorkflowMarkdown = @(
    "# Agent Review Full Toolbox Decision Loop Workflow",
    "",
    "- Passed: ``$WorkflowPassed``",
    "- Stamp: ``$Stamp``",
    "- Provider execution performed: ``$([bool]$RunGpuNpuProvider)``",
    "- Patch application performed: ``False``",
    "- SQLite write performed: ``False``",
    "- Persistent memory write performed: ``False``",
    "- Recommendation count: ``$($WorkflowReport.recommendation_count)``",
    "- Patch plan count: ``$($WorkflowReport.patch_plan_count)``",
    "- Bundle validation passed: ``$($WorkflowReport.bundle_validation_passed)``",
    "",
    "## Evidence to commit",
    ""
) + $EvidenceLines
$WorkflowMarkdown | Set-Content -Path $WorkflowMd -Encoding UTF8

Write-Host ""
Write-Host "=== Full toolbox decision loop summary ==="
Write-Host "Workflow: $WorkflowJson"
Write-Host "Markdown: $WorkflowMd"
Write-Host "Evidence bundle: $BundleJson"
Write-Host "Evidence markdown: $BundleMd"
Write-Host "Passed: $WorkflowPassed"
Write-Host "Recommendation count: $($WorkflowReport.recommendation_count)"
Write-Host "Patch plan count: $($WorkflowReport.patch_plan_count)"
Write-Host ""
Write-Host "Git policy: stage only docs/LOCAL_VALIDATION_EVIDENCE outputs listed in workflow evidence_to_commit. Do not stage output/**, *.db or *.sqlite."
