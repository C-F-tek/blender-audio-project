# Final Purpose Run-Owned Readable Product - 2026-05-14

## Operator request

Run the heap universe long enough to regenerate full startup context and produce the final product through the run itself.

The final product is not a manual recomposition outside the run. The run must call the deterministic final readable product assembler after composer and external post-run packaging, then verify that the Documents package contains:

```text
FINAL_READABLE_PRODUCT.md
FINAL_READABLE_PRODUCT.txt
FINAL_READABLE_PRODUCT.json
adjacent aicarmine_heap_final_proposals_<stamp>.zip
```

## Required decision quality

The final readable product must be a complete operator decision document, not only one AI iteration.

It must include:

- final decision status;
- why provider proposal output is apply-ready or diagnostic-only;
- concrete code changes proposed for review;
- file-level targets;
- validation commands;
- run evidence status;
- code execution matrix status;
- risks and blocked conditions;
- clear next operator decision.

## Required code matrix scope

The code execution matrix must include the run-owned final readable product path:

```text
Tools/ai/assemble_heap_final_readable_product.py
Tools/validation/run_heap_final_readable_product_smoke.py
Tools/ai/heap_context_closure/cli.py
Tools/ai/heap_runtime/completeness_gate/cli.py
Tools/ai/runtime_tool/agent_broker.py
Tools/ai/heap_runtime/code_execution_tool/cli.py
Tools/ai/_shared/heap_code_execution_tool_core.py
Tools/ai/_shared/heap_final_code_product.py
Tools/ai/_shared/heap_final_readable_synthesis.py
Tools/ai/heap_final_proposals/cli.py
Tools/ai/_shared/heap_proposal_gate.py
Tools/validation/heap_runtime/code_execution_tool_smoke/cli.py
Tools/validation/test_proposal_gate.py
```

## Runtime expectations

Use regenerated startup context, current repository evidence, prior revision context when useful, GPU1/GPU0/NPU provider lanes, broker tool evidence and deterministic validators.

GPU1 may enrich already written chunks. A richer final product may be a composition of previous chunks, code matrix evidence, peer reviews and deterministic gates.

If provider patch candidates are rejected, the run must still publish a readable diagnostic-only final product that explains the rejected candidates and exposes the deterministic code-change decision surface.

The final product must not be a one-shot GPU1 summary. GPU1 works inside the heap on pointer chunks, can move backward/forward through previous/refines/resume pointers, and can use brokered debug/tool evidence. The final document is assembled deterministically from N persisted turns, pointer blocks, peer reviews, virtual development environment reports, code execution matrix evidence and external long-response chunks.

The product may be long. It should scale with the number of persisted turns/files instead of being bounded by a single provider context window.

The final product must be a decision synthesis, not duplicated raw pointer text. It should collapse repeated provider chunks into one diagnosis, group deterministic code changes by file and purpose, and make the next operator action obvious enough that a human or Codex can apply/review the project-advancement changes directly from the document.
