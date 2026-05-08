# Script census and validation flow — 2026-05-07

Status: active code-driven navigation map  
Scope: IA-Carmine script families, app flow, run variants, validation cycles and smoke strategy.

This document prevents operator/agent disorientation. It starts from source-code behavior and routes work through the correct script family.

## First rule

The normal operator does not start from random scripts.

Canonical entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Canonical runbook:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Current code-derived behavior map:

```text
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
```

## App flow: Markdown to product review

Current intended flow:

```text
Task Markdown input
-> unified launcher
-> manifest and phase reports
-> deterministic foundation
-> provider mesh when selected
-> peer exchange when provider report exists
-> telemetry/capability/evidence bundle
-> patch suggestion product report when selected
-> deterministic apply report when selected
-> product separation validator when review PR/apply path is selected
-> explicit include-path review PR preparation when selected
```

Current implementation limit:

```text
Review PR staging requires explicit ReviewPrIncludePath.
Draft PR creation is not implemented by prepare_review_pr.py yet.
```

## Run variants

| Variant | Use | Key flags | Provider expected |
|---|---|---|---|
| Isolated smoke | Check launcher plumbing only. | `-Mode smoke -NoStrictRealRunActivation -Prod -NoExecutionTail` | No |
| Phase diagnostic | Isolate one mode. | `-Mode md/json/python/... -NoStrictRealRunActivation` | Only for provider modes |
| Full product run | Real TUTTO SU TUTTO run. | `-Full0To10 -RunIntensity quick/balanced/deep/custom` | Yes unless disabled/degraded |
| Light evidence run | Fast evidence/profile. | `-LightFull0To10` | No |
| Patch suggestion dry-run | Inspect applicable suggestions. | `apply_patch_suggestion_bundle.py` without `--apply` | No |
| Deterministic apply | Apply deterministic operations on review branch. | `--apply` or launcher review apply flag | No |
| Review PR preparation | Commit/push/create PR for reviewed paths. | `-PrepareReviewPr -ReviewPrIncludePath ...` | No direct provider requirement |
| Reset plan | Plan cleanup only. | reset mode without apply confirmation | No |

## No-strict diagnostic template

Use this for single-mode diagnostics:

```powershell
$Stamp = "debug_<mode>_$(Get-Date -Format 'yyyyMMdd-HHmmss')"
$Task = ".\docs\LOCAL_AI_TASKS\pr206-patch-suggestion-product-full-run-2026-05-07.md"

powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -RepoRoot . `
  -Mode <mode> `
  -TaskFile $Task `
  -Stamp $Stamp `
  -SkipGitSync `
  -NoBranch `
  -AllowDirty `
  -NoStrictRealRunActivation `
  -Prod `
  -NoExecutionTail
```

If `run_agent_gpu*`, `run_npu*`, `run_agent_review_full_toolbox*` or `ollama.exe runner` appears during an isolated non-provider diagnostic, the command is wrong or strict activation was not disabled.

## Script family census

### Workflow entrypoints

| Script | Role | Operator status |
|---|---|---|
| `Tools/workflow/run_unified_local_ai_refactor.ps1` | Canonical launcher. | Primary entrypoint. |
| `Tools/workflow/run_agent_review_full_toolbox_decision_loop.py` | Python control entrypoint for full toolbox engine. | Launcher/internal advanced use. |
| `Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1` | Thin PowerShell wrapper for the Python engine. | Supporting wrapper. |
| `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_engine.py` | Static foundation and phase sequence. | Internal engine. |
| `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_mesh.py` | GPU1/GPU0/NPU mesh, heap, broker, peer exchange. | Internal engine. |
| `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_product.py` | Decision loop, bundle, telemetry, final product reports. | Internal engine. |
| `Tools/workflow/run_agent_review_full_toolbox_decision_loop/py_support.py` | Shared path/execution helpers. | Internal helper. |
| `Tools/workflow/run_unified_light_full0to10_profile.ps1` | Evidence-only profile dispatcher. | Launcher-selected/supporting. |
| `Tools/workflow/run_full0to10_light_evidence_only.ps1` | Light evidence report. | Supporting. |
| `Tools/workflow/run_local_ai_task_via_pipeline.ps1` | Official adapter lane. | Launcher-selected/supporting. |
| `Tools/workflow/run_post_validation_ai_packet.ps1` | Post-validation advisory packet lane. | Launcher-selected/supporting. |
| `Tools/workflow/run_parallel_ai_provider_multistep.ps1` | Multistep provider workflow. | Launcher-selected/supporting. |

### AI orchestration and provider scripts

| Script family | Role |
|---|---|
| `run_agent_gpu_npu_parallel_orchestrator.py` | GPU1 primary provider orchestration with GPU0/NPU support lanes. |
| `run_agent_gpu_deep_planning_supervised.py` | GPU advisory planner called by provider orchestrator. |
| `run_gpu0_peer_companion_worker.py` | GPU0 peer response and tool request producer. |
| `run_npu_gpu_deep_review_auditor.py` | NPU semantic/auditor or micro peer support when explicitly selected. |
| `build_ai_peer_exchange_packet.py` | GPU1/GPU0/NPU exchange packet and summary builder. |
| `agent_runtime_tool_broker.py` | Broker-controlled execution of provider tool requests. |
| `provider_runtime_heap*.py` | Runtime heap/event/snapshot/live-signal reports. |
| `check_local_resource_lanes.py` | Provider/resource lane probe. |
| `run_local_provider_probe.py` | Local provider probe. |

### Deterministic foundation scripts

| Script family | Role |
|---|---|
| `build_repository_consistency_map.py` | Repository consistency evidence. |
| `build_code_interpreter_report.py` | Static code/interpreter style report. |
| `build_agent_review_evidence_sufficiency.py` | Evidence sufficiency report. |
| `run_megalithic_repo_review.py` | Broad repo review signal builder. |
| `refine_megalithic_review_signals.py` | Refines broad review/proposal signals. |
| `build_deterministic_recommendations.py` | Deterministic recommendation recovery. |
| `build_agent_review_patch_plan.py` | Patch plan builder. |
| `build_openvino_hardware_governance_report.py` | Hardware/provider governance report. |

### Context, memory and index scripts

| Script family | Role |
|---|---|
| `build_ai_context_pack.py` | Context pack builder. |
| `select_semantic_code_chunks.py` | Semantic chunk selector. |
| `build_agent_state_packet.py` | Agent state packet. |
| `agent_state.py` | Agent state implementation. |
| `review_agent_memory.py` | Memory review. |
| `agent_runtime_sqlite_memory.py` | Runtime SQLite memory helper. |
| `agent_memory_routing_policy.py` | Memory routing policy report. |

SQLite outputs are local runtime state and must not be committed.

### Patch suggestion and review PR scripts

| Script | Role |
|---|---|
| `Tools/ai/build_task_patch_suggestion_report.py` | Task-scoped patch suggestion report. |
| `Tools/ai/apply_patch_suggestion_bundle.py` | CLI wrapper for deterministic patch suggestion dry-run/apply. |
| `Tools/ai/patch_suggestion_bundle/cli.py` | Discovery, product separation and deterministic operation apply implementation. |
| `Tools/ai/patch_suggestion_bundle/common.py` | Shared operation model and reusable repo/report path normalization. |
| `Tools/ai/patch_suggestion_bundle/product.py` | Product/supplemental classification with published-vs-total review counts. |
| `Tools/validation/run_patch_suggestion_bundle_apply_smoke.py` | Smoke for dry/apply behavior in temp repo. |
| `Tools/validation/run_full0to10_product_pr_chain_smoke.py` | End-to-end product PR chain smoke plus real launcher workflow trace. |
| `Tools/validation/check_patch_suggestion_product_separation.py` | Report-only validation of product/supplemental separation. |
| `Tools/ai/prepare_review_pr.py` | Explicit include-path staging, commit, optional push and PR creation. |

### Validation and smoke scripts

| Script family | Role |
|---|---|
| `check_python_syntax.py` | Python syntax validation. |
| `check_validation_report_contract.py` | JSON/report contract validation. |
| `build_script_inventory.py` | Script inventory and CSV surfaces. |
| `build_markdown_inventory.py` | Markdown inventory. |
| `check_docs_links.py` | Documentation link validation. |
| `check_file_line_limits.py` | Report-only line limit check. |
| `run_repository_consistency_map_smoke.py` | Repository consistency smoke. |
| `run_gpu_planner_json_contract_smoke.py` | GPU planner contract smoke. |
| `run_deterministic_recommendation_synthesizer_smoke.py` | Deterministic recommendation smoke. |
| `run_agent_review_decision_loop_smoke.py` | Decision loop smoke. |
| `run_agent_runtime_tool_broker_smoke.py` | Broker smoke. |
| `check_ai_peer_exchange_contract.py` | Peer exchange contract validation. |
| `check_provider_evidence_contract.py` | Provider evidence contract validation. |

## Validation cycles

### Cycle A: docs-only change

```text
docs link validation
git diff --check
file-line-limit report when scope touches MD policy
```

No provider execution is required.

### Cycle B: Python/script change

```text
python -m py_compile for touched Python files
check_python_syntax.py for broad syntax
relevant focused smoke
git diff --check
line count for touched scripts
```

### Cycle C: launcher or workflow change

```text
PowerShell parser check
no-strict single-mode smoke
manifest inspection
contract validation
then one real Full0To10 or LightFull0To10 run depending on intended behavior
```

### Cycle D: provider mesh change

```text
provider-capable Python preflight
local resource lane probe
GPU planner contract smoke
provider evidence contract
peer exchange contract
runtime heap/broker telemetry inspection
```

### Cycle E: patch suggestion/review PR change

```text
patch suggestion apply smoke
Full0To10 product PR chain smoke with launcher trace
product separation validator
dry-run by Stamp
explicit include-path review PR preparation smoke
check generated review_pr_prepare report
```

## Output ownership

Do not commit raw runtime output:

```text
output/**
*.db
*.sqlite
*.sqlite3
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
```

Commit only compact documentation, source changes and allowed compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE` when useful and explicitly selected.

## When uncertain

Read in this order:

```text
source script
code-derived-ai-toolchain-map-2026-05-07.md
this document
unified-local-ai-refactor-launcher.md
UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
relevant package README
```

Do not infer active behavior from historical handoff text.
