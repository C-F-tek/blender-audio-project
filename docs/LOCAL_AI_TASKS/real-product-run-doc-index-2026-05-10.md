# Real product run documentation index — 2026-05-10

## Canonical purpose

Questo indice serve a non sovraccaricare ulteriormente `Tools/workflow/README.md`. La README resta router generale e conserva gli anchor usati dagli smoke; i dettagli della run unica e dell'igiene sono spostati nei documenti dedicati.

## Documenti attivi

| Documento | Ruolo | Quando usarlo |
|---|---|---|
| `docs/LOCAL_AI_TASKS/real-product-run-unica-runbook-2026-05-10.md` | runbook operativo | Prima di lanciare o rilanciare la run unica real product. |
| `docs/LOCAL_AI_TASKS/problems-and-hygiene-candidates-2026-05-10.md` | coda problemi/igiene | Per scegliere patch safe dopo una run reale. |
| `docs/LOCAL_AI_TASKS/documentation-code-alignment-audit-2026-05-10.md` | audit doc/codice | Per verificare se i documenti descrivono il codice effettivo. |
| `docs/LOCAL_AI_TASKS/md-line-budget-triage-2026-05-10.md` | policy MD lunghi / split triage | Prima di espandere README o creare runbook lunghi. |
| `Tools/workflow/README.md` | router e contratti storici/correnti | Per trovare entrypoint, policy, anchor e tool classification. |

## Owner code principali

| Concetto | Owner code |
|---|---|
| Entrata unica real product | `Tools/workflow/run_unified_real_product_pr.ps1` |
| Universo heap/exchange | `Tools/workflow/run_unified_local_ai_refactor.ps1` |
| Preflight obbligatorio | `Tools/validation/run_real_product_preflight_gate.py` |
| GPU0 workload osservabile | `Tools/ai/build_openvino_gpu0_workload_report.py` |
| NPU micro peer diagnostic/report lane | `Tools/ai/build_npu_micro_task_companion_report.py` |
| Empty generated product fail-fast | `Tools/ai/apply_generated_patch_specs_for_review_pr.py` |
| Runtime evidence proposal feed | `Tools/ai/build_repository_change_proposals.py` |
| Concrete ops into patch specs | `Tools/ai/build_patch_specs_from_proposals.py` |
| Runtime evidence proposal smoke | `Tools/validation/run_repository_change_proposals_runtime_evidence_smoke.py` |
| Empty product smoke | `Tools/validation/run_generated_patch_specs_empty_product_smoke.py` |
| Markdown line-budget policy | `Tools/validation/check_file_line_limits.py` |

## Dottrina sintetica corrente

- Il Task MD è input, non prodotto.
- Il prodotto deve emergere da heap/exchange e generated patch specs.
- GPU1/Ollama advisory deve leggere evidenze runtime current-stamp.
- GPU0 deve dimostrare attività osservabile, non solo presenza di device.
- NPU resta peer micro/diagnostic finché non esiste compute lane validata.
- Metadata-only patch specs non sono prodotto PR.
- `operation_count=0` con `--apply` è fallimento.
- Draft PR finale è valido solo se `prepare_review_pr.py` produce prodotto reale e il final product contract passa.
- Ogni nuovo MD operativo deve restare sotto la soglia policy o diventare indice + parti.

## Drift da evitare

- Non aggiungere altre sezioni lunghe a `Tools/workflow/README.md`.
- Non duplicare comandi completi in più file se cambiano spesso.
- Non documentare NPU come compute provider se il codice la classifica diagnostic/report-only.
- Non indicare `P-NEXT-NPU-OBSERVABILITY` come successo finale quando esiste evidenza runtime current-stamp e il prodotto è metadata-only.
- Non suggerire commit di `output/**`, `indexAI/code_chunks/**`, `docs/LOCAL_VALIDATION_EVIDENCE/**`, database o renders.
- Non creare nuovi runbook monolitici: usare il validator line-limit come gate di igiene.

## Prossimo ciclo consigliato

1. sincronizzare `master`;
2. eseguire gli smoke #295/#296;
3. rilanciare run unica real product;
4. se fallisce, classificare con `problems-and-hygiene-candidates-2026-05-10.md`;
5. se passa e crea PR, ispezionare touched files, line counts, validators e product contract;
6. prima di espandere docs, consultare `md-line-budget-triage-2026-05-10.md`;
7. solo dopo valutare refactor README/line-budget.

## Standalone heap incubation document

| Documento | Ruolo | Quando usarlo |
|---|---|---|
| `docs/LOCAL_AI_TASKS/standalone-heap-universe-incubation-2026-05-10.md` | standalone heap universe incubation | Quando si lavora sul nuovo runtime heap slegato dalla full run, prima della promozione nella run-unica. |

The standalone heap lane is not the current full product entrypoint. It is the robustness lane for testing strict input, preload, SQLite/memory/chunk context, GPU1/GPU0/NPU cooperation, in-heap refinement and composed output before promotion into `run_unified_real_product_pr.ps1`.

## Standalone heap tool surface document

| Documento | Ruolo | Quando usarlo |
|---|---|---|
| `docs/LOCAL_AI_TASKS/standalone-heap-universe-tool-surface-2026-05-10.md` | standalone heap tool/memory surface map | Quando si verifica che SQLite/FTS5, chunk memory, context namespace, tool catalog, broker, provider lanes and validators siano caricati come fatti heap prima della promozione nella run-unica. |
