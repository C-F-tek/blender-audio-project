# Current runtime Markdown contract

## Status

Current repository-wide Markdown contract for IA-Carmine runtime, provider, tool/lab and product wording.

This file is the canonical wording target for Markdown refreshes. Older runbooks, task notes and chat handoffs remain historical unless a current root/model document links them as active.

## Provider lane semantics

- `GPU1/NVIDIA primary Ollama lane` is the operational center. GPU1 advances through heap pointers independently and does not wait for GPU0/NPU sidecar work to continue its own cycle.
- GPU0 and NPU are sidecars with `sidecar_scope_mode=packet_review_only`. They start only after a reviewable GPU1 packet exists, inspect that packet and related refs, and do not perform broad exploration, final synthesis or product closure.
- GPU0/NPU sidecar evidence is deferred/non-terminal evidence. It can hold product acceptance only after GPU1 consumes it in a later pointer/recovery/congruence turn.
- GPU1 recovery/congruence must preserve pointer continuity fields: `previous_block_id`, `refines_block_id`, `resume_from_block_id`, consumed peer ids, target pointer and revision.
- If the GPU1 cycle or soft budget ends, the run exits with a product/blocked/continuation classification; it does not need exhaustive validation of every historical pointer.

## Tool, lab, matrix and debug semantics

Tool calling, virtual dev, code matrix and debug lab are effective runtime surfaces, not decorative status text.

Reports must distinguish:

- `lab_called`: a lab/matrix/debug/tool surface was requested or invoked.
- `lab_report_written`: a concrete report artifact was written.
- `lab_usable`: the report had real targets/evidence usable for product decisions.
- `lab_status`: explicit status such as `usable`, `called_no_targets`, `called_failed`, `report_missing`, or `not_requested`.

Tool calls that were attempted but failed remain failed tool evidence. They must not be hidden as absence, and they must not be promoted to usable lab evidence without report and target proof.

## File-backed transport semantics

HTTP/API coordinates work at boundaries; it is not the container for the runtime universe. Large operator requests, GPU1 prompt/chat material, heap context, RAG/context chunks, patch candidates, provider outputs and stdout/stderr must be persisted as run artifacts and passed by stable refs.

- Small inline JSON is allowed only for healthcheck, status, metadata and simple job control.
- Medium/large payloads use `payload_file` or explicit artifact refs with `path`, `kind`, `bytes` and `sha256`.
- Multi-file context uses `ia_carmine_runtime_payload_manifest` plus semantic chunks and deterministic `read_order`.
- Artifact refs also declare `source`/provenance; manifest validation checks file existence, bytes and sha256 rather than treating non-empty JSON as proof.
- `gpu1_dynamic_context_pack` is the active provider context surface; legacy `startup_unified_context_pack` can remain attached evidence but is not the terminal hard blocker.
- GPU1 keeps its full prompt/chat/product role; the mass is materialized on disk and referenced, not sliced into body excerpts. Ollama/provider reports store prompt refs, bytes, chars and sha256, not the request prompt body.
- Tool/lab/matrix/debug payloads and results count only through native broker request/result artifacts. For Ollama/Qwen this means parsed `message.tool_calls[]`, the exact qwen2.5-coder template-native `<tool_call>{"name": ..., "arguments": ...}</tool_call>` envelope, or the strict qwen2.5-coder chat-tools adapter that accepts only a whole-message JSON object with registered `name` and `arguments` produced by `session.chat(..., tools=...)`. Markdown, fenced JSON, mixed prose and prompt-only tool names remain `provider_textual_tool_call_not_executable`.
- If GPU1 requests a broker tool, the GPU1 packet enters `pending_tool_result`: GPU0/NPU wait, the broker writes `tool_result`, and GPU1 must resume through the Ollama chat API with a `role="tool"` / `tool_name=<function>` message whose JSON `content` carries the broker result refs. GPU1 must then cite the result in `CONSUMED_EVIDENCE/tool_or_matrix_refs`.
- The active `qwen2.5-coder:14b` Ollama model reports the `tools` capability and its local template expects assistant tool calls as `<tool_call>{"name": ..., "arguments": ...}</tool_call>` with no surrounding text, and tool results as `role=tool` content rendered inside `<tool_response>`. On the current workstation the model can instead emit the same call as a whole-message JSON object; the Ollama adapter may normalize that exact `chat(tools=...)` shape, but it must not normalize Markdown/prose or JSON from non-tool chat paths.
- `tool_result_written` is not product evidence by itself. It becomes operational evidence only when the same GPU1 lane consumes it; otherwise the run records `gpu1_tool_result_pending` or `gpu1_requested_tool_result_not_consumed`.
- `runtime_file_refs` proves target/path resolution only. It does not prove that GPU1 has read source content.
- `runtime_file_window` is the brokered file-content read surface. It is a bounded repo-owned artifact reader, not a generic absolute-path reader; oversize limits and paths outside the checkout block with typed errors.
- Long responses, logs and reports return paths plus short diagnostic tails. Full content stays file-backed.
- Legacy gateway/deep-planning dispatch surfaces are historical/non-run-unica unless explicitly promoted into the current dynamic-pack/native-broker contract.

## Final product surfaces

- `FINAL_PRODUCT` is one product: text, code, or text+code.
- `PLAN_PRODUCT_FULL_PATCH.md` is the text/prose/decision surface of that single product.
- `CODE_PRODUCT_FULL_PATCH.md` is the code/diff surface of that same product only when verified code exists.
- When the product is text-only, `CODE_PRODUCT_FULL_PATCH.md` may report `NO_APPLICABLE_CODE_PRODUCT` while the run still has a valid text product surface.
- GPU1 contributes `FINAL_PRODUCT_DELTA` records during each heap turn. GPU1 must declare `FINAL_PRODUCT_KIND`, `FINAL_PRODUCT_ACTION`, `CURRENT_POINTER`, `CONSUMED_EVIDENCE`, `NEXT_RUNTIME_INTENT` and `FINAL_PRODUCT_DELTA`.
- GPU1 cannot emit a grounded code diff for `FINAL_PRODUCT_KIND=code` or `FINAL_PRODUCT_KIND=text_and_code` until it has consumed a successful API-native broker `runtime_file_window` result for the target source content and cites that result in `CONSUMED_EVIDENCE`. Path allowlists, prompt context, `runtime_file_refs` and raw prose are not file-content evidence.
- If GPU1 has not read the target source content, it may emit a text-only delta or `gpu1_decision=needs_refine` with `NEXT_RUNTIME_INTENT` requesting `runtime_file_window`; any diff-like code delta is classified as `gpu1_code_delta_without_file_read`.
- GPU1 does not emit `blocked` as a final-product value. `blocked_with_reason` is a runtime/gate classification.
- The final composer must apply ordered GPU1 deltas through `append`, `replace`, `supersede` and `refine`; it must not create a new final GPU synthesis and must not present raw proposal-body collage as the product.
- Pointer graph, recovery/congruence and heap/pointer files remain technical attachments proving how the product surface was composed.

## Missing value and device policy

Markdown and reports must not render text placeholder tokens for absent values. Optional absent values remain empty/null. Required missing devices or required provider prerequisites raise or block with a typed reason instead of producing fake reports.

## Terminal smoke semantics

Terminal smoke reports must separate expected negative fixture errors from real regressions:

- `expected_negative_fixture_errors` or equivalent: deliberate `AI STAI GIOCANDO` fixture violations used to prove the guard.
- `unexpected_errors`: real errors that fail the smoke.

A passed terminal negative smoke proves the guard detected fixture violations; it does not mean those violations happened in the current runtime.

## Explicit complete-run command contract

Complete/operator-facing runs must provide all required runtime flags explicitly, including:

```text
--files-per-round
--gpu0-ollama-num-ctx
--npu-micro-start-mode
--npu-final-wait-seconds
--max-degraded-lanes
```

Dry-run/effective-config output must expose the real source for each field (`cli_arg`, `optional_unset`, or `runtime_derived`) and must not claim a hardcoded/profile source.

RAG has its own explicit profile surface: `--rag-profile`. It scopes retrieval/index/query context behavior only. It must not select provider models, hardware lanes, complete-run semantics, validator suites or runtime universe profiles.
