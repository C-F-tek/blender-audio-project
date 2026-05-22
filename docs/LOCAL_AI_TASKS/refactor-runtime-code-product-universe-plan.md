# Refactor Runtime Code Product Universe Plan

## Scopo

Questo piano rende il prodotto codice IA-Carmine tracciabile da file locali reali fino a `CODE_PRODUCT_FULL_PATCH.md`.
Il refactor non deve aggiungere un altro layer parallelo: deve centralizzare path, target, artifact, lab, matrix e final product in contratti riusabili.

## Dataflow Attuale Osservato

Run locale esaminata:

`output/validation/operator_product_launcher_lab/heap_context_closure_20260517-111005`

Flusso visto:

1. startup/context/memory reload produce artifact e broker evidence;
2. provider GPU1/GPU0/NPU produce revisioni e proposal testuali;
3. broker esegue `run_heap_virtual_dev_environment`;
4. broker esegue `run_heap_code_execution_tool`;
5. matrix verifica 15 target reali ma conta prodotto solo da `git diff` worktree;
6. final assembler genera `CODE_PRODUCT_FULL_PATCH.md` vuoto perche non esistono diff worktree;
7. final status resta diagnostico anche quando la richiesta chiede implementazione.

## Bug Architetturali Trovati

- `python -m ia_carmine.cli run_heap_runtime_completeness_gate` usava una lista statica di target matrix.
- `python -m ia_carmine.cli run_heap_code_execution_tool` considerava concreta solo una modifica gia presente nel worktree.
- `VALIDATION_COMMANDS` poteva viaggiare vicino a `TARGET_FILES` senza un modello runtime separato.
- `output/**` e artifact citati dal provider non avevano un tipo che impedisse la promozione a source target.
- `python -m ia_carmine.cli run_heap_virtual_dev_environment` duplicava regole path/test invece di usare un resolver comune.
- `heap_final_code_product.py` distingueva poco tra target verificato, prodotto patchabile e blocco diagnostico.
- Il provider vedeva allowlist testuale, ma non un riepilogo chiaro del runtime file universe.

## Refactor Plan

1. Introdurre `ia_carmine/runtime/runtime_tool/file_refs/`.
   - Ogni ref diventa `RuntimeFileRef`.
   - Campi: repo-relative, absolute path, kind, provenance, status, consumers.
   - Stati: verified, missing, output_only, validation_only, rejected_non_allowlisted.

2. Introdurre `ia_carmine/runtime/runtime_universe/`.
   - Indicizza file reali di `Tools/`, `docs/`, `config/`.
   - Indicizza validation/test e artifact `output/validation`.
   - Riassume tool catalog, memory, context, semantic e startup artifacts quando presenti.

3. Collegare resolver e universe ai consumer.
   - Matrix usa target risolti.
   - Virtual dev usa target risolti.
   - Broker espone patch synthesis e inoltra operator request.
   - Gate pubblica il runtime universe prima dei provider.
   - Provider prompt riceve summary del runtime file universe.

4. Aggiungere `synthesize_patch_candidates.py`.
   - Scrive solo JSON/MD/.diff sotto `output/validation/**`.
   - Non modifica source.
   - Usa `git apply --check` per validare candidati.
   - I candidati validati entrano in `concrete_code_proposals`.

5. Rendere il final product rigido.
   - `CODE_PRODUCT_FULL_PATCH.md` contiene diff solo da matrix/lab/candidate validati.
   - Se target esistono ma non ci sono diff validi, status esplicito:
     `TARGETS_FOUND_BUT_NO_VALID_PATCH_CANDIDATE`.

## File Coinvolti

- `ia_carmine/runtime/runtime_tool/file_refs/*`
- `ia_carmine/runtime/runtime_universe/*`
- `ia_carmine/synthesize_patch_candidates.py`
- `ia_carmine/runtime/heap_runtime/code_execution_tool/cli.py`
- `ia_carmine/_shared/heap_code_execution_tool_core.py`
- `ia_carmine/runtime/heap_runtime/virtual_dev_environment/cli.py`
- `ia_carmine/runtime/runtime_tool/agent_broker.py`
- `ia_carmine/runtime/heap_runtime/completeness_gate/cli.py`
- `ia_carmine/_shared/heap_final_code_product.py`
- `ia_carmine/assemble_heap_final_readable_product.py`
- `Tools/validation/run_runtime_file_refs_smoke.py`
- `Tools/validation/runtime_universe/runtime_universe_smoke/cli.py`
- `Tools/validation/run_patch_candidate_synthesis_smoke.py`

## Rischi

- Alcuni script esistenti restano oversized e vanno splittati progressivamente.
- I provider possono ancora produrre testo insufficiente; la matrix ora deve produrre blocco esplicito o patch candidate validato.
- Il primo synthesis pattern e intenzionalmente conservativo: meglio pochi diff applicabili che molti sketch non validi.
- L'indicizzazione universe deve restare filesystem-first, non fallback statico.

## Validazioni

- `python -m Tools.validation check_python_syntax --repo-root . --output .\output\validation\python_syntax_oop_runtime_universe.json`
- `python -m Tools.validation run_runtime_file_refs_smoke --repo-root .`
- `python -m Tools.validation run_runtime_universe_smoke --repo-root .`
- `python -m Tools.validation run_patch_candidate_synthesis_smoke --repo-root .`
- `python -m Tools.validation run_heap_code_execution_tool_smoke --repo-root .`
- `python -m Tools.validation run_heap_virtual_dev_environment_smoke --repo-root .`
- `python -m Tools.validation run_heap_final_readable_product_smoke --repo-root .`
- `python -m Tools.validation run_operator_product_launcher_smoke --repo-root .`
- full run finale con `python -m ia_carmine.cli heap_context_closure` attraverso launcher reale.
