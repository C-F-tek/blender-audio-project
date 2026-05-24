# Tools/validation context index

Use this index to find the nearest validation context before adding or changing checks.

| Family | Context file |
| --- | --- |
| Agent context and RAG context packs | `Tools/validation/agent_context/TOOL_CONTEXT.md` |
| Agent memory | `Tools/validation/agent_memory/TOOL_CONTEXT.md` |
| Agent review | `Tools/validation/agent_review/TOOL_CONTEXT.md` |
| AI workload | `Tools/validation/ai_workload/TOOL_CONTEXT.md` |
| Code product | `Tools/validation/code_product/TOOL_CONTEXT.md` |
| Deterministic recommendations | `Tools/validation/deterministic_recommendations/TOOL_CONTEXT.md` |
| Docs hygiene | `Tools/validation/docs_hygiene/TOOL_CONTEXT.md` |
| Generated artifacts | `Tools/validation/generated_artifacts/TOOL_CONTEXT.md` |
| Generated patch specs | `Tools/validation/generated_patch_specs/TOOL_CONTEXT.md` |
| Heap exchange | `Tools/validation/heap_exchange/TOOL_CONTEXT.md` |
| Heap final proposals | see `docs/CONTEXT_COVERAGE_STATUS.md` (`stub-missing`) |
| Heap provider | `Tools/validation/heap_provider/TOOL_CONTEXT.md` |
| Heap runtime | `Tools/validation/heap_runtime/TOOL_CONTEXT.md` |
| Legacy Blender | `Tools/validation/legacy_blender/TOOL_CONTEXT.md` |
| Patch product | `Tools/validation/patch_product/TOOL_CONTEXT.md` |
| Pipeline | `Tools/validation/pipeline/TOOL_CONTEXT.md` |
| Provider mesh | `Tools/validation/provider_mesh/TOOL_CONTEXT.md` |
| Real product | `Tools/validation/real_product/TOOL_CONTEXT.md` |
| Repository product | `Tools/validation/repository_product/TOOL_CONTEXT.md` |
| Runtime tool | `Tools/validation/runtime_tool/TOOL_CONTEXT.md` |
| Runtime universe | `Tools/validation/runtime_universe/TOOL_CONTEXT.md` |
| Schema repair | `Tools/validation/schema_repair/TOOL_CONTEXT.md` |
| Workflow run | `Tools/validation/workflow_run/TOOL_CONTEXT.md` |

Canonical command surface:

```powershell
python -m Tools.validation <tool> [args...]
```

Public validation tool names are registered in `Tools/validation/dispatch.py`.

A validation report proves only the checked contract. It does not replace current source inspection.

## AI workload report quality gate

- Validator: `Tools/validation/ai_workload/check_ai_workload_report_quality.py`.
- Dispatch/tool surface: `ai_workload_report_quality`.
- Contract doc: `docs/AI_WORKLOAD_REPORT_QUALITY_GATE.md`.
- Purpose: keep metadata-only or empty provider reports from being promoted as useful workload evidence.
- Required classifier examples include `usable_text_lanes_only_for_advisory_context` and `npu_review_metadata`.
- Provider-quality reports stay report-only evidence with `provider_execution_performed=false` unless a broker/provider workload contract proves execution.
