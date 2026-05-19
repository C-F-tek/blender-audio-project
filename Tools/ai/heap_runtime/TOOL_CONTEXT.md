# Tools/ai/heap_runtime context

## Role

`Tools/ai/heap_runtime` contains runtime-facing tools used by the heap closure and product cycle: launcher command construction, completeness gate invocation, code execution/matrix lab, virtual development environment, event pointers and product packaging.

This area bridges runtime orchestration and deterministic product evidence.

## Main responsibilities

- Build or invoke heap runtime launch commands.
- Run completeness gates and terminal checks.
- Execute code-oriented lab/matrix checks in controlled mode.
- Inspect targets through import/help/AST/smoke probes where supported.
- Produce code execution reports and debug lab evidence.
- Maintain event pointer artifacts.
- Package runtime product evidence without applying source changes directly.

## Typical tool surface

Use via dispatcher:

```powershell
python -m Tools.ai heap_runtime_launcher_command ...
python -m Tools.ai run_heap_runtime_completeness_gate ...
python -m Tools.ai run_heap_code_execution_tool ...
python -m Tools.ai run_heap_code_execution_matrix ...
python -m Tools.ai run_heap_virtual_dev_environment ...
python -m Tools.ai heap_event_pointers ...
python -m Tools.ai build_heap_runtime_product_package ...
```

## Code product rule

The matrix/lab layer is the deterministic source for code product applicability.

```text
provider proposal -> evidence
matrix/lab diff/code -> code product candidate
intake/review -> safe apply or blocked/manual review
```

A code product must not be declared apply-ready merely because a provider returned text.

## Expected artifacts

Typical runtime artifacts include:

```text
heap_runtime_completeness_gate_report.json/.md
heap_code_execution_tool.json/.md
heap_code_execution_tool_debug_lab.json
virtual_dev_environment_report.json/.md
event pointer reports
runtime product package reports
```

## Guardrails

- No free shell exposure.
- No source writes unless explicitly routed through a reviewed apply path.
- No Git writes from runtime lab/matrix tools.
- `output/**` is local runtime evidence, not Git-trackable source.
- Failed or empty code product must be explicit, not disguised as success.

## Extension notes

When adding runtime capabilities, add matching validation under `Tools/validation/heap_runtime` or `Tools/validation/runtime_universe`. Prefer report-only first for risky capabilities.
