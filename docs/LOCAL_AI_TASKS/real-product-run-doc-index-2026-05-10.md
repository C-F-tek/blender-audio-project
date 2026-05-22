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
| Entrata unica real product | `python -m ia_carmine.cli run` |
| Universo heap/exchange | `python -m Tools.workflow run_unified_local_ai_refactor` |
| Preflight obbligatorio | `Tools/validation/real_product/preflight_gate/cli.py` |
| GPU0 workload osservabile | `ia_carmine/providers/provider_mesh/openvino_gpu0_workload_report.py` |
| NPU micro peer diagnostic/report lane | `ia_carmine/providers/provider_mesh/npu_micro_task_companion_report.py` |
| Empty generated product fail-fast | `ia_carmine/product/generated_patch_specs/apply_cli.py` |
| Runtime evidence proposal feed | `ia_carmine/product/repository_product/repository_change_proposals/cli.py` |
| Concrete ops into patch specs | `ia_carmine/product/generated_patch_specs/proposal_cli.py` |
| Runtime evidence proposal smoke | `Tools/validation/repository_product/repository_change_proposals_runtime_evidence_smoke/cli.py` |
| Empty product smoke | `Tools/validation/generated_patch_specs/empty_product_smoke/cli.py` |
| Markdown line-budget policy | `python -m Tools.validation check_file_line_limits` |

## Dottrina sintetica corrente

- Il Task MD è input, non prodotto.
- Il prodotto deve emergere da heap/exchange e generated patch specs.
- GPU1/Ollama advisory deve leggere evidenze runtime current-stamp.
- GPU0 deve dimostrare attività osservabile, non solo presenza di device.
- NPU resta peer micro/diagnostic finché non esiste compute lane validata.
- Metadata-only patch specs non sono prodotto PR.
- `operation_count=0` con `--apply` è fallimento.
- Draft PR finale è valido solo se `agent_review_prepare_pr.py` produce prodotto reale e il final product contract passa.
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
