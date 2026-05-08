# Local AI Core/Tool Activation

## Purpose

Policy and visibility guide for IA-Carmine core/tool activation.

This is not a command catalog. Current command and owner sources:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
```

## Intent

Local AI core/tools must produce concrete artifacts that can be validated, reviewed and iterated on.

The activation lane is app-agnostic. Blender/audio are downstream application domains, not the activation boundary.

## Primary entrypoint

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

All activation profiles must be selected as launcher modes, profiles or flags.

The older wrapper remains supporting only:

```text
Tools/workflow/run_local_ai_core_tool_activation.ps1
```

Use it only when a task explicitly targets that wrapper or when the unified launcher delegates to it. Do not document it as a parallel full-run entrypoint.

## Full-run activation doctrine

Core/tool activation is part of **TUTTO SU TUTTO** when selected by `Full0To10` or explicit launcher modes.

Activation artifacts are not enough by themselves. Production handoff must include the relevant state surfaces:

```text
launcher manifest
phase_status / phase_reports
runtime tool usage telemetry
runtime/hardware capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
file-line-limit report when maintainability is in scope
generated artifact path policy when evidence/bundle names are staged or pushed
```

Telemetry explains whether activation lanes were:

```text
executed
failed
blocked
degraded
intentionally disabled
unavailable
planned-only
```

Telemetry accompanies evidence, patch specs and patch plans; it does not replace them.

## Philosophy

```text
artifact-first
validator-first
manual-review-only
provider execution explicit through launcher/full-run selection
app-agnostic core before domain runtime
macro patch as draft/spec, never automatic apply
manifest-first visibility
launcher-first execution
telemetry/capability handoff when tools execute
small-file maintainability visibility
product/evidence/readiness output over chat-only summaries
```

## Tool ownership

Do not duplicate tool owners here. Use:

```text
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
Tools/ai/README.md
Tools/workflow/README.md
Tools/validation/README.md
```

Core owners include:

```text
run_unified_local_ai_refactor.ps1
run_agent_review_full_toolbox_decision_loop.py
py_engine.py / py_mesh.py / py_product.py / py_support.py
agent_runtime_tool_broker.py
build_ai_peer_exchange_packet.py
run_gpu0_peer_companion_worker.py
build_runtime_tool_usage_telemetry.py
build_full_toolbox_run_telemetry_summary.py
build_shared_toolbox_ai_to_ai_bundle.py
build_task_patch_suggestion_report.py
apply_patch_suggestion_bundle.py
prepare_review_pr.py
```

## Provider execution

Provider execution is selected through the unified launcher/full-run/provider flags, not through ad-hoc scripts.

Expected roles:

```text
GPU1/Ollama/RTX 5080 = primary advisory planner/worker behind quality gate
GPU0/OpenVINO = companion peer worker and broker-visible tool-request producer
NPU/OpenVINO = non-blocking micro-fast task assistant / diagnostic / lightweight tool-support lane
deterministic scripts = heavy audit and validation authority
```

Provider path must preserve:

```text
provider-capable runners prefer IA_CARMINE_PYTHON / .venv before system python
provider_execution_performed is explicit and visible
provider diagnostics and degradation state flow into telemetry/bundle surfaces
patch_application_performed=false unless a separately reviewed patch-apply command is authorized
manual_review_only for proposals and patch specs
```

Effective-use, quality-product, bridge/readiness and capability artifacts must not be treated as provider runtime proof when their safety flags say `provider_execution_performed=false`.

## Macro patch and patch suggestion lanes

Macro patch and patch suggestion outputs are review material by default.

They must not:

```text
apply patches automatically
queue patch specs for automatic execution
merge branches
rewrite source files directly
change Blender runtime
edit full analysis JSON
commit SQLite DB files
```

Patch suggestion dry-run/apply owner:

```text
Tools/ai/apply_patch_suggestion_bundle.py
```

Review PR preparation owner:

```text
Tools/ai/prepare_review_pr.py
```

Current limitation:

```text
ReviewPrIncludePath is explicit.
prepare_review_pr.py does not auto-discover include paths yet.
prepare_review_pr.py does not create draft PRs yet.
```

## AI workload report quality gate

Provider/probe reports must pass workload quality routing before generated workload reports influence advisory packets.

Expected semantics:

```text
usable provider text -> advisory context
unusable output -> excluded from advisory context
```

Quality gate is report-only. It must not execute providers, promote NPU to advisory, introduce OpenVINO GPU as primary lane or apply patches.

## Expected output classes

Do not list every filename here; use the data-flow and script census maps for current surfaces.

Output classes:

```text
manifest and phase reports
context/chunk/agent-state artifacts
provider/peer/broker artifacts
runtime telemetry and capability artifacts
full toolbox summary and AI-to-AI bundle
patch suggestion product and apply reports
review PR prepare reports
compact GitHub evidence under docs/LOCAL_VALIDATION_EVIDENCE
```

Do not commit:

```text
output/**
output/patch_specs/** unless explicitly promoted as reviewed evidence
indexAI/agent_memory/**
SQLite DB files
raw provider outputs
full analysis JSON files
manual generated-index edits
```

## Validation ownership

Broad activation validation uses the unified launcher.

Focused validation selection lives in:

```text
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

Broad-run acceptance signal is launcher manifest plus telemetry/capability handoff surfaces, especially:

```text
phase_status
phase_reports
provider_execution_requested
workload_quality_routing_ok
quality_gate_passed
patch_specs_requested
patch_application_performed
runtime tool usage telemetry
runtime/hardware capability manifest
file-line-limit report when maintainability is in scope
full toolbox telemetry summary
errors
warnings
```

## Guardrails

The activation lane must remain:

```text
app-agnostic
report-only by default
provider execution only when selected through launcher/full-run semantics
manual-review-only for patch material
destructive-operation-free
manifest-first
launcher-first
telemetry/capability-visible when operational tools execute
small-file-policy visible when maintainability is in scope
```

Keep these terms stable in reports and docs:

```text
provider_execution_performed
patch_application_performed
manual_review_only
code_contract_drift
docs_contract_drift
runtime_tool_usage_telemetry
runtime_or_hardware_capability_manifest
file_line_limit_report
full_toolbox_run_telemetry_summary
```
