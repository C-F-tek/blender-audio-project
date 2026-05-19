# Tools/npu context

## Role

`Tools/npu` owns NPU/provider-side support packages used by IA-Carmine for local provider context, Blender/audio context packets, code/manual indexing, NPU review and guardrail services.

Canonical invocation:

```powershell
python -m Tools.npu <tool> [tool args...]
```

The source of truth for public NPU tools is `Tools/npu/dispatch.py`.

## Main families

### Context builders

Use these to build structured input packets for provider lanes, not to directly patch source files.

Representative tools:

```text
build_music_context
music_context
build_blender_manual_context
build_npu_code_context
build_project_ai_index
project_ai_index
build_semantic_code_chunks
```

Expected outputs include manifests, chunks, summaries and context files. They are runtime/context artifacts unless explicitly promoted as documentation.

### Knowledge broker and service packets

Use these when NPU/provider lanes need compact packets rather than raw repository scans.

Representative tools:

```text
build_npu_knowledge_broker_packet
npu_knowledge_broker_packet
build_ai_service_packet
build_provider_result_report
build_runtime_output_manifest
```

These tools should reduce context pressure and make provider output auditable. They should not invent source targets.

### NPU review and guardrails

Use these to audit provider output, generated artifacts, placeholder content, invented paths and source-write claims.

Representative tools:

```text
npu_guardrail
npu_guardrail_service
run_npu_review
npu_review_runner
run_npu_artifact_reviewer
```

The NPU lane is a sampled auditor/guardrail lane, not the primary planner. It should reject false claims, placeholder patches and unsafe write assumptions.

### Dual AI / music pipeline

Use these for the Blender/audio-reactive local AI pipeline where music analysis, code context and provider outputs are combined into candidate scene or implementation artifacts.

Representative tools:

```text
run_dual_ai_pipeline
run_ollama_music_agent
```

Generated Blender or scene artifacts must be reviewed before use. Do not treat generated scripts as committed product unless they pass validation and are intentionally staged.

### PowerShell support

`run_npu_context` is a maintained PowerShell wrapper registered through the dispatcher. Use the dispatcher invocation instead of direct path execution when possible.

## Memory and output policy

- NPU outputs are evidence/context unless explicitly converted into reviewed code product.
- Do not commit raw generated runtime outputs, database files, render outputs or chunk caches.
- Keep `indexAI/code_chunks/**` and runtime chunk/cache directories out of Git unless a compact Git-trackable manifest is explicitly produced.
- Use the AI/validation dispatchers to validate NPU contracts rather than adding standalone validation scripts.

## Safe extension rules

- Add new NPU/provider functionality under `Tools/npu/provider_mesh/<family>/` when possible.
- Keep shared runtime helpers under `provider_mesh/_shared/` only when they are genuinely reused.
- Register public commands in `Tools/npu/dispatch.py`.
- Keep provider outputs structured as JSON/Markdown evidence with explicit guardrails.
