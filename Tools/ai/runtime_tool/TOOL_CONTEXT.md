# Tools/ai/runtime_tool context

## Role

`Tools/ai/runtime_tool` contains broker-facing runtime tools and metadata used by heap/provider workflows. It provides controlled tool execution, file references, usage telemetry, capability manifests and runtime debug support.

This area is the tool-control plane. It should reduce ad-hoc execution and make tool results auditable.

## Main responsibilities

- Expose brokered tools through stable CLIs.
- Build runtime tool capability manifests.
- Collect runtime tool usage telemetry.
- Resolve and classify runtime file references.
- Provide debug-lab support for agent/tool interactions.
- Keep tool execution evidence structured.

## Representative command surface

Use through the AI dispatcher:

```powershell
python -m Tools.ai agent_runtime_tool_broker ...
python -m Tools.ai runtime_tool_broker ...
python -m Tools.ai build_runtime_tool_capability_manifest ...
python -m Tools.ai runtime_tool_usage_telemetry ...
python -m Tools.ai runtime_file_refs ...
python -m Tools.ai agent_runtime_debug_lab ...
```

## Broker model

```text
provider/request -> broker request -> controlled tool invocation -> structured tool output
-> guardrails/evidence -> heap state or downstream matrix
```

Tool output must preserve enough information for later validation. Broker request/response should remain lossless enough for review.

## Guardrails

- Do not expose uncontrolled free shell behavior through this layer.
- Distinguish generated report writes from source writes.
- Do not treat runtime file refs as patch targets without downstream verification.
- Emit `provider_execution_performed`, `patch_application_performed`, `source_writes_performed` and related flags accurately when available.
- Keep telemetry as evidence, not as product.

## Expected artifacts

```text
runtime tool capability manifest
runtime usage telemetry
broker request/result reports
file reference classification reports
runtime debug lab reports
```

## Extension notes

New runtime tools should be registered through `Tools/ai/dispatch.py` and validated through `Tools/validation/runtime_tool`. Prefer small tool adapters with explicit allowed arguments.
