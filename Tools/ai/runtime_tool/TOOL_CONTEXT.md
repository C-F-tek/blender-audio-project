# Tools/ai/runtime_tool context

## Role

`Tools/ai/runtime_tool` contains broker-facing runtime tools and metadata used by heap/provider workflows. It provides controlled tool execution, file references, capability manifests and runtime debug support.

This area is the tool-control plane for Universo IA. It should reduce ad-hoc execution and make tool results auditable.

It concretizes parts of:

```text
docs/HEAP_EXCHANGE_USEFUL_MODEL.md
docs/STANDALONE_HEAP_SURFACE_MODEL.md
docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md
docs/COMPACT_EVIDENCE_MODEL.md
docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
```

## Main responsibilities

- Expose brokered tools through stable CLIs.
- Build runtime tool capability manifests.
- Resolve and classify runtime file references.
- Provide debug-lab support for agent/tool interactions.
- Keep tool execution evidence structured.
- Distinguish provider execution, tool execution, generated report writes, patch application and source writes.

## Representative command surface

Use through the AI dispatcher:

```powershell
python -m Tools.ai agent_runtime_tool_broker ...
python -m Tools.ai runtime_tool_broker ...
python -m Tools.ai build_runtime_tool_capability_manifest ...
python -m Tools.ai runtime_file_refs ...
python -m Tools.ai agent_runtime_debug_lab ...
```

## Broker model

```text
provider/request
-> broker request
-> controlled tool invocation
-> structured tool output
-> guardrails/evidence
-> heap state or downstream matrix
```

Tool output must preserve enough information for later validation. Broker request/response should remain lossless enough for review.

## Runtime file refs model

`runtime_file_refs` helps classify files that appear in runtime reports.

It should answer:

```text
what file was referenced?
where did the reference come from?
is it source, generated report, compact evidence, runtime output, or unknown?
is it safe to use as evidence?
is it unsafe to treat as a patch target?
```

Runtime file references are not patch targets unless downstream source inspection and product-boundary validation confirm them.

## Debug-lab model

`agent_runtime_debug_lab` is diagnostic support.

It may reveal:

```text
tool visibility
tool request flow
provider/tool mismatch
runtime bridge gaps
artifact classification problems
```

It is evidence, not a product.

## Guardrails

- Do not expose uncontrolled free shell behavior through this layer.
- Distinguish generated report writes from source writes.
- Do not treat runtime file refs as patch targets without downstream verification.
- Emit `provider_execution_performed`, `tool_execution_performed`, `patch_application_performed`, `source_writes_performed` and related flags accurately when available.
- Keep debug-lab output out of source modification paths unless converted into reviewed product evidence.

## Expected artifacts

```text
runtime tool capability manifest
broker request/result reports
file reference classification reports
runtime debug lab reports
provider tool evidence reports
```

## Validation expectations

Relevant validation areas:

```powershell
python -m Tools.validation run_agent_runtime_tool_broker_smoke ...
python -m Tools.validation run_runtime_tool_feedback_loop_smoke ...
python -m Tools.validation run_runtime_tool_guidance_fallback_smoke ...
python -m Tools.validation run_runtime_file_refs_smoke ...
python -m Tools.validation run_agent_runtime_debug_lab_smoke ...
python -m Tools.validation run_provider_tool_loop_smoke ...
python -m Tools.validation run_provider_tool_evidence_chain_smoke ...
python -m Tools.validation check_runtime_tool_broker_dispatch_alignment ...
```

## Extension notes

New runtime tools should be registered through `Tools/ai/dispatch.py` and validated through `Tools/validation/runtime_tool`. Prefer small tool adapters with explicit allowed arguments.
