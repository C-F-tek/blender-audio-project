<!-- IA-CARMINE-MD-SPLIT: index -->
# Indice — UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md

## Status

Current launcher contract index.

Use this contract with the current heap/exchange and patchkit operating model:

```text
../LOCAL_AI_TASKS/heap-exchange-and-patchkit-operating-model-2026-05-09.md
../LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md
../LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md
```

When reviewing product-path runs, verify that the launcher manifest/phase reports expose heap/exchange entry, runtime state, exit product, lifecycle validation and patchkit or deterministic patch bridge reports when those lanes are selected.

Documento monolitico trasformato da file `docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md` a directory-form.
Limite massimo configurato: `400` righe per file Markdown.

## Parti

1. [`part-001.md`](part-001.md)
2. [`part-002.md`](part-002.md)

## Nomenclatura canonica

```text
0Full10 = run unica concettuale
Full0To10 / -Full0To10 = spelling CLI/flag di compatibilità quando presente nel launcher
run unica = workflow completo 0-to-10 sul perimetro attivo del progetto
```

Regola pratica: `0Full10` non deve diventare un flag magico. La run unica deve essere descrivibile dalla combinazione esplicita degli altri parametri: task input, run identity, real-run activation, intensity/budget, provider lanes, evidence lanes, patch/review lanes e opt-out `-No*`. Il flag `-Full0To10`, quando usato, è una scorciatoia compatibile che seleziona quel profilo completo; nel tempo può essere assorbito dalla configurazione esplicita delle lane.

## Guida operativa parametri

Per scegliere correttamente i parametri del launcher senza leggere l'intera superficie CLI, usare:

```text
docs/LOCAL_AI_TASKS/unified-launcher-parameter-decision-map-2026-05-09.md
```

Regola pratica: scegliere prima la lane/prodotto (`smoke`, fase singola, `0Full10`/run unica, `LightFull0To10`, provider, review PR), poi modificare solo il gruppo di parametri pertinente.

## Mappa profondità capability

Per capire cosa esiste davvero, quanto è profondo, cosa produce e quali potenzialità sono attive o solo target, usare:

```text
docs/LOCAL_AI_TASKS/current-capability-depth-map-2026-05-09.md
```

Regola pratica: non confondere un target architetturale con una capability eseguita. Una capability è provata solo da manifest, phase report, validator report, telemetry, observer pointer, bundle o report prodotto dalla lane.

## Superfici prodotto post-heap/exchange

Per run che preparano prodotti review PR o patch, il contratto va letto insieme a queste superfici:

```text
heap_exchange_runtime_entry.json/md
heap_exchange_runtime_state.jsonl
heap_exchange_runtime_exit_product.json/md
heap_exchange_runtime_lifecycle_<stamp>.json/md
patchkit_apply_report quando una patchkit bundle viene applicata
patch_suggestion_bundle_apply report per il bridge legacy di patch suggestion
prepare_review_pr report/PR product
```

Il successo del run non va inferito da file existence o metadata-only patch drafts.

## Regola

Split directory-form conforme alla policy: `nomefile.md/part-xxx.md`.
