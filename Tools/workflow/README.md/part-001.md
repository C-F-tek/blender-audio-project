<!-- IA-CARMINE-MD-SPLIT: part -->
# README â€” parte 001 di 003

Sorgente indice: [`README.md`](README.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

# Workflow Tools

`Tools/workflow/` contains launcher and workflow helper scripts for IA-Carmine.

This directory currently has two canonical entrypoints with different ownership:

```text
python -m Tools.ai run
python -m Tools.workflow run_unified_local_ai_refactor
```

Use `run_unified_real_product_pr.ps1` for the operator-facing real product path: Task MD or `-ProcessGateTask` in, mandatory preflight, heap/exchange universe, generated patch specs, product validation and draft review PR out.

Use `run_unified_local_ai_refactor.ps1` as the internal unified launcher and for focused diagnostics. For single-phase diagnostics, pass `-NoStrictRealRunActivation`.

Current command ownership lives in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/real-product-run-doc-index-2026-05-10.md
docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md
```

Current code-driven navigation, validation and hygiene ownership lives in:

```text
docs/LOCAL_AI_TASKS/documentation-code-alignment-audit-2026-05-10.md
docs/LOCAL_AI_TASKS/problems-and-hygiene-candidates-2026-05-10.md
docs/LOCAL_AI_TASKS/md-line-budget-triage-2026-05-10.md
docs/LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

## Current doctrine

```text
Real product run = one wrapper entry, one dynamic heap/exchange center, one validated review-PR product exit
run_unified_real_product_pr.ps1 = operator-facing product entrypoint
run_unified_local_ai_refactor.ps1 = unified launcher / dynamic heap-exchange executor
quick/balanced/deep/custom = intensity, not scope
supporting wrappers are implementation lanes, not first entrypoints
provider/probe/workload-quality lanes are opt-out in real unified product runs
GPU1/GPU0/NPU peer exchange must enter telemetry, bundle and acceptance evidence
GPU1/Ollama advisory must consume current-stamp runtime evidence when available
GPU0 OpenVINO lane must be observable workload/support evidence, not only device presence
NPU is peer micro/diagnostic/report lane until a compute-provider lane is validated
runtime tool telemetry must use normalized statuses and broker-measured elapsed seconds when tools execute
final NPU provider work must not run on the performance-critical close path unless NpuMicroStartMode=final-provider
provider-capable workflow runners prefer IA_CARMINE_PYTHON, then .venv, before system python
CSV/index/discovery/file-line-limit surfaces are evidence lanes when relevant
heap/exchange entry and exit are deterministic boundaries around the dynamic center
patchkit is the preferred deterministic source-write boundary for future long or delicate patch bundles
generated patch specs must produce concrete deterministic operations for product PR application
metadata-only generated patch specs with --apply are a hard failure, not a reviewable product
preferred active runbook/docs size <=400 lines
active Markdown hard threshold <=500 lines
maintained source/script target <=400 lines
limitations are backlog to overcome, not reasons to skip available tools
```

## Operator routing

| Need | Start here |
|---|---|
| Real full product run | `run_unified_real_product_pr.ps1 -ProcessGateTask` or `-TaskFile <md>`; it performs mandatory preflight and delegates to `run_unified_local_ai_refactor.ps1` with the complete heap/exchange product lane. |
| Single-phase diagnostic | `run_unified_local_ai_refactor.ps1` with `-NoStrictRealRunActivation`. |
| Heap/exchange lifecycle product path | Real product wrapper or unified launcher with provider/evidence/patch/review lanes selected. |
| Patchkit source-write boundary | `Tools/ai/patchkit/apply_patch_bundle.py` after a reviewed `patch_specs/<bundle>/bundle.json`. |
| Markdown-to-review-PR product path | Real product wrapper plus generated patch specs/review PR flags; current owner chain below. |
| Full-toolbox internals | `python -m Tools.workflow run_agent_review_full_toolbox_decision_loop` and packaged engine. |
| Script family census | `docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md`. |
| Source-code behavior map | `docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md`. |

Do not start a normal workflow from an internal helper unless the launcher/runbook explicitly delegates to that helper or the task is a focused tool validation.

## Real product PR profile

~~~powershell
python -m Tools.ai run `
  -RepoRoot . `
  -ProcessGateTask `
  -RunIntensity custom `
  -BudgetMinutes 10 `
  -MaxRounds 600 `
  -FilesPerRound 6 `
  -MaxContextFiles 3020 `
  -MaxCharsPerFile 7000 `
  -MaxNewTokens 2200 `
  -KeepAlive 15m `
  -ProviderMaxContextChars 14000 `
  -ContextPackMaxTotalChars 72000 `
  -ContextPackMaxFileChars 5000 `
  -AgentStateMaxMemoryChars 28000 `
  -MaxRecommendations 700 `
  -MaxPatchPlans 700 `
  -OfficialAdapterTimeoutSeconds 600 `
  -PreflightTimeoutSeconds 180 `
  -OpenObserverConsoles `
  -OpenExtendedObserverConsoles `
  -ObserverRefreshSeconds 2 `
  -UseGeneratedPatchSpecs `
  -ReviewPrMaxAppliedPatches 5 `
  -Push `
  -CreatePr `
  -DraftPr
~~~

This profile is the operator-facing path from task Markdown or generated process-gate task to reviewable PR product. It enables mandatory preflight, task ingress, heap/exchange, GPU1/GPU0/NPU peer runtime evidence, shared memory, closure audit, patch suggestion/apply report, runtime evidence correlation, prepare_review_pr and optional remote draft PR creation.

The profile owns the architectural lane flags internally and keeps runtime sizing, model, Python, observer and review-PR controls external. Operators should pass task-specific budgets and context limits from the CLI instead of editing the wrapper. Its default NPU micro-start mode is `peer`, so the heap/exchange product lane starts with GPU1/GPU0/NPU as coordinated peers instead of deferring NPU participation.

## Runtime boundary

Current full product path is:

```text
IN
  task Markdown or generated process-gate task
  RepoPy/PYTHONPATH gate
  mandatory real-product preflight
  inventories/context/agent-state
  workload/capability evidence

LOOP / HEAP / EXCHANGE
  dynamic provider/context/broker/runtime lane cooperation
  GPU1/Ollama advisory
  GPU0 OpenVINO observable support workload
  NPU micro peer diagnostic/report lane
  runtime state
  public exchange events

OUT
  heap exchange exit product
  generated patch specs
  concrete deterministic operation candidates
  lifecycle validation
  runtime evidence correlation
  patchkit or deterministic patch bridge
  prepare_review_pr.py
  review PR product
```

The center is dynamic. Entry and exit are controlled.

## Markdown-to-review-PR product chain

Current owner chain:

```text
run_unified_real_product_pr.ps1
  -> docs/LOCAL_AI_TASKS/<task>.md or output/local_ai_task_inputs/<generated-task>.md
  -> mandatory preflight
  -> run_unified_local_ai_refactor.ps1
  -> inventories/context/agent-state/workload-quality
  -> Tools/ai/build_heap_exchange_runtime_entry.py
  -> official adapter/provider/patch-spec lanes
  -> Tools/ai/build_heap_exchange_runtime_exit.py
  -> Tools/validation/check_heap_exchange_runtime_lifecycle.py
  -> Tools/ai/build_repository_change_proposals.py
  -> Tools/ai/build_patch_specs_from_proposals.py
  -> Tools/ai/apply_generated_patch_specs_for_review_pr.py
  -> Tools/ai/prepare_review_pr.py
  -> Tools/validation/check_review_pr_final_product_contract.py
```

Legacy deterministic suggestion bridge remains available:

```text
Tools/ai/build_task_patch_suggestion_report.py
Tools/ai/apply_patch_suggestion_bundle.py
Tools/validation/check_patch_suggestion_product_separation.py
```

Focused chain smoke:

```text
Tools/validation/run_heap_exchange_runtime_lifecycle_smoke.py
Tools/validation/run_patchkit_smoke.py
Tools/validation/run_repository_change_proposals_runtime_evidence_smoke.py
Tools/validation/run_generated_patch_specs_empty_product_smoke.py
```

Current limitations and hard gates:

```text
ReviewPrIncludePath remains supported for explicit/manual allowlists.
prepare_review_pr.py can auto-discover include paths from apply reports with `--auto-include-from-apply-report` plus `--apply-report`.
prepare_review_pr.py supports draft PR creation through `--draft-pr` when `--create-pr` and `--push` are selected.
metadata-only patch drafts are not enough for a successful review PR product.
operation_count=0 under generated patch-spec --apply is a hard failure.
P-NEXT-NPU-OBSERVABILITY is fallback/backlog, not final success when runtime peer evidence exists.
P-RUNTIME-PEER-EVIDENCE-FEED is the expected proposal when runtime evidence exists but prior generated product was metadata-only.
```
