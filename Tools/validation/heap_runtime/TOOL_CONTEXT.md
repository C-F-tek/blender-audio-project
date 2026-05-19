# Tools/validation/heap_runtime context

## Role

`Tools/validation/heap_runtime` contains smoke tests and contract checks for heap runtime behavior.

It validates startup, completeness gate behavior, source allowlists, terminal invariants, code execution matrix, virtual development environment and final readable product assembly.

## Responsibilities

- Verify heap runtime completeness gate behavior.
- Check file-backed startup/request handling.
- Validate source allowlist and source anchor behavior.
- Validate code execution matrix and virtual dev reports.
- Check final readable product assembly rules.
- Check terminal invariants and non-applicable product states.

## Representative command surface

Use through the validation dispatcher:

```powershell
python -m Tools.validation run_heap_runtime_completeness_gate_smoke ...
python -m Tools.validation run_heap_code_execution_tool_smoke ...
python -m Tools.validation run_heap_virtual_dev_environment_smoke ...
python -m Tools.validation run_heap_final_readable_product_smoke ...
python -m Tools.validation run_heap_file_backed_request_startup_smoke ...
python -m Tools.validation run_heap_source_allowlist_contract_smoke ...
python -m Tools.validation run_heap_source_anchor_priority_smoke ...
python -m Tools.validation run_heap_gate_terminal_invariants_smoke ...
```

## Validation model

```text
runtime behavior -> report artifact -> assertion -> pass/fail contract
```

A passing smoke only proves the property under test.

## Boundaries

- Do not use smokes to bypass product gates.
- Keep fixtures isolated.
- Do not write real source files from validation unless using a fixture-only apply test.
- Distinguish diagnostic output from apply-ready code product.

## Expected artifacts

```text
smoke report JSON/MD
fixture output
terminal invariant report
code execution matrix smoke evidence
final readable product smoke evidence
```

## Extension notes

When changing heap runtime behavior, add or update a validation in this area before relying on the new behavior in operator flows.