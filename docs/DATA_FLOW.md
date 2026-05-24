# DATA FLOW — IA-Carmine Heap/Runtime Contract

This file is a required context-pack contract for runtime data-flow validation.
It describes the expected flow of information through the heap, brokered tools, memory, chunks, providers and final product output.

## Primary flow

The runtime flow is:

1. request input
2. heap user_request event
3. brokered tool catalog discovery
4. shared memory inventory
5. operational memory write
6. operational memory search
7. transient request context build
8. semantic code chunk selection
9. AI context pack build
10. semantic evidence chunk build when evidence/context exceeds direct prompt budget
11. GPU0 peer observation
12. NPU micro-task/auditor observation
13. GPU1 cumulative synthesis
14. product signal
15. output contract

## Data surfaces

The flow must expose these data surfaces when the heap runtime completeness gate is used:

- events.jsonl
- heap snapshot
- broker bridge report
- broker tool output artifacts
- memory inventory report
- operational memory write/read reports
- transient request context report
- selected semantic chunks report
- AI context pack report and evidence report
- semantic evidence chunk manifest
- GPU0 provider report
- NPU micro-task report
- GPU1 provider report
- final heap runtime completeness report

## Memory and chunk semantics

Memory is not decorative. Operational memory must be both written and queried inside the same run when the heartbeat/request path requires memory proof.

Chunking is not simple truncation. Chunk tools exist to turn oversized repository/context surfaces into bounded logical units that can be consumed by different providers while remaining linked through manifests and previous/next relationships.

A valid large-context run should be able to distribute or expose different logical pieces to different provider lanes, while GPU1 receives enough context to synthesize a single product output.

## Provider visibility semantics

Provider lanes must not operate as isolated scripts.

GPU0, NPU and GPU1 are separate lanes inside one shared heap/team runtime. The final GPU1 prompt/context must make clear that GPU1 is not alone and must consume:

- request input
- memory outputs
- context/chunk outputs
- GPU0 role contribution
- NPU role contribution
- relevant validation evidence

If GPU1 produces a final response that contradicts visible team evidence, the final response is semantically invalid.

## Product readiness semantics

product_status may be ready only when all required runtime surfaces for the selected gate are present and valid.

For heap heartbeat/team runtime validation, ready requires at least:

- provider_execution_performed = true
- provider_lane_count includes GPU0, NPU and GPU1 when teamwork is required
- tool_request_count > 0
- tool_execution_count > 0
- bridge_reports is not empty
- operational memory write count > 0
- operational memory search count > 0
- shared context evidence exists
- semantic chunk/context evidence exists
- AI context pack evidence exists when the profile requires it
- response_text_ref or long-response artifact is present, readable, checksum verified and `full_verified=true`; response tails are preview/fallback only
- errors is empty

If any required surface is missing, the product must be blocked_with_reason.

## Guardrails

Required files must not be muted to make validation pass.

The correct response to missing required data-flow contracts is to restore, update or version the required contract file.

Do not bypass broker, memory, chunk or context-pack layers when validating the heap universe.
