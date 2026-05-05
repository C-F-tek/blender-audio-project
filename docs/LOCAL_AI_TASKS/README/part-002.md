<!-- IA-CARMINE-MD-SPLIT: part -->
# README — parte 002 di 002

Sorgente indice: [`../README.md`](../README.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

## SQLite memory / context enrichment

SQLite-backed memory is an active local-AI enrichment capability, not a future placeholder.

Relevant files:

```text
Tools/ai/agent_state.py
Tools/ai/build_agent_state_packet.py
Tools/ai/review_agent_memory.py
Tools/ai/agent_memory_policy.py
Tools/npu/build_semantic_code_chunks.py
Tools/ai/build_ai_context_pack.py
docs/LOCAL_AI_TASKS/enrich-local-ai-memory-chunks-context-wrapper.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Default memory DB path used by the local flow:

```text
indexAI/agent_memory/agent_memory.sqlite
```

Policy:

```text
SQLite DB files are local/private runtime state.
Do not commit .sqlite/.db files.
Do not remove SQLite-memory references from docs unless the tools are actually removed from the repo.
If a referenced tool is missing, mark it optional/future or remove the reference immediately.
```

## Reset mode policy

Reset mode is for local generated artifacts, not source cleanup.

Default reset behavior:

```text
plan only
no deletion
writes local_ai_reset_plan_*.json/.md under output/validation
```

Deletion requires the explicit confirmation flags documented in the unified launcher runbook.

Reset may include memory/generated-index candidates only when explicitly requested.

## Local validation evidence policy

The local-machine validation contract lives at:

```text
docs/LOCAL_VALIDATION_EVIDENCE/LOCAL_MACHINE_VALIDATION.md
```

Use it whenever a run creates ignored local reports under `output/**` and needs a Git-trackable compact evidence handoff.

## Historical task files

Historical handoffs and generated evidence remain useful as past state, but must not become the first reading path unless explicitly referenced.

Rules:

```text
Do not promote historical PR handoffs back to active entrypoints.
Do not use generated evidence snapshots as canonical workflow docs.
Do not delete production evidence automatically; evidence pruning requires a separate explicit evidence-retention decision.
```

## Agent anti-laziness checklist

Before editing local-AI flow docs or wrappers, check these files explicitly:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1
Tools/workflow/run_local_ai_task_via_pipeline.ps1
Tools/workflow/run_post_validation_ai_packet.ps1
Tools/workflow/run_parallel_ai_provider_multistep.ps1
Tools/validation/check_ai_workload_report_quality.py
Tools/validation/build_markdown_inventory.py
Tools/validation/build_script_inventory.py
Tools/validation/check_docs_links.py
Tools/validation/check_validation_report_contract.py
Tools/ai/build_agent_state_packet.py
Tools/ai/agent_state.py
Tools/npu/build_semantic_code_chunks.py
Tools/ai/build_ai_context_pack.py
Tools/ai/agent_runtime_tool_broker.py
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
docs/LOCAL_AI_TASKS/tool-inventory-placement-audit-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-promotion-and-insertion-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/no-audio-media-output-guardrail-2026-05-05.md
docs/LOCAL_AI_TASKS/forgotten-scripts-documentation-audit.md
docs/LOCAL_AI_TASKS/enrich-local-ai-memory-chunks-context-wrapper.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

If a documented tool is not present, do not pretend it is available. Either remove the reference or mark it explicitly as optional/future with a stop condition.
