# Forgotten Scripts Documentation Audit

## Purpose

Identify repository scripts that appear operationally relevant but are not visible enough in current Markdown entrypoints.

This is a documentation/audit task only. It does not delete, rename, deprecate or execute scripts.

This file is not a command catalog. Current script-inventory commands live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/validation/README.md
```

## Source of this audit

GitHub code search found script files under these areas:

```text
Tools/workflow/
Tools/workflow/gui/
Tools/ai/
Tools/validation/
Tools/npu/
```

Follow-up searches for exact script names in `*.md` returned no obvious Markdown references for several tools. Those tools are therefore candidates for documentation triage.

## Classification policy

Every script candidate should be classified as exactly one:

| Status | Meaning | Action |
|---|---|---|
| `canonical-entrypoint` | User/operator should run it directly. | Only the unified launcher currently qualifies. |
| `launcher-internal` | Called by `run_unified_local_ai_refactor.ps1`. | Document under unified launcher internals. |
| `supporting-tool` | Useful focused tool, not primary. | Add to tool catalog. |
| `diagnostic-only` | Local diagnostic/probe/smoke script. | Document as explicit local-only diagnostic. |
| `gui-or-shell-helper` | Interactive UI/shell wrapper. | Document separately from headless launcher. |
| `legacy-superseded` | Replaced by unified launcher. | Mark historical/supporting; do not start from it. |
| `unsafe-or-write-capable` | Can push, write source, or mutate external state. | Document guardrails and require explicit approval. |
| `delete-candidate` | Appears obsolete after code/reference review. | Do not delete without explicit user approval. |

## Full-run visibility rule

A script is not fully documented when it is promoted into the full-run perimeter but lacks visible output surfaces.

If a script participates in `Full0To10`, broker execution, provider diagnostics, patch planning, evidence generation, registry building or AI-to-AI handoff, its documentation must identify at least one of:

```text
launcher mode or flag
manifest phase_status key
manifest phase_reports key
runtime telemetry surface
runtime capability manifest surface
full toolbox telemetry summary surface
shared AI-to-AI bundle surface
compact evidence output
```

Telemetry is a completeness accessory for evidence and patch plans. It does not replace them, but it must accompany promoted operational scripts so a future AI can distinguish executed, failed, blocked, degraded, disabled and planned-only states.

## Candidate group: workflow shell / GUI helpers

These were found in code search but not clearly referenced in current Markdown docs:

```text
Tools/workflow/workflow_shell.py
Tools/workflow/workflow_shell_with_push.py
Tools/workflow/workflow_debug.py
Tools/workflow/gui/workflow_gui_modern.py
Tools/workflow/gui/workflow_gui_with_push.py
```

Initial classification:

```text
workflow_shell.py                 gui-or-shell-helper
workflow_shell_with_push.py       unsafe-or-write-capable, gui-or-shell-helper
workflow_debug.py                 diagnostic-only
workflow_gui_modern.py            gui-or-shell-helper
workflow_gui_with_push.py         unsafe-or-write-capable, gui-or-shell-helper
```

Documentation action:

```text
Add or maintain a small shell/GUI helper catalog.
Clarify that the unified launcher remains the headless canonical entrypoint.
Any push-capable wrapper must require explicit user intent and must not be invoked by documentation examples as a default flow.
Push/write-capable helpers must not bypass manifest, telemetry, capability or git visibility surfaces.
```

## Candidate group: workflow context/domain helpers

```text
Tools/workflow/asset_inventory.py
Tools/workflow/scene_brief.py
Tools/workflow/artifact_consult.py
Tools/workflow/project_awareness.py
Tools/workflow/smart_ai_context.py
Tools/workflow/ai_runtime_diagnostics.py
```

Initial classification:

```text
asset_inventory.py        supporting-tool
scene_brief.py            supporting-tool, application-domain helper
artifact_consult.py       supporting-tool
project_awareness.py      supporting-tool
smart_ai_context.py       supporting-tool
ai_runtime_diagnostics.py diagnostic-only
```

Documentation action:

```text
Document in MODULE_MAP or workflow helper policy.
Do not promote them above the unified launcher.
Clarify which are application-domain helpers versus AI orchestration helpers.
Record outputs in manifest/context/report/telemetry surfaces if they become full-run lanes.
```

## Candidate group: GPU/NPU/orchestrator diagnostics

```text
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py
Tools/ai/run_npu_gpu_deep_review_auditor.py
Tools/validation/run_gpu_runner_provider_error_smoke.py
Tools/validation/run_orchestrator_direct_gpu_counter_smoke.py
Tools/validation/run_orchestrator_gpu_runtime_tool_routing_smoke.py
```

Initial classification:

```text
run_agent_gpu_npu_parallel_orchestrator.py            launcher-internal or legacy-superseded; verify before editing docs
run_npu_gpu_deep_review_auditor.py                   diagnostic-only
run_gpu_runner_provider_error_smoke.py               diagnostic-only
run_orchestrator_direct_gpu_counter_smoke.py         diagnostic-only
run_orchestrator_gpu_runtime_tool_routing_smoke.py   diagnostic-only
```

Documentation action:

```text
Document as explicit diagnostics/probes only.
Do not present them as replacement entrypoints for the unified launcher.
If the unified launcher calls them or supersedes them, state that relation directly.
If their reports feed telemetry or AI-to-AI bundle state, document the exact field/surface.
```

## Candidate group: memory, inventory and evidence helpers

```text
Tools/ai/build_agent_memory_inventory.py
Tools/ai/build_code_interpreter_report.py
Tools/ai/build_agent_agnostic_tool_inventory.py
Tools/ai/build_refactor_duplication_audit.py
Tools/ai/github_evidence_bundle_reports.py
```

Initial classification:

```text
build_agent_memory_inventory.py        supporting-tool, memory visibility
build_code_interpreter_report.py       supporting-tool, code-interpreter visibility
build_agent_agnostic_tool_inventory.py supporting-tool, toolbox visibility
build_refactor_duplication_audit.py    supporting-tool, refactor/documentation audit
github_evidence_bundle_reports.py      library/helper for evidence bundles
```

Documentation action:

```text
Add memory/toolbox/evidence helper catalog entries.
For libraries, document as internal helper modules rather than user commands.
If promoted to broker/full-run lanes, document runtime telemetry and capability-manifest surfaces.
```

## Candidate group: runtime/memory internals that must not be treated as missing

```text
Tools/ai/agent_runtime_sqlite_memory.py
Tools/ai/agent_memory_routing_policy.py
Tools/ai/agent_memory_policy.py
Tools/ai/agent_state.py
Tools/npu/ai_memory_context.py
```

Documentation action:

```text
Keep them connected to AI_MEMORY_POLICY, LOCAL_AI_TASKS/README and the unified launcher memory section.
Do not commit SQLite DBs generated by these tools.
```

## Candidate group: provider/runtime helper modules

```text
Tools/npu/ollama_runtime.py
Tools/npu/npu_runtime.py
Tools/npu/build_provider_result_report.py
Tools/npu/run_npu_review.py
Tools/npu/pipeline/config.py
Tools/npu/pipeline/prompts.py
Tools/npu/pipeline/providers.py
Tools/npu/pipeline/io_utils.py
Tools/npu/pipeline/validators.py
```

Documentation action:

```text
Link from Tools/npu/pipeline/README.md or MODULE_MAP.
Do not imply provider execution unless a command explicitly loads/runs a provider.
Metadata-only and validation-only paths must remain clearly separated from provider execution.
If provider/runtime helper outputs become part of the full-run handoff, document provider diagnostics and telemetry fields.
```

## Required next checks

On a local workstation, generate fresh script inventory through the unified launcher `python` phase or the focused validator command documented in `Tools/validation/README.md`.

Then compare inventory to docs and update:

```text
docs/MODULE_MAP.md
docs/WORKFLOW_HELPER_SCRIPTS_POLICY.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
Tools/validation/README.md
Tools/npu/pipeline/README.md
```

For scripts promoted into `Full0To10`, also verify:

```text
manifest visibility
telemetry/capability visibility
compact evidence visibility
AI-to-AI bundle inclusion or explicit exclusion
```

## Acceptance criteria

```text
No script deleted.
No script promoted to canonical entrypoint unless truly intended.
Push-capable wrappers documented as explicit-risk helpers.
Diagnostic/probe scripts separated from normal flow.
Internal helper libraries separated from executable commands.
Unified launcher remains primary local-AI entrypoint.
Forgotten scripts either indexed, marked internal, or queued for deletion review.
Full-run scripts expose manifest/report/telemetry/capability/evidence surfaces.
Telemetry accompanies full-run evidence and patch plans when operational scripts are involved.
```
