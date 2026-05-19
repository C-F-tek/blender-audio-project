# Tools/validation/runtime_tool context

## Role

`Tools/validation/runtime_tool` contains checks for runtime tool reports and broker-related contracts.

## Main responsibilities

- Check runtime tool report shape.
- Check broker dispatch alignment.
- Check provider tool-loop report shape.
- Check runtime file-reference reports.
- Check GPU/NPU runtime tool reports.

## Representative commands

Use through the validation dispatcher:

```powershell
python -m Tools.validation run_agent_runtime_tool_broker_smoke ...
python -m Tools.validation check_runtime_tool_broker_dispatch_alignment ...
python -m Tools.validation run_provider_tool_loop_smoke ...
python -m Tools.validation run_provider_tool_evidence_chain_smoke ...
python -m Tools.validation run_runtime_file_refs_smoke ...
python -m Tools.validation run_gpu_runtime_tool_bootstrap_smoke ...
python -m Tools.validation run_npu_runtime_tool_context_smoke ...
```

## Output role

Outputs from this area are validation reports. They help confirm that runtime tool artifacts keep the expected structure.

## Notes

- Keep checks focused and fixture-oriented where possible.
- Keep runtime reports separate from final product artifacts.
- Add dispatcher registration when adding new public checks.
