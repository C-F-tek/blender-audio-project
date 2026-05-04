# Local AI Core/Tool Activation

This document defines the priority activation lane for IA-Carmine repository work.

It is a policy and tool-visibility document, not a command catalog. Current executable commands live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

## Intent

The project should use local AI core/tools to produce concrete artifacts that can be validated, reviewed and iterated on.

The activation lane is app-agnostic. It is not Blender-specific, audio-specific or provider-specific. Blender/audio remain downstream domains that consume the same repository workflow contracts.

## Primary entrypoint

The primary operator entrypoint is the unified launcher:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

All activation profiles must be selected as launcher modes, profiles or flags.

The older core activation wrapper remains a supporting lane:

```text
Tools/workflow/run_local_ai_core_tool_activation.ps1
```

Use it only when a task explicitly targets that wrapper or when the unified launcher delegates to it. Do not document it as a parallel full-run entrypoint.

## Philosophy

```text
artifact-first
validator-first
manual-review-only
provider execution explicit-only
app-agnostic core before domain runtime
macro patch as draft/spec, never automatic apply
manifest-first visibility
launcher-first execution
```

The core/tool workflow should produce real artifacts:

```text
selected chunks
selected-chunks evidence
context pack
agent state packet
memory inventory / memory handoff when enabled
enrichment plan
adapter manifest
repository proposals
NPU knowledge-broker packet
GitHub evidence bundle
optional macro patch draft specs
```

These artifacts give the repo concrete material for review and tests instead of relying only on chat summaries.

## Tool visibility map

| Area | Tool/script | Status |
|---|---|---|
| Unified launcher | `Tools/workflow/run_unified_local_ai_refactor.ps1` | Canonical entrypoint. |
| Core activation wrapper | `Tools/workflow/run_local_ai_core_tool_activation.ps1` | Supporting/legacy lane only. |
| Semantic chunks | `Tools/npu/build_semantic_code_chunks.py` | Supporting tool, provider-free, launcher `chunks` phase. |
| Context pack | `Tools/ai/build_ai_context_pack.py` | Supporting tool, provider-free, launcher `context_pack` phase. |
| Agent state packet | `Tools/ai/build_agent_state_packet.py` | Supporting tool, optional SQLite memory, launcher `agent_state` phase. |
| Memory inventory | `Tools/ai/build_agent_memory_inventory.py` | Supporting visibility tool. |
| Agent memory policy | `Tools/ai/agent_memory_policy.py` | Internal deterministic policy module. |
| Agent memory routing | `Tools/ai/agent_memory_routing_policy.py` | Internal routing policy module. |
| Runtime SQLite memory | `Tools/ai/agent_runtime_sqlite_memory.py` | Internal/local runtime helper. |
| Tool inventory | `Tools/ai/build_agent_agnostic_tool_inventory.py` | Supporting toolbox visibility tool. |
| Code interpreter report | `Tools/ai/build_code_interpreter_report.py` | Supporting capability report. |
| Refactor duplication audit | `Tools/ai/build_refactor_duplication_audit.py` | Supporting audit tool. |
| Official adapter | `Tools/workflow/run_local_ai_task_via_pipeline.ps1` | Launcher/internal adapter lane. |
| Ollama advisory packet | `Tools/workflow/run_post_validation_ai_packet.ps1` | Explicit advisory implementation lane. |
| Multistep provider | `Tools/workflow/run_parallel_ai_provider_multistep.ps1` | Explicit provider/probe implementation lane. |
| NPU knowledge broker | `Tools/npu/build_npu_knowledge_broker_packet.py` | Supporting packet builder. |
| Evidence bundle | `Tools/ai/build_github_evidence_bundle.py` | Compact GitHub evidence builder. |

Forgotten-script audit:

```text
docs/LOCAL_AI_TASKS/forgotten-scripts-documentation-audit.md
```

## Provider execution

Provider execution is opt-in only through the unified launcher modes/flags or a focused provider wrapper explicitly scoped by the operator.

Expected provider roles:

```text
Ollama/GPU = primary advisory provider behind quality gate
NPU/OpenVINO = probe / guardrail / decode diagnostic / knowledge broker
OpenVINO GPU != primary lane
```

The provider path must remain advisory/report-only and must preserve:

```text
provider_execution_performed is explicit and visible
patch_application_performed=false unless a separately reviewed patch-apply command is authorized
manual_review_only for proposals and patch specs
```

## Macro patch lane

Macro patch mode is allowed only as draft/spec generation and must route through the unified launcher when used as part of a broad activation flow.

Macro patch mode may produce:

```text
output/patch_specs/local_ai_core_tool_activation_patch_specs_manifest.json
output/patch_specs/local_ai_core_tool_activation_*.json
```

It must not:

```text
apply patches
queue patch specs for automatic execution
merge branches
rewrite source files directly
change Blender runtime
edit full analysis JSON
commit SQLite DB files
```

Macro patch promotion remains a separate reviewed step.

## Documentation patch-plan lane

For documentation-only manual-review patch plans, use the task-scoped review lane and preserve launcher-first visibility when part of broad local-AI work.

Relevant task/wrapper:

```text
docs/LOCAL_AI_TASKS/apply-agent-review-doc-patch-plan.md
Tools/validation/run_agent_review_patch_plan_full_validation.py
```

Expected compact evidence:

```text
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.md
```

This lane is for already-generated review/evidence reports. It must remain:

```text
documentation-only
provider-free
patch-runner-free
manual-review-only
task-scoped evidence only
```

## AI workload report quality gate

The local AI core/tool activation lane must use the AI workload report quality gate after provider/probe reports exist and before generated workload reports influence advisory packets.

Expected routing semantics:

```text
Ollama/GPU usable_text -> primary advisory context
NPU/OpenVINO unusable_output -> excluded from advisory context
```

The quality gate remains report-only. It must not execute providers, promote NPU to advisory, introduce OpenVINO GPU as primary lane or apply patches.

Broad activation runs must expose quality-gate state in the unified launcher manifest.

## Expected outputs

Unified launcher output:

```text
output/local_ai_runs/<timestamp>_<mode>_unified/pipeline/unified_local_ai_refactor_manifest.json
```

Activation-supporting outputs may include:

```text
output/local_ai_runs/<timestamp>_local_ai_core_tool_activation/
output/ai_pipeline/local_ai_core_tool_activation_summary.json
output/ai_pipeline/local_ai_core_tool_activation_summary.md
output/ai_pipeline/local_ai_core_tool_activation_npu_knowledge_broker_packet.json
output/ai_pipeline/local_ai_core_tool_activation_npu_knowledge_broker_packet.md
output/validation/local_ai_core_tool_activation_adapter_manifest_contract.json
output/validation/local_ai_core_tool_activation_npu_knowledge_broker_packet_contract.json
output/validation/local_ai_core_tool_activation_github_evidence_bundle.json
docs/LOCAL_VALIDATION_EVIDENCE/local_ai_core_tool_activation_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/local_ai_core_tool_activation_evidence.md
```

If macro patch drafts are generated, also expect draft-only patch specs under:

```text
output/patch_specs/
```

For the documentation patch-plan lane, expected tracked evidence is instead:

```text
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.md
```

## Validation ownership

Broad activation validation uses the unified launcher.

Focused validator commands belong in `Tools/validation/README.md` and should be used only when debugging or validating a specific validator/report contract.

The broad-run acceptance signal is the launcher manifest, especially:

```text
phase_status
phase_reports
context_files
report_files
provider_execution_requested
workload_quality_routing_ok
quality_gate_passed
patch_specs_requested
patch_application_performed
errors
warnings
```

## Commit policy

Allowed tracked outputs:

```text
docs/LOCAL_VALIDATION_EVIDENCE/local_ai_core_tool_activation_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/local_ai_core_tool_activation_evidence.md
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/agent_review_doc_patch_plan_evidence.md
```

Do not commit:

```text
output/**
output/patch_specs/**
indexAI/agent_memory/**
SQLite DB files
raw provider outputs
full analysis JSON files
manual generated-index edits
```

## Guardrails

The activation lane must remain:

```text
app-agnostic
report-only by default
provider-free by default
manual-review-only for macro patch
destructive-operation-free
manifest-first
launcher-first
```

The documentation patch-plan lane inherits the same guardrails and additionally stays task-scoped to the explicit patch-plan evidence bundle.

## Patch-plan contract terms

Keep these contract terms visible in docs and reports:

```text
provider_execution_performed
patch_application_performed
manual_review_only
code_contract_drift
docs_contract_drift
```

If a report uses different terms, document the mapping or add a compatibility field instead of silently changing meaning.
