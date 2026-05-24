# ia_carmine/runtime/heap_runtime context

<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:START -->
## Current Runtime/Tool Contract (2026-05-24)

Canonical wording: `docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md`.

- GPU1/NVIDIA primary Ollama lane is the operational center and advances by heap pointer/recovery turns without waiting for GPU0/NPU sidecar completion.
- GPU0/NPU are `packet_review_only` sidecars: they start only after a reviewable GPU1 packet, do not close product, and remain deferred evidence until a later GPU1 turn consumes their pointer ids.
- Tool/lab/matrix/debug reporting must distinguish `lab_called`, `lab_report_written`, `lab_usable` and `lab_status`; attempted tool calls are evidence, not automatic usable lab output.
- `FINAL_PRODUCT` is single: text, code, or text+code. `PLAN_PRODUCT_FULL_PATCH.md` is its text/prose surface; `CODE_PRODUCT_FULL_PATCH.md` is its code/diff surface only when verified code exists. GPU1 emits causal `FINAL_PRODUCT_DELTA` records; blocked status is runtime/gate classification, not GPU1 output.
- Missing optional values stay empty/null; required missing devices or provider prerequisites raise or block with a typed reason rather than emitting placeholder text.
- Complete runs require explicit config flags, including `--files-per-round`, `--gpu0-ollama-num-ctx`, `--npu-micro-start-mode`, `--npu-final-wait-seconds` and `--max-degraded-lanes`.
<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:END -->


## Role

`ia_carmine/runtime/heap_runtime` contains runtime-facing tools used by the heap closure and product cycle: completeness gate invocation, code execution/matrix lab, virtual development environment, event pointers and product packaging.

This area bridges runtime orchestration and deterministic product evidence.

## Main responsibilities

- Invoke heap runtime closure through `ia_carmine run` explicit parameters.
- Run completeness gates and terminal checks.
- Execute code-oriented lab/matrix checks in controlled mode.
- Inspect targets through import/help/AST/smoke probes where supported.
- Produce code execution reports and debug lab evidence.
- Maintain event pointer artifacts.
- Package runtime product evidence without applying source changes directly.

## Typical tool surface

Use via dispatcher:

```powershell
python -m ia_carmine.cli run_heap_runtime_completeness_gate ...
python -m ia_carmine.cli run_heap_code_execution_tool ...
python -m ia_carmine.cli run_heap_code_execution_matrix ...
python -m ia_carmine.cli run_heap_virtual_dev_environment ...
python -m ia_carmine.cli heap_event_pointers ...
python -m ia_carmine.cli build_heap_runtime_product_package ...
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
