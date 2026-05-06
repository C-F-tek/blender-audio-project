param(
    [string]$RepoRoot = ".",
    [string]$Stamp = "",
    [string]$OutputRoot = "output",
    [string]$EvidenceDir = "docs/LOCAL_VALIDATION_EVIDENCE",
    [switch]$RunGpuNpuProvider,
    [switch]$RequireProviderArtifacts,
    [switch]$SkipMemoryReload,
    [switch]$SkipPostValidationPacket,
    [switch]$SkipSharedToolboxBundle,
    [int]$BudgetMinutes = 30,
    [int]$MaxRounds = 20,
    [int]$FilesPerRound = 8,
    [int]$MaxContextFiles = 220,
    [int]$MaxCharsPerFile = 6000,
    [int]$MaxNewTokens = 3600,
    [int]$MaxRecommendations = 20,
    [int]$MaxPatchPlans = 20,
    [string]$KeepAlive = "35m",
    [int]$NpuAuditorEveryRounds = 3,
    [int]$NpuAuditorTimeoutSeconds = 420,
    [int]$NpuMaxContextChars = 8000,
    [int]$NpuMaxPromptChars = 1200,
    [int]$NpuMaxNewTokens = 384,
    [int]$NpuFinalWaitSeconds = 180,
    [int]$MinRecommendations = 1,
    [int]$MinPatchPlans = 1,
    [int]$RepositoryConsistencyMapWorkers = 8
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


# IA_CARMINE_REQUIRED_PROVIDER_ARTIFACTS_BEGIN
function Write-JsonArtifact {
    param(
        [string]$Path,
        [object]$Payload
    )

    $Parent = Split-Path -Parent $Path
    if ($Parent) {
        New-Item -ItemType Directory -Force -Path $Parent | Out-Null
    }
    ($Payload | ConvertTo-Json -Depth 12) | Set-Content -LiteralPath $Path -Encoding UTF8
}

function Write-TextArtifact {
    param(
        [string]$Path,
        [string[]]$Lines
    )

    $Parent = Split-Path -Parent $Path
    if ($Parent) {
        New-Item -ItemType Directory -Force -Path $Parent | Out-Null
    }
    $Lines | Set-Content -LiteralPath $Path -Encoding UTF8
}

function Ensure-RequiredProviderArtifacts {
    param(
        [string]$StampValue,
        [bool]$RunProvider,
        [bool]$RequireArtifacts,
        [string]$EvidencePath,
        [string]$OrchestratorPath,
        [string]$OrchestratorMarkdownPath,
        [string]$GpuPath,
        [string]$GpuMarkdownPath
    )

    if (-not $RunProvider -or -not $RequireArtifacts) {
        return
    }

    $GeneratedAt = (Get-Date).ToString("o")
    $Missing = @()
    if (-not (Test-Path -LiteralPath $EvidencePath -PathType Leaf)) { $Missing += $EvidencePath }
    if (-not (Test-Path -LiteralPath $OrchestratorPath -PathType Leaf)) { $Missing += $OrchestratorPath }
    if (-not (Test-Path -LiteralPath $GpuPath -PathType Leaf)) { $Missing += $GpuPath }

    if ($Missing.Count -eq 0) {
        return
    }

    foreach ($Item in $Missing) {
        [void]$Errors.Add("required provider artifact missing: $Item")
    }

    if (-not (Test-Path -LiteralPath $OrchestratorPath -PathType Leaf)) {
        $OrchPayload = [ordered]@{
            schema_version = 1
            kind = "agent_gpu_npu_parallel_orchestrator"
            generated_at = $GeneratedAt
            stamp = $StampValue
            passed = $false
            provider_execution_requested = $true
            provider_execution_performed = $false
            patch_application_performed = $false
            source_writes_performed = $false
            classification = "required_provider_artifact_missing"
            reason = "Strict real-run activation required an orchestrator report, but the provider lane did not produce one."
            errors = @("required orchestrator artifact missing before fallback generation")
            warnings = @()
            outputs = [ordered]@{
                evidence = $EvidencePath
                gpu_report = $GpuPath
            }
            guardrails = [ordered]@{
                report_only = $true
                provider_execution_performed = $false
                patch_application_performed = $false
                source_writes_performed = $false
                blender_runtime_execution_performed = $false
                ffmpeg_execution_performed = $false
            }
        }
        Write-JsonArtifact -Path $OrchestratorPath -Payload $OrchPayload
        Write-TextArtifact -Path $OrchestratorMarkdownPath -Lines @(
            "# Required provider orchestrator fallback",
            "",
            '- Passed: `False`',
            '- Provider execution requested: `True`',
            '- Provider execution performed: `False`',
            '- Classification: `required_provider_artifact_missing`',
            "",
            "Strict real-run activation required an orchestrator report, but the provider lane did not produce one."
        )
    }

    if (-not (Test-Path -LiteralPath $GpuPath -PathType Leaf)) {
        $GpuPayload = [ordered]@{
            schema_version = 1
            kind = "agent_gpu_parallel_report"
            generated_at = $GeneratedAt
            stamp = $StampValue
            passed = $false
            provider_execution_requested = $true
            provider_execution_performed = $false
            patch_application_performed = $false
            source_writes_performed = $false
            classification = "required_provider_artifact_missing"
            provider_error = "GPU primary advisory output was required by strict real-run activation but was not produced."
            provider_empty_response = $true
            recommendation_count = 0
            recommendations = @()
            errors = @("required GPU provider artifact missing before fallback generation")
            warnings = @()
            guardrails = [ordered]@{
                report_only = $true
                provider_execution_performed = $false
                patch_application_performed = $false
                source_writes_performed = $false
                blender_runtime_execution_performed = $false
                ffmpeg_execution_performed = $false
            }
        }
        Write-JsonArtifact -Path $GpuPath -Payload $GpuPayload
        Write-TextArtifact -Path $GpuMarkdownPath -Lines @(
            "# Required GPU provider fallback",
            "",
            '- Passed: `False`',
            '- Provider execution requested: `True`',
            '- Provider execution performed: `False`',
            '- Classification: `required_provider_artifact_missing`',
            "",
            "Strict real-run activation required GPU primary advisory output, but the provider lane did not produce it."
        )
    }

    if (-not (Test-Path -LiteralPath $EvidencePath -PathType Leaf)) {
        $EvidencePayload = [ordered]@{
            schema_version = 1
            kind = "agent_review_evidence_sufficiency"
            generated_at = $GeneratedAt
            stamp = $StampValue
            passed = $false
            evidence_sufficient = $false
            provider_execution_requested = $true
            provider_execution_performed = $false
            patch_application_performed = $false
            source_writes_performed = $false
            classification = "required_provider_artifact_missing"
            reason = "Strict real-run activation required evidence sufficiency output, but the provider/orchestrator lane did not produce one."
            errors = @("required evidence sufficiency artifact missing before fallback generation")
            warnings = @()
            checks = [ordered]@{
                orchestrator_report_exists = (Test-Path -LiteralPath $OrchestratorPath -PathType Leaf)
                gpu_report_exists = (Test-Path -LiteralPath $GpuPath -PathType Leaf)
            }
            guardrails = [ordered]@{
                report_only = $true
                provider_execution_performed = $false
                patch_application_performed = $false
                source_writes_performed = $false
                blender_runtime_execution_performed = $false
                ffmpeg_execution_performed = $false
            }
        }
        Write-JsonArtifact -Path $EvidencePath -Payload $EvidencePayload
    }
}
# IA_CARMINE_REQUIRED_PROVIDER_ARTIFACTS_END

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
$EvidenceMd = ".\output\ai_pipeline\agent_review_evidence_sufficiency.md"
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
$ProviderEvidenceContractJson = ".\output\validation\provider_evidence_contract_full_toolbox_$Stamp.json"
$ProviderEvidenceContractMd = ".\output\validation\provider_evidence_contract_full_toolbox_$Stamp.md"
$Gpu0CompanionJson = ".\output\validation\gpu0_companion_task_lane_$Stamp.json"
$Gpu0CompanionMd = ".\output\validation\gpu0_companion_task_lane_$Stamp.md"
$Gpu0CompanionToolRequestsJson = ".\output\validation\gpu0_companion_tool_requests_$Stamp.json"
$Gpu0CompanionContractJson = ".\output\validation\gpu0_companion_contract_$Stamp.json"
$Gpu0CompanionContractMd = ".\output\validation\gpu0_companion_contract_$Stamp.md"

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
$TelemetrySummaryJson = ".\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_run_telemetry_summary_$Stamp.json"
$TelemetrySummaryMd = ".\docs\LOCAL_VALIDATION_EVIDENCE\full_toolbox_run_telemetry_summary_$Stamp.md"
$RuntimeToolTelemetryJson = ".\docs\LOCAL_VALIDATION_EVIDENCE\runtime_tool_usage_telemetry_$Stamp.json"
$RuntimeToolTelemetryMd = ".\docs\LOCAL_VALIDATION_EVIDENCE\runtime_tool_usage_telemetry_$Stamp.md"
$RuntimeToolCapabilityJson = ".\docs\LOCAL_VALIDATION_EVIDENCE\runtime_tool_capability_manifest_$Stamp.json"
$RuntimeToolCapabilityMd = ".\docs\LOCAL_VALIDATION_EVIDENCE\runtime_tool_capability_manifest_$Stamp.md"
$RuntimeToolBootstrapRequestJson = ".\output\validation\runtime_tool_bootstrap_requests_$Stamp.json"
$RuntimeToolBrokerJson = ".\output\validation\runtime_tool_broker_full_toolbox_$Stamp.json"
$RuntimeToolBrokerMd = ".\output\validation\runtime_tool_broker_full_toolbox_$Stamp.md"
$RuntimeToolOutputDir = ".\output\ai_runtime_tools\$Stamp"
$EvidenceChunkBase = "full_toolbox_${Stamp}_cloud_semantic_deterministic"
$EvidenceChunkDir = ".\docs\LOCAL_VALIDATION_EVIDENCE\${EvidenceChunkBase}_chunks"
$EvidenceChunkManifestJson = ".\docs\LOCAL_VALIDATION_EVIDENCE\${EvidenceChunkBase}_chunk_manifest.json"
$EvidenceChunkManifestMd = ".\docs\LOCAL_VALIDATION_EVIDENCE\${EvidenceChunkBase}_chunk_manifest.md"
$EvidenceChunkZip = ".\output\validation\${EvidenceChunkBase}_chunks.zip"

Write-Host "=== Agent Review Full Toolbox Decision Loop ==="
Write-Host "Repo: $RepoRootPath"
Write-Host "Stamp: $Stamp"
Write-Host "RunGpuNpuProvider: $RunGpuNpuProvider"
Write-Host "RequireProviderArtifacts: $RequireProviderArtifacts"
Write-Host "RepositoryConsistencyMapWorkers: $RepositoryConsistencyMapWorkers"
Write-Host "MaxRecommendations: $MaxRecommendations"
Write-Host "MaxPatchPlans: $MaxPatchPlans"
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
    ".\Tools\ai\build_full_toolbox_run_telemetry_summary.py",
    ".\Tools\ai\build_runtime_tool_usage_telemetry.py",
    ".\Tools\ai\build_runtime_tool_capability_manifest.py",
    ".\Tools\ai\build_semantic_evidence_chunks.py",
    ".\Tools\ai\build_agent_review_evidence_sufficiency.py",
    ".\Tools\ai\run_agent_review_decision_loop.py",
    ".\Tools\ai\build_repository_consistency_map.py",
    ".\Tools\validation\run_repository_consistency_map_smoke.py",
    ".\Tools\validation\run_gpu_planner_json_contract_smoke.py",
    ".\Tools\validation\run_deterministic_recommendation_synthesizer_smoke.py",
    ".\Tools\validation\run_agent_review_decision_loop_smoke.py",
    ".\Tools\validation\check_provider_evidence_contract.py"
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

Invoke-RepoPython -Label "Repository consistency map" -ArgsList @(
    ".\Tools\ai\build_repository_consistency_map.py",
    "--repo-root", ".",
    "--output", $RepositoryConsistencyJson,
    "--markdown-output", $RepositoryConsistencyMd,
    "--workers", "$RepositoryConsistencyMapWorkers"
)

Invoke-RepoPython -Label "Repository consistency map smoke" -ArgsList @(
    ".\Tools\validation\run_repository_consistency_map_smoke.py",
    "--repo-root", ".",
    "--map-report", $RepositoryConsistencyJson,
    "--output", $RepositoryConsistencySmokeJson,
    "--markdown-output", $RepositoryConsistencySmokeMd,
    "--workers", "$RepositoryConsistencyMapWorkers"
)

Invoke-RepoPython -Label "Agent review evidence sufficiency" -ArgsList @(
    ".\Tools\ai\build_agent_review_evidence_sufficiency.py",
    "--repo-root", ".",
    "--refined-review", $RefinedReview,
    "--report-file", $RepositoryConsistencyJson,
    "--report-file", $RepositoryConsistencySmokeJson,
    "--report-file", $CodeInterpreterJson,
    "--report-file", $LineCountJson,
    "--report-file", $PythonSyntaxJson,
    "--output", $Evidence,
    "--markdown-output", $EvidenceMd
)

Invoke-RepoPython -Label "GPU0 companion worker task lane" -ArgsList @(
    ".\Tools\ai\build_gpu0_companion_task_lane.py",
    "--repo-root", ".",
    "--stamp", $Stamp,
    "--output", $Gpu0CompanionJson,
    "--markdown-output", $Gpu0CompanionMd,
    "--tool-requests-output", $Gpu0CompanionToolRequestsJson,
    "--source-report", $Evidence,
    "--source-report", $RepositoryConsistencyJson,
    "--source-report", $RepositoryConsistencySmokeJson,
    "--source-report", $CodeInterpreterJson,
    "--source-report", $LineCountJson,
    "--source-report", $PythonSyntaxJson,
    "--source-report", $NpuEnvJson
)

Invoke-RepoPython -Label "GPU0 companion worker contract" -ArgsList @(
    ".\Tools\validation\check_gpu0_companion_contract.py",
    "--report", $Gpu0CompanionJson,
    "--output", $Gpu0CompanionContractJson,
    "--markdown-output", $Gpu0CompanionContractMd
)

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
        "--report-file", $Gpu0CompanionJson,
        "--report-file", $Gpu0CompanionContractJson,
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

Ensure-RequiredProviderArtifacts -StampValue $Stamp `
    -RunProvider ([bool]$RunGpuNpuProvider) `
    -RequireArtifacts ([bool]$RequireProviderArtifacts) `
    -EvidencePath $Evidence `
    -OrchestratorPath $OrchOut `
    -OrchestratorMarkdownPath $OrchMd `
    -GpuPath $GpuOut `
    -GpuMarkdownPath $GpuMd

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

if ($RunGpuNpuProvider) {
    $ProviderEvidenceArgs = @(
        ".\Tools\validation\check_provider_evidence_contract.py",
        "--repo-root", ".",
        "--stamp", $Stamp,
        "--orchestrator", $OrchOut,
        "--gpu-report", $GpuOut,
        "--gpu-npu-sync", $GpuNpuSyncJson,
        "--local-provider-probe", ".\output\validation\local_provider_probe.json",
        "--output", $ProviderEvidenceContractJson,
        "--markdown-output", $ProviderEvidenceContractMd
    )
    if ($RequireProviderArtifacts) {
        $ProviderEvidenceArgs += @("--require-gpu-provider", "--require-npu-auditor")
    }
    Invoke-RepoPython -Label "Strict provider evidence contract" -ArgsList $ProviderEvidenceArgs
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
    $ProviderEvidenceContractJson,
    $Gpu0CompanionJson,
    $Gpu0CompanionContractJson,
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
    "--min-patch-plans", "$MinPatchPlans",
    "--max-recommendations", "$MaxRecommendations",
    "--max-patch-plans", "$MaxPatchPlans"
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
        $ProviderEvidenceContractMd,
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
        $ProviderEvidenceContractJson,
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


# IA_CARMINE_RUNTIME_TOOL_BROKER_BOOTSTRAP_BEGIN
$RuntimeToolBootstrapPayload = [ordered]@{
    schema_version = 1
    kind = "runtime_tool_bootstrap_requests"
    generated_at = (Get-Date).ToString("o")
    stamp = $Stamp
    purpose = "Exercise minimal report-only runtime tool broker activation during full-toolbox runs."
    provider_execution_performed = $false
    patch_application_performed = $false
    source_writes_performed = $false
    tool_requests = @(
        [ordered]@{
            id = "full_toolbox_bootstrap_python_syntax"
            tool = "check_python_syntax"
            reason = "Exercise brokered Python syntax validation as a report-only runtime tool."
            args = [ordered]@{}
        },
        [ordered]@{
            id = "full_toolbox_bootstrap_python_line_count"
            tool = "build_python_line_count_csv"
            reason = "Exercise brokered Python inventory as a report-only runtime tool."
            args = [ordered]@{
                exclude_dir = ".venv,venv,__pycache__"
            }
        },
        [ordered]@{
            id = "full_toolbox_bootstrap_validation_contract"
            tool = "check_validation_report_contract"
            reason = "Exercise brokered validation report contract check against full-run decision outputs."
            args = [ordered]@{
                report_file = "$DecisionLoopJson,$PatchPlanJson"
            }
        }
    )
}
Write-JsonArtifact -Path $RuntimeToolBootstrapRequestJson -Payload $RuntimeToolBootstrapPayload

Invoke-RepoPython -Label "Runtime tool broker bootstrap activation" -ArgsList @(
    ".\Tools\ai\agent_runtime_tool_broker.py",
    "--repo-root", ".",
    "--request-file", $RuntimeToolBootstrapRequestJson,
    "--tool-output-dir", $RuntimeToolOutputDir,
    "--stamp", $Stamp,
    "--timeout-seconds", "240",
    "--output", $RuntimeToolBrokerJson,
    "--markdown-output", $RuntimeToolBrokerMd
)
Add-ExistingPath -List $Reports -Path $RuntimeToolBrokerJson
Add-ExistingPath -List $Artifacts -Path $RuntimeToolBrokerMd

Invoke-RepoPython -Label "Runtime tool usage telemetry pre-bundle" -ArgsList @(
    ".\Tools\ai\build_runtime_tool_usage_telemetry.py",
    "--repo-root", ".",
    "--stamp", $Stamp,
    "--orchestrator", $OrchOut,
    "--gpu-report", $GpuOut,
    "--gpu-npu-sync", $GpuNpuSyncJson,
    "--decision-loop", $DecisionLoopJson,
    "--broker-report", $RuntimeToolBrokerJson,
    "--output", $RuntimeToolTelemetryJson,
    "--markdown-output", $RuntimeToolTelemetryMd
)

Invoke-RepoPython -Label "Runtime tool capability manifest pre-bundle" -ArgsList @(
    ".\Tools\ai\build_runtime_tool_capability_manifest.py",
    "--repo-root", ".",
    "--tool-usage", $RuntimeToolTelemetryJson,
    "--output", $RuntimeToolCapabilityJson,
    "--markdown-output", $RuntimeToolCapabilityMd
)
# IA_CARMINE_RUNTIME_TOOL_BROKER_BOOTSTRAP_END

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

$TelemetryArgs = @(
    ".\Tools\ai\build_full_toolbox_run_telemetry_summary.py",
    "--repo-root", ".",
    "--stamp", $Stamp,
    "--decision-loop", $DecisionLoopJson,
    "--recommendations", $RecommendationsJson,
    "--patch-plan", $PatchPlanJson,
    "--repository-consistency", $RepositoryConsistencyJson,
    "--repository-consistency-smoke", $RepositoryConsistencySmokeJson,
    "--gpu-npu-sync", $GpuNpuSyncJson,
    "--orchestrator", $OrchOut,
    "--gpu-report", $GpuOut,
    "--budget-minutes", "$BudgetMinutes",
    "--max-rounds", "$MaxRounds",
    "--files-per-round", "$FilesPerRound",
    "--max-context-files", "$MaxContextFiles",
    "--max-chars-per-file", "$MaxCharsPerFile",
    "--max-new-tokens", "$MaxNewTokens",
    "--npu-auditor-every-rounds", "$NpuAuditorEveryRounds",
    "--repository-consistency-map-workers", "$RepositoryConsistencyMapWorkers",
    "--output", $TelemetrySummaryJson,
    "--markdown-output", $TelemetrySummaryMd
)
foreach ($Path in @(
    $MemoryBundleJson,
    $MemoryBundleMd,
    $MemoryLineCountCsv,
    $LineCountCsv,
    $BundleJson,
    $BundleMd,
    ".\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_ai_to_ai_bundle_$Stamp.json",
    ".\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_ai_to_ai_bundle_$Stamp.md"
)) {
    if (Test-Path $Path) {
        $TelemetryArgs += @("--evidence-to-commit", $Path)
    }
}
$BundleValidationForTelemetry = Read-JsonFile $BundleValidationJson
if ($BundleValidationForTelemetry -and $BundleValidationForTelemetry.passed -eq $true) {
    $TelemetryArgs += @("--bundle-validation-passed")
}
Invoke-RepoPython -Label "Full toolbox run telemetry summary" -ArgsList $TelemetryArgs

Invoke-RepoPython -Label "Runtime tool usage telemetry" -ArgsList @(
    ".\Tools\ai\build_runtime_tool_usage_telemetry.py",
    "--repo-root", ".",
    "--stamp", $Stamp,
    "--orchestrator", $OrchOut,
    "--gpu-report", $GpuOut,
    "--gpu-npu-sync", $GpuNpuSyncJson,
    "--decision-loop", $DecisionLoopJson,
    "--broker-report", $RuntimeToolBrokerJson,
    "--output", $RuntimeToolTelemetryJson,
    "--markdown-output", $RuntimeToolTelemetryMd
)

Invoke-RepoPython -Label "Runtime tool capability manifest" -ArgsList @(
    ".\Tools\ai\build_runtime_tool_capability_manifest.py",
    "--repo-root", ".",
    "--tool-usage", $RuntimeToolTelemetryJson,
    "--output", $RuntimeToolCapabilityJson,
    "--markdown-output", $RuntimeToolCapabilityMd
)

$SemanticChunkSources = @(
    $BundleJson,
    $BundleMd,
    $TelemetrySummaryJson,
    $TelemetrySummaryMd,
    $RuntimeToolTelemetryJson,
    $RuntimeToolTelemetryMd,
    $RuntimeToolCapabilityJson,
    $RuntimeToolCapabilityMd
) | Where-Object { Test-Path $_ }
$SemanticChunkArgs = @(
    ".\Tools\ai\build_semantic_evidence_chunks.py",
    "--repo-root", ".",
    "--basename", $EvidenceChunkBase,
    "--output-dir", $EvidenceDir,
    "--chunk-output-dir", $EvidenceChunkDir,
    "--chunk-max-chars", "12000",
    "--chunk-overlap-lines", "12",
    "--zip-output", $EvidenceChunkZip,
    "--no-ollama"
)
foreach ($Path in $SemanticChunkSources) {
    $SemanticChunkArgs += @("--source", $Path)
}
Invoke-RepoPython -Label "Semantic evidence chunking for cloud handoff" -ArgsList $SemanticChunkArgs

foreach ($Path in @(
    $MemoryWorkflow, $Evidence, $ProviderEvidenceContractJson, $RepositoryConsistencyJson, $RepositoryConsistencySmokeJson, $LineCountJson, $PythonSyntaxJson, $CodeInterpreterJson, $GpuContractSmokeJson,
    $DeterministicSmokeJson, $DecisionLoopSmokeJson, $NpuEnvJson, $OrchOut, $GpuOut, $GpuReplayJson,
    $GpuNpuSyncJson, $ProviderEvidenceContractJson, $RecommendationsJson, $BridgeJson, $DecisionLoopJson, $PatchPlanJson,
    $BundleValidationJson, $FinalPythonSyntaxJson, $FinalContractJson
)) {
    Add-ExistingPath -List $Reports -Path $Path
}
foreach ($Path in @(
    $MemoryBundleJson, $MemoryBundleMd, $MemoryLineCountCsv, $EvidenceMd, $ProviderEvidenceContractMd, $RepositoryConsistencyMd, $RepositoryConsistencySmokeMd, $LineCountAllMd, $LineCountCsv,
    $CodeInterpreterMd, $GpuContractSmokeMd, $DeterministicSmokeMd, $DecisionLoopSmokeMd,
    $NpuEnvMd, $OrchMd, $GpuMd, $GpuReplayMd, $GpuNpuSyncMd, $ProviderEvidenceContractMd, $RecommendationsMd,
    $DecisionLoopMd, $PatchPlanMd, $TelemetrySummaryJson, $TelemetrySummaryMd, $RuntimeToolTelemetryJson, $RuntimeToolTelemetryMd,
    $RuntimeToolCapabilityJson, $RuntimeToolCapabilityMd, $EvidenceChunkManifestJson, $EvidenceChunkManifestMd, $BundleJson, $BundleMd
)) {
    Add-ExistingPath -List $Artifacts -Path $Path
}

$DecisionSummary = Read-JsonFile $DecisionLoopJson
$BundleValidation = Read-JsonFile $BundleValidationJson
$ProviderAdvisoryFailures = [System.Collections.ArrayList]@()
$ProviderAdvisoryReports = @($OrchOut, $GpuOut)
foreach ($ReportPath in $Reports) {
    $Data = Read-JsonFile $ReportPath
    if ($Data -and ($null -ne $Data.passed) -and ($Data.passed -eq $false)) {
        $DecisionLaneReady = (
            $DecisionSummary -and
            ($DecisionSummary.passed -eq $true) -and
            ([int]$DecisionSummary.recommendation_count -ge $MinRecommendations) -and
            ([int]$DecisionSummary.patch_plan_count -ge $MinPatchPlans)
        )
        if (($ProviderAdvisoryReports -contains $ReportPath) -and $DecisionLaneReady -and (-not [bool]$RequireProviderArtifacts)) {
            [void]$ProviderAdvisoryFailures.Add($ReportPath)
            [void]$Warnings.Add("${ReportPath}: passed=false degraded to provider advisory warning because decision loop passed with sufficient recommendations/patch plans")
        } else {
            [void]$Errors.Add("${ReportPath}: passed=false")
        }
    }
}
$WorkflowPassed = ($Errors.Count -eq 0)
$EvidenceToCommit = @(
    $MemoryBundleJson,
    $MemoryBundleMd,
    $MemoryLineCountCsv,
    $LineCountCsv,
    $BundleJson,
    $BundleMd,
    ".\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_ai_to_ai_bundle_$Stamp.json",
    ".\docs\LOCAL_VALIDATION_EVIDENCE\shared_toolbox_ai_to_ai_bundle_$Stamp.md",
    $TelemetrySummaryJson,
    $TelemetrySummaryMd,
    $RuntimeToolTelemetryJson,
    $RuntimeToolTelemetryMd,
    $RuntimeToolCapabilityJson,
    $RuntimeToolCapabilityMd,
    $EvidenceChunkManifestJson,
    $EvidenceChunkManifestMd
) | Where-Object { Test-Path $_ }

$ChunkManifestForCommit = Read-JsonFile $EvidenceChunkManifestJson
if ($ChunkManifestForCommit -and $ChunkManifestForCommit.chunk_files) {
    foreach ($ChunkPath in $ChunkManifestForCommit.chunk_files) {
        if (Test-Path $ChunkPath) {
            $EvidenceToCommit += @($ChunkPath)
        }
    }
}

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
    provider_advisory_failure_count = $ProviderAdvisoryFailures.Count
    provider_advisory_failures = @($ProviderAdvisoryFailures)
    max_recommendations = $MaxRecommendations
    max_patch_plans = $MaxPatchPlans
    reports = @($Reports)
    artifacts = @($Artifacts)
    evidence_to_commit = @($EvidenceToCommit)
    guardrails = [ordered]@{
        provider_execution_requires_explicit_flag = $true
        run_gpu_npu_provider = [bool]$RunGpuNpuProvider
        require_provider_artifacts = [bool]$RequireProviderArtifacts
        strict_provider_failures_block_workflow = [bool]$RequireProviderArtifacts
        patch_application_performed = $false
        source_writes_performed = $false
        sqlite_write_performed = $false
        persistent_memory_write_performed = $false
        blender_runtime_execution_performed = $false
        raw_output_commit_allowed = $false
        provider_advisory_failures_are_non_blocking_when_decision_lane_passes = $true
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
    "- Max recommendations: ``$MaxRecommendations``",
    "- Max patch plans: ``$MaxPatchPlans``",
    "- Provider advisory failure count: ``$($WorkflowReport.provider_advisory_failure_count)``",
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
