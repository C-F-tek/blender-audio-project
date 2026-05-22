# Tools/validation/heap_runtime context

## Role

`Tools/validation/heap_runtime` contains smoke tests and contract checks for heap runtime behavior.

It validates startup, completeness gate behavior, source allowlists, terminal invariants, code execution matrix, virtual development environment, preview/rewrite safety and final readable product assembly.

It supports the runtime side of:

```text
docs/HEAP_EXCHANGE_USEFUL_MODEL.md
docs/STANDALONE_HEAP_SURFACE_MODEL.md
docs/REAL_PRODUCT_RUN_MODEL.md
docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

## Responsibilities

- Verify heap runtime completeness gate behavior.
- Check file-backed startup/request handling.
- Validate startup context ingestion.
- Validate source allowlist and source anchor behavior.
- Validate code execution matrix and virtual dev reports.
- Check final readable product assembly rules.
- Check terminal invariants and non-applicable product states.
- Guard against unsafe negative preview/rewrite behavior.
- Preserve the distinction between runtime evidence and apply-ready product.

## Representative command surface

Use through the validation dispatcher:

```powershell
python -m Tools.validation run_heap_runtime_completeness_gate_smoke ...
python -m Tools.validation run_heap_code_execution_tool_smoke ...
python -m Tools.validation run_heap_virtual_dev_environment_smoke ...
python -m Tools.validation run_heap_final_readable_product_smoke ...
python -m Tools.validation run_heap_file_backed_request_startup_smoke ...
python -m Tools.validation run_heap_startup_context_ingestion_smoke ...
python -m Tools.validation run_heap_source_allowlist_contract_smoke ...
python -m Tools.validation run_heap_source_anchor_priority_smoke ...
python -m Tools.validation run_heap_negative_preview_rewrite_contract_smoke ...
python -m Tools.validation run_heap_gate_terminal_invariants_smoke ...
```

## Validation model

```text
runtime behavior -> report artifact -> assertion -> pass/fail/blocked contract
```

A passing smoke only proves the property under test.

## Product-boundary checks

Heap runtime validation should protect these boundaries:

```text
startup file/context exists != run completed
runtime evidence != code product
readable product != apply-ready patch
negative preview/rewrite != source write
matrix/lab output needs intake/review before apply
```

## Boundaries

- Do not use smokes to bypass product gates.
- Keep fixtures isolated.
- Do not write real source files from validation unless using a fixture-only apply test.
- Distinguish diagnostic output from apply-ready code product.
- Missing or non-applicable product must be explicit, not disguised as success.

## Expected artifacts

```text
smoke report JSON/MD
fixture output
startup context ingestion evidence
terminal invariant report
code execution matrix smoke evidence
virtual dev environment smoke evidence
final readable product smoke evidence
negative preview/rewrite contract evidence
```

## Extension notes

When changing heap runtime behavior, add or update a validation in this area before relying on the new behavior in operator flows. Update `ia_carmine/runtime/heap_runtime/TOOL_CONTEXT.md` and `docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md` when semantic meaning changes.