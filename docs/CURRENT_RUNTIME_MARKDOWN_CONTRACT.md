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
- Tool/lab/matrix/debug payloads and results count only through native broker request/result artifacts. Textual tool calls in prose remain non-executable evidence.
- `runtime_file_window` is a bounded repo-owned artifact reader, not a generic absolute-path reader; oversize limits and paths outside the checkout block with typed errors.
- Long responses, logs and reports return paths plus short diagnostic tails. Full content stays file-backed.
- Legacy gateway/deep-planning dispatch surfaces are historical/non-run-unica unless explicitly promoted into the current dynamic-pack/native-broker contract.

## Final product files

- `CODE_PRODUCT_FULL_PATCH.md` is the final patch/code product. It is reviewable only when it contains concrete diff/code, explicit no-op, already-integrated or non-applicable classification backed by matrix/lab/patch evidence.
- `PLAN_PRODUCT_FULL_PATCH.md` is the final real prompt/chat product from the heap. Its main content is the GPU1-generated content of any nature across heap rounds, recomposed as one readable final product. Pointer graph, recovery/congruence and heap/pointer files are technical attachments, not the main content.

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

Dry-run/effective-config output must expose the real source for each field (`cli_arg`, `profile:<name>`, or `runtime_derived`) and must not claim a hardcoded source.
