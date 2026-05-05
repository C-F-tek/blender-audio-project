# Future tool usage

Il controlled applier sarà usato come base per tool futuri.

## Pattern di estensione

Ogni nuovo kind deve aggiungere:

1. classificatore;
2. patch-spec;
3. transform controllato;
4. dry-run diff;
5. smoke;
6. docs;
7. validation post-apply.

## Candidati futuri

- `markdown_split_apply`;
- `docs_index_refresh`;
- `python_helper_extract_plan`;
- `gpu_telemetry_contract_patch`;
- `npu_gpu0_contract_patch`;
- `bundle_manifest_refresh`.

## Regola

Nessun nuovo kind deve entrare in `ALLOWED_APPLY_KINDS` senza smoke specifico.
