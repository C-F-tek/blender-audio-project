# ia_carmine/runtime/runtime_tool context

<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:START -->
## Current Runtime/Tool Contract (2026-05-24)

Canonical wording: `docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md`.

- GPU1/NVIDIA primary Ollama lane is the operational center and advances by heap pointer/recovery turns without waiting for GPU0/NPU sidecar completion.
- GPU0/NPU are `packet_review_only` sidecars: they start only after a reviewable GPU1 packet, do not close product, and remain deferred evidence until a later GPU1 turn consumes their pointer ids.
- Tool/lab/matrix/debug reporting must distinguish `lab_called`, `lab_report_written`, `lab_usable` and `lab_status`; attempted tool calls are evidence, not automatic usable lab output.
- `CODE_PRODUCT_FULL_PATCH.md` is the final patch/code product; `PLAN_PRODUCT_FULL_PATCH.md` is the final recomposed GPU1 prompt/chat product, with pointer graph and recovery/congruence as technical attachments.
- HTTP/API coordinates only job control and refs; filesystem artifacts carry context mass, heap chunks, provider inputs/outputs, logs and `ia_carmine_runtime_payload_manifest` evidence.
- Missing optional values stay empty/null; required missing devices or provider prerequisites raise or block with a typed reason rather than emitting placeholder text.
- Complete runs require explicit config flags, including `--files-per-round`, `--gpu0-ollama-num-ctx`, `--npu-micro-start-mode`, `--npu-final-wait-seconds` and `--max-degraded-lanes`.
<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:END -->


## Role

`ia_carmine/runtime/runtime_tool` contains broker-facing runtime tools and metadata used by heap/provider workflows. It provides controlled tool execution, file references, capability manifests and runtime debug support.

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
python -m ia_carmine.cli agent_runtime_tool_broker ...
python -m ia_carmine.cli runtime_tool_broker ...
python -m ia_carmine.cli build_runtime_tool_capability_manifest ...
python -m ia_carmine.cli runtime_file_refs ...
python -m ia_carmine.cli runtime_file_window ...
python -m ia_carmine.cli agent_runtime_debug_lab ...
python -m ia_carmine.cli generic_write ...
python -m ia_carmine.cli rag_context_pack ...
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

HTTP/API requests to this layer carry small control metadata or `payload_file`/artifact refs. Large operator requests, provider proposal text, debug-lab request JSON and runtime-file-ref text are materialized under the run/tool output directory before execution and reported with `source`, `bytes` and `sha256`. The broker executor validates schemas after materialization, so tool enforcement and provider schema publication use the same API-ready contract.

`generic_write` writes refined request/action-plan Markdown/JSON for the next provider turn. It is broker evidence when called by GPU1/GPU0 native tools; after three consumed refinements the heap may expose it as a readable refined product, including code content, without claiming source writes or patch application.

`rag_context_pack` builds the internal SQLite/FTS5/vector context pack as broker evidence. It is a base context requirement when wired into heap startup, but it remains context only: no provider execution, source writes or patch application.

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

`runtime_file_window` is the read-only companion for large file-backed artifacts. It reads bounded `{path, offset, limit}` byte windows from repo-owned artifacts only, rejects paths outside the checkout and rejects limits above the configured maximum so stdout/stderr/logs/context can remain on disk without stuffing full content back into provider or HTTP bodies.

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
python -m Tools.validation run_file_backed_transport_contract_smoke ...
python -m Tools.validation run_agent_runtime_debug_lab_smoke ...
python -m Tools.validation run_provider_tool_loop_smoke ...
python -m Tools.validation run_provider_tool_evidence_chain_smoke ...
python -m Tools.validation run_rag_broker_alignment_smoke ...
python -m Tools.validation check_runtime_tool_broker_dispatch_alignment ...
```

## Extension notes

New runtime tools should be registered through `ia_carmine/dispatch.py` and validated through `Tools/validation/runtime_tool`. Prefer small tool adapters with explicit allowed arguments.
