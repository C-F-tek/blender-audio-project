# Tools/validation/runtime_tool context

## Role

`Tools/validation/runtime_tool` contains checks for runtime tool reports, broker-related contracts, runtime file references, debug-lab reports and provider-tool evidence chains.

It validates the control-plane/evidence layer described by:

```text
ia_carmine/runtime/runtime_tool/TOOL_CONTEXT.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
docs/HEAP_EXCHANGE_USEFUL_MODEL.md
docs/COMPACT_EVIDENCE_MODEL.md
```

## Main responsibilities

- Check runtime tool report shape.
- Check broker dispatch alignment.
- Check provider tool-loop report shape.
- Check provider tool-evidence chain reports.
- Check runtime file-reference reports.
- Check runtime feedback/guidance fallback behavior.
- Check runtime debug-lab reports.
- Check GPU/NPU runtime tool reports.
- Keep runtime tool evidence separate from final product artifacts.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation run_agent_runtime_tool_broker_smoke ...
python -m Tools.validation check_runtime_tool_broker_dispatch_alignment ...
python -m Tools.validation run_provider_tool_loop_smoke ...
python -m Tools.validation run_provider_tool_evidence_chain_smoke ...
python -m Tools.validation run_runtime_tool_feedback_loop_smoke ...
python -m Tools.validation run_runtime_tool_guidance_fallback_smoke ...
python -m Tools.validation run_runtime_file_refs_smoke ...
python -m Tools.validation run_agent_runtime_debug_lab_smoke ...
python -m Tools.validation run_gpu_runtime_tool_bootstrap_smoke ...
python -m Tools.validation run_npu_runtime_tool_context_smoke ...
python -m Tools.validation run_npu_runtime_tool_execution_smoke ...
python -m Tools.validation run_npu_runtime_tool_fallback_smoke ...
```

## Output role

Outputs from this area are validation reports. They help confirm that runtime tool artifacts keep the expected structure and preserve evidence needed by heap/exchange/product gates.

## Boundary rules

- A broker report is evidence, not final product.
- File refs are evidence/classification, not source patch targets by themselves.
- Debug-lab reports are diagnostics, not product.
- Tool-loop success must not be confused with provider product success.
- `generic_write` smoke coverage must prove GPU1/GPU0 can expose it through Ollama native tool schemas and that it remains broker evidence until the heap validates the three-refinement product rule.
- Validation should check flags such as provider execution, tool execution, source writes and patch application when reports expose them.

## Notes

- Keep checks focused and fixture-oriented where possible.
- Keep runtime reports separate from final product artifacts.
- Add dispatcher registration when adding new public checks.
- Update `ia_carmine/runtime/runtime_tool/TOOL_CONTEXT.md` and `docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md` when runtime tool semantics change.
