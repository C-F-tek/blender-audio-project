# Run Unica CLI Esplicita

<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:START -->
## Current Runtime/Tool Contract (2026-05-24)

Canonical wording: `docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md`.

- GPU1/NVIDIA primary Ollama lane is the operational center and advances by heap pointer/recovery turns without waiting for GPU0/NPU sidecar completion.
- GPU0/NPU are `packet_review_only` sidecars: they start only after a reviewable GPU1 packet, do not close product, and remain deferred evidence until a later GPU1 turn consumes their pointer ids.
- Tool/lab/matrix/debug reporting must distinguish `lab_called`, `lab_report_written`, `lab_usable` and `lab_status`; attempted tool calls are evidence, not automatic usable lab output.
- `FINAL_PRODUCT` is single: text, code, or text+code. `PLAN_PRODUCT_FULL_PATCH.md` is its text/prose surface; `CODE_PRODUCT_FULL_PATCH.md` is its code/diff surface only when verified code exists.
- Missing optional values stay empty/null; required missing devices or provider prerequisites raise or block with a typed reason rather than emitting placeholder text.
- Complete runs require explicit config flags, including `--files-per-round`, `--gpu0-ollama-num-ctx`, `--npu-micro-start-mode`, `--npu-final-wait-seconds` and `--max-degraded-lanes`.
<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:END -->


Documento operativo root-level per lanciare `python -m ia_carmine.cli run` senza profili impliciti, senza config JSON nascosta e senza fallback tecnici. Ogni parametro operator-facing deve essere dichiarato nella CLI. Se manca un parametro richiesto, la run deve fermarsi prima dei provider.

## Regole

- Non usare `--profile` per propagare parametri runtime.
- Non usare `--operator-config`.
- Non affidarsi a variabili ambiente per modello, URL, budget, RAG, memoria o tooling.
- Prima eseguire sempre il dry-run: deve mostrare `effective_universe_config`, `field_sources` e `expanded_heap_command`.
- La run reale usa lo stesso array di argomenti del dry-run, senza `--dry-run`.

## Template CLI Esplicito

```powershell
$RepoRoot = (Resolve-Path .).Path
$RepoPy = Read-Host "Python IA_CARMINE_PYTHON completo"
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = $RepoRoot

$TaskFile = Read-Host "Task file completo"
$Stamp = "run-unica-$(Get-Date -Format yyyyMMdd-HHmmss)"
$IntermediateRoot = Join-Path $RepoRoot "output\validation\operator_product_launcher_lab"
$FinalRoot = Join-Path $RepoRoot "output\validation\$Stamp\final_product"

$Gpu1Model = Read-Host "GPU1 Ollama model"
$Gpu1BaseUrl = Read-Host "GPU1 Ollama base URL"
$Gpu0Model = Read-Host "GPU0 Ollama/Vulkan model"
$Gpu0BaseUrl = Read-Host "GPU0 Ollama/Vulkan base URL"
$Gpu0VulkanVisibleDevices = Read-Host "GPU0 Vulkan visible devices"
$NpuModelDir = Read-Host "NPU OpenVINO model dir"
$RagDb = Read-Host "RAG sqlite path"
$RagEmbeddingEndpoint = Read-Host "RAG embedding endpoint"
$RagEmbeddingModel = Read-Host "RAG embedding model"

$BudgetMinutes = Read-Host "budget-minutes"
$MaxIterations = Read-Host "max-iterations"
$MaxRounds = Read-Host "max-rounds"
$FilesPerRound = Read-Host "files-per-round"
$MaxProviderRevisions = Read-Host "max-provider-revisions"
$TimeoutSeconds = Read-Host "timeout-seconds"
$PreflightTimeoutSeconds = Read-Host "preflight-timeout-seconds"
$MaxDegradedLanes = Read-Host "max-degraded-lanes"

$OllamaNumCtx = Read-Host "GPU1 ollama-num-ctx"
$Gpu0OllamaNumCtx = Read-Host "GPU0 ollama-num-ctx"
$OllamaGpuLayers = Read-Host "ollama-gpu-layers"
$OllamaContextCandidates = Read-Host "ollama-context-candidates"
$MaxNewTokens = Read-Host "GPU1 max-new-tokens"
$Gpu0MaxNewTokens = Read-Host "GPU0 max-new-tokens"
$KeepAlive = Read-Host "keep-alive"

$RunLabel = Read-Host "run-label"
$RevisionContext = Read-Host "revision-context"
$RevisionContextMaxTasks = Read-Host "revision-context-max-tasks"
$MinRuntimeRounds = Read-Host "min-runtime-rounds"
$MinProposalIterations = Read-Host "min-proposal-iterations"
$Gpu0Iterations = Read-Host "gpu0-iterations"
$Gpu0MinSeconds = Read-Host "gpu0-min-seconds"

$NpuMicroTimeoutSeconds = Read-Host "npu-micro-timeout-seconds"
$NpuMicroStartMode = Read-Host "npu-micro-start-mode"
$NpuFinalWaitSeconds = Read-Host "npu-final-wait-seconds"
$NpuMaxContextChars = Read-Host "npu-max-context-chars"
$NpuMaxPromptChars = Read-Host "npu-max-prompt-chars"
$NpuMaxNewTokens = Read-Host "npu-max-new-tokens"
$NpuDeviceWorkloadSeconds = Read-Host "npu-device-workload-seconds"
$NpuDeviceWorkloadIterations = Read-Host "npu-device-workload-iterations"

$StartupMaxMemoryChars = Read-Host "startup-max-memory-chars"
$StartupMaxContextFiles = Read-Host "startup-max-context-files"
$StartupScanContextFiles = Read-Host "startup-scan-context-files"
$StartupMaxCharsPerFile = Read-Host "startup-max-chars-per-file"
$StartupProviderInputWorkers = Read-Host "startup-provider-input-workers"
$StartupRequiredContextProfile = Read-Host "startup-required-context-profile"
$StartupOperationalMemoryQuery = Read-Host "startup-operational-memory-query"
$StartupOperationalMemoryLimit = Read-Host "startup-operational-memory-limit"

$RagIndexPolicy = Read-Host "rag-index-policy"
$RagIngestBatchSize = Read-Host "rag-ingest-batch-size"
$RagEmbedSmokeBatchSize = Read-Host "rag-embed-smoke-batch-size"
$RagChunkMinChars = Read-Host "rag-chunk-min-chars"
$RagChunkMaxChars = Read-Host "rag-chunk-max-chars"
$RagChunkOverlapChars = Read-Host "rag-chunk-overlap-chars"
$RagMaxFileSize = Read-Host "rag-max-file-size"
$RagTopK = Read-Host "rag-top-k"
$RagCharBudget = Read-Host "rag-char-budget"

$ContextDocumentCount = Read-Host "context-document-count"
$ContextDocumentPreviewChars = Read-Host "context-document-preview-chars"
$SemanticCodeChunkLimit = Read-Host "semantic-code-chunk-limit"
$SemanticCodeChunkPreviewChars = Read-Host "semantic-code-chunk-preview-chars"
$SemanticEvidenceChunkLimit = Read-Host "semantic-evidence-chunk-limit"
$MemorySearchLimit = Read-Host "memory-search-limit"
$ToolCatalogLimit = Read-Host "tool-catalog-limit"

$ToolInventoryRoots = Read-Host "tool-inventory-roots"
$SemanticPathBoosts = Read-Host "semantic-path-boosts"
$AiContextPackProfile = Read-Host "ai-context-pack-profile"
$CodeInterpreterInputs = Read-Host "code-interpreter-inputs"
$DuplicationAuditRoots = Read-Host "duplication-audit-roots"
$ProviderPromptToolCatalogCap = Read-Host "provider-prompt-tool-catalog-cap"

$AllowProviderGeneration = Read-Host "allow-provider-generation true/false"
$RequireOllamaGpuResidency = Read-Host "require-ollama-gpu-residency true/false"
$AllowNpuDeviceWorkload = Read-Host "allow-npu-device-workload true/false"

$RunArgs = @(
  "--repo-root", $RepoRoot,
  "--python-exe", $RepoPy,
  "--request-file", $TaskFile,
  "--run-label", $RunLabel,
  "--intermediate-root", $IntermediateRoot,
  "--final-root", $FinalRoot,
  "--stamp", $Stamp,

  "--revision-context", $RevisionContext,
  "--revision-context-max-tasks", $RevisionContextMaxTasks,

  "--budget-minutes", $BudgetMinutes,
  "--max-iterations", $MaxIterations,
  "--min-runtime-rounds", $MinRuntimeRounds,
  "--min-proposal-iterations", $MinProposalIterations,
  "--max-rounds", $MaxRounds,
  "--files-per-round", $FilesPerRound,
  "--max-provider-revisions", $MaxProviderRevisions,
  "--timeout-seconds", $TimeoutSeconds,
  "--preflight-timeout-seconds", $PreflightTimeoutSeconds,
  "--max-degraded-lanes", $MaxDegradedLanes,

  "--provider-model", $Gpu1Model,
  "--gpu1-base-url", $Gpu1BaseUrl,
  "--gpu0-model", $Gpu0Model,
  "--gpu0-base-url", $Gpu0BaseUrl,
  "--gpu0-vulkan-visible-devices", $Gpu0VulkanVisibleDevices,
  "--ollama-num-ctx", $OllamaNumCtx,
  "--gpu0-ollama-num-ctx", $Gpu0OllamaNumCtx,
  "--ollama-gpu-layers", $OllamaGpuLayers,
  "--ollama-context-candidates", $OllamaContextCandidates,
  "--max-new-tokens", $MaxNewTokens,
  "--gpu0-max-new-tokens", $Gpu0MaxNewTokens,
  "--keep-alive", $KeepAlive,

  "--gpu0-iterations", $Gpu0Iterations,
  "--gpu0-min-seconds", $Gpu0MinSeconds,

  "--npu-model-dir", $NpuModelDir,
  "--npu-micro-timeout-seconds", $NpuMicroTimeoutSeconds,
  "--npu-micro-start-mode", $NpuMicroStartMode,
  "--npu-final-wait-seconds", $NpuFinalWaitSeconds,
  "--npu-max-context-chars", $NpuMaxContextChars,
  "--npu-max-prompt-chars", $NpuMaxPromptChars,
  "--npu-max-new-tokens", $NpuMaxNewTokens,
  "--npu-device-workload-seconds", $NpuDeviceWorkloadSeconds,
  "--npu-device-workload-iterations", $NpuDeviceWorkloadIterations,

  "--startup-max-memory-chars", $StartupMaxMemoryChars,
  "--startup-max-context-files", $StartupMaxContextFiles,
  "--startup-scan-context-files", $StartupScanContextFiles,
  "--startup-max-chars-per-file", $StartupMaxCharsPerFile,
  "--startup-provider-input-workers", $StartupProviderInputWorkers,
  "--startup-required-context-profile", $StartupRequiredContextProfile,
  "--startup-operational-memory-query", $StartupOperationalMemoryQuery,
  "--startup-operational-memory-limit", $StartupOperationalMemoryLimit,

  "--rag-db", $RagDb,
  "--rag-index-policy", $RagIndexPolicy,
  "--rag-embedding-endpoint", $RagEmbeddingEndpoint,
  "--rag-embedding-model", $RagEmbeddingModel,
  "--rag-ingest-batch-size", $RagIngestBatchSize,
  "--rag-embed-smoke-batch-size", $RagEmbedSmokeBatchSize,
  "--rag-chunk-min-chars", $RagChunkMinChars,
  "--rag-chunk-max-chars", $RagChunkMaxChars,
  "--rag-chunk-overlap-chars", $RagChunkOverlapChars,
  "--rag-max-file-size", $RagMaxFileSize,
  "--rag-top-k", $RagTopK,
  "--rag-char-budget", $RagCharBudget,

  "--context-document-count", $ContextDocumentCount,
  "--context-document-preview-chars", $ContextDocumentPreviewChars,
  "--semantic-code-chunk-limit", $SemanticCodeChunkLimit,
  "--semantic-code-chunk-preview-chars", $SemanticCodeChunkPreviewChars,
  "--semantic-evidence-chunk-limit", $SemanticEvidenceChunkLimit,
  "--memory-search-limit", $MemorySearchLimit,
  "--tool-catalog-limit", $ToolCatalogLimit,

  "--tool-inventory-roots", $ToolInventoryRoots,
  "--semantic-path-boosts", $SemanticPathBoosts,
  "--ai-context-pack-profile", $AiContextPackProfile,
  "--code-interpreter-inputs", $CodeInterpreterInputs,
  "--duplication-audit-roots", $DuplicationAuditRoots,
  "--provider-prompt-tool-catalog-cap", $ProviderPromptToolCatalogCap
)

if ($AllowProviderGeneration -eq "true") { $RunArgs += "--allow-provider-generation" } else { $RunArgs += "--no-allow-provider-generation" }
if ($RequireOllamaGpuResidency -eq "true") { $RunArgs += "--require-ollama-gpu-residency" } else { $RunArgs += "--no-require-ollama-gpu-residency" }
if ($AllowNpuDeviceWorkload -eq "true") { $RunArgs += "--allow-npu-device-workload" } else { $RunArgs += "--no-allow-npu-device-workload" }

# Preview: non esegue provider.
& $RepoPy -m ia_carmine.cli run @RunArgs --dry-run

# Run reale.
& $RepoPy -m ia_carmine.cli run @RunArgs
```

## Campi Da Aggiornare Di Solito

- `$TaskFile`: richiesta operatore corrente.
- `$Stamp`: lasciare dinamico salvo riproduzione di una run specifica.
- `$NpuModelDir`: directory modello OpenVINO NPU locale.
- `--provider-model`: modello GPU1/Ollama.
- `--gpu0-model`: modello GPU0/Ollama Vulkan.
- Budget, round, context e token: aggiornare solo come flag CLI espliciti.

## Verifica Attesa Del Dry-Run

Il dry-run deve mostrare:

- `execution_performed=false`
- `provider_execution_performed=false`
- `effective_universe_config`
- `field_sources` con i parametri operativi segnati come `cli_arg`
- `expanded_heap_command` completo

Se il comando manca parametri richiesti, l'errore corretto e':

```text
missing explicit Universo IA run parameter(s); provide CLI flags
```
