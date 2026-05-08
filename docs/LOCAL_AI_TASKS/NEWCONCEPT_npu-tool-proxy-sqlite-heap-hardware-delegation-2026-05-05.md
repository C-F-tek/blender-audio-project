# NEWCONCEPT_npu-tool-proxy-sqlite-heap-hardware-delegation-2026-05-05

Status: historical / concept reference.

This file is retained for older NPU/tool-proxy/SQLite-heap/hardware-delegation design context. It is not the current runtime architecture contract and must not be treated as implemented behavior.

Current implementation and architecture references:

```text
docs/MAIN_RUNTIME_ARCHITECTURE.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_mesh.py
Tools/ai/agent_runtime_tool_broker.py
Tools/ai/provider_runtime_heap.py
```

Current rule:

```text
Concept docs do not authorize new runtime owners.
Reuse current broker, runtime heap, provider mesh and validator owners first.
```

The old split folder for this document is legacy. New Markdown splits must use the `name.md/part-001.md` layout.

Use the legacy parts only for design comparison.
