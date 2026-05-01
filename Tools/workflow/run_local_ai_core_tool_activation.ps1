<#
.SYNOPSIS
  Activate the app-agnostic local AI core/tool pipeline and produce concrete review artifacts.

.DESCRIPTION
  This runner is the priority activation lane for IA-Carmine repository work.
  It uses the existing FullContextGoldenPath preset to build real local artifacts
  for review and testing while preserving explicit-provider and no-apply guardrails.

  Default behavior is provider-free and patch-free:
    - builds selected chunks, selected-chunks evidence, context pack, agent state,
      enrichment plan, advisory packet/proposals and compact GitHub evidence;
    - builds and validates an NPU knowledge-broker packet as context-only metadata;
    - validates adapter manifest and selected artifacts;
    - does not apply patches, run Blender, run FFmpeg or merge anything.

  Macro patch mode is manual-review-only. It may generate draft patch specs under
  output/patch_specs/ when -GenerateMacroPatchDrafts is passed, but it never
  applies them and never queues them for automatic execution.

  Provider execution remains explicit and opt-in through -UseExplicitProviders.
#>
[CmdletBinding()]
param(
    [string]$RepoRoot = ".",
    [string]$TaskFile = "docs/LOCAL_AI_TASKS/full-context-ai-npu-golden-path.md",
    [string]$RunName = "local_ai_core_tool_activation",
    [string]$Objective = "Activate the app-agnostic IA-Carmine local AI core/tool pipeline, generate concrete repository artifacts, validate NPU knowledge-broker context and prepare manual-review macro patch drafts when explicitly requested.",
    [switch]$UseExplicitProviders,
    [switch]$GenerateMacroPatchDrafts,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-ExistingPath {
    param([string]$PathValue)
    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return (Resolve-Path $PathValue).Path
    }
    return (Resolve-Path (Join-Path (Get-Location) $PathValue)).Path
}

function Invoke-Checked {
    param(
        [string]$Label,
        [scriptblock]$Block
    )
    Write-Host ""
    Write-Host "=== $Label ===" -ForegroundColor Cyan
    & $Block
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE"
    }
}

function Join-Args {
    param([string[]]$Values)
    return ($Values -join " ")
}

$RepoRootPath = Resolve-ExistingPath $RepoRoot
Set-Location $RepoRootPath

$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$SafeRunName = [regex]::Replace($RunName.ToLowerInvariant(), "[^a-z0-9._-]+", "_").Trim("._-")
if ([string]::IsNullOrWhiteSpace($SafeRunName)) { $SafeRunName = "local_ai_core_tool_activation" }
$RunDir = "output/local_ai_runs/${Stamp}_${SafeRunName}"
$PipelineDir = "$RunDir/pipeline"
$Basename = "local_ai_core_tool_activation"
$ProposalBasename = "local_ai_core_tool_activation_proposals"
$EvidenceBasename = "local_ai_core_tool_activation_evidence"
$KnowledgePacket = "output/ai_pipeline/local_ai_core_tool_activation_npu_knowledge_broker_packet.json"
$KnowledgePacketMd = "output/ai_pipeline/local_ai_core_tool_activation_npu_knowledge_broker_packet.md"
$KnowledgeValidation = "output/validation/local_ai_core_tool_activation_npu_knowledge_broker_packet_contract.json"
$AdapterManifest = "$PipelineDir/${Basename}_adapter_manifest.json"
$AdapterManifestValidation = "output/validation/local_ai_core_tool_activation_adapter_manifest_contract.json"
$GithubEvidenceValidation = "output/validation/local_ai_core_tool_activation_github_evidence_bundle.json"
$SelectedChunks = "output/ai_context_packs/full_context_golden_selected_chunks.json"
$ContextPack = "output/ai_context_packs/full_context_golden_core_ai_backend.json"

Write-Host "=== IA-Carmine Local AI Core/Tool Activation ===" -ForegroundColor Green
Write-Host "Repo: $RepoRootPath"
Write-Host "Task file: $TaskFile"
Write-Host "Run dir: $RunDir"
Write-Host "Use explicit providers: $UseExplicitProviders"
Write-Host "Generate macro patch drafts: $GenerateMacroPatchDrafts"
Write-Host "Dry run: $DryRun"

$PipelineArgs = @(
    "-NoProfile", "-ExecutionPolicy", "Bypass",
    "-File", ".\Tools\workflow\run_local_ai_task_via_pipeline.ps1",
    "-PromptFile", ".\$TaskFile",
    "-TaskFile", ".\$TaskFile",
    "-RunDir", ".\$RunDir",
    "-FullContextGoldenPath",
    "-Basename", $Basename,
    "-ProposalBasename", $ProposalBasename,
    "-EvidenceBasename", $EvidenceBasename,
    "-AgentStateObjective", $Objective,
    "-BuildEvidence"
)

if ($UseExplicitProviders) {
    $PipelineArgs += @(
        "-RunMultistepProviderWorkflow",
        "-RunOllamaProbe",
        "-RunNpuProbe",
        "-RunNpuDecodeSmoke",
        "-UsePrimaryAdvisoryProvider"
    )
}

if ($GenerateMacroPatchDrafts) {
    $PipelineArgs += "-GeneratePatchSpecs"
}

if ($DryRun) {
    $PipelineArgs += "-DryRun"
}

Invoke-Checked -Label "Run full-context local AI core/tool activation pipeline" -Block {
    powershell.exe @PipelineArgs
}

if (-not $DryRun) {
    Invoke-Checked -Label "Validate local AI adapter manifest" -Block {
        python .\Tools\validation\check_local_ai_adapter_manifest.py `
            --repo-root . `
            --manifest $AdapterManifest `
            --output $AdapterManifestValidation
    }

    Invoke-Checked -Label "Build NPU knowledge-broker context packet" -Block {
        python .\Tools\npu\build_npu_knowledge_broker_packet.py `
            --repo-root . `
            --objective $Objective `
            --selected-chunks $SelectedChunks `
            --context-pack $ContextPack `
            --adapter-manifest $AdapterManifest `
            --output $KnowledgePacket `
            --markdown-output $KnowledgePacketMd `
            --max-candidates 24
    }

    Invoke-Checked -Label "Validate NPU knowledge-broker context packet" -Block {
        python .\Tools\validation\check_npu_knowledge_broker_packet.py `
            --repo-root . `
            --packet $KnowledgePacket `
            --output $KnowledgeValidation `
            --min-candidates 3 `
            --max-candidates 24
    }

    Invoke-Checked -Label "Validate generated GitHub evidence bundle" -Block {
        python .\Tools\validation\check_github_evidence_bundle.py `
            --repo-root . `
            --bundle ".\docs\LOCAL_VALIDATION_EVIDENCE\${EvidenceBasename}.json" `
            --output $GithubEvidenceValidation
    }

    if ($GenerateMacroPatchDrafts) {
        $PatchManifest = "output/patch_specs/${Basename}_patch_specs_manifest.json"
        if (Test-Path -LiteralPath $PatchManifest -PathType Leaf) {
            Invoke-Checked -Label "Validate macro patch draft specs" -Block {
                python .\Tools\validation\check_patch_spec_drafts.py `
                    --repo-root . `
                    --manifest $PatchManifest `
                    --output "output/validation/${Basename}_macro_patch_drafts.json"
            }
        }
        else {
            Write-Warning "Macro patch drafts were requested but no manifest was found: $PatchManifest"
        }
    }
}

$Summary = [ordered]@{
    schema_version = 1
    kind = "local_ai_core_tool_activation_summary"
    generated_at = (Get-Date -Format o)
    repo_root = $RepoRootPath
    run_dir = $RunDir.Replace("\", "/")
    pipeline_dir = $PipelineDir.Replace("\", "/")
    task_file = $TaskFile.Replace("\", "/")
    use_explicit_providers = [bool]$UseExplicitProviders
    generate_macro_patch_drafts = [bool]$GenerateMacroPatchDrafts
    dry_run = [bool]$DryRun
    provider_execution_policy = "explicit_only"
    apply_policy = "manual_review_only_no_auto_apply"
    app_agnostic = $true
    blender_runtime_touched = $false
    patch_application_performed = $false
    outputs = [ordered]@{
        adapter_manifest = $AdapterManifest.Replace("\", "/")
        adapter_manifest_validation = $AdapterManifestValidation.Replace("\", "/")
        proposals_json = "$PipelineDir/$ProposalBasename.json"
        proposals_markdown = "$PipelineDir/$ProposalBasename.md"
        github_evidence_json = "docs/LOCAL_VALIDATION_EVIDENCE/${EvidenceBasename}.json"
        github_evidence_markdown = "docs/LOCAL_VALIDATION_EVIDENCE/${EvidenceBasename}.md"
        selected_chunks = $SelectedChunks
        context_pack = $ContextPack
        npu_knowledge_broker_packet = $KnowledgePacket
        npu_knowledge_broker_markdown = $KnowledgePacketMd
        npu_knowledge_broker_validation = $KnowledgeValidation
        macro_patch_manifest = "output/patch_specs/${Basename}_patch_specs_manifest.json"
    }
}

$SummaryPath = "output/ai_pipeline/local_ai_core_tool_activation_summary.json"
$SummaryMd = "output/ai_pipeline/local_ai_core_tool_activation_summary.md"
New-Item -ItemType Directory -Force -Path "output/ai_pipeline" | Out-Null
($Summary | ConvertTo-Json -Depth 8) | Set-Content -LiteralPath $SummaryPath -Encoding UTF8
@(
    "# Local AI Core/Tool Activation Summary",
    "",
    "- Run dir: $($Summary.run_dir)",
    "- Explicit providers: $UseExplicitProviders",
    "- Macro patch drafts: $GenerateMacroPatchDrafts",
    "- Apply policy: $($Summary.apply_policy)",
    "- App agnostic: $($Summary.app_agnostic)",
    "",
    "## Outputs",
    "",
    "- Adapter manifest: $AdapterManifest",
    "- GitHub evidence: docs/LOCAL_VALIDATION_EVIDENCE/${EvidenceBasename}.json",
    "- NPU knowledge broker packet: $KnowledgePacket",
    "- Macro patch manifest: output/patch_specs/${Basename}_patch_specs_manifest.json"
) | Set-Content -LiteralPath $SummaryMd -Encoding UTF8

Write-Host ""
Write-Host "[OK] Core/tool activation complete" -ForegroundColor Green
Write-Host "[OK] Summary: $SummaryPath"
Write-Host "[OK] Run dir: $RunDir"
Write-Host "[OK] Provider execution explicit-only: True"
Write-Host "[OK] Patch application performed: False"
