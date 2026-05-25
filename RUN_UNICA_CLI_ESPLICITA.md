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

## Comando Minimo Attuale

```powershell
cd C:\Users\carmi\ProjectsDir\blender-audio-project

$RepoRoot = (Resolve-Path .).Path
$RepoPy = "C:\Users\carmi\blender\blender-audio-project\.venv\Scripts\python.exe"
$env:IA_CARMINE_PYTHON = $RepoPy
$env:PYTHONPATH = $RepoRoot

$TaskFile = Join-Path $RepoRoot "docs\LOCAL_AI_TASKS\run-unica-real-product-contract-2026-05-21\URGENT.md"
$Stamp = "run-unica-$(Get-Date -Format yyyyMMdd-HHmmss)"
$IntermediateRoot = Join-Path $RepoRoot "output\validation\operator_product_launcher_lab"
$FinalRoot = Join-Path $RepoRoot "output\validation\$Stamp\final_product"
$NpuModelDir = "C:\Users\carmi\blender\npu-models\Phi-3.5-mini-instruct-int4-cw-ov"

$RunArgs = @(
  "--repo-root", $RepoRoot,
  "--python-exe", $RepoPy,
  "--request-file", $TaskFile,
  "--run-label", "spark_direct",
  "--intermediate-root", $IntermediateRoot,
  "--final-root", $FinalRoot,
  "--stamp", $Stamp,

  "--revision-context", "auto_latest",
  "--revision-context-max-tasks", "6",

  "--budget-minutes", "5",
  "--max-iterations", "5",
  "--min-runtime-rounds", "1",
  "--min-proposal-iterations", "0",
  "--max-rounds", "8",
  "--files-per-round", "4",
  "--max-provider-revisions", "5",
  "--timeout-seconds", "600",
  "--preflight-timeout-seconds", "90",
  "--max-degraded-lanes", "0",

  "--provider-model", "qwen2.5-coder:14b",
  "--gpu1-base-url", "http://127.0.0.1:11434",
  "--gpu0-model", "qwen3:1.7b",
  "--gpu0-base-url", "http://127.0.0.1:11435",
  "--gpu0-vulkan-visible-devices", "1",
  "--ollama-num-ctx", "16384",
  "--gpu0-ollama-num-ctx", "2048",
  "--ollama-gpu-layers", "all",
  "--ollama-context-candidates", "8192,4096",
  "--max-new-tokens", "900",
  "--gpu0-max-new-tokens", "96",
  "--keep-alive", "120s",

  "--gpu0-iterations", "16",
  "--gpu0-min-seconds", "0.1",

  "--npu-model-dir", $NpuModelDir,
  "--npu-micro-timeout-seconds", "60",
  "--npu-micro-start-mode", "deferred",
  "--npu-final-wait-seconds", "60",
  "--npu-max-context-chars", "8000",
  "--npu-max-prompt-chars", "1200",
  "--npu-max-new-tokens", "384",
  "--npu-device-workload-seconds", "3.0",
  "--npu-device-workload-iterations", "2500",

  "--startup-max-memory-chars", "32000",
  "--startup-max-context-files", "48",
  "--startup-scan-context-files", "48",
  "--startup-max-chars-per-file", "8000",
  "--startup-provider-input-workers", "6",
  "--startup-required-context-profile", "project_self_improvement",
  "--startup-operational-memory-query", "operator_product_launcher run-unica heap context closure provider lanes",
  "--startup-operational-memory-limit", "8",

  "--rag-db", "output/ai_runtime_memory/rag/rag.sqlite",
  "--rag-index-policy", "auto",
  "--rag-embedding-endpoint", "http://127.0.0.1:11434",
  "--rag-embedding-model", "bge-m3",
  "--rag-ingest-batch-size", "8",
  "--rag-embed-smoke-batch-size", "8",
  "--rag-chunk-min-chars", "1500",
  "--rag-chunk-max-chars", "4000",
  "--rag-chunk-overlap-chars", "300",
  "--rag-max-file-size", "250000",
  "--rag-top-k", "20",
  "--rag-char-budget", "32000",

  "--context-document-count", "24",
  "--context-document-preview-chars", "1200",
  "--semantic-code-chunk-limit", "32",
  "--semantic-code-chunk-preview-chars", "1400",
  "--semantic-evidence-chunk-limit", "24",
  "--memory-search-limit", "12",
  "--tool-catalog-limit", "80",

  "--tool-inventory-roots", "Tools,ia_carmine",
  "--semantic-path-boosts", "ia_carmine/runtime/heap_gate,ia_carmine/runtime/run,ia_carmine/context,Tools/validation",
  "--ai-context-pack-profile", "core_ai_backend",
  "--code-interpreter-inputs", "ia_carmine,Tools,docs",
  "--duplication-audit-roots", "ia_carmine,Tools",
  "--provider-prompt-tool-catalog-cap", "80",

  "--allow-provider-generation",
  "--require-ollama-gpu-residency",
  "--allow-npu-device-workload"
)

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
